---
type: skill
skill_type: agent
created: 2026-03-17
updated: 2026-03-17
status: active
category: operations
trigger: "Campaign completion, or when mission deliverables contain reusable knowledge"
last_edited_by: agent_init
tags: [skill, context, graduation, knowledge-capture]
---

# Skill: Context Graduation

## Purpose

Systematic process for promoting campaign and mission deliverables into the permanent context library. Prevents knowledge loss when campaigns complete — reusable findings, patterns, and guides graduate from ephemeral mission artifacts to durable context files.

## When to Invoke

- **Primary trigger**: Campaign completion (after AAR)
- **Secondary trigger**: Mission completion with significant deliverables
- **Manual trigger**: User identifies reusable knowledge in any project artifact

## Graduation Criteria

A deliverable qualifies for graduation if it meets ALL of:

| Criterion | Test |
|-----------|------|
| **Reusability** | Would 2+ future tasks benefit from this knowledge? |
| **Token threshold** | Contains >1K tokens of distilled, actionable content? |
| **Not ephemeral** | Content is durable (not tied to a specific date, sprint, or one-time event)? |
| **Not redundant** | No existing context file covers this topic adequately? |

## Procedure

### Step 1: Scan Deliverables

After campaign/mission completion, scan all deliverables and artifacts:
- Mission files (`how/missions/` or campaign `missions/`)
- Artifact files (`how/missions/artifacts/`)
- Decision records (`what/decisions/`)
- Session files with significant findings

### Step 2: Filter Candidates

Apply graduation criteria to each deliverable. Record candidates:

```markdown
| Source File | Candidate Topic | Tokens | Reuse Potential | Existing Coverage |
|------------|----------------|--------|-----------------|-------------------|
| {file} | {topic} | ~{N}K | {high/medium} | {none/partial/full} |
```

Discard files that fail any criterion. If existing coverage is `full`, skip (no graduation needed). If `partial`, consider updating the existing file instead of creating a new one.

### Step 3: Route to Context Library

For each qualifying candidate:

1. **Identify the target topic** — which `what/context/{topic}/` directory?
2. **Choose subtype** — `context_research`, `context_guide`, or `context_core`
3. **Determine action**:
   - **New file**: No existing coverage → create new subtopic file
   - **Update**: Partial coverage → merge findings into existing file
   - **New topic**: No relevant topic exists → create new topic directory with AGENTS.md

### Step 4: Produce Context Files

For each new or updated context file:

1. Extract reusable content from the source deliverable
2. Strip ephemeral details (dates, session references, one-time context)
3. Restructure into standard context format (Key Principles → Recommendations → Examples → Anti-Patterns → Sources)
4. Apply quality rubric — target 3.5+ composite, no floor violations
5. Add quality_score frontmatter
6. Update topic AGENTS.md with new subtopic entry

### Step 5: Update Indexes

- Update `what/context/{topic}/AGENTS.md` — add subtopic row
- Update `what/context/AGENTS.md` — update topic token total and quality average
- Update `what/context/context_recipes.md` — add recipes if new subtopic enables new combinations
- Cross-reference new context from relevant AGENTS.md files

### Step 6: Report

```markdown
## Context Graduation Report — {campaign_id}

### Graduated
| Source | Target Context File | Action | ~Tokens |
|-------|-------------------|--------|---------|
| {source} | {target} | new/update | ~{N}K |

### Not Graduated (with rationale)
| Source | Reason |
|-------|--------|
| {source} | {reason} |

### Follow-Up
- {any quality improvement tasks or recipe updates needed}
```

## Outputs

- New or updated context files in `what/context/`
- Updated AGENTS.md indexes
- Updated context_recipes.md (if applicable)
- Graduation report (rendered to user)

## Anti-Patterns

1. **Graduating everything.** Not all campaign output is reusable. Apply the criteria strictly.
2. **Copy-pasting raw artifacts.** Mission artifacts contain ephemeral details. Extract and restructure.
3. **Skipping quality scoring.** Every graduated file must meet rubric standards before filing.
4. **Orphaned context.** Every new file must be indexed in its topic AGENTS.md — otherwise it's invisible.
