---
type: manifest
role: template
created: 2026-02-17
updated: 2026-04-03
last_edited_by: agent_init
tags: [manifest, governance]
---

# Agentic-DNA — Project Manifest

## Project Identity

<!-- CUSTOMIZE THIS: Replace the description below with your project's name and purpose. -->
<!-- Example: "**my-project** — AI-powered market research platform for B2B SaaS companies." -->

**Agentic-DNA** — A standalone knowledge architecture for building personal lattices and knowledge graphs. Designed for both humans (via Obsidian) and AI agents (via Claude Code). aDNA is the foundational building block of the Lattice federated computing protocol.

This repo is a self-contained aDNA deployment that anyone can clone and immediately start using. It includes templates, tools, example lattices, and the operational infrastructure (sessions, missions, campaigns) needed to run an AI-native project from day one.

## Architecture

This project uses the **aDNA (Agentic DNA)** knowledge architecture — a bare triad deployment.

```
Agentic-DNA/
├── what/        # WHAT — Knowledge objects, context library, lattice tools
├── how/         # HOW — Plans, sessions, templates, pipelines
├── who/         # WHO — People, teams, coordination, governance
│                # Community infrastructure lives inside the triad:
│                #   how/quests/          — quest specs + results
│                #   what/lattices/tools/ — aggregation scripts
```

| Layer | Question | Contains |
|-------|----------|----------|
| **what/** | WHAT does this project know? | Context library (5 topics, 27 subtopics), decisions, aDNA docs, lattice YAML tools + schema + examples |
| **how/** | HOW does this project work? | Missions, sessions, 22 templates, 13 skills, backlog, campaigns, PRD/RFC pipeline |
| **who/** | WHO is involved? | People, teams, coordination, governance |

### Base Ontology

14 entity types across 3 triad legs: WHO (3: governance, team, coordination), WHAT (4: context, decisions, modules, lattices), HOW (7: campaigns, missions, sessions, templates, skills, pipelines, backlog). Extend by adding domain-specific entities under the appropriate leg (e.g., `what/experiments/`). Full table: see CLAUDE.md § Domain Knowledge.

## Entry Points

| Audience | Start Here | Then |
|----------|-----------|------|
| **Agents** | `CLAUDE.md` (auto-loaded) | `STATE.md` → `how/sessions/active/` → work |
| **Humans** | `README.md` | `MANIFEST.md` → browse triad → `STATE.md` |

## Key Components

### Context Library

| Topic | Subtopics | Tokens | Location |
|-------|-----------|--------|----------|
| Prompt Engineering | 7 | ~21K | `what/context/prompt_engineering/` |
| aDNA Core | 13 | ~35K | `what/context/adna_core/` |
| Claude Code | 4 | ~12K | `what/context/claude_code/` |
| Lattice Basics | 2 | ~4.5K | `what/context/lattice_basics/` |
| Object Standards | 1 | ~3K | `what/context/object_standards/` |

Cross-topic recipes: `what/context/context_recipes.md` (6 domain-neutral recipes, 3-tier budget system).

Load via `what/context/AGENTS.md` → topic `AGENTS.md` → individual subtopics as needed.

### Lattice YAML Tools

| Tool | Location | Purpose |
|------|----------|---------|
| `lattice_validate.py` | `what/lattices/tools/` | Validate `.lattice.yaml` against JSON Schema |
| `lattice2canvas.py` | `what/lattices/tools/` | Convert lattice YAML → Obsidian canvas |
| `canvas2lattice.py` | `what/lattices/tools/` | Convert Obsidian canvas → lattice YAML |
| `lattice_yaml_schema.json` | `what/lattices/` | JSON Schema for lattice definitions |

### Planning Pipeline

```
how/pipelines/prd_rfc/
├── 01_research/      → Problem space exploration
├── 02_requirements/  → PRD authoring (human gate)
├── 03_design/        → RFC authoring
└── 04_review/        → Final approval (human gate)
```

### Templates (22)

| Template | Auto-triggers in |
|----------|-----------------|
| `template_session.md` | `how/sessions/active/` |
| `template_mission.md` | `how/missions/` |
| `template_context.md` | `what/context/` |
| `template_adr.md` | `what/decisions/` |
| `template_coordination.md` | `who/coordination/` |
| `template_backlog.md` | `how/backlog/` |
| `template_campaign.md` | `how/campaigns/` |
| `template_campaign_mission.md` | `how/campaigns/campaign_*/missions/` |
| `template_prd.md` | `how/pipelines/prd_rfc/02_requirements/` |
| `template_rfc.md` | `how/pipelines/prd_rfc/03_design/` |
| `template_skill.md` | `how/skills/` |
| `template_aar.md` | `how/missions/artifacts/` |
| `template_aar_lightweight.md` | — |
| `template_strategic_compass.md` | `who/governance/` |
| `template_campaign_claude.md` | `how/campaigns/campaign_*/` |
| `template_registry.md` | — |
| `template_data_record.md` | — |
| `template_folder_note.md` | — |
| `template_governance.md` | — |
| `template_migration.md` | `how/migrations/` |
| `template_side_quest.md` | `how/quests/` |
| `template_quest_result.md` | `how/quests/results/` |

## Active Builds

| Component | Status | Description |
|-----------|--------|-------------|
| aDNA Standard v2.2 | Shipped | Core specification — triad, ontology (14 base + 8 extension), sessions, missions, campaigns |
| Context library | Shipped | 5 topics, 27 subtopics, ~75K tokens. Cross-topic recipe system with 6 recipes |
| Lattice YAML tools | Shipped | Validate, convert (YAML↔canvas), JSON Schema, 15 example lattices + 3 canvas templates |
| Mermaid-enhanced spec docs | Shipped | 19 diagrams across 3 aDNA specification documents |
| PRD/RFC pipeline | Shipped | 4-stage planning pipeline (research → requirements → design → review) |
| 22 templates | Shipped | Session, mission, campaign, campaign mission, context, ADR, backlog, coordination, PRD, RFC, skill, AAR, lightweight AAR, strategic compass, campaign CLAUDE.md, registry, data record, folder note, governance, migration, side quest, quest result |
| Execution hierarchy v2 | Shipped | OODA cascade (3-level evaluation loops), AAR protocol, mission classes, escalation cascade |
| Quality framework | Shipped | 10-dimension compliance rubric, quality audit skill, context graduation pipeline |

See `how/missions/` for mission details and `STATE.md` for current operational state.
