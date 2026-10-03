---
layout: post
title: "No API? No Problem: Browser Reverse-Engineering with CDP to Supercharge AI Agents"
date: 2026-10-03 09:00:00 +0100
categories: automation ai agents cdp playwright mcp browser reverse-engineering
tags: [cdp, playwright, mcp, ai-agents, browser-automation, reverse-engineering, sso, tunnels]
---

My AI agents read my mail, answer Teams messages, book my timesheets, verify deployments through an ERP web client on a Windows terminal server, and manage API keys in a SaaS portal. None of these systems expose an API I'm allowed to use.

They all have web UIs, though. And that turns out to be enough.

The trick is simple to state and messy to implement well: **treat the web app itself as the API.** Drive a real browser session through the Chrome DevTools Protocol (CDP), wrap it in MCP tools, and hand those tools to your agents. This post is about the patterns that make the difference between a toy demo and something that runs unattended for months.

## The Architecture: MCP as the Bridge

The layering I've settled on:

```
AI Agent ──> MCP Server (tools: "send message", "list mail", "book hours")
                │
                ▼
        Playwright / CDP client
                │
                ▼
        Real browser session (Edge/Chrome, logged in)
                │
                ▼
        The web app (the actual "API")
```

The agent never sees a browser. It sees clean, high-level tools: `teams_send_message`, `outlook_get_freebusy`, `navision_open_journal`. The browser automation lives entirely inside the MCP server.

This matters more than it sounds. If your agent has to reason about "click the third button in the ribbon, then wait for the spinner", it will do it wrong at 3 AM. If it can call `navision_post_timesheet(week=40)`, it does it right every time.

## Pattern 1: One Login, Months of Headless Operation

The first thing everyone asks: "Don't you have to log in constantly?" No — and solving this properly is the foundation of everything else.

- **Dedicated browser profile per target.** Each web app gets its own persistent profile directory. Cookies, session state, and (where the app supports it) "remember me" tokens survive restarts.
- **Owner-mode login exactly once.** For the initial login and every rare re-auth, the automation opens a *visible* browser window (WSLg in my case) on my desktop. I log in, the session persists to the profile, and the window closes. From then on, headless instances reuse that profile.
- **Silent renewal where possible.** Many SSO providers (Keycloak, Entra ID) support silent token renewal as long as the session cookie is alive. The bridge renews in the background; nobody notices.

The lesson: **the login is a one-time human event, not a recurring automation problem.** Design for it explicitly — a `login` tool that opens the owner window — instead of scattering credential handling through your code.

## Pattern 2: Remote Browsers over Throwaway Tunnels

The nastiest case: the app you need runs *on a terminal server*. You can't install Playwright there, and RDP screenshots into an LLM are slow, lossy and fragile.

The pattern that works:

1. Run an Edge/Chrome instance **on the terminal server** with `--remote-debugging-port=9222`.
2. Expose CDP through a **Cloudflare Quick Tunnel** (`cloudflared tunnel --url http://localhost:9222`). No firewall rules, no VPN, no static IP — you get a random `*.trycloudflare.com` URL.
3. Write that URL to a file that syncs to the machine where your agent runs (I use OneDrive: `tunnel-url.txt`). The CDP client reads it at connect time.
4. Put a **basic-auth injector** in front of the tunnel. A random public URL that speaks raw CDP is an remote-code-execution-as-a-service; don't ship that.

Yes, the tunnel URL rotates. That's a feature — it forces you to build the self-healing described below.

## Pattern 3: Extract What the LLM Needs, Not What Exists

Naive browser automation fails because it passes *pixels* or *raw HTML* to the model. Both are expensive and brittle. What works:

- **`innerText` over screenshots.** A page's visible text is cheap, deterministic, and usually all the agent needs to decide what to do.
- **ARIA labels over CSS selectors.** CSS classes get regenerated on every deploy. ARIA labels (`aria-label="Week view"`, grid cell labels) survive redesigns because they're the accessibility contract. My calendar automation reads busy slots from ARIA labels of the week view — it has survived two UI updates untouched.
- **Structured extraction at the bridge.** Parse tables, message lists, and attachments *inside* the MCP server; return JSON. The agent gets `"from": "...", "subject": "...", "unread": true` instead of a wall of DOM.
- **Trigger words, not full text, for classification calls.** When the agent needs a second opinion, send extracted keywords only — never paste the raw page into a model.

## Pattern 4: Self-Healing Bridges (This Is the Real Work)

Everything above breaks eventually. Tunnels rotate, sessions expire, the target deploys a redesign on a Friday. The difference between a demo and production is what happens next:

- **Health checks before every use.** Ping the CDP endpoint (or validate the session) before executing a tool call. Detect breakage *before* the agent does.
- **Reconnect from the source of truth.** If the tunnel URL changed, re-read the synced file. If the session died, reopen with the persistent profile. If that fails, surface a single actionable message to the human — "SSO login required" — with a `login` tool to fix it, instead of a stack trace.
- **Retry with suppression, not alert storms.** A flaky endpoint should not page you twelve times. Log suppressed retries (`notify_suppressed`), escalate only on state *changes* (broken → recovered always notifies; same-state re-notifies at most every few hours).
- **Fail safe, fail idempotent.** Cursor files and processed-markers for anything the agent harvests or books. A crashed run must never cause double-submission.

## Pattern 5: When Scraping Fails, Go Raw

Sometimes the UI is the wrong layer — too dynamic, too slow, or mid-redesign. The web UI is a *client* of an internal API, and that API is usually reachable with the same session cookies.

- Open the browser's dev tools once, watch the network tab, and note the GraphQL/REST endpoints the app actually calls.
- Replay them with the session token from your persistent profile — or better, reconstruct the **token refresh chain** yourself (for Keycloak: a single refresh-token request against the realm's token endpoint).
- Keep the UI path as fallback. Raw API for reads, UI for the writes you don't fully understand yet.

This hybrid saved one of my integrations entirely: the portal's SPA was rebuilt, all selectors died, and the raw GraphQL calls with a hand-rolled refresh chain kept working without any browser at all.

## The Boring Rules That Keep It Alive

A few things that sound obvious and still cost me debugging nights:

- **Never log secrets.** API keys, cookies, tokens — mask or omit. (Pro tip: if you ever paste a key into a chat with an agent, *the error message of the next failed call* will happily leak its hash. Logs are forever.)
- **One session per target, one target per session.** Multi-tenant apps (multiple Microsoft 365 tenants, multiple accounts) need *separate* browser profiles. Mixing tenants in one profile is how messages end up in the wrong place.
- **Read-only by default.** Destructive tools exist but stay behind explicit confirmation. The agent proposes; the human disposes — except for the workflows you've explicitly promoted to autonomous.
- **Verify the recipient before every send.** Contact-name fuzziness ("Top" vs "Tobi") is real. A message to the wrong chat is not retrievable.

## What This Buys You

Once the bridges exist, agents stop being chat toys and become operators:

- "What's on my calendar Thursday?" — answered from the actual calendar, not a guess.
- "Check the unread mail from last night and summarize anything important." — every morning, before I wake up.
- "Book this week's timesheets per our conventions." — prepared as copy-paste blocks with rounding rules applied.
- "Check the AI portal's new model announcements." — extracted from a UI whose only public interface is JavaScript.

The web app becomes just another tool in the agent's belt — same status as the shell or the filesystem.

## Limits & Etiquette

Be honest about the trade-offs: UI redesigns *will* break selectors (ARIA helps, doesn't immunize); you're dependent on session lifetimes you don't control; and this only ever runs against **accounts you own** — your own mail, your own tenant, your own portal logins. Automating *your* use of *your* accounts through *their* intended UI is one thing; scraping other people's systems is a different conversation entirely.

## Wrap-up

CDP-based browser automation is the pragmatic superpower for AI agents in a world where most useful software still ships without a usable API. The ingredients are unglamorous — persistent profiles, tunnels, ARIA selectors, retry logic — but together they turn "the web app" into a first-class tool surface. Start with one app you touch daily, build the bridge, and let your agents do the clicking.

If this sounds familiar from the MCP world: yes, this is exactly the "agent harness meets legacy reality" story. The browser was always the universal API. Now your agents know how to drive it.
