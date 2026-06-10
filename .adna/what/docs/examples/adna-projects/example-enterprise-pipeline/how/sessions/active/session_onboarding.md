---
type: session
session_id: session_onboarding
operator: user
started: 2026-03-19
status: completed
created: 2026-03-19
updated: 2026-03-19
last_edited_by: agent_init
tags: [session, onboarding]
---

# Session: Onboarding

## Interview Answers

| Question | Answer |
|----------|--------|
| Q1: What are you building? | A data integration platform connecting CRM, analytics, and ML pipelines for mid-market SaaS clients |
| Q2: Domain? | enterprise |
| Q3: Team or solo? | small-team (3 people) |
| Q4: Tooling? | obsidian |
| Q5: Personality? | custom — "Ops" (ship fast, measure everything, automate the boring stuff) |

## Configuration Applied

- **Skeleton tier**: Standard (small-team)
- **Domain extensions**: customers, partners, contacts, projects, services, apis, deployments, incidents
- **Personality**: Ops (custom)
- **Tooling**: Obsidian
- **Collision prevention**: Tier 2 (read-before-write + updated check + last_edited_by)
- **Coordination**: `who/coordination/` directory for team handoffs

## Files Created

- CLAUDE.md, MANIFEST.md, STATE.md, AGENTS.md, README.md
- what/context/, what/decisions/, what/services/, what/apis/
- how/missions/, how/sessions/active/, how/sessions/history/, how/templates/, how/backlog/, how/deployments/, how/incidents/
- who/customers/, who/partners/, who/contacts/, who/projects/, who/coordination/, who/governance/

## Suggested Next Steps

1. Add your first customer record to `who/customers/`
2. Document key services in `what/services/`
3. Set up coordination notes for your team in `who/coordination/`
4. Create API docs for your integration endpoints in `what/apis/`
