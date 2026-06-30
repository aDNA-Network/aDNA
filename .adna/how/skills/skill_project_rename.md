---
type: skill
skill_type: agent
created: 2026-06-29
updated: 2026-06-29
status: active
category: vault_maintenance
trigger: "A vault / project / persona is being renamed (or a fleet rename touched this vault) — sweep its own live-routing self-references to the old name at rename-time (Standard §6.5)"
last_edited_by: agent_stanley
tags: [skill, rename, self_routing, obe_residue, keep_strip_classifier, drydock, adr_042]

requirements:
  tools: [grep/rg, git]
  context:
    - what/docs/adna_standard.md  # §6.5 Rename Protocol
    - what/decisions/adr_042_fork_template_hygiene_and_rename_protocol.md
  permissions:
    - path-scoped edits to the renamed vault's own governance files
---

# Skill: Project Rename (self-routing sweep)

## Overview

When a vault, project, or persona is renamed, this skill sweeps the vault's **own live-routing governance files** (`CLAUDE.md`, `STATE.md`, `AGENTS.md`) of self-references to the **old** name — closing the out-by-event (OBE) rename-residue class (Standard §6.5; ADR-042). It is the rename-time companion to [[how/skills/skill_project_fork|skill_project_fork.md]] (sibling structure) and is distinct from [[how/skills/skill_workspace_path_migration|skill_workspace_path_migration.md]] (which *moves* a vault between directories rather than renaming its identity).

**The load-bearing rule** is scope discipline: the sweep touches the **live-routing self-reference subset ONLY**. A naive whole-vault grep over-counts the defect by an order of magnitude — most hits are legitimate historical cross-references that MUST be retained (archive-don't-delete, §15). This skill's value is the **keep/strip classifier** (Step 4) that separates the two.

## Trigger

Invoke as a **mandatory step of any rename** (Standard §6.5 makes the rename-time sweep a MUST), or retroactively when OBE residue is discovered in a vault that was renamed without a sweep. Renames include vault renames (e.g. `Cmux → Terminal`), persona renames (e.g. `Hermes → Mondrian`), and the harder supersession renames (e.g. `LatticeAgent → Harness`, `LatticeTerminal → Terminal`).

Do **NOT** invoke for a directory move with no identity change (that is `skill_workspace_path_migration`), nor to bulk-rewrite history (that violates §15).

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `old_name` | Yes | The prior identity token(s) — vault name and/or persona being retired (e.g. `Cmux`, `SpeechForge`, `Hermes`). Accepts several when a rename cascades (e.g. `LatticeHome → Home` + `LatticeNetwork → Network`). |
| `new_name` | Yes | The current identity token(s) the routing should reflect. |
| `vault_root` | Yes | The renamed vault's root directory. |
| `dry_run` | No (default true) | Report the classified keep/strip set without editing. Operator confirms before strips land. |

## Implementation

### Step 1: Collect rename identity
Record each `old_name → new_name` pair (vault and/or persona). A supersession rename usually carries two or more pairs; collect them all.

### Step 2: Scoped grep (governance files only)
Restrict the search to the vault's **own** live-routing governance files — never the whole tree:

```bash
grep -rnE "<old_name>" "$vault_root" \
  --include='CLAUDE.md' --include='STATE.md' --include='AGENTS.md'
```

This already excludes session history, ADR files, backlog, and content — the bulk of legitimate historical refs live outside the three governance file types. (Nested `CLAUDE.md`/`AGENTS.md` inside campaigns/topics ARE in scope — they route too.)

### Step 3: Read each hit in context
Read the full line (and surrounding sentence) for every hit. Classification is a per-line judgment, never a blind `sed`.

### Step 4: Keep/Strip classifier (the load-bearing step)

For each hit, decide **STRIP** vs **KEEP**:

| Verdict | The reference is… | Examples |
|---------|-------------------|----------|
| **STRIP** | The vault naming **itself, in a current/routing sense**, using the old name with no historical framing | persona/identity line ("You are <persona>, governing `OldName.aDNA`"); present-tense path routing ("state lives in `OldName.aDNA/STATE.md`"); a header/frontmatter presenting the old name as the current identity |
| **KEEP** | A **historical** statement, provenance, or a reference to **another** entity | "Renamed from `OldName` 2026-06-15 (shim active)"; "was `OldName.aDNA`"; dated changelog/AAR entries; ADR/session lineage; a cross-ref to a *different* vault that legitimately still bears a name; a back-compat shim declaration |

**Tells.** A line is almost always **KEEP** if it carries a provenance marker — `renamed from` · `was` · `formerly` · `→` · `supersed*` · `shim` · `archive` · a date · `PT pt##`. A line is **STRIP** if it self-identifies in the present tense with the old name and no such marker. When genuinely ambiguous, **KEEP and flag** (a retained historical ref is harmless; a wrongly-stripped one destroys provenance, §15).

> ⚠️ **Over-count trap (recorded).** Raw grep counts at Drydock M00 were MoleculeForge 28 · ComfyForge 28 · SpeechForge 20 · VAASLattice 11 · TappInterface 4 — but most were legitimate SO-7 provenance prose. The true-defect subset is the STRIP rows only. Report both numbers (raw hits vs. classified-strip) so the denominator is honest.

### Step 5: Apply strips (path-scoped) and re-measure
On operator confirmation (after the dry-run), edit only the STRIP lines, replacing `old_name → new_name` in the live-routing context (path-scoped `git add` of the vault's own governance files only — never `-A`). Re-grep; the residual should equal the KEEP set exactly. Update `last_edited_by`/`updated` on each touched file.

### Step 6: Record
Note the rename + the classified counts (raw vs. strip) in the vault's `STATE.md` and, for a tracked cleanup, the originating mission/idea. If invoked **at rename-time**, this skill's run is part of the rename's own session record.

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Classified keep/strip set | report | Per-line verdict with raw-vs-strip counts (honest denominator) |
| Swept governance files | files | STRIP lines updated `old → new`; KEEP lines untouched |
| Residual = KEEP set | verification | Re-grep confirms only historical refs remain |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Raw grep returns dozens of hits | Historical provenance prose counted | Expected — run the Step-4 classifier; do not bulk-replace |
| A shim/back-compat declaration matched | Legitimate routing for the OLD path | KEEP — the shim must keep naming the old path to resolve |
| Ambiguous self-vs-historical line | Mixed prose | KEEP and flag for the operator; never strip on uncertainty (§15) |
| Old name appears in another vault's files | Cross-reference, not self-routing | Out of scope — this skill sweeps the renamed vault's OWN files only; cross-vault refs route via coordination (Rule 10) |

## Related
- [[what/docs/adna_standard|adna_standard.md §6.5]] — Rename Protocol (the normative requirement this skill satisfies)
- [[what/decisions/adr_042_fork_template_hygiene_and_rename_protocol|ADR-042]] — the decision that established §6.5 + this recipe
- [[how/skills/skill_project_fork|skill_project_fork.md]] — sibling (creates a vault; this one renames one)
- [[how/skills/skill_workspace_path_migration|skill_workspace_path_migration.md]] — moves a vault between directories (no identity change)
