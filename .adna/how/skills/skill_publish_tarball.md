---
type: skill
skill_type: agent
created: 2026-05-18
updated: 2026-05-18
status: active
category: development
trigger: When an operator needs a reproducible offline tarball of the vault for shipping by non-GitHub channels (USB, partner upload, archive)
last_edited_by: agent_stanley
tags: [skill, publish, tarball, offline, archive, sketch, v7_0]

requirements:
  tools: [git, sha256sum (or shasum on macOS)]
  context: [how/standard/hooks/pre-push-sanitize.sh]
  permissions: [read access to vault; write access to output directory]
---

# Skill: Publish Tarball

> **Status — sketch (v7.0)**: This skill ships as a working sketch covering the core flow. Full expansion (per-platform sha256 variations, sanitization-warning surface, large-vault chunking) defers to M07 or first operator use. Open an issue or expand at first-use if the sketch is insufficient.

## Overview

Generate a reproducible offline tarball of the vault for shipping by non-GitHub channels — USB sticks for air-gapped environments, partner uploads, long-term archival, or providing a snapshot to collaborators without GitHub access. The tarball is `git archive`-based (so it respects `.gitignore` and stays clean of working-tree artifacts) and ships with a sha256 manifest sidecar for integrity verification.

This skill is **optional** — vaults that publish exclusively via GitHub (`skill_vault_publish`) never need it. Operators in air-gapped, partner-handoff, or archival scenarios use it as needed.

## Trigger

Invoke when:
- An operator needs to ship the vault to an air-gapped environment.
- A partner requests a vault snapshot without GitHub access (rare; usually a one-time hand-off).
- An archival pass requires a reproducible snapshot artifact.

**Pre-requisites**:
- Vault is a git repo with at least one commit.
- Working tree is clean (`git status --porcelain` is empty) — tarballs reflect commits, not working-tree state.

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `output_dir` | path | No | `./` | Where to write the tarball + manifest. |
| `tag_or_commit` | string | No | `HEAD` | Git ref to archive (tag for milestone snapshots; commit sha for arbitrary points). |
| `dry_run` | bool | No | false | Show what would be created without executing. |

## Requirements

### Tools/APIs
- `git` (modern version with `git archive`).
- `sha256sum` (Linux) or `shasum -a 256` (macOS) — autodetected.

### Permissions
- Read access to the vault.
- Write access to `output_dir`.

## Implementation

### Step 1: Pre-flight

```bash
# Working tree must be clean (tarball reflects committed state)
[[ -z "$(git status --porcelain)" ]] || {
  echo "ERROR: uncommitted changes. Commit or stash first."
  git status --short
  exit 1
}

# Resolve tag_or_commit to a full sha
commit_full=$(git rev-parse "${tag_or_commit:-HEAD}")
commit_short=$(git rev-parse --short "${tag_or_commit:-HEAD}")
vault_name=$(basename "$PWD")
ts=$(date -u +"%Y%m%dT%H%M%SZ")
```

### Step 2: (Optional) Sanitization scan

Run the pre-push hook in informational mode against the working tree (recommended; not strictly required since `git archive` respects `.gitignore`):

```bash
# Post-M03-flatten canonical path (vault-local); fallback to legacy .adna/ layout
hook="how/standard/hooks/pre-push-sanitize.sh"
[[ -x "$hook" ]] || hook=".adna/how/standard/hooks/pre-push-sanitize.sh"
if [[ -x "$hook" ]]; then
  # Sanitization is best-effort here; the hook is designed for git push, not archive
  echo "INFO: tarball respects .gitignore; sanitization scan is advisory only."
fi
```

### Step 3: Create tarball

```bash
tarball="${output_dir%/}/${vault_name}_${commit_short}_${ts}.tar.gz"

if [[ "$dry_run" == "true" ]]; then
  echo "DRY-RUN: git archive --format=tar.gz --prefix=${vault_name}/ -o ${tarball} ${commit_full}"
else
  git archive \
    --format=tar.gz \
    --prefix="${vault_name}/" \
    -o "$tarball" \
    "$commit_full"
  echo "INFO: tarball → $tarball ($(du -h "$tarball" | cut -f1))"
fi
```

### Step 4: Compute sha256 + manifest sidecar

```bash
if command -v sha256sum >/dev/null 2>&1; then
  tarball_sha=$(sha256sum "$tarball" | cut -d' ' -f1)
elif command -v shasum >/dev/null 2>&1; then
  tarball_sha=$(shasum -a 256 "$tarball" | cut -d' ' -f1)
else
  echo "ERROR: no sha256sum or shasum available; cannot create manifest."
  exit 1
fi

manifest="${tarball}.manifest"
cat > "$manifest" <<EOF
---
type: tarball_manifest
vault: ${vault_name}
commit: ${commit_full}
commit_short: ${commit_short}
tag_or_commit_param: ${tag_or_commit:-HEAD}
tarball: $(basename "$tarball")
sha256: ${tarball_sha}
created: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
sanitization: respects-gitignore
git_version: $(git --version | head -1)
---

# Tarball manifest — ${vault_name}

Reproducible vault snapshot.

- Source commit: \`${commit_full}\`
- Tarball: \`$(basename "$tarball")\`
- SHA-256: \`${tarball_sha}\`

**Verify integrity**:
\`\`\`bash
echo "${tarball_sha}  $(basename "$tarball")" | sha256sum -c
\`\`\`

**Extract**:
\`\`\`bash
tar -xzf $(basename "$tarball")
\`\`\`

The tarball expands to \`${vault_name}/\` and reflects the vault at commit \`${commit_short}\`.
EOF

echo "INFO: manifest → $manifest"
```

### Step 5: (Operator hand-off — out of scope for skill)

The tarball + manifest are transient outputs intended for out-of-band delivery (USB, partner upload, archive store). They are **not** committed back into the vault — the source commit is already the canonical record.

## Outputs

| Output | Type | Description |
|---|---|---|
| Tarball | `<vault>_<commit-short>_<UTC>.tar.gz` | gzipped tar of the vault at the specified commit |
| Manifest | `<tarball>.manifest` | YAML+markdown sidecar with sha256 + extraction instructions |

## Error Handling

| Error | Cause | Resolution |
|---|---|---|
| `uncommitted changes` | Working tree dirty | Commit or stash before retrying |
| `git ref not found` | `tag_or_commit` doesn't resolve | Use `git tag -l` / `git log` to find a valid ref |
| `no sha256 tool available` | Minimal environment | Install `coreutils` (Linux) or use macOS default `shasum` |

## Sketch limitations (deferred to first operator use or M07)

- **No large-vault chunking**: tarballs over a few hundred MB may need split into multiple parts (`split -b 500m`); not currently handled.
- **No per-platform sha256 variation**: assumes either `sha256sum` (Linux) or `shasum -a 256` (macOS); Windows variation deferred.
- **No GPG signing**: the manifest could be signed for stronger integrity; deferred to first operator who needs it.
- **No tarball encryption**: assumes the operator handles encryption out-of-band if needed (e.g., `gpg`-encrypted disk for USB transport).

If you need any of these, expand this skill at first use and contribute the addition upstream.

## Self-reference (Standing Order #2)

This skill demonstrates the v7.0 "publish via non-git channel" alternative. The manifest is itself a content file with the standard frontmatter pattern — even a transient artifact follows the vault's content conventions. The skill explicitly ships as a sketch (Standing Order #7 dual-audience: sketches are legitimate v7.0 ship-shape when the full spec exceeds first-use needs).

## Related

- **`skill_vault_publish.md`** — primary publish path (GitHub git push); use this skill instead for non-GitHub scenarios.
- **`skill_git_remote_setup.md`** — first-time GitHub remote (not needed for tarball flow).
- **`what/decisions/adr_010_publish_skill_naming.md`** — the v7.0 publish-skill family decision.
