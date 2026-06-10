---
type: directory_index
created: 2026-02-17
updated: 2026-03-03
last_edited_by: agent_init
tags: [directory_index, pipeline, review]
---

# Stage 4: Review — Final Approval & Deliverable Commit

## Instructions

Present the completed PRD+RFC package for final human review. On approval, commit both documents to their destination with pipeline metadata stripped. Optionally create a mission stub.

This is a **mandatory human gate** — no files leave this stage without explicit user approval.

### Steps

1. **List** all files in `04_review/` (excluding this `AGENTS.md`)
2. **Group files by `project_slug`** — a complete package includes one PRD + one RFC with matching slugs
3. **Verify package completeness**:
   - PRD present with `approved_by` set (Stage 2 gate passed)
   - RFC present with traceability table (Stage 3 gate passed)
   - Both files share the same `project_slug`

   If incomplete, identify the missing piece and note which stage needs revisiting.

4. **Present the PRD+RFC package** for final review (see Presentation Format below)
5. **Wait for user decision**:
   - **Approve** → commit to deliverables (step 6)
   - **Revise** → apply corrections, re-present (step 8)
   - **Reject** → return to appropriate stage with feedback (step 9)

### On Approval (commit to deliverables)

6. For each approved package:
   a. **Strip pipeline frontmatter** — remove `pipeline`, `stage`, `source_type`, `source_ref`, `initiated` fields
   b. **Retain document frontmatter** — keep `type`, `project_slug`, `project_title`, `version`, `owner`, `approved_by`, `approved_date`, `created`, `updated`, `last_edited_by`, `tags`
   c. **Determine destination**:
      - **Campaign-linked**: Move PRD and RFC to `how/campaigns/campaign_<name>/planning/`
      - **Standalone**: Files remain in `04_review/` as committed artifacts (set `stage: committed` in frontmatter)
   d. **Remove** pipeline tracking frontmatter from both files
   f. **Log** committed files in the session activity log

7. **Optional: Create mission stub**
   - Ask the user if they want a mission created for this project
   - If yes, create `how/missions/mission_<project_slug>.md` with:
     - Link to PRD and RFC in deliverables
     - Skeleton task list derived from RFC design elements
     - Status: `planned`
   - If no, note that no mission was created

### On Revision

8. Apply the user's corrections directly to the relevant file(s) in `04_review/`. Re-present the updated package for approval (return to step 4).

### On Rejection

9. Determine which stage needs rework:
   - **Requirements issue** → move PRD back to `../02_requirements/` with feedback, move RFC back to `../03_design/`
   - **Design issue** → move RFC back to `../03_design/` with feedback, keep PRD in `04_review/`
   - **Fundamental issue** → move both back to `../01_research/` with feedback

### Quality Gate

**MANDATORY HUMAN GATE** — Every PRD+RFC package must receive explicit approval before committing to deliverables. The agent must never:
- Auto-commit files without user review
- Batch-approve packages without per-package review
- Skip the review step for any reason
- Commit files with pipeline frontmatter still present

### Presentation Format

When presenting a PRD+RFC package for final review:

```
## Final Review: {project_title}

### PRD Summary
- **Project**: {project_slug}
- **Priority**: {priority}
- **Requirements**: {N} Must, {N} Should, {N} Could
- **PRD approved by**: {approved_by} on {approved_date}

### RFC Summary
- **Design approach**: {one-sentence summary}
- **Components**: {list key components}
- **Alternatives considered**: {count}
- **Requirement coverage**: {N}/{total} requirements traced

### Package Health
- [ ] PRD approved at Stage 2
- [ ] All MUST requirements have design coverage
- [ ] Architecture diagram present
- [ ] Testing strategy defined
- [ ] No unresolved open questions (or list remaining)

[Approve / Revise / Reject]
```

### Edge Cases

- **Partial packages**: If only a PRD or only an RFC is present for a slug, do not present for final review. Note the missing piece and which stage should produce it.
- **Stale packages**: If files sit in `04_review/` for more than 7 days without review, create a coordination note in `who/coordination/` flagging the backlog.
- **PRD amended after RFC**: If the PRD was amended after RFC completion, verify the traceability table still holds. Flag any broken traceability links.
- **Multiple packages**: When multiple packages are ready, present them one at a time in priority order.

## Load/Skip Decision

**Load this directory when**:
- A PRD+RFC package has been moved into `04_review/` for final human approval
- Checking whether a complete package exists (both PRD and RFC with matching slug)
- Presenting the final review to the user for approve/revise/reject decision

**Skip when**:
- No files are present in `04_review/` (empty stage)
- Working on files in earlier pipeline stages (01, 02, 03)
- Performing non-pipeline operational work

**Token cost**: ~850 tokens (this AGENTS.md)
