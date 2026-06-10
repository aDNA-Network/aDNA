---
type: directory_index
created: 2026-03-19
updated: 2026-03-19
last_edited_by: agent_init
tags: [directory_index, who]
---

# who/ — Organization (Agent Reference)

## Purpose

`who/` holds organization records — the **WHO** of **example-enterprise-pipeline**. Customers, partners, contacts, project records, coordination notes, and governance.

## Subdirectories

| Folder | Purpose | Status |
|--------|---------|--------|
| `customers/` | Customer records — company profiles, deal status, engagement history | Active |
| `partners/` | Partner records — integrations, agreements, joint initiatives | Active |
| `contacts/` | Individual contact records — roles, communication preferences | Active |
| `projects/` | Project records — scope, timeline, deliverables, stakeholders | Active |
| `coordination/` | Cross-agent ephemeral notes — handoffs, urgency signals | Active |
| `governance/` | Roles, decision authority, policies | Active |

## Working Rules

- All files follow `type_descriptive_name.md` (underscores only, never hyphens)
- Check `updated` field before modifying files — if today and you didn't make the last edit, confirm with the user
- Set `last_edited_by` and `updated` in frontmatter when modifying any file
- This is a team vault (3 collaborators) — always follow collision prevention rules in CLAUDE.md

## Cross-References

- [what/AGENTS](../what/AGENTS.md) — Knowledge objects (context, decisions, services, APIs)
- [how/AGENTS](../how/AGENTS.md) — Operations (missions, sessions, deployments, incidents)
