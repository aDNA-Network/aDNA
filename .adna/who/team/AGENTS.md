---
type: directory_index
created: 2026-03-18
updated: 2026-03-18
last_edited_by: agent_init
tags: [directory_index, team]
---

# who/team/ — Team Members

## Purpose

Team member profiles — roles, expertise, access levels, and responsibilities. Each person who contributes to the project gets a record here.

## Naming

Pattern: `team_full_name.md` (underscores, lowercase)

## Required Frontmatter

```yaml
---
type: team_member
name: "Full Name"
role: "Role Title"
status: active|inactive
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_edited_by: agent_{username}
tags: [team]
---
```

Optional extension fields: `joined`, `expertise` (list), `access_level`, `email`, `github`.

## Load/Skip Decision

**Load when**: Onboarding a new team member, reviewing access levels, or looking up expertise.
**Skip when**: Working on technical content unrelated to team management.

**Token cost**: ~200 tokens (this AGENTS.md)
