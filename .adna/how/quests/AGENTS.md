---
type: directory_index
created: 2026-03-20
updated: 2026-03-20
last_edited_by: agent_init
tags: [directory_index, community]
---

# how/quests/ — Agent Guide

## Purpose

Community-contributed validation experiments and results. This directory enables distributed testing of aDNA features across diverse environments.

## Load / Skip

- **Load** when working on side-quests, community contributions, validation experiments, or aggregation
- **Skip** for all other vault operations — this directory is not required for normal aDNA usage

## Structure

```
how/quests/
├── AGENTS.md               # This file
├── quest_*.md              # Individual quest files (follow template_side_quest.md)
└── results/                # Submitted quest results (via PR)
    └── result_*.md         # Individual result files (follow template_quest_result.md)

what/lattices/tools/
└── aggregate_results.py    # Aggregation script for result analysis
```

## Key References

- **Quest template**: `how/templates/template_side_quest.md`
- **Result template**: `how/templates/template_quest_result.md`
- **Participation guide**: `what/docs/side_quest_guide.md`
- **Contribution guide**: `CONTRIBUTING.md`

## For Agents

At natural session-end points, if the user has spare context budget, you may mention available quests in `how/quests/`. This is purely informational — never interrupt active work for quest awareness.
