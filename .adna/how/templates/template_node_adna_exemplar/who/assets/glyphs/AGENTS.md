---
type: directory_index
created: 2026-06-10
updated: 2026-06-10
last_edited_by: agent_hestia
tags: [directory_index, assets, glyphs, node_adna, exemplar, reserve]
---

# who/assets/glyphs/ — Edge-relationship glyphs (reserve class)

Square neon glyph per **edge type** of the topology canvas: `federation` · `succession` · `kinship` ·
`sequencing`.

> **Reserve class — not yet auto-consumed.** Neither shipped generator embeds these PNGs; edge
> semantics currently render as edge *color + style* (see `what/canvas/AGENTS.md`). The reference
> node generated them at M2.4 for the parked legend/interaction layer (M2.5, plugin-gated). A fresh
> node should **skip generating these** until it wires a consumer — documented here so the asset
> taxonomy round-trips honestly.

**Naming**: `<edge_type>.png` (lowercase, e.g. `federation.png`).

**Generate** (when wired): square (1:1), dark `#16161e` ground, single de-labelled symbol in the
edge-type hue + cyan accents. **No-text clause** (F-M2.4-A) applies doubly here — relationship words
leak as letters; prompt pure symbols.
