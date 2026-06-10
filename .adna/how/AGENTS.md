---
type: directory_index
created: 2026-02-17
updated: 2026-03-19
last_edited_by: agent_init
tags: [directory_index, ops]
---

# how/ — Operations (Agent Reference)

## Purpose

`how/` holds operations — the **HOW** of this project. Plans, sessions, templates, and optionally backlog, pipelines, tasks, and skills all live here.

## Subdirectories

| Folder | Purpose | Status |
|--------|---------|--------|
| `missions/` | Build plans for multi-session work | Required |
| `sessions/` | Session tracking and audit trail | Required |
| `templates/` | Reusable templates for all content types | Required |
| `backlog/` | Durable ideation and improvement tracking | Active |
| `campaigns/` | Multi-mission strategic initiatives | Active |
| `pipelines/` | Content-as-code folder workflows | Active |
| `migrations/` | Version migration prompts for upgrading CLAUDE.md versions | Active |
| `skills/` | Reusable agent recipes and documented procedures | Active |

## Key Distinctions

| Type | What It Is | Execution Model |
|------|-----------|----------------|
| **Mission** | Multi-session project decomposed into tasks | Agent sessions with handoff |
| **Campaign** | Multi-mission strategic initiative | Phased execution with user gates |
| **Pipeline** | Folder-based workflow where file location = state | Automated / agent-driven |
| **Skill** | Reusable agent recipe or documented procedure | On-demand invocation |

## Naming

All files follow `type_descriptive_name.md` (underscores only, never hyphens).

## Progressive Loading

**This file is a routing index.** Read it to understand what `how/` contains, then drill into the specific subdirectory relevant to your task. Do not load all subdirectory AGENTS.md files at once — each contains detailed protocol that is only useful when you're working in that domain.

**Recommended loading path**: Root AGENTS.md → `how/AGENTS.md` (this file) → specific subdirectory AGENTS.md

## Load/Skip Decision

**Load this directory when**:
- Orienting on what operational systems exist (missions, campaigns, sessions, pipelines, skills, templates, backlog)
- Deciding which subdirectory to drill into for a specific operational task
- Understanding how the HOW leg connects to WHAT and WHO

**Skip when**:
- Already know which subdirectory you need — go directly to its AGENTS.md
- Working purely in `what/` or `who/` with no operational system interaction
- Mid-session and already oriented on the `how/` structure

**Token cost**: ~400 tokens (this AGENTS.md)

## Cross-References

- [how/missions/AGENTS](missions/AGENTS.md) — Mission protocol
- [how/sessions/AGENTS](sessions/AGENTS.md) — Session lifecycle and tracking
- [how/backlog/AGENTS](backlog/AGENTS.md) — Backlog and ideation protocol
- [how/campaigns/AGENTS](campaigns/AGENTS.md) — Campaign protocol
- [how/migrations/AGENTS](migrations/AGENTS.md) — Version migration registry
- [how/pipelines/AGENTS](pipelines/AGENTS.md) — Pipeline paradigm and index
- [how/skills/AGENTS](skills/AGENTS.md) — Skills protocol
- [how/templates/AGENTS](templates/AGENTS.md) — Reusable templates
- [what/AGENTS](../what/AGENTS.md) — Knowledge objects (WHAT)
- [who/AGENTS](../who/AGENTS.md) — Organization (WHO)
