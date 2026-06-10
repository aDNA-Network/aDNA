---
type: context_guide
topic: adna_core
subtopic: fair_mapping
created: 2026-03-02
updated: 2026-03-18
sources: ["campaign_adna_lattice/artifacts/m16_fair_canonical_mapping.md"]
context_version: "1.0"
token_estimate: ~500
last_edited_by: agent_init
tags: [context, adna_core, fair, mapping, federation]
quality_score: 4.0
signal_density: 4
actionability: 4
coverage_uniformity: 4
source_diversity: 3
cross_topic_coherence: 4
freshness_category: durable
last_evaluated: 2026-03-17
---

# aDNA Core: FAIR Mapping

## Key Principles

1. **Nested FAIR is canonical; flat FAIR is transport.** Vault frontmatter uses the full hierarchical `fair:` block (findable/accessible/interoperable/reusable). YAML files (`.lattice.yaml`, `.dataset.yaml`) use the compact flat form.

2. **Round-trip safe for core fields.** `flat → nested → flat` produces identical output. `nested → flat` loses extension fields (reproducibility, quality) that only exist in the nested form.

3. **Two required fields in both forms.** `keywords` (min 1) and `license` (SPDX identifier) are the minimum valid FAIR envelope. All other fields are optional.

4. **`creators` lives in flat YAML but in body text for nested.** This is the one asymmetry — flat FAIR has a `creators` list; nested FAIR puts attribution in the document body section.

## Field Correspondence

| Flat FAIR | Nested FAIR Path | Required |
|-----------|------------------|----------|
| `fair.keywords` | `fair.findable.keywords` | **Yes** |
| `fair.license` | `fair.accessible.license` | **Yes** |
| `fair.identifier` | `fair.findable.identifier` | No |
| `fair.creators` | (body section) | No |
| `fair.provenance` | `fair.reusable.provenance` | No |
| `fair.location` | `fair.accessible.location` | No |
| `fair.access_protocol` | `fair.accessible.access_protocol` | No |
| `fair.format` | `fair.interoperable.format` | No |
| `fair.schema` | `fair.interoperable.schema` | No |

## Recommendations

- **Use flat FAIR in `.lattice.yaml` and `.dataset.yaml`.** These are machine-parsed transport formats — flat is compact and sufficient.
- **Use nested FAIR in vault `.md` frontmatter.** The hierarchical structure is more readable for humans and supports extension fields.
- **Always include `keywords` and `license`.** These two fields are the minimum for FAIR compliance across both forms.
- **Use `access_protocol` enum values.** `direct` (local), `api` (REST/gRPC), `request` (manual), `https` (web), `container` (Docker/OCI).
- **Use type vocabulary for `format` field.** Reference canonical types from the type vocabulary (e.g., `pdb_file`, `fasta_file`, `score_table`).

## Examples

### Flat FAIR (in .lattice.yaml)

```yaml
fair:
  license: "MIT"
  keywords: [protein-design, binder, computational-biology]
  creators: ["Lattice Labs"]
  provenance: "Designed for de novo protein binder pipeline"
```

### Nested FAIR (in vault frontmatter)

```yaml
fair:
  findable:
    keywords: [protein-design, binder, computational-biology]
  accessible:
    license: "MIT"
    access_protocol: direct
  reusable:
    provenance: "Designed for de novo protein binder pipeline"
```

## Anti-Patterns

- **Don't mix flat and nested in the same file.** YAML files use flat; `.md` frontmatter uses nested. Never hybrid.
- **Don't omit `license` for shared objects.** License is the most critical FAIR field for federation trust.
- **Don't use `protocol` as a field name.** The canonical name is `access_protocol` (renamed for clarity in Decision 11).

## Sources

- FAIR Canonical Mapping (Decision 11): flat↔nested interconversion rules
- FAIR Principles: go-fair.org/fair-principles
