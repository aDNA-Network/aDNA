---
type: context_core
topic: claude_code
subtopic: config_cascade
created: 2026-03-27
updated: 2026-04-03
sources: ["Claude Code documentation", "aDNA Standard v2.2", "Claude Code settings hierarchy"]
context_version: "1.0"
token_estimate: ~2000
last_edited_by: agent_init
runtime: claude_code
tags: [context, claude_code, config_cascade, claude_md, inheritance]
quality_score: 4.0
signal_density: 4
actionability: 5
coverage_uniformity: 4
source_diversity: 2
cross_topic_coherence: 5
freshness_category: stable
last_evaluated: 2026-04-03
---

# System Configuration: Config Cascade

> **Runtime scope:** This file documents the Claude Code implementation. The underlying pattern applies to any runtime; only the implementation details are Claude Code-specific.

How CLAUDE.md files, rules, and settings layer from global scope down to individual projects. Understanding this cascade is essential for keeping agent context lean, non-redundant, and correctly scoped.

---

## Key Principles

### 1. Three-Tier CLAUDE.md Inheritance

Claude Code loads CLAUDE.md files from three scopes, merged in order:

| Tier | Path | Scope | What Belongs Here |
|------|------|-------|-------------------|
| Global | `~/.claude/CLAUDE.md` | All projects, all repos | Agent identity, universal protocol, autonomy rules |
| Workspace | `<workspace>/.claude/CLAUDE.md` | All projects in a workspace | Session workflow, commit conventions, shared tooling |
| Project | `<project>/.claude/CLAUDE.md` | Single repo or subdirectory | Stack-specific gates, domain glossary, project map |

Each level adds specificity. Content flows downward; child levels never repeat parent rules.

### 2. Rules Modularization

`.claude/rules/*.md` files extend CLAUDE.md without bloating it. Each file covers one concern:

- **invariants.md** -- security contracts, data integrity, non-negotiable rules
- **patterns.md** -- naming conventions, error handling, logging standards
- **preferences.md** -- formatting, tooling, commit style (negotiable defaults)
- **parallel-first.md** -- execution strategy for multi-task work

Rules files are loaded automatically alongside CLAUDE.md. They count against the session token budget, so keep each one focused (under 80 lines).

### 3. Settings Layering

Two settings files control Claude Code behavior at the project level:

| File | Checked In | Purpose |
|------|-----------|---------|
| `.claude/settings.json` | Yes | Shared team settings: default permissions, hooks |
| `.claude/settings.local.json` | No (gitignored) | Personal overrides: local permissions, env vars, MCP servers |

Local settings merge over shared settings. When both define the same key, local wins.

### 4. Token Budget Awareness

CLAUDE.md loads every session, every conversation. This makes it high-value real estate with a real cost:

- **Target**: under 200 lines per CLAUDE.md file
- **Escape hatch**: move verbose reference material to `_meta/reference/` and load on demand
- **Rules files add up**: 4 rules files at 60 lines each = 240 lines of always-loaded context
- **Audit periodically**: if your combined always-loaded context exceeds 500 lines, refactor

### 5. Inheritance Principle

Each level contains only what is NEW at that scope. Never duplicate upward content:

- Global says "search before asking" -- project does not repeat this
- Workspace says "commit immediately after push" -- project does not repeat this
- Project says "use pytest, 4-space indent" -- this is new, project-specific

If you find yourself copying rules downward, the rule belongs at a higher level.

### 6. Auto-Memory Complements Config

Claude Code maintains auto-memory at `~/.claude/projects/<path-hash>/memory/`:

| Mechanism | Who Writes | Purpose |
|-----------|-----------|---------|
| CLAUDE.md | Human | Prescriptive -- rules, structure, protocol |
| Auto-memory | Claude | Descriptive -- learned preferences, corrections, project facts |

Both load at session start. Do not re-encode in CLAUDE.md what auto-memory already captured. Check memory files before adding "learned" rules to config.

---

## The Cascade Visualized

```
~/.claude/CLAUDE.md                        # Tier 1: Global
    |  Agent identity, universal protocol,
    |  autonomy framework, model routing
    |
    v  inherited by
~/aDNA/.claude/CLAUDE.md                # Tier 2: Workspace
    |  Session workflow, _meta routing,
    |  commit rules, AgentDB conventions
    |
    v  inherited by
~/aDNA/my_project/.claude/CLAUDE.md     # Tier 3: Project
    |  Domain map, quality gates, stack
    |  conventions, glossary
    |
    v  complemented by
~/aDNA/my_project/.claude/rules/        # Modular rule files
    ├── invariants.md                      # Security, data integrity
    ├── patterns.md                        # Naming, error handling
    ├── preferences.md                     # Formatting, tooling
    └── parallel-first.md                  # Execution strategy
```

---

## Minimal CLAUDE.md at Each Level

**Global** (`~/.claude/CLAUDE.md`):
```markdown
# Agent Protocol
- Search exhaustively before asking questions
- Push back on vague requests -- demand clarity
- State opinions, not options
- Autonomy: act on reversible, pause on destructive
```

**Workspace** (`~/aDNA/.claude/CLAUDE.md`):
```markdown
# Workspace Rules
- Session tracking: create file in how/sessions/active/ before work
- All generated output to _meta/, never to .claude/
- Commit immediately after each working state
- AgentDB paths must be absolute
```

**Project** (`~/aDNA/my_project/.claude/CLAUDE.md`):
```markdown
# Project: My Research Lab
- Stack: Python 3.12, pytest, ruff
- Quality gates: types check (mypy --strict), lint clean, tests pass
- Domain glossary: "target" = dataset_class: target, "lattice" = .lattice.yaml
- Project map: [directory tree here]
```

---

## Settings File Structure

**Shared settings** (`.claude/settings.json`, checked in):
```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep"],
    "deny": ["Bash(rm -rf *)"]
  }
}
```

**Local settings** (`.claude/settings.local.json`, gitignored):
```json
{
  "permissions": {
    "allow": ["Bash(git:*)", "Read", "Edit", "Write"]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash guard.sh"
          }
        ]
      }
    ]
  },
  "env": {
    "ENABLE_LSP_TOOL": "1",
    "PROJECT_ENV": "development"
  }
}
```

Hooks run before or after tool invocations. Use them for guardrails (pre-write validation), logging, or environment setup.

---

## Anti-Patterns

| Anti-Pattern | Why It Hurts | Fix |
|-------------|-------------|-----|
| Duplicating rules across levels | Token waste, drift risk when one copy updates | Put rule at highest applicable level only |
| Bloated CLAUDE.md (200+ lines) | Loads every session, crowds out conversation context | Extract to `rules/` files or `_meta/reference/` |
| Mixing shared and local settings | Personal permissions leak into team config via git | Keep personal config in `settings.local.json` only |
| Ignoring auto-memory | Re-encoding learned preferences Claude already tracks | Check `~/.claude/projects/` before adding "learned" rules |
| Hardcoded absolute paths | Breaks portability across machines and users | Use relative paths in project configs |
| Monolithic rules file | One huge `rules/everything.md` defeats modularization | One concern per file, under 80 lines each |
| Config without audit cycle | Stale rules accumulate, token budget creeps up | Review config quarterly, archive unused rules |

---

## Decision Checklist: Where Does This Rule Go?

```
Does it apply to ALL projects on this machine?
  YES --> ~/.claude/CLAUDE.md
  NO  --> Does it apply to all projects in this workspace?
            YES --> <workspace>/.claude/CLAUDE.md
            NO  --> <project>/.claude/CLAUDE.md
                    Is it verbose or rarely needed?
                      YES --> _meta/reference/ (load on demand)
                      NO  --> Is it a standalone concern?
                                YES --> .claude/rules/<concern>.md
                                NO  --> Keep in project CLAUDE.md
```

---

## Operational Notes

- **Load order**: Global CLAUDE.md, then workspace CLAUDE.md, then project CLAUDE.md, then all `.claude/rules/*.md` files, then auto-memory. Later content can override earlier content.
- **Conflict resolution**: when two levels contradict, the more specific (lower) level wins. Project overrides workspace overrides global.
- **Testing your config**: start a new Claude Code session and ask "what rules are you following?" to verify the cascade loaded correctly.
- **Migration**: when upgrading aDNA versions, check `how/skills/skill_version_migration.md` for config changes between versions.

---

## Sources

- **Claude Code documentation** -- CLAUDE.md loading behavior, settings hierarchy, auto-memory system, hooks API
- **aDNA Standard v2.2** -- governance file conventions, _meta routing, session protocol
- **Claude Code settings hierarchy** -- permissions model, environment variable layering, local vs shared config
