---
type: skill
skill_type: agent
created: 2026-07-06
updated: 2026-07-06
status: active
category: vault_maintenance
trigger: "One `<Name>.aDNA` graph is being absorbed into another — drain the source into an absorber vault, fold its content, repoint every live reference, and archive the drained shell"
last_edited_by: agent_rosetta
tags: [skill, merge, absorb, fold, federation, cross_vault, guardrail6, archive, lifecycle]

requirements:
  tools: [git, grep/rg]
  context:
    - CLAUDE.md                         # the workspace router (rows change)
    - how/skills/skill_project_archive.md  # the archive step this skill ends by calling
    - how/skills/skill_project_rename.md   # the shared keep/strip sweep classifier
  permissions:
    - fold the source's content into the absorber (a second persona's vault — via coordination memo)
    - path-scoped edits to the workspace router, node inventory, and consumer federation wrappers
    - archive the drained source (via skill_project_archive) and register a merge-archive shim
---

# Skill: Graph Merge (absorb one vault into another, then archive the source)

## Overview

A **merge** drains one `<Source>.aDNA` graph **into** another `<Absorber>.aDNA` — folding the source's content
into the absorber, repointing every live reference to its new home, and archiving the drained shell. It is the
heavier sibling of [[how/skills/skill_graph_rename|skill_graph_rename.md]]: the two share their reference-sweep
machinery, but a merge adds five concerns a rename never has — a **second persona's vault is written into**,
**content moves** (not just a name), the **source is archived with no live-name symlink**, **federation
re-anchors** to the absorber, and **cross-vault write authority** must be resolved (Guardrail 6).

**Plain version:** sometimes two projects should become one. A merge carefully pours everything worth keeping
from the old project into the surviving one, updates every signpost that pointed at the old project so it now
points at the right shelf inside the new one, and then retires the emptied old project to the archive — without
losing history or breaking anything that depended on it.

**The load-bearing discipline is *repoint-before-archive*.** After a merge the source's internal layout
*changes* (`<Source>/what/x/` becomes `<Absorber>/what/<topic>/x/`), so — unlike a rename symlink — a
`<Source> → Archive/<Source>` shim resolves **only top-level audit paths to the frozen archived copy**, never
sub-paths into the absorber. The gate is therefore **zero broken live pointers**: every live reference is
repointed to its new absorber home *first*; the shim is an audit convenience for stragglers, not a substitute.
The second discipline is **Guardrail 6** — the absorber belongs to another persona, so a coordination memo
precedes the fold and the absorber-side commit lands under the receiving persona's authority.

## Trigger

Invoke when a decision (an accepted ADR / merge mission / operator directive) names a **source** graph to be
absorbed into a named **absorber** graph.

Do **NOT** invoke:
- For a **rename** (the vault keeps its content and lives on under a new name) → [[how/skills/skill_graph_rename|skill_graph_rename.md]].
- For a **directory move with no absorption** (relocating an active vault) → `skill_workspace_path_migration`.
- To archive a **standalone** finished vault (nothing folds anywhere) → [[how/skills/skill_project_archive|skill_project_archive.md]] directly.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `source_vault` | string | Yes | — | The graph being drained + archived, e.g. `OldVault.aDNA` |
| `absorber_vault` | string | Yes | — | The surviving graph the content folds into |
| `fold_map` | table | No | proposed in memo | Per-subtree disposition (WHAT→fold-path · live-HOW→fold · closed-HOW/WHO/gov→archive); the receiving persona confirms the absorber `what/` home |
| `dry_run` | bool | No | `true` | Produce the classified ref-sweep + the proposed fold-map without touching disk; the receiving persona + operator confirm before any write |

## Requirements

### Tools/APIs
- `git` (per-vault surgical commits; history-preserving archive move), `grep`/`rg` (fleet-wide ref sweep).
- Composes [[how/skills/skill_project_archive|skill_project_archive.md]] (the final archive step) and reuses
  [[how/skills/skill_project_rename|skill_project_rename.md]]'s keep/strip classifier for the sweep.

### Context Files
- The workspace router `CLAUDE.md`, the node inventory, and any consumer `federation_ref` wrappers on the source.

### Permissions
- Fold content into the absorber (via the coordination memo — the absorber is another persona's vault);
  path-scoped repoints to the router / inventory / consumer wrappers; archive the source + register the shim.

## Implementation

### Step 1: Pre-flight (hard gate)
Confirm the merge is decided and read any merge manifest. Verify HEAD and **no conflicting active session**
(resume-race). Confirm the **source** working tree is clean and it is not mid-campaign.

### Step 2: Full-grep the source + classify (don't trust the count)
Grep the workspace for the source name and classify every hit — the raw total runs **~3× the true live set**,
so the count is a planning signal, never a gate:

```bash
grep -rl "<source_vault>" ~/<workspace_root> --include='*.md' --include='*.yaml' --include='*.json' \
  | grep -vE '/_archive/|/sessions/history/' | sort
```

| Class | Disposition |
|-------|-------------|
| **LIVE** | routing / `federation_ref` / live specs+ADRs / configs — **repoint to the absorber path** |
| **HISTORICAL** | CHANGELOG · STATE narration · AARs · dated coord memos — **verbatim, never counted** |
| **TEMPLATE-EXAMPLE** | skill/doc files naming the source as an *illustrative example* (copied fleet-wide) — refresh via the template-release / doc-currency pass, **not** this sweep |
| **DERIVED** | render projections (vault cards, curation, canvas, registry JSON) — **batch-regen**, never per-merge |

In `dry_run`, stop after classification and report the LIVE set (if it comes back large, re-check the
classifier — especially the template-example bucket — before any write).

### Step 3: Absorber-capacity pre-check (the merge go/no-go)
A merge writes *into* a second vault. Gate the absorber before any fold — this is the merge's analog of the
rename test-gate:
```bash
git -C <absorber_vault> status --short     # MUST be clean — a dirty absorber ⇒ defer (collision risk)
ls <absorber_vault>/how/campaigns/         # scan for a concurrent active campaign/mission
```
A clean tree is mandatory. A concurrent active mission is **not** a block but a **timing** point — the merge
never auto-advances the absorber's own held phase; the receiving persona reconciles that next session. **Never**
make a vault both a source and an absorber in the same wave.

### Step 4: Code-coupled pre-check
If the source carries a code-as-WHAT layer (a package on `sys.path`, a nested repo, a re-export shim), **defer
its relocation to the P5 code-as-WHAT phase** unless the absorber's `what/` is demonstrably ready. Establish a
**green test gate** across the fold for any code that does move (green-before / green-after).

### Step 5: Coordination memo → receiving persona (Guardrail 6)
The fold is a heavy write into another persona's graph, so the single-writer rule is honored by a memo that
**precedes** the fold: it states the fold target, what folds vs. what's preserved-in-archive, the federation
re-anchor, and the archive plan. The receiving persona answers the absorber `what/` home; their ack authorizes
the absorber-side writes. *(When source and absorber share one persona, this step is light — there is no
cross-persona authority handoff; the driver becomes absorber-concurrency, not authority.)*

### Step 6: Content-fold (preserve-don't-rewrite)
Fold per subtree, per the confirmed `fold_map`:

| Source subtree | Default disposition |
|----------------|---------------------|
| **WHAT** (`context/`, `decisions/`, `docs/`, `lattices/`, assets, ontology) | **fold** → `<Absorber>/what/<topic>/` (the substantive payload) |
| **HOW** — *live* campaigns/missions/skills | **fold** → `<Absorber>/how/` only if still operative |
| **HOW** — *closed*/source-specific records (sessions, AARs, the source's own migration campaign) | **preserve in archive** (audit trail) |
| **WHO** + governance (CLAUDE/MANIFEST/STATE/CHANGELOG, genesis narrative) | **preserve in archive** — the absorber keeps **its own** identity; never rewrite the source's genesis story into it |

**Preserve-don't-rewrite:** counsel-gated, legal-provenance, or brand-framed content folds **verbatim** —
location changes, framing does not. A fold that *honors* a prior keep-decision is not a rebrand; a genuine
reversal of a prior split **is** — flag a true reversal in the manifest.

### Step 7: Re-anchor federation
Repoint each consumer's `federation_ref` (`source_vault`/`source_path`) from the source to the absorber's new
fold path. The source's **own** wrappers (e.g. its `iii/` consumer registration) **transfer** to the absorber if
it doesn't already consume that framework, or **dissolve/dedupe** into the absorber's existing wrapper if it
does. Re-verify the wrapper census **live** — manifests undercount wrappers by ~3× (application-named wrappers
hide).

### Step 8: Absorber commit (receiving persona's authority)
Commit the fold into the absorber attributed to / acked by the receiving persona (the mechanical work may be
executed by the merge driver, but the commit lands under the absorber persona's authority per the memo).

### Step 9: Cross-fleet live-ref sweep
Repoint every remaining **LIVE** pointer (router row, node inventory, live specs/ADRs) source → absorber-path,
with **per-vault surgical commits** (stage only swept paths; one vault = one commit; a dirty vault → skip + flag).
Historical stays verbatim; template-example + derived defer to the doc-currency/regen pass.

### Step 10: Archive the drained source
Call [[how/skills/skill_project_archive|skill_project_archive.md]] with `retirement_reason: merged` and
`successor_or_quarry: <absorber_vault>/what/<topic>/`. It moves the source intact under the Archive holder,
banners it, moves the router row, drops the registry entry, and registers the shim — **class `merge-archive`**,
whose retire-condition notes that consumers still resolving through it (deferred code/wrapper refederation) must
be repointed before retirement.

### Step 11: Close
Re-grep the source name → confirm **zero broken live pointers** (historical / template-example / derived remain
— correct). Record the count. Batch the one coordinated inventory/curation/canvas regen for the drop. File the
5-line AAR in the mission record.

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Folded content | edits | Source WHAT (+ live HOW) now under `<Absorber>/what/<topic>/`, preserve-set intact in the archive |
| Re-anchored federation | edits | Consumer `federation_ref`s + the source's own wrappers point at the absorber |
| Repointed live refs | edits | Every live inbound pointer now resolves to the absorber path (zero broken) |
| Archived source | move | `Archive.aDNA/<source_vault>/` (banner + `merge-archive` shim) via `skill_project_archive` |
| Retired router row + dropped registry entry | edits | Router reflects the merge; inventory row dropped; `vault_count` −1 |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Broken sub-path links after archiving | Relied on the shim to resolve sub-paths into the absorber | The merge shim resolves **top-level only** to the frozen archive — repoint sub-path refs to the absorber (Step 9); fix folded-content internal self-refs at the doc-currency pass |
| Absorber tree dirty / mid-campaign | Skipped Step 3 | Defer the fold until the absorber is clean; a concurrent mission is a timing point for the receiving persona, not a merge auto-advance |
| Cross-vault write without authorization | Skipped the Guardrail-6 memo | The absorber is another persona's vault — the memo + their ack authorize the fold; the absorber commit lands under their authority |
| LIVE set came back huge | Template-example / historical hits miscounted as live | Re-run the Step-2 classifier; the true live set is small — trust the classifier, not the raw count |
| Genesis story duplicated in the absorber | WHO/governance folded instead of archived | Preserve WHO/governance/genesis in the archive; the absorber keeps its own identity (data-integrity) |
| Code broke after the fold | Code-as-WHAT relocated before the absorber was ready | Defer code relocation to P5 behind a green test gate (Step 4); the local merge commits but never pushes — remote-repo disposition is a separate downstream step |

## Related
- [[how/skills/skill_project_archive|skill_project_archive.md]] — the leaf this skill calls to retire the drained source
- [[how/skills/skill_graph_rename|skill_graph_rename.md]] — the sibling; shares the reference-sweep machinery (a rename keeps a live symlink, a merge does not)
- [[how/skills/skill_project_rename|skill_project_rename.md]] — the keep/strip classifier reused in Step 2
- [[how/skills/skill_second_genesis|skill_second_genesis.md]] — the `merge_into_X` verdict routes here
- [[how/skills/skill_workspace_spring_clean|skill_workspace_spring_clean.md]] — gathers many merges behind one operator gate
- **Skills Protocol**: `how/skills/AGENTS.md`

## Provenance

Codified from a merge/absorb playbook that converged across four graph merges on the reference node (a
whitepaper→protocol consolidation, a forge→standard-bearer absorption, a code-coupled reversal, and an
intra-persona HQ merge; 2026-06 cohort). The proven findings it carries: difficulty scales with code-coupling +
reversal-of-prior-decision + absorber-concurrency (never source file-count); the absorber-capacity pre-check is
the merge analog of the rename test-gate; and *partial-by-mandate* merges (a defined slice stays live for a later
phase) are a first-class shape whose deferred half rides the shim's retire-gate. *(Historical origin note — the
recipe is node-agnostic.)*
