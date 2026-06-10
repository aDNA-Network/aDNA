---
type: context_core
topic: claude_code
subtopic: memory_integration
created: 2026-03-27
updated: 2026-04-03
sources: ["Claude Code auto-memory documentation", "aDNA operational protocols", "AgentDB implementation patterns"]
context_version: "1.0"
token_estimate: ~3000
last_edited_by: agent_init
runtime: claude_code
tags: [context, claude_code, memory, persistence, auto_memory, agentdb, learnings]
quality_score: 4.4
signal_density: 5
actionability: 5
coverage_uniformity: 5
source_diversity: 2
cross_topic_coherence: 5
freshness_category: stable
last_evaluated: 2026-04-03
---

# System Configuration: Memory Integration

> **Runtime scope:** This file documents the Claude Code implementation. The underlying pattern applies to any runtime; only the implementation details are Claude Code-specific.

AI-native projects need four distinct persistence layers, each serving a different purpose. No single system handles all needs. This file documents how Claude Code's native auto-memory composes with aDNA's custom persistence to form a complete memory architecture.

---

## Key Principles

1. **Four persistence layers** -- each layer exists because it solves a problem the others cannot.

| Layer | What It Stores | Who Writes | Persistence | Loaded When |
|-------|---------------|-----------|-------------|-------------|
| **Auto Memory** | User identity, preferences, corrections, reference paths | Claude (automatically) | Cross-session, per project scope | Every session start (first 200 lines of MEMORY.md) |
| **Learnings (_learnings.md)** | Technical patterns, failure modes, rule evolutions | Agent (explicitly) | Cross-session, per vault | On demand or session start |
| **AgentDB (agent.db)** | Contracts, errors, checkpoints, operational state | Agent (explicitly) | Cross-session, per project/vault | Session start query |
| **Active Context (active.md)** | Current session state, in-progress work, handoff notes | Agent (explicitly) | Single session (or until cleared) | Current session only |

2. **CLAUDE.md is prescriptive; Auto Memory is descriptive** -- CLAUDE.md contains rules you write and enforce ("always do X"). Auto Memory contains observations Claude makes ("user prefers Y, confirmed on date Z"). Both load at session start, but they serve opposite roles. Never duplicate between them.

3. **Auto Memory is Claude Code's native system** -- stored at `~/.claude/projects/<project-path>/memory/`. Claude writes it automatically when it learns something about the user, receives corrections, or discovers reference information. The index file (MEMORY.md) auto-loads at session start (first 200 lines). Topic files are referenced from the index and loaded on demand.

4. **Auto Memory types** -- four categories, each serving identity and behavioral memory:

| Type | Purpose | Example |
|------|---------|---------|
| `user` | Role, expertise, responsibilities, knowledge level | "Senior engineer, prefers terse output" |
| `feedback` | Corrections and confirmed approaches | "Never add Co-Authored-By to commits" |
| `project` | Ongoing work, goals, deadlines, stakeholder context | "Auth rewrite targeting v2.3 release" |
| `reference` | Where to find things in external systems | "Bugs tracked in Linear project INGEST" |

5. **Learnings vs Auto Memory boundary** -- Auto Memory captures user-facing preferences and identity. Learnings capture technical patterns and failure modes. The test: "Is this about the user or about the technology?" User --> Auto Memory. Technology --> _learnings.md. Both --> prefer Auto Memory for the user aspect, _learnings.md for the technical aspect.

6. **AgentDB vs Learnings boundary** -- Learnings are human-readable markdown, appended over time, useful for pattern scanning. AgentDB is structured SQL data -- queryable, pruneable, with reinforcement counts and timestamps. The test: "Do I need to query this or just scan it?" Query --> AgentDB. Scan --> _learnings.md.

7. **Scope determines which memories load** -- Auto-memory is per project scope. Changing directories changes which memories load. Use this intentionally: vault-level memories for broad patterns, project-level for specific context. AgentDB follows the same pattern with per-project databases that can optionally sync upward to vault-level.

8. **200-line MEMORY.md limit** -- Claude Code only auto-loads the first 200 lines of the index file. Content past that threshold requires explicit reads. Keep the index lean; put detail in topic files referenced from the index.

---

## Layer Composition Model

The four layers form a stack with decreasing persistence and increasing specificity:

```
+--------------------------------------------------+
| Auto Memory (cross-session, cross-conversation)  |  Identity layer
|  "Who is this user? What do they prefer?"        |  Claude-written
+--------------------------------------------------+
| Learnings (cross-session, per vault)             |  Knowledge layer
|  "What technical patterns have we discovered?"   |  Agent-written
+--------------------------------------------------+
| AgentDB (cross-session, per project)             |  State layer
|  "What contracts/errors/checkpoints are active?" |  Agent-written
+--------------------------------------------------+
| Active Context (single session)                  |  Working layer
|  "What am I doing right now?"                    |  Agent-written
+--------------------------------------------------+
```

**Information flows upward on discovery, downward on load.** A session discovers a pattern (active context) --> records it (AgentDB or learnings) --> if it's about the user, Claude auto-captures it (auto memory). At session start, information flows downward: auto memory loads first, then AgentDB queries, then learnings scan, then active context resumes.

---

## Routing Table: What Goes Where

| Information | Correct Layer | Why |
|-------------|--------------|-----|
| "User is a senior engineer, prefers terse output" | Auto Memory (user) | About the user, not the code |
| "Never add Co-Authored-By to commits" | Auto Memory (feedback) OR CLAUDE.md | Correction --> feedback; non-negotiable rule --> CLAUDE.md |
| "WAL mode prevents SQLite locking under concurrent reads" | _learnings.md | Technical pattern, vault-wide relevance |
| "Auth middleware rewrite in progress, 3/5 files done" | AgentDB (contract) | Operational state, needs structured query |
| "Currently refactoring the payment module" | active.md | Session-scoped, ephemeral |
| "Bugs tracked in Linear project INGEST" | Auto Memory (reference) | External system pointer |
| "Gmail OAuth token expires every ~2 weeks" | Auto Memory (feedback) + _learnings.md | User-facing gotcha + technical pattern |
| "Session S-2026-0327-001 completed migration" | AgentDB (checkpoint) | Structured operational record |
| "User corrected: use 2-space indent in YAML" | Auto Memory (feedback) | Behavioral correction |
| "Python 3.12 broke our subprocess calls" | _learnings.md | Technical failure mode |

**Decision heuristic in order:**
1. Is it about the user? --> Auto Memory
2. Is it a non-negotiable rule? --> CLAUDE.md
3. Is it a technical pattern? --> _learnings.md
4. Does it need structured query? --> AgentDB
5. Is it ephemeral? --> active.md

---

## File Layout

Full memory landscape for a project:

```
~/.claude/
├── CLAUDE.md                              # Global: agent protocol, universal rules
├── projects/
│   └── -Users-me-lattice-my_project/
│       └── memory/                        # Auto Memory (Claude-written)
│           ├── MEMORY.md                  # Index (first 200 lines auto-load)
│           ├── user_profile.md            # type: user
│           ├── feedback_no_summaries.md   # type: feedback
│           ├── project_current_sprint.md  # type: project
│           └── reference_deploy_paths.md  # type: reference

~/aDNA/my_project/
├── .claude/CLAUDE.md                      # Project: prescriptive rules
├── _meta/
│   ├── _learnings.md                      # Technical patterns (human-readable)
│   ├── agentdb/
│   │   └── agent.db                       # Operational state (SQL-queryable)
│   └── context/
│       └── active.md                      # Current session state
```

---

## Auto Memory File Format

Each topic file in the auto-memory directory follows this structure:

```markdown
---
name: no trailing summaries
description: user wants terse output, no recap after completing tasks
type: feedback
---

Don't summarize what was just done at the end of responses. The user
reads diffs directly.

**Why:** User explicitly corrected this behavior -- they find summaries
redundant.
**How to apply:** After completing any task, stop. Don't add "Here's
what I did" paragraphs.
```

The `type` field matches one of the four auto-memory types (user, feedback, project, reference). The `name` field is a short identifier. The body contains the actual memory content with application guidance.

---

## Recommendations

| # | Recommendation | Rationale |
|---|---------------|-----------|
| 1 | Let auto-memory handle user identity and preferences | Don't manually encode "user prefers X" in CLAUDE.md -- Claude learns it from corrections |
| 2 | Use CLAUDE.md for non-negotiable rules | Rules that must survive even if auto-memory is cleared belong in CLAUDE.md |
| 3 | Use _learnings.md for vault-wide technical patterns | Technical discoveries that benefit the whole vault, not just one project |
| 4 | Use AgentDB for queryable operational state | Active contracts, error patterns, session checkpoints -- anything that needs SQL |
| 5 | Use active.md for session handoff | Without explicit state capture, agents lose context on session boundaries |
| 6 | Keep MEMORY.md index under 200 lines | Content past line 200 won't auto-load; use topic files for detail |
| 7 | Review auto-memory periodically | Stale memories (outdated preferences, completed projects) create noise |
| 8 | Use project scoping intentionally | Vault-level memories for broad patterns, project-level for specific context |
| 9 | Don't fight the auto-capture | If Claude keeps recording something, it's probably useful -- refine the wording rather than deleting |
| 10 | Cross-reference, don't duplicate | If a pattern exists in _learnings.md, reference it from auto-memory rather than restating it |

---

## Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|-------------|---------|-----------------|
| Encoding preferences in CLAUDE.md that Claude would learn naturally | Creates maintenance burden and duplication | Let auto-memory capture preferences from corrections |
| Using auto-memory for technical patterns | Wrong layer -- it's for user identity and behavior | Use _learnings.md for engineering knowledge |
| Storing operational state in _learnings.md | Append-only markdown is not queryable | Use AgentDB for state that needs structured access |
| Ignoring the 200-line MEMORY.md limit | Content past line 200 silently fails to auto-load | Use topic files referenced from a lean index |
| No active.md for session handoff | Agents lose context on session boundaries | Always write session state before closing |
| Single persistence layer for everything | Each layer has a purpose; overloading one creates confusion | Route information to the correct layer using the decision heuristic |
| Manual memory management only | Missing auto-captured insights that Claude notices | Let auto-memory complement explicit persistence |
| Duplicating between CLAUDE.md and auto-memory | Conflicting sources of truth when one updates | CLAUDE.md for rules, auto-memory for observations -- distinct purposes |

---

## Session Lifecycle Integration

How the four layers interact during a typical session:

**Session Start:**
1. Claude Code loads CLAUDE.md (prescriptive rules)
2. Claude Code loads MEMORY.md first 200 lines (descriptive identity)
3. Agent queries AgentDB for active contracts, recent errors, relevant learnings
4. Agent scans _learnings.md for patterns relevant to current domain
5. Agent checks active.md for any prior session handoff notes

**During Session:**
- Claude auto-captures corrections and discoveries to auto-memory
- Agent writes operational state changes to AgentDB
- Agent appends technical discoveries to _learnings.md
- Agent updates active.md with current progress

**Session End:**
- Agent writes SITREP with session summary
- Agent checkpoints to AgentDB (close contracts, record learnings)
- Agent updates active.md with handoff notes for next session
- Claude may auto-capture session-level insights to memory

---

## Sources

- Claude Code auto-memory documentation -- MEMORY.md format, type system, auto-load behavior, project scoping
- aDNA operational protocols -- _meta/ conventions, session lifecycle, _learnings.md format
- AgentDB implementation patterns -- SQLite schema, contract protocol, learning capture
