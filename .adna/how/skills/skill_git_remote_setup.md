---
type: skill
skill_type: agent
created: 2026-05-18
updated: 2026-07-13
status: active
category: development
trigger: When a vault has no GitHub remote configured and the operator wants to publish it for the first time
last_edited_by: agent_rosetta
tags: [skill, git, remote, github, first_time_setup, naming_convention]

requirements:
  tools: [git, gh CLI authenticated to the target org]
  context: [adr_009_aDNA_naming_convention.md, skill_vault_publish.md, skill_deploy.md]
  permissions: [GitHub repo:create scope on the gh token; GitHub org membership if creating under an org]
---

# Skill: Git Remote Setup

## Overview

First-time GitHub remote configuration for a vault. Performs `gh repo create` + `git remote add origin` + initial `git push -u` in a single skill invocation. Idempotent — re-running on a vault with `origin` already configured is a no-op.

The skill is the precondition for `skill_vault_publish` — `skill_vault_publish` Step 1 fails if `origin` is missing and points the operator here.

## Scope

This skill performs **first-time** remote configuration. It is **not** for:
- Updating an existing remote URL (use `git remote set-url origin <new-url>` directly).
- Adding a second remote (e.g., `upstream`) — out of scope; operator runs `git remote add upstream ...` directly.
- Renaming an existing repo on GitHub (use `gh repo rename` or the GitHub UI directly).

If `origin` already exists, the skill exits cleanly with a message and does nothing. This makes it idempotent — safe to re-run.

## Trigger

Invoke when:
- A vault was created (typically via `skill_project_fork`) and the operator wants to publish it to GitHub.
- A vault was cloned without a remote (rare; usually means the vault was cloned by directory copy rather than `git clone`).
- A naming-convention audit flagged a vault as remoteless and the operator wants to add one.

**Pre-requisites**:
- `gh` CLI is installed and authenticated to the target org or user account (verify with `gh auth status`).
- Git working tree has at least one commit (the skill pushes existing history; it does not initialize the repo).
- The vault directory name follows the naming convention `<name>.aDNA/` (skill warns if not — see §Special cases).

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `org` | string | Yes | — | GitHub organization or user (e.g., `aDNA-Network`). |
| `repo_name` | string | No | derived | If omitted: derived from the vault directory name (`<name>.aDNA/` → `<name>.aDNA`). Override only if the operator wants a non-conformant name (warns). |
| `description` | string | No | — | GitHub repo description. Recommended (improves discoverability). |
| `homepage` | URL | No | — | Optional homepage URL (e.g., a docs site). |
| `visibility` | enum | No | `public` | `public` or `private`. Default `public` matches the open-source norm for aDNA vaults. |
| `branch` | string | No | `main` | Default branch to push. The skill renames the current branch to this name before pushing if needed. |
| `dry_run` | bool | No | false | Preview commands without executing. |

## Requirements

### Tools/APIs
- `git` (modern version with `branch -M`, `remote add`, `push -u`).
- `gh` CLI (used for `gh auth status`, `gh repo create`).

### Context Files
- `what/decisions/adr_009_aDNA_naming_convention.md` — the naming convention this skill enforces (informational at first; enforced after the audit pass). Documents how pre-existing non-conformant repo names are grandfathered (rather than force-renamed) and the path-style-remote exception.

### Permissions
- `gh` token must have `repo:create` scope on the target org (verify via `gh auth status`).
- If pushing to an org repo, the operator must be a member with appropriate permissions.

## Implementation

### Step 1: Idempotency check

```bash
if git remote -v | grep -q '^origin'; then
  echo "INFO: origin already configured:"
  git remote -v | grep '^origin'
  echo "INFO: skill_git_remote_setup is a no-op when origin exists."
  echo "INFO: To change the origin URL, use 'git remote set-url origin <new-url>' directly."
  exit 0
fi
```

### Step 2: Derive `repo_name` and lint against the naming convention

```bash
# Derive default repo_name from the vault directory name
vault_dir=$(basename "$PWD")  # e.g., "MyProject.aDNA"

if [[ -z "$repo_name" ]]; then
  repo_name="$vault_dir"
fi

# Lint: warn if the name doesn't follow <name>.aDNA convention
# Grandfathered exceptions per ADR-009 — repo names created before the convention
# that the operator has chosen not to rename. Empty by default; populate for your
# own workspace if needed, e.g.: GRANDFATHERED=("legacy-project" "old-name-flat")
GRANDFATHERED=()

if [[ "$repo_name" != *.aDNA ]] && \
   ! printf '%s\n' "${GRANDFATHERED[@]}" | grep -qx "$repo_name"; then
  echo "WARNING: repo_name '$repo_name' does not follow <name>.aDNA convention."
  echo "WARNING: ADR-009 recommends <name>.aDNA form for vault repos."
  [[ ${#GRANDFATHERED[@]} -gt 0 ]] && echo "WARNING: Grandfathered exceptions: ${GRANDFATHERED[*]}"
  echo "WARNING: Override with --repo-name if intentional, or rename the vault directory."
  # TODO(ADR-009): consider flipping this from warn-and-continue to hard-fail after a future audit pass
  read -p "Continue with non-conformant name? [y/N] " yn
  [[ "$yn" =~ ^[Yy]$ ]] || exit 1
fi
```

### Step 3: Verify `gh` authentication

```bash
gh auth status >/dev/null 2>&1 || {
  echo "ERROR: gh CLI not authenticated. Run 'gh auth login' first."
  exit 1
}
```

### Step 4: Create the GitHub repository

```bash
gh_args=(--description "$description")
[[ -n "$homepage" ]] && gh_args+=(--homepage "$homepage")
if [[ "$visibility" == "private" ]]; then
  gh_args+=(--private)
else
  gh_args+=(--public)
fi

if [[ "$dry_run" == "true" ]]; then
  echo "DRY-RUN: gh repo create $org/$repo_name ${gh_args[*]}"
else
  gh repo create "$org/$repo_name" "${gh_args[@]}"
fi
```

`gh repo create` produces an empty remote repo (no auto-init); we'll push our local history into it.

### Step 5: Add the remote

```bash
remote_url="https://github.com/$org/$repo_name.git"
if [[ "$dry_run" == "true" ]]; then
  echo "DRY-RUN: git remote add origin $remote_url"
else
  git remote add origin "$remote_url"
  echo "INFO: origin set to $remote_url"
fi
```

### Step 6: Rename the local branch if needed

```bash
current_branch=$(git rev-parse --abbrev-ref HEAD)
if [[ "$current_branch" != "$branch" ]]; then
  echo "INFO: renaming branch '$current_branch' → '$branch'"
  if [[ "$dry_run" != "true" ]]; then
    git branch -M "$branch"
  fi
fi
```

### Step 7: Initial push

```bash
if [[ "$dry_run" == "true" ]]; then
  echo "DRY-RUN: git push -u origin $branch --tags"
else
  git push -u origin "$branch" --tags
fi
```

`-u` sets the upstream so subsequent `git pull` / `git push` work without explicit refs. `--tags` pushes any pre-existing local tags so the remote starts in sync.

### Step 8: Record receipt

```bash
mkdir -p who/peers/published
receipt_ts=$(date -u +"%Y%m%dT%H%M%SZ")
receipt_file="who/peers/published/${receipt_ts}_remote_setup.md"
operator=$(git config user.email)

# Determine naming-lint outcome
naming_lint="pass"
if [[ "$repo_name" != *.aDNA ]]; then
  if printf '%s\n' "${GRANDFATHERED[@]}" | grep -qx "$repo_name"; then
    naming_lint="grandfathered:${repo_name}"
  else
    naming_lint="override"
  fi
fi

cat > "$receipt_file" <<EOF
---
type: publish_receipt
receipt_subtype: remote_setup
created_at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
remote_url: https://github.com/${org}/${repo_name}.git
visibility: ${visibility}
branch: ${branch}
operator: ${operator}
naming_lint: ${naming_lint}
---

# Remote setup receipt — $(date -u +"%Y-%m-%d")

Configured \`origin\` for vault \`${vault_dir}\`:
- Remote URL: https://github.com/${org}/${repo_name}.git
- Visibility: ${visibility}
- Default branch: ${branch}
- Initial push: $(git rev-parse --short HEAD) + $(git tag | wc -l | tr -d ' ') tags

Naming convention check: ${naming_lint}.

Next: run \`skill_deploy\` to install the pre-push hook before the first \`skill_vault_publish\` run.
EOF
```

The receipt is committed in a follow-up `git commit` so the audit trail persists.

## Outputs

| Output | Type | Description |
|---|---|---|
| GitHub repository | Remote | New empty-then-populated repo at `https://github.com/<org>/<repo_name>` |
| Local origin config | git config | `origin` remote pointing at the new URL |
| Default branch | Remote main | `<branch>` set as the remote's default |
| Receipt | `who/peers/published/<UTC>_remote_setup.md` | Audit record |

## Error Handling

| Error | Cause | Resolution |
|---|---|---|
| `origin already configured` | Idempotency check (Step 1) — not an error, INFO only | None — skill exits cleanly |
| `gh CLI not authenticated` | `gh auth status` fails (Step 3) | Run `gh auth login`; retry |
| `name conflict on GitHub` | `gh repo create` fails — repo already exists | Either pick a different `repo_name` (use `--repo-name`) or — if the existing repo IS the intended remote — run `git remote add origin` directly with the existing URL and skip Steps 4-5 |
| `permission denied creating repo` | `gh` token lacks `repo:create` on the org | Re-auth `gh` with the right scopes; or ask the org admin to create the repo and provide the URL |
| `nothing to push (no commits)` | First-ever push and the vault has no commits yet | Make at least one commit (`git commit -m "Initial vault scaffold"`) before re-running |
| `non-fast-forward push rejected` | The remote was created with `auto-init` and has unrelated history | Delete the remote (`gh repo delete`) and re-run, OR force-push (`git push -u origin <branch> --force`) — only if you're sure no one else has cloned the empty remote |
| `naming-convention lint refused` | Operator answered N to the lint prompt (Step 2) | Either rename the vault directory to follow `<name>.aDNA/` or re-run with explicit `--repo-name` to confirm intent |

## Special cases

### The aDNA template repo itself

Per `adr_006_github_repo_rename_to_adna.md` (amended 2026-05-18), the template repo is `aDNA-Network/aDNA` (mixed-case canonical, no `.aDNA` suffix) — **not** `<name>.aDNA` form. This is intentional: the template repo IS the convention's source, not a consumer of it. ADR-009 documents this as the canonical exception. (The amendment supersedes an earlier lowercase target; URLs route case-insensitively so lowercase forms still resolve via 301.)

**Skill behavior for the template repo**: not applicable — the template repo's remote is configured upstream by `aDNA-Network`. Operators of the template repo do not run this skill.

### Grandfathered non-conformant repo names

A workspace may contain repos created before the `<name>.aDNA` convention (or under a different scheme) that the operator has chosen not to rename. Add them to the `GRANDFATHERED` array (Step 2) and the skill recognizes them instead of warning. Otherwise the skill warns and proceeds (after operator confirmation) — renames are **operator-discretionary**, handled at the operator's pace, never forced.

### Primary use case: vaults with no configured remote

The skill's primary use case. Any vault created without a configured git remote can run `skill_git_remote_setup` once to configure a remote that follows the convention out of the box.

### Path-style local remotes

A vault may have a remote that points at a local filesystem path rather than a hosting URL — an artifact of a separate-repo-but-co-located history. The skill does not migrate this — the operator decides whether to re-anchor at a git host. The skill warns if it detects an existing non-URL remote and recommends `git remote set-url` directly rather than running this skill.

## Self-reference (Standing Order #2)

The skill enforces the convention ADR-009 codifies. Until a future audit pass flips this from warn-and-continue to hard-fail, the lint is informational. This staging — *informational → enforced* — demonstrates how convention codification works: the convention is built, then the tooling enforces it, then the ecosystem migrates at its own pace.

Grandfathered exceptions live in this skill's own source (the `GRANDFATHERED` array) — an operator who populates it for their workspace encounters the convention's boundary cases directly, and learns the rule by naming its exceptions. The convention is taught by the tool that enforces it.

## Related

- **`skill_vault_publish.md`** — uses `origin` configured by this skill.
- **`skill_deploy.md`** — installs the pre-push hook (run after this skill).
- **`what/decisions/adr_009_aDNA_naming_convention.md`** — the naming convention.
- **`what/decisions/adr_010_publish_skill_naming.md`** — the publish-skill family decision.
- **`how/skills/skill_project_fork.md`** — the skill that creates new vaults; suggests running this skill afterward if GitHub publish is desired.
