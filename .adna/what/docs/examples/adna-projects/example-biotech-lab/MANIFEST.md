---
type: manifest
created: 2026-03-19
updated: 2026-03-19
status: active
last_edited_by: agent_init
tags: [manifest, biotech]
---

# example-biotech-lab

## What This Is

A rare disease genomics research lab tracking experiments, compound libraries, and therapeutic targets.

## Architecture

This project uses the aDNA knowledge architecture:

```
example-biotech-lab/
├── CLAUDE.md          # Agent governance
├── MANIFEST.md        # This file — project overview
├── STATE.md           # Current phase and next steps
├── README.md          # Human getting-started guide
├── what/              # Knowledge objects and context
│   ├── context/       # Domain knowledge library
│   ├── decisions/     # Architecture decisions
│   ├── experiments/   # Experiment records (biotech)
│   ├── compounds/     # Compound library (biotech)
│   ├── protocols/     # SOPs and protocols (biotech)
│   └── targets/       # Therapeutic targets (biotech)
├── how/               # Operations and processes
│   ├── missions/      # Multi-session plans
│   ├── sessions/      # Session tracking
│   ├── templates/     # Reusable templates
│   └── backlog/       # Ideas and improvements
└── who/               # People and coordination
    ├── coordination/  # Cross-agent notes
    └── governance/    # Roles and policies
```

## Entry Points

| Starting point | When to use |
|---------------|-------------|
| `CLAUDE.md` | Agent orientation (auto-loaded) |
| `STATE.md` | Current status and next steps |
| `what/experiments/` | Experiment tracking |
| `what/targets/` | Therapeutic target profiles |
