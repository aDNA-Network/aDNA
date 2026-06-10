---
type: directory_index
created: 2026-02-18
updated: 2026-05-14
last_edited_by: agent_stanley
tags: [directory_index, skill]
---

# how/skills/ — Agent Reference

## Purpose

Reusable procedures and capabilities — both agent-automated recipes and documented human/hybrid processes. This directory consolidates all "how to do X" knowledge into a single location.

## What is a Skill?

A skill is a documented, reusable capability that can be executed by an AI agent, a human, or both. Skills encapsulate:
- **Trigger conditions** — when to invoke the skill
- **Required inputs** — what the skill needs to run
- **Execution steps** — the procedure to follow
- **Expected outputs** — what the skill produces

## Skill Types

| Type | Description | Format |
|------|-------------|--------|
| `agent` | Automated agent recipe — encapsulated automation capability | Single-file: `skill_[name].md` |
| `process` | Documented human or hybrid procedure for recurring operations | Single-file or directory-based: `skill_[name].md` or `[name]/AGENTS.md` |

**Discriminator**: `skill_type` frontmatter field (`agent` or `process`)

## Skills vs. Lattices

Skills (`how/skills/`) are Markdown procedures — step-by-step instructions an agent reads and follows. Lattices with `lattice_type: skill` (`what/lattices/`) are executable YAML directed graphs. **Start with a skill file.** Promote to a lattice when you need registry publishing, runtime execution, or composition with other lattices. Promotion workflow: `skill_lattice_publish.md`. Full comparison: [`what/docs/standard_reading_guide.md` §4](../../what/docs/standard_reading_guide.md#4-skill-vs-lattice-when-to-use-which).

## Skills as Runbooks

Skills can serve as operational runbooks — not just automated recipes, but documented procedures that an operator follows step-by-step. Examples: `skill_l1_upgrade.md` (phased compute upgrade), `skill_workspace_init.md` (workspace bootstrap). When writing a skill as a runbook, include verification steps after each phase so the operator can confirm progress.

## Skill Categories

| Category | Description |
|----------|-------------|
| `setup` | Machine setup, environment configuration |
| `research` | Information gathering and analysis |
| `development` | Code and documentation generation |
| `operations` | Operational tasks and maintenance |
| `communication` | Messaging and reporting |
| `data` | Data processing, export, transformation |
| `onboarding` | Customer, partner, or team onboarding |
| `review` | Model review, code review, audit |
| `emergency` | Incident response and emergency procedures |
| `node_operations` | Per-node operational maintenance (inventory refresh, health checks, credential audits, cross-vault git pulls) — typically invoked from `LatticeHome.aDNA/` operator persona |

## Directory Structure

```
how/skills/
├── AGENTS.md                    # This file (protocol)
├── skill_[name].md              # Single-file skills (agent or process)
├── [name]/                      # Directory-based skills (complex processes)
│   ├── AGENTS.md                # Process operational manual
│   └── ...                      # Phase directories, configs, templates
└── archive/                     # Deprecated skills
```

## Naming Convention

Pattern: `skill_[name].md`

Examples:
- `skill_machine_setup.md` (agent)
- `skill_create_deck.md` (agent)
- `skill_customer_onboarding.md` (process)
- `skill_incident_response.md` (process)
- `skill_lattice_publish.md` (agent)
- `skill_context_quality_audit.md` (agent)
- `skill_context_graduation.md` (agent)
- `skill_version_migration.md` (agent)
- `skill_workspace_upgrade.md` (agent)
- `skill_vault_review.md` (process)
- `skill_node_bootstrap_interview.md` (agent) — hybrid 19-question interview filling operator-specific fields of a freshly-forked `LatticeHome.aDNA/` (invoked from workspace router Step 0.3 between `skill_inventory_refresh` auto-detect and `skill_node_health_check` validation; Hestia voice; 4-7 min runtime)
- `skill_inventory_refresh.md` (agent) — rebuild `inventory_vaults.{md,yaml}` + `inventory_system.{md,yaml}` from current node state; detect new/removed vaults + version drift + tool-chain drift (graduated from LatticeHome.aDNA@411660e at M-H.1.5)
- `skill_node_credentials_audit.md` (agent) — enumerate credential SOURCES on a node (env-var NAMES, gh CLI auth status, SSH pubkeys, keychain entry NAMES). NAMES-only discipline; never persists values (graduated at M-H.1.5)
- `skill_node_health_check.md` (agent) — D10 reproducibility gate for `LatticeHome.aDNA/`; validates file presence + frontmatter + YAML companion + federation block + inventory-vs-disk consistency + identity drift (graduated at M-H.1.5)
- `skill_update_all_vaults.md` (agent) — `git pull --ff-only` across every vault listed in `inventory_vaults.yaml`; safe-by-default + flags conflicts as `#needs-human` (graduated at M-H.1.5)

## Template

Use `how/templates/template_skill.md` to create new skill files.

## Required Frontmatter

```yaml
---
type: skill
skill_type: agent|process
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active|draft|deprecated
category: setup|research|development|operations|communication|data|onboarding|review|emergency
trigger: <when to invoke>
last_edited_by: agent_<username>
tags: []
---
```

## Load/Skip Decision

**Load this directory when**:
- Invoking an existing skill by name (read the specific skill file, not all skills)
- Creating a new skill — check naming conventions, categories, and template reference
- Modifying or extending an existing skill's procedure
- Onboarding — learning what automated capabilities and documented procedures exist

**Skip when**:
- Performing routine session work that doesn't involve skill invocation or creation
- Working on missions, campaigns, or pipelines that don't reference skills
- Already know the skill file path and can load it directly

**Token cost**: ~700 tokens (this AGENTS.md). Individual skill files vary widely (50-400 lines).
