---
type: directory_index
created: 2026-02-19
updated: 2026-10-20
last_edited_by: agent_rosetta
tags: [directory_index, lattice, tools, compliance]
---

# what/lattices/tools/ — aDNA Tooling

## Purpose

Python utilities for validating aDNA objects, scoring compliance, and converting between `.lattice.yaml` and Obsidian `.canvas` formats.

## Tools

| Tool | Function |
|------|----------|
| `compliance_checker.py` | Score vault objects across 11 aDNA compliance dimensions (0–3 each; d11 derivability applies to registries only). Outputs YAML scorecard + MD report. |
| `lattice_validate.py` | Validate `.lattice.yaml` against JSON Schema + federation readiness checks. Enum values come from `faces/lattice.schema.json` |
| `adna_validate.py` | Validate aDNA instance conformance per §5.5 (starter/standard/full levels). `--governance` also checks stamp currency (aDNA.aDNA ADR-067 clause 4) |
| `faces/` | `lattice.schema.json`: a byte copy of the lattice master's generated face (LinkML.aDNA), pinned in `faces/upstream.json`. Re-vendor it from its source and update the pin; never edit it |
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
python adna_validate.py ~/aDNA/adna --governance        # Governance sync checks + stamp currency
```

**Stamp currency** (`--governance`): every generated face that carries `Master: <path>  sync_hash: <hex>` (or `source_sha256:` on a canvas twin), and every copy pinned in an `upstream.json`, is re-hashed against its master or source. A mismatch is a **warning**. A master or source that is not on this node is reported **unverifiable** (an info line), never failed.

**Dates in frontmatter**: YAML loads an unquoted `2026-10-20` as a date object, not a string. Before validating frontmatter against a JSON Schema (such as `frontmatter_schema.json`), convert date values to ISO strings, for example `json.loads(json.dumps(data, default=str))`. Otherwise every date field fails a `type: string` rule.

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
