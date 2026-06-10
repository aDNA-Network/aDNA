---
type: directory_index
created: 2026-02-17
updated: 2026-02-19
last_edited_by: agent_init
tags: [directory_index, lattice]
---

# what/lattices/ — Lattice YAML Definitions

## Purpose

This directory contains the Lattice YAML ecosystem: schema definitions, conversion tools, interop specifications, and example lattice files.

## Contents

| Path | Purpose |
|------|---------|
| `lattice_yaml_schema.json` | JSON Schema for `.lattice.yaml` validation |
| `canvas_yaml_interop.md` | Bidirectional mapping spec between `.lattice.yaml` and Obsidian `.canvas` |
| `tools/` | Python tools for validation and conversion |
| `examples/` | Example `.lattice.yaml` files |

## Tools

| Tool | Function | Usage |
|------|----------|-------|
| `tools/lattice_validate.py` | Validate `.lattice.yaml` against schema | `validate_lattice(data)` or `validate_lattice_file(path)` |
| `tools/lattice2canvas.py` | Convert `.lattice.yaml` → Obsidian `.canvas` | `lattice_to_canvas(data)` or `lattice_file_to_canvas(yaml_path, canvas_path)` |
| `tools/canvas2lattice.py` | Convert `.canvas` → `.lattice.yaml` | `canvas_to_lattice(data)` or `canvas_file_to_lattice(canvas_path, yaml_path)` |

### Installation

```bash
pip install -r tools/requirements.txt  # pyyaml only
```

### Quick Start

```python
from what.lattices.tools import validate_lattice_file, LatticeValidationResult

result = validate_lattice_file("examples/deep_research.lattice.yaml")
print(f"Valid: {result.valid}")
for error in result.errors:
    print(f"  Error: {error}")
```

## Examples

| File | Type | Description |
|------|------|-------------|
| `examples/hello_world.lattice.yaml` | pipeline (workflow) | Minimal valid lattice for onboarding |
| `examples/deep_research.lattice.yaml` | pipeline (hybrid) | Multi-agent research pipeline with validation loops |
| `examples/research_orchestrator.lattice.yaml` | agent (hybrid) | Orchestrator for deep research process |
| `examples/protein_binder_design.lattice.yaml` | pipeline (workflow) | Computational protein design pipeline with federation |
| `examples/knowledge_base.lattice.yaml` | context_graph (reasoning) | Knowledge retrieval + reasoning lattice |
| `examples/docking_assessment.lattice.yaml` | pipeline (workflow) | Sub-lattice extraction with full federation properties |

## Lattice Types

| Type | Description | Mode |
|------|-------------|------|
| `pipeline` | Deterministic DAG of modules | `workflow` |
| `agent` | LLM-driven reasoning | `reasoning` |
| `context_graph` | Knowledge structure | varies |
| `workflow` | Operational process | `workflow` |

## Federation & Sub-Lattice Extraction

Lattices support optional `federation` metadata for cross-instance sharing:

| Property | Purpose |
|----------|---------|
| `shareable` | Whether this lattice can be shared with other instances |
| `source_instance` | Originating aDNA instance identifier |
| `parent_lattice` | Source lattice name (for extracted sub-lattices) |
| `version_policy` | Upstream tracking: `locked`, `patch`, `minor`, `latest` |
| `extracted_nodes` | Node IDs extracted from parent — must exist in this lattice's nodes |

**Sub-lattice extraction pattern**: Extract a subset of nodes from a parent lattice into a standalone `.lattice.yaml`. Set `federation.parent_lattice` to the source name and `federation.extracted_nodes` to the list of node IDs carried over. The validator cross-checks that all listed node IDs exist in the new lattice's `nodes` array.

## Load/Skip Decision

**Load this directory when**:
- Working with `.lattice.yaml` files — authoring, validating, or converting
- Understanding the lattice type system (pipeline, agent, context_graph, workflow)
- Creating a new lattice and need schema reference or examples

**Skip when**:
- Performing operational work (sessions, missions, campaigns) not involving lattice definitions
- Working on context library, governance, or CRM content
- Already inside a specific subdirectory (tools/ or examples/) — load that AGENTS.md directly

**Token cost**: ~550 tokens (this AGENTS.md). Subdirectories: tools/ AGENTS.md (~400 tokens), examples/ AGENTS.md (~250 tokens).

## Cross-References

- [what/AGENTS](../AGENTS.md) — Knowledge layer index
- [what/lattices/tools/AGENTS](tools/AGENTS.md) — Python validation and conversion tools
- [what/lattices/examples/AGENTS](examples/AGENTS.md) — Reference lattice implementations
- [canvas_yaml_interop](canvas_yaml_interop.md) — Interop specification
