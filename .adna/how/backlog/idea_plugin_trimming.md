---
type: backlog_idea
status: planned
priority: high
created: 2026-04-04
last_edited_by: agent_init
tags: [backlog, obsidian, performance, clone-size]
---

# Idea: Obsidian Plugin Trimming

## Problem
15 plugins bundled (13MB, 87% of .obsidian/). Most are cosmetic. New users clone 13MB of plugins they may never use. Clone time and disk space impacted.

## Proposed Solution
Ship only essential plugins (~1.5MB): obsidian-advanced-canvas + templater-obsidian + optionally obsidian-tasks-plugin. Document remaining 12 as optional. Update setup.sh. **Co-executor must test Obsidian UX after trimming.**

## Origin
campaign_adna_polish pre-merge efficiency audit. 85% potential size reduction.
