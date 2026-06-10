---
type: directory_index
created: 2026-03-19
updated: 2026-03-19
last_edited_by: agent_init
tags: [directory_index, what]
---

# what/ — Knowledge Layer (Agent Reference)

## Purpose

`what/` holds knowledge objects — the **WHAT** of **example-biotech-lab**. Experimental records, compound libraries, protocols, targets, context, and decisions.

## Subdirectories

| Folder | Purpose | Status |
|--------|---------|--------|
| `context/` | Agent context library — synthesized knowledge for domain work | Active |
| `decisions/` | Architecture Decision Records — significant decisions and rationale | Active |
| `experiments/` | Experimental records — hypotheses, methods, results, analysis | Active |
| `compounds/` | Compound library — chemical entities, properties, sourcing | Active |
| `protocols/` | Lab protocols — standardized procedures, SOPs | Active |
| `targets/` | Biological targets — proteins, pathways, disease models | Active |

## Working Rules

- All files follow `type_descriptive_name.md` (underscores only, never hyphens)
- Context files carry `token_estimate` in frontmatter for budget planning
- Experiments link to the protocol they follow and the compounds/targets they involve

## Cross-References

- [who/AGENTS](../who/AGENTS.md) — Organization (lab members, governance)
- [how/AGENTS](../how/AGENTS.md) — Operations (missions, sessions, templates)
