---
type: directory_index
created: 2026-06-10
updated: 2026-06-10
last_edited_by: agent_hestia
tags: [directory_index, assets, emblems, node_adna, exemplar]
---

# who/assets/emblems/ — Per-vault topic emblems

Neon-heraldic **function logo per vault** (what the vault *does*, vs `sigils/` = who its persona *is*).
First lookup in the icon chain both shipped generators use — `build_curation_cards.py` resolves
`icon_path` as **emblem > persona sigil > category crest**, and `build_topology_canvas.py` embeds the
same emblem (falling back to sigil, else no icon) as the node's `![[icon|44]]` avatar. Graceful-skip
when absent: persona-less vaults without an emblem simply render off the band crest / no avatar.

**Naming**: `<Vault>.aDNA.png` — the inventory `name:` exactly, including the `.aDNA` suffix
(e.g. `SiteForge.aDNA.png`).

**Generate**: square (1:1), dark `#16161e` ground, neon-heraldic medallion motif + the vault's
function symbol; one category hue + cyan accents. Style-lock by passing 2–3 existing emblems/sigils
as reference images. **No-text clause** (reference-node finding F-M2.4-A): concept-words render as
stray letters — prompt for *de-labelled symbols only*. Reference node used the Gemini image pipeline
(`what/code/api_helpers.py image_generate`, ~$0.04/img). Not bundled — generate per node as the
fleet grows; placeholder-free dirs are the documented day-1 state.
