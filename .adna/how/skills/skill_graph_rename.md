---
type: skill
skill_type: agent
created: 2026-07-06
updated: 2026-07-06
status: active
category: vault_maintenance
trigger: "A fleet-referenced `<Old>.aDNA` graph is being renamed to `<New>.aDNA` — mv the vault, register a back-compat shim, sweep every live reference across the fleet, and refederate consumer wrappers"
last_edited_by: agent_rosetta
tags: [skill, rename, ref_sweep, identity_cascade, shim, federation, graduation, two_layer, lifecycle]

requirements:
  tools: [git, grep/rg, perl/sed]
  context:
    - CLAUDE.md                          # the workspace router row + layout tree
    - how/skills/skill_project_rename.md   # DELEGATE the vault's own self-routing sweep to this
    - what/decisions/adr_042_fork_template_hygiene_and_rename_protocol.md  # §6.5 rename protocol
  permissions:
    - rename the vault directory + create/register a back-compat shim
    - path-scoped edits to the renamed vault's own surfaces, the router, and consumer wrappers
    - rename a code-coupled layer under a green test gate (separate rollback unit)
---

# Skill: Graph Rename (rename a fleet-referenced vault, sweep every live reference)

## Overview

This skill renames a `<Old>.aDNA` graph to `<New>.aDNA` and repoints every **live** reference across the
fleet — the vault's own surfaces, the workspace router, cross-vault pointers, and consumer `federation_ref`
wrappers — while leaving the audit trail verbatim and keeping consumers resolving through a back-compat shim.
It is the sibling of [[how/skills/skill_graph_merge|skill_graph_merge.md]] (a rename keeps a live symlink; a
merge does not) and the fleet-scale big brother of [[how/skills/skill_project_rename|skill_project_rename.md]]
— **it delegates the renamed vault's own self-routing sweep to that skill's keep/strip classifier** rather than
re-deriving it.

**Plain version:** renaming a project is not just moving its folder — dozens of other files point at the old
name. This skill moves the folder, leaves a forwarding symlink so nothing breaks immediately, then walks the
whole workspace fixing every *live* signpost (routing, wrappers, configs) to the new name — while carefully
leaving *historical* mentions (changelogs, past decisions) exactly as they were, because rewriting history
would falsify the record.

**The load-bearing rule is the *live-vs-historical* split, and it drives the shim-retirement gate — not the
rename.** A raw grep of the old name runs **~3× the true live set**; most hits are legitimate historical
provenance that MUST stay verbatim (archive-don't-delete). Because the rename leaves a `<Old> → <New>` symlink,
old paths keep resolving, so the goal is *zero live refs to the old name*, which retires the shim later (never
racing the rename). The second rule is the **two-layer split**: the governance/identity layer renames freely,
but a **code-coupled** layer (importable package, machine-consumed identifiers) renames only under a green test
gate — or defers wholesale when its owning repo is dirty or the change is upstream-gated.

## Trigger

Invoke as the mechanism of any vault/persona rename that other vaults reference (Standard §6.5 makes the
rename-time live-ref sweep a MUST), or to complete a rename that was done without one.

Do **NOT** invoke:
- For a vault's **own** self-routing residue with no fleet cascade (a light, single-vault sweep) →
  [[how/skills/skill_project_rename|skill_project_rename.md]] directly.
- For absorbing one graph **into** another (content folds, source archives) → [[how/skills/skill_graph_merge|skill_graph_merge.md]].
- For a directory move with no identity change → `skill_workspace_path_migration`.
- To bulk-rewrite historical mentions (that falsifies the audit trail, §15).

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `old_name` | string | Yes | — | The retiring identity token(s) — vault and/or persona (accepts several when a rename cascades) |
| `new_name` | string | Yes | — | The current identity token(s) the routing should reflect |
| `has_code_layer` | bool | No | detect | Whether a code-as-WHAT package carries the old identity (found by `rev-parse`, not assumption) |
| `dry_run` | bool | No | `true` | Full-grep + classify + locate the code layer without editing; operator confirms before any write |

## Requirements

### Tools/APIs
- `git` (per-vault surgical commits, separate code-repo rollback unit), `grep`/`rg` (fleet-wide sweep),
  `perl`/`sed` (idempotent scoped edits — BSD `sed` lacks `\b`, so use `perl -pe` for word boundaries).
- Delegates to [[how/skills/skill_project_rename|skill_project_rename.md]] for the vault's own self-routing sweep.

### Context Files
- The workspace router `CLAUDE.md`, the node inventory (`inventory_vaults`), and consumer wrappers.

### Permissions
- Rename the directory + register the shim; path-scoped repoints across the fleet; rename the code layer under
  a test gate.

## Implementation

### Step 1: Pre-flight — full-grep + classify (the count is a planning signal, never a gate)
Verify HEAD and no conflicting active session. Grep the old name fleet-wide; record the total, then **classify**
(the raw total runs ~3× the true live set):

```bash
grep -rl "<old_name>" ~/<workspace_root> --include='*.md' --include='*.yaml' --include='*.py' \
  --include='*.toml' --include='*.json' --include='*.canvas' | grep -v '/_archive/' | sort
```

| LIVE (repoint) | HISTORICAL (verbatim) | DEFERRED (swept elsewhere) |
|----------------|------------------------|-----------------------------|
| router rows · `federation_ref` · current ADRs/skills/configs · `inventory_*` · active pointers | CHANGELOG · STATE narration · AARs · dated coord memos · router backups · `_archive/` | **derived renders** (cards/curation/canvas/registry JSON → one batched regen) · **in-flight internal campaigns** (→ owning persona's cadence) · **soft refs in already-stale lists** (→ their cohort) |

Heuristic: *drives a live action (resolves a path, federates, routes, configures)?* → LIVE. *Narrates something that happened?* → HISTORICAL.

### Step 2: Code-coupled pre-check (locate by `rev-parse`, not assumption)
Find any code-as-WHAT layer **wherever it lives** — nested (`find <old>.aDNA/what -name .git -type d`) *or* a
sibling repo. `git -C <code-dir> rev-parse --show-toplevel` to learn the *owning* repo, and `git -C <owner>
status --short` for whether it is dirty / mid-migration. **If the owner can't take a clean commit this leg, or
the change is upstream-gated → defer the whole code layer** (two-layer split; lock its target name in the ADR +
deferral ledger). Flag any schema `const` / federation field-names as **graduation-class** (Step 5). Establish
the **green test baseline** (record the pass count). Skip if wrapper-only — confirm "code-coupled layer: NONE".

### Step 3: Internal rename + shim (register at creation)
```bash
mv <old>.aDNA <new>.aDNA          # disk-only — the workspace root is not a git repo
ln -s <new>.aDNA <old>.aDNA       # back-compat shim
```
**Register the shim row immediately** in the node shim ledger (class `rename` · window · retire-condition
`ref-sweep-zero + wrappers repointed` · owner) per Standing Rule 9. Order matters (Guardrail #9): rename +
register **before** touching consumer wrappers.

### Step 4: Sweep the renamed vault's own surfaces — DELEGATE to `skill_project_rename`
Run [[how/skills/skill_project_rename|skill_project_rename.md]] (`old_name`, `new_name`, `vault_root=<new>.aDNA`)
to sweep the vault's **own** live-routing governance files with its **keep/strip classifier** — that skill owns
the per-line strip-vs-keep judgment; do not re-derive it here. Then extend the scoped, idempotent sed
(`@` delimiter) to the vault's other live surfaces its classifier doesn't cover — `skills/`, `*.lattice.yaml`,
configs — leaving internal historical prose verbatim.

> **Word-collision case** (the new name is also a common word, e.g. a framework it builds): a blanket replace
> corrupts prose. Use a **two-pass, qualified-token** sed — flip everything to the **qualified `<New>.aDNA`**
> form (qualified-first so pass 2 can't double-suffix), never the bare new word; guard remote-URL lines; add a
> one-line identity clarifier to the new `CLAUDE.md`; and **post-sweep re-grep the old name to catch guard
> false-negatives** — never trust the guarded sed alone.

### Step 5: Two-layer split — code layer under a green test gate
Rename the code-coupled layer as a **separate rollback unit**, sweeping *all* of: import statements · bare
`X.attr` in bodies + docstrings · quoted module-path strings · dir-name strings / CLI defaults · `pyproject.toml`
(name, packages, mypy overrides, coverage source, script targets — **preserve `[project.urls]`**) · `MANIFEST.in`
· pre-commit hook `entry:` · version tags. Reinstall editable; **re-run the test gate → green-after, 0 new
failures**; red → `git reset --hard` to the governance checkpoint. Commit in the **code repo** (its own HEAD is
the rollback unit). Graduation-class (schema `const` / field names / consumer contracts) → apply the
**accept-both** deprecation pattern (`const`→`enum [new, old]`; keep both fields; register the alias as a §C
deprecation shim; verify a new pin validates, an old pin validates, a missing-required pin is rejected —
**before** committing) and surface the true scope to the operator first.

### Step 6: Router (serialize — no parallel router edits)
Back up `~/<workspace_root>/CLAUDE.md`; update the router row + Workspace-Layout tree + ecosystem mention; note
the shim. Commit.

### Step 7: Cross-fleet live-ref sweep
For each **other** vault with live breaking refs: `git status` (dirty → skip + flag in the deferral ledger);
else scoped sed of live pointers only, **per-vault surgical commit** (never `git add -A` a vault you don't own).
Historical stays verbatim; derived + stale-list refs defer.

### Step 8: Wrapper refederation (re-verify the census LIVE)
For each consumer `<old>/` wrapper: `mv <old>/ <new>/`; repoint `federation_ref` (`source_vault`/`source_path`);
re-pin if pinned; per-vault commit; **prove federation resolves** through the symlink. **Re-glob the live
`<old>/` dirs at execution — manifests undercount wrappers by ~3×** (application-named + node-side wrappers hide).

### Step 9: Close
Update the node `inventory_vaults` + the shim ledger; the docs registry / ecosystem spec (coord memo if
cross-vault). Re-grep the old name → confirm **zero LIVE refs** (historical mentions remain — correct); record
the count. Commit local, **do not push** — the graph rename ≠ the GitHub remote-repo rename (a separate
downstream step); the local commit sitting ahead of the still-old-named remote is expected. File the 5-line AAR.

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Renamed vault + shim | move + symlink | `<new>.aDNA` with a registered `<old> → <new>` back-compat shim |
| Swept own surfaces | edits | The vault's own live routing flipped (via `skill_project_rename`); historical verbatim |
| Renamed code layer | edits | Package/identifiers flipped under a green test gate (separate commit); graduation → accept-both |
| Cross-fleet repoints | edits | Every live inbound pointer + consumer wrapper resolves to `<new>` |
| Zero-live re-grep | verification | Only historical mentions of `<old>` remain; count recorded; shim retires later at its window |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Dozens of hits, most legitimate | Historical provenance counted as live | Expected — classify (Step 1); the true live set is small (~10% of raw); trust the classifier |
| Prose corrupted by the sweep | New name is a common word, blanket replace | Two-pass qualified-token recipe (flip to `<New>.aDNA`, never the bare word) + post-sweep re-grep |
| Imports/lattice resolution break | Code layer renamed without the full sweep or no test gate | The test gate is the spine — green-before/green-after; sweep bare `X.attr` + quoted strings + pyproject, not just imports |
| A "rename" won't stay backward-compatible | It reached a schema `const` / field / contract — it's a **graduation** | Surface scope to the operator; apply accept-both + a deprecation-window alias; verify old+new+missing before commit |
| Wrapper count wrong at retire time | Trusted the manifest census | Re-glob the live `<old>/` dirs at execution — manifests undercount ~3× |
| Owning code repo is dirty / mid-archive | Tried to rename the code layer in the same leg | Defer the whole code layer (two-layer split) with its target name locked in the ADR + deferral ledger |

## Related
- [[how/skills/skill_project_rename|skill_project_rename.md]] — the delegated self-routing sweep + keep/strip classifier (Step 4)
- [[how/skills/skill_graph_merge|skill_graph_merge.md]] — the sibling; a merge archives (no live symlink), a rename keeps one
- [[how/skills/skill_project_fork|skill_project_fork.md]] — vault birth (renames the identity a fork established)
- [[how/skills/skill_workspace_spring_clean|skill_workspace_spring_clean.md]] — gathers renames behind one operator gate
- ADR-042 (fork-template hygiene + rename protocol) — Standard §6.5, the rename protocol this satisfies
- **Skills Protocol**: `how/skills/AGENTS.md`

## Provenance

Codified from a rename/ref-sweep playbook that converged across a seven-rename cascade + a doctrine relocation
on the reference node (2026-06 cohort), reusing the sweep machinery a graph merge also inherits. The proven
findings it carries: difficulty scales with name-collision + genesis-density + code-coupling (never ref count —
the cohort's highest-count rename was among the easiest); the test gate is the spine for any code-coupled
rename; and a "rename" that reaches a schema `const` or federation contract is a **graduation**, mission-sized,
whose scope must be surfaced to the operator before executing. *(Historical origin note — the recipe is
node-agnostic.)*
