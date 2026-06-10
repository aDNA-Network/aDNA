---
type: skill
skill_type: agent
created: 2026-05-11
updated: 2026-05-14
status: active
category: node_operations
trigger: "Run `git pull --ff-only` across every vault listed in `inventory_vaults.md`. Per-vault outcome: pulled-clean / already-up-to-date / merge-conflict / network-error / not-a-git-repo. Does NOT auto-resolve conflicts (flags `#needs-human`)."
last_edited_by: agent_stanley
graduated_from: LatticeHome.aDNA@411660e  # v0.1 initial bootstrap, M04 S2 of campaign_adna_v2_infrastructure
graduated_at: 2026-05-14
graduated_via: campaign_federation_beta_planning M-H.1.5
tags: [skill, node_adna, vault_update, git_pull, graduated]

requirements:
  tools: [git, yq-or-python-yaml]
  context: [what/inventory/inventory_vaults.yaml]
  permissions: [read inventory_vaults.yaml, run git commands in each listed vault]
---

# Skill: Update All Vaults

## Overview

Runs `git pull --ff-only` across every vault listed in `what/inventory/inventory_vaults.yaml`. Reports a per-vault outcome table. Does NOT auto-resolve merge conflicts — surfaces them as `#needs-human` so the operator can decide.

Safe-by-default: uses `--ff-only` (fails on non-fast-forward); skips vaults with no remote configured (local-by-default vaults like `LatticeHome.aDNA/` itself).

## Trigger

Invoked when:

- Operator asks: "Update all my vaults" or "Run a git pull across everything"
- A cross-vault session detects stale state in multiple vaults
- Scheduled maintenance (weekly recommended)
- After a known upstream release affecting multiple vaults

## Parameters

| Parameter | Source | Required |
|---|---|---|
| `dry_run` | CLI flag | No (default: false — when true, reports what would be pulled without doing it) |
| `filter` | CLI arg | No (default: all — can limit to a subset, e.g., `--filter .aDNA` or `--filter forge`) |
| `skip_local` | CLI flag | No (default: true — skips vaults with no remote like `LatticeHome.aDNA/` itself) |

## Requirements

### Tools/APIs

- `git` — for `git pull` + `git remote` queries
- `python3` with `yaml` module (or `yq`) — to parse `inventory_vaults.yaml`

### Context Files

- `what/inventory/inventory_vaults.yaml` — source of truth for the vault list

### Permissions

- Read `inventory_vaults.yaml`
- Run `git pull` in each listed vault (operator's git credentials)
- No write access to vault content (git handles that)

## Implementation

### Step 1: Load Inventory

Parse `what/inventory/inventory_vaults.yaml` to get the full list. Combine `vaults:` + `named_projects:` (skip `drift:` entries).

### Step 2: For Each Vault, Detect Git State

For each vault path:

1. Does the path exist? (if not: outcome = `MISSING`)
2. Is it a git repo? (`test -d <path>/.git` or `git -C <path> rev-parse --git-dir`)
   - If no: outcome = `NOT_A_GIT_REPO`
3. Does it have a remote configured? (`git -C <path> remote`)
   - If no AND `skip_local: true`: outcome = `SKIPPED_LOCAL_ONLY` (e.g., this vault itself)
   - If no AND `skip_local: false`: outcome = `NO_REMOTE` (flag)

### Step 3: Run Git Pull

For each git-repo-with-remote vault:

```bash
git -C <path> pull --ff-only
```

Capture outcome:

- Exit 0 + "Already up to date" → outcome = `UP_TO_DATE`
- Exit 0 + content pulled → outcome = `PULLED_CLEAN` (capture commits-pulled-count)
- Exit ≠0 + "fatal: Not possible to fast-forward" → outcome = `NON_FAST_FORWARD` (flag `#needs-human`)
- Exit ≠0 + network error (timeout / DNS / refused) → outcome = `NETWORK_ERROR`
- Exit ≠0 + auth error → outcome = `AUTH_FAILED` (flag `#needs-human`)
- Exit ≠0 + other → outcome = `OTHER_ERROR`

### Step 4: Emit SITREP Table

```
=== Update All Vaults — SITREP ===
<timestamp>

Vault                                   Outcome              Detail
─────────────────────────────────────────────────────────────────────────
aDNA.aDNA                               UP_TO_DATE           HEAD: <sha>
CanvasForge.aDNA                        PULLED_CLEAN         3 commits pulled
ComfyForge.aDNA                         NON_FAST_FORWARD     #needs-human (divergent local commits)
ComicForge.aDNA                         SKIPPED_LOCAL_ONLY   (no remote configured)
...
LatticeHome.aDNA                               SKIPPED_LOCAL_ONLY   (this vault — local-by-default)

Summary:
- N vaults checked
- M up-to-date
- P pulled clean (Q commits total)
- R conflicts (#needs-human)
- S network errors
- T skipped (local-only)
```

### Step 5: Optional Logging

Write the SITREP to `who/coordination/note_YYYYMMDD_update_all_vaults.md` with `urgency: info` (or `warning` if any `#needs-human` flagged).

### Step 6: Exit

Exit code summary:

- 0 = all vaults up-to-date or pulled clean (no `#needs-human`)
- 1 = at least one `#needs-human` (conflicts, auth, missing vault)
- 2 = network errors but no conflicts (transient — re-run later)

## Output

Per-vault outcomes:

- `UP_TO_DATE` — no action needed
- `PULLED_CLEAN` — content updated
- `NON_FAST_FORWARD` — local commits diverge; manual merge needed (`#needs-human`)
- `MERGE_CONFLICT` — pull initiated merge that conflicts (`#needs-human`)
- `NETWORK_ERROR` — transient; re-run later
- `AUTH_FAILED` — credential issue (`#needs-human`)
- `MISSING` — vault path doesn't exist (inventory drift)
- `NOT_A_GIT_REPO` — directory exists but no `.git/`
- `SKIPPED_LOCAL_ONLY` — no remote configured (e.g., this vault); not a problem

## Error Handling

| Outcome | Action |
|---|---|
| `NON_FAST_FORWARD` | Operator decides: rebase, merge, or reset (skill does not auto-decide) |
| `MERGE_CONFLICT` | Operator resolves conflicts in affected vault; re-run skill |
| `AUTH_FAILED` | Run `skill_node_credentials_audit` to verify auth state |
| `MISSING` | Run `skill_inventory_refresh` to reconcile inventory with disk |
| `NETWORK_ERROR` | Re-run later; transient |

## Related

- `how/skills/skill_inventory_refresh.md` — reconcile inventory with disk after this skill flags `MISSING`
- `how/skills/skill_node_health_check.md` — D10 reproducibility gate (validates inventory consistency)
- `how/skills/skill_node_credentials_audit.md` — diagnose `AUTH_FAILED` outcomes
- `what/inventory/inventory_vaults.yaml` — source of vault list
