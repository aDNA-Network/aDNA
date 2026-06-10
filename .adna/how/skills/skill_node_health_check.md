---
type: skill
skill_type: agent
created: 2026-05-11
updated: 2026-05-14
status: active
category: node_operations
trigger: "Validate LatticeHome.aDNA vault state — file presence, frontmatter validity, inventory-vs-disk consistency, federation block validity, freshness. Run as the D10 reproducibility gate (post-bootstrap; pre-AAR; periodically)."
last_edited_by: agent_stanley
graduated_from: LatticeHome.aDNA@411660e  # v0.1 initial bootstrap, M04 S2 of campaign_adna_v2_infrastructure
graduated_at: 2026-05-14
graduated_via: campaign_federation_beta_planning M-H.1.5
tags: [skill, node_adna, health_check, d10, reproducibility_gate, graduated]

requirements:
  tools: [grep, ls, find, python3, yq-or-python-yaml]
  context: [CLAUDE.md, MANIFEST.md, STATE.md, inventory/*, identity/*]
  permissions: [read all LatticeHome.aDNA files, read ~/aDNA/ directory listing]
---

# Skill: Node Health Check

## Overview

The **D10 reproducibility gate** for `LatticeHome.aDNA/`. Validates the vault is internally consistent and aligned with ground truth (disk + tool-chain). Reports drift in SITREP form. Exit code 0 = healthy; >0 = drift detected.

Designed to run in <30 seconds so it can be invoked frequently (post-bootstrap, pre-AAR, periodically, on session start when stale-state suspected).

## Trigger

Invoked when:

- M04 Session 2 closes (verify the just-bootstrapped vault)
- M04 Session 3 runs the 10-dim compliance audit (D10 dimension)
- An operator asks: "Run the health check"
- A cross-vault session needs to confirm node state before acting
- `STATE.md`'s `last_full_health_check` is more than 7 days old

## Parameters

| Parameter | Source | Required |
|---|---|---|
| `verbose` | CLI flag | No (default: false) |
| `update_state` | CLI flag | No (default: true — writes `last_full_health_check` timestamp to STATE.md on success) |

## Requirements

### Tools/APIs

- `ls`, `find` for filesystem checks
- `grep` for frontmatter scanning
- `python3` + `yaml` module for YAML companion validation
- Read access to `LatticeHome.aDNA/` and `~/aDNA/` (for inventory-vs-disk reconciliation)

### Context Files

- `CLAUDE.md`, `MANIFEST.md`, `STATE.md` — top-level governance
- `what/inventory/*.md`, `what/inventory/*.yaml`
- `who/identity/*.md`, `who/identity/*.yaml`
- `how/skills/skill_node_*.md` (verifies the 4 node-skills are present)

### Permissions

- Read all `LatticeHome.aDNA/` files
- Read `~/aDNA/` directory listing (to reconcile against `inventory_vaults.md`)
- Write to `LatticeHome.aDNA/STATE.md` if `update_state: true`

## Implementation

### Step 1: Top-Level File Presence

Required files (exit 1 if any missing):
- `CLAUDE.md`
- `AGENTS.md`
- `MANIFEST.md`
- `STATE.md`
- `README.md`
- `CHANGELOG.md`

### Step 2: Scaffold Directory Presence

Required directories with required AGENTS.md (exit 2 if any missing):
- `what/inventory/AGENTS.md`
- `who/identity/AGENTS.md`
- `what/decisions/AGENTS.md`
- `who/coordination/AGENTS.md`
- `how/skills/AGENTS.md` (inherited)

### Step 3: Inventory Scaffolds Presence

Required files (exit 3 if any missing):
- `what/inventory/inventory_vaults.md` + `.yaml`
- `what/inventory/inventory_system.md` + `.yaml`
- `what/inventory/inventory_memberships.md` + `.yaml`

### Step 4: Identity Scaffolds Presence

Required files (exit 4 if any missing):
- `who/identity/identity_node.md` + `.yaml`
- `who/identity/identity_lattice_protocol.md` + `.yaml`

### Step 5: 4 Node-Skills Presence

Required files (exit 5 if any missing):
- `how/skills/skill_node_health_check.md` (this file)
- `how/skills/skill_update_all_vaults.md`
- `how/skills/skill_inventory_refresh.md`
- `how/skills/skill_node_credentials_audit.md`

### Step 6: Frontmatter Validity (yaml.safe_load)

For every `.md` file in `LatticeHome.aDNA/` (recursively), parse the YAML frontmatter (between `---` markers). Fail (exit 6) if:

- YAML doesn't parse
- Missing required fields: `type`, `created`, `updated`, `last_edited_by`
- `last_edited_by: agent_init` (would indicate the file is in template state, NOT customized — operator persona should never see this in a customized vault)

### Step 7: YAML Companion Schema Validity

For every `.yaml` companion file in `what/inventory/` and `who/identity/`, parse with `yaml.safe_load`. Fail (exit 7) if:

- YAML doesn't parse
- `type` field doesn't match the corresponding MD file's `type`
- Required schema fields missing (see entity-type AGENTS.md for required fields)

### Step 8: Federation Block Validity

`what/inventory/inventory_memberships.yaml` must contain a `federation:` block with all 8 keys: `shareable`, `discoverable`, `source_instance`, `version_policy`, `share_policy`, `license`, `creators`, `keywords`. Fail (exit 8) if any are missing.

### Step 9: Inventory-vs-Disk Consistency

For each vault in `inventory_vaults.yaml` `vaults:` list, verify the path exists at `~/aDNA/<name>/`. Report DRIFT (warning, not failure) if:

- A listed vault is missing on disk
- A `.aDNA/` directory exists on disk but is NOT in the inventory

Drift is logged in the report; exit code 9 ONLY if a vault is listed-and-missing (the inventory is incorrect about ground truth). Disk-extras-not-in-inventory are warnings (exit 0) because they may be in-progress new vaults.

### Step 10: Last-Update Freshness

For each `inventory_*.md` file, check the `updated` frontmatter field. If older than 7 days, log a warning (exit 0 still).

### Step 11: Identity Drift Check

Read `who/identity/identity_node.md`. Compare hostname, operator against current node state (`hostname`, `whoami`). If mismatch, fail (exit 11) — node identity drift is high-severity per `who/identity/AGENTS.md`.

### Step 12: Optional STATE.md Update

If `update_state: true` and all prior steps passed (exit 0), update `STATE.md` frontmatter:

```yaml
last_full_health_check: <iso-timestamp>
healthy_count: <count of vaults with health=pending|healthy>
drift_count: <count of vaults with health=drift>
blocked_count: 0
```

## Output

### On success (exit 0)

```
=== LatticeHome.aDNA health check ===
✓ Top-level files: 6/6
✓ Scaffold directories: 5/5
✓ Inventory scaffolds: 6/6 (3 MD + 3 YAML)
✓ Identity scaffolds: 4/4 (2 MD + 2 YAML)
✓ Node-skills: 4/4
✓ Frontmatter valid: N files
✓ YAML companions valid: 5 files
✓ Federation block valid (8 keys)
✓ Inventory-vs-disk: M vaults listed; M on disk (D drift warnings)
✓ Last-update freshness: all <7 days
✓ Identity drift: hostname=<host> matches; operator=<operator> matches

Healthy. Last full health check: <iso-timestamp>.
Exit 0.
```

### On failure (exit >0)

```
=== LatticeHome.aDNA health check FAILED ===
✗ Step <N>: <description of failure>
<details>

Exit <N>.
```

## Error Handling

| Exit Code | Cause | Resolution |
|---|---|---|
| 0 | Healthy | No action |
| 1 | Top-level file missing | Restore from git history or re-bootstrap from template per `skill_project_fork` |
| 2-5 | Scaffold/skill missing | Re-run M04 Session 2 bootstrap (or just re-create the missing file) |
| 6 | Frontmatter invalid | Inspect the failing file; fix YAML; re-run check |
| 7 | YAML companion schema invalid | Run `skill_inventory_refresh` to regenerate |
| 8 | Federation block missing keys | Restore `inventory_memberships.yaml` from git |
| 9 | Vault listed-and-missing | Either restore the vault or run `skill_inventory_refresh` to remove from inventory |
| 11 | Identity drift | `#needs-human` — verify hostname/operator change is intentional |

## Related

- `how/skills/skill_inventory_refresh.md` — regenerates inventory from current state (use when check reports drift)
- `how/skills/skill_update_all_vaults.md` — `git pull` across listed vaults
- `who/identity/AGENTS.md` — identity drift discipline
- `what/inventory/AGENTS.md` — inventory refresh discipline
- `aDNA.aDNA/CLAUDE.md` § Compliance Dimensions — D10 rubric definition
