---
type: decision
adr_id: adr_002
adr_number: 2
title: "YAML as Lattice Canonical Format"
status: accepted
created: 2026-03-18
updated: 2026-03-18
last_edited_by: agent_init
supersedes:
superseded_by:
tags: [adr, decision, yaml, lattice, format]
---

# ADR-002: YAML as Lattice Canonical Format

## Status

Accepted

## Context

Lattices — directed graphs of connected modules — need a canonical serialization format. Requirements:
- Human-readable and human-editable (non-engineers must be able to understand and modify)
- Compatible with Obsidian frontmatter (YAML is already the vault metadata language)
- Supports nested structures (nodes, edges, metadata, FAIR annotations)
- Parseable by AI agents without specialized tooling
- Diffable in git (line-oriented text, not binary or minified)

Alternatives evaluated: JSON (verbose, no comments, harder to hand-edit), TOML (weak nested support), CUE (powerful but unfamiliar to most users), Protocol Buffers (binary, requires compilation).

## Decision

Use **YAML** as the canonical format for lattice definitions (`.lattice.yaml`). YAML serves triple duty:
1. **Frontmatter** in Markdown files (type, status, tags)
2. **Object definitions** for modules (`.module.yaml`), datasets (`.dataset.yaml`), and lattices (`.lattice.yaml`)
3. **State tracking** (`.lattice_state.yaml` for deployment state)

The lattice YAML schema defines:
- `nodes` — module references with typed inputs/outputs
- `edges` — connections between node ports (type-checked)
- `metadata` — version, description, FAIR annotations
- `execution` — mode (sequential, parallel, event-driven), runtime config

## Consequences

### Positive
- Single format across frontmatter, objects, and state — reduces cognitive overhead
- Human-readable without tooling — scientists and non-engineers can inspect lattice definitions
- AI agents parse YAML natively — no custom deserializer needed
- Git-friendly diffs for change tracking and review

### Negative
- YAML's implicit typing can cause surprises (e.g., `on` parsed as boolean, Norway problem)
- Deep nesting becomes hard to read beyond 4-5 levels
- No native schema validation — requires external tooling or runtime checks

### Neutral
- YAML 1.2 (strict) is the target spec, avoiding YAML 1.1 implicit typing issues
- Round-trip fidelity (comments, ordering) requires specialized YAML libraries in some languages
