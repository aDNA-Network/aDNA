---
type: directory_index
created: 2026-02-19
updated: 2026-03-21
last_edited_by: agent_init
tags: [directory_index, lattice, tools, compliance]
---

# what/lattices/tools/ — aDNA Tooling

## Purpose

Python utilities for validating aDNA objects, scoring compliance, and converting between `.lattice.yaml` and Obsidian `.canvas` formats.

## Tools

| Tool | Function |
|------|----------|
| `compliance_checker.py` | Score vault objects across 10 aDNA compliance dimensions. Outputs YAML scorecard + MD report. |
| `lattice_validate.py` | Validate `.lattice.yaml` against JSON Schema + federation readiness checks |
| `adna_validate.py` | Validate aDNA instance conformance per §5.5 (starter/standard/full levels) |
| `lattice2canvas.py` | Convert `.lattice.yaml` → Obsidian `.canvas` |
| `canvas2lattice.py` | Convert Obsidian `.canvas` → `.lattice.yaml` |
| `frontmatter_schema.json` | JSON Schema for aDNA frontmatter validation |

## Dependencies

```bash
pip install -r requirements.txt  # pyyaml only
```

No additional dependencies beyond `pyyaml` and the Python standard library.

## Quick Usage

### Score vault compliance

```bash
python compliance_checker.py ~/aDNA/<project_name>.aDNA                    # Score all objects
python compliance_checker.py ~/aDNA/<project_name>.aDNA --type module      # Filter by type
python compliance_checker.py ~/aDNA/<project_name>.aDNA --file what/modules/x.md  # Single file
python compliance_checker.py ~/aDNA/<project_name>.aDNA --output yaml -v   # YAML only, verbose
```

### Validate a lattice file

```python
from what.lattices.tools.lattice_validate import validate_lattice_file

result = validate_lattice_file("examples/deep_research.lattice.yaml")
print(f"Valid: {result.valid}")
for error in result.errors:
    print(f"  Error: {error}")
```

### Validate an aDNA instance

```bash
python adna_validate.py ~/aDNA/adna                     # Auto-detect level
python adna_validate.py ~/aDNA/adna --level standard    # Check specific level
python adna_validate.py ~/aDNA/adna --governance        # Governance sync checks
```

### Convert lattice to canvas

```python
from what.lattices.tools.lattice2canvas import lattice_file_to_canvas

lattice_file_to_canvas("input.lattice.yaml", "output.canvas")
```

### Convert canvas to lattice

```python
from what.lattices.tools.canvas2lattice import canvas_file_to_lattice

canvas_file_to_lattice("input.canvas", "output.lattice.yaml")
```

## Load/Skip Decision

**Load this directory when**:
- Scoring vault compliance or running pre-upgrade audits
- Validating a new or modified `.lattice.yaml` file against the schema
- Validating aDNA instance conformance (starter/standard/full)
- Converting between `.lattice.yaml` and Obsidian `.canvas` formats
- Debugging validation errors or extending the tooling

**Skip when**:
- Working on non-lattice, non-compliance tasks (sessions, CRM, general context)
- Reading or authoring YAML manually without needing programmatic validation

**Token cost**: ~500 tokens (this AGENTS.md). `compliance_checker.py` is ~1085 lines; other Python files are ~200-460 lines each.

## Cross-References

- [what/lattices/AGENTS](../AGENTS.md) — Lattice YAML ecosystem overview
- [what/lattices/examples/AGENTS](../examples/AGENTS.md) — Reference lattice implementations
- `../lattice_yaml_schema.json` — JSON Schema used by the validator
- `../canvas_yaml_interop.md` — Bidirectional mapping specification
