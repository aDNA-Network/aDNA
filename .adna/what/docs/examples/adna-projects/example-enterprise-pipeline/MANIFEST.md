---
type: manifest
created: 2026-03-19
updated: 2026-03-19
status: active
last_edited_by: agent_init
tags: [manifest, enterprise]
---

# example-enterprise-pipeline

## What This Is

A data integration platform connecting CRM, analytics, and ML pipelines for mid-market SaaS clients.

## Architecture

This project uses the aDNA knowledge architecture:

```
example-enterprise-pipeline/
├── CLAUDE.md          # Agent governance
├── MANIFEST.md        # This file — project overview
├── STATE.md           # Current phase and next steps
├── AGENTS.md          # Root agent guide
├── README.md          # Human getting-started guide
├── what/              # Knowledge objects and context
│   ├── context/       # Domain knowledge library
│   ├── decisions/     # Architecture decisions
│   ├── services/      # Service catalog (enterprise)
│   └── apis/          # API documentation (enterprise)
├── how/               # Operations and processes
│   ├── missions/      # Multi-session plans
│   ├── sessions/      # Session tracking (active + history)
│   ├── templates/     # Reusable templates
│   ├── backlog/       # Ideas and improvements
│   ├── deployments/   # Deployment records (enterprise)
│   └── incidents/     # Incident reports (enterprise)
└── who/               # People and coordination
    ├── customers/     # Client records (enterprise)
    ├── partners/      # Vendor relationships (enterprise)
    ├── contacts/      # Individual contacts (enterprise)
    ├── projects/      # Client projects (enterprise)
    ├── coordination/  # Cross-agent notes (team mode)
    └── governance/    # Roles and policies
```

## Entry Points

| Starting point | When to use |
|---------------|-------------|
| `CLAUDE.md` | Agent orientation (auto-loaded) |
| `STATE.md` | Current status and next steps |
| `who/customers/` | Client management |
| `how/deployments/` | Deployment tracking |
