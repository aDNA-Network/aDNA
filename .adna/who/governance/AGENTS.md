---
type: directory_index
created: 2026-02-17
updated: 2026-03-28
last_edited_by: agent_aria
tags: [directory_index, governance]
---

# who/governance/ — Governance (Agent Reference)

## Purpose

Team governance for this project. Defines roles, decision authority, and operational policies that govern how the project operates.

## Key Files

| File | Purpose |
|------|---------|
| `governance_roles.md` | Team members, responsibilities, and areas of ownership |
| `governance_decision_authority.md` | Decision authority matrix — who approves what category of change |
| `governance_policies.md` | Operational policies — collision prevention, naming, sessions, escalation |
| `governance_agent_protocol.md` | Agent behavioral contract — partnership model, challenge phase, autonomy framework |

Create governance files as the project matures. Start with roles and policies, add decision authority when the team grows.

## Conventions

- **Naming**: `governance_{topic}.md` (underscores only)
- **Frontmatter**: All files require `type: governance` plus base fields
- **Updates**: Changes to governance files should be coordinated — read before write, confirm with user if `updated` is recent
- **Scope**: Governance files define rules that all agents and users must follow. Treat as authoritative.

## Load/Skip Decision

**Load this directory when**:
- Reviewing or modifying governance policies (roles, decision authority, operational rules)
- Onboarding a new team member and need to understand team roles and decision-making
- Proposing changes to governance structure (use a Tier 2 session)

**Skip when**:
- Performing routine operational work that doesn't touch governance policies
- Working on domain content (context, lattices, CRM) without governance implications
- Already familiar with current governance structure and not modifying it

**Token cost**: ~300 tokens (this AGENTS.md). Individual governance files are ~100-200 lines each.

## Cross-References

- [CLAUDE.md](../../CLAUDE.md) — Master agent context (references governance rules)
- [who/coordination/AGENTS](../coordination/AGENTS.md) — Cross-agent ephemeral notes
- [how/sessions/AGENTS](../../how/sessions/AGENTS.md) — Session protocol
