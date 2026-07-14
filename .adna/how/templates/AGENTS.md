---
type: directory_index
created: 2026-02-19
updated: 2026-07-13
last_edited_by: agent_rosetta
tags: [directory_index, templates]
---

# how/templates/ — Reusable Templates

## Purpose

Templates for all content types in the vault. Each template defines the frontmatter schema, body structure, and naming convention for its target entity type. Templates ensure consistency across files created by different agents and users.

## Template Index

> **30 `template_*.md` total** = 12 auto-triggered + 13 manual-apply + 5 operational. (The Fork-Skeleton Bundle is a directory, not a `template_*.md`, so it sits outside the 30.)

### Auto-Triggered Templates (12)

These templates are applied by Templater when creating a new file in the mapped directory:

| Template | Target Type | Trigger Directory | Frontmatter `type` |
|----------|------------|-------------------|-------------------|
| `template_adr.md` | Architecture Decision Record | `what/decisions/` | `decision` |
| `template_backlog.md` | Backlog idea | `how/backlog/` | `backlog` |
| `template_campaign.md` | Campaign master document | `how/campaigns/` | `campaign` |
| `template_context.md` | Context library file | `what/context/` | `context_research` / `context_guide` / `context_core` |
| `template_coordination.md` | Coordination note | `who/coordination/` | `coordination` |
| `template_inventory_entry.md` | Inventory record (base type) | `what/inventory/` | `inventory` |
| `template_identity_entry.md` | Identity record (base type) | `who/identity/` | `identity` |
| `template_mission.md` | Mission / plan | `how/missions/` | `mission` |
| `template_prd.md` | Product Requirements Document | `how/pipelines/prd_rfc/02_requirements` | `prd` |
| `template_rfc.md` | Request for Comments | `how/pipelines/prd_rfc/03_design` | `rfc` |
| `template_session.md` | Session tracking file | `how/sessions/active/` | `session` |
| `template_skill.md` | Skill recipe or procedure | `how/skills/` | `skill` |

### Manual-Apply Templates (13)

These templates have no Templater auto-trigger. Copy their structure manually or use `Templater: Insert template` command:

| Template | Target Type | Typical Location | Frontmatter `type` | Why No Trigger |
|----------|------------|-----------------|-------------------|----------------|
| `template_aar.md` | After-Action Review (full) | `how/missions/artifacts/` | `artifact` | Artifacts dir contains mixed types |
| `template_aar_lightweight.md` | Lightweight 5-line AAR | any mission/campaign | `template` | Appended to existing files, not standalone |
| `template_campaign_mission.md` | Campaign-linked mission | `how/campaigns/campaign_*/missions/` | `plan` | Campaign missions have campaign-specific fields |
| `template_campaign_claude.md` | Per-campaign CLAUDE.md | `how/campaigns/campaign_*/` | `governance` | Glob patterns not supported by Templater |
| `template_home_claude.md` | Home-class node governance CLAUDE.md (`{{persona}}`/`{{node_hostname}}`/`{{operator}}`/`{{workspace_root}}`) | `Home.aDNA/` (fork-install) | `governance` | Home-class fork install, not a new-file trigger |
| `template_data_record.md` | Generic data record | varies | varies | Generic — no single target directory |
| `template_folder_note.md` | Folder index note | any directory | `folder_note` | Used everywhere, can't map to one folder |
| `template_governance.md` | Governance document | `who/governance/` | `governance` | Governance dir has AGENTS.md + mixed policy docs |
| `template_migration.md` | Version migration prompt | `how/migrations/` | `migration` | Migrations are created per-version, not on new-file trigger |
| `template_registry.md` | Registry publication metadata | varies | `template` | Used for publishing, not regular file creation |
| `template_strategic_compass.md` | Strategic compass | `who/governance/` | `governance` | Rare — governance dir already mapped for other use |
| `template_quest_result.md` | Side-quest result record | `how/quests/` | `quest_result` | Quest dir mixes definitions + results |
| `template_side_quest.md` | Side-quest definition | `how/quests/` | `side_quest` | Quest dir mixes definitions + results |

### Operational / Lifecycle Templates (5)

Vault-agnostic operational templates (manual-apply; not entity-type templates). Added since the original index was written:

| Template | Target Type | Typical Location | Frontmatter `type` |
|----------|------------|-----------------|-------------------|
| `template_disposition_ledger.md` | Workspace-houseclean disposition ledger (§A–H; §C = standing shim registry) | fleet spring-clean (`skill_workspace_spring_clean`) | `disposition_ledger` |
| `template_lattice_home_render.md` | Lattice-home render — vault-agnostic terminal cold-start splash | `Home.aDNA/` / any vault root | `template` |
| `template_ratification_record.md` | Ratification record (ceremony header + per-ADR/decision block) | `what/decisions/` · `how/gates/` | `ratification_record` |
| `template_second_genesis_dossier.md` | Second-genesis intake dossier (9-section read of a stale vault) | new `<Name>.aDNA/` re-genesis intake | `second_genesis_dossier` |
| `template_workspace_claude.md` | Workspace-root router CLAUDE.md (the `~/aDNA/CLAUDE.md` project-routing file) | workspace root (fork / init) | `template` |

### Fork-Skeleton Bundles (1)

Multi-file fork skeletons (not single-file templates; not Templater-triggered). Rendered via the bundle's own `smoke_render.py --materialize DIR`, or installed by a fork skill:

| Bundle | Target Type | Typical Location | Invoked By |
|--------|------------|-----------------|------------|
| `template_node_adna_exemplar/` | Polished node-vault home skeleton (HOME.md + §Gallery/§Topology Bases + persona CSS + canvas generators + Canvas.aDNA `canvasforge/` wrapper) | `<Node>.aDNA/` (fork overlay) | `skill_project_fork --exemplar-home` (P4 wiring); `smoke_render.py --materialize` (upstreamed Hearthstone P3, 2026-06-19) |

## Filled Examples

See `examples/` for completed samples showing what quality output looks like:

| Example | Based on template | Shows |
|---------|------------------|-------|
| `example_context_market_analysis.md` | `template_context.md` | Filled context file with real research, competitive analysis, and anti-patterns |
| `example_mission_product_launch.md` | `template_mission.md` | Completed mission with 5 tasks, status tracking, and completion summary |
| `example_session_customer_research.md` | `template_session.md` | Completed session with activity log, SITREP, and next session prompt |

Use these to understand the expected level of detail before creating your own files.

## Usage Notes

- **Templater integration**: If using Obsidian with the Templater plugin, templates can auto-populate when creating files in their trigger directory
- **Frontmatter first**: Always fill the YAML frontmatter before writing body content — frontmatter drives type detection and search
- **Extend, don't fork**: If you need a variant, add optional fields to the existing template rather than creating a copy
- **`type` field is mandatory**: Every file created from a template must retain the `type` frontmatter field — it's the entity discriminator

## Load/Skip Decision

**Load this directory when**:
- Creating a new file and unsure which frontmatter fields or body structure to use
- Onboarding and learning what entity types the vault supports
- Modifying template conventions across the vault (Tier 2 session recommended)

**Skip when**:
- Already know which template to use and remember the required fields
- Working with existing files that already have correct frontmatter
- Performing non-creation tasks (reading, analyzing, searching)

**Token cost**: ~400 tokens (this AGENTS.md). Individual templates are ~50-150 lines each.

## Cross-References

- [how/AGENTS](../AGENTS.md) — Operations layer index
- [what/context/AGENTS](../../what/context/AGENTS.md) — Context library (uses `template_context.md`)
- [how/sessions/AGENTS](../sessions/AGENTS.md) — Session protocol (uses `template_session.md`)
- [how/missions/AGENTS](../missions/AGENTS.md) — Mission protocol (uses `template_mission.md`)
- [how/campaigns/AGENTS](../campaigns/AGENTS.md) — Campaign protocol (uses `template_campaign.md`)
- [how/skills/AGENTS](../skills/AGENTS.md) — Skills protocol (uses `template_skill.md`)
