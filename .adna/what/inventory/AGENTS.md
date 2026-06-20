---
type: directory_index
created: 2026-06-18
updated: 2026-06-18
last_edited_by: agent_rosetta
tags: [directory_index, inventory]
---

# what/inventory/ — Inventory

## Purpose

The `inventory` base entity type (WHAT leg): the **point-in-time state of what is installed and configured** for this graph's host context — installed `.aDNA` vaults, system/tool state, network memberships, and domain-specific component inventories. It is structurally distinct from the four knowledge-artifact WHAT types (`context` / `decisions` / `modules` / `lattices`): those capture *what you know and have decided*; `inventory` captures *what is actually present on the machine right now*.

`inventory` is a **canonical, un-namespaced base type** (`merge: invariant`) — promoted from a node-local extension by [[../decisions/adr_035_inventory_identity_base_entity_types|ADR-035]] (aDNA standard v2.3). Its WHO-leg complement is [[../../who/identity/AGENTS|`identity`]] (`inventory` = *what's installed*; `identity` = *who/where this is*). The canonical reference implementation lives at `Home.aDNA/what/inventory/`; this directory in `aDNA.aDNA` demonstrates the type it documents (Standing Order #8 — the structure is the lesson).

> **Self-referential note.** In a freshly-bootstrapped node vault this directory holds real inventory entries. Here in the standard's dev graph it carries the genericized scaffold only — the same scaffold that ships to `.adna/` so every fork inherits the type.

## Directory Structure

```
what/inventory/
├── AGENTS.md (this file)
├── inventory_vaults.md + .yaml         # installed .aDNA vaults + sibling code repos
├── inventory_system.md + .yaml         # machine class, tool versions, PATH, env-var NAMES, shell/OS
└── inventory_memberships.md + .yaml    # network memberships (federation block lives here)
```

`vaults` / `system` / `memberships` are the canonical node subtypes; domain vaults add their own (e.g., a Platform vault inventorying deployment installs, an IDE vault inventorying installed layers/packages). The directory *is* the type (directory-as-ontology).

## Entry Format

**Filename**: `inventory_<subtype>.md` + a paired `.yaml` companion (Compliance Dimension **D9**).

**Required frontmatter**:

```yaml
---
type: inventory
subtype: vaults | system | memberships | <domain>
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
last_edited_by: agent_{username}
tags: [inventory, <subtype>]
---
```

Template: [[../../how/templates/template_inventory_entry|template_inventory_entry]] (carries the `.md` + paired `.yaml` companion skeleton).

## Companion Discipline (D9)

Every entry is markdown-canonical with a paired `.yaml` companion: the `.md` is the human/agent narrative; the `.yaml` is the machine-readable projection. Write both atomically and keep them in sync — a refresh skill regenerates both from current state.

## Federation (D7)

Only **network-facing** records (e.g., `inventory_memberships.yaml`) carry a `federation` block governing opt-in cross-node sharing. Default posture is **node-private**: `shareable: false`, `discoverable: false` — opt in deliberately, never by default. All other inventory files are node-private with no federation block.

## Refresh & Validation

Inventory drifts from reality the moment something is installed, removed, or upgraded — so it is refreshed, not hand-maintained:

- A **refresh skill** rebuilds these files from current host state (run after installing/uninstalling a vault, upgrading toolchain, or on a schedule). Canonical example: `Home.aDNA`'s `skill_inventory_refresh`.
- A **health check** validates inventory-vs-disk consistency and surfaces drift as a reproducibility (D10) finding. Canonical example: `Home.aDNA`'s `skill_node_health_check`.

## Load/Skip Decision

**Load** when: querying installed vaults/components, running a health check, refreshing inventory, or troubleshooting drift between recorded inventory and actual state.

**Skip** when: doing knowledge or operational work that doesn't depend on what's installed.

**Token cost**: ~500 tokens (this AGENTS.md).

## Cross-References

- [[../ontology|what/ontology]] — base ontology (row 15: `inventory`)
- [[../decisions/adr_035_inventory_identity_base_entity_types|ADR-035]] — the promotion to a base entity type (standard v2.3)
- [[../../who/identity/AGENTS|who/identity]] — the WHO-leg complement
- [[../../how/templates/template_inventory_entry|template_inventory_entry]] — entry template (+ `.yaml` companion)
- [[../AGENTS|what/AGENTS]] — knowledge-layer index
