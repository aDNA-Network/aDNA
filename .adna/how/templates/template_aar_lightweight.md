---
type: template
title: "Lightweight AAR (After-Action Review)"
created: 2026-04-03
updated: 2026-10-16   # v8.13 — §Boundary AAR-light appended; the five-line format unchanged
last_edited_by: agent_rosetta
tags: [template, aar, governance]
---

# Lightweight AAR Template

Every mission MUST include this AAR before setting `status: completed`. Completable in under 2 minutes.

## Format

```markdown
## AAR
- **Worked**: [what went well — one line]
- **Didn't**: [what didn't work or surprised us — one line]
- **Finding**: [key insight or discovery — one line]
- **Change**: [process change for next time — one line, or "none"]
- **Follow-up**: [link to backlog/mission/issue, or "none"]
```

## Rules

1. Every mission gets an AAR — no exceptions
2. One line per field — keep it tight
3. "None" is valid for Change and Follow-up
4. Be specific — "went well" is too vague; "parallel agent execution cut review time 50%" is useful
5. Findings that affect campaign-level decisions should propagate upward to the campaign doc

## Campaign AAR

Campaigns also get an AAR using the same format, appended to the campaign master document at completion. Campaign AARs summarize across all missions — patterns, not individual findings.

## Boundary AAR-light (phase seam) — optional

*(v8.13.)* At each **phase close**, after the verdict and the rulings, a campaign may file a boundary AAR-light — the five lines above **plus** two sections that read the **live system**, not the record (a verdict reads the record; this reads the running product):

```markdown
## Gap register (read from the live system)
| # | Gap | Where seen (live) | Disposition (by name) |
|---|-----|-------------------|-----------------------|
| 1 | {what the product does not yet do} | {command / surface / path} | {a roadmap row · a risk row · a watch row · a standard ask — named} |

## Improvements
- {each improvement, dispositioned into a named file — never "noted"}
```

Companion artefact: a **campaign update for the operator** — milestones · the product measured · the remaining phases. The boundary AAR-light sits *beside* the drift-triggered AAR-light (ADR-016 of `aDNA.aDNA`, > 2× the band) and the closing full AAR; it is **recommended at every phase seam, not gating** (`template_campaign.md` §Verification Per-Phase). *(Evidence: Terminal's first boundary AAR-light found two product gaps no verdict had named, because the verdicts read the record and the AAR-light read the running system.)*
