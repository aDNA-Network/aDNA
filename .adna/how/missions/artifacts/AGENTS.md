---
type: directory_index
created: 2026-03-17
updated: 2026-03-17
last_edited_by: agent_init
tags: [directory_index, artifacts, aar]
---

# Mission Artifacts

## Purpose

Persistent outputs from mission and campaign execution — AARs (After-Action Reviews), gap registers, verification reports, and other structured deliverables that outlive the session that produced them.

## Naming Convention

```
{campaign_id}_{mission_id}_aar.md       # After-Action Review
{campaign_id}_gap_register.md           # Campaign-level gap register
{descriptive_name}.md                   # Other mission artifacts
```

## Key Artifact Types

| Type | `artifact_type` | Template | When Created |
|------|----------------|----------|--------------|
| After-Action Review | `aar` | `template_aar.md` | Mission completion |
| Gap Register | `gap_register` | — | Campaign-level tracking |
| Verification Report | `verification` | — | Phase gate or campaign close |

## Load/Skip Decision

**Load when**: Reviewing mission outcomes, checking gap status, preparing for next mission in a campaign sequence.

**Skip when**: Routine session work, creating new missions, or working on unrelated campaigns.

**Token cost**: ~300 tokens (this AGENTS.md). Individual artifacts vary (50-200 lines).
