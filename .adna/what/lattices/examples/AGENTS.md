---
type: directory_index
created: 2026-02-19
updated: 2026-03-02
last_edited_by: agent_init
tags: [directory_index, lattice, examples, canvas]
---

# what/lattices/examples/ — Reference Lattice Implementations

## Purpose

Example `.lattice.yaml` files demonstrating different lattice types, execution modes, and composition patterns. Use as starting templates when creating new lattices.

## Examples

### General-Purpose Examples

| File | Lattice Type | Execution Mode | Demonstrates |
|------|-------------|---------------|-------------|
| `hello_world.lattice.yaml` | pipeline | workflow | Minimal valid lattice — simplest pipeline for onboarding |
| `sales_pipeline.lattice.yaml` | pipeline | workflow | B2B sales funnel — lead capture through close. Business use case |
| `product_launch.lattice.yaml` | pipeline | hybrid | Cross-functional launch — market research (LLM) through go-to-market |
| `learning_path.lattice.yaml` | workflow | workflow | Personal learning cycle with iterative assessment loop |
| `creative_brief.lattice.yaml` | pipeline | hybrid | Client project workflow — brief through revision cycle with LLM feedback |
| `deep_research.lattice.yaml` | pipeline | hybrid | Multi-agent research pipeline with validation loops and phase gates |
| `knowledge_base.lattice.yaml` | context_graph | reasoning | Knowledge retrieval + LLM reasoning — only `context_graph` type example |
| `research_orchestrator.lattice.yaml` | agent | hybrid | Orchestrator pattern — LLM-driven coordination with human checkpoints |

### Biotech / Federation Examples

| File | Lattice Type | Execution Mode | Demonstrates |
|------|-------------|---------------|-------------|
| `protein_binder_design.lattice.yaml` | pipeline | workflow | Deterministic computational biology pipeline — linear DAG, federation metadata |
| `docking_assessment.lattice.yaml` | pipeline | workflow | Sub-lattice extracted from protein_binder_design — demonstrates all 5 federation properties |
| `binder_generation.lattice.yaml` | pipeline | workflow | Generative design sub-lattice — interface descriptor + federation extraction |
| `composed_therapeutics.lattice.yaml` | pipeline | workflow | Single external reference composition — uses docking_assessment via `lattice://` URI |
| `full_therapeutics.lattice.yaml` | pipeline | workflow | Multi-lattice composition — composes both binder_generation and docking_assessment |

## Canvas Visual Examples

Obsidian Canvas (`.canvas`) files provide visual node-graph representations of lattices. These follow Canvas Standard v1.0.0 conventions (node colors, shapes, edge styles, `_lattice_meta` group).

### Demonstration Canvas

| File | Layout | Source YAML | Demonstrates |
|------|--------|-------------|-------------|
| `hello_world.canvas` | DAG (3 nodes) | `hello_world.lattice.yaml` | Minimal canvas — dataset→process→dataset with M8-compliant colors and shapes |

### Template Canvases

Copy-and-modify starters for the three core layout patterns.

| File | Layout Pattern | Nodes | Demonstrates |
|------|---------------|-------|-------------|
| `template_pipeline.canvas` | DAG (left-to-right) | 4 stages, 4 placeholder nodes | Pipeline template with stage groups, usage guide card |
| `template_agent_graph.canvas` | Radial (center-out) | 1 orchestrator + 4 spokes | Agent/hub-spoke pattern with straight-path edges |
| `template_architecture.canvas` | Grid (L1/L2/L3) | 3 tier zones, 7 nodes | Architecture diagram with data flow + federation edges |

**Canvas conventions**:
- Node colors: green (`"5"`) = dataset, cyan (`"4"`) = module, purple (`"6"`) = reasoning, default = process
- Node shapes: `database` = dataset/hardware, `predefined-process` = module, `diamond` = reasoning
- Edge styles: solid = data flow, `long-dashed` = control/federation, `dotted` = optional
- All edges use `toEnd: "arrow"` explicitly
- `_lattice_meta` group encodes lattice name and version
- `_reserved` metadata block for future canvas-as-authoring extensions

## How to Use

### YAML Examples

1. **Pick the closest example** to your target lattice type and execution mode
2. **Copy** the file with a new name: `your_lattice_name.lattice.yaml`
3. **Modify** nodes, edges, metadata, and FAIR block to match your design
4. **Validate** with `tools/lattice_validate.py` to check schema compliance

### Canvas Templates

1. **Pick the closest layout pattern** (pipeline, agent graph, or architecture)
2. **Copy** the `.canvas` file with a new name
3. **Replace placeholder nodes** — drag vault `.md` files for `file` nodes, or edit text content
4. **Update edge labels** with actual data flow names
5. **Delete the usage guide card** (if present) when done

## Load/Skip Decision

**Load this directory when**:
- Creating a new `.lattice.yaml` file and need a structural template
- Learning the lattice YAML format by example
- Comparing execution modes (workflow vs. reasoning vs. hybrid)

**Skip when**:
- Already familiar with the `.lattice.yaml` format and not creating new lattices
- Working on non-lattice tasks (sessions, context, governance)

**Token cost**: ~400 tokens (this AGENTS.md). Individual YAML files are ~500-1,000 tokens each. Canvas files are ~500-2,000 tokens each.

## Cross-References

- [what/lattices/AGENTS](../AGENTS.md) — Lattice YAML ecosystem overview
- [what/lattices/tools/AGENTS](../tools/AGENTS.md) — Validation and conversion tools
- `../lattice_yaml_schema.json` — JSON Schema for validation
- `../canvas_yaml_interop.md` — Canvas ↔ YAML bidirectional mapping
- Canvas Standard v1.0.0 — Node type mapping, edge conventions, layout patterns
