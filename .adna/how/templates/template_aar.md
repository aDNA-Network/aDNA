---
type: artifact
artifact_type: aar
mission_id: "{mission_id}"
campaign_id: "{campaign_id}"
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_edited_by: agent_{username}
tags: [aar, artifact]
---

# AAR: {Mission Title}

## Mission Identity

| Field | Value |
|-------|-------|
| Mission | {mission_id} |
| Campaign | {campaign_id} |
| Status | completed / abandoned |
| Sessions | {count} |
| Duration | {start_date} — {end_date} |

## Scorecard

| # | Deliverable | Status | Notes |
|---|-------------|--------|-------|
| 1 | {deliverable description} | validated / partial / failed | {brief note} |
| 2 | {deliverable description} | validated / partial / failed | {brief note} |

**Validated**: {N}/{total} deliverables

## Gap Register

| # | Gap | Severity | Source | Remediation |
|---|-----|----------|--------|-------------|
| 1 | {gap description} | critical / high / medium / low | {where discovered} | {action or backlog ref} |

## Technical Debt

| # | Debt | Impact | Priority | Tracking |
|---|------|--------|----------|----------|
| 1 | {debt description} | {what breaks if ignored} | high / medium / low | {backlog ref or mission ref} |

## Readiness Assessment

| Criterion | Status | Evidence |
|-----------|--------|----------|
| All deliverables validated | GO / NO-GO | {N}/{total} validated |
| No critical gaps | GO / NO-GO | {count} critical gaps remaining |
| Dependencies met for next mission | GO / NO-GO | {assessment} |

**Overall**: **GO** / **NO-GO** for {next_mission_id}

**Rationale**: {1-2 sentence justification}

## Recommendation

{What should happen next. If GO: proceed to next mission. If NO-GO: what remediation is needed before proceeding.}

## Lessons Learned

- {Key insight that should inform future missions}
