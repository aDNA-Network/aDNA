---
type: directory_index
created: 2026-02-17
updated: 2026-02-19
last_edited_by: agent_init
tags: [directory_index, pipeline, requirements]
---

# Stage 2: Requirements — PRD Authoring

## Instructions

Verify research completeness, then author a Product Requirements Document (PRD) using the PRD template. This stage ends with a **mandatory human gate** — the PRD must be approved before design work begins.

### Steps

1. **List** all files in `02_requirements/` (excluding this `AGENTS.md`)
2. **Read** each research file completely
3. **Verify research completeness** — confirm all four quality gate dimensions from Stage 1 are present:
   - Problem defined
   - Prior art surveyed
   - Constraints identified
   - Opportunity assessed

   If any dimension is missing or weak, move the file back to `../01_research/` with a note describing what's needed.

4. **Apply the PRD template** (`how/templates/template_prd.md`):
   - Copy template structure
   - Preserve `project_slug`, `project_title`, and pipeline frontmatter
   - Set `type: prd` and `stage: requirements`

5. **Author PRD sections**:
   - **Problem Statement** — distill from research findings
   - **Users & Stakeholders** — who benefits, who's affected
   - **Requirements** — MoSCoW tables with:
     - Unique IDs: `REQ-{SLUG}-{NNN}` (e.g., `REQ-TV-001`)
     - Priority: Must / Should / Could / Won't
     - Acceptance criteria for each requirement
   - **Scope** — explicit in/out boundaries
   - **Dependencies** — other systems, teams, or work affected
   - **Success Metrics** — measurable outcomes
   - **Timeline** — target dates or phase alignment
   - **Open Questions** — unresolved items flagged for review

6. **Update pipeline frontmatter**:
   ```yaml
   stage: requirements
   ```

7. **Present PRD for human approval** — this is a **mandatory human gate**

### Human Gate: PRD Approval

**MANDATORY** — No file advances to `03_design/` without explicit user approval.

When presenting the PRD for review:

```
## PRD Review: {project_title}
- **Project**: {project_slug}
- **Priority**: {priority}
- **Requirements count**: {N} Must, {N} Should, {N} Could
- **Scope**: {brief in/out summary}
- **Open questions**: {count}

Key requirements:
- REQ-{SLUG}-001: {summary}
- REQ-{SLUG}-002: {summary}
- ...

[Approve / Revise / Reject]
```

On approval:
- Set `approved_by` and `approved_date` in frontmatter
- Move to `../03_design/`

On revision:
- Apply requested changes
- Re-present for approval

On rejection:
- Move back to `../01_research/` with feedback
- Set `stage: research`

### Quality Gate

**Every PRD must have:**
- All MoSCoW requirement IDs assigned (no unnumbered requirements)
- Acceptance criteria defined for every MUST requirement
- Scope explicitly bounded (in/out lists)
- At least one success metric defined
- Open questions section present (even if empty)

### Edge Cases

- **Requirements that can't be quantified**: Use qualitative acceptance criteria rather than leaving criteria blank.
- **Scope creep during authoring**: If PRD authoring reveals the project is larger than initially scoped, note this in Open Questions and flag to the user during the human gate.
- **Multiple stakeholders**: List all in Users & Stakeholders. If stakeholders have conflicting needs, document the conflict in Open Questions.
- **Dependency on uncommitted work**: If a requirement depends on another in-flight plan or pipeline item, document the dependency and flag risk.

## Load/Skip Decision

**Load this directory when**:
- A research file has been moved into `02_requirements/` and needs PRD authoring
- Verifying whether a file's research is complete enough to advance from Stage 1
- Reviewing an existing PRD before the human approval gate

**Skip when**:
- No files are present in `02_requirements/` (empty stage)
- Working on files in other pipeline stages (01, 03, 04)
- Performing non-pipeline operational work

**Token cost**: ~800 tokens (this AGENTS.md)
