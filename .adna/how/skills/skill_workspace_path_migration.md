---
type: skill
skill_type: agent
created: 2026-06-09
updated: 2026-06-10
status: active
category: migration
trigger: "Operator on a legacy workspace root (default ~/lattice) wants to migrate to the recommended ~/aDNA root — or any OLD_ROOT → NEW_ROOT workspace-root move"
last_edited_by: agent_stanley
tags: [skill, migration, workspace_root, path_migration, lattice_to_adna, symlink_shim, harness_rekey, reversible, candidate_upstream]

requirements:
  tools: []
  context: ["CLAUDE.md (workspace router)", "MANIFEST.md"]
  permissions:
    - "move the workspace-root directory (mv OLD_ROOT NEW_ROOT)"
    - "create a back-compat symlink (ln -s NEW_ROOT OLD_ROOT)"
    - "recreate Python venvs in the workspace"
    - "edit shell rc, Obsidian registrations, daemon LaunchAgents/units"
    - "rename ~/.claude/projects/ + memory directories (harness re-key)"
    - "path-scoped edits + git commits across live-consumer vault files"
---

# Skill: Workspace Path Migration (`OLD_ROOT → NEW_ROOT`)

## Overview

Agentically migrates an aDNA **workspace root** from `OLD_ROOT` to `NEW_ROOT` — by default `~/lattice → ~/aDNA`, the Lattice→aDNA brand-pivot doc-default flip — **reversibly**. The workspace root is the directory that *contains* `.adna/` (the base template); it is an **operator convention**, never a hardcoded path — aDNA tooling resolves a detected `<workspace_root>`. This skill therefore changes operator-side state (the directory, system anchors, and live references), not the standard itself.

The move is **not** cosmetic. A bare symlink alias does **not** achieve a workspace move: the agent harness keys session history + memory by the **realpath** of the working directory, so only a real `mv` (plus a harness re-key) carries context into the new structure. The symlink is the *safety shim* that keeps every hardcoded `OLD_ROOT/...` reference valid mid-migration, making nearly every step reversible.

This generalizes the Stanley-node runbook (`aDNALabs.aDNA` Operation Homecoming) into a reusable, any-user, any-root procedure. It is a **candidate upstream** skill → `.adna/how/skills/` (per `skill_upstream_contribution.md`); file the idea, never push to `.adna/` directly.

> **Worked example (canonical):** `aDNALabs.aDNA/how/campaigns/campaign_adnalabs_genesis/missions/mission_path_migration_l1.md` is the canonical Stanley-node instance (`~/lattice → ~/aDNA`, L1-first, reversible, harness re-key R5 as the crux). **Mechanism reference:** `aDNALabs.aDNA/what/migration/path_migration_execution_playbook.md` (7 system anchors, sequencing, rollback). **Risks:** `aDNALabs.aDNA/what/migration/migration_risk_register.md` R5 (harness context-key loss) + R7 (names-before-path).

> **Standalone shell companion:** `how/skills/migrate_workspace_root.sh` (this directory) performs the mechanical preflight/move/sweep/proofs for operators outside an agent session; this skill remains the canonical agentic path and uniquely owns the harness re-key (Step 5).

## Trigger

Invoked when an operator on a legacy workspace root asks to adopt the recommended root (default `~/lattice → ~/aDNA`), or for any `OLD_ROOT → NEW_ROOT` workspace-root move. Not automatic — always operator-initiated; the move is system-level and crosses a human gate (Standing Order: destructive/irreversible actions require confirmation).

## Parameters

| Parameter | Source | Required | Default |
|-----------|--------|----------|---------|
| `OLD_ROOT` | The current workspace-root path (the directory containing `.adna/`) | Yes | `~/lattice` (auto-detected) |
| `NEW_ROOT` | The target workspace-root path | Yes | `~/aDNA` |
| `carry_history` | Whether to rename harness project/memory dirs so session history + memory follow the move (vs. accept fresh keys) | No | `true` (carry) |
| `keep_shim_grace` | Keep the `OLD_ROOT → NEW_ROOT` symlink for a defined grace period after full verify | No | operator choice |

**Detect, do not assume.** Resolve `OLD_ROOT` as the realpath of the directory containing `.adna/` (e.g. `dirname` of `$(find . -maxdepth 2 -name .adna -type d)` from the workspace, or the parent of the running vault). Never hardcode `~/lattice` — confirm the detected value with the operator before any move.

## Requirements

### Tools/APIs
- Directory move (`mv`) + symlink (`ln -s`)
- Python venv recreation (`python -m venv` + dependency reinstall)
- File read/write (shell rc, Obsidian `obsidian.json`, daemon LaunchAgents/systemd units, `.claude/` configs)
- Directory rename for harness re-key (`mv ~/.claude/projects/-...-<oldroot>-* → -<newroot>-*`)
- Path-scoped git staging + commit per vault

### Context Files
- The workspace router `CLAUDE.md` (`OLD_ROOT/CLAUDE.md`) — the primary live-consumer reference
- Per-vault `CLAUDE.md` / `AGENTS.md`, `doctrine_*` files, and any `federation_ref` blocks carrying absolute roots
- The credential broker's path exports (if a `Home.aDNA`/Hestia-style broker is present) — coordinate, do not unilaterally rewrite

### Permissions
- Move the workspace-root directory and create the shim
- Recreate venvs; edit shell rc / Obsidian regs / daemon definitions
- Rename `~/.claude/projects/` + memory dirs (harness re-key)
- Path-scoped edits to live-consumer vault files (never `git add -A`)

## Preconditions

1. **Names before paths (R7).** Any in-flight vault/service **renames are LOCKED first.** Migrating the path while names are still moving leaves refs like `NEW_ROOT/OldName.aDNA/` looking stale mid-project. Confirm the rename wave is complete before the path move.
2. **Quiesce the workspace.** Stop any vault daemon (e.g. a TaskForge bridge: `launchctl bootout …` / `systemctl --user stop …`); **close Obsidian**; finish and **commit all vault git state** (every lineage vault clean — `git status` clean).
3. **Pick a quiet window.** A system reset/refresh is the ideal window — daemon + venvs are already being disrupted, so the recreate cost is "free." Schedule for the first refresh **after** the rename wave, not before.
4. **Back up small high-value dirs.** Before touching anything: back up `~/.claude/projects/` (+ memory dir), the shell rc, and Obsidian `obsidian.json`. These are tiny and make rollback trivial.
5. **Operator confirmation.** Surface `OLD_ROOT`, `NEW_ROOT`, `carry_history`, and the chosen window; get explicit GO. This is a destructive/irreversible-class action.

## Implementation

The seven steps mirror the playbook's 7 system anchors. The shim (Step 2) holds hardcoded refs valid so anchors 1–7 can be re-pointed in any order without breakage.

### Step 1: Pre-flight + back up
- Re-confirm preconditions (names locked, git clean, daemon stopped, Obsidian closed).
- Detect and confirm `OLD_ROOT` (dir containing `.adna/`) and `NEW_ROOT`.
- Back up `~/.claude/projects/` (+ memory), shell rc, and `obsidian.json` to a safe location.

### Step 2: Move + back-compat shim
```bash
mv "$OLD_ROOT" "$NEW_ROOT"
ln -s "$NEW_ROOT" "$OLD_ROOT"     # every hardcoded OLD_ROOT/... ref keeps resolving
```
From here the workspace lives at `NEW_ROOT`; the shim makes the move reversible (`mv "$NEW_ROOT" "$OLD_ROOT"` + remove shim restores prior state).

### Step 3: Recreate Python venvs (anchor #1)
venv interpreters are **absolute** (shebangs + `pyvenv.cfg command=` hardcode `OLD_ROOT/...`). The shim keeps them working *temporarily*; **recreate** each in place (`python -m venv` + reinstall deps) before dropping the shim. Audit every `.venv`/`venv` under the workspace (the daemon's bridge venv, any product/runtime venvs).

### Step 4: Re-point system anchors (anchors #2–4, #6)
- **Daemon (#2):** if the daemon binary lives *outside* the workspace it survives the move, but it operates *through* the vault — re-verify its health endpoint + any claim-lease after the move; reinstall the LaunchAgent/unit only if its provenance venv moved.
- **Obsidian registrations (#3):** `obsidian.json` carries absolute vault paths — rewrite `OLD_ROOT→NEW_ROOT` (or re-add the vaults); re-point any REST/integration plugin and daemon vault path.
- **Shell rc (#4):** re-point `$HOME/<oldroot>/...` exports (editor dirs, credential-inventory pointers). If a credential broker is present, **coordinate** the credential-path exports + any Keychain ACL binary paths with the broker — do not unilaterally rewrite credential state.
- **Workspace symlinks + git + `.claude/` (#6):** verify back-compat symlinks still resolve post-move; `sed` git hooks + `.claude/settings*`/hooks/plans absolute refs (git *remotes* are URLs — fine).

### Step 5: Harness re-key — the crux (anchor #5)
The harness keys session history + memory by the **realpath** of the working directory: `~/.claude/projects/-Users-<user>-<oldroot>-*` (and the parallel memory dir). A real move changes the realpath → new `-…-<newroot>-*` keys → **history + memory do not auto-carry** (the symlink does NOT fix this — realpath still resolves to the moved target name).

Decide per `carry_history`:
- **Carry (default):** rename the harness project dirs (and memory subdirs) `…-<oldroot>-* → …-<newroot>-*`. Same-volume, metadata-only rename. **Test on a COPY first**, then rename in place. This is what actually "builds context in the target structure."
- **Accept fresh keys:** skip the rename; new sessions start clean under the new root (prior history stays under the old keys, still readable).

### Step 6: Staged reference sweep (anchor #7) — live-consumer subset only
Sweep the **live-consumer** references (the ones an agent or tool actually resolves), not every prose mention:
- workspace router `CLAUDE.md`, per-vault `CLAUDE.md` / `AGENTS.md`
- `federation_ref` blocks, `doctrine_*` files, code literals (hardcoded absolute roots in scripts)

`sed`-replace `OLD_ROOT/ → NEW_ROOT/` (and the absolute `/Users/<user>/<oldroot>/ → /Users/<user>/<newroot>/`), **commit per vault**, verify links. **Leave prose/historical narrative** describing past events — the shim covers those until it is dropped, and historical accuracy is preserved (do not rewrite the record). Stage **explicit path-scoped files only** (never `git add -A`); verify `git diff --cached --name-only` before each commit; no force-push.

### Step 7: Verify battery → drop shim
Run the full verify battery and require all-green before dropping the shim:
- **Links** resolve (no broken wikilinks / dead absolute paths in swept files).
- **Daemon health** endpoint + claim-lease (if applicable) respond.
- **Obsidian** opens every vault from the new root.
- **Credential exports** resolve (broker env-vars / `op read` still work).
- **Harness** opens a session under the new key with history/memory present (if `carry_history`).

Once **zero** refs resolve through the symlink and the battery is green: `rm "$OLD_ROOT"` (or keep it for `keep_shim_grace`). The migration is complete.

> **Multi-node note:** only the L1 operator workspace moves. Remote roots (L2 clusters, partner nodes) **do not move** — reconcile them via an environment override (e.g. a `REMOTE_BASE` env-var), never by moving their roots.

## Universal Rollback

The shim + git history make every step reversible **except** the harness re-key, which is reversible by renaming the dirs back:

1. **Directory:** `mv "$NEW_ROOT" "$OLD_ROOT"` and remove the shim — restores the prior root.
2. **Harness keys:** rename `~/.claude/projects/-…-<newroot>-* → -…-<oldroot>-*` (and memory dirs) back. (You backed these up in Step 1; restore from backup if a rename went wrong.)
3. **References:** per-file `git revert` / checkout the per-vault sweep commits.
4. **System anchors:** restore shell rc / `obsidian.json` / daemon definitions from the Step 1 backup; recreate venvs against `OLD_ROOT` if already recreated against `NEW_ROOT`.

Because the shim keeps `OLD_ROOT/...` valid throughout, partial rollback at any single step is safe — nothing depends on a step that hasn't been reverted yet.

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Migrated workspace | Directory | Workspace root relocated `OLD_ROOT → NEW_ROOT` |
| Back-compat shim | Symlink | `OLD_ROOT → NEW_ROOT` (dropped after full verify, or kept for grace) |
| Re-keyed harness state | Directories | `~/.claude/projects/` + memory dirs renamed (if `carry_history`) — history + memory carried |
| Re-pointed anchors | Files | venvs recreated; shell rc, Obsidian regs, daemon, `.claude/` configs updated |
| Swept references | Git commits | Per-vault path-scoped commits across the live-consumer subset |
| Verify battery result | Report | All-green gate before shim drop |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `NEW_ROOT` already exists | Target collision | Stop; ask the operator to choose a different target or clear the path. Never overwrite. |
| Harness re-key loses history | Wrong dir pattern / cross-volume copy | Restore `~/.claude/projects/` from the Step 1 backup; re-test the rename on a copy before retrying. |
| venv won't run after move | Recreated against the wrong root, or not recreated | Recreate against `NEW_ROOT` (the shim keeps the old paths valid until you do). |
| Daemon health red post-move | Vault path not re-pointed / venv moved | Re-point the daemon's vault path; reinstall the LaunchAgent/unit if its venv moved; re-verify. |
| Broken refs after shim drop | A live-consumer ref was missed in the sweep | Re-create the shim (`ln -s`), find the missed ref, sweep + commit, re-verify, drop again. |
| Names still moving | R7 violated (path moved before rename lock) | Roll back the path move (Universal Rollback); complete the rename wave first; re-run. |

## Related

- [[../../../aDNALabs.aDNA/how/campaigns/campaign_adnalabs_genesis/missions/mission_path_migration_l1|mission_path_migration_l1.md]] — canonical Stanley-node worked example (`~/lattice → ~/aDNA`, L1-first)
- [[../../../aDNALabs.aDNA/what/migration/path_migration_execution_playbook|path_migration_execution_playbook.md]] — mechanism-complete playbook (7 anchors, sequencing, rollback)
- [[../../../aDNALabs.aDNA/what/migration/migration_risk_register|migration_risk_register.md]] — R5 (harness context-key loss) + R7 (names-before-path)
- [[skill_upstream_contribution|skill_upstream_contribution.md]] — mechanism for upstreaming this skill → `.adna/how/skills/`
- [[skill_project_fork|skill_project_fork.md]] — workspace-root detection precedent (`<workspace_root>` = dir containing `.adna/`)
- [[../../what/docs/projects_folder_pattern|projects_folder_pattern.md]] — workspace-root convention + back-compat note
