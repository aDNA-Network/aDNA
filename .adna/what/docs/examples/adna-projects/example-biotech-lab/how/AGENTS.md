---
type: directory_index
created: 2026-03-19
updated: 2026-03-19
last_edited_by: agent_init
tags: [directory_index, how]
---

# how/ — Operations (Agent Reference)

## Purpose

`how/` holds operations — the **HOW** of **example-biotech-lab**. Missions, sessions, templates, and backlog for lab operations and research coordination.

## Subdirectories

| Folder | Purpose | Status |
|--------|---------|--------|
| `missions/` | Build plans for multi-session work | Active |
| `sessions/` | Session tracking and audit trail (`active/` + `history/`) | Active |
| `templates/` | Reusable templates for experiments, protocols, sessions | Active |
| `backlog/` | Ideas and improvement tracking | Active |

## Working Rules

- All files follow `type_descriptive_name.md` (underscores only, never hyphens)
- Sessions go in `sessions/active/` while open, then archive to `sessions/history/YYYY-MM/`
- Missions are multi-session plans — decompose large tasks into missions before starting

## Cross-References

- [who/AGENTS](../who/AGENTS.md) — Organization (lab members, governance)
- [what/AGENTS](../what/AGENTS.md) — Knowledge objects (experiments, compounds, protocols, targets)
