---
type: skill
lattice_type: skill
skill_type: agent
created: 2026-05-12
updated: 2026-05-12
mission_origin: campaign_b_iii_federation MB-6
status: active
category: onboarding
trigger: "A vault is adopting III.aDNA for the first time — operator asks to 'set up III', 'add III review', 'federate against III', or 'add an iii/ wrapper'"
last_edited_by: agent_stanley
tags: [skill, iii, federation, onboarding, consumer_wrapper]
federation:
  discoverable: true
  source_instance: III.aDNA
  version_policy: minor
fair:
  keywords: [iii, federation, consumer_wrapper, onboarding, quality_review]
  license: Apache-2.0
---

# Skill: III Setup (Consumer Onboarding)

## Overview

Adds an `iii/` consumer wrapper to a new vault so it can run III (Inspect / Introspect / Improve) reviews against the canonical III.aDNA framework. The wrapper is lightweight: a single `CLAUDE.md` with a `federation_ref` block + optional `local_extensions` + (in almost all cases) an empty local learning-store JSONL. III canonical content (skill, modules, packs, lattice, canonical corrections.jsonl) is **never** copied into the consumer vault — only referenced.

This skill is the counterpart to `skill_iii_review.md` — that skill runs the review; this skill bootstraps the substrate so a vault can call it.

Canonical contract: [ADR-002 Consumer Federation Contract](../../what/decisions/adr_002_consumer_federation_contract.md) (`federation_ref` schema + `kind:` enum) + [ADR-003 Learning Store Ownership](../../what/decisions/adr_003_learning_store_ownership.md) (per-vault local store + canonical-as-read-only + graduation ceremony).

## When to Use

1. **A vault is adopting III for the first time** — operator says "set up III" / "add III review" / "federate this vault against III".
2. **A pre-federation vault is migrating** — vault has been calling the III skill ad-hoc against `<workspace_root>/III.aDNA/how/skills/skill_iii_review.md` without a wrapper; needs to formalize per ADR-002.
3. **A vault is forking a new sub-domain** — same vault, but a new modality (e.g., wga adding a sonification trap pack) wants a fresh `local_extension` entry under the root wrapper. (Run this skill once per vault, not per sub-domain — sub-domains compose under one wrapper. See § Variants below.)

Do NOT use this skill to:
- Copy III modules / skills / packs into a consumer vault (forbidden by ADR-002 §6).
- Modify the canonical learning store at `<workspace_root>/III.aDNA/what/context/core_domain_packs/iii_corrections_canonical.jsonl` (use the ADR-003 §3 graduation ceremony instead).
- Author a wrapper that points at a non-pinned `version:` (every wrapper pins to a specific III.aDNA version + commit per ADR-002 §3).

## Prerequisites

- The consumer vault exists at `<workspace_root>/<consumer>.aDNA/` (or equivalent path) and has a root `CLAUDE.md`.
- III.aDNA upstream is reachable — either locally at `<workspace_root>/III.aDNA/` (preferred) or via the GitHub remote `https://github.com/LatticeProtocol/III.aDNA`.
- The operator can decide pack selection (or accepts the minimal baseline default — see Step 3).
- Familiarity with ADR-002 + ADR-003 (or willingness to read them inline during the procedure).

## Inputs / Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `consumer_vault_path` | yes | Absolute path to consumer vault root (e.g., `<workspace_root>/wga.aDNA/`) |
| `iii_version` | yes | III.aDNA version to pin against (default: latest annotated tag — `v0.2.0` as of 2026-05-10) |
| `iii_commit` | yes | Exact commit hash for the pinned version. Verify with `git rev-parse <tag>^{commit}` inside `<workspace_root>/III.aDNA/` |
| `packs_used` | recommended | Pack set the consumer will load. Default minimal baseline: `inspect_procedures`, `introspect_checks`, `learning_store`, `domain_packs_web_design`, `vault_maintenance`. See Step 3 for full enumeration. |
| `modules_used` | recommended | Default all 8. Reduce only if there's a specific reason. |
| `local_extensions` | optional | Consumer-specific `kind:` entries (`domain_pack`, `reviewer_registry`, `bridge_pack`, `local_skill`, `learning_store_local`). See Step 5 for the enum walkthrough. |
| `mission_origin` | optional | If this skill is invoked from a specific III.aDNA campaign mission (e.g., Campaign B MB-N), record the mission id in the wrapper frontmatter for provenance. |

## Procedure

### Step 1 — Identify consumer vault + pin the III.aDNA version

1. Confirm the consumer vault path and that its root `CLAUDE.md` exists.
2. Resolve the III.aDNA version pin:
   - If `<workspace_root>/III.aDNA/` exists locally: `cd <workspace_root>/III.aDNA && git rev-parse <tag>^{commit}` (e.g., `git rev-parse v0.2.0^{commit}` → returns `246124d...`). Use the **short hash** (7 chars) in the wrapper.
   - If only the GitHub remote is available: pull `git ls-remote --tags origin <tag>` for the commit hash; record the date the pin was taken (`pinned_at: <YYYY-MM-DD>`).
3. Record `version`, `pinned_at_commit`, and `pinned_at` for use in Step 2.

**Pin convention** (per ADR-002 §3): the wrapper pins to a specific minor.patch version AND the exact closure commit. Patch bumps apply transparently; minor bumps trigger consumer-side review of the upstream CHANGELOG diff before updating.

### Step 2 — Author `iii/CLAUDE.md`

Create `<consumer_vault>/iii/CLAUDE.md`. Use this skeleton (fill the bracketed values):

```markdown
---
type: federation_wrapper
wrapper_for: III.aDNA
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
last_edited_by: <agent_id>
mission_origin: <campaign>.<mission> (e.g., III.aDNA campaign_b_iii_federation MB-6)
status: active
tags: [federation, iii, consumer_wrapper, <vault_name>]
---

# <vault_name> `iii/` — III.aDNA Consumer Wrapper

This is the <vault_name> federation wrapper for **III.aDNA** (Inspect / Introspect / Improve framework, persona Argus Panoptes). It declares which III capabilities <vault_name> consumes, pins the upstream version, and routes ACCUMULATE writes to the <vault_name>-local learning store instead of the canonical upstream store.

Per **ADR-002** (consumer federation contract) and **ADR-003** (learning store ownership) at III.aDNA, this wrapper is lightweight: a `federation_ref` block + optional `local_extensions`. III canonical content (skill, modules, packs, lattice, canonical corrections.jsonl) is **never** copied here — only referenced.

## federation_ref

```yaml
federation_ref:
  source_vault: III.aDNA
  source_path: <workspace_root>/III.aDNA
  source_skill: how/skills/skill_iii_review.md
  version: "<X.Y.Z>"                       # pinned at wrapper creation
  version_policy: minor                     # minor | locked
  pinned_at_commit: "<short_hash>"
  pinned_at: <YYYY-MM-DD>
  packs_used:
    - <pack_1>
    - <pack_2>
    # ... (see Step 3)
  modules_used:
    - module_iii_dispatch
    - module_iii_inspect_text
    - module_iii_inspect_code
    - module_iii_inspect_visual
    - module_iii_inspect_data
    - module_iii_introspect
    - module_iii_improve
    - module_iii_accumulate
  lattice: <workspace_root>/III.aDNA/what/lattices/lattice_iii_verification_oracle.lattice.yaml
  lattice_version: "<x.y.z>"                # e.g., 1.2.1 as of 2026-05-12
  local_extensions:
    # See Step 5 — declare any consumer-specific extensions here
    - kind: learning_store_local
      path: <workspace_root>/<vault_name>.aDNA/iii/what/context/<vault_name>_iii_learning_store.jsonl
      rationale: Per ADR-003 §2 at III.aDNA; ACCUMULATE writes target this file, never the canonical upstream.
```

## Active campaigns using this wrapper

(none yet — populated as new campaigns invoke III review under this wrapper)

## Local extensions explained

(one subsection per `local_extensions` entry — explain why it exists, what it contains, and graduation eligibility)

## Routing notes

1. **ACCUMULATE always writes local.** Never edit `iii_corrections_canonical.jsonl` from the <vault_name> side. Use the ADR-003 graduation PR process for upstream changes.
2. **Pack precedence on conflict** (per ADR-003 §2): if a local-extension pack and a canonical pack name the same trap, **local wins** (consumer knows its domain better). Mark such overrides in the local pack's frontmatter for graduation review.
3. **Version-policy bump.** When III.aDNA bumps minor, this wrapper agent reviews the upstream CHANGELOG diff before updating `version:`. Patch bumps apply transparently.
4. **Skill invocation.** Active campaigns load this CLAUDE.md first → follow `federation_ref.source_skill` to the canonical III skill → III skill orchestrates pack loading from `packs_used` + `local_extensions`.

## Cross-References

- Upstream identity + protocol: `<workspace_root>/III.aDNA/CLAUDE.md`
- Upstream skill: `<workspace_root>/III.aDNA/how/skills/skill_iii_review.md`
- ADR-002 (consumer federation contract): `<workspace_root>/III.aDNA/what/decisions/adr_002_consumer_federation_contract.md`
- ADR-003 (learning store ownership): `<workspace_root>/III.aDNA/what/decisions/adr_003_learning_store_ownership.md`
- <vault_name> root governance: `<workspace_root>/<vault_name>.aDNA/CLAUDE.md` (Standing Order routing III review through this wrapper)
- Worked precedents: see III.aDNA MANIFEST.md § Active Consumers
- Mission origin: <campaign>.<mission>, session `<session_file_name>`
```

### Step 3 — Choose packs (the `packs_used` list)

III.aDNA ships 7 canonical packs at `<workspace_root>/III.aDNA/what/context/core_domain_packs/`. Each pack is opt-in per consumer:

| Pack | When to include |
|------|------------------|
| `context_iii_inspect_procedures` | **Always** — 4-modality INSPECT procedure reference. Every consumer needs it. |
| `context_iii_introspect_checks` | **Always** — 7 INTROSPECT structural checks. Every consumer needs it. |
| `context_iii_learning_store` | **Always** — describes the JSONL schema + graduation contract. Every consumer needs it. |
| `context_iii_domain_packs_web_design` | Vault produces web pages, UI components, design tokens, or HTML/CSS/Astro/React/Vue content. (Most vaults.) |
| `context_iii_whitepaper_communication` | Vault produces formal academic prose, whitepapers, citations, structured argumentation. (LPWhitepaper, lattice-labs whitepaper authors, WilhelmAI charter authors.) |
| `context_iii_canvas_visual` | Vault produces canvas-substrate artifacts (decks, comics, posters, infographics). Note: if the vault has its own canvas-trap catalog (e.g., CanvasForge with 10 traps vs the canonical 8), prefer a `bridge_pack` local_extension and **deliberately omit** the canonical pack — see Step 5. |
| `context_iii_vault_maintenance` | **Strongly recommended for all aDNA vaults** — staleness, wikilinks, frontmatter discipline, MIGRATION_NOTE.md hygiene. Universal hygiene; applies to every vault. |

**Minimal baseline** (5/7 packs, wga MB-5 + VideoForge MB-3 + CanvasForge MB-4 precedent):

```yaml
packs_used:
  - context_iii_inspect_procedures
  - context_iii_introspect_checks
  - context_iii_learning_store
  - context_iii_domain_packs_web_design
  - context_iii_vault_maintenance
```

This minimal baseline serves all consumers that produce web content + want hygiene checks but don't produce whitepapers or canvas artifacts. It is the recommended starting point.

**Document exclusions explicitly.** If you drop `whitepaper_communication` or `canvas_visual`, add an inline note in the wrapper body (under § federation_ref) explaining why and naming the revisit-at-next-minor-bump escape hatch. Example from wga MB-5: *"`whitepaper_communication` — wga has no whitepaper-style outputs at v0.2.0 time. Revisit at v0.2.1 minor bump if curriculum work evolves toward whitepaper-style outputs."*

### Step 4 — Choose modules (the `modules_used` list)

Default: all 8 modules. Reducing the list is exceptional — you must explicitly opt out of a phase.

The 8 modules are:

```yaml
modules_used:
  - module_iii_dispatch        # Auto-selects packs + depth + modalities
  - module_iii_inspect_text    # Five Traps + domain-pack precision check
  - module_iii_inspect_code    # Function names + CLI commands + paths verified against codebase
  - module_iii_inspect_visual  # Image refs, screenshot accuracy, label/caption consistency
  - module_iii_inspect_data    # Schema consistency, statistics vs prose
  - module_iii_introspect      # 7 structural checks (confidence gradient, denominator, meta-patterns…)
  - module_iii_improve         # Prioritized improvement table
  - module_iii_accumulate      # Writes to local learning store after operator approval
```

If your vault genuinely never reviews code (e.g., a pure-prose archive), you may drop `module_iii_inspect_code`. Document the omission in the wrapper.

### Step 5 — Declare `local_extensions` (the `kind:` enum)

ADR-002 §1a defines 5 valid `kind:` values. Every entry MUST declare exactly one. Most wrappers have 1–3 entries. The minimal wrapper (wga MB-5) has exactly one: `learning_store_local`.

| `kind:` | When to use it |
|---------|----------------|
| `learning_store_local` | **Always include this.** Per-vault JSONL fork of the canonical learning store. ACCUMULATE writes target this file, never canonical. Required for any consumer that runs ACCUMULATE cycles (i.e., every consumer that does real III work). Seed empty. |
| `domain_pack` | Vault has a consumer-specific trap pack that **extends** (not replaces) canonical packs. Example: lattice-labs KINN brand-voice traps. Subject to graduation per ADR-003 §3 if domain-general. |
| `reviewer_registry` | Vault uses multi-voice review (named voices like Voice Critic / Design / UX / SEO / Brand). YAML registry declares the voices. Example: SiteForge MB-2 `siteforge_reviewers.yaml`. |
| `bridge_pack` | Vault has a consumer-specific operation catalog or domain trap pack that **supersedes** a canonical pack on overlapping traps. **Carries `not_graduating_to_canonical: true`** per ADR-002 §6 (modality-agnostic-core boundary). Examples: VideoForge ADR-006 bridge (MB-3); CanvasForge 10-trap canvas pack (MB-4). |
| `local_skill` | Vault has a consumer-specific orchestration skill that composes multi-voice voice definitions or modality-specific dispatch. Does **not** replace the canonical III skill; supplies consumer-side orchestration the canonical can't know. Example: CanvasForge `skill_canvas_iii_review.md` (MB-4, 5-voice canvas review). |

**Decision tree for new consumer wrappers**:

```
Always:    1 × learning_store_local (seeded empty)
            │
            ├── Vault has a trap pack that extends canonical?
            │       → add 1 × domain_pack
            │
            ├── Vault has a trap pack that supersedes a canonical pack?
            │       → add 1 × bridge_pack (+ omit the superseded canonical pack from packs_used)
            │
            ├── Vault uses multi-voice review with named voices?
            │       → add 1 × reviewer_registry
            │
            └── Vault has a consumer-specific orchestration skill?
                    → add 1 × local_skill
```

**Field requirements** (per ADR-002 §1a):

- Every entry MUST have `kind:`, `path:`, and `rationale:` (one-line consumer-specific justification).
- Optional: `not_graduating_to_canonical: true` for `bridge_pack` / `local_skill` / consumer-specific `domain_pack` entries that intentionally stay consumer-side.
- **New `kind:` values require an ADR amendment** — coordinate via the v0.2 cross-vault request surface first (see `<workspace_root>/III.aDNA/what/artifacts/iii_airlock_standard_spec.md` §4), then propose the ADR-002 amendment. Do NOT ship a new `kind:` until the amendment lands.
- **New instances of existing kinds are additive** — no ADR amendment needed; the wrapper declares them inline.

### Step 6 — Seed the local learning store

Create the empty file:

```bash
mkdir -p <workspace_root>/<vault_name>.aDNA/iii/what/context/
touch <workspace_root>/<vault_name>.aDNA/iii/what/context/<vault_name>_iii_learning_store.jsonl
```

Per ADR-003 §2:
- File is 0 bytes at wrapper creation.
- ACCUMULATE writes append corrections here, never to canonical.
- The canonical store at `<workspace_root>/III.aDNA/what/context/core_domain_packs/iii_corrections_canonical.jsonl` (md5 `dde2cbd88c0b45956fb22285a2a0f856` as of 2026-05-12, 26 founding entries) is **read-only** from the consumer side.
- Graduation ceremony (ADR-003 §3) flips eligible local entries upstream when frequency ≥ 3 across ≥ 2 sessions and acceptance ≥ 80%, subject to operator + Argus approval.

**If migrating from pre-federation**: a pre-existing operational corrections jsonl at the vault (e.g., `<vault>/what/context/iii_domain_packs/iii_corrections.jsonl`) is **retired**, not migrated. Truncate it to 0 bytes (`truncate -s 0 <file>` or `: > <file>`) and author a sibling `MIGRATION_NOTE.md` documenting the disposition. All entries in the pre-federation jsonl that already exist in canonical are accounted for upstream from MA-1; the local store starts fresh post-wrapper. (Worked precedent: lattice-labs MB-1, SiteForge MB-2.)

### Step 7 — Add a Standing Order to the vault root `CLAUDE.md`

Add a Standing Order (or Standing Rule, whichever the vault uses) routing all III review through the new wrapper. Place it after the last existing Standing Order. Template:

```markdown
**Standing Order N** ([YYYY-MM-DD]) — III review routes through the `iii/` wrapper at `<vault_name>/iii/CLAUDE.md`. The wrapper pins III.aDNA at version `<X.Y.Z>` (commit `<short_hash>`) per ADR-002 §3. Local extensions: <enumerate kind: path pairs>. ACCUMULATE writes target the local learning store at `<path>` per ADR-003 §2; the canonical upstream at `<workspace_root>/III.aDNA/what/context/core_domain_packs/iii_corrections_canonical.jsonl` is read-only from this vault.
```

Precedent voice (mirror these for tonal consistency):

- lattice-labs `CLAUDE.md` Rule 12
- SiteForge `CLAUDE.md` Standing Order 7
- VideoForge `CLAUDE.md` (Standing Rule, MB-3 close)
- CanvasForge `CLAUDE.md` Standing Order 12
- wga `CLAUDE.md` Standing Order 7

### Step 8 — Verify downstream-safety

Check whether any other vaults federate against THIS vault as a `source_vault`. If yes, the wrapper edits must be additive only — never move or rename paths that downstream wrappers pin.

```bash
grep -r "source_vault:.*<vault_name>" <workspace_root>/*/iii/CLAUDE.md <workspace_root>/*/*/CLAUDE.md 2>/dev/null
```

Expected outcomes:
- **Zero downstream consumers** (wga MB-5 case): vacuous pass. All changes are additive at the new vault root.
- **Active downstream consumers** (CanvasForge MB-4 case — 3 downstream wrappers at SS + CC): verify that the paths the downstream wrappers pin are NOT touched by the new `iii/` directory + Standing Order. Document the downstream-safety check in the wrapper file.

### Step 9 — Wikilink sweep (only if migrating from pre-federation)

For vaults that had pre-federation III usage, sweep for stale references:

```bash
cd <workspace_root>/<vault_name>.aDNA/
grep -r "iii_corrections\|iii_domain_packs\|context_iii_" \
    --include="*.md" --include="*.yaml" --include="*.yml" \
    | grep -v "^Binary"
```

For each hit:
- If it points at the now-retired pre-federation path: either replace with the wrapper-managed path, or leave as a stale reference + add a row to `MIGRATION_NOTE.md` for later disposition.
- If it points at the canonical III.aDNA upstream: leave as-is (canonical references are correct).

### Step 10 — Register the new consumer at III.aDNA (optional but recommended)

If you have write access to III.aDNA, add a row to the MANIFEST.md § Active Consumers table:

```markdown
| `<vault_name>.aDNA` | `<vault_name>.aDNA/iii/` | <packs_used joined by comma> | **<MB-N> ✅ <YYYY-MM-DD>** — pinned at `vX.Y.Z` (commit `<hash>`); N/7 canonical packs; M modules; K local_extensions (enumerated) |
```

If you do not have write access (or the new consumer is external to the Lattice ecosystem), the wrapper still works — III.aDNA's MANIFEST is informational, not a runtime gate.

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `<vault>/iii/CLAUDE.md` | new file | Federation wrapper (federation_ref + body) |
| `<vault>/iii/what/context/<vault>_iii_learning_store.jsonl` | new file (0 bytes) | Local learning store |
| `<vault>/iii/what/context/<extension files>` | new files (if any) | Any `domain_pack` / `bridge_pack` / `local_skill` / `reviewer_registry` artifacts declared in `local_extensions` |
| `<vault>/CLAUDE.md` | edited | Standing Order added |
| `<workspace_root>/III.aDNA/MANIFEST.md` Active Consumers row | edited (optional) | New consumer registered |
| Optional: `<vault>/what/context/iii_domain_packs/MIGRATION_NOTE.md` | new file | If migrating from pre-federation, document the disposition of retired artifacts |

## Variants

### Minimal wrapper (wga MB-5 precedent)

For clean-slate consumers with no domain-specific traps, no multi-voice review, no consumer-specific orchestration skill:

- 5/7 canonical packs (minimal baseline from Step 3)
- All 8 modules
- **1** `local_extensions` entry: `learning_store_local` seeded empty
- No pre-federation migration

Fastest wrapper to author (~0.5 session). Recommended for new vaults that adopt III early.

### Full-extension wrapper (CanvasForge MB-4 precedent)

For consumers with rich domain-specific III infrastructure:

- 5/7 canonical packs (with one canonical pack deliberately omitted — e.g., `canvas_visual` — in favor of a `bridge_pack`)
- All 8 modules
- **3+** `local_extensions` entries: `bridge_pack` + `local_skill` + `learning_store_local`
- May involve pre-federation artifact relocation (worked precedent at MB-4 closed via governance registration — physical move had already happened)
- Verify downstream-safety carefully (Step 8)

Longest wrapper to author (~1 session). Required when the consumer has accumulated significant pre-federation III work.

### Bridge wrapper (VideoForge MB-3 precedent)

For consumers whose primary III usage is gated through a separate operation catalog or ADR-defined operation set (the bridge is a pointer-only pack that maps III canonical procedures onto the consumer's operations):

- 5/7 canonical packs
- All 8 modules
- **2** `local_extensions` entries: `bridge_pack` (pointer-only; `not_graduating_to_canonical: true`) + `learning_store_local`
- No `domain_pack` (the bridge_pack supplies what a domain_pack would, but pointer-only)

~1 session. Use when the consumer's domain-specific content lives in an ADR or external catalog rather than a trap pack.

### Multi-voice wrapper (SiteForge MB-2 precedent)

For consumers that use named voices in INSPECT (Voice Critic / Design / UX / SEO / Brand etc.):

- 5/7 canonical packs
- All 8 modules
- **2** `local_extensions` entries: `reviewer_registry` (YAML registry of voices) + `learning_store_local`
- Voices participate in INSPECT alongside the standard modalities; see `skill_iii_review.md` § "Reviewer Orchestra (Multi-Voice Mode)" for the activation contract.

~1 session. The reviewer registry lives in the consumer vault's existing context library (the wrapper points at it rather than relocating it).

## Worked Precedents

All 5 live wrappers in the Lattice ecosystem (as of 2026-05-12):

| Wrapper | Mission | Pin | Shape | Story |
|---------|---------|-----|-------|-------|
| `lattice-labs/iii/` | MB-1 (2026-05-08) | `v0.1.0` (`1628793`) | 7/7 packs + 8 modules + 2 local_extensions (`domain_pack` KINN brand-voice; `learning_store_local`) | First consumer wrapper; retired the operational pre-migration corrections.jsonl; KINN pack physically relocated at MB-7 |
| `SiteForge.aDNA/iii/` | MB-2 (2026-05-10) | `v0.2.0` (`04ae724`) | 5/7 packs + 8 modules + 2 local_extensions (`reviewer_registry`; `learning_store_local`) | First multi-voice wrapper; MA-3 carry-forward #2 absorbed |
| `VideoForge.aDNA/iii/` | MB-3 (2026-05-11) | `v0.2.0` (`246124d`) | 5/7 packs + 8 modules + 2 local_extensions (`bridge_pack` ADR-006; `learning_store_local`) | First inbound v0.2 cross-vault request to traverse full lifecycle; R3 risk closed |
| `CanvasForge.aDNA/iii/` | MB-4 (2026-05-11) | `v0.2.0` (`246124d`) | 5/7 packs (canvas_visual deliberately omitted) + 8 modules + 3 local_extensions (`bridge_pack` canvas; `local_skill` 5-voice canvas review; `learning_store_local`) | Full-extension; downstream-safety verified for 3 downstream wrappers at SS + CC |
| `wga.aDNA/iii/` | MB-5 (2026-05-11) | `v0.2.0` (`246124d`) | 5/7 packs + 8 modules + 1 local_extension (`learning_store_local`) | Minimal-wrapper baseline; clean-slate consumer; zero downstream vaults |

Read any of these wrappers as a concrete reference. The minimal-baseline (wga MB-5) is the cleanest starting template.

## Cross-References

- Upstream identity + protocol: `<workspace_root>/III.aDNA/CLAUDE.md`
- Companion skill (run the loop): `<workspace_root>/III.aDNA/how/skills/skill_iii_review.md`
- Consumer federation contract: `<workspace_root>/III.aDNA/what/decisions/adr_002_consumer_federation_contract.md`
- Learning store ownership: `<workspace_root>/III.aDNA/what/decisions/adr_003_learning_store_ownership.md`
- Cross-vault request standard (when consumers need to coordinate with III.aDNA on new kinds): `<workspace_root>/III.aDNA/what/artifacts/iii_airlock_standard_spec.md` (v0.2.0)
- Active consumers registry: `<workspace_root>/III.aDNA/MANIFEST.md` § Active Consumers
- Workspace router (Framework Ecosystem section): `<workspace_root>/CLAUDE.md`

## Provenance

Authored at III.aDNA Campaign B MB-6 (2026-05-12) after the 5-wrapper Campaign B P2 precedent had stabilized the federation pattern. Published to the adna base template (`<workspace_root>/.adna/how/skills/skill_iii_setup.md`) so any new aDNA vault forked from the template can self-onboard against III.aDNA without re-reading the precedent wrappers from scratch. Per ADR-002 §7 (existing consumer migration path) and Campaign B R5 (adna template is a public repo — additive only), this publication is strictly additive.
