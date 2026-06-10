---
type: context_core
topic: object_standards
subtopic: overview
created: 2026-03-05
updated: 2026-04-03
sources: ["aDNA Standard v2.1 (what/docs/adna_standard.md)", "lattice_yaml_schema.json", "dataset_yaml_schema.json"]
context_version: "2.1"
token_estimate: ~600
last_edited_by: agent_init
tags: [context, object_standards]
quality_score: 4.1
signal_density: 5
actionability: 4
coverage_uniformity: 4
source_diversity: 3
cross_topic_coherence: 4
freshness_category: stable
last_evaluated: 2026-04-03
---

# Object Standards: Overview

Quick reference for the three core aDNA object types. Normative specification: `what/docs/adna_standard.md` (RFC 2119 keywords).

## Object Reference

| Object | Directory | Schema | Spec Section | Key Concept |
|--------|-----------|--------|-------------|-------------|
| **Module** | `what/modules/` | -- | v2.1 ss4.1 | Atomic capability: one function, one model, one tool. Typed I/O from 19-type vocabulary. |
| **Dataset** | `what/datasets/` | `dataset_yaml_schema.json` | v2.1 ss4.2 | Data layer: 7 storage providers, lineage tracking, federation metadata. Subtype: `target` (`dataset_class: target`). |
| **Lattice** | `what/lattices/` | `lattice_yaml_schema.json` | v2.1 ss4.3 | Directed graph of modules + datasets. Types: `pipeline`, `agent`, `context_graph`, `workflow`. 13 examples in `what/lattices/examples/`. |

## Required Frontmatter (All Objects)

Every object needs: `type`, `status`, typed I/O (modules), `storage` + `lineage` (datasets), `nodes` + `edges` (lattices).

All deployed objects require FAIR metadata. Minimum:

```yaml
fair:
  keywords: ["domain", "tags"]
  license: MIT
```

Full FAIR envelope (nested + flat transport forms): see `what/context/adna_core/context_adna_core_fair_mapping.md`.

## Quality Criteria (Modules)

1. Single responsibility -- one module, one purpose
2. Typed I/O -- canonical 19-type vocabulary
3. Explicit dependencies
4. Version tracked
5. FAIR annotated (`keywords` + `license` minimum)

## Lattice Design Principles

1. **Typed edges** -- data types from 19-type vocabulary
2. **Composability** -- lattices reference sub-lattices
3. **Reproducibility** -- full config for deterministic replay
4. **Visualization** -- Canvas JSON (`.canvas`) via round-trip tools

## Type Vocabulary Quick Reference

| Tier | Types |
|------|-------|
| Primitives | `string`, `number`, `boolean`, `path`, `json`, `binary` |
| Structured | `csv`, `dataframe`, `yaml_config`, `parameter_set` |
| Molecular | `protein_sequence`, `pdb_structure`, `sdf_molecule`, `msa_alignment`, `docking_result`, `md_trajectory`, `density_map` |
| Media | `image`, `canvas_json` |

Full reference: `what/context/adna_core/context_adna_core_type_vocabulary.md`.

## Sources

- aDNA Standard v2.1 (`what/docs/adna_standard.md`) -- normative specification
- Lattice YAML schema (`what/lattices/lattice_yaml_schema.json`)
- Dataset YAML schema (`what/datasets/dataset_yaml_schema.json`)
- Type vocabulary context (`what/context/adna_core/context_adna_core_type_vocabulary.md`)
- FAIR mapping context (`what/context/adna_core/context_adna_core_fair_mapping.md`)
