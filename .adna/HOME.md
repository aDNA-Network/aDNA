---
type: home_page
node: "{{node_hostname}}"
operator: "{{operator}}"
persona: "{{persona}}"
governance: CLAUDE.md
data_source: what/inventory/inventory_vaults.yaml
updated: "{{interview_date}}"
last_edited_by: "agent_{{operator}}"
tags: [home, lattice_home, gallery, "{{persona_lower}}", node_adna]
---

# Lattice — {{node_hostname}} (operator: {{operator}})

> The integrated control plane for this node's lattice. {{persona}} lives here ([[CLAUDE]]). Use this page to browse the catalog of context graphs on this machine, jump into specific vaults, and link out to the marketplace.

| | |
|---|---|
| **Node** | `{{node_hostname}}` |
| **Operator** | `{{operator}}` |
| **Machine class** | {{machine_class}} |
| **Persona** | {{persona}} |
| **Workspace root** | `{{workspace_root}}` |
| **Vault count** | {{vault_count}} `.aDNA` + {{named_project_count}} named projects |
| **Drift entries** | {{drift_count}} (see §Drift below) |
| **Last inventory refresh** | {{last_inventory_refresh}} |
| **Governance** | [[CLAUDE]] · [[MANIFEST]] · [[STATE]] · [[CHANGELOG]] |

Counts and entries are sourced from `./what/inventory/inventory_vaults.yaml`. Refresh via `how/skills/skill_inventory_refresh.md`.

---

## Context Graphs ({{vault_count}} `.aDNA` vaults)

Grouped by aDNA class. Click a vault name to open it in a file manager; from there, "Open with Obsidian" to enter that vault as its own session.

{{vaults_table}}

<!--
  The vaults_table placeholder above is substituted at interview-time by skill_node_bootstrap_interview.md.
  Format: markdown tables grouped by aDNA class — Forges / Frameworks / Platforms /
  Org-Vaults / Documents-Knowledge-Tooling-Workspace-Standard / Superseded.
  Each row: [vault](relative-path) · Persona · Notes. Empty-inventory case shows only
  this Home.aDNA row and adds a Next Steps section linking to skill_project_fork.md.
-->

---

## Named Projects ({{named_project_count}} grandfathered)

{{named_projects_table}}

<!--
  The named_projects_table placeholder format: rows of [project](relative-path) · Type · Sibling for · Notes.
  If named_project_count is 0, this section renders "No named projects on this node yet."
-->

---

## Drift ({{drift_count}} entries — items in the workspace that don't match the canonical inventory)

{{drift_table}}

<!--
  The drift_table placeholder format: rows of Path · Reason · Action required.
  Drift is surfaced here so it stays visible at-a-glance during operator sessions.
  If drift_count is 0, this section renders "No drift detected — node inventory matches workspace state."
-->

Triage and resolution belong in node-operational campaigns or the aDNA standard's review pass.

---

## Marketplace

[Lattice Protocol marketplace](https://lattice-protocol.com/marketplace) — discover, publish, and federate context graphs across the LP network.

> _Link target may be a `[TBD per LP marketplace launch]` placeholder until the marketplace is live. Update this section when the destination is confirmed._

---

## Tools & quick nav

### Personae on this node
- [[CLAUDE|{{persona}} (this node)]] — per-node operational vault (you are here)
- See `./what/inventory/inventory_vaults.yaml` `personae` block for other personae on this node (each vault carries its own persona; this list is rendered into the vaults table above)

### Node-skills ({{persona}}'s domain)
- [[how/skills/skill_node_health_check|skill_node_health_check]] — validate full vault state (D10 reproducibility gate)
- [[how/skills/skill_update_all_vaults|skill_update_all_vaults]] — `git pull --ff-only` across every installed vault
- [[how/skills/skill_inventory_refresh|skill_inventory_refresh]] — rebuild `inventory_*.md` from current node state and refresh this gallery
- [[how/skills/skill_node_credentials_audit|skill_node_credentials_audit]] — enumerate credential sources (NAMES ONLY, redaction-aware)

### Inventory data sources
- [[what/inventory/inventory_vaults|inventory_vaults.md]] · `inventory_vaults.yaml` — vaults + named projects + drift (this gallery reads here)
- [[what/inventory/inventory_system|inventory_system.md]] · `inventory_system.yaml` — machine class + tool versions + env-var names
- [[what/inventory/inventory_memberships|inventory_memberships.md]] · `inventory_memberships.yaml` — LatticeProtocol network memberships + federation block

---

{{next_steps_section}}

<!--
  The next_steps_section placeholder renders ONLY when inventory_vaults.yaml has 0 .aDNA vaults
  beyond this newly-forked Home.aDNA (i.e., empty-inventory case). It links the
  operator to skill_project_fork.md for forking their first non-node vault.
  When there are existing vaults, this section is empty (renders as nothing).
-->

## Maintenance

When inventory changes (new vault forked, vault removed, drift resolved):

1. Run `skill_inventory_refresh.md` to rebuild `what/inventory/inventory_vaults.{md,yaml}` from current node state.
2. Re-render this HOME.md gallery — either manually edit the tables above, or extend `skill_inventory_refresh.md` to regenerate the tables from the YAML.
3. Commit the refreshed inventory and HOME.md in a single node-operational session.

The gallery is intentionally a **static markdown view** of inventory state so it renders in any Obsidian build regardless of Bases plugin schema. If the operator later wires Obsidian Bases against this YAML, the tables here can become a fallback under the dynamic view.

---

> _This is the lattice-home gallery for this node. The role expansion pattern is documented at the standard level (see `aDNA.aDNA/what/decisions/`); see [[MANIFEST]] and [[STATE]] for vault identity + operational state._

<!--
  TEMPLATE NOTES (this comment block stays in `.adna/HOME.md` but skill_node_bootstrap_interview.md
  strips it during fork-time substitution; the substituted HOME.md in a fresh Home.aDNA/ does not
  include these notes):

  Substitution points (all `{{VARS}}` are filled at fork-time by
  skill_node_bootstrap_interview.md Step 9):

  - {{node_hostname}}        ← `hostname -s` (or operator U1 override)
  - {{operator}}             ← interview U1
  - {{operator_lower}}       ← {{operator}} lowercased for tags
  - {{machine_class}}        ← interview H1
  - {{persona}}              ← `Hestia` (constant for Home.aDNA class)
  - {{persona_lower}}        ← `hestia`
  - {{workspace_root}}       ← `pwd -P` parent (or `$LATTICE_ROOT`)
  - {{vault_count}}          ← derived from inventory_vaults.yaml count
  - {{named_project_count}}  ← derived from inventory_vaults.yaml count
  - {{drift_count}}          ← derived from inventory_vaults.yaml drift section
  - {{last_inventory_refresh}} ← inventory_vaults.yaml `updated:` field
  - {{interview_date}}       ← interview-run date (YYYY-MM-DD)
  - {{vaults_table}}         ← markdown tables grouped by aDNA class
  - {{named_projects_table}} ← markdown table or "No named projects on this node yet."
  - {{drift_table}}          ← markdown table or "No drift detected..."
  - {{next_steps_section}}   ← Next Steps block when inventory is empty; nothing otherwise

  Empty-inventory case (new operator who has not forked any .aDNA/ vaults yet beyond
  this Home.aDNA):
  - {{vaults_table}} shows only the Home.aDNA row
  - {{named_projects_table}} shows "No named projects on this node yet."
  - {{drift_table}} shows "No drift detected..."
  - {{next_steps_section}} renders:

    ## Next Steps

    You're set up. The next thing most operators do is fork their first vault:
    - Run `.adna/how/skills/skill_project_fork.md` (or invoke it through your agent — e.g., "fork a new project called X")
    - Pick a name following ADR-009 (`<name>.aDNA/`, snake_case, single-word lowercase OK)
    - The new vault becomes a new row in the gallery above on next inventory refresh

  Pattern reference: `Home.aDNA/HOME.md` on the canonical reference node is the live working
  example this template was extracted from (M-LWX-02 close 2026-05-12).
-->
