---
type: context_core
topic: lattice_basics
subtopic: core_concepts
created: 2026-03-05
updated: 2026-03-18
sources: ["aDNA Standard v2.1 (what/docs/adna_standard.md)", "aDNA Design Document (what/docs/adna_design.md)", "adna_core lattice_design context", "hello_world.lattice.yaml example", "type_vocabulary context"]
context_version: "2.0"
token_estimate: ~1000
last_edited_by: agent_init
tags: [context, lattice_basics]
quality_score: 4.0
signal_density: 4
actionability: 4
coverage_uniformity: 4
source_diversity: 3
cross_topic_coherence: 4
freshness_category: stable
last_evaluated: 2026-03-18
---

# Lattice Basics: Core Concepts

## What is aDNA?

**aDNA** (Autonomous DNA) is a framework for organizing human-AI collaborative work. It provides:

1. **A vault structure** (who/what/how triad) — the knowledge graph
2. **Object types** (modules, datasets, lattices) — composable building blocks
3. **Operational protocols** (campaigns, missions, sessions) — structured execution
4. **Agent integration** — AI agents operate alongside humans using governance files

aDNA works in two forms: a **bare triad** (standalone Obsidian vault, like this repo) or an **embedded triad** (`.agentic/` directory inside a code repo). See `what/docs/adna_bridge_patterns.md` for multi-vault composition.

## The Three Object Types

### Modules

Self-contained computational units with typed inputs and outputs. A module wraps one function, one model, or one tool.

```yaml
# Example: protein structure predictor module
type: module
module_type: compute  # compute | mcp_server | data_pipeline | utility
status: active
inputs:
  - name: sequence
    type: protein_sequence       # from the 19-type vocabulary
    description: "Amino acid sequence to fold"
outputs:
  - name: structure
    type: pdb_structure
    description: "Predicted 3D structure"
fair:
  keywords: ["protein", "structure prediction"]
  license: MIT
```

Module types: `compute` (runs code), `mcp_server` (tool endpoint), `data_pipeline` (ETL), `utility` (helper). See `what/docs/adna_standard.md` §4.1 for the full spec.

### Datasets

Data collections with storage abstraction, lineage tracking, and federation metadata. Subtypes include `target` (biological targets, in `what/datasets/targets/`).

```yaml
# Example: protein sequence dataset
type: dataset
dataset_class: source  # source | derived | target | benchmark
status: active
storage:
  provider: local      # s3 | minio | gcs | azure | ceph | local | fuse
  path: /data/sequences/
  format: fasta        # csv | parquet | pdb | fasta | sdf | json
lineage:
  source: "UniProt release 2026_01"
  transformations: ["filtered to human proteins", "length > 50 residues"]
```

The `.dataset.yaml` schema (`what/datasets/dataset_yaml_schema.json`) provides machine-readable metadata for deployed datasets. See `what/docs/adna_standard.md` §4.2.

### Lattices

Directed graphs connecting modules and datasets into executable workflows. Lattices are the composition layer — they define **how** objects connect.

```yaml
# Example: hello_world.lattice.yaml (from what/lattices/examples/)
lattice:
  name: hello_world
  version: "1.0.0"
  lattice_type: pipeline     # pipeline | agent | context_graph | workflow
  description: "Minimal pipeline — read, transform, write"
  execution:
    mode: workflow            # workflow | reasoning | hybrid
    runtime: local            # local | ray | kubernetes
    tier: L1                  # L1 (edge) | L2 (regional) | L3 (cloud)
  nodes:
    - id: input_data
      type: dataset
      description: "Input dataset"
    - id: transform
      type: process
      description: "Apply transformation"
    - id: output_data
      type: dataset
      description: "Transformed output"
  edges:
    - from: input_data
      to: transform
      label: "raw data"
    - from: transform
      to: output_data
      label: "processed data"
  fair:
    license: "MIT"
    keywords: ["hello world", "onboarding"]
```

**Start here**: Copy `what/lattices/examples/hello_world.lattice.yaml` and customize. 13 examples ship across business, research, creative, and biotech domains. See `what/docs/adna_standard.md` §4.3 for the full lattice spec.

## Type Vocabulary

19 canonical I/O types across 4 tiers define the connection language between modules:

| Tier | Types |
|------|-------|
| **Primitives** | `string`, `number`, `boolean`, `path`, `json`, `binary` |
| **Structured** | `csv`, `dataframe`, `yaml_config`, `parameter_set` |
| **Molecular** | `protein_sequence`, `pdb_structure`, `sdf_molecule`, `msa_alignment`, `docking_result`, `md_trajectory`, `density_map` |
| **Media** | `image`, `canvas_json` |

Use these in module `inputs:`/`outputs:` and lattice edge `data_mapping`. Full reference: `what/context/adna_core/context_adna_core_type_vocabulary.md`.

## FAIR Metadata

All deployed objects carry FAIR (Findable, Accessible, Interoperable, Reusable) metadata. Minimum requirement: `keywords` + `license`. Full envelope supports nested or flat forms — see `what/context/adna_core/context_adna_core_fair_mapping.md` for interconversion rules.

## Where to Go Next

| Goal | Read |
|------|------|
| Understand vault structure | `context_lattice_basics_vault_architecture.md` (this topic) |
| Design a lattice | `what/context/adna_core/context_adna_core_lattice_design.md` |
| Learn object standards | `what/context/object_standards/context_object_standards_overview.md` |
| Extend the ontology | `what/context/adna_core/context_adna_core_ontology_design.md` |
| Full normative spec | `what/docs/adna_standard.md` |

## Sources

- aDNA Standard v2.1 (`what/docs/adna_standard.md`) — normative specification
- aDNA Design Document (`what/docs/adna_design.md`) — architecture rationale
- Lattice design context (`what/context/adna_core/context_adna_core_lattice_design.md`) — YAML schema reference
- Hello World example (`what/lattices/examples/hello_world.lattice.yaml`) — minimal valid lattice
- Type vocabulary context (`what/context/adna_core/context_adna_core_type_vocabulary.md`) — 19 I/O types
