---
type: directory_index
created: 2026-02-17
updated: 2026-02-19
last_edited_by: agent_init
tags: [directory_index, pipeline, design]
---

# Stage 3: Design — RFC Authoring

## Instructions

Author a Request for Comments (RFC) document that translates approved PRD requirements into a concrete technical design. Every design decision must trace back to a PRD requirement.

### Steps

1. **List** all files in `03_design/` (excluding this `AGENTS.md`)
2. **Read** the approved PRD file completely — note `approved_by` and `approved_date` in frontmatter
3. **Verify PRD approval** — confirm `approved_by` is set. If not, move the file back to `../02_requirements/` — design must not begin without PRD approval.
4. **Load relevant context** from `what/context/` — check for topics related to the design domain
5. **Apply the RFC template** (`how/templates/template_rfc.md`):
   - Copy template structure
   - Preserve `project_slug`, `project_title`, and pipeline frontmatter
   - Set `type: rfc`, `stage: design`, and `prd_ref` pointing to the PRD
6. **Author RFC sections**:
   - **Summary** — one-paragraph design overview
   - **Motivation** — why this design, linking back to PRD problem statement
   - **Proposed Design** — the core design:
     - Architecture diagram (Mermaid)
     - Component design with interfaces
     - Data flow and state management
     - API contracts (if applicable)
   - **Requirement Traceability** — table mapping every PRD requirement to specific design elements
   - **Alternatives Considered** — minimum 2 alternatives with pros/cons and reason for rejection
   - **Migration / Rollout** — how to deploy, phase, or migrate
   - **Security & Privacy** — security implications, if any
   - **Testing Strategy** — how to verify the design works
   - **Open Questions** — unresolved design decisions

7. **Update pipeline frontmatter**:
   ```yaml
   stage: design
   ```

8. **Move** completed RFC to `../04_review/` along with its companion PRD file

### Quality Gate

**Every RFC must have:**
- Every MUST and SHOULD requirement from the PRD mapped in the traceability table
- At least 2 alternatives considered with documented rationale for rejection
- Architecture diagram (Mermaid) present
- Migration/rollout plan defined
- Testing strategy defined

A design document without requirement traceability fails the gate — design must demonstrably satisfy requirements.

### Edge Cases

- **Requirements that don't map to design**: If a PRD requirement is process-oriented rather than technical, note it in the traceability table with `N/A — process requirement` and describe how it will be addressed outside the RFC.
- **Design reveals requirement gaps**: If the design process reveals missing requirements, document them in Open Questions and recommend a PRD amendment. Do not add requirements to the RFC that aren't in the PRD.
- **Multiple valid designs**: If two designs are genuinely equivalent, present both in Alternatives Considered and recommend one with rationale. Flag for user decision in review.
- **Dependencies on external systems**: Document external dependencies in the design with version requirements, fallback behavior, and risk assessment.
- **PRD amendment needed**: If design work reveals the PRD needs changes, create a coordination note and pause. Do not proceed with a design that contradicts approved requirements.

## Load/Skip Decision

**Load this directory when**:
- An approved PRD has been moved into `03_design/` and needs RFC authoring
- Loading relevant context from `what/context/` to inform a technical design
- Reviewing RFC quality gates before advancing to Stage 4

**Skip when**:
- No files are present in `03_design/` (empty stage)
- Working on files in other pipeline stages (01, 02, 04)
- Performing non-pipeline operational work

**Token cost**: ~550 tokens (this AGENTS.md)
