---
type: directory_index
created: 2026-02-17
updated: 2026-02-19
last_edited_by: agent_init
tags: [directory_index, who]
---

# who/ — Organization (Agent Reference)

## Purpose

`who/` holds organization records — the **WHO** of this project. People, teams, coordination notes, governance policies, and optionally customers, partners, contacts, and communications.

## Subdirectories

| Folder | Purpose | Status |
|--------|---------|--------|
| `coordination/` | Cross-agent ephemeral notes — handoffs, urgency signals | Required |
| `governance/` | Roles, decision authority, policies | Required |

Add project-specific subdirectories as needed (e.g., `customers/`, `partners/`, `contacts/`, `team/`, `communications/`, `roadmap/`).

## Naming

All files follow `type_descriptive_name.md` (underscores only, never hyphens).

## Progressive Loading

**This file is a routing index.** Read it to understand what `who/` contains, then drill into the specific subdirectory relevant to your task. The WHO leg is lightweight — coordination (~400 tokens) and governance (~300 tokens) are the two subdirectories.

**Recommended loading path**: Root AGENTS.md → `who/AGENTS.md` (this file) → specific subdirectory AGENTS.md

## Load/Skip Decision

**Load this directory when**:
- Orienting on what organizational systems exist (coordination, governance, and any project-specific extensions)
- Deciding which subdirectory to drill into for people or governance work
- Understanding how the WHO leg connects to WHAT and HOW

**Skip when**:
- Already know which subdirectory you need — go directly to its AGENTS.md
- Working purely in `what/` or `how/` with no organizational interaction
- Mid-session and already oriented on the `who/` structure

**Token cost**: ~300 tokens (this AGENTS.md)

## Cross-References

- [who/coordination/AGENTS](coordination/AGENTS.md) — Cross-agent coordination protocol
- [who/governance/AGENTS](governance/AGENTS.md) — Governance reference
- [what/AGENTS](../what/AGENTS.md) — Knowledge objects (WHAT)
- [how/AGENTS](../how/AGENTS.md) — Operations (HOW)
