---
type: directory_index
created: 2026-03-19
updated: 2026-03-19
last_edited_by: agent_init
tags: [directory_index, who]
---

# who/ — Organization (Agent Reference)

## Purpose

`who/` holds organization records — the **WHO** of **example-biotech-lab**. Lab members, collaborators, coordination notes, and governance.

## Subdirectories

| Folder | Purpose | Status |
|--------|---------|--------|
| `coordination/` | Cross-agent ephemeral notes — handoffs, urgency signals | Active |
| `governance/` | Roles, decision authority, lab policies | Active |

## Working Rules

- All files follow `type_descriptive_name.md` (underscores only, never hyphens)
- Check `updated` field before modifying files — if today and you didn't make the last edit, confirm with the user
- Set `last_edited_by` and `updated` in frontmatter when modifying any file

## Cross-References

- [what/AGENTS](../what/AGENTS.md) — Knowledge objects (experiments, compounds, protocols, targets)
- [how/AGENTS](../how/AGENTS.md) — Operations (missions, sessions, templates)
