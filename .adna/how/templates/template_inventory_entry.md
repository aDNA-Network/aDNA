---
type: inventory
subtype: {vaults | system | memberships | <domain>}
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
last_edited_by: agent_{username}
tags: [inventory, {subtype}]
---

# inventory_{subtype} — {Human-readable title}

## Overview

{One or two sentences: what installed/configured state this record captures, and for which host/graph. State whether it is refreshed by a skill or hand-maintained.}

## Inventory

{The records themselves — a table is typical. Adapt columns to the subtype.}

| Item | Class | Path / Location | Status | Notes |
|------|-------|-----------------|--------|-------|
| {name} | {class} | {path} | {active \| pending \| archived} | {note} |

## Maintenance

- Refreshed by: {refresh skill, e.g., `skill_inventory_refresh`, or "hand-maintained"}
- Validated by: {health-check skill, e.g., `skill_node_health_check`} — drift is a D10 reproducibility finding.
- Refresh cadence: {after install/uninstall/upgrade | quarterly | on-demand}

## Paired `.yaml` companion (Compliance Dimension D9)

Every inventory entry is markdown-canonical with a paired machine-readable `.yaml` of the same basename (`inventory_{subtype}.yaml`). Write both atomically and keep them in sync. Skeleton:

```yaml
type: inventory
subtype: {subtype}
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_edited_by: agent_{username}

items:
  - name: {item_name}
    class: {class}
    path: {path}
    status: {active | pending | archived}
    note: "{note}"

# Federation block (Compliance Dimension D7) — include ONLY for network-facing records
# (e.g., memberships). Default posture is node-private; opt in deliberately. Omit entirely
# for node-private inventory (vaults, system).
# federation:
#   shareable: false        # opt-in only
#   discoverable: false     # separate opt-in decision
#   source_instance: {hostname}
#   version_policy: locked
#   license: private
#   creators: [{username}]
#   keywords: [{tag}]
```

## Cross-References

- [[../../what/inventory/AGENTS|what/inventory]] — the `inventory` entity-type scaffold (format, federation, refresh discipline)
- [[../../what/ontology|ontology]] — base ontology (row 15: `inventory`)
- [[../../what/decisions/adr_035_inventory_identity_base_entity_types|ADR-035]] — base-type promotion (standard v2.3)
- [[../../who/identity/AGENTS|who/identity]] — the WHO-leg complement (`identity`)
