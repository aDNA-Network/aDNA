# example-enterprise-pipeline

A data integration platform connecting CRM, analytics, and ML pipelines for mid-market SaaS clients.

## Structure

This project uses the [aDNA](https://github.com/LatticeProtocol/adna) knowledge architecture:

- **`who/`** — Customers, partners, contacts, projects, coordination
- **`what/`** — Knowledge, context, services, APIs
- **`how/`** — Operations, missions, deployments, incidents

## Getting Started

### With an AI agent (recommended)

Open this directory in [Claude Code](https://docs.anthropic.com/en/docs/claude-code) or another AI coding assistant. The agent will read `CLAUDE.md` and orient automatically.

### Without an AI agent

Browse the vault in [Obsidian](https://obsidian.md) or any Markdown editor. Start with `MANIFEST.md` for the project overview, then `STATE.md` for current status.

## Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Agent governance and project identity |
| `MANIFEST.md` | Project overview and architecture |
| `STATE.md` | Current phase, next steps, blockers |
| `AGENTS.md` | Directory index for agents |

## Enterprise Extensions

| Directory | What goes here |
|-----------|---------------|
| `who/customers/` | Client records — deal status, contacts, engagement history |
| `who/partners/` | Vendor and integration partner profiles |
| `who/contacts/` | Individual contact profiles |
| `who/projects/` | Client project records — scope, timeline, deliverables |
| `what/services/` | Service catalog — capabilities, SLAs, dependencies |
| `what/apis/` | API documentation — endpoints, auth, schemas |
| `how/deployments/` | Deployment records — what shipped, when, to whom |
| `how/incidents/` | Incident reports — root cause, impact, resolution |

## Team Collaboration

This vault is configured for a team of 3. Key conventions:

- **Check `who/coordination/`** for handoff notes between sessions
- **Set `last_edited_by`** in frontmatter on every edit
- **Check `updated` dates** before overwriting files edited today by someone else
