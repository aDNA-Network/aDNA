---
type: dashboard
name: "Project Home"
tags: [dashboard, homepage]
cssclasses: [dashboard]
status: active
created: 2026-02-19
updated: 2026-04-03
last_edited_by: agent_init
---

# Agentic-DNA

*A standalone knowledge architecture for building personal lattices and knowledge graphs with AI agents.*

> An AI-native knowledge vault built on the **aDNA paradigm** — where humans browse in Obsidian and agents operate via Claude Code.

---

## Operational State

> [!info] Current Phase
> **Phase 0 — Setup.** Vault initialized from the aDNA-Obsidian starter kit. Customize `CLAUDE.md`, `MANIFEST.md`, and `STATE.md` with your project identity, then begin your first campaign.
>
> [[STATE|Operational State]] | [[MANIFEST|Project Overview]] | [[CLAUDE|Agent Context]]

> [!tip] First Time Here?
> Click the button below to start an agent session — **Berthier** will guide you through setting up your project interactively.
>
> ```meta-bind-button
> label: Launch Claude Code
> icon: terminal
> id: launch-claude
> style: primary
> action:
>   type: command
>   command: termy:claude-code
> ```
>
> ```meta-bind-button
> label: Open Web Browser
> icon: globe
> id: open-browser
> style: primary
> action:
>   type: command
>   command: webviewer:open
> ```
>
> Don't see a terminal? Termy downloads a small binary on first launch (requires internet).
> Prefer doing it yourself? Edit [[CLAUDE]], [[MANIFEST]], and [[STATE]] with your project details.

---

## Recent Sessions

```dataview
TABLE WITHOUT ID
  link(file.path, session_id) AS "Session",
  intent AS "Focus",
  status AS "Status"
FROM "how/sessions"
WHERE type = "session"
SORT created DESC
LIMIT 5
```

> [!note] No sessions yet?
> Use the **Launch Claude Code** button above to start your first agent session, or create a session manually in `how/sessions/active/`.

---

## Active Campaigns

```dataview
TABLE WITHOUT ID
  link(file.path, title) AS "Campaign",
  status AS "Status",
  owner AS "Owner"
FROM "how/campaigns"
WHERE type = "campaign" AND status != "completed"
SORT created DESC
```

> [!note] No campaigns yet?
> Campaigns coordinate multi-mission initiatives. Create one in `how/campaigns/` when you have a strategic goal that requires multiple work streams.

---

## Vault Overview

| Layer | Files | Purpose |
|-------|-------|---------|
| **what/** | `$= dv.pages('"what"').length` | Knowledge objects, context library, lattice tools |
| **how/** | `$= dv.pages('"how"').length` | Missions, sessions, campaigns, templates, pipelines |
| **who/** | `$= dv.pages('"who"').length` | People, teams, coordination, governance |

---

## Quick Start

> [!abstract] Getting Started
> 1. **Click "Launch Claude Code"** above — Berthier will guide you through interactive onboarding
> 2. **Or customize manually** — edit `CLAUDE.md`, `MANIFEST.md`, `STATE.md` with your project details
> 3. **Start building** — create a campaign, start a session, add context to `what/context/`

### Templates

| Template | Location | Creates in |
|----------|----------|-----------|
| Session | `how/templates/template_session.md` | `how/sessions/active/` |
| Mission | `how/templates/template_mission.md` | `how/missions/` |
| Campaign | `how/templates/template_campaign.md` | `how/campaigns/` |
| Context Entry | `how/templates/template_context.md` | `what/context/` |

---

## Navigation

> [!quote]
> **[[what/AGENTS|Knowledge (what/)]]** — what you know, what you've learned, what you've decided
> **[[how/AGENTS|Operations (how/)]]** — how you work, missions, sessions, templates
> **[[who/AGENTS|Organization (who/)]]** — who's involved, coordination, governance

---

## Key Documents

| Document | Purpose |
|----------|---------|
| [[CLAUDE]] | Agent master context — project identity, safety rules, protocol |
| [[MANIFEST]] | Project overview — architecture, entry points, active builds |
| [[STATE]] | Operational state — current phase, blockers, next steps |
| [[AGENTS]] | Root agent guide — directory overview, naming, startup |

---

<div class="homepage-footer">

Agentic-DNA — a standalone knowledge architecture built on the [aDNA paradigm](https://github.com/LatticeProtocol/adna) | foundational building block of the [Lattice Protocol](https://github.com/LatticeProtocol/lattice-protocol)

</div>
