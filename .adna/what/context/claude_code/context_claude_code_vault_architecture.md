---
type: context_guide
topic: claude_code
subtopic: vault_architecture
created: 2026-03-27
updated: 2026-04-03
sources: ["aDNA Standard v2.2", "Claude Code project scoping"]
context_version: "1.1"
token_estimate: ~1100
last_edited_by: agent_init
runtime: claude_code
tags: [context, claude_code, vault_architecture, multi_vault, organization]
quality_score: 4.2
signal_density: 5
actionability: 4
coverage_uniformity: 4
source_diversity: 2
cross_topic_coherence: 5
freshness_category: stable
last_evaluated: 2026-04-03
---

# System Configuration: Vault Architecture

> **Runtime scope:** Claude Code implementation. The underlying pattern is runtime-agnostic.

Multi-vault organization for AI-native projects. Humans browse in Obsidian; agents operate via Claude Code.

For directory trees and file locations, see CLAUDE.md Vault Map.

---

## Core Invariants

1. **Multi-vault separation** — split by domain. Each vault = Obsidian vault + Claude Code project scope. Narrower context for agents, cleaner nav for humans.
2. **`_meta/` as operational layer** — all generated output (plans, reports, logs, memory) routes here. Source directories stay clean. Gitignored at every repo root.
3. **`.claude/` is READ-ONLY** — configuration only (CLAUDE.md, settings, rules, hooks). Never write generated content here.
4. **Output routing discipline** — every artifact has a canonical `_meta/` subdirectory (see table below).

## Output Routing Table

| Artifact | `_meta/` subdir |
|----------|----------------|
| Plans | `plans/` |
| Generated docs | `docs/` |
| Session state | `context/` |
| Cost tracking | `logs/` |
| Reports & audits | `reports/` |
| Agent memory | `agentdb/` (SQLite) |
| Research cache | `research/` |
| On-demand rules | `reference/` |

---

## Governance Cascade

Configuration inherits top-down. Each level adds rules but must not contradict parents.

```
~/.claude/CLAUDE.md              # Global: identity, core obligations
  └── ~/aDNA/CLAUDE.md        # Workspace: shared invariants
      └── vault/.claude/         # Vault: domain conventions
          └── project/.claude/   # Project: specific overrides
```

**Absolute paths required** when reading/writing `_meta/`. Sub-repos with their own `_meta/` silently route to the wrong database if you rely on `$PWD`.

---

## Vault Root Requirements

Every vault root needs: `.claude/CLAUDE.md`, `.gitignore` (excluding `_meta/`), and a `_meta/` directory. Optionally: project-level `CLAUDE.md`, `MANIFEST.md`, `STATE.md`.

## Recommendations

- Start with 2 vaults max (code + everything else). Split further only when it reduces context noise.
- Keep workspace `CLAUDE.md` minimal — it inherits from global and adds workspace-level rules only.
- Keep the base template repo (e.g., `adna/`) as read-only upstream. Fork for actual work.
- Each project gets its own `_meta/agentdb/agent.db`. Cross-project memory at workspace level.

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|-----------|
| Write generated content to `.claude/` | Violates READ-ONLY invariant | Route to `_meta/` |
| Single monolithic vault | Agents load irrelevant context | Split by domain |
| Skip `_meta/` separation | Generated and source content mix | Create `_meta/` at every level |
| Hardcode absolute paths in configs | Breaks portability | Use env vars or relative paths |
| Nest beyond 3 levels (workspace > vault > project) | Cognitive overhead without benefit | Flatten; use naming conventions |
| Share `_meta/` via git | Causes conflicts, leaks session data | Gitignore at every repo root |

## When to Create a New Vault

New vault if: fundamentally different file types, agents need narrower context, or collaborators need different access. Otherwise: same vault, new subdirectory.

---

## Sources

- **aDNA Standard v2.2** — triad structure, governance files, entity types
- **Claude Code project scoping** — `.claude/` scope chain, global-to-project inheritance
