---
type: reference
title: "template_node_adna_exemplar — Reusable Exemplar HOME Bundle"
created: 2026-06-01
updated: 2026-06-10
status: active
last_edited_by: agent_hestia
campaign: campaign_lattice_compliance_upgrade
mission: mission_lattice_comp_m25_template_node_adna_exemplar
tags: [reference, template, exemplar, node_adna, home, m25, prytaneion_m3_4, prytaneion_m6_1]
---

# `template_node_adna_exemplar/`

A reusable bundle that bootstraps a **premium, themed, generator-driven exemplar HOME** for any
`Home.aDNA`-class node — the "AI data product" presentation that this reference node (host `Dyrnwyn`,
persona Hestia) accreted across compliance-campaign missions **M15–M24** and Operation-Prytaneion
phases **P1–P5**, packaged so a fresh node (or a re-bootstrap) gets the shape immediately instead of
reconstructing it by hand. Kept at parity with the live instance by Prytaneion **M3.4/M6.1** (see
`SUBSTITUTIONS.md` §Skeleton-parity invariant).

Built by **M25** (`campaign_lattice_compliance_upgrade` Phase 4-Closing). It is the **themed superset**
of the base `.adna/HOME.md` — it reuses that template's canonical inventory vars verbatim and adds a
theming + gallery + topology layer on top.

## What it produces

A bootstrapped node gets:
- **`HOME.md`** — the Prytaneion-elevated themed home: persona banner, a **landing strip** (aDNA-network
  intro + an `adna.network` meta-bind CTA + marketplace link), a one-line **dashboard band** (5-second
  status: N vaults · drift · blocked · last check), greeting, a **Bases-rendered §Gallery** of per-vault
  curation cards, a §Topology link, and four progressive-disclosure callout folds holding all audit-grade
  detail (node detail · all-vaults index · non-vault projects · operator utilities). Resting view ≈1.5 viewports.
- **`.obsidian/snippets/<persona>_accent.css`** — the persona-accented "Bio-Digital Cozy" CSS layer.
- **`.obsidian/snippets/<persona>_canvas.css`** (M6.1) — the topology-canvas **card chrome** (status
  pills · corner glyphs · accent stripe · typography grammar). **Required** for the canvas: the
  generator emits `cf-pill`/`cf-glyph` spans that render as bare text without it.
- **`what/code/build_topology_canvas.py` + `build_curation_cards.py`** — the generators that keep the
  §Gallery and §Topology current from `inventory_vaults.yaml` (no hand-maintained lists). The canvas
  generator carries the exemplar **layout + sizing system** (consumer-adjacent band order, barycenter
  placement, legend left-rail, degree-tiered hub/standard/leaf cards — Prytaneion M2.2/M2.3) and an
  optional style-override surface (`CANVAS_STYLE_OVERRIDE`, see `what/canvas/AGENTS.md`).
- **`what/canvas/topology_relationships.yaml`** (from the `.template` seed) — the hand-authored edge seed.
- **`who/curation/` + `who/assets/`** — the curation-card schema + imagery skeleton, including the M2.4
  **icon system** (emblems > sigils > crests fallback chain; per-dir AGENTS.md generation recipes;
  pattern-not-binaries — empty dirs are the documented day-1 state).
- **`what/canvasforge/CLAUDE.md`** — the Canvas.aDNA `canvas_core` consumer wrapper (triad placement per ADR-004; substrate → `Canvas.aDNA/what/production/canvas_core` at PT P5).
- **`ONBOARDING.md`** (M6.1) — the first-run walkthrough a fresh fork reads before anything else.

## How it's consumed

Two entry points (both canonical in `.adna/`; this bundle is the data they lay down):

1. **`skill_node_bootstrap_interview.md` Step 9** — the 19-question interview already substitutes
   `HOME.md {{VARS}}`. The exemplar profile points that step at `HOME.md.template` here and additionally
   materializes the CSS, generators, seed, and skeleton. *(Wiring proposed upstream — see below.)*
2. **`skill_project_fork.md --exemplar-home`** (or `project_name = Home`) — lays the bundle down at fork
   time. The **local** `Home.aDNA/how/skills/skill_project_fork.md` carries a worked hook demonstrating
   this (M25 D1).

### Substitution flow

```
collect node identity (hostname, operator, persona, machine_class, workspace_root)
  + pick persona accents (primary/secondary/tertiary hex)  ← see SUBSTITUTIONS.md §2
        │
        ▼
for each *.template file in this bundle:
    replace every {{var}} per SUBSTITUTIONS.md  →  drop the `.template` suffix
    (the file `{{persona_lower}}_accent.css.template`  →  e.g. `hestia_accent.css`)
        │
        ▼
materialize who/assets skeleton (+ operator's real banner as {{banner_image}})
copy generators verbatim (no {{vars}} — they read env/inventory at runtime)
rename topology_relationships.yaml.template → topology_relationships.yaml; edit to taste
        │
        ▼
first regen:  CANVAS_CORE_HOME=… TOPOLOGY_GENERATED_DATE=$(date +%F) \
              python what/code/build_topology_canvas.py        # §Topology
              python what/code/build_curation_cards.py         # §Gallery
        │
        ▼
open in Obsidian → operator aesthetic sign-off (Standing Order #1)
```

The full `{{var}}` catalog (source · example · required) is in **`SUBSTITUTIONS.md`**.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `cannot import ... canvas_core` | the `canvas_core` substrate or its `canvas_std` dep isn't resolvable | set `$CANVAS_CORE_HOME` (deprecated alias `$CANVASFORGE_CODE`) to the `canvas_core` location, ensure `adna-canvas-std` is importable (ADR-004 §4), or skip the optional topology canvas |
| `ModuleNotFoundError: yaml` | ran under `python3` (lacks PyYAML) | use `python` (3.12.2 on the reference node) |
| §Gallery empty in Obsidian | `who/curation/` not yet built, or the Bases core plugin disabled | run `python what/code/build_curation_cards.py`; enable **Bases** (core plugin) |
| canvas cards show literal `<span class="cf-pill">…` text / no pills or glyphs | the canvas-chrome snippet isn't enabled | enable `<persona>_canvas.css` under Appearance → CSS snippets (ships in this bundle alongside the accent snippet) |
| broken banner image | `{{banner_image}}` points at a missing file | drop a real banner in `who/assets/banners/` and set `{{banner_image}}` (placeholder ships as `banner_placeholder.png`) |
| canvas shows old vault after a rename | hand seed still names the old vault | `skill_inventory_refresh.md` Step 9.5 rename-drift procedure |
| huge but empty-looking canvas diff | `canvas_core` reformatted (compact↔pretty) | expected on a `canvas_core` upgrade — not drift |

## Customization points

- **Persona** — the exemplar is persona-portable; Hestia is the reference, not a requirement. Pick a
  persona + accent triple at bootstrap (`SUBSTITUTIONS.md` §2 has a default lookup table).
- **Gallery cadence** — regenerate curation cards whenever inventory/imagery changes (it's idempotent).
- **§Vaults rendering** — `{{vaults_table}}` is the shared insertion point; the exemplar (M3.4) emits
  **`>`-prefixed callout-body bullets** inside the `> [!abstract]-` disclosure fold (NOT `.vault-grid`
  divs / a markdown table — those break the callout open). Never hand-maintain a static vault list.
- **Plugins (not bundled)** — enable at bootstrap: **Bases** (Obsidian core plugin — the §Gallery cards
  view), **Advanced Canvas** (§Topology), **Meta Bind** (the `adna.network` landing button). Dataview is
  *optional* — the dormant `.curation-card` DataviewJS path, off by default since Prytaneion M3.2. **Both
  CSS snippets** (`<persona>_accent.css` + `<persona>_canvas.css`) must be enabled under Appearance → CSS snippets.
- **Terminal/CLI layer (not bundled)** — the exemplar node pairs this Obsidian surface with a configured
  terminal operation layer (shell profiles, keybindings, agent-in-terminal ergonomics). That doctrine is
  node-local context, not template material: see the reference node's
  `what/context/context_terminal_operation.md` (Prytaneion M5.1) for the worked example to adapt.

## Upstream

M25 files two upstream-contribution ideas so this becomes a v8+ standard offering rather than a
node-local artifact:
- `aDNA.aDNA/how/backlog/idea_upstream_node_exemplar_template.md` — promote this bundle into `.adna/`.
- `aDNA.aDNA/how/backlog/idea_upstream_project_fork_exemplar_invocation.md` — add the `--exemplar-home`
  hook + the persona-accent interview questions to the canonical `.adna/` skills.

Per Standing Rule 1, `.adna/` is not edited directly; these ideas route through the standard team.
