---
type: directory_index
created: 2026-02-17
updated: 2026-02-20
last_edited_by: agent_init
tags: [directory_index, what]
---

# what/ — Knowledge Layer (Agent Reference)

## Purpose

`what/` holds knowledge objects — the **WHAT** of this project. Context library, decisions, reference material, and domain-specific entities all live here.

## Key Files

| File | Purpose |
|------|---------|
| `ontology.md` | Base ontology artifact — 14 entity types, Mermaid ER diagrams, convergence + unification annotations |

## Subdirectories

| Folder | Purpose | Status |
|--------|---------|--------|
| `context/` | Agent context library — synthesized knowledge agents load before domain work | Required |
| `decisions/` | Architecture Decision Records — significant decisions and rationale | Recommended |
| `docs/` | Specification documents — aDNA standard, design doc, bridge patterns | Active |
| `lattices/` | Lattice YAML definitions, tools, schema, and examples | Active |

## Registry Pattern

what/ serves as a registry layer. Entries describe and link to objects — they do not duplicate source material. Each entry has frontmatter with type, status, and links to the implementation or source.

## Naming

All files follow `type_descriptive_name.md` (underscores only, never hyphens).

## Progressive Loading

**This file is a routing index.** Read it to understand what `what/` contains, then drill into the specific subdirectory relevant to your task. Do not load all subdirectory AGENTS.md files at once — each contains detailed protocol (context library: ~1,100 tokens, lattices: ~550 tokens, docs: ~300 tokens, decisions: ~350 tokens).

**Recommended loading path**: Root AGENTS.md → `what/AGENTS.md` (this file) → specific subdirectory AGENTS.md

## Load/Skip Decision

**Load this directory when**:
- Orienting on what knowledge objects exist (context, decisions, docs, lattices)
- Deciding which subdirectory to drill into for domain work
- Understanding how the WHAT leg connects to HOW and WHO

**Skip when**:
- Already know which subdirectory you need — go directly to its AGENTS.md
- Working purely in `how/` or `who/` with no knowledge object interaction
- Mid-session and already oriented on the `what/` structure

**Token cost**: ~350 tokens (this AGENTS.md)

## Cross-References

- [ontology.md](ontology.md) — Base ontology (14 entity types, 5 Mermaid diagrams)
- [what/context/AGENTS](context/AGENTS.md) — Context library protocol and topic index
- [what/decisions/AGENTS](decisions/AGENTS.md) — Architecture Decision Records
- [what/docs/AGENTS](docs/AGENTS.md) — aDNA specification documents
- [what/lattices/AGENTS](lattices/AGENTS.md) — Lattice YAML tools and examples
- [how/AGENTS](../how/AGENTS.md) — Operations (HOW)
- [who/AGENTS](../who/AGENTS.md) — Organization (WHO)
