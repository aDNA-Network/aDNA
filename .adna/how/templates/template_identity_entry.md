---
type: identity
subtype: {node | <network> | <platform_deployment> | consumer}
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
last_edited_by: agent_{username}
tags: [identity, {subtype}]
---

# identity_{subtype} — {Human-readable title}

## Overview

{One or two sentences: what identity this record captures (host identity, network identity, deployment identity) and what external reality it validates against.}

## Identity

{Field/value table. Use the rows that fit the subtype — node fields for `node`; peer/key/role fields for a network subtype.}

| Field | Value |
|-------|-------|
| Hostname | `{hostname}` |
| Operator | `{operator}` |
| Machine class | {e.g., Apple Silicon Mac (arm64)} |
| OS | {os + version} |
| Persistent UUID | {generated at first health-check run, or `null`} |
| Network peer-id | {peer-id, or `null` until joined} |
| Signing-key reference | {path/source reference only — never the key value} |

## Drift Policy

Identity drift is a **high-severity** finding (see [[../../who/identity/AGENTS|who/identity]] § Identity-Drift Discipline). Any change to hostname, operator, persistent UUID, or peer-id is flagged — not auto-corrected; operator changes escalate `#needs-human`.

## Not Persisted (privacy)

- CPU serial number, MAC addresses, OS machine UUID — OS-managed, queried on demand, never written here.
- Signing-key **values** — only the path/source reference is recorded.

## Paired `.yaml` companion (Compliance Dimension D9)

Every identity entry is markdown-canonical with a paired `.yaml` of the same basename (`identity_{subtype}.yaml`). Skeleton:

```yaml
type: identity
subtype: {subtype}
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_edited_by: agent_{username}

{subtype}:
  hostname: {hostname}        # node subtype
  operator: {operator}
  machine_class: {machine_class}
  persistent_uuid: null       # set at first health-check run
  # network subtype instead carries:
  # peer_id: null
  # signing_key_path: null    # reference only — never the key value
  # role: null

# Federation block (Compliance Dimension D7) — ONLY for network-facing identity.
# Default node-private; identity is sensitive node-fingerprint data — opt in deliberately.
# federation:
#   shareable: false
#   discoverable: false
#   source_instance: {hostname}
#   license: private
#   creators: [{username}]
```

## Cross-References

- [[../../who/identity/AGENTS|who/identity]] — the `identity` entity-type scaffold (drift discipline, privacy, federation)
- [[../../what/ontology|ontology]] — base ontology (row 16: `identity`)
- [[../../what/decisions/adr_035_inventory_identity_base_entity_types|ADR-035]] — base-type promotion (standard v2.3)
- [[../../what/inventory/AGENTS|what/inventory]] — the WHAT-leg complement (`inventory`)
