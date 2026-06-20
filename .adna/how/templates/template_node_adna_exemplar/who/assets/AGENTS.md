---
type: directory_index
created: 2026-06-01
updated: 2026-06-01
last_edited_by: agent_hestia
tags: [directory_index, assets, node_adna, exemplar]
---

# who/assets/ — Node Imagery

Premium imagery for the exemplar HOME: `banners/` (hero), `portraits/` (personae), `dividers/` (section art), `vault_cards/` (per-vault product cards), `screenshots/`, `diagrams/`. The §Gallery in `HOME.md` reads `vault_cards/` + `portraits/` *indirectly* via the curation cards in `who/curation/`.

**Canvas/gallery icon system** (M2.4 backbone): `emblems/` (per-vault function logos) · `sigils/` (persona avatars) · `crests/` (category band-headers) — the generators resolve icons **emblem > sigil > crest** with graceful-skip, so empty dirs are a valid day-1 state. `glyphs/` + `backplates/` are **reserve classes** (no consumer wired yet — see their AGENTS.md). Per-dir AGENTS.md carries each naming convention + generation recipe.

**No binaries ship in the template** except `banners/banner_placeholder.png` (a grey 1920×400 stand-in). Replace it with your real banner and set `{{banner_image}}` in HOME. Track asset state in `asset_registry.yaml`.
