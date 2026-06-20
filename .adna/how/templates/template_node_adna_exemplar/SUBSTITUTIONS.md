---
type: reference
title: "template_node_adna_exemplar — Substitution Catalog"
created: 2026-06-01
updated: 2026-06-05
status: active
last_edited_by: agent_hestia
tags: [reference, template, exemplar, substitutions, node_adna, m25, prytaneion_m3_4]
---

# `template_node_adna_exemplar/` — Substitution Catalog

Every `{{var}}` in this bundle, its source, an example value, and whether it's required.
Keystone deliverable of compliance-campaign **M25** (`mission_lattice_comp_m25_template_node_adna_exemplar.md`);
the HOME structure was round-tripped from the Prytaneion-elevated live page by **M3.4**
(`mission_p3_m3_4_template_parity.md`) — landing layer + dashboard band + Bases §Gallery + disclosure folds.

**Three classes** of substitution:
1. **Shared base vars** — already defined by `.adna/HOME.md` + `skill_node_bootstrap_interview.md` Step 9.
   The exemplar **reuses** these verbatim so the interview fills the base *and* exemplar HOME identically.
   Do not rename.
2. **Exemplar theming vars** — NEW; the premium/themed layer. Extend the base interview. The upstream
   contribution idea (`aDNA.aDNA/how/backlog/idea_upstream_node_exemplar_template.md`) proposes adding
   these as interview questions so a fresh node can pick a persona accent at bootstrap.
3. **Generator runtime params** — NOT file `{{var}}` substitutions. The generators read these from env /
   CLI args at regen time; listed here so the bundle is self-documenting.

The substitution token style is `{{snake_case}}` (the established vault convention; 200+ in-vault uses).

---

## 1. Shared base vars (canonical — from `.adna/HOME.md`; do not rename)

| var | source | example | required |
|---|---|---|---|
| `{{node_hostname}}` | interview U1 / `hostname -s` / `who/identity/identity_node.yaml` `node.hostname` | `Mac` | yes |
| `{{operator}}` | interview U1 / `node.operator` | `stanley` | yes |
| `{{persona}}` | interview / persona pick (exemplar is persona-portable) | `Hestia` | yes |
| `{{persona_lower}}` | derived: `{{persona}}` lowercased — drives CSS selectors, var names, the CSS filename, portrait path | `hestia` | yes |
| `{{machine_class}}` | interview H1 / `node.machine_class` | `Apple Silicon Mac` | yes |
| `{{workspace_root}}` | `pwd -P` parent / `$LATTICE_ROOT` / `node.workspace_root` | `/Users/stanley/aDNA/` | yes |
| `{{vault_count}}` | derived from `inventory_vaults.yaml` | `39` | yes |
| `{{named_project_count}}` | derived from `inventory_vaults.yaml` | `8` | no |
| `{{drift_count}}` | derived from `inventory_vaults.yaml` drift section | `0` | no |
| `{{healthy_count}}` | derived from `inventory_vaults.yaml` health section (same source as `{{drift_count}}`; M3.4 — dashboard band + Node-detail fold) | `39` | no |
| `{{blocked_count}}` | derived from `inventory_vaults.yaml` health section (M3.4 — dashboard band) | `0` | no |
| `{{last_inventory_refresh}}` | `inventory_vaults.yaml` `updated:` | `2026-05-31` | yes |
| `{{interview_date}}` | interview-run date (YYYY-MM-DD) | `2026-06-01` | yes |
| `{{vaults_table}}` | rendered by interview. **Exemplar profile (M3.4): callout-body lines ONLY** — the all-vaults index lives inside a `> [!abstract]-` disclosure fold, so every emitted line MUST be `>`-prefixed (`> - **<Category> (n)** · [Name](../Name.aDNA/) · …`, one per aDNA class). NOT the legacy `.vault-grid` divs / base markdown table — a `<div>` or blank-line-bearing table breaks the callout open. `../Name.aDNA/` links flow from inventory, never hand-pasted. | _(`>`-prefixed bullets)_ | yes |
| `{{named_projects_table}}` | rendered by interview as **callout-body `>`-prefixed lines (M3.4)** — named-projects + external-deps + archived groups inside the `> [!note]-` fold; or `> No named projects on this node yet.` | _(`>`-prefixed bullets)_ | no |

> The base `.adna/HOME.md` also carries `{{operator_lower}}`, `{{drift_table}}`, `{{next_steps_section}}`.
> The exemplar HOME does not use those directly (it leans on the §Gallery/§Topology instead), but the
> interview still resolves them for the base HOME — keep them populated.

## 2. Exemplar theming vars (NEW — extend the base interview)

| var | source | example | required |
|---|---|---|---|
| `{{persona_greeting}}` | persona archetype line / operator | `Tending the hearth.` | yes |
| `{{banner_image}}` | operator-supplied banner filename in `who/assets/banners/` (default = the placeholder until replaced) | `banner_hestia.jpg` | yes |
| `{{banner_title}}` | operator | `aDNA-Network Home` (or `{{node_hostname}} Home`) | yes |
| `{{last_health_check}}` | `STATE.md` / last `skill_node_health_check` run | `2026-05-31` | no |
| `{{accent_primary_hex}}` | persona-archetype accent lookup (below) / operator | `#663399` | yes |
| `{{accent_secondary_hex}}` | persona-archetype accent lookup / operator | `#f5c97a` | yes |
| `{{accent_tertiary_hex}}` | persona-archetype accent lookup / operator (emissive/genesis tertiary; also the canvas mono-box color) | `#7dcfff` | yes |
| `{{canvas_text_strong_hex}}` | canvas-chrome card title/strong text (M6.1; default = Hestia value — pick a near-white tinted toward your primary) | `#f2eefb` | yes |
| `{{canvas_text_em_hex}}` | canvas-chrome card persona/em text (M6.1; default = Hestia value — a soft pastel of your primary) | `#c0a6e8` | yes |
| `{{health_detail_note}}` | optional free-text appended to the Node-detail Health line (leading space; **default = empty string**) — lets a node carry health-narrative without breaking skeleton parity (M6.1/J1) | _(empty)_ | no |

### Persona accent default lookup (suggested — extend at will)

| persona | primary | secondary | tertiary | canvas strong | canvas em |
|---|---|---|---|---|---|
| Hestia (exemplar) | `#663399` | `#f5c97a` | `#7dcfff` | `#f2eefb` | `#c0a6e8` |
| _Athena (example)_ | `#4444AA` | `#cfd8ff` | `#7dffd0` | `#eef2fb` | `#a6b8e8` |
| _(other)_ | operator-supplied | operator-supplied | operator-supplied | near-white toward primary | pastel of primary |

> The CSS var names keep their original color-descriptive suffixes (`--{{persona_lower}}-purple`,
> `--{{persona_lower}}-gold`) — only the **values** are parametrized, so a non-purple persona gets a
> cosmetically-named-but-correct token. See the CSS template header.
>
> **Translucent accents** (rgba with alpha — e.g. `rgba(102, 51, 153, 0.x)`, and the callout-family
> `--callout-color: 159, 124, 216`) are intentionally left as **literals**: this CSS has no
> `color-mix`/relative-color, so only solid color stops and the named `--{{persona_lower}}-*` / `--cc-*`
> tokens are parametrized. The M3.4 landing-strip + dashboard-band + callout blocks follow this convention.

## 3. Generator runtime params (NOT file `{{var}}` substitutions)

The canvas/curation generators read these at regen time (env or CLI), so they are not text-substituted
into any file. They exist because the live generators hardcode node-local values that a fresh node must
override.

| param | mechanism | default | why |
|---|---|---|---|
| `CANVAS_CORE_HOME` | env var read by `build_topology_canvas.py` (deprecated alias: `CANVASFORGE_CODE`) | `{{workspace_root}}/Canvas.aDNA/what/production` (P5+; interim falls through to the `CanvasForge.aDNA` archive) | portability — locates the `canvas_core` producer engine (Canvas.aDNA, ADR-004; lands at PT P5). The generator also adds `Canvas.aDNA/what/code/canvas_std/src` to sys.path (`canvas_core` needs `canvas_std` — ADR-004 §4); degrades with a clear message if absent |
| `TOPOLOGY_GENERATED_DATE` | env var read by `build_topology_canvas.py` | `{{interview_date}}` (today) | determinism — the canvas stamps a fixed date so re-runs are byte-identical; a fresh node sets its own |
| `CANVAS_STYLE_OVERRIDE` | env var (path) read by `build_topology_canvas.py` | `what/canvas/canvas_style.yaml` — **absent = no-op** | bounded style/geometry tuning without editing the generator (`category_color:` / `edge_color:` / `state_dim:` / `geometry:` / `band_order:`); the M1.3 cadence-harness "improve" surface. See `what/canvas/AGENTS.md` |

---

## Cross-check (M25 Exit-Gate; extended M6.1)

- Every `{{var}}` appearing in any `*.template` file in this bundle **must** have a row above.
- Smoke test (`SMOKE_TEST_DRY_RUN.md`) renders the bundle with example values and greps for leftover `{{`.
- Files carrying `{{vars}}`: `HOME.md.template`, `.obsidian/snippets/{{persona_lower}}_accent.css.template`,
  `.obsidian/snippets/{{persona_lower}}_canvas.css.template` (M6.1 — REQUIRED for canvas chrome),
  `what/canvasforge/CLAUDE.md.template`, `what/canvas/topology_relationships.yaml.template`,
  `who/assets/asset_registry.yaml.template`, and the two `{{persona_lower}}_*.css.template` filenames themselves.
- **Node-agnostic static assets** (NO `{{vars}}`; ship verbatim, NOT materialization targets — the smoke
  test does not render them): `what/inventory/curation_gallery.base` (the §Gallery Bases cards view, added
  M3.4 when the engine switched DataviewJS→Bases), the generators under `what/code/`, and every `AGENTS.md`.

### Skeleton-parity invariant (M6.1/J1 — checkable)

`HOME.md.template` rendered with the reference node's real values **equals the live `HOME.md` byte-for-byte**,
modulo exactly two enumerated divergences:

1. **Template-guidance HTML comments** (`<!-- … -->` blocks) — template-only by design; stripped before compare.
2. **The Personae line** in the Operator-utilities fold — template ships the generic line; a live node
   enriches it with its real cross-vault persona links (expected, desirable).

Everything else a live node narrates (health detail, fold-title freshness date) is carried **inside var
values** (`{{health_detail_note}}`, `{{last_inventory_refresh}}`), so the check stays meaningful. Run it:
`python smoke_render.py --parity` (reference node only). Frontmatter renders **unquoted** (matches the
live emission style of `skill_inventory_refresh`/SC-8 tooling).
