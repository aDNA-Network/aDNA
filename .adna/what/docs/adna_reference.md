---
type: documentation
created: 2026-07-13
updated: 2026-07-13
status: active
last_edited_by: agent_rosetta
tags: [reference, ontology, lattice, compliance, domain_knowledge]
---

# aDNA Reference — Domain Knowledge Tables

> Reference companion to `CLAUDE.md`. The **16-entity base ontology triad** (WHO/WHAT/HOW) stays inline in
> `CLAUDE.md` → Domain Knowledge; everything below was extracted here (v8.8) so the always-loaded governance layer
> stays lean. Load this doc when you need the tables.

## Lattice Types

| Type | Description | Execution Mode |
|------|-------------|---------------|
| `pipeline` | Deterministic DAG of modules | `workflow` |
| `agent` | LLM-driven reasoning | `reasoning` |
| `context_graph` | Knowledge structure | varies |
| `workflow` | Operational process | `workflow` |
| `infrastructure` | Physical/network topology (nodes, edges, services) | varies |
| `context_set` | Disease/domain-specific overlay inheriting from a base lattice | varies |
| `skill` | Claude Skill promoted to lattice registry | varies |

## Execution Modes

| Mode | Description |
|------|-------------|
| `workflow` | Deterministic DAG — fixed sequence of steps |
| `reasoning` | LLM-driven — model decides next steps |
| `hybrid` | Mixed — workflow structure with reasoning at decision points |

## Object Standards

Three core object types have type-standard docs, YAML schemas, and FAIR metadata requirements. Targets are a dataset
subtype (`dataset_class: target`).

| Object | Context Reference | Schema |
|--------|------------------|--------|
| Module | `what/context/object_standards/` | — |
| Dataset | `what/context/object_standards/` | — |
| Lattice | `what/context/object_standards/` | `what/lattices/lattice_yaml_schema.json` |

> Note: Full object standard docs (`standard_module.md`, `standard_dataset.md`, `standard_lattice.md`) are
> vault-specific files. This repo carries the context library summaries and schemas.

**Canvas authority model (Decision 9)**: `.lattice.yaml` is authoritative; `.canvas` is the view/interaction layer.
Round-Trip Protocol v1.0 governs bidirectional conversion.

**Type vocabulary (Decision 10)**: 19 canonical I/O types across 4 tiers (primitives → structured → molecular →
media) for module `inputs:`/`outputs:` annotations. Snake_case, file types end in `_file`.

## Registry Awareness

Lattices can be published to and pulled from registries for sharing across instances. The registry is local-first
(`MarketplaceRegistry`), with federation enabling cross-instance exchange.

- **Publish**: `latlab lattice publish <path>` — registers a lattice with its metadata, FAIR block, and federation
  info. Requires 6 readiness checks (shareable, source_instance, version_policy, license, keywords, valid
  lattice_type).
- **Pull**: `latlab lattice pull <name>` — downloads a published lattice by name (optionally pinned to a version).
- **Compose**: `latlab lattice compose <parent> <child> --pattern external|inline --seam-edges <json>` — combines two
  lattices. External keeps them separate with seam edges; inline merges child nodes into the parent.
- **Skills as lattices**: Skills (`lattice_type: skill`) are a degenerate lattice and can be published to the registry
  like any other lattice. See the Skill–Lattice Interop Standard for promotion from skill files to lattice records.
- **Workflow skill**: `how/skills/skill_lattice_publish.md` — full agent recipe for validate → check readiness →
  publish/pull/compose.
- **Registry template**: `how/templates/template_registry.md` — metadata checklist for federation publication.

## Compute Tiers

| Tier | Scope | Example |
|------|-------|---------|
| **L0** (Local) | Knowledge architecture only — Obsidian + Claude Code, no compute services | Fresh `~/aDNA/` workspace |
| **L1** (Edge) | Local/edge compute, lightweight inference — JupyterHub + Lattice network | Laptop GPU, edge device |
| **L2** (Regional) | Institutional clusters, moderate training | University cluster, on-prem HPC |
| **L3** (Cloud/HPC) | Large-scale data centers, heavy training | Cloud GPU fleet |

**L0 → L1 Upgrade**: L0 workspaces can be upgraded to L1 compute nodes by adding JupyterHub and connecting to the
Lattice network. See `how/skills/skill_l1_upgrade.md` for the phased upgrade path.

## FAIR Metadata

Every `.lattice.yaml` includes a `fair` block with:
- `license` — SPDX identifier (e.g., `MIT`, `Apache-2.0`)
- `creators` — list of creator names
- `keywords` — semantic tags for findability
- `identifier` — optional DOI or persistent ID
- `provenance` — origin and methodology description

## Convergence Model

The execution hierarchy (Campaign → Mission → Objective) is a convergent decomposition: each level narrows context,
reducing token count while increasing signal density.

| Level | Structural Parallel (informal) | Effect |
|-------|-------------------------------|--------|
| **Vault** | Finite collection | Total knowledge — full token count |
| **Campaign** | Subset selection | Strategic initiative — hundreds of files → tens |
| **Mission** | Narrower subset selection | Decomposed task — tens of files → handful |
| **Objective** | Exact file selection | Session work — the exact files needed |

> These are structural analogies, not formal mathematical equivalences.

Context serving implements this as graph traversal: load only the subgraph reachable from the current objective.
Each `AGENTS.md` helps agents decide whether to load its directory. See
`what/context/prompt_engineering/context_prompt_engineering_convergence_model.md` for the full articulation.

## Compliance Dimensions

Object quality is measured across 10 dimensions (scored 0-5 each, 50 max):

1. **Triad structure** — correct directory placement
2. **Governance** — CLAUDE.md, MANIFEST.md, STATE.md coherence
3. **Frontmatter** — required fields present and valid
4. **FAIR metadata** — keywords, license, identifier, provenance
5. **Type vocabulary** — canonical I/O types on module inputs/outputs
6. **Versioning** — semver in frontmatter, CHANGELOG entries
7. **Federation** — discoverable flag, federation block
8. **Registration** — lattice registry readiness
9. **Companions** — YAML companion files for non-YAML objects
10. **Reproducibility** — clear inputs, outputs, and execution context

Reference: `what/lattices/tools/compliance_checker.py` for automated checking.
