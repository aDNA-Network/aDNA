---
type: skill
skill_type: agent
created: 2026-05-11
updated: 2026-05-14
status: active
category: node_operations
trigger: "Rebuild `inventory_vaults.{md,yaml}` + `inventory_system.{md,yaml}` from current node state. Detect new vaults at `~/aDNA/*.aDNA/` (or grandfathered named projects); detect removed vaults (was-listed-now-missing); detect version drift (semver bump in target vault's CHANGELOG.md vs inventory-recorded version). Updates `STATE.md` `last_full_health_check` timestamp."
last_edited_by: agent_stanley
graduated_from: LatticeHome.aDNA@411660e  # v0.1 initial bootstrap, M04 S2 of campaign_adna_v2_infrastructure
graduated_at: 2026-05-14
graduated_via: campaign_federation_beta_planning M-H.1.5
tags: [skill, node_adna, inventory_refresh, graduated]

requirements:
  tools: [ls, find, git, python3, yq-or-python-yaml]
  context: [what/inventory/*]
  permissions: [read ~/aDNA/ listing, read each vault's CHANGELOG.md + CLAUDE.md frontmatter, write what/inventory/*]
---

# Skill: Inventory Refresh

## Overview

Rebuilds `what/inventory/inventory_vaults.{md,yaml}` and `what/inventory/inventory_system.{md,yaml}` from current node state. Surfaces:

- **New vaults**: present on disk, not in inventory
- **Removed vaults**: in inventory, not on disk (or moved)
- **Version drift**: a vault's `CHANGELOG.md` shows a newer version than the inventory recorded
- **Tool-chain drift**: a recorded tool version differs from current

Writes both MD and YAML atomically. Both formats are kept in sync — never write one without the other.

## Trigger

Invoked when:

- Operator asks: "Refresh the inventory" or "What's new on this node?"
- After installing a new `.aDNA` vault (`skill_project_fork`)
- After upgrading toolchain (Homebrew bump, node/python upgrade)
- Quarterly review
- When `skill_node_health_check` reports drift in inventory-vs-disk

## Parameters

| Parameter | Source | Required |
|---|---|---|
| `target` | CLI arg | No (default: `all` — can limit to `vaults`, `system`, or `memberships`) |
| `interactive` | CLI flag | No (default: false — when true, prompts for new-vault classifications) |

## Requirements

### Tools/APIs

- `ls`, `find` to enumerate `~/aDNA/`
- `git` for HEAD info on each vault
- `python3` + `yaml` to read/write YAML files
- Tool-version commands: `git --version`, `node --version`, `python3 --version`, `uv --version`, `brew --version`, `gh --version`, `rg --version`, `zsh --version`
- `uname -a`, `sw_vers`, `hostname`, `whoami` for machine info

### Context Files

- Current `what/inventory/*.md` + `*.yaml` (for diff)
- Each vault's `CHANGELOG.md` + `CLAUDE.md` frontmatter (for version detection)

### Permissions

- Read `~/aDNA/` listing + each vault's top-level files
- Write `what/inventory/*` (both MD + YAML atomically)

## Implementation

### Step 1: Enumerate Workspace Directories

```bash
ls -d ~/aDNA/*/ | xargs -I{} basename {} | sort > /tmp/disk_list.txt
```

Filter:
- `.aDNA/` suffix → vault candidates
- Workspace-router-named projects → grandfathered candidates
- Everything else → "other" (runtime/work/external — not tracked in inventory_vaults)

### Step 2: Load Current Inventory

Parse current `inventory_vaults.yaml` `vaults:` + `named_projects:` lists into a dict keyed by name.

### Step 3: Compute Diff

For each disk entry:
- In inventory + on disk → `UNCHANGED` (refresh `last_sync` if relevant)
- On disk, NOT in inventory → `NEW` (queue for addition)
- In inventory, NOT on disk → `REMOVED` (queue for removal)

### Step 4: Classify New Vaults (interactive or heuristic)

For each `NEW` entry:

- Check `<path>/MANIFEST.md` frontmatter for `type: manifest`, look for category hints
- Check `<path>/CLAUDE.md` for persona declaration
- Check `<path>/what/decisions/adr_000_project_identity.md` if exists (Platform.aDNA / Framework.aDNA / Org-Vault.aDNA / Org-Graph.aDNA pattern)

Default classification: `unclassified` (operator can refine via `interactive: true` or manual edit).

### Step 5: Detect Version Drift

For each unchanged vault, read `<path>/CHANGELOG.md` head — extract the most recent version (e.g., `## [v1.2] — 2026-05-04`). Compare with inventory-recorded `version` field. If different → flag as `VERSION_DRIFT`.

### Step 6: Refresh Tool Versions

Run each tool-version command. Compare with `inventory_system.yaml` `tools:` block. Update if different.

### Step 7: Refresh Machine Info

Re-derive: `hostname`, `os_version`, `os_build`, `kernel`, `arch`, `workspace_root`. Compare with `inventory_system.yaml` `machine:` block. Update if different.

### Step 8: Write Inventory Files Atomically

For each of `inventory_vaults.{md,yaml}`, `inventory_system.{md,yaml}`:

1. Compute new MD content (humans read this)
2. Compute new YAML content (agents query this)
3. Update `updated:` field to today's date in both
4. Write `.yaml` first, then `.md` (so if one fails, the YAML is the canonical truth)
5. Commit both together

### Step 9: Update STATE.md

Update `STATE.md` frontmatter:

```yaml
last_full_health_check: <timestamp>
vault_count: <N>
healthy_count: <pending until skill_node_health_check runs>
drift_count: <D — count of DRIFT entries>
blocked_count: 0
```

### Step 10: Emit SITREP

```
=== Inventory Refresh — SITREP ===
<timestamp>

Vault changes:
- N new vaults detected: <names>
- R removed vaults: <names>
- V version drift: <name (recorded → current)>
- U unchanged: <count>

Tool-chain changes:
- T tool versions updated: <tool (old → new)>

Files written:
- what/inventory/inventory_vaults.md + .yaml
- what/inventory/inventory_system.md + .yaml
- STATE.md (last_full_health_check + counts)
```

## Output

| Output | Type | Description |
|---|---|---|
| `inventory_vaults.md` + `.yaml` | File | Refreshed vault inventory |
| `inventory_system.md` + `.yaml` | File | Refreshed system inventory |
| `STATE.md` | File | Updated `last_full_health_check` + counts |
| SITREP | stdout | Human-readable diff summary |

## Error Handling

| Error | Cause | Resolution |
|---|---|---|
| Read fail on `<path>/CHANGELOG.md` | Vault lacks CHANGELOG | Skip version check; flag as `NO_CHANGELOG` in drift list |
| YAML parse fail on current inventory | Corrupted prior state | Backup current files; rewrite from disk truth; flag for operator review |
| Tool-version command fails | Tool not installed | Record `not_installed` in inventory_system; do not fail the skill |
| New vault with no CLAUDE.md | Likely incomplete fork | Flag as `INCOMPLETE_BOOTSTRAP`; operator decides whether to include |

## Related

- `how/skills/skill_node_health_check.md` — validates inventory-vs-disk consistency (call this after refresh)
- `how/skills/skill_update_all_vaults.md` — `git pull` across vaults (refresh AFTER to pick up new content)
- `how/skills/skill_node_credentials_audit.md` — separate credentials enumeration (NAMES ONLY)
- `what/inventory/AGENTS.md` — refresh discipline
