---
type: directory_index
created: 2026-02-17
updated: 2026-04-03
last_edited_by: agent_init
tags: [directory_index, root]
---

# Agentic-DNA — Agent Guide

## Purpose

This is the root agent reference for the Agentic-DNA project. It routes agents to the appropriate triad leg (what/how/who) based on their current task. This file is always loaded — it does not have a Load/Skip section because agents need it for orientation on every session.

## Quick Orientation

| Document | What You'll Find |
|----------|-----------------|
| **CLAUDE.md** | Agent operating context — safety rules, startup checklist, protocols |
| **MANIFEST.md** | Project overview — architecture, entry points, active builds |
| **STATE.md** | Current operational state — phase, blockers, next steps |
| **README.md** | Human-readable getting-started guide |

## Project Structure

```
adna/
├── what/        # WHAT — Knowledge objects, context library, decisions, docs, lattices
├── how/         # HOW — Campaigns, missions, sessions, templates, pipelines, skills, backlog
├── who/         # WHO — Coordination, governance (extend with team/, customers/, etc.)
│   └── quests/  # Community-contributed validation experiments and results
```

**Navigation**: Read this file → follow the Layer References below into the triad leg matching your task → drill into specific subdirectories as needed. Each AGENTS.md narrows context progressively.

## Agent Startup

1. **CLAUDE.md** — auto-loaded; confirms project structure and rules
2. **Template/first-run check** — if `role: template` in MANIFEST.md, guide project creation via `skill_project_fork.md`; if uncustomized project (`agent_init`), invoke onboarding skill (`how/skills/skill_onboarding.md`)
3. **STATE.md** — operational snapshot: current phase, blockers, next steps
4. **`how/sessions/active/`** — check for conflicting sessions
5. **`who/coordination/`** — read any urgent cross-agent notes
6. **`how/backlog/`** — quick scan for ideas relevant to current session
7. **`how/campaigns/`** — check for active campaigns
8. **`how/missions/`** — check for active missions
9. **Create session file** in `how/sessions/active/` and begin work

## Layer References

- [what/AGENTS](what/AGENTS.md) — Knowledge objects (WHAT)
- [how/AGENTS](how/AGENTS.md) — Operations (HOW)
- [who/AGENTS](who/AGENTS.md) — Organization (WHO)

## Upstream Contribution Awareness

When you discover framework-level improvements during normal work (missing template fields, undocumented patterns, naming inconsistencies), note them for potential upstream contribution to the aDNA repo. See `how/skills/skill_upstream_contribution.md` for the full protocol.

## Safety Rules

- **Read before write** — always read current content before modifying
- **Check `updated` field** — if updated today by someone else, confirm before overwriting
- **Set `last_edited_by` and `updated`** — on every modification
- **New files are safe** — creating new files has no collision risk

## Priority Hierarchy

1. **Data integrity** — never corrupt or lose existing data
2. **User-requested tasks** — explicit instructions from current user
3. **Operational maintenance** — session tracking, plan updates
4. **Exploration** — research, audits, improvements
