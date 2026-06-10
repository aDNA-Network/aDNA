---
type: skill
skill_type: agent
created: 2026-05-18
updated: 2026-05-18
status: active
category: development
trigger: When a vault is ready to publish to its GitHub remote (push commits, optionally tag a milestone)
last_edited_by: agent_stanley
tags: [skill, publish, vault, git, github, sanitization, v7_0]

requirements:
  tools: [git, gh (optional for tag creation)]
  context: [how/standard/hooks/pre-push-sanitize.sh, skill_git_remote_setup.md, skill_deploy.md]
  permissions: [git push to origin]
---

# Skill: Vault Publish

## Overview

Publish a vault to its GitHub remote. The vault IS the git repo — `.gitignore` already excludes private files (`what/local/`, `how/local/`, `who/operators/`, `deploy/`, `.publish-clone/`). Sanitization runs automatically as a pre-push hook. The publish operation is a normal `git push`, optionally followed by a milestone tag.

> **Note**: This skill publishes a *vault* to its GitHub remote. To publish a `.lattice.yaml` *object* to a registry via `latlab`, see `skill_lattice_publish.md`.

## Trigger

Invoke when:
- A vault has commits ready to push to its GitHub remote.
- A vault has reached a milestone (e.g., campaign close) and should receive a `vN.M` tag.
- An operator wants to confirm sanitization is current before pushing.

**Pre-requisites**:
- Vault has `origin` configured (run `skill_git_remote_setup` first if not).
- Pre-push hook is installed (run `skill_deploy` if `.git/hooks/pre-push` is missing or out of date).
- All intended changes are committed (`git status --porcelain` is clean).

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `tag` | string | No | — | Milestone tag (e.g., `v7.0`). If set, after the push the skill creates and pushes the tag. |
| `tag_message` | string | No (required if `tag` set) | — | Annotated tag message. |
| `dry_run` | bool | No | false | Preview what would be pushed without actually pushing. |
| `force_unsafe` | bool | No | false | Bypass pre-push hook (NOT recommended; logged in receipt as `force_unsafe`). Reserved for hook-debug scenarios only. |

## Requirements

### Tools/APIs
- `git` (modern version supporting `--porcelain`, `push --tags`, `hooks/pre-push`).
- `gh` CLI (optional — used only for milestone-tag GitHub release creation in Step 5).

### Context Files
- `how/standard/hooks/pre-push-sanitize.sh` — the sanitization rules the hook enforces (vault-local post-M03-flatten; `.adna/how/standard/hooks/pre-push-sanitize.sh` is the legacy fallback location).
- `how/skills/skill_git_remote_setup.md` — the first-time-setup precondition.
- `how/skills/skill_deploy.md` — installs the pre-push hook.

### Permissions
- `git push` to `origin` (vault-author or organization member with push rights).
- For milestone-release creation: GitHub `releases:write` scope on the `gh` token.

## Implementation

### Step 1: Pre-flight check

```bash
# Vault must have a configured remote
git remote -v | grep -q '^origin' || {
  echo "ERROR: no origin configured. Run skill_git_remote_setup first."
  exit 1
}

# Pre-push hook must be installed
[[ -x .git/hooks/pre-push ]] || {
  echo "ERROR: pre-push hook missing. Run skill_deploy to install."
  exit 1
}

# Working tree must be clean
[[ -z "$(git status --porcelain)" ]] || {
  echo "ERROR: uncommitted changes. Commit or stash before publishing."
  git status --short
  exit 1
}
```

### Step 2: Pre-push hook runs automatically on push

The pre-push hook (`pre-push-sanitize.sh`, sourced from `.adna/how/standard/hooks/`) runs LAYER_CONTRACT §4 sanitization scan. Three exit conditions:

| Hook exit | Meaning | Skill action |
|---|---|---|
| **0** | Clean | Push proceeds |
| **1** | FAIL — sanitization violation | Push aborted by git; skill reports the hook output and exits non-zero. Operator must fix violations and re-invoke. |
| **2** | WARN — borderline finding | Hook prompts operator via tty; if confirmed, hook returns 0 internally and push proceeds; if rejected, push aborted. |

If `force_unsafe=true`: skill invokes `git push --no-verify` (bypassing the hook entirely) and writes a `force_unsafe push` record to the publish receipt (Step 5) so the audit trail captures the bypass.

### Step 3: Push commits

```bash
current_branch=$(git rev-parse --abbrev-ref HEAD)

if [[ "$force_unsafe" == "true" ]]; then
  git push --no-verify origin "$current_branch"
elif [[ "$dry_run" == "true" ]]; then
  git push --dry-run origin "$current_branch"
else
  git push origin "$current_branch"
fi
```

### Step 4: Milestone tag (if `tag` parameter provided)

```bash
if [[ -n "$tag" ]]; then
  git tag -a "$tag" -m "$tag_message"
  git push origin "$tag"

  # If gh is installed and operator wants a GitHub release surface:
  if command -v gh >/dev/null 2>&1; then
    gh release create "$tag" --title "$tag" --notes "$tag_message"
  fi
fi
```

### Step 5: Record publish receipt

Write a receipt to the vault's `who/peers/published/` directory (creating the directory if missing):

```bash
mkdir -p who/peers/published
receipt_ts=$(date -u +"%Y%m%dT%H%M%SZ")
receipt_file="who/peers/published/${receipt_ts}.md"
commit=$(git rev-parse HEAD)
branch=$(git rev-parse --abbrev-ref HEAD)
operator=$(git config user.email)

cat > "$receipt_file" <<EOF
---
type: publish_receipt
published_at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
commit: ${commit}
branch: ${branch}
tag: ${tag:-null}
sanitization: $([[ "$force_unsafe" == "true" ]] && echo "force_unsafe" || echo "hook-verified")
operator: ${operator}
---

# Publish receipt — $(date -u +"%Y-%m-%d")

Pushed \`${commit}\` (branch \`${branch}\`) to \`origin\`.
$([[ -n "$tag" ]] && echo "Tagged as \`${tag}\`. ${tag_message}")
$([[ "$force_unsafe" == "true" ]] && echo "⚠ Pre-push hook bypassed (\`force_unsafe=true\`). Audit follow-up: confirm sanitization-clean state on next normal publish.")
EOF
```

The receipt is itself committed in a follow-up `git commit` so the audit trail is preserved across clones. (The receipt's own commit does *not* trigger a recursive publish — operators run the skill again later if the receipt commit should also be pushed.)

## Outputs

| Output | Type | Description |
|---|---|---|
| Remote update | git push | `origin/<branch>` advances; tag pushed if requested |
| GitHub release | (optional) gh release | Surfaces `tag` as a Releases-page entry |
| Publish receipt | `who/peers/published/<UTC>.md` | Audit record committed locally |

## Error Handling

| Error | Cause | Resolution |
|---|---|---|
| `no origin configured` | First-time vault | Run `skill_git_remote_setup` first |
| `pre-push hook missing` | Hook never installed or `.git` was re-initialized | Run `skill_deploy` to install the hook |
| `uncommitted changes` | Working tree dirty | Commit or stash before retrying |
| `pre-push hook FAIL` | Sanitization violation | Read hook output; remediate (e.g., remove leaked secrets, untracked private files, accidental binaries); recommit; retry |
| `pre-push hook WARN` | Borderline finding | Operator confirms via hook prompt; if rejected, treat as FAIL |
| `tag already exists locally` | Operator re-tagging an existing milestone | `git tag -d <tag>` and retry, or pick a new tag name |
| `tag already exists on remote` | Race or duplicate publish | `git push origin :refs/tags/<tag>` and retry, or coordinate with co-publishers |

## Self-reference (Standing Order #2)

The receipt at `who/peers/published/<UTC>.md` is itself a vault content file with the standard frontmatter pattern. Future agents reading the receipt see the campaign's content conventions in action — the publish operation produces a content artifact that follows the same rules as every other content file in the vault. The publishing infrastructure follows the same content conventions as the published content.

## Related

- **`skill_lattice_publish.md`** — the *separate* lattice-object registry-publish skill (publishes `.lattice.yaml` objects to a registry via `latlab`; do not confuse).
- **`skill_git_remote_setup.md`** — first-time remote configuration (precondition for first run).
- **`skill_deploy.md`** — installs the pre-push hook.
- **`skill_publish_tarball.md`** — optional offline-tarball alternative.
- **`how/standard/hooks/pre-push-sanitize.sh`** — the pre-push sanitization hook (enforced automatically; `.adna/how/standard/hooks/pre-push-sanitize.sh` is the legacy fallback).
- **`what/decisions/adr_010_publish_skill_naming.md`** — the naming decision that motivates this skill's existence as a separate file.
