---
type: context_guide
topic: adna_core
subtopic: lattice_design
created: 2026-02-20
updated: 2026-03-18
sources: ["lattice_yaml_schema.json (draft-2020-12)", "aDNA Standard v2.1 (§5.1)", "Example lattices (6): deep_research, protein_binder_design, org_formation, hello_world, knowledge_base, docking_assessment"]
context_version: "1.0"
token_estimate: ~1000
last_edited_by: agent_init
tags: [context, adna_core, lattice, yaml, schema, federation]
quality_score: 4.4
signal_density: 5
actionability: 5
coverage_uniformity: 4
source_diversity: 3
cross_topic_coherence: 4
freshness_category: stable
last_evaluated: 2026-02-20
---

# aDNA Core: Lattice Design Guide

## Key Principles

1. **A lattice is a composition graph.** It describes a workflow of nodes (modules, datasets, processes) connected by edges (data flow). Lattices are declarative — they define structure, not runtime code.

2. **Schema governs all lattice files.** Every `.lattice.yaml` must validate against `lattice_yaml_schema.json`. The schema enforces structure while allowing extension via `additionalProperties`.

3. **Four lattice types cover all patterns.**

| Type | Purpose | Example |
|------|---------|---------|
| `pipeline` | Sequential data processing | protein_binder_design |
| `agent` | Agentic decision-making loops | (not yet exampled) |
| `context_graph` | Knowledge retrieval/reasoning | knowledge_base |
| `workflow` | Orchestrated multi-step operations | deep_research |

4. **Three execution modes define runtime behavior.**

| Mode | Pattern | When |
|------|---------|------|
| `sequential` | Nodes execute in topological order | Simple pipelines |
| `parallel` | Independent nodes run concurrently | Fan-out stages |
| `hybrid` | Mix of sequential and parallel | Most real lattices |

5. **FAIR metadata ensures discoverability.** Every lattice includes `fair` block: license, creators, keywords, provenance, and optional DOI identifier.

## Lattice YAML Structure

```yaml
lattice:
  name: my_lattice                    # ^[a-z][a-z0-9_]*$ (required)
  version: "1.0.0"                    # semver (required)
  lattice_type: pipeline              # enum: pipeline|agent|context_graph|workflow|skill|infrastructure|context_set
  description: "What this lattice does"

  execution:                          # Required
    mode: sequential                  # enum: sequential|parallel|hybrid
    runtime: ray                      # Optional: ray|local|kubernetes
    tier: L2                          # Optional: L1|L2|L3

  nodes:                              # Required, 1+ nodes
    - id: node_name                   # ^[a-z][a-z0-9_]*$ (required)
      type: module                    # enum: module|dataset|process|checkpoint|...
      ref: "what/modules/module_x"    # Optional: link to implementation
      description: "Node purpose"     # Required
      config: {}                      # Optional: additionalProperties allowed

  edges:                              # Required, 1+ edges (for 2+ nodes)
    - from: node_a                    # Required: source node id
      to: node_b                      # Required: target node id
      label: "data flow description"  # Optional
      data_mapping:                   # Optional: explicit field mapping
        source_field: target_field

  fair:                               # Required
    license: "MIT"
    creators: ["Lattice Labs"]
    keywords: ["domain", "keywords"]
    provenance: "Origin description"

  federation:                         # Optional — enables sharing
    shareable: false                  # Opt-in for federation
    source_instance: ""              # Originating aDNA instance
    parent_lattice: ""               # If extracted from larger lattice
    version_policy: minor            # locked|patch|minor|latest
    extracted_nodes: []              # Node IDs from parent
```

## Design Decisions

### Choosing Lattice Type

| If your workflow... | Use |
|---------------------|-----|
| Processes data through stages | `pipeline` |
| Makes decisions, loops, evaluates | `agent` |
| Retrieves and reasons over knowledge | `context_graph` |
| Orchestrates multiple sub-processes | `workflow` |

### Choosing Node Type

| Node Type | Purpose | Has `ref`? |
|-----------|---------|------------|
| `module` | Executable compute unit | Yes — links to `what/modules/` |
| `dataset` | Data source or training set | Yes — links to `what/datasets/` |
| `process` | Human or agent procedure | Optional |
| `checkpoint` | Quality gate / review point | No |

### Edge Design

- Edges define data flow direction (from → to)
- Use `label` for human-readable descriptions
- Use `data_mapping` for explicit field mapping between nodes
- Use `port` when connecting to federated child lattice entry nodes

### Federation Readiness

To make a lattice shareable across aDNA instances:

| Property | Required | Why |
|----------|----------|-----|
| `federation.shareable: true` | Yes | Explicit opt-in |
| `federation.source_instance` | Yes | Provenance |
| `fair.license` | Yes | Legal clarity |
| `fair.keywords` (≥1) | Yes | Findability |
| All `ref` fields resolve | Yes | No broken references |

## Validation

```bash
# Validate a lattice file against the schema
python what/lattices/tools/lattice_validate.py path/to/my_lattice.lattice.yaml
```

The validator checks: schema compliance, node ID uniqueness, edge reference validity, federation property consistency (extracted_nodes cross-ref), and self-referential edge warnings.

## Example Lattice Patterns

### Minimal (hello_world — 3 nodes)

```yaml
nodes:
  - id: collect_data
    type: process
    description: "Gather input data"
  - id: transform
    type: module
    description: "Transform data"
  - id: output
    type: process
    description: "Deliver results"
edges:
  - from: collect_data
    to: transform
  - from: transform
    to: output
```

### Federation Demo (docking_assessment — sub-lattice)

```yaml
federation:
  shareable: true
  source_instance: adna
  parent_lattice: protein_binder_design
  version_policy: locked
  extracted_nodes: [structure_prediction, interface_analysis, ranking]
```

## Anti-Patterns

1. **Unnamed nodes.** Every node needs a descriptive `id` — avoid `node_1`, `step_a`.
2. **Missing edges.** Nodes without edges are disconnected — they serve no workflow purpose.
3. **Implicit data mapping.** Use explicit `data_mapping` on edges rather than assuming field names match.
4. **Federation without license.** `shareable: true` without `fair.license` blocks federation validation.
5. **Monolithic lattices.** Extract sub-lattices for reusable sub-workflows rather than building one massive graph.

## Sources

1. `lattice_yaml_schema.json` — JSON Schema (draft-2020-12), authoritative structure definition
2. aDNA Standard v2.1 — §5.1 (what/ registry pattern, ontology artifact)
3. Example lattices — 6 validated examples covering all types and federation patterns
