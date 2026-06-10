---
type: template
created: 2026-03-08
updated: 2026-03-08
status: active
last_edited_by: agent_init
tags: [template, registry, federation]
---

# Template: Registry Entry

Use this template when preparing a lattice for registry publication. It documents the metadata fields required for federation sharing, FAIR compliance, and discoverability.

## Required Federation Block

Add this block to your `.lattice.yaml` under the top-level `lattice:` key:

```yaml
federation:
  shareable: true                    # Must be true for publication
  source_instance: adna              # Your vault/instance identifier
  version_policy: minor|locked|major # How downstream updates are handled
```

### Version Policy

| Policy | Meaning |
|--------|---------|
| `minor` | Downstream receives patch/minor updates automatically |
| `locked` | Pinned to exact version at time of pull — no auto-updates |
| `major` | Only major version bumps propagate |

### Extracted Sub-Lattices

If this lattice was extracted from a parent, add:

```yaml
federation:
  shareable: true
  source_instance: adna
  parent_lattice: parent_name        # Name of the source lattice
  version_policy: locked
  extracted_nodes: [node_a, node_b]  # Nodes extracted from parent
```

## Required FAIR Metadata

Every published lattice must include a `fair:` block:

```yaml
fair:
  license: "MIT"                     # SPDX identifier (required)
  creators:                          # At least one creator (required)
    - "Your Name or Org"
  keywords:                          # 3+ semantic tags (required)
    - keyword_one
    - keyword_two
    - keyword_three
  identifier: ""                     # DOI or persistent ID (optional)
  provenance: >                      # Origin and methodology (recommended)
    Description of how this lattice was developed
    and what problem it solves.
```

## Lattice Type Discriminator

The `lattice_type` field determines how the registry classifies your lattice:

| Type | Description |
|------|-------------|
| `pipeline` | Deterministic DAG of modules |
| `agent` | LLM-driven reasoning lattice |
| `context_graph` | Knowledge structure |
| `workflow` | Operational process |
| `skill` | Encapsulated agent capability (see Skill–Lattice Interop Standard) |

## Naming Conventions

- **File**: `name.lattice.yaml` — always underscores, never hyphens
- **Lattice name**: Must match filename stem (e.g., `protein_binder_design`)
- **Version**: Semantic versioning (`"1.0.0"`, `"2.1.0"`)

## Federation Readiness Checklist

Before publishing, verify all 6 checks pass:

- [ ] `federation.shareable` is `true`
- [ ] `federation.source_instance` is set
- [ ] `federation.version_policy` is set (`minor`, `locked`, or `major`)
- [ ] `fair.license` is set (SPDX identifier)
- [ ] `fair.keywords` has 3+ entries
- [ ] `lattice_type` is a valid discriminator value

## Example

See `what/lattices/examples/protein_binder_design.lattice.yaml` for a fully federation-ready lattice with all required fields.

## Related

- **Publish workflow**: `how/skills/skill_lattice_publish.md`
- **Lattice standard**: `what/lattices/standard_lattice.md`
- **Skill–Lattice Interop**: For `lattice_type: skill` entries
