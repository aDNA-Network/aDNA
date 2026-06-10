---
type: directory_index
created: 2026-03-19
updated: 2026-03-19
last_edited_by: agent_init
tags: [directory_index, what]
---

# what/ — Knowledge Layer (Agent Reference)

## Purpose

`what/` holds knowledge objects — the **WHAT** of **example-enterprise-pipeline**. Context library, architectural decisions, service definitions, and API specifications.

## Subdirectories

| Folder | Purpose | Status |
|--------|---------|--------|
| `context/` | Agent context library — synthesized knowledge for domain work | Active |
| `decisions/` | Architecture Decision Records — significant decisions and rationale | Active |
| `services/` | Service definitions — microservice contracts, dependencies, SLAs | Active |
| `apis/` | API specifications — endpoints, schemas, versioning | Active |

## Working Rules

- All files follow `type_descriptive_name.md` (underscores only, never hyphens)
- Context files carry `token_estimate` in frontmatter for budget planning
- Service and API entries link to their deployment configs in `how/deployments/`

## Cross-References

- [who/AGENTS](../who/AGENTS.md) — Organization (customers, partners, contacts, projects)
- [how/AGENTS](../how/AGENTS.md) — Operations (missions, sessions, deployments, incidents)
