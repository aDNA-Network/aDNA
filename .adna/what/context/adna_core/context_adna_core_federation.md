---
type: context_guide
topic: adna_core
subtopic: federation
created: 2026-02-20
updated: 2026-03-18
sources: ["Lattice Federation & Sharing Protocol v1.0 (lattice_federation.md)", "Lattice YAML Schema (federation block)", "Lattice Interop Standard v1.0 (lattice_interop.md)"]
context_version: "1.0"
token_estimate: ~1000
last_edited_by: agent_init
tags: [context, adna_core, federation, sharing, composition, uri]
quality_score: 4.2
signal_density: 5
actionability: 4
coverage_uniformity: 4
source_diversity: 3
cross_topic_coherence: 4
freshness_category: stable
last_evaluated: 2026-02-20
---

# aDNA Core: Federation Guide

> **Scope note**: This file is the concrete aDNA protocol distillation — how to federate lattices using the defined protocol. For general federation and composability research patterns (SPARQL federation, SHACL, MOMo, FAIR principles), see `prompt_engineering/federation_composability`.

## Key Principles

1. **Federation is a 5-capability lifecycle.** Validate → Export → Share → Import → Compose. Each capability maps to a state transition.

2. **Import triggers ontology unification.** Federation is not just file transfer — every import runs the ontology compatibility check (M9 merge algorithm).

3. **Two composition patterns are available.** Inline (merge child nodes with namespace prefix) and external reference (child as opaque node via URI). They are mutually exclusive per composition.

4. **Schema is sufficient.** The `federation` block (5 properties) in `lattice_yaml_schema.json` provides all metadata needed. No schema changes required.

## Federation Lifecycle

```
Private → Shareable → Exported → Shared → Imported → Composed
           (validate)   (export)   (share)   (import)   (compose)
```

### Readiness Criteria (6 checks)

| # | Criterion | How to Verify |
|---|-----------|--------------|
| 1 | Schema validation passes | Run `lattice_validate.py` |
| 2 | `federation.shareable: true` | Explicit opt-in |
| 3 | `federation.source_instance` set | Provenance established |
| 4 | `fair.license` declared | Legal clarity |
| 5 | `fair.keywords` ≥ 1 | Findability |
| 6 | All `ref` fields resolve or use URIs | No broken references |

## URI Scheme

Cross-instance references use `lattice://`:

```
lattice://<instance_id>/<lattice_name>[/<node_id>]
```

| Component | Pattern | Example |
|-----------|---------|---------|
| `instance_id` | `[a-z][a-z0-9-]*` (hyphens, DNS-safe) | `adna` |
| `lattice_name` | `[a-z][a-z0-9_]*` (underscores, schema-match) | `docking_assessment` |
| `node_id` | `[a-z][a-z0-9_]*` (optional) | `structure_prediction` |

**Resolution**: Instance → filesystem/git lookup → lattice file → node within lattice.

## Composition Patterns

### Inline Composition

Child nodes merge into parent with namespace prefix.

| Property | Detail |
|----------|--------|
| Node visibility | Child nodes become first-class in parent |
| ID format | `{child_name}_{node_id}` |
| Token cost | +N tokens (all child nodes materialized) |
| When to use | Parent needs fine-grained access to child nodes |
| Seam edges | Required: parent → child entry, child exit → parent |

### External Reference

Child appears as single opaque node with `lattice://` URI.

| Property | Detail |
|----------|--------|
| Node visibility | Child internal structure is opaque |
| Node type | `module` with `ref: lattice://...` |
| Token cost | +1 token (single opaque node) |
| When to use | Parent treats child as black-box |
| Seam edges | Required: edges to/from opaque node with `data_mapping` + `port` |

**Default recommendation**: External reference — minimizes token cost while preserving composability.

## Seam Edge Specification

Seam edges connect parent to child across composition boundaries:

```yaml
# External reference seam edge
- from: parent_sequence_design
  to: docking_assessment                # opaque child node
  label: "designed sequences for validation"
  data_mapping:
    sequences: input_sequences           # explicit mapping required
  port: structure_prediction             # identifies child entry node
```

**Rules**:
- At least one edge into child entry and one out of child exit
- Explicit `data_mapping` required — no implicit pass-through
- `port` field identifies child entry/exit nodes for external references

## Interop Conventions

### Interface Descriptors (Design-Time)

Lattices may declare interfaces via a `lattice_interface` metadata node:

```yaml
- id: lattice_interface
  type: process
  description: "Interface descriptor"
  config:
    interface_version: "1.0.0"
    entry_nodes: [structure_prediction]
    exit_nodes: [ranking]
    ports:
      structure_prediction:
        accepts: [pdb_structure, fasta_sequence]
      ranking:
        produces: [binding_scores, ranked_candidates]
```

### Version Drift Detection (Runtime)

| Policy | Behavior |
|--------|----------|
| `locked` | HALT if any version change |
| `patch` | Accept patches, halt on minor/major |
| `minor` | Accept minor, halt on major |
| `latest` | Always use latest, warn on breaking changes |

Breaking changes: node addition/removal, port rename, type change. Non-breaking: description change, config addition, label change.

## Pre-Federation Checklist

- [ ] Lattice passes schema validation (0 errors)
- [ ] `federation.shareable: true` set deliberately
- [ ] `federation.source_instance` matches your instance
- [ ] `fair.license` is set and accurate
- [ ] All `ref` fields resolve locally or are valid URIs
- [ ] No sensitive/proprietary data in node configs
- [ ] `fair.provenance` describes origin

## Post-Federation Checklist

- [ ] Imported lattice passes validation in target context
- [ ] Ontology compatibility verified (or conflicts resolved per M9)
- [ ] Composed parent passes validation
- [ ] All seam edges have explicit `data_mapping`
- [ ] Unresolved URIs logged and documented
- [ ] Provenance chain intact

## Sources

1. Lattice Federation & Sharing Protocol v1.0 — full 5-capability specification with worked round-trip
2. Lattice YAML Schema — federation block definition (5 properties)
3. Lattice Interop Standard v1.0 — interface descriptors, runtime data flow, version drift
