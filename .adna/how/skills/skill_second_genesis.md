---
type: skill
skill_type: process
created: 2026-07-06
updated: 2026-07-06
status: active
category: vault_maintenance
trigger: "A vault has drifted far from the current standard (old-generation template, months-stale STATE, a goal that moved on) and is worth re-founding rather than deleting or blindly reviving"
last_edited_by: agent_rosetta
tags: [skill, second_genesis, re_genesis, stale_vault, fork, migration, dossier, operator_brief, lifecycle]

requirements:
  tools: [git, grep/rg]
  context:
    - how/skills/skill_project_fork.md      # P2 re-fork
    - how/skills/skill_project_archive.md   # P1 archive-old-first
    - how/templates/template_second_genesis_dossier.md
  permissions:
    - author a dossier + collect an operator brief
    - archive the old vault (via skill_project_archive) and fork a fresh one (via skill_project_fork)
    - run the re-genesis as its own follow-on campaign
---

# Skill: Second Genesis (re-found a stale vault at the current standard)

## Overview

> **A stale vault is not a dead vault.** When a context graph has drifted from the standard — old-generation
> template, months-stale STATE, goals that moved on without it — the answer is rarely deletion and rarely
> blind revival. **Second Genesis re-founds the vault**: a fresh fork at the **current** standard, seeded by a
> structured intake of the old graph plus a fresh operator brief, executed as its own small campaign that
> researches → reviews → improves → upgrades the old content into the new vault. The old graph archives intact
> as a quarry (SO-6/7).

This is the middle path the standard was missing between its two existing moves: **fork** (birth, from scratch)
and **version-migration** (in-place upgrade of a near-current vault). Second Genesis is for the common case in
between — a vault worth re-founding, not deleting and not blindly reviving.

**Plain version:** some projects fall so far behind that patching them in place would touch nearly every file
anyway — but they still hold real value. Rather than delete them or force a messy in-place upgrade, you re-birth
them: start a clean project at today's standard, then carefully carry the good parts across, keeping the old
version on the archive shelf as a reference.

This is a **`process`** skill: an agent authors the dossier, runs the moves, and drives the re-genesis
campaign, but the **P0 verdict** (revive-fork vs merge vs archive-only) and the campaign's phase gates are
operator decisions.

## Trigger

A vault **qualifies** when **≥2** of these hold:
- STATE.md `updated:` is >30 days old while `status:` still claims active (drift between claim and reality)
- Old-generation template markers (root `adna.md`/`CONTRIBUTING.md`; missing triad `AGENTS.md`; no `iii/`
  wrapper; a pre-current CLAUDE.md shape)
- Naming-convention drift (e.g. lowercase `oldname.aDNA` vs `<Name>.aDNA`)
- The operator's goal for the domain has changed since genesis
- Structural drift large enough that in-place upgrade would touch most files anyway

**Fork-vs-upgrade rule of thumb:** fresh-fork (this skill) when the template generation is old, staleness
>30 days, or the goal moved; **upgrade-in-place** (`skill_version_migration`) only when the vault is
near-current and merely dormant with an unchanged goal.

Do **NOT** invoke for a near-current dormant vault (that is `skill_version_migration`), nor to archive a vault
that is genuinely finished (that is `skill_project_archive` directly, `archive-only`).

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `old_vault` | string | Yes | — | The stale vault, read-only until P1 |
| `dossier` | file | Yes | — | The 9-section intake dossier (see schema below), one file `dossier_<vault>.md` |
| `operator_brief` | Q1–Q7 | Yes | — | Operator answers (collected via an ISS form per Standing Rule 8, or inline) |
| `verdict` | enum | Yes (P0) | — | `revive_fork` \| `merge_into_X` \| `archive_only` — the operator's P0 decision |

## Requirements

### Tools/APIs
- `git`, `grep`/`rg`. Composes `skill_project_archive` (P1) and `skill_project_fork` (P2).

### Context Files
- The old graph (read-only during design) + `template_second_genesis_dossier.md` for the dossier shape.

### Permissions
- Author the dossier; on P0 verdict, archive the old vault and fork a fresh one; run the re-genesis campaign.

## Dossier schema (9 sections)

The intake dossier is the structured read of the old graph that seeds the re-genesis. Template:
`how/templates/template_second_genesis_dossier.md`.

| § | Section | Captures |
|---|---------|----------|
| 1 | Identity & purpose | persona · mission statement · FAIR block · template generation · why the vault existed |
| 2 | Graph census | file counts per triad leg · top ~10 WHAT artifacts ranked with keep/improve/drop marks |
| 3 | Open work | campaigns w/ true phase reached · in-flight missions · last session · completed-without-AAR debt |
| 4 | Decisions | ADR list, each marked carry / supersede / re-decide |
| 5 | Cross-refs (breakage map) | inbound refs (router row · node inventory/curation/canvas · consumer wrappers · peer memos) + outbound refs — this map drives the close-out sweep |
| 6 | Standard drift | file-set diff vs current `.adna` · old-gen markers · missing wrappers · naming drift |
| 7 | Salvage shortlist | survive-verbatim / improve-then-carry / drop |
| 8 | Operator brief | Q1 still a live goal — **revive-fork / merge-into-X / archive-only**? · Q2 the goal NOW (1–3 sentences) · Q3 persona + new-name confirm · Q4 what is precious · Q5 what must NOT carry over · Q6 research the agent should do first · Q7 priority + first milestone |
| 9 | Recommendation | fork-vs-upgrade-vs-merge verdict + estimated re-genesis campaign size |

## Implementation — the flow (P0–P5)

Runs as its own follow-on campaign, **not** inside whatever houseclean surfaced the candidate.

### P0 — VERDICT *(operator gate)*
The operator brief Q1 decides: `revive_fork` | `merge_into_X` | `archive_only`.
- `merge_into_X` → the target vault's persona designs the absorption ([[how/skills/skill_graph_merge|skill_graph_merge.md]]).
- `archive_only` → [[how/skills/skill_project_archive|skill_project_archive.md]] path, no re-fork.
- `revive_fork` → continue to P1.

### P1 — ARCHIVE-OLD *(archive-first, because name reuse is typical)*
Archive the old vault → `Archive.aDNA/<Name>.aDNA` via `skill_project_archive` with a supersession banner
("re-genesized as `<New>.aDNA` `<date>`; dossier at `<path>`; quarry pointers …"), the root shim registered in
the node ledger, and the router-row move. **Archive-first** because the typical case reuses the canonical name
for the new vault (a name collision otherwise).

### P2 — FORK
`skill_project_fork` from the current `.adna` at the canonical `<Name>.aDNA`.

### P3 — P0-DESIGN
One design mission **in the new vault** consumes (dossier + brief + old graph read-only) → produces the
re-genesis campaign charter: research → review → improve → upgrade phases sized to the salvage shortlist. The
ADR carry-set (§4) is re-ratified **explicitly** in the new vault.

### P4 — EXECUTE
Per that charter. Old content migrates **selectively**: *improve-then-carry > verbatim*; Q5 exclusions
enforced; **reference-pointers into the archive beat wholesale copying**.

### P5 — CLOSE
Breakage-map sweep (every §5 inbound ref repointed) · node fleet-delta memo (inventory/curation/canvas regen)
· AARs · the shim retires at its window per the ledger.

## Guardrails

- **Old graph is read-only until P1**, and immutable-in-archive after.
- **Archive, never delete** (SO-6/7). The dossier + banner make the archive navigable, not a tomb.
- **Name collision → always archive-old-first** (P1 before P2).
- **Forge vaults**: consumer-wrapper contracts (`federation_ref` pins) are part of the breakage map — the
  re-genesis campaign must version-bump or hold-compatible, never silently break consumers.
- **Sensitive engagements** (client / clinical / PII-adjacent): the dossier records structure only, never
  content; credential routing per the credential-handling doctrine; the operator confirms external-party comms
  before any visible rename.
- **One re-genesis campaign at a time** per the operator priority queue — these are small campaigns, but
  parallel re-foundings multiply fleet-delta churn.

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Intake dossier | file | `dossier_<vault>.md` (9 sections) |
| Archived old graph | move | `Archive.aDNA/<Name>.aDNA` (banner + quarry) via `skill_project_archive` |
| Fresh vault | fork | `<Name>.aDNA` at the current standard via `skill_project_fork` |
| Re-genesis campaign | campaign | Charter + AARs (research → review → improve → upgrade) |
| Updated fleet surfaces | edits | Router / inventory / curation / canvas; retired shim (post-window) |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Qualifying tests fail (only 1 criterion holds) | The vault is near-current, merely dormant | Route to `skill_version_migration` (upgrade-in-place), not this skill |
| Name collision on P2 fork | Old vault still occupies the canonical name | Expected — that is why P1 (archive-old) precedes P2 (fork); never fork before archiving |
| A consumer breaks after re-genesis | `federation_ref` wrapper not repointed | The §5 breakage map must repoint every inbound ref at P5; forge vaults version-bump or hold-compatible |
| Old content copied wholesale | Verbatim migration instead of improve-then-carry | Prefer improve-then-carry + reference-pointers into the archive; enforce Q5 exclusions |

## Related
- [[how/skills/skill_project_archive|skill_project_archive.md]] — P1 archive-old-first (dependency)
- [[how/skills/skill_project_fork|skill_project_fork.md]] — P2 re-fork at the current standard
- [[how/skills/skill_graph_merge|skill_graph_merge.md]] — the `merge_into_X` verdict path
- [[how/skills/skill_workspace_spring_clean|skill_workspace_spring_clean.md]] — the houseclean that typically surfaces re-genesis candidates
- [[how/templates/template_second_genesis_dossier|template_second_genesis_dossier.md]] — the dossier schema
- **Skills Protocol**: `how/skills/AGENTS.md`

## Provenance

Designed from an operator directive to *"take in information on the old graph… and comprehensively design the
campaign planning mission that would research/review/improve/upgrade the old graph to the new standard."*
Reference implementation ran a first cohort of six intake dossiers gated in one operator pass — four re-fork
verdicts and **two deviation flags where the fork criteria correctly failed** (one routed to upgrade-in-place,
one to a merge/integration), evidence that the qualifying tests discriminate. *(Historical origin note — the
recipe is node-agnostic.)*
