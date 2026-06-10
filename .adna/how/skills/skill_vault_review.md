---
type: skill
skill_type: process
created: 2026-03-18
updated: 2026-03-18
status: active
category: review
trigger: "Monthly or after significant vault changes (10+ files modified, new entity types, context topic additions)"
last_edited_by: agent_init
tags: [skill, review, quality, process]

requirements:
  tools: ["Obsidian (Dataview queries)", "Claude Code or manual review"]
  context: ["what/context/AGENTS.md", "context_recipes.md"]
  permissions: ["Read access to all vault directories"]
---

# Skill: Vault Review

## Overview

A periodic human/hybrid quality review process for aDNA vaults. Checks structural integrity, content freshness, naming compliance, and context library health. Designed to run monthly or after significant vault changes to prevent drift and quality degradation.

## Trigger

Run this review when:
- Monthly scheduled review (recommended cadence)
- After adding 10+ files or a new entity type
- After a context topic is added or overhauled
- Before publishing or sharing the vault with new users
- After onboarding a new contributor who created multiple files

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| scope | string | No | `full` | `full` (entire vault), `who`, `what`, or `how` (single triad leg) |
| depth | string | No | `standard` | `quick` (naming + frontmatter only), `standard` (+ content quality), `deep` (+ cross-ref audit) |

## Implementation

### Step 1: Structural Integrity Check

Verify vault structure is intact:
- [ ] All three triad directories exist (`who/`, `what/`, `how/`)
- [ ] Each directory has an `AGENTS.md` file
- [ ] No orphaned directories (directories without AGENTS.md or content)
- [ ] `.obsidian/` config is present and plugins are listed in `community-plugins.json`

### Step 2: Naming Compliance Scan

Check all content files follow naming conventions:
- [ ] Underscores only, no hyphens in filenames
- [ ] Pattern matches `type_descriptive_name.md`
- [ ] No spaces or special characters in filenames
- [ ] Template files prefixed with `template_`
- [ ] Skill files prefixed with `skill_`

**Quick scan** (Dataview query):
```dataview
TABLE file.name FROM "" WHERE !contains(file.name, "_") AND file.name != "AGENTS" AND file.name != "CLAUDE" SORT file.name
```

### Step 3: Frontmatter Completeness

Check all content files have required frontmatter:
- [ ] `type` field present on every content file
- [ ] `created` and `updated` dates present
- [ ] `status` field present where applicable
- [ ] `last_edited_by` field present
- [ ] `tags` field present (can be empty list)

**Quick scan** (Dataview query):
```dataview
TABLE type, created, updated, status FROM "" WHERE !type SORT file.name
```

### Step 4: Freshness Audit (Standard+ depth)

Check content currency:
- [ ] No files with `updated` older than 90 days in active directories
- [ ] Context files with `freshness_category: volatile` reviewed within 30 days
- [ ] Active campaigns and missions have recent updates
- [ ] Stale files flagged with `#context-update-needed`

### Step 5: Context Library Health (Standard+ depth)

Review the context library specifically:
- [ ] Topic AGENTS.md files list accurate subtopic counts and token estimates
- [ ] `context_recipes.md` references exist and token budgets are accurate
- [ ] No context files below quality floor (composite < 3.0 or any axis < 3)
- [ ] All context files have `token_estimate` in frontmatter

### Step 6: Cross-Reference Audit (Deep depth only)

Verify link integrity:
- [ ] No broken wikilinks (use Obsidian's built-in broken link report)
- [ ] No phantom references in AGENTS.md files (topics listed but files missing)
- [ ] Template trigger table matches actual Templater folder mappings
- [ ] Skill index in `how/skills/AGENTS.md` lists all skill files

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Review checklist | Markdown | Completed checklist with pass/fail per item |
| Issue list | Markdown | List of issues found, severity, and suggested fixes |
| Metrics | Frontmatter update | Update `updated` date on reviewed AGENTS.md files |

## Scoring

After completing the review, score the vault on these dimensions:

| Dimension | Score (A-F) | Criteria |
|-----------|-------------|----------|
| Structure | | Triad intact, AGENTS.md coverage, no orphans |
| Naming | | Convention compliance rate (target: >95%) |
| Frontmatter | | Required fields present rate (target: >90%) |
| Freshness | | Files updated within policy windows |
| Context Quality | | All files above floor, recipes accurate |
| Cross-References | | Link resolution rate (target: 100%) |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Missing AGENTS.md | Directory created without index | Create from template_folder_note or directory_index pattern |
| Broken wikilinks | Files renamed or deleted without updating refs | Use Obsidian rename (auto-updates links) or manual search-replace |
| Token estimate drift | File content changed without updating frontmatter | Re-count tokens (rough: words × 1.3) and update `token_estimate` |

## Related

- **Skills Protocol**: `how/skills/AGENTS.md`
- **Context Quality Audit**: `how/skills/skill_context_quality_audit.md` (agent skill — narrower scope, context-only)
- **Context Engineering**: `what/context/adna_core/context_adna_core_context_engineering.md`
