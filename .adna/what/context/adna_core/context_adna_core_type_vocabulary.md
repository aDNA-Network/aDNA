---
type: context_guide
topic: adna_core
subtopic: type_vocabulary
created: 2026-03-02
updated: 2026-03-18
sources: ["campaign_adna_lattice/artifacts/m16_type_vocabulary.md"]
context_version: "1.0"
token_estimate: ~500
last_edited_by: agent_init
tags: [context, adna_core, type_vocabulary, module, io]
quality_score: 4.0
signal_density: 4
actionability: 4
coverage_uniformity: 4
source_diversity: 3
cross_topic_coherence: 5
freshness_category: durable
last_evaluated: 2026-03-17
---

# aDNA Core: Type Vocabulary

## Key Principles

1. **19 canonical types across 4 tiers.** The type vocabulary standardizes module I/O annotations and lattice edge `data_mapping` entries. Types are descriptive (documenting what flows), not prescriptive (no runtime enforcement in v1.0).

2. **Snake_case naming, file types end in `_file`.** Consistent with aDNA naming conventions. `pdb_file` not `PDB`, `score_table` not `ScoreTable`. File format types are distinguished from data concept types.

3. **Tiers scope from universal to domain-specific.** Tier 1 (primitives) and Tier 2 (structured) are domain-neutral. Tier 3 (molecular biology) and Tier 4 (media) are domain extensions.

4. **Cardinality uses bracket notation.** `list[pdb_file]` for sequences, `map[string, float]` for key-value mappings. Base type names are always singular.

5. **Covers 95%+ of current usage.** Based on scan of 30+ modules and 9+ lattice YAMLs. Extensible — new types can be added without breaking existing annotations.

## Type Reference

### Tier 1 — Primitives (6)

| Type | Description | Examples |
|------|-------------|---------|
| `string` | Text value | Prompts, names, descriptions |
| `integer` | Whole number | Counts, indices, lengths |
| `float` | Decimal number | Scores, thresholds, weights |
| `boolean` | True/false | Feature toggles, requirements |
| `path` | File/directory path or URI | Input files, model paths |
| `list` | Ordered sequence | Residue lists, parameter arrays |

### Tier 2 — Structured (4)

| Type | Description | Examples |
|------|-------------|---------|
| `config` | Configuration object (YAML/JSON) | Module parameters, run overrides |
| `tensor` | N-dimensional numeric array | Embeddings, contact maps, PAE matrices |
| `score_table` | Tabular metrics output | pLDDT scores, binding energies, rankings |
| `markdown` | Formatted text | Reports, summaries, documentation |

### Tier 3 — Molecular Biology (7)

| Type | Description | Formats |
|------|-------------|---------|
| `pdb_file` | Protein/molecular 3D structure | PDB, mmCIF, CIF |
| `fasta_file` | Biological sequence(s) | FASTA, multi-FASTA |
| `smiles` | Molecular structure string | SMILES, SDF, MOL |
| `alignment` | Multiple sequence alignment | A3M, MSA, Stockholm |
| `trajectory` | Molecular dynamics trajectory | DCD, XTC, TRR |
| `vcf` | Genetic variant calls | VCF |
| `audio` | Audio/voice waveform | WAV, MP3, PCM stream |

### Tier 4 — Media (2)

| Type | Description | Formats |
|------|-------------|---------|
| `image` | Visual media | PNG, JPG, SVG, TIFF |
| `document` | Structured document | PDF, DOCX, HTML |

## Recommendations

- **Use canonical type names in module `inputs:` and `outputs:` blocks.** Avoid ad hoc descriptions like "PDB file" or "CSV metrics" — use `pdb_file` and `score_table`.
- **Use cardinality notation for collections.** `list[pdb_file]` not `pdb_files`. `map[string, score_table]` for keyed collections.
- **Add new domain types at Tier 3.** Follow the naming pattern: snake_case, file formats get `_file` suffix. Register in the type vocabulary artifact.
- **Reference type vocabulary in FAIR metadata.** The `interoperable.format` field in FAIR envelopes should use vocabulary types.

## Anti-Patterns

- **Don't use framework-specific type names.** `tensor` not `pytorch_tensor` or `numpy_array`.
- **Don't pluralize type names.** `list[string]` not `strings`. Cardinality is a separate concern.
- **Don't use types for runtime validation yet.** The vocabulary is descriptive in v1.0. Runtime type checking is deferred to the build system campaign.

## Sources

- Type Vocabulary (Decision 10): module I/O annotation standard
- Module Standard: canonical module frontmatter and YAML fields
