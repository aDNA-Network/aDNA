---
type: skill
skill_type: agent
created: 2026-05-11
updated: 2026-05-14
status: active
category: node_operations
trigger: "Enumerate credential SOURCES on this node — env-vars matching `*_TOKEN`/`*_KEY`/`*_SECRET`, gh CLI auth status (token-NAME only, never value), ssh public keys at `~/.ssh/*.pub`, keychain entries by name (where queryable). Emits a redacted summary. Flags `#needs-human` if expired tokens detected. **NAMES ONLY** — never persists credential values, hashes, or last-4-chars."
last_edited_by: agent_stanley
graduated_from: LatticeHome.aDNA@411660e  # v0.1 initial bootstrap, M04 S2 of campaign_adna_v2_infrastructure
graduated_at: 2026-05-14
graduated_via: campaign_federation_beta_planning M-H.1.5
tags: [skill, node_adna, credentials, audit, redaction_aware, graduated]

requirements:
  tools: [env, gh, ssh-keygen, security (macOS keychain CLI)]
  context: [who/identity/identity_lattice_protocol.md]
  permissions: [read env-var NAMES (never values), read ~/.ssh/*.pub (public keys only), read keychain entry NAMES (never values), read gh auth status]
---

# Skill: Node Credentials Audit

## Overview

Enumerates **credential SOURCES** on this node — never values. Surfaces what kinds of credentials are configured and where they live so the operator can rotate, revoke, or re-issue. **Redaction-aware**: NAMES ONLY. The actual credential values live in OS-managed stores (keychain, gpg-agent, env vars set by shell rc) and are never persisted to the vault.

## Trigger

Invoked when:

- Operator asks: "Audit my credentials" or "What tokens/keys does this node have?"
- After credential rotation (verify the rotation took effect)
- Quarterly review
- Before a node transfer (e.g., new machine, hand-off)
- When `skill_update_all_vaults` reports `AUTH_FAILED` outcomes

## Parameters

| Parameter | Source | Required |
|---|---|---|
| `verbose` | CLI flag | No (default: false — when true, includes "last_used" timestamps where queryable) |
| `format` | CLI arg | No (default: `markdown` — also supports `yaml` for programmatic consumption) |

## Requirements

### Tools/APIs

- `env` — list env-var names (NOT values; output is filtered to names matching credential-shaped patterns)
- `gh auth status` — GitHub CLI auth state (token type + scopes; NOT the token value)
- `ssh-keygen -l -f <pub-key>` — fingerprint public keys (public keys only; private keys NOT read)
- `security` (macOS keychain CLI) — list keychain entry names

### Context Files

- `who/identity/identity_lattice_protocol.md` — for LP signing-key reference (path only)

### Permissions

- Read env-var NAMES (filter against credential patterns; never extract values)
- Read `~/.ssh/*.pub` (public keys only; never `~/.ssh/id_*` private keys)
- Read keychain entry NAMES (never values)
- Read `gh auth status` output (parses NAME + scopes; never token value)

## Implementation

### Step 1: Env-Var Names

```bash
env | awk -F'=' '{print $1}' | grep -E '_(TOKEN|KEY|SECRET|API|AUTH|PWD|PASSWORD)$' | sort
```

Output: list of env-var NAMES only. NEVER extract values. Common patterns:

- `GITHUB_TOKEN`, `GH_TOKEN`
- `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- `HF_TOKEN` (Hugging Face)
- etc.

### Step 2: GH CLI Auth Status

```bash
gh auth status 2>&1 | grep -E "Logged in|Token:" | sed 's/Token: .*/Token: <REDACTED>/'
```

Output: hostname + login + token scopes; token value redacted. Captures:

- Logged in to: github.com as <login>
- Token: `<REDACTED>` (NAMES of scopes: `repo`, `read:org`, ...)
- Token expiry: (where queryable; flag `#needs-human` if expired)

### Step 3: SSH Public Keys

```bash
ls ~/.ssh/*.pub 2>/dev/null | xargs -I{} ssh-keygen -l -f {}
```

Output: per pubkey — fingerprint + algorithm + comment. NEVER read private keys (`~/.ssh/id_*` without `.pub` suffix).

Common pubkey filenames:
- `id_ed25519.pub`
- `id_rsa.pub`
- `id_ecdsa.pub`

### Step 4: macOS Keychain Entries (NAMES only)

```bash
security list-keychains | xargs security dump-keychain 2>/dev/null | grep -E "0x00000007|svce" | head -50
```

Output: list of service NAMES (typically: `GitHub PAT for <login>`, `AWS Access Key for <profile>`, etc.). Filter heavily — keychain dumps can be noisy.

### Step 5: LP Signing-Key Reference

Read `who/identity/identity_lattice_protocol.yaml`. Report `signing_key_path:` value (the PATH, never the key contents).

### Step 6: Emit Redacted Summary

```
=== Node Credentials Audit — REDACTED SUMMARY ===
<timestamp>
Host: <hostname> · Operator: <operator>

Env-Var NAMES (no values):
- GITHUB_TOKEN
- HF_TOKEN
- OPENAI_API_KEY
- ...

GitHub CLI Auth:
- Logged in to: github.com as <login>
- Token: <REDACTED>
- Scopes: repo, read:org, workflow
- Expiry: <date> (or "no-expiry" or "EXPIRED — #needs-human")

SSH Public Keys (~/.ssh/*.pub):
- id_ed25519.pub: SHA256:xyz...abc (ed25519 256) — comment: "<operator>@<hostname>"
- ...

macOS Keychain Service NAMES (truncated to top 50):
- GitHub PAT for <login>
- AWS Access Key for <profile>
- ...

LP Signing Key:
- Path: <placeholder> (not yet populated; see who/identity/identity_lattice_protocol.md)

Flags:
- (none) — or list of #needs-human items (expired tokens, missing keys, etc.)
```

### Step 7: Output Targets

- **`markdown` format**: emit to stdout (default)
- **`yaml` format**: emit to stdout as structured YAML (for programmatic consumption)
- Optionally write to `who/coordination/note_YYYYMMDD_credentials_audit.md` (urgency: `info` or `warning` per flags)

### Step 8: Update inventory_system.yaml `env_var_names`

If `env_var_names` was empty (first run), populate it with the NAMES discovered in Step 1. NEVER write values.

## Output

| Output | Type | Description |
|---|---|---|
| Redacted summary | stdout (markdown or yaml) | NAMES-only audit of credentials |
| `inventory_system.yaml` update | File | Env-var NAMES populated (first run) |
| Optional coord note | File | If flags present, write `who/coordination/note_YYYYMMDD_credentials_audit.md` |

## Hard Constraints (NAMES ONLY discipline)

- **Never** read env-var VALUES (only names matching credential patterns)
- **Never** read private SSH keys (`~/.ssh/id_*` without `.pub`)
- **Never** dump keychain entry VALUES — service NAMES only
- **Never** persist credential fingerprints, hashes, or last-4-chars
- **Never** log credentials to file (the audit summary may go to `who/coordination/` BUT must contain only NAMES + status; never values)

## Error Handling

| Error | Cause | Resolution |
|---|---|---|
| `gh auth status` fails | Not logged in | Report "not logged in"; not an error |
| `~/.ssh` doesn't exist | No SSH keys configured | Report "no SSH keys"; not an error |
| `security` keychain access denied | macOS prompt declined | Re-run with operator approval |
| Expired token detected | GH token past expiry | Flag `#needs-human`; recommend rotation |
| Env-var name matches pattern but value unset | Empty env-var | Report as "set but empty"; not a credential leak |

## Related

- `how/skills/skill_node_health_check.md` — overall vault health (this audit feeds inventory_system.yaml)
- `who/identity/identity_lattice_protocol.md` — LP signing-key reference (path only)
- `what/inventory/inventory_system.md` — machine state (this audit populates env_var_names section)
- Standing Order: Local-by-default; credentials never leave the node
