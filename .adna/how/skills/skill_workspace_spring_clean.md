---
type: skill
skill_type: process
created: 2026-07-06
updated: 2026-07-06
status: active
category: vault_maintenance
trigger: "The workspace has accumulated drift — cruft at the root, stale vaults, superseded graphs, unregistered shims — and needs a fleet-wide houseclean that classifies every disposition into one ledger and executes it behind a single operator gate"
last_edited_by: agent_rosetta
tags: [skill, spring_clean, houseclean, disposition_ledger, orchestrator, shim_registry, operator_gate, lifecycle]

requirements:
  tools: [git, grep/rg]
  context:
    - CLAUDE.md                              # the workspace router (rows change across the clean)
    - how/templates/template_disposition_ledger.md  # the single decision surface this skill fills
    - how/skills/skill_create_iss.md          # THE operator gate is rendered as an ISS
  permissions:
    - author a read-only disposition ledger over the whole workspace (nothing mutates before the gate)
    - on operator ratification, execute the ledger in waves — calling the lifecycle skills
    - install/maintain the STANDING shim registry (§C) + record pre-authorized retirement waves
---

# Skill: Workspace Spring Clean (fleet houseclean behind one operator gate)

## Overview

Spring Clean is the **orchestrator** of the graph lifecycle. Where [[how/skills/skill_project_archive|skill_project_archive.md]],
[[how/skills/skill_graph_merge|skill_graph_merge.md]], [[how/skills/skill_graph_rename|skill_graph_rename.md]],
and [[how/skills/skill_second_genesis|skill_second_genesis.md]] each retire, fold, rename, or re-found **one**
graph, Spring Clean surveys the **whole workspace**, classifies every disposition — root cruft, stale vaults,
superseded graphs, salvage candidates, unregistered shims — into **one disposition ledger**, and executes them
in waves **behind a single operator gate**. It is a periodic program, not a one-off.

**Plain version:** every workspace collects clutter over time — leftover files at the root, projects that
drifted or were replaced, forwarding-links no one tracked. Rather than clean these piecemeal (and pester the
operator for each), Spring Clean does one thorough walk-through, writes down every proposed disposition in a
single list, gets **one** yes/no/amend from the operator on the whole list, then carries it out in tidy waves —
keeping a permanent registry of every forwarding-link so none is ever silently retired.

**The load-bearing discipline is *one gate, nothing-before-it*.** The entire survey is **read-only** until the
operator ratifies the ledger — nothing mutates on disk before the verdict. Spring Clean's value is exactly that
it **batches** what would otherwise be dozens of individual lifecycle-skill dry-runs into one decision surface,
so the operator ratifies once and the waves execute deterministically. Its second discipline is the **STANDING
shim registry** (ledger §C): every forwarding symlink is registered at creation and only ever retired on the
conjunctive gate *window-lapse ∧ ref-sweep-zero ∧ owner-ack* (Standing Rule 9) — a lapsed window alone never
auto-retires.

## Trigger

Invoke periodically, or when fleet drift has accumulated: cruft at the workspace root, vaults whose STATE is
months-stale, graphs superseded/merged without a clean archive, or a health check flagging unregistered shims.

Do **NOT** invoke:
- For a **single known disposition** — call the specific lifecycle skill directly (archive / merge / rename /
  second-genesis). Spring Clean is for the *fleet-wide* sweep that batches many.
- To mutate anything **before** the operator gate — the survey is read-only by contract.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `workspace_root` | string | Yes | — | The workspace to survey (all top-level objects + every `<Name>.aDNA` vault) |
| `ledger` | file | Yes (Phase 1) | — | The disposition ledger (`template_disposition_ledger.md`), §A–H — the single decision surface |
| `operator_verdicts` | per-section | Yes (Phase 2) | — | Operator approve/amend per ledger section, collected at the gate |

## Requirements

### Tools/APIs
- `git`, `grep`/`rg`. Renders the gate via an operator decision surface (`skill_create_iss` where the vault ships it, else `AskUserQuestion`) and calls the
  four single-graph lifecycle skills during execution.

### Context Files
- The workspace router + node inventory; the disposition-ledger template for the ledger shape.

### Permissions
- Author the read-only ledger; on ratification, execute the waves; install/maintain the §C shim registry.

## Implementation — the phased flow

### Phase 1 — Survey & Ledger (read-only)
Snapshot the pre-clean state. Author the disposition ledger (template: `how/templates/template_disposition_ledger.md`):
- **§A top-level objects** — every root object with a proposed disposition, tiered **T0** (auto-safe: OS cruft,
  `__pycache__`), **T1** (per-item: loose specs to move + ref-sweep, orphan scaffolds to archive), **T2** (gated:
  legacy code repos, large/sensitive data → salvage or `#needs-human`). Preserve-first: caches are **never**
  auto-deleted.
- **§D vault triage** — every vault gets a verdict: `active` · `second-genesis` (stale, re-found) · `archive`
  (superseded/finished) · `compliant-by-ADR` (recorded so audits stop re-flagging).
- **§F salvage manifest** — for any legacy code/vault to subsume: keep/improve/drop rows + the intake drop.
- Author a **second-genesis dossier** (read-only, 9-section) for each candidate the triage marks re-found
  ([[how/skills/skill_second_genesis|skill_second_genesis.md]]).

Nothing touches disk in Phase 1 beyond the ledger + dossiers themselves.

### Phase 2 — THE operator gate
Render the ledger as an ISS decision surface (`skill_create_iss`). Submit the ledger + triage + dossiers +
salvage manifest + the shim policy + any pre-authorizations. **Nothing mutates until the verdict.** The operator
approves/amends **per section**; the ledger records every verdict. Archive the gate; release the execution
waves.

### Phase 3 — Execute in waves
- **Wave 1 — root hygiene + governance:** T0 auto-clean; T1 per-item moves + their ref-sweeps; `git init` any
  untracked vault; register every new shim in §C.
- **Wave 2 — salvage/subsume + archive:** stage the intake drop for salvage targets (ack-keyed); on ack, retire
  via [[how/skills/skill_project_archive|skill_project_archive.md]]. Superseded/merged graphs archive (archive)
  or fold ([[how/skills/skill_graph_merge|skill_graph_merge.md]]); renames run
  [[how/skills/skill_graph_rename|skill_graph_rename.md]]. Each re-genesis candidate spins its **own follow-on
  campaign** (`skill_second_genesis`), **not** inside this houseclean.
- **Wave 3 — archive index + compression + shim ledger:** author the archive index; compress P1-deferred blobs
  (count → `tar` → verify → remove original); install/refresh the **§C STANDING** registry banner + wire the
  health-check that flags unregistered shims.

### Phase 4 — Close
File upstream ideas for any framework gaps surfaced. Run **one coordinated** fleet-delta regen
(inventory/curation/canvas) — never per-event. Record **pre-authorized shim-retirement waves** (dated
one-liners, no new gate) so lapsed shims retire in batches on their conjunctive condition. Close with the
campaign AAR.

## The disposition ledger (§A–H)

The ledger is the single decision surface. Template: `how/templates/template_disposition_ledger.md`.

| § | Section | Mutability |
|---|---------|-----------|
| **A** | Top-level objects (disposition + tier per row) | closes after Wave 1 |
| **B** | Router & registry deltas | closes after Wave 3 |
| **C** | **Shim & symlink registry** | **STANDING (post-campaign)** — the load-bearing section |
| **D** | Vault triage (operator verdict per vault) | closes after Phase 1 |
| **E** | Second-genesis queue (dossiers + verdicts) | dispatch outstanding after close |
| **F** | Salvage & subsume manifest | closes with the ack-keyed archive |
| **G** | Deferred / `#needs-human` (operator/owner-gated) | remains open |
| **H** | Upstream artifacts (ideas filed) | closes at Phase 4 |

**Shim-window discipline (Standing Rule 9).** Every shim is registered at creation with **class · window
(default 30d) · retire-condition · owner**. Retirement is **conjunctive** — *window-lapse ∧ verified
ref-sweep-zero (excluding `_archive/` + session history) ∧ owner-ack (where owner ≠ the node steward)*. A lapsed
window alone never auto-retires; retirements batch into pre-authorized waves. Classes expand over time
(`rename` · `archive` · `merge-archive` · `dual-home` · `deprecation` · `host-move` · `wrapper-relocation` · …).

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Disposition ledger | file | §A–H, ratified per section at the gate — the audit record of every disposition |
| Executed waves | edits + moves | Root hygiene · archives/merges/renames · salvage subsumes · compression |
| Second-genesis queue | dossiers | Read-only dossiers with operator verdicts, dispatched as follow-on campaigns |
| STANDING shim registry | §C + health-check | Every shim registered; unregistered shims flagged; retirement waves recorded |
| One fleet-delta regen | edits | Single coordinated inventory/curation/canvas regen for all drops |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Disk mutated before the gate | Ran a wave in Phase 1 | Phase 1 is read-only by contract — only the ledger + dossiers are authored; all mutation waits for the Phase 2 verdict |
| A cache/data tree was auto-deleted | T0 mis-tiered | T0 is OS cruft + regenerable caches only; legacy code, `.venv`, and large/sensitive data are T2 (gated) or `#needs-human` (§G) |
| A shim can never be retired | Registered without a retire-condition | Register class + window + retire-condition + owner at creation; retire only on the conjunctive gate |
| A re-genesis ran inside the houseclean | Re-founding folded into the sweep | Each re-genesis is its **own** follow-on campaign (`skill_second_genesis`); the houseclean only surfaces + dossiers the candidate |
| Fleet renders churned N times | Regenerated per-event | Batch **one** coordinated fleet-delta regen at Phase 4 |

## Related
- [[how/skills/skill_project_archive|skill_project_archive.md]] — the archive disposition (Wave 2)
- [[how/skills/skill_graph_merge|skill_graph_merge.md]] — the merge disposition (Wave 2)
- [[how/skills/skill_graph_rename|skill_graph_rename.md]] — the rename disposition (Wave 2)
- [[how/skills/skill_second_genesis|skill_second_genesis.md]] — the re-found disposition (its own follow-on campaign)
- [[how/templates/template_disposition_ledger|template_disposition_ledger.md]] — the §A–H ledger this skill fills
- `skill_create_iss` (project-level ISS skill, where the vault ships it) — renders THE operator gate (Phase 2)
- **Skills Protocol**: `how/skills/AGENTS.md`

## Provenance

Codified from a two-operation fleet-houseclean campaign on the reference node (a pre-migration *mise en place*
then a post-move *spring clean*, 2026-06 cohort) whose eight-mission arc established this skill's spine: one
read-only ledger, one operator gate, waved execution, and the STANDING shim registry that became Standing Rule
9. It is the orchestration layer above the four single-graph lifecycle skills — the houseclean that surfaces the
candidates the others then retire, fold, rename, or re-found. *(Historical origin note — the recipe is
node-agnostic.)*
