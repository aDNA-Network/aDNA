---
type: disposition_ledger
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
last_edited_by: agent_{username}
tags: [disposition_ledger, spring_clean, houseclean, shim_registry]
workspace_root: ~/<workspace_root>
campaign: campaign_<slug>
gate_status: # pre_gate | ratified | executing | closed
---

# Disposition Ledger — {campaign}

> The **single decision surface** for a workspace houseclean (`how/skills/skill_workspace_spring_clean.md`).
> Author §A–H **read-only** in Phase 1; the operator ratifies **per section** at THE gate (Phase 2); the waves
> execute (Phase 3). **§C is STANDING** — it outlives the campaign as the node's permanent shim registry.
> Nothing in this ledger mutates disk before ratification.

**Tier key** — **T0** auto-safe (OS cruft, regenerable caches) · **T1** per-item (moves + ref-sweeps, orphan
archives) · **T2** gated (legacy code, large/sensitive data). **Preserve-first:** caches (`.venv`,
`__pycache__`) are **never** auto-deleted; T0 is OS cruft only.

## §A — Top-level objects
Every object at the workspace root with a proposed disposition. *Closes after Wave 1.*

| Entry | Size | Class | Proposed disposition | Tier | Notes |
|-------|------|-------|----------------------|------|-------|
| `<object>` | | cruft / loose-spec / orphan-scaffold / legacy-repo / cache | delete / move→`<path>` (+ref-sweep) / archive→`_archive/` / →§F salvage | T0/T1/T2 | |

## §B — Router & registry deltas
Changes to the workspace router + node inventory driven by this clean. *Closes after Wave 3.*

| Delta | Status | Notes |
|-------|--------|-------|
| Router row `<Vault>.aDNA` | pending / done | updated / dropped / archived-form |
| Inventory row `<Vault>.aDNA` | pending / done | `vault_count` ±N |
| Derived projections (cards/curation/canvas/registry) | → one batched regen | never per-event |

## §C — Shim & symlink registry  *(STANDING — post-campaign; the load-bearing section)*
Every forwarding symlink on the node. **Register at creation.** Retirement is **conjunctive**: *window-lapse ∧
verified ref-sweep-zero (excl. `_archive/` + session history) ∧ owner-ack (where owner ≠ node steward)*. A
lapsed window alone never auto-retires; retirements batch into pre-authorized waves.

| Shim | Target | Class | Window-end | Retire-condition | Owner | Retired (date · commit) |
|------|--------|-------|-----------|------------------|-------|--------------------------|
| `<Old>.aDNA` | `<New>.aDNA` | rename | ~+30d | window ∧ ref-0 ∧ wrappers repointed | `<persona>` | |
| `<Old>.aDNA` | `Archive.aDNA/<Old>.aDNA` | archive | ~+30d | window ∧ ref-0 ∧ owner-ack | `<steward>` | |
| `<Source>.aDNA` | `Archive.aDNA/<Source>.aDNA` | merge-archive | ~+30d | window ∧ ref-0 (0 broken live; content folded) ∧ absorber-persona ack | `<steward>+<absorber>` | |

> Classes (expand as needed): `rename` · `archive` · `merge-archive` · `dual-home` (code relocation) ·
> `deprecation` (in-code/in-schema alias) · `host-move` (git remote) · `wrapper-relocation` · `runtime-state-dir`
> · `env-var-alias`. Row-notes record unusual conditions (code-coupled, partial-by-mandate, cross-org) + the
> coordinating memo/ADR.

## §D — Vault triage
Every `<Name>.aDNA` vault gets an operator verdict. *Closes after Phase 1.*

| Vault | Verdict | Evidence / next step |
|-------|---------|----------------------|
| `<Vault>.aDNA` | active / **second-genesis** / **archive** / **compliant-by-ADR** | STATE freshness · health · dossier ref |

## §E — Second-genesis queue
Re-found candidates with read-only dossiers + gate verdicts. *Dispatch outstanding after close (each is its own
follow-on campaign — `skill_second_genesis`).*

| Old vault | Recommendation | Dossier | Gate verdict | Priority |
|-----------|----------------|---------|--------------|----------|
| `<Vault>.aDNA` | re-fork / merge-into-`<X>` / archive-only | `dossier_<vault>.md` | approve / amend | |

## §F — Salvage & subsume manifest
Legacy code/vaults folded into a target. *Closes with the ack-keyed archive.*

| Target | Size | Manifest | Intake drop | Ack | End-state |
|--------|------|----------|-------------|-----|-----------|
| `<Legacy>` → `<Absorber>` | | keep/improve/drop rows | manifest + quarry index | pending / ✅ `<persona>` | archived → `Archive.aDNA/` + shim §C#N |

## §G — Deferred / `#needs-human`
Operator/owner-gated; **no action this campaign.** *Remains open.*

| Item | Why deferred | Owner gate |
|------|--------------|-----------|
| `<item>` | legal/IP · policy cadence · cross-vault ownership | operator / `<persona>` |

## §H — Upstream artifacts
Framework gaps surfaced by the clean, filed as `idea_upstream_*`. *Closes at Phase 4.*

| Artifact | Source finding | Status |
|----------|----------------|--------|
| `idea_upstream_<name>.md` | | filed / accepted |
