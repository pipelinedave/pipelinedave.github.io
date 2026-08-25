---
layout: post
title: "restgeld.: Daily Allowance Tracking Without the Frustration"
date: 2026-08-25 09:30:00 +0200
categories: projects devops self-hosting kubernetes
tags: [restgeld, golang, vue, pwa, k3s, kubernetes, personal-finance, open-source, devops]
---

Traditional budgeting apps have a fundamental flaw: **they demand bookkeeping where all you actually want is peace of mind.**

Who genuinely enjoys splitting a grocery receipt into 14 distinct categories—*groceries*, *household*, *pharmacy*, *entertainment*—only to be greeted on the 20th of the month by a glaring red progress bar and buyer's remorse? The inevitable outcome: after two weeks of meticulous ledger-keeping, you burn out and abandon the app.

That's why I built **[restgeld.](https://pipelinedave.github.io/restgeld/)**—a radically minimalist, mobile-first **Daily Allowance Tracker (PWA)** built on a simple philosophy: **Every day is a fresh start with a single, clear number.**

---

## The Name: A Bilingual Double Entendre

The name **restgeld.** works on two distinct levels:

* In **German**, *"Rest"* means *what's left / remaining* and *"Geld"* means *money*—literally your remaining spending money for the day.
* In **English**, *"Rest"* embodies *calm, tranquility, and peace of mind*. 

Combine the two, and you get the core ethos: you can **rest easy** knowing your daily **geld** is 100% guilt-free and fully allocated. No mental math at the checkout, no late-month panic.

---

## The Core Concept: One Number for the Here & Now

Instead of watching a monthly budget pool slowly evaporate into abstract anxiety, **restgeld.** takes your freely available pocket money (whatever remains after rent, utilities, fixed subscriptions, and savings targets) and splits it evenly across the days of your billing cycle.

$$\text{Daily Budget} = \frac{\text{Monthly Budget}}{\text{Days in Period}}$$

The magic lies in how it adapts to daily human reality:

1. **Spent less today?** The unused portion automatically flows into your savings cushion and increases your daily allowance for the remaining days.
2. **Had a bigger expense?** Going over doesn't trigger guilt trips or broken graphs—it gently redistributes the difference across the rest of the month.
3. **Zero-euro days?** Taking a "no-spend" day noticeably boosts your allowance for the rest of the week.

```text
Monthly Budget: 350 € (31 Days) ➔ Base: 11.29 € / day
2 Zero-Spend Days / Week ➔ True Active Budget: ~15.80 € / day 🔥
```

---

## Feature Highlights: Zero Friction in Daily Life

When designing **restgeld.**, the guiding principle was speed and real-world utility:

* ⚡ **2-Second Expense Logging:** Custom mobile numpad integration with decimal mode (`inputmode="decimal"`), real-time budget impact feedback, and one-tap quick-note chips for frequent purchases (*Coffee*, *Snack*, *Lunch*).
* 🔥 **Gamification & Spar-Streaks:** An animated flame badge, streak milestones, and a zero-euro day counter that turn mindful spending into a satisfying daily habit.
* 📱 **Offline-First PWA:** Zero mobile reception in a supermarket basement? An offline outbox queues your transactions and transparently syncs them as soon as connectivity returns.
* 🔮 **Month-End Projection:** At-a-glance forecasting that tells you exactly where you'll land by the end of the period based on your current spending velocity.
* 🔒 **100% Data Sovereignty:** No banking API integrations required, no third-party tracking, no forced cloud accounts. Full one-click CSV and JSON backup/restore built straight into settings.

---

## Under the Hood: Clean, Fast & Self-Hostable

No bloated client-side frameworks, no heavy backend middleware.

```text
┌──────────────────────────────────────────────────────────┐
│                      restgeld. Stack                     │
├─────────────────────────┬────────────────────────────────┤
│ Frontend                │ Vue 3 + TypeScript + Vite PWA  │
│ Backend API             │ Go 1.22 (net/http + lib/pq)    │
│ Database                │ PostgreSQL 16 (PVC)            │
│ Deployment              │ Vercel Preview, k3s & Docker   │
└─────────────────────────┴────────────────────────────────┘
```

* **Go REST Backend:** Compiles into a scratch container image with sub-millisecond response times and automated schema migrations via Go `embed.FS`.
* **Vue 3 Mobile PWA:** Minimalist OLED-dark aesthetic without heavy CSS frameworks, achieving instant load times and tested with Vitest and Playwright.
* **GitOps & Deployment Pipeline:** Dual setup leveraging automated **Vercel Preview Deployments** for pull requests alongside GitOps automation via **Flux CD** on my local k3s cluster (`restgeld.stillon.top`).

---

## Quickstart: Self-Host in Seconds

If you want to run your own private instance, you can spin it up with Docker Compose in seconds:

```bash
git clone https://github.com/pipelinedave/restgeld.git
cd restgeld
docker compose up -d
```

The app is immediately live at `http://localhost:3000` (or behind your favorite reverse proxy / Cloudflare tunnel).

---

## Explore the Project

* 🌐 **Landing Page & Interactive Calculator:** [pipelinedave.github.io/restgeld](https://pipelinedave.github.io/restgeld/)
* 💻 **GitHub Source Code:** [github.com/pipelinedave/restgeld](https://github.com/pipelinedave/restgeld)

Check it out, try the interactive calculator on the landing page, and let me know your thoughts!
