---
type: directory_index
created: 2026-03-27
updated: 2026-03-28
token_estimate: 10000
last_edited_by: agent_aria
runtime: claude_code
tags: [directory_index, context, claude_code]
---

# Claude Code — Context Index

## Overview

Technical knowledge about the Claude Code operating environment for aDNA projects. This topic is **runtime-specific** — it documents how Claude Code implements the patterns that underpin aDNA (config cascade, lifecycle hooks, vault architecture, persistence layers). Agents on other runtimes should reference their own runtime documentation and can use this topic as a reference implementation example.

This topic is part of a **cross-triad domain** (see ADR-003). Governance and operational components live in their triad-correct locations; this directory holds the WHAT (technical knowledge) portion:

| Component | Triad | Location |
|-----------|-------|----------|
| Agent protocol | WHO | `who/governance/governance_agent_protocol.md` |
| Orchestration tiers | HOW | `how/skills/skill_orchestration_tiers.md` |
| SQLite persistence pattern | HOW | `how/skills/skill_sqlite_persistence.md` |
| Vault architecture | WHAT | this directory |
| Config cascade | WHAT | this directory |
| Hook system | WHAT | this directory |
| Memory integration | WHAT | this directory |
| **Full topology** | — | `what/lattices/examples/claude_code.lattice.yaml` |

## Subtopics

| # | Subtopic | File | ~Tokens | Subtype | Key Content |
|---|----------|------|---------|---------|-------------|
| 1 | Vault Architecture | `context_claude_code_vault_architecture.md` | ~2,500 | context_guide | Multi-vault separation, .claude/ read-only, workspace convention |
| 2 | Config Cascade | `context_claude_code_config_cascade.md` | ~2,000 | context_core | CLAUDE.md inheritance, rules modularization, settings layering, token budgets |
| 3 | Hook System | `context_claude_code_hook_system.md` | ~2,500 | context_guide | 6 lifecycle events, guard pattern, auto-approve, pre-compaction, async vs blocking |
| 4 | Memory Integration | `context_claude_code_memory_integration.md` | ~3,000 | context_core | Four persistence layers, persistence model, layer boundaries |

## Total Token Budget

~10,000 tokens to load all subtopics. Typical session loads 2-3 subtopics (~4K-5K tokens).

For the full system picture (~14K tokens), also load:
- `who/governance/governance_agent_protocol.md` (~1,900 tokens)
- `how/skills/skill_orchestration_tiers.md` (~2,100 tokens)
- `how/skills/skill_sqlite_persistence.md` — if setting up cross-session state querying

## Usage by Task

| Task | Load |
|------|------|
| Setting up a new workspace | vault_architecture, config_cascade |
| Configuring agent behavior | `who/governance/governance_agent_protocol.md`, config_cascade |
| Adding lifecycle hooks | hook_system, config_cascade |
| Adding cross-session state querying | `how/skills/skill_sqlite_persistence.md` |
| Planning multi-agent work | `how/skills/skill_orchestration_tiers.md`, `how/skills/skill_sqlite_persistence.md` |
| Understanding where to store what | memory_integration, vault_architecture |
| Debugging config inheritance | config_cascade, hook_system |
| Onboarding a new agent | `who/governance/governance_agent_protocol.md`, vault_architecture, memory_integration |
| Navigating full topology | `what/lattices/examples/claude_code.lattice.yaml` |

## Dependency Notes

- **vault_architecture** and **config_cascade** are complementary — architecture defines structure, cascade defines how configuration flows through that structure
- **hook_system** depends on config_cascade — hooks are configured in settings files
- **memory_integration** is the capstone — references all other components to explain how the layers compose
- **skill_sqlite_persistence** (`how/skills/`) is the operational counterpart — not a context file, but the companion skill for adding a queryable state layer
- The **claude_code.lattice.yaml** context graph models all 8 components (including cross-triad ones) as nodes with directed edges showing dependency flow

## Load/Skip Decision

**Load when**:
- Setting up or configuring a new aDNA workspace or vault
- Troubleshooting hook failures, config inheritance, or memory issues
- Onboarding a new agent or explaining the operating environment

**Skip when**:
- Working on domain-specific content (ontologies, lattices, campaigns)
- Performing routine session work in an already-configured vault
- Need agent protocol only → load `who/governance/` directly
- Need orchestration only → load `how/skills/skill_orchestration_tiers.md` directly

**Skip entirely** when running aDNA on a non-Claude Code runtime — this topic documents Claude Code specifics.

**Token cost**: ~500 tokens (this AGENTS.md)
