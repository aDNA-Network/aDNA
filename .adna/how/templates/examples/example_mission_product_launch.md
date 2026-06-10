---
plan_id: plan_q2_product_launch
type: plan
title: "Q2 Product Launch — Agent Onboarding Feature"
owner: <username>
status: completed
created: 2026-01-20
updated: 2026-03-15
last_edited_by: agent_init
tags: [plan, product, launch]
---

# Q2 Product Launch — Agent Onboarding Feature

## Goal

Ship the interactive agent onboarding experience that walks new users from clone to productive vault in under 30 minutes. Includes domain detection, ontology extension suggestions, governance file customization, and personality configuration.

## Tasks

### 1. Design onboarding conversation flow
- **Status**: completed
- **Session**: session_example_20260120_onboarding_design
- **Description**: Map the 10-step onboarding flow. Define decision points, fallback paths, and completion markers. Review against 4 target personas (startup, researcher, creative, PKM).
- **Files**: `how/skills/skill_onboarding.md`, `how/pipelines/prd_rfc/02_requirements/prd_onboarding.md`
- **Depends on**: none

### 2. Build domain detection logic
- **Status**: completed
- **Session**: session_example_20260125_domain_detection
- **Description**: Implement Step 5 (Discovery Conversation) with signal-based domain classification. Map domain signals to ontology extension suggestions. Cover 6 domain categories: biotech, software, research, business, creative, personal.
- **Files**: `how/skills/skill_onboarding.md` (Steps 5-6)
- **Depends on**: 1

### 3. Implement governance file customization
- **Status**: completed
- **Session**: session_example_20260128_governance_custom
- **Description**: Build Step 7 — automated customization of MANIFEST.md, STATE.md, and CLAUDE.md based on discovery conversation. Preserve structural integrity while updating project-specific content.
- **Files**: `how/skills/skill_onboarding.md` (Step 7), `MANIFEST.md`, `STATE.md`, `CLAUDE.md`
- **Depends on**: 2

### 4. Add personality customization
- **Status**: completed
- **Session**: session_example_20260130_personality
- **Description**: Implement Step 8 — optional agent personality replacement. User provides name, archetype, operating principles; agent generates updated Identity & Personality section. Default (Berthier) preserved if declined.
- **Files**: `how/skills/skill_onboarding.md` (Step 8)
- **Depends on**: 3

### 5. End-to-end testing with 4 personas
- **Status**: completed
- **Session**: session_example_20260205_persona_testing
- **Description**: Run full onboarding simulation for each target persona. Verify domain suggestions are appropriate, governance customization is correct, and the experience completes in under 30 minutes. Fix any friction points.
- **Files**: `how/missions/plan_q2_product_launch.md` (this file — completion summary)
- **Depends on**: 4

## Notes

- Personality customization was originally planned as a separate skill but was simpler as an inline step (Step 8) in the onboarding flow.
- Domain detection accuracy improved significantly when we added follow-up questions based on initial signals rather than trying to classify from a single question.
- The 30-minute target was met for all personas except "creative professional" which took ~35 minutes due to longer ontology extension discussion. Acceptable.

## Completion Summary

### Deliverables
- `how/skills/skill_onboarding.md` — 10-step onboarding skill (220 lines)
- CLAUDE.md first-run detection integrated (2 conditions)
- STATE.md partial-resume detection section added
- 6 domain categories with extension suggestions

### Descoped
- Automated personality gallery (preset personalities to choose from) — deferred to v2

### Key Findings
- Users engage more when the agent explains *why* a directory goes under a specific triad leg, not just *where*
- Solo users often skip session tracking — should document what's optional for single-user setups
- The "marketplace teaser" (Step 9) generated the most follow-up questions — good engagement signal

### Scope Changes
- Added Step 9 (Marketplace Teaser) mid-execution — not in original PRD but natural fit
- Removed "template walkthrough" step — too detailed for onboarding, better as a separate skill
