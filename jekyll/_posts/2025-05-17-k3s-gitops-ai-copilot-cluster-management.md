---
layout: post
title: "K3s, GitOps, and AI: My Copilot-Powered Cluster Management"
date: 2025-05-17 10:00:00 +0100
categories: kubernetes gitops flux copilot automation devops k3s
tags: [kubernetes, k3s, gitops, flux, copilot, ai, automation, devops, cluster-management]
---

Managing Kubernetes clusters, even a relatively streamlined one like k3s, can often feel like a juggling act. There are manifests to write, configurations to track, deployments to verify, and the ever-present challenge of keeping documentation in sync with reality. For a while now, I've been on a journey to refine my k3s cluster management, and I'm thrilled to share a setup that has truly transformed my workflow: a GitOps-centric approach supercharged by GitHub Copilot.

My entire cluster configuration lives in my `k3s-config` repository, which you can explore to see these principles in action.

## The Foundation: GitOps with FluxCD

At the heart of my strategy is a steadfast commitment to GitOps. For me, this means the `k3s-config` Git repository is the *single source of truth*. If it's not in the repo, it doesn't (or shouldn't) exist in the cluster. FluxCD is the diligent operator that makes this happen, continuously reconciling the state of my cluster with what's defined in the `main` branch.

This provides a solid baseline:

* **Version Control for Infrastructure**: Every change is a commit, auditable and revertible.
* **Consistency**: What you see in Git is what you get in the cluster.
* **Automation**: Flux handles the deployment pipeline automatically.

But even with this robust foundation, the manual effort of creating, updating, and documenting configurations can be significant. That's where my AI assistant steps in.

## The Supercharger: GitHub Copilot Joins the Fray

Integrating GitHub Copilot into my daily operations has been nothing short of a game-changer. It's not just about code completion; it's about having an intelligent partner that understands my specific context, patterns, and even my documentation needs.

Here’s how Copilot elevates my GitOps workflow:

### 1. Accelerated Development and Manifest Creation

Writing YAML can be tedious and error-prone. Copilot, armed with the context of my repository (including my `cluster-context.md` which outlines my specific conventions), significantly speeds this up.

* **Smart Manifest Generation**: Need a new Deployment, Service, or Ingress? Copilot can draft it based on a simple prompt, often correctly inferring details like application names and port numbers.
* **Adherence to Standards**: I have critical protection policies, like ensuring all PersistentVolumeClaims (PVCs) include the `kubernetes.io/pvc-protection` finalizer and that all Ingresses follow my `app-name.stillon.top` domain schema with `letsencrypt-prod` issuer. Copilot helps me remember and implement these by suggesting the correct snippets or even modifying existing manifests to include them.
* **Flux Kustomizations**: Creating the `Kustomization` resources in my `apps/` directory to tell Flux about new applications is also streamlined. Copilot knows the structure and can generate the necessary YAML quickly.

### 2. Living, Breathing Documentation

This is perhaps one of the most remarkable aspects. I've established an "Auto-Documentation Update" process where Copilot plays a key role. When I make significant changes or explicitly ask, Copilot helps me:

* **Update Application Lists**: It can scan my `apps/` and `apps-incomplete/` directories and update the "Fully Managed Applications" and "Partially Managed Applications" sections in my documentation.
* **Verify Repository Structure**: It helps ensure my documented repository structure matches reality.
* **Keep Key Scripts Documented**: New scripts in `scripts/` or changes to existing ones? Copilot assists in updating their descriptions.

This means my `docs/README.md` and the crucial `cluster-context.md` (which Copilot itself uses for context!) stay remarkably up-to-date. It’s like having a dedicated technical writer who’s also an expert on my system.

### 3. Intelligent Cluster Interaction via MCP Tools

Through Model Context Protocol (MCP) tools, Copilot can directly (but safely) interact with my cluster for verification and troubleshooting. Instead of me manually running a series of `kubectl` or `flux` commands, I can ask Copilot:

* "Are all pods running in the `choremane-prod` namespace?" (Uses `bb7_pods_list_in_namespace`)
* "What's the status of the `docspell` Kustomization in Flux?" (Uses `bb7_get_kubernetes_resources`)
* "Show me the recent logs for the `linkding` pod." (Uses `bb7_pods_log`)

If something seems off, Copilot can even suggest reconciliation commands or help pinpoint issues by analyzing resource statuses.

### 4. Guardian of Best Practices

My workflow has specific manual steps, like creating namespaces with `kubectl create namespace <namespace>` *before* Flux tries to deploy to them (a crucial step to protect PVCs). Copilot consistently reminds me of these nuances. Similarly, when handling sensitive data, it guides me through the SealedSecrets workflow: create locally, use `kubeseal`, commit the sealed version, and delete the original.

## A Peek Inside My `k3s-config` Repository

My repository structure is designed to support this workflow:

* `kustomize/` and `kustomize-incomplete/`: Contain the actual Kubernetes manifests.
* `apps/` and `apps-incomplete/`: House the Flux Kustomization CRDs that point to the manifest directories.
* `flux-system/`: Holds the Flux bootstrap configuration.
* `docs/`: The comprehensive documentation hub, co-maintained by me and Copilot.
* `scripts/`: Utility scripts, often for tasks that bridge manual steps and GitOps.

This clear separation of concerns makes it easy for both humans and Copilot to navigate and understand the configuration.

## The Payoff: Tangible Benefits

Adopting this Copilot-enhanced GitOps model has yielded significant advantages:

* **Increased Speed**: Repetitive tasks are automated or significantly sped up.
* **Improved Consistency**: Adherence to my standards is much higher.
* **Reduced Errors**: Fewer typos or forgotten critical configurations in my YAML.
* **Truly Up-to-Date Documentation**: This alone is a massive win.
* **Empowered Me**: Complex Kubernetes operations become more accessible with an AI assistant ready to guide and explain.
* **Enhanced Learning**: Copilot often shows me efficient ways to achieve tasks or reminds me of commands and configurations, acting as an interactive learning tool.

## Looking Ahead

My journey with k3s, GitOps, Flux, and now GitHub Copilot has been incredibly rewarding. It feels like I'm at the forefront of a new era in operations, where AI doesn't just assist with code but becomes an integral part of managing complex systems. The `k3s-config` repository is a living testament to this synergy.

If you're managing Kubernetes, I highly encourage you to explore how a GitOps foundation, coupled with the intelligence of tools like GitHub Copilot, can revolutionize your workflows. It certainly has for me!
