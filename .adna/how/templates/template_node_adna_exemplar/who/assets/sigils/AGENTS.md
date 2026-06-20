---
type: directory_index
created: 2026-06-01
updated: 2026-06-01
last_edited_by: agent_hestia
tags: [directory_index, assets, sigils, node_adna, exemplar]
---

# who/assets/sigils/ — Persona sigil emblems

Neon circular avatar sigil per persona codename. `build_curation_cards.py` uses
`who/assets/sigils/<persona>.png` as the §Gallery `persona_portrait` **fallback** when no painterly
`portraits/portrait_<persona>.jpg` exists (gap-fill for personas postdating the portrait set).

**Naming**: `<persona>.png` (lowercase codename, e.g. `hestia.png`).

**Generate**: square (1:1), dark `#16161e` ground, persona-archetype motif + persona accent + cyan. Not bundled — generate per node as needed.
