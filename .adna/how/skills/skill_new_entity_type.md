---
type: skill
skill_type: agent
created: 2026-02-20
updated: 2026-02-20
status: active
category: ontology
trigger: "User requests a new entity type or onboarding Step 6 suggests extensions"
last_edited_by: agent_init
tags: [skill, ontology, scaffolding]

requirements:
  tools: []
  context: ["CLAUDE.md", "what/ontology.md (if present)"]
  permissions: ["create directories", "write AGENTS.md", "write templates"]

parameters:
  - name: entity_name
    type: string
    required: true
    description: "Singular name for the entity type (e.g., 'customer', 'experiment', 'contract')"
  - name: triad_leg
    type: string
    required: true
    description: "Which triad leg: who, what, or how"
  - name: description
    type: string
    required: true
    description: "One-sentence description of what this entity type represents"
  - name: key_fields
    type: list
    required: false
    description: "Domain-specific frontmatter fields beyond the base set (e.g., 'deal_stage', 'priority')"
---

# Skill: New Entity Type Scaffolding

## Overview

Scaffolds a complete new entity type in the aDNA ontology: creates the directory under the correct triad leg, generates an AGENTS.md with working rules, and creates a template in `how/templates/`. Produces output that is usable without manual editing.

## Trigger

- Onboarding Step 6 confirms an ontology extension
- User explicitly requests a new entity type
- Agent identifies a need for a new entity type during work

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `entity_name` | Yes | Singular name (e.g., `customer`, `experiment`) |
| `triad_leg` | Yes | `who`, `what`, or `how` |
| `description` | Yes | One-sentence purpose of this entity type |
| `key_fields` | No | Extra frontmatter fields beyond base set |

## Requirements

### Tools/APIs
- File read/write access to the vault

### Context Files
- `CLAUDE.md` — naming conventions and frontmatter standards
- `what/ontology.md` — if present, for ontology registry update

### Permissions
- Create directories under triad legs
- Write AGENTS.md files
- Write template files in `how/templates/`

## Implementation

### Step 1: Validate Parameters

Verify:
- `entity_name` is lowercase, underscores only, singular (not plural)
- `triad_leg` is one of `who`, `what`, `how`
- The directory `{triad_leg}/{entity_name}s/` does not already exist (pluralize for directory)
- Explain the triad placement to the user: "I'm putting `{entity_name}` under `{triad_leg}/` because..."

If the directory exists, inform the user and offer to update the existing AGENTS.md instead.

### Step 2: Create Directory

```bash
mkdir -p {triad_leg}/{entity_name}s/
```

Use the plural form for the directory name (e.g., `who/customers/`, `what/experiments/`).

### Step 3: Generate AGENTS.md

Create `{triad_leg}/{entity_name}s/AGENTS.md` with the following structure:

```markdown
---
type: directory_index
created: {today}
updated: {today}
last_edited_by: agent_{username}
tags: [directory_index, {entity_name}]
---

# {triad_leg}/{entity_name}s/ — Agent Guide

## What's Here

{description}. One file per {entity_name}.

## Working Rules

- **Naming**: `{entity_name}_{descriptive_name}.md` (underscores, lowercase)
- **Required frontmatter**: `type: {entity_name}`, `created`, `updated`, `status`, `last_edited_by`, `tags`
- **Check before overwriting**: Read `updated` field — if edited today by someone else, confirm with user
- **Set audit trail**: Update `last_edited_by` and `updated` on every edit

## Load/Skip Decision

**Load this directory when**:
- Creating or modifying {entity_name} records
- Looking up information about specific {entity_name}s
- Building cross-references to {entity_name} records

**Skip when**:
- Working on unrelated tasks
- {entity_name} data is not relevant to current session

**Token cost**: ~200 tokens (this AGENTS.md). Individual records are ~100-300 tokens each.
```

Customize the working rules based on the entity type:
- WHO entities: Add linking rules (e.g., "Link to contacts via `[[contacts/contact_name]]`")
- WHAT entities: Add knowledge-specific rules (e.g., "Include sources and methodology")
- HOW entities: Add process-specific rules (e.g., "Track status transitions")

### Step 4: Generate Template

Create `how/templates/template_{entity_name}.md`:

```markdown
---
type: {entity_name}
created: 2026-02-28
updated: 2026-02-28
status: active
last_edited_by:
tags: [{entity_name}]
{key_fields with defaults}
---

# {entity_name}_{name}

## Overview

{Brief description of this {entity_name}.}

## Details

{Key details — customize sections based on entity type.}

## Related

- {Links to related entities}
```

Include any `key_fields` in the frontmatter with sensible defaults.

### Step 5: Update Template Index (Optional)

If `how/templates/AGENTS.md` exists, add an entry for the new template in the template index table.

### Step 6: Update Ontology (Optional)

If `what/ontology.md` exists, add the new entity type to the appropriate triad section.

### Step 7: Confirm to User

Report what was created:
- Directory: `{triad_leg}/{entity_name}s/`
- Agent guide: `{triad_leg}/{entity_name}s/AGENTS.md`
- Template: `how/templates/template_{entity_name}.md`
- Triad placement rationale

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Entity directory | Directory | `{triad_leg}/{entity_name}s/` |
| AGENTS.md | File | Per-directory agent guide with working rules |
| Template | File | Frontmatter schema and body structure in `how/templates/` |
| Template index update | Edit | Entry added to `how/templates/AGENTS.md` (if present) |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Directory already exists | Entity type previously created | Offer to update existing AGENTS.md or skip |
| Invalid triad leg | User specified wrong leg | Explain the Question Test and suggest correct placement |
| Naming conflict | Entity name conflicts with existing directory | Suggest alternative name with disambiguation |
| Template directory missing | `how/templates/` doesn't exist | Create it first |

## Examples

### Example 1: Startup adding investors

```
Parameters:
  entity_name: investor
  triad_leg: who
  description: "Investor profiles tracking fund details, check sizes, portfolio focus, and relationship status"
  key_fields: [fund_name, check_size_range, portfolio_focus, relationship_stage]

Creates:
  who/investors/AGENTS.md
  how/templates/template_investor.md
```

### Example 2: Research lab adding experiments

```
Parameters:
  entity_name: experiment
  triad_leg: what
  description: "Experiment records documenting hypothesis, methodology, results, and conclusions"
  key_fields: [hypothesis, methodology, status, principal_investigator]

Creates:
  what/experiments/AGENTS.md
  how/templates/template_experiment.md
```

### Example 3: Creative agency adding revision cycles

```
Parameters:
  entity_name: revision_cycle
  triad_leg: how
  description: "Revision tracking for creative deliverables — feedback rounds, approval status, version history"
  key_fields: [project, client, revision_number, approval_status]

Creates:
  how/revision_cycles/AGENTS.md
  how/templates/template_revision_cycle.md
```

## Related

- **Onboarding Skill**: `how/skills/skill_onboarding.md` — Step 6 triggers this skill
- **Ontology Extension**: See README § Extending the Ontology
- **Template Library**: `how/templates/AGENTS.md`
