---
type: directory_index
created: 2026-02-17
updated: 2026-02-19
last_edited_by: agent_init
tags: [directory_index, pipeline, research]
---

# Stage 1: Research — Problem Space Exploration

## Instructions

Classify incoming problem statements, feature requests, and backlog ideas. Research the problem space thoroughly. Produce structured research findings that feed into PRD authoring.

### Steps

1. **List** all files in `01_research/` (excluding this `AGENTS.md`)
2. **Read** each input file completely
3. **Assign `project_slug`** — a short, underscored identifier that will thread through all pipeline artifacts (e.g., `topology_validation`, `edge_inference`, `auth_refactor`)
4. **Classify `source_type`**:
   - `backlog_idea` — from `how/backlog/`
   - `feature_request` — from user or stakeholder communications
   - `problem_statement` — identified during work or exploration
5. **Research the problem space**:
   - Define the problem clearly — what's broken, missing, or suboptimal?
   - Survey prior art — how do others solve this? What exists already?
   - Identify constraints — technical, organizational, timeline, resource
   - Assess opportunity — what's the value of solving this?
6. **Load relevant context** from `what/context/` if a relevant topic exists
7. **Add pipeline frontmatter**:
   ```yaml
   ---
   pipeline: prd_rfc
   stage: research
   project_slug: <identifier>
   project_title: "Human-readable title"
   priority: 1 | 2 | 3
   source_type: backlog_idea | feature_request | problem_statement
   source_ref: "path/to/source.md"
   initiated: YYYY-MM-DD
   ---
   ```
8. **Move** completed research file to `../02_requirements/`

### Quality Gate

**All four research dimensions must be addressed before advancing:**

- **Problem defined** — clear statement of what's broken, missing, or suboptimal
- **Prior art surveyed** — at least 2 existing approaches or tools documented
- **Constraints identified** — technical, organizational, and resource constraints listed
- **Opportunity assessed** — value proposition and impact estimate provided

A file with only a problem statement and no research fails the gate.

### Edge Cases

- **Vague inputs**: If the input is too vague to research effectively, add a note requesting clarification and leave the file in `01_research/` with `stage: research_blocked`.
- **Multiple problems in one input**: Split into separate files, one per problem, each with its own `project_slug`. Link them via a `related_projects` frontmatter field.
- **Existing research**: If `what/context/` already contains extensive coverage of this problem domain, summarize and reference it rather than duplicating. Focus research on gaps.
- **Cross-cutting concerns**: If research reveals the problem spans multiple domains, document all dimensions but recommend a primary owner domain.
- **Backlog graduation**: When a backlog idea enters this pipeline, update the backlog idea's status to `in_pipeline` and add `pipeline_ref: prd_rfc/<project_slug>`.

## Load/Skip Decision

**Load this directory when**:
- Processing a file that has been placed in `01_research/` for problem space exploration
- Starting a new R&D→PRD→RFC pipeline run — this is the entry stage
- Checking whether a backlog idea is ready to graduate into the pipeline

**Skip when**:
- No files are present in `01_research/` (empty stage)
- Working on files already in later pipeline stages (02, 03, 04)
- Performing non-pipeline operational work

**Token cost**: ~550 tokens (this AGENTS.md)
