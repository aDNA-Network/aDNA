---
type: skill
skill_type: process
created: 2026-03-27
updated: 2026-03-28
status: active
category: operations
trigger: "Multi-file tasks, tier classification, agent spawning, model routing decisions"
last_edited_by: agent_aria
tags: [skill, orchestration, tiers, model_routing, parallel, agents]
requirements:
  tools: ["Agent spawning capability", "Shared coordination store (see skill_sqlite_persistence.md)"]
  context: ["what/context/claude_code/"]
  permissions: ["Ability to spawn sub-agents", "Read/write project state"]
---

# Skill: Orchestration Tiers

## Overview

Classify tasks by complexity, route to the right execution tier, spawn agents for parallel work, and coordinate via contracts. This skill governs how multi-file work gets decomposed and distributed.

The tier determines how many agents participate, whether adversarial review is required, and which models handle which subtasks. This replaces ad-hoc execution with a repeatable decision framework.

## Trigger

Any task touching 2+ files, or any request that needs scoping before execution. Also triggered when an agent is unsure whether to execute directly or delegate.

## Parameters

None — this is a process skill (mental model + decision procedure), not a parameterized automation.

## Implementation

### Step 1: Classify

Count files that will change. Determine tier.

| Tier | Files | Execution | Quality Gate |
|------|-------|-----------|-------------|
| 1 | 1-2 | Execute directly | Self-review |
| 2 | 3-5 | Orchestrate with surgeon agent(s) | Orchestrator review |
| 3 | 6+ | Surgeon agents + adversarial QA | Adversary review (up to 3 iterations) |
| Ambiguous | ? | Assume higher tier | Higher tier's gate |

**Decision rule:** When ambiguous, assume the higher tier. Downgrading is cheap; recovering from under-scoped work is expensive.

### Step 2: Route Model

Match task type to model class. Routing cheap work to expensive models is waste; routing critical work to cheap models is risk.

| Task Type | Model Class | Principle |
|-----------|------------|-----------|
| Drafts, brainstorm, variations | Fast/cheap | Iterate freely, cost near-zero |
| Web search, bulk reads (50+ files) | Large context | Leverage the context window |
| Secondary impl, synthesis, file writes | Balanced | Cost-effective quality |
| Planning, design, orchestration, review | Most capable | Quality over cost |
| Test execution, lint, typecheck | Fast | Trivial checks, fast feedback |

Define a routing table in your project's `CLAUDE.md` or rules file. Explicit routing prevents defaulting to the most expensive model for every task.

### Step 3: Load Skills

Check `how/skills/` for relevant methodology before acting. Loading order matters — primary skill sets the framework, secondary skills add gates.

| Task Type | Skills to Load |
|-----------|---------------|
| Building new features | build, quality, testing |
| Fixing bugs | debug, testing |
| Refactoring | refactor, architecture, quality |
| Code review | quality, testing, security |
| API work | api, backend, security |
| Frontend work | design, e2e, quality |
| Security audit | security, quality, testing |
| Performance work | performance, quality, testing |

Always load quality-related skills alongside implementation skills.

### Step 4: Execute by Tier

**Tier 1 — Direct execution:**
1. Read the file(s)
2. Implement the change
3. Run tests
4. Commit

No ceremony needed. One agent, one pass.

**Tier 2 — Contract and delegate:**
1. Write contract to shared coordination store (see `how/skills/skill_sqlite_persistence.md`) (goal, files, tier, success criteria, skills, branch)
2. Spawn surgeon agent(s) — parallel when files are independent
3. Review surgeon output
4. Run quality gates (tests, lint, typecheck)
5. Commit

The orchestrator does NOT write code. It writes contracts and reviews output.

**Tier 3 — Contract, delegate, and verify:**
1. Write contract to shared coordination store (see `how/skills/skill_sqlite_persistence.md`)
2. Spawn surgeon agent(s) — parallel when files are independent
3. Spawn adversary agent to review surgeon output
4. If adversary rejects: return to surgeons with feedback (max 3 iterations)
5. Run quality gates
6. Commit

Role separation at tier 2+:

| Role | Responsibility | Writes Code? |
|------|---------------|-------------|
| Orchestrator | Scope, plan, coordinate, review | No |
| Surgeon | Implement changes within contract scope | Yes |
| Adversary | Test, find edge cases, challenge assumptions | No (writes tests) |
| Validator | Run lint, typecheck, quality gates | No |

### Step 5: Coordinate

**Contract fields for tier 2+:**

| Field | Purpose |
|-------|---------|
| `goal` | What this work accomplishes |
| `files` | Exact files in scope (agents touch nothing else) |
| `tier` | Complexity classification |
| `success_criteria` | Measurable conditions for completion |
| `skills` | Which skills agents should load |
| `branch` | Git branch for isolation |

**Parallel-first rule:** When tasks decompose into independent work units, spawn parallel agents. Serial execution is the exception.

Detection:
- 2+ independent files to create or modify? Parallelize.
- 2+ independent systems to test or verify? Parallelize.
- Research + implementation + documentation? Parallelize.
- Any list of tasks in the description? Parallelize.

Only skip parallelization when the task is one step, steps are dependent (output of A feeds into B), or the user explicitly requests serial execution.

**Commit after every working state.** Small, frequent commits beat large batches. Each commit is a safe rollback point.

**Baseline before changing.** Run tests before making changes (baseline) and after (verification). Comparison catches regressions.

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Tier classification | Decision | Which tier the task falls into |
| Contract | Coordination store record | Goal, files, tier, success criteria for tier 2+ |
| Completed work | Files | Implemented changes passing quality gates |
| Quality gate results | Evidence | Test output, lint output, typecheck output |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Adversary rejects (tier 3) | Quality gate failure | Return to surgeons with feedback, max 3 retries then escalate to human |
| Tests fail after changes | Implementation bug | Diagnose, fix, re-execute. Compare against baseline to distinguish regressions from pre-existing failures |
| Blocked on missing info | Unclear scope or dependency | Checkpoint to shared coordination store and STOP. Ask human. Do not guess. |
| Scope creep detected | Agent touching files outside contract | Checkpoint and STOP. Orchestrator approves scope expansion or rejects |
| Model routing unclear | Task doesn't fit a clean category | Default to most capable model. Downgrade after first pass if overkill |

## Anti-Patterns

| Anti-Pattern | Why It Fails | Do This Instead |
|-------------|-------------|-----------------|
| Serial execution of independent tasks | 3x slower, wastes time and tokens | Spawn parallel agents |
| Orchestrator writing code at tier 2+ | Pollutes context window, blocks parallelism | Delegate to surgeon agents |
| No tier classification | Under-scoped work, missed edge cases | Count files, classify, then route |
| Skipping skill loading | Improvised approaches miss proven patterns | Load relevant skills before acting |
| One model for everything | Expensive model on lint = waste; cheap model on design = risk | Route by task type |
| No contract for multi-agent work | Agents duplicate effort or conflict | Write contract to shared coordination store |
| No baseline test run | Cannot distinguish pre-existing failures from regressions | Run tests before and after changes |
| Committing without quality gates | Broken code reaches the branch | Run gates before every commit |

## Integration with aDNA Execution Hierarchy

Orchestration tiers map to the Campaign/Mission/Objective hierarchy:

| aDNA Level | Typical Tier | Pattern |
|-----------|-------------|---------|
| Campaign | Tier 3 | Multi-mission coordination, phased execution |
| Mission | Tier 2-3 | Multi-objective, surgeon agents per objective |
| Objective | Tier 1-2 | Single-session, direct execution or small delegation |

Campaigns set strategic direction. Missions decompose into objectives. Objectives map to orchestration tiers for execution. The tier system handles the *how*; the hierarchy handles the *what* and *when*.

## Examples

### Tier Classification

```
User: "Add authentication middleware and update all route handlers"

Step 1 — Count files:
  auth middleware (1) + route handlers (likely 4+) = 5+ files

Step 2 — Classify:
  Tier 3 (6+ files, cross-cutting concern)

Step 3 — Route:
  Orchestrate -> surgeon agents -> adversary review

Step 4 — Load skills:
  build, security, quality
```

### Tier 2 Contract

```json
{
  "goal": "Add rate limiting to API endpoints",
  "files": [
    "src/middleware/rate-limit.ts",
    "src/config/limits.ts",
    "tests/rate-limit.test.ts"
  ],
  "tier": 2,
  "skills": ["build", "security", "testing"],
  "branch": "feat/rate-limiting",
  "success_criteria": [
    "Rate limiter applies to all /api routes",
    "Configurable per-endpoint limits",
    "Tests cover limit exceeded and reset scenarios"
  ]
}
```

### Parallel Agent Spawn

```
Spawning 3 parallel agents:

Agent 1 (surgeon): Implement rate-limit middleware
  -> Writes: src/middleware/rate-limit.ts
  -> Skills: build, security

Agent 2 (surgeon): Add configuration schema
  -> Writes: src/config/limits.ts
  -> Skills: build

Agent 3 (surgeon): Write test suite
  -> Writes: tests/rate-limit.test.ts
  -> Skills: testing

All agents write files directly.
Orchestrator reviews merged output.
Quality gates before commit.
```
