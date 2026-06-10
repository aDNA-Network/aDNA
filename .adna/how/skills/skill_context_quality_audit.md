---
type: skill
skill_type: agent
created: 2026-03-17
updated: 2026-03-17
status: active
category: review
trigger: "Context quality audit requested, or periodic review of context library health"
last_edited_by: agent_init
tags: [skill, context, quality, audit]
---

# Skill: Context Quality Audit

## Purpose

Systematic evaluation of context library files against the 6-axis quality rubric. Identifies floor violations, scores trends, and produces actionable improvement recommendations.

## Inputs

| Input | Required | Default |
|-------|----------|---------|
| Scope | No | All context files |
| Topic filter | No | All topics |
| Floor-only mode | No | false (full scoring) |

## Procedure

### Step 1: Inventory

Scan `what/context/` for all `context_*.md` files. For each, record:
- File path
- Current `quality_score` (if present)
- `last_evaluated` date (if present)
- `freshness_category`

### Step 2: Prioritize

Score files needing evaluation:
1. Files with no `quality_score` frontmatter (never evaluated)
2. Files with `last_evaluated` > 90 days ago
3. Files with `freshness_category: volatile` and `last_evaluated` > 30 days ago
4. Files with any axis ≤ 2 (floor violations from prior evaluation)

### Step 3: Evaluate

For each file in priority order:

1. Read the file in full
2. Identify 2-3 related files for cross-topic coherence assessment
3. Score each of the 5 numeric axes (1-5) using the rubric at `what/docs/context_quality_rubric.md`
4. Assign freshness category (volatile/stable/durable/mixed)
5. Compute composite = average of 5 numeric axes
6. Check floor rule: any axis ≤ 2 triggers revision flag

### Step 4: Update Frontmatter

Add or update quality fields in each evaluated file:
```yaml
quality_score: {composite}
signal_density: {score}
actionability: {score}
coverage_uniformity: {score}
source_diversity: {score}
cross_topic_coherence: {score}
freshness_category: {category}
last_evaluated: {today}
```

### Step 5: Report

Produce an audit summary:

```markdown
## Context Quality Audit — {date}

### Summary
- Files evaluated: {N}
- Average composite: {avg}
- Floor violations: {count}
- Files needing revision: {list}

### Scores by Topic
| Topic | Files | Avg Score | Floor Violations |
|-------|-------|-----------|-----------------|
| {topic} | {N} | {avg} | {count} |

### Floor Violations
| File | Axis | Score | Recommendation |
|------|------|-------|---------------|
| {file} | {axis} | {score} | {action} |

### Trends (if prior audit exists)
| File | Previous | Current | Change |
|------|----------|---------|--------|
| {file} | {prev} | {curr} | {delta} |
```

### Step 6: Update Topic AGENTS.md

Update the `Avg Quality` column in each topic's AGENTS.md and in `what/context/AGENTS.md`.

## Outputs

- Updated frontmatter on all evaluated context files
- Audit summary (rendered to user or saved to `how/missions/artifacts/`)
- Updated AGENTS.md quality averages

## Frequency

- **Periodic**: Monthly for active projects, quarterly for stable projects
- **Triggered**: After any campaign that creates or modifies context files
- **Floor-only mode**: Quick check that only evaluates files with known floor violations
