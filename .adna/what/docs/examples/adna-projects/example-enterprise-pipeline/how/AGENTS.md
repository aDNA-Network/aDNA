---
type: directory_index
created: 2026-03-19
updated: 2026-03-19
last_edited_by: agent_init
tags: [directory_index, how]
---

# how/ — Operations (Agent Reference)

## Purpose

`how/` holds operations — the **HOW** of **example-enterprise-pipeline**. Missions, sessions, templates, deployments, and incidents.

## Subdirectories

| Folder | Purpose | Status |
|--------|---------|--------|
| `missions/` | Build plans for multi-session work | Active |
| `sessions/` | Session tracking and audit trail (`active/` + `history/`) | Active |
| `templates/` | Reusable templates for all content types | Active |
| `backlog/` | Ideas and improvement tracking | Active |
| `deployments/` | Deployment records — release history, rollback procedures | Active |
| `incidents/` | Incident records — detection, response, postmortem | Active |

## Working Rules

- All files follow `type_descriptive_name.md` (underscores only, never hyphens)
- Sessions go in `sessions/active/` while open, then archive to `sessions/history/YYYY-MM/`
- Deployments link to the services they affect in `what/services/`
- Incidents reference the deployment or change that triggered them

## Cross-References

- [who/AGENTS](../who/AGENTS.md) — Organization (customers, partners, contacts, projects)
- [what/AGENTS](../what/AGENTS.md) — Knowledge objects (context, decisions, services, APIs)
