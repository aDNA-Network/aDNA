---
type: skill
skill_type: agent
created: 2026-05-18
updated: 2026-05-18
status: active
category: development
trigger: When a vault is initialized or upgraded — installs deploy-time scaffolding (pre-push sanitization hook)
last_edited_by: agent_stanley
tags: [skill, deploy, hook, installer, idempotent, v7_0, sanitization]

requirements:
  tools: [bash, cp, chmod]
  context: [how/standard/hooks/pre-push-sanitize.sh]
  permissions: [write access to .git/hooks/]
---

# Skill: Deploy

## Overview

Installs deploy-time scaffolding for the vault. At v7.0, the primary install is the pre-push sanitization hook — copies `how/standard/hooks/pre-push-sanitize.sh` (vault-local, post-M03-flatten canonical) or `.adna/how/standard/hooks/pre-push-sanitize.sh` (template-shipped fallback, for legacy per-vault-`.adna/` layouts) to `.git/hooks/pre-push` with executable permissions.

Idempotent: re-running on a vault with the current hook installed is a no-op (overwrites with identical content). Future v7.x+ template upgrades that ship new or updated hooks should re-run this skill to keep installations current.

## Trigger

Invoke when:
- A vault is freshly forked via `skill_project_fork` and the operator wants publish capability.
- A vault clones from an existing remote (hooks live in `.git/hooks/`, not version-controlled — they don't transfer via `git clone`).
- The `.adna/` template is upgraded (`git -C .adna pull`) and the hook source has changed.
- An operator wants to verify the installed hook matches the current template.

**Pre-requisites**:
- The pre-push hook source exists at `how/standard/hooks/pre-push-sanitize.sh` (vault-local, post-M03-flatten canonical) OR `.adna/how/standard/hooks/pre-push-sanitize.sh` (template-shipped fallback). If neither exists, the template is pre-v7.0 — run `git -C .adna pull` first.
- The vault is a git repo with a `.git/` directory.

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `force` | bool | No | false | If true, overwrite an existing custom hook without prompting. Default: prompt if `.git/hooks/pre-push` differs from the template source. |
| `dry_run` | bool | No | false | Show what would be installed without executing. |
| `skip_self_test` | bool | No | false | Skip the post-install `--self-test` invocation. Useful when fixtures aren't present yet. |

## Requirements

### Tools/APIs
- `bash` (the hook script is bash).
- `cp`, `chmod`, `diff` (standard POSIX).

### Context Files
- `how/standard/hooks/pre-push-sanitize.sh` — the canonical hook source post-M03-flatten (vault-local copy via `skill_project_fork`). The pre-flatten location `.adna/how/standard/hooks/pre-push-sanitize.sh` is checked as a fallback.

### Permissions
- Write access to `.git/hooks/`.

## Implementation

### Step 1: Verify hook source exists

```bash
# Post-M03-flatten canonical path (vault-local copy via skill_project_fork)
hook_source="how/standard/hooks/pre-push-sanitize.sh"
# Fallback: pre-flatten layout (vault has child .adna/ template subdir)
[[ -f "$hook_source" ]] || hook_source=".adna/how/standard/hooks/pre-push-sanitize.sh"

if [[ ! -f "$hook_source" ]]; then
  echo "ERROR: hook source not found at how/standard/hooks/pre-push-sanitize.sh"
  echo "ERROR: (fallback .adna/how/standard/hooks/pre-push-sanitize.sh also missing)"
  echo "ERROR: Template may be pre-v7.0. Run 'git -C .adna pull' to refresh."
  exit 1
fi
```

### Step 2: Check for existing custom hook

```bash
hook_install=".git/hooks/pre-push"

if [[ -f "$hook_install" ]]; then
  if diff -q "$hook_source" "$hook_install" >/dev/null 2>&1; then
    echo "INFO: pre-push hook already current; no install needed."
    [[ "$skip_self_test" == "true" ]] && exit 0
  else
    echo "WARN: existing pre-push hook differs from template source."
    if [[ "$force" != "true" ]]; then
      diff -u "$hook_install" "$hook_source" | head -20
      read -p "Overwrite existing hook? [y/N] " yn
      [[ "$yn" =~ ^[Yy]$ ]] || {
        echo "INFO: install aborted by operator. Existing hook preserved."
        exit 0
      }
    fi
  fi
fi
```

### Step 3: Install hook

```bash
if [[ "$dry_run" == "true" ]]; then
  echo "DRY-RUN: cp $hook_source $hook_install"
  echo "DRY-RUN: chmod +x $hook_install"
else
  cp "$hook_source" "$hook_install"
  chmod +x "$hook_install"
  echo "INFO: installed pre-push hook → $hook_install"
fi
```

### Step 4: Run hook in self-test mode

```bash
if [[ "$skip_self_test" != "true" && "$dry_run" != "true" ]]; then
  if "$hook_install" --self-test; then
    echo "✓ self-test PASSED"
  else
    echo "❌ self-test FAILED — hook may be corrupted; investigate before publishing."
    exit 1
  fi
fi
```

### Step 5: Record install receipt

```bash
mkdir -p who/peers/deployed
receipt_ts=$(date -u +"%Y%m%dT%H%M%SZ")
receipt_file="who/peers/deployed/${receipt_ts}.md"
operator=$(git config user.email 2>/dev/null || echo "unknown")
hook_version=$(grep -oE 'LAYER_CONTRACT_VERSION=[0-9.]+' "$hook_install" | head -1 | cut -d= -f2)

cat > "$receipt_file" <<EOF
---
type: deploy_receipt
deployed_at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
hook_installed: pre-push
hook_source: ${hook_source}
hook_version: ${hook_version:-unknown}
self_test: $([[ "$skip_self_test" == "true" ]] && echo "skipped" || echo "passed")
operator: ${operator}
---

# Deploy receipt — $(date -u +"%Y-%m-%d")

Installed pre-push sanitization hook:
- Source: \`${hook_source}\`
- Installed at: \`${hook_install}\`
- LAYER_CONTRACT_VERSION: \`${hook_version:-unknown}\`
- Self-test: $([[ "$skip_self_test" == "true" ]] && echo "skipped" || echo "passed")

Next: run \`skill_vault_publish\` to publish the vault (hook will run automatically on push).
EOF
```

The receipt is committed in a follow-up `git commit` so the audit trail persists across clones.

## Outputs

| Output | Type | Description |
|---|---|---|
| Installed hook | `.git/hooks/pre-push` | Executable hook script copied from template |
| Self-test result | stdout | PASS/FAIL of `--self-test` invocation |
| Deploy receipt | `who/peers/deployed/<UTC>.md` | Audit record committed locally |

## Error Handling

| Error | Cause | Resolution |
|---|---|---|
| `hook source not found` | Pre-v7.0 template | Run `git -C .adna pull` to refresh; retry |
| `self-test FAILED` | Hook corruption or fixture issue | Investigate hook source; report upstream if reproducible |
| `existing custom hook` | Operator-modified hook in `.git/hooks/pre-push` | Review diff; use `--force` to overwrite or preserve custom version |
| `permission denied writing .git/hooks/` | Unusual permission state | Check filesystem permissions; ensure operator has write access |

## Self-reference (Standing Order #2)

This skill demonstrates the v7.0 "deploy-time install" pattern in working form: scaffolding that doesn't version-control (`.git/hooks/` is gitignored by git itself) gets installed by an idempotent skill, with a receipt recording the install for audit. The skill itself follows the same content conventions as the published content — frontmatter, dual-audience overview, copy-pasteable steps.

## Related

- **`how/standard/hooks/pre-push-sanitize.sh`** — the hook this skill installs (vault-local post-M03-flatten; `.adna/how/standard/hooks/pre-push-sanitize.sh` is the fallback for legacy per-vault-`.adna/` layouts).
- **`skill_vault_publish.md`** — the publish skill that depends on the hook being installed.
- **`skill_git_remote_setup.md`** — first-time remote configuration (run before this skill).
- **`what/decisions/adr_010_publish_skill_naming.md`** — the v7.0 publish-skill family decision.
