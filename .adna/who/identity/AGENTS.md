---
type: directory_index
created: 2026-06-18
updated: 2026-06-18
last_edited_by: agent_rosetta
tags: [directory_index, identity]
---

# who/identity/ — Identity

## Purpose

The `identity` base entity type (WHO leg): **stable identity records that persist across sessions and validate against external reality** — hostname, operator, machine class, persistent UUID, and network peer-id / signing-key references. It is the WHO-leg complement to [[../../what/inventory/AGENTS|`inventory`]]: `inventory` answers *what is installed*; `identity` answers *who and where this is*.

`identity` is a **canonical, un-namespaced base type** (`merge: invariant`) — promoted from a node-local extension by [[../../what/decisions/adr_035_inventory_identity_base_entity_types|ADR-035]] (aDNA standard v2.3). The canonical reference implementation lives at `Home.aDNA/who/identity/`; this directory in `aDNA.aDNA` demonstrates the type it documents (Standing Order #8).

> **Self-referential note.** In a bootstrapped node vault these records carry the machine's real identity. Here in the dev graph this is the genericized scaffold that ships to `.adna/`.

## Directory Structure

```
who/identity/
├── AGENTS.md (this file)
├── identity_node.md + .yaml              # this host's identity (hostname, operator, machine class, persistent UUID)
└── identity_<network>.md + .yaml         # network identity (peer-id, signing-key ref, permissions, role)
```

`node` is the canonical subtype; networked vaults add a network subtype (e.g., `identity_lattice_protocol`), platform deployments add `identity_<platform_deployment>`, and consumer vaults may add `identity_consumer` declaring federation attribution. The directory *is* the type.

## Entry Format

**Filename**: `identity_<subtype>.md` + a paired `.yaml` companion (Compliance Dimension **D9**).

**Required frontmatter**:

```yaml
---
type: identity
subtype: node | <network> | <platform_deployment> | consumer
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
last_edited_by: agent_{username}
tags: [identity, <subtype>]
---
```

Template: [[../../how/templates/template_identity_entry|template_identity_entry]].

## Identity-Drift Discipline

Identity drift is a **high-severity** finding — surfaced by a health check (canonical example: `Home.aDNA`'s `skill_node_health_check`), never auto-corrected:

- **Hostname change** — likely a machine rebuild or rename. Flag; do not auto-update.
- **Operator change** — likely a takeover or shared-machine misconfiguration. Flag `#needs-human`.
- **Persistent-UUID mismatch** — the host was re-bootstrapped or restored from backup. Investigate.
- **Network peer-id rotation** — expected after key rotation; verify against the operator's network-CLI state.

## Privacy

- Hostname, operator, and machine class are persisted (low sensitivity).
- CPU serial, MAC addresses, and OS machine UUIDs are **NOT** persisted (high sensitivity; OS-managed, queried on demand).
- A signing-key **value** is never persisted — only the path/source reference.

## Federation (D7)

Network-facing identity records carry a `federation` block governing opt-in cross-node sharing; default **node-private** (`shareable: false`, `discoverable: false`). Identity is sensitive node-fingerprint data — opt in deliberately.

## Load/Skip Decision

**Load** when: a cross-vault session needs to know which host it runs on; troubleshooting identity drift; reviewing network permissions; running a credentials audit.

**Skip** when: doing work that doesn't depend on host/network identity (most inventory updates, knowledge work).

**Token cost**: ~500 tokens (this AGENTS.md).

## Cross-References

- [[../../what/ontology|what/ontology]] — base ontology (row 16: `identity`)
- [[../../what/decisions/adr_035_inventory_identity_base_entity_types|ADR-035]] — the promotion to a base entity type (standard v2.3)
- [[../../what/inventory/AGENTS|what/inventory]] — the WHAT-leg complement
- [[../../how/templates/template_identity_entry|template_identity_entry]] — entry template (+ `.yaml` companion)
- [[../AGENTS|who/AGENTS]] — organization-layer index
