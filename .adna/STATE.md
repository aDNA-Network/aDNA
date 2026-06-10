---
type: state
created: 2026-02-17
updated: 2026-04-03
status: active
last_edited_by: agent_init
last_session: session_example_20260402_identity_rename
tags: [state, governance]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

## Current Phase

**Production-validated.** Agentic-DNA v7.0 with hardened object standards, Canvas Standard v1.0.0, execution hierarchy v2 (OODA + AAR), 15 example lattices, community infrastructure (contribution system, side-quests, vision document), and the v7.0 repo flatten + airlock template stub (campaign_adna_v2_infrastructure M03 2026-05-11). aDNA Standard v2.2 (maintenance pass complete). Identity rename from `adna` to `Agentic-DNA` complete (display name `Agentic-DNA`; repo URL slug `LatticeProtocol/adna` per ADR-006 v7.0 GitHub repo rename).

## What's Working

- aDNA triad deployed (what/how/who, 5 governance files, 14 base entity types)
- Object standards hardened: module, dataset, lattice (targets as dataset subtype)
- Canvas Standard v1.0.0 with Round-Trip Protocol v1.0 (YAML authoritative, canvas as view layer)
- Type vocabulary: 19 canonical I/O types (Decision 10)
- FAIR metadata: flat↔nested envelope interconversion (Decision 11)
- `.dataset.yaml` schema: multi-cloud storage, 7 providers, FUSE support (Decision 12)
- Lattice YAML validation tool (`lattice_validate.py`) + JSON Schema
- Canvas-YAML bidirectional conversion (`lattice2canvas.py`, `canvas2lattice.py`)
- 15 example lattice files + 3 canvas templates + 1 demonstration canvas
- Context library: 5 topics, 27 subtopics, ~75K tokens (prompt_engineering, adna_core, claude_code, lattice_basics, object_standards)
- Sync protocol: vault↔repo `adna_core/` sync (backlog: formal sync skill not yet created)
- Cross-topic recipe system: 6 domain-neutral recipes with 3-tier budgets
- Execution hierarchy v2: OODA cascade (3-level), AAR protocol (5-step), mission classes (5 types)
- Quality framework: 6-axis rubric, quality audit skill, context graduation pipeline
- Strategic compass template + escalation cascade (session→mission→campaign→STATE.md)
- 22 templates including AAR, lightweight AAR, campaign mission, strategic compass, campaign CLAUDE.md, registry, data record, folder note, PRD, RFC, migration, side quest, quest result
- R&D→PRD→RFC planning pipeline (4 stages)
- Agent-driven onboarding (`how/skills/skill_onboarding.md`) — runs in forked projects, not base template
- Template detection + project fork flow (`role: template` in MANIFEST.md, `skill_project_fork.md`)
- `~/aDNA/` workspace convention for L0 node bootstrap
- 13 skills (project fork, onboarding, workspace init, L1 upgrade, lattice publish, new entity type, context quality audit, context graduation, vault review, upstream contribution, version migration, sqlite persistence, orchestration tiers)
- Session tracking, mission/campaign/backlog systems
- 10 CSS snippets for Obsidian visual polish
- CHANGELOG.md with version policy and migration cross-links
- CONTRIBUTING.md with Agent Contribution Mode (organic upstream contribution)
- Upstream contribution skill (`how/skills/skill_upstream_contribution.md`)
- Side-quest infrastructure: quest specs, result templates, aggregation tool (`how/quests/`, `what/lattices/tools/`)
- `who/governance/VISION.md` — decentralized frontier lab model with participation ladder

## Recent Decisions

| Date | Decision | Source |
|------|----------|--------|
| 2026-03-02 | Decision 9: YAML authoritative, canvas is view layer | campaign_adna_lattice M08 |
| 2026-03-02 | Decision 10: 19-type I/O vocabulary | campaign_adna_lattice M16 |
| 2026-03-02 | Decision 11: Nested FAIR canonical, flat FAIR transport | campaign_adna_lattice M16 |
| 2026-03-02 | Decision 12: Multi-cloud `.dataset.yaml` with FUSE | campaign_adna_lattice M16 |

## Recent Upgrades

| Date | Upgrade | Source |
|------|---------|--------|
| 2026-04-03 | v6.0 validation pass — template count 20→22, example count 16→15, CHANGELOG expanded (M05-M07), schema/validator/spec aligned | campaign_arih M08-M09 |
| 2026-04-03 | CLAUDE.md v6.0 — Agentic-DNA identity rename, .aDNA convention, vault backport, III findings, count reconciliation | campaign_arih M04-M07 |
| 2026-03-20 | CLAUDE.md v5.5 — VISION.md, ecosystem section in README, governance file coherence pass | campaign_adna_ecosystem_evolution M15 |
| 2026-03-20 | CLAUDE.md v5.4 — side-quest infrastructure, quest/result templates, aggregation tool | campaign_adna_ecosystem_evolution M14 |
| 2026-03-20 | CLAUDE.md v5.3 — CONTRIBUTING.md, Agent Contribution Mode, upstream contribution skill | campaign_adna_ecosystem_evolution M13 |
| 2026-03-19 | CLAUDE.md v5.2 — CHANGELOG.md, version policy, migration cross-links | campaign_adna_ecosystem_evolution M12 |
| 2026-03-18 | CLAUDE.md v5.1 — lattice types table (7 values), template count (17), standard file path fixes | campaign_adna_comprehensive_review M08 |
| 2026-03-18 | aDNA Standard v2.2 — federation stub, vault extensions, campaign system, factual fixes | campaign_adna_comprehensive_review M07 |
| 2026-03-18 | Repo sync complete: 13 adna_core subtopics (was 10), 3 new files from vault sync | campaign_adna_comprehensive_review M01 |
| 2026-03-18 | README quickstart refined, FAQ section, plugin tiers documented | campaign_adna_comprehensive_review M03 |
| 2026-03-18 | Quality floor remediation: lattice_basics 3.0→4.0, object_standards 3.4→4.0 | campaign_adna_comprehensive_review M04 |
| 2026-03-17 | CLAUDE.md v5.0 — OODA cascade, AAR protocol, escalation cascade, context recipes | Framework port from lattice-labs |
| 2026-03-17 | 10 adna_core subtopics (was 8) — added ooda_cascade, ontology_workshop | Framework port |
| 2026-03-17 | Quality scoring on all 18 context files — 3 floor violations identified | Quality audit |
| 2026-03-17 | 4 new templates, 2 new skills, mission class discriminator | Framework port |

## Active Blockers

None.

## Next Steps

1. **Clone into `~/aDNA/`** — `mkdir -p ~/aDNA && cd ~/aDNA && git clone https://github.com/LatticeProtocol/aDNA.git adna`
2. **Run Claude Code** in `~/aDNA/adna/` — the agent detects this is the base template, creates your workspace, and helps fork your first project
3. **Or customize manually** — fork `adna/` to a project directory, edit MANIFEST.md, STATE.md, and CLAUDE.md § Identity with your project identity
4. **Extend the ontology** — add domain-specific directories under who/what/how (see README § Extending the Ontology, or load `ontology_workshop` context)
5. **Explore the context library** — read `what/context/AGENTS.md` for topic index, or check `context_recipes.md` for pre-built assemblies
6. **Build a lattice** — copy an example from `what/lattices/examples/` and customize it

## Partial-Resume Detection

**Template** (`role: template` in MANIFEST.md): This is the base template. It should never enter partial-resume state — onboarding runs in forked projects, not here.

**Forked project** (no `role` field): If session history is non-empty but MANIFEST.md still shows `last_edited_by: agent_init`, onboarding was started but governance was not customized. Read `how/skills/skill_onboarding.md` and resume from the first step that hasn't produced output (check for customized MANIFEST.md, personalized CLAUDE.md § Identity, and updated STATE.md).
