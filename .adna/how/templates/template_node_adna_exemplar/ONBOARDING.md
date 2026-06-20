---
type: reference
title: "Welcome — your exemplar Home vault, first run"
created: 2026-06-10
updated: 2026-06-10
status: active
last_edited_by: agent_hestia
tags: [reference, onboarding, exemplar, node_adna, first_run]
---

# Welcome — first run of your exemplar Home vault

This vault was laid down from `template_node_adna_exemplar/` — the premium, generator-driven node
home (persona banner → landing strip → dashboard band → Bases §Gallery → topology canvas → disclosure
folds). This file is your **one-time setup walkthrough**: work it top-to-bottom (~15 min + optional
imagery), then delete it — it carries no `{{vars}}` and nothing else links to it.

> **Where this sits in the bigger flow**: the base `.adna` fork/bootstrap (`skill_project_fork` →
> first-open `skill_onboarding` → `skill_node_bootstrap_interview`) creates the vault and fills
> identity. This walkthrough is the **exemplar layer on top** — it assumes that base flow ran (or
> that you copied the bundle by hand) and gets the *presentation* system live. It does not repeat
> base onboarding.

## 0 · What you're looking at

| Surface | File | Fed by |
|---|---|---|
| Home page | `HOME.md` | `what/inventory/inventory_vaults.yaml` via the two generators |
| §Gallery cards | `what/inventory/curation_gallery.base` (Bases) | `who/curation/*.yaml` ← `build_curation_cards.py` |
| Topology canvas | `what/canvas/topology.canvas` | `build_topology_canvas.py` (inventory + relationships seed) |
| Theming | `.obsidian/snippets/<persona>_accent.css` + `<persona>_canvas.css` | your persona accent values |

Nothing on the home page is hand-maintained: vault lists, cards, and the canvas all regenerate from
inventory. **If you see literal `{{placeholders}}` anywhere**, the substitution step hasn't run —
go back to `skill_node_bootstrap_interview.md` Step 9 (or render by hand per `SUBSTITUTIONS.md` in
the template bundle) before continuing.

## 1 · Make it yours (5 min)

1. **Persona + accents** — the exemplar is persona-portable (Hestia is the reference, not a rule).
   Your persona's accent triple + canvas text pair live in the two snippet files; the default lookup
   table is `SUBSTITUTIONS.md` §2 in the template bundle. Edit the hex values in place if you want a
   different mood — only solid color stops are persona-tokened; rgba() translucents are shared design
   constants, leave them.
2. **Banner** — drop a real hero image (≈1920×400) into `who/assets/banners/` and point HOME's
   frontmatter `feature:` + the `<img src=…>` banner line at it. Until then the grey
   `banner_placeholder.png` renders (by design — honest day-1 state).
3. **Greeting** — the one italic line under the identity row. Make it sound like your persona.

## 2 · Enable the rendering stack (3 min, Obsidian settings)

- **Appearance → CSS snippets**: enable **both** `<persona>_accent.css` and `<persona>_canvas.css`.
  (Without the canvas snippet, canvas cards show literal `<span class="cf-pill">…` text.)
- **Core plugins**: enable **Bases** (the §Gallery cards view).
- **Community plugins**: **Advanced Canvas** (topology canvas) + **Meta Bind** (the `adna.network`
  landing button). Dataview is *optional* (a dormant legacy gallery path — skip it).

## 3 · First regen (2 min, terminal at the vault root)

```bash
# Use `python`, NOT `python3` — the generators need PyYAML and on many nodes
# (including the reference) only `python` has it. smoke/parity tools are stdlib-safe.
mv what/canvas/topology_relationships.yaml.template what/canvas/topology_relationships.yaml  # if not already renamed

python what/code/build_curation_cards.py          # §Gallery cards from inventory

CANVAS_CORE_HOME=/path/to/Canvas.aDNA/what/production \
TOPOLOGY_GENERATED_DATE=$(date +%F) \
python what/code/build_topology_canvas.py         # the topology canvas
python what/code/build_topology_canvas.py --check # objective layout gate (schema + overlaps)
```

- `CANVAS_CORE_HOME` points at the `canvas_core` substrate — canonical `Canvas.aDNA/what/production/canvas_core`
  per Canvas **ADR-004**, lands at **PT P5**; until then it resolves via the `CanvasForge.aDNA` archive shim
  (`CANVASFORGE_CODE` is a deprecated alias). `canvas_core` needs `canvas_std` too — the generator auto-adds
  `Canvas.aDNA/what/code/canvas_std/src` (ADR-004 §4), or install `adna-canvas-std`. The topology canvas is
  optional — skip it if the substrate isn't present.
- The canvas is **deterministic** — re-runs are byte-identical until inputs change.
- Edit `topology_relationships.yaml` to declare succession/kinship/sequencing ties (federation edges
  are auto-probed from wrapper dirs; empty lists are valid). See `what/canvas/AGENTS.md`.

## 4 · Imagery, at your pace (optional, ~$0.04/image)

Empty asset dirs are the **documented day-1 state** — everything renders with graceful fallbacks.
When ready, each dir's `AGENTS.md` carries its naming convention + generation recipe:

1. `who/assets/sigils/` — persona avatars (gallery portrait fallback + canvas avatar)
2. `who/assets/emblems/` — per-vault function logos (first pick in the icon chain)
3. `who/assets/crests/` — category band-headers on the canvas
4. `glyphs/` + `backplates/` — **reserve classes; skip** until a consumer is wired (their AGENTS.md explain)

Track what you generate in `who/assets/asset_registry.yaml`. Style discipline: dark `#16161e`
ground, your accent + cyan, **no text in the image** (words leak as broken letters).

## 5 · Verify (2 min)

1. Open `HOME.md` in reading view — banner (or placeholder), landing strip, dashboard band, gallery
   cards, all four folds collapsed.
2. Open the topology canvas — bands + legend rail render; cards show pills/glyphs (if not → §2).
3. `python what/code/build_topology_canvas.py --check` exits 0.
4. **Operator eye** — the standing rule from the reference node: *no canvas ships without a human
   look at the rendered surface.* If it doesn't feel premium yet, iterate §1 colors + §4 imagery.

## 6 · Living with it

- **On inventory change**: `skill_inventory_refresh` → `python what/code/build_curation_cards.py` →
  regen the canvas → commit inventory + cards together (the HOME folds tell you this too).
- **Style tuning without code edits**: optional `what/canvas/canvas_style.yaml`
  (`CANVAS_STYLE_OVERRIDE`) — colors, geometry, band order. Absent = byte-stable default.
- **Stay current with the exemplar**: the reference bundle evolves (parity-swept by its campaign);
  diff your snippets/generators against a fresh `template_node_adna_exemplar/` when you sync.

*Done? Delete this file (`ONBOARDING.md`) — your vault's own `AGENTS.md`/`CLAUDE.md` govern from here.*
