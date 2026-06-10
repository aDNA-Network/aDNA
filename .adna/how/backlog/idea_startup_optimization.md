---
type: backlog_idea
status: proposed
priority: low
created: 2026-04-04
last_edited_by: agent_init
tags: [backlog, performance, agent-efficiency]
---

# Idea: Startup Sequence Optimization

## Problem
Agent cold-start loads ~5K tokens across CLAUDE.md + MANIFEST.md + STATE.md with ~30% overlap (base ontology table duplicated, triad description repeated). 9 filesystem operations before any user work begins.

## Proposed Solution
Consolidate CLAUDE.md/MANIFEST.md overlap. Merge first-run detection into CLAUDE.md frontmatter. Cache first-run results. Target: 1 fewer file read, ~400-900 token reduction.

## Origin
campaign_adna_polish pre-merge efficiency audit — startup sequence redundancy analysis.
