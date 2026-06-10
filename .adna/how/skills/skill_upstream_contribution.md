---
type: skill
skill_type: agent
category: development
created: 2026-03-20
updated: 2026-03-20
status: active
last_edited_by: agent_init
token_estimate: ~800
tags: [skill, agent, contributing, upstream, community]
---

# Skill: Upstream Contribution Awareness

## Purpose

Teach agents to notice framework-level improvement opportunities during normal work and surface them to the user for optional upstream submission to the aDNA repo.

## Trigger

During any task, you notice something that would improve the **aDNA framework itself** — not just the current project. Examples:

- A template missing fields you had to add manually
- A context recipe that should exist but doesn't
- A naming inconsistency between the standard and actual practice
- A skill you built that would be broadly useful
- A gap in the standard docs you had to work around
- A workflow pattern used repeatedly but not yet documented

## What Does NOT Qualify

- **Project-specific content** — your customer data, custom templates, or domain objects
- **Personal preference** — the user's template tweaks or naming style
- **Already known** — check `how/backlog/` for existing `idea_upstream_*` files first
- **Mid-crisis context** — never derail active debugging or urgent work

## Interaction Pattern

Surface suggestions at **natural pause points** only — end of a task, session SITREP, or mission AAR. Never interrupt mid-task.

Phrasing should be lightweight and deferential:

> "While working on [task], I noticed [observation]. This seems like it could improve the aDNA framework for all users. Want me to file a backlog idea for upstream consideration?"

If the user says no, drop it. If yes, proceed to submission.

## Submission Mechanism

### Step 1: Create a backlog idea file

Create `how/backlog/idea_upstream_<short_description>.md` in the **user's current vault** (not the adna repo itself):

```yaml
---
type: backlog
category: governance
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: idea
last_edited_by: agent_{username}
tags: [backlog, upstream-suggestion]
upstream_target: LatticeProtocol/adna
---
```

Body should include:
- **Observation**: What you noticed (specific, reproducible)
- **Context**: What task you were doing when you noticed it
- **Suggested improvement**: What the fix or addition would look like
- **Affected files** (if known): Which aDNA repo files would change

### Step 2 (Optional): Open a GitHub issue

If the `gh` CLI is configured and the user approves:

```bash
gh issue create --repo LatticeProtocol/adna \
  --title "Suggestion: <short description>" \
  --body "<observation + context from the backlog file>"
```

Only offer this step if the user has `gh` authenticated. Never push directly to the upstream repo.

## Constraints

- **One suggestion per pause point.** Don't batch-dump 5 ideas at the user.
- **No auto-filing.** Always get explicit user approval before creating files or issues.
- **Framework-level only.** The test: "Would this help someone using aDNA on a completely different project?"
