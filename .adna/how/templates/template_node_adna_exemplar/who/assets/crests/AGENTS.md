---
type: directory_index
created: 2026-06-01
updated: 2026-06-01
last_edited_by: agent_hestia
tags: [directory_index, assets, crests, node_adna, exemplar]
---

# who/assets/crests/ — Category crest emblems

Neon heraldic emblem per pattern category, embedded by `build_topology_canvas.py` as a band-header
emblem in the topology canvas's left gutter (graceful-skip if absent).

**Naming**: `<category_slug>.png` — `forge` · `framework` · `platform` · `org_vault` · `org_graph` · `network` · `coordination` · `node_tooling`.

**Generate**: square (1:1), dark `#16161e` ground (no transparency needed), one category hue + cyan accents. The reference node used the Gemini image pipeline (`what/code/api_helpers.py image_generate`). Not bundled — generate per node (or skip; the canvas falls back to the category glyph in the band label).
