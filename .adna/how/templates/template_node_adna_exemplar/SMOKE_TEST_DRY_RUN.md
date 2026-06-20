---
type: reference
title: "M25 Smoke Test — node-bravo dry-run"
created: 2026-06-01
updated: 2026-06-10
status: active
last_edited_by: agent_hestia
tags: [reference, template, exemplar, smoke_test, m25, prytaneion_m3_4, prytaneion_m6_1]
---

# Smoke Test — hypothetical `node-bravo.aDNA` dry-run

Renders every `*.template` in this bundle with a fabricated non-Hestia node profile and proves zero
leftover `{vars}`. Exit-Gate 6 / Obj 9 of M25. **Re-run after editing any template:**

```
python3 smoke_render.py     # or: python smoke_render.py — stdlib only, no PyYAML
```

The harness is now a **persisted bundle artifact** (`./smoke_render.py`, Prytaneion M3.4 — it used to
live only in the M25 session log). This file records the latest outcome.

## Fabricated profile (deliberately unlike the reference node)

| var | value |
|---|---|
| `{node_hostname}` | node-bravo |
| `{operator}` | ada |
| `{persona}` / `{persona_lower}` | Athena / athena |
| `{machine_class}` | Linux x86_64 |
| `{accent_primary/secondary/tertiary_hex}` | #4444AA / #cfd8ff / #7dffd0 |
| `{banner_image}` | banner_athena.jpg |
| (full map) | see `SUBSTITUTIONS.md` |

## Result (re-run 2026-06-10, Prytaneion M6.1)

- **Templates rendered (6)**:
  - .obsidian/snippets/athena_accent.css
  - .obsidian/snippets/athena_canvas.css
  - HOME.md
  - what/canvas/topology_relationships.yaml
  - what/canvasforge/CLAUDE.md
  - who/assets/asset_registry.yaml
- **Leftover `{{vars}}` after render**: NONE ✓
- **Vars used but absent from `SUBSTITUTIONS.md`**: none ✓
- **Vars exercised (24)**: the M3.4 set of 21 **+`canvas_text_strong_hex` +`canvas_text_em_hex`**
  (M6.1 canvas-chrome snippet) **+`health_detail_note`** (M6.1/J1 optional health narrative — the
  fabricated profile exercises the *empty* default). The two table vars (`vaults_table` /
  `named_projects_table`) render as `>`-prefixed callout-body bullets per the M3.4 disclosure-fold profile.
- **Skeleton-parity check** (M6.1, reference node only): `python smoke_render.py --parity` → ✓ PARITY
  (live `HOME.md` matches the template structure modulo the 2 enumerated divergences — see
  `SUBSTITUTIONS.md` §Skeleton-parity invariant).

✓ **PASS** — every placeholder resolves to a node-bravo value; the persona-named CSS files
materialize as `athena_accent.css` + `athena_canvas.css`; no Hestia/`#663399` literal leaks into a
foreign-persona render.

> **New modes (M6.1):** `--materialize DIR` writes a rendered fork skeleton (renders the 6 templates,
> copies verbatim assets, skips bundle docs; smoke invariants enforced first); `--parity` runs the
> reference-node skeleton check. Default invocation unchanged.

> **Static assets (NOT rendered/checked):** `what/inventory/curation_gallery.base` (the §Gallery Bases
> cards view, added M3.4) and `what/code/*.py` carry no `{{vars}}` and ship verbatim. Bundle docs
> (`README.md`, `SUBSTITUTIONS.md`, `AGENTS.md`) intentionally *mention* `{vars}` as reference text and
> are likewise not materialization targets — only `*.template` files are rendered/checked.
