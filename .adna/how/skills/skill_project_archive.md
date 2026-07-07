---
type: skill
skill_type: agent
created: 2026-07-06
updated: 2026-07-06
status: active
category: vault_maintenance
trigger: "A vault/project is superseded, wound down, or merged away — archive it intact under the Archive holder (archive-never-delete, SO-6/7) instead of deleting it"
last_edited_by: agent_rosetta
tags: [skill, archive, supersession, wind_down, shim, registry_drop, so7, lifecycle]

requirements:
  tools: [git, grep/rg]
  context:
    - CLAUDE.md            # the workspace router (the row that moves)
    - what/docs/adna_standard.md  # SO-6/7 archive-never-delete
  permissions:
    - move the retired vault under the Archive holder (git mv / same-device mv)
    - path-scoped edits to the workspace router row + node inventory + the retired vault's own banner
    - register a back-compat shim in the node shim ledger
---

# Skill: Project Archive (retire a vault, never delete it)

## Overview

The standard has [[how/skills/skill_project_fork|skill_project_fork.md]] for vault **birth** — this skill is
its mirror, vault **retirement**. When a `<Name>.aDNA` graph is superseded, wound down, or drained by a merge,
it does not get deleted (**Standing Order 6/7: archive, never delete** — the audit trail is permanent). It
moves intact under the **Archive holder** with a supersession banner, its router row and registry entry are
retired, a back-compat shim preserves old paths, and any salvage happens through a quarry pointer — never by
re-editing the archive.

**Plain version:** deleting a project loses its history and silently breaks everything that pointed at it.
This skill retires a project the safe way — it gets moved to an "archive shelf," clearly labelled with why
and where its work continued, with a forwarding address left behind so old links still resolve.

**The load-bearing discipline** is *repoint-before-you-retire*: an archived vault must have every **live**
inbound reference repointed to its successor **first**; the back-compat shim is an audit-convenience for
stragglers, not a substitute for repointing. Skip that and the archive becomes a set of dangling links.

## Trigger

Invoke when a vault reaches one of three **retirement modes**:

| Mode | Meaning | Typical predecessor step |
|------|---------|--------------------------|
| **superseded** | A successor vault now carries this vault's role | an ADR/mission that names the successor |
| **wound down** | The effort halts and will not resume; assets preserved as a quarry | a wind-down decision |
| **merged away** | Content was folded into another vault; the drained shell is archived | [[how/skills/skill_graph_merge\|skill_graph_merge.md]] |

Do **NOT** invoke:
- For a **rename** (the vault lives on under a new name) → [[how/skills/skill_graph_rename|skill_graph_rename.md]].
- For a **directory move with no retirement** (relocating an active vault) → `skill_workspace_path_migration`.
- To delete anything. This skill has no delete step; that is the point.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `vault_name` | string | Yes | — | The retiring vault, e.g. `OldVault.aDNA` |
| `retirement_reason` | enum | Yes | — | `superseded` \| `wound_down` \| `merged` |
| `successor_or_quarry` | string | Yes | — | Where the role/content continued (successor vault) or where salvage is indexed (quarry) — goes in the banner |
| `holder` | string | No | `Archive.aDNA/` | The Archive holder directory at the workspace root |
| `dry_run` | bool | No | `true` | Produce the inbound-ref sweep + the planned moves without touching disk; operator confirms before the move lands |

## Requirements

### Tools/APIs
- `git` (history-preserving `git mv`; a same-device `mv` for locked/large data trees), `grep`/`rg` (inbound-ref sweep).

### Context Files
- The workspace router `CLAUDE.md` (the row that moves) and the node inventory (the registry row that drops).

### Permissions
- Move the vault under the holder; path-scoped edits to the router row, node inventory, and the retired
  vault's own `CLAUDE.md`/`STATE.md` banner; register the shim in the node ledger.

## Implementation

### Step 1: Pre-check (hard gate)
Confirm the retirement is decided (an accepted ADR / mission close / operator directive names the reason and
successor). Confirm the vault's working tree is clean and it is **not** mid-campaign or holding a
merge-**source** role. A retirement is a governance event — nothing archives from open WIP.

### Step 2: Inbound-reference sweep (repoint-before-retire)
Grep the workspace for **live** inbound references to `vault_name` — the router row, node
inventory/curation/render artifacts, consumer `federation_ref` wrappers, and peer coordination memos:

```bash
grep -rnE "<vault_name>" ~/<workspace_root> \
  --include='CLAUDE.md' --include='STATE.md' --include='AGENTS.md' --include='*.yaml' --include='*.md' \
  | grep -v '/_archive/' | grep -v '/sessions/history/'
```

Classify each hit **live-routing** (must repoint to `successor_or_quarry` first) vs **historical provenance**
(KEEP — dated prose, changelogs, lineage). Repoint the live set **before** the move. (Same keep/strip
discipline as [[how/skills/skill_project_rename|skill_project_rename.md]] Step 4.) In `dry_run`, stop here and
report the classified set.

### Step 3: Banner the retiring vault
Prepend a **supersession / wind-down banner** to the vault's own `CLAUDE.md` and `STATE.md`, and set
frontmatter `status: archived`:

> **⚠️ ARCHIVED `<date>` — <reason>.** Role/content continued at `<successor_or_quarry>`. This vault is
> **immutable** — read for audit only; do not edit. Salvage via the quarry index, never by editing here.

### Step 4: Move under the holder (history-preserving)
Move the vault intact into the holder, preserving its internal structure and in-vault `.git`:

```bash
git mv <vault_name> <holder><vault_name>     # or: same-device `mv` when a locked/large data tree forbids git mv
```

Commit inside the archived vault's own repo where one exists. The holder (`Archive.aDNA/`) is **not itself a
vault** (no governance of its own) — it is a shelf.

### Step 5: Register the back-compat shim
Create a root symlink `~/<workspace_root>/<vault_name> → <holder><vault_name>` and **register it at creation**
in the node shim ledger with **class · window · retire-condition · owner** (see the shim-window discipline,
Standing Rule 9 / `idea_upstream_shim_window_discipline`). The shim resolves top-level paths for stragglers;
it never substitutes for the Step-2 repoints.

### Step 6: Move the router row
In the workspace router `CLAUDE.md`, move the vault's row to its archived form (or fold it under the Archive
holder row): routing identity only, with the **archive date + successor pointer + a note that the shim is
active**. Keep it to ~1 line (router row discipline).

### Step 7: Drop the registry entry
Remove the vault's node-inventory row (leave a dated drop-comment in place). Derived render artifacts (curation
cards, canvas node, HOME index) regenerate without it and `vault_count` recomputes. Render-asset *images* may
be retained (they are assets, not registry pointers).

### Step 8: Quarry pointer (if salvage will happen)
If a consumer will scavenge the archive, add an explicit **quarry index** in the *consumer* vault
(`<Consumer>.aDNA/what/intake/<source>_salvage_<date>/quarry_index.md`) that points into the archive. Salvage
reads the archive; it never re-edits it.

### Step 9: Batch the fleet-delta regen
Do **one** coordinated inventory / curation / canvas regen for the drop — never regenerate per-event. If
several vaults retire together, batch them (this is where [[how/skills/skill_workspace_spring_clean|skill_workspace_spring_clean.md]]
gathers many archive events behind one gate).

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Archived vault | move | `<holder><vault_name>/` intact, banner applied, `status: archived`, `.git` preserved |
| Repointed live refs | edits | Every live inbound reference now points at `successor_or_quarry` |
| Registered shim | ledger + symlink | Root back-compat symlink + a node-ledger row (class/window/retire/owner) |
| Retired router row + dropped registry entry | edits | Router row moved to archived form; inventory row dropped; `vault_count` −1 |
| Quarry index (optional) | file | In the consumer, when salvage is planned |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Live inbound refs remain after the move | Step 2 skipped or incomplete | The archive now has dangling links — repoint the live set (Step 2) and re-sweep to zero before continuing |
| `git mv` fails on a large/locked data tree | Submodule, external mount, or huge blob | Use a same-device `mv` (preserves inode) and commit the pointer change; note the exception in the ledger |
| Name collision in the holder | A vault of that name was archived before (e.g. second-genesis re-fork of the same name) | Disambiguate the archived copy (e.g. `<Name>Old.aDNA`) and record both in the ledger |
| Shim never retires | Registered without a retire-condition | A shim needs window + retire-condition + owner at creation (Standing Rule 9); a lapsed window alone never auto-retires — retire only on verified ref-sweep-zero + owner-ack |
| Render artifacts still show the vault | Regen not run | Run the batched fleet-delta regen (Step 9) |

## Related
- [[how/skills/skill_project_fork|skill_project_fork.md]] — vault birth (this skill is its death mirror)
- [[how/skills/skill_graph_merge|skill_graph_merge.md]] — a merge ends by archiving the drained source here
- [[how/skills/skill_second_genesis|skill_second_genesis.md]] — P1 archives the old graph via this skill (archive-old-first)
- [[how/skills/skill_workspace_spring_clean|skill_workspace_spring_clean.md]] — orchestrates many archive events behind one operator gate
- [[how/skills/skill_project_rename|skill_project_rename.md]] — the keep/strip classifier reused in Step 2
- **Skills Protocol**: `how/skills/AGENTS.md`

## Provenance

Codified from a stable convention that converged across five archive events on the reference node
(2026-06 cohort) and was filed upstream as `idea_upstream_skill_project_archive`; the Archive-holder + shim
registry disciplines are Standing Rules established there. *(Historical origin note — the recipe itself is
node-agnostic.)*
