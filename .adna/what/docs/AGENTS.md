---
type: directory_index
created: 2026-02-19
updated: 2026-03-19
last_edited_by: agent_init
tags: [directory_index, docs]
token_estimate: ~350
---

# what/docs/ — aDNA Specification Documents

## Purpose

Core specification documents that define the aDNA (Agentic DNA) knowledge architecture standard. These are the authoritative references for how aDNA vaults are structured, governed, and composed.

## Contents

| Document | Token Estimate | Purpose |
|----------|---------------|---------|
| `adna_standard.md` | ~8,000 | Normative aDNA specification v2.1 — triad structure, entity types, governance, pipelines, FAIR metadata. 9 Mermaid diagrams. |
| `adna_design.md` | ~5,000 | Design rationale and deployment patterns — standalone, nested, federated forms. 5 Mermaid diagrams. |
| `adna_bridge_patterns.md` | ~4,000 | Composition patterns for multi-vault architectures — nesting, federation, discovery. 5 Mermaid diagrams. |
| `migration_guide.md` | ~3,500 | Adding aDNA to existing projects — decision tree (bare vs. embedded), step-by-step walkthroughs, starter templates, common pitfalls. |
| `agent_first_guide.md` | ~3,500 | Terminal-first aDNA setup — using aDNA with Claude Code without Obsidian, feature parity audit (22/6/12 split), session workflow, Claude Code configuration. |
| `standard_reading_guide.md` | ~3,000 | Reading guide for the standard — three persona-based paths (new adopter, extension builder, contributor), section map with line ranges, skill/lattice disambiguation, quick reference decision tree. |
| `start_kit_prd.md` | ~4,000 | Lattice Start Kit PRD — 1-click onboarding design: 4 personas, packaging evaluation, 5-question interview, `adna new` + `adna init` flow mockups, MoSCoW requirements, success metrics. Design only — build deferred to `campaign_lattice_start_kit`. |
| `context_quality_rubric.md` | ~2,000 | 6-axis quality evaluation framework for context files — scoring methodology, calibration examples. |
| `version_migration_guide.md` | ~1,200 | Maintainer guide for the version migration system — when to create prompts, how to write and test them, sequential composition design. |
| `migration_safety_framework.md` | ~800 | Migration safety guarantees, known limitations, backup best practices, error recovery ladder (L1-L5), worktree-based testing procedure. |
| `ontology_unification.md` | ~8,000 | Ontology unification protocol — merge algorithm (4-step with Mermaid flowchart + pseudo-code), 10-type conflict taxonomy, namespace specification, worked example (org_formation + vault). |
| `lattice_federation.md` | ~8,000 | Federation & sharing protocol — 5 capabilities (validate, export, share, import, compose), `lattice://` URI scheme, inline vs. external reference composition, import algorithm with M9 integration, worked round-trip example. |
| `lattice_interop.md` | ~5,500 | Lattice interop standard — design-time interface descriptors (`lattice_interface` node convention), 8-step runtime execution sequence for `lattice://` references, version drift detection and resolution (severity classification, policy strategies, drift recovery workflow). 2 Mermaid diagrams. |

## Total Token Budget

~56,500 tokens to load all 13 documents. These are heavy reference documents — load specific files based on need.

## Load/Skip Decision

**Load this directory when**:
- Understanding or extending the aDNA standard itself (read `adna_standard.md`)
- Designing a new aDNA instance or evaluating deployment form (read `adna_design.md`)
- Adding aDNA to an existing project or codebase (read `migration_guide.md`)
- Setting up aDNA without Obsidian, terminal-first workflow (read `agent_first_guide.md`)
- Navigating the standard by persona or section, or clarifying skill vs. lattice (read `standard_reading_guide.md`)
- Planning multi-vault composition or federation (read `adna_bridge_patterns.md`)
- Evaluating context file quality or setting up review processes (read `context_quality_rubric.md`)
- Merging ontologies from different aDNA instances or integrating sub-lattices (read `ontology_unification.md`)
- Federating, sharing, importing, or composing lattice artifacts across instances (read `lattice_federation.md`)
- Designing interface contracts, runtime execution, or version management for cross-instance lattice references (read `lattice_interop.md`)
- Building or extending the Lattice Start Kit CLI, onboarding flow, or scaffolding system (read `start_kit_prd.md`)
- Understanding or creating version migration prompts (read `version_migration_guide.md`)
- Evaluating migration safety, rollback procedures, or testing protocols (read `migration_safety_framework.md`)

**Skip when**:
- Performing operational work within an established aDNA vault (sessions, missions, CRM)
- Working on domain-specific content that doesn't touch the aDNA standard
- Already familiar with the standard and not modifying its structure

**Token cost**: ~300 tokens (this AGENTS.md). Individual docs are 2,000-8,000 tokens each — load selectively.

## Reading Order (for federation & interop)

For agents working on cross-instance lattice composition, the recommended reading order is:
1. `lattice_federation.md` (M10) — URI scheme, composition patterns, import algorithm
2. `ontology_unification.md` (M9) — merge algorithm for import compatibility
3. `lattice_interop.md` (M11) — interface contracts, runtime flow, version drift

## Cross-References

- [what/AGENTS](../AGENTS.md) — Knowledge layer index
- [what/context/AGENTS](../context/AGENTS.md) — Context library (builds on these specs)
- [CLAUDE.md](../../CLAUDE.md) — Governance (implements the standard)
