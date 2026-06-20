---
type: directory_index
created: 2026-06-01
updated: 2026-06-10
last_edited_by: agent_hestia
tags: [directory_index, canvas, topology, node_adna, exemplar, template]
---

# what/canvas/ — Generated Topology Canvas (exemplar regen docs)

## Purpose

Holds the node's **topology canvas** — an Obsidian Advanced Canvas map of the vault-of-vaults (every
installed `.aDNA` vault grouped by pattern category) plus the WHO/WHAT/HOW triad. It is the **spatial
twin of the §Gallery** in `HOME.md`: every vault title on the canvas is a hotspot into that vault's
curation card. Generator-driven (compliance-campaign M24 pattern; templatized at M25).

## Directory Structure (at bootstrap)

```
what/canvas/
├── AGENTS.md (this file)
├── topology_relationships.yaml   # hand-authored edges + code-repo annotations (INPUT; rename from .template)
└── topology.canvas               # GENERATED — do not hand-edit (created by first regen)
```

## Input → Generator → Output

`topology.canvas` is a **generated artifact**. Never hand-edit it — edits are silently lost on the next
rebuild. Change an input instead:

| To change… | Edit | The generator then… |
|---|---|---|
| a node (vault) or its category | `what/inventory/inventory_vaults.yaml` | adds/moves the node automatically |
| a federation edge | nothing — drop/add the on-disk wrapper dir (`iii/`, `siteforge/`, …) | auto-probes it |
| a succession / kinship / sequencing edge, or a ⛓ code-repo annotation | `topology_relationships.yaml` (one line) | renders the edge/annotation |
| layout / colors / legend | `what/code/build_topology_canvas.py` | re-emits the canvas |

Regenerate (needs **PyYAML** — on the reference node that interpreter is `python` 3.12.2, *not*
`python3`, which lacks yaml):

```bash
python what/code/build_topology_canvas.py            # write the canvas
python what/code/build_topology_canvas.py --check    # validate only (schema + overlaps), no write
```

The generator is **deterministic** — output is a pure function of the two input files (fixed build date
+ sha256-of-inputs hash; no wall-clock), so re-runs don't churn git.

## Portability (set on a fresh node)

Two node-local values are env-overridable so the generator runs anywhere (defaults preserve the
reference node's behavior):

| env var | default | set it when… |
|---|---|---|
| `CANVAS_CORE_HOME` (alias `CANVASFORGE_CODE`) | `<workspace>/Canvas.aDNA/what/production` (P5+; interim → `CanvasForge.aDNA` archive) | the `canvas_core` producer engine (Canvas.aDNA, ADR-004; lands at PT P5) lives elsewhere on your node |
| `TOPOLOGY_GENERATED_DATE` | `2026-05-31` (reference) | always, on a fresh node — stamp your own build date |
| `CANVAS_STYLE_OVERRIDE` | `what/canvas/canvas_style.yaml` (**absent = no-op**, byte-stable) | you want bounded style/geometry tuning without editing the generator — optional YAML with `category_color:` / `edge_color:` / `state_dim:` / `geometry:` (node/band dims, `per_row`, `triad_x`) / `band_order:` (permutation of the category bands — the M2.1 de-spaghetti lever) |

```bash
CANVAS_CORE_HOME=/path/to/Canvas.aDNA/what/production \
TOPOLOGY_GENERATED_DATE=$(date +%F) \
python what/code/build_topology_canvas.py
```

## Substrate: `canvas_core` (Canvas.aDNA/what/production; ADR-004, lands PT P5)

The generator is built on the **`CanvasBuilder`** substrate — owned by **Canvas.aDNA** since the
CanvasForge→Canvas merge (pt09; canonical `Canvas.aDNA/what/production/canvas_core` per ADR-004, lands at PT
P5, via the `CanvasForge.aDNA` archive shim until then) — imported via `sys.path` from `$CANVAS_CORE_HOME`
plus `Canvas.aDNA/what/code/canvas_std/src` (`canvas_core` needs `canvas_std`, ADR-004 §4); see the consumer wrapper
`canvasforge/CLAUDE.md`. This gives:
- `CanvasBuilder.validate()` — Canvas Standard schema check.
- `canvas_core.spatial.detect_overlaps` / `containment_check` — the **objective layout gate** in
  `--check`: bands/lanes/callouts must not collide, every vault/entity node must sit inside its band.
  `--check` exits non-zero (refuses to write) on any schema error or layout violation.

> The generator self-heals a federation edge when you add/remove a wrapper dir, but a **vault rename**
> is count-stable and the auto-probe can't fix the hand-authored `topology_relationships.yaml` (it still
> names the old vault) — `--check` surfaces this as an `unresolved endpoint` flag. See
> `how/skills/skill_inventory_refresh.md` Step 9.5 for the rename-drift procedure.

Offline preview (no Obsidian needed): `python what/code/render_canvas_offline.py [canvas] [out.png]`
renders the `.canvas` geometry via matplotlib — useful before the vault is ever opened in Obsidian
(dev tool; the authoritative aesthetic check is the live render + operator eye).

## Design system (Prytaneion M2.2/M2.3 — ships in the generator)

The bundled generator carries the exemplar layout + chrome grammar; no extra setup beyond the snippet:

- **Layout (M2.2)**: category bands reordered for consumer-adjacency + barycenter node placement
  (crossing reduction); a bounded **legend group** ("Legend · how to read this canvas") anchored as a
  left rail under the triad lanes; resting edges muted (`EDGE_REST_DIM`) so the structure reads on the
  dark ground; snap-grid spacing throughout.
- **Node sizing (M2.3)**: degree-tiered — **hub** (total degree ≥6, ≈1.25× card) · **standard** ·
  **leaf** (degree 0–1, smaller); three discrete tiers, not a ramp, so the small-multiples discipline
  holds. Tier sizes scale off the `geometry:` override, so style-override tuning still flows through.
- **Card chrome (M2.3)**: status pills (`cf-active`/`cf-genesis`/`cf-dim`), corner category glyph,
  per-category accent stripe, typography grammar (bold = vault · italic = persona · mono = repo path).
  **Requires the canvas snippet**: the generator emits inline `<span class="cf-pill">`/`cf-glyph`
  accents that are invisible until `.obsidian/snippets/<persona>_canvas.css` (materialized from this
  bundle) is enabled in `appearance.json → enabledCssSnippets`, alongside the accent snippet.

## Hotspot Mechanism

Obsidian's vault root is the node vault, so sibling vaults live *outside* it and a canvas `file:` node
can't reach `../<Vault>/CLAUDE.md`. Vault nodes therefore wikilink to their **in-vault** curation card
(`who/curation/curation_<vault>.md`), which links onward to the real CLAUDE/MANIFEST/STATE. Triad entity
nodes → `<leg>/<entity>/AGENTS.md`; the meta node → `STATE.md`.

## Load/Skip Decision

**Load** when: building/regenerating the topology canvas, reasoning about vault relationships. **Skip**
otherwise. **Token cost**: ~600 tokens.
