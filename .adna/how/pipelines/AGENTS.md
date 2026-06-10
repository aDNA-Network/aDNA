---
type: directory_index
created: 2026-02-17
updated: 2026-02-19
last_edited_by: agent_init
tags: [directory_index, pipeline]
---

# Pipelines — Content-as-Code Workflows

## Purpose

Pipelines implement the **content-as-code** paradigm: folder-based workflows where a file's location IS its state. Instead of tracking status in frontmatter or databases, files flow through stage directories. Each stage has its own `AGENTS.md` with instructions.

## Paradigm

```
A file's location in the directory tree IS its pipeline state.
```

- **No status field needed** — the directory name tells you the stage
- **Movement = state transition** — moving a file to the next directory advances it
- **AGENTS.md = stage instructions** — each stage directory contains agent instructions
- **Quality gates** — each stage defines criteria that must be met before advancement

## Available Pipelines

| Pipeline | Stages | Purpose |
|----------|--------|---------|
| `prd_rfc/` | 4 (research → requirements → design → review) | R&D → PRD → RFC product planning |

## Pipeline Index

### prd_rfc/ — Product Planning Pipeline

```
how/pipelines/prd_rfc/
├── AGENTS.md              # Pipeline overview and entry point
├── 01_research/           # Problem space exploration
│   ├── AGENTS.md          # Stage instructions
│   └── (input files)
├── 02_requirements/       # PRD authoring
│   ├── AGENTS.md          # Stage instructions
│   └── (research → PRD)
├── 03_design/             # RFC authoring
│   ├── AGENTS.md          # Stage instructions
│   └── (PRD → RFC)
└── 04_review/             # Final approval
    ├── AGENTS.md          # Stage instructions
    └── (PRD+RFC package)
```

**Output**: Approved PRD + RFC documents committed to campaign `planning/` dirs or `04_review/` committed

## Creating New Pipelines

To add a new pipeline:

1. Create a directory under `how/pipelines/` named for the workflow
2. Create numbered stage subdirectories (`01_name/`, `02_name/`, etc.)
3. Write an `AGENTS.md` in each stage with processing instructions
4. Write a pipeline-level `AGENTS.md` with overview and entry point
5. Document the pipeline in this index

## Rules

- **File location = state** — never track pipeline state in frontmatter when the directory structure already captures it
- **Stage AGENTS.md is authoritative** — agents follow the stage instructions, not general intuition
- **Quality gates are mandatory** — files must meet stage exit criteria before advancing
- **Human gates are human gates** — stages marked as mandatory human review must never be auto-approved

## Load/Skip Decision

**Load this directory when**:
- Starting or continuing a content-as-code workflow (e.g., R&D→PRD→RFC planning)
- Creating a new pipeline type for a repeatable folder-based workflow
- Understanding the "file location = state" paradigm before building pipeline stages

**Skip when**:
- No active pipeline runs and not creating a new pipeline
- Working on missions, sessions, or backlog outside of pipeline context
- Already inside a specific pipeline — load that pipeline's AGENTS.md directly

**Token cost**: ~600 tokens (this AGENTS.md)

## Cross-References

- [how/pipelines/prd_rfc/AGENTS](prd_rfc/AGENTS.md) — Product planning pipeline
- [how/missions/AGENTS](../missions/AGENTS.md) — Mission protocol (pipelines feed into missions)
- [how/templates/AGENTS](../templates/AGENTS.md) — Templates used within pipeline stages
