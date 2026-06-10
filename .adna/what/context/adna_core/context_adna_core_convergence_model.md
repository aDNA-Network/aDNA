---
type: context_core
topic: adna_core
subtopic: convergence_model
created: 2026-02-20
updated: 2026-03-18
sources: ["aDNA Standard v2.1 (§8.7, §10)", "aDNA Design Document (§3, §6)", "campaign_adna_review operational data (126+ sessions)"]
context_version: "1.0"
token_estimate: ~500
last_edited_by: agent_init
tags: [context, adna_core, convergence, token_budget, narrowing]
quality_score: 4.0
signal_density: 4
actionability: 5
coverage_uniformity: 4
source_diversity: 3
cross_topic_coherence: 4
freshness_category: durable
last_evaluated: 2026-02-20
---

# aDNA Core: Convergence Model — Operational Quick-Reference

> **Scope note**: This file is the operational quick-reference for applying the convergence model in daily work. For the full articulation (convergent narrowing model, structural parallel table, mathematical note), see `prompt_engineering/convergence_model`.

## Key Principles

1. **Each execution level narrows context.** Campaign → Mission → Objective is a monotone-decreasing chain of working sets. At each level, irrelevant knowledge is pruned.

2. **AGENTS.md is the routing mechanism.** Each directory's AGENTS.md tells agents what this directory contains and whether to load or skip. The Load/Skip Decision section implements selective loading — it selects the relevant subset.

3. **Token budget decreases at each level.** The total tokens an agent needs decreases monotonically as specificity increases:

| Level | Typical Scope | ~Tokens | Reduction |
|-------|--------------|---------|-----------|
| Instance (full vault) | All knowledge | ~500K | — |
| Campaign | Strategic initiative | ~50K | 90% |
| Mission | Decomposed task | ~15K | 70% |
| Objective | Single session work | ~5K | 67% |

## How to Apply

### When Designing Structures

| Decision | Convergent (prefer) | Divergent (avoid) |
|----------|-------------------|-------------------|
| Directory organization | Flat with AGENTS.md routing | Deep nesting requiring traversal |
| Context file scope | One subtopic per file, 150-300 lines | Monolithic topic files |
| Frontmatter fields | Minimal, queryable, typed | Verbose, unstructured |
| AGENTS.md content | Load/Skip decision + token estimate | Exhaustive listings |
| Campaign scope | Phased with gates | Unbounded "improve everything" |
| Mission decomposition | 3-7 objectives per mission | Single-objective or 15+ |

### When Starting a Session

1. **Read CLAUDE.md** — orient to full instance (~2K tokens)
2. **Read STATE.md** — narrow to current operational state (~3K tokens)
3. **Identify campaign/mission** — narrow to strategic initiative (~1K tokens)
4. **Load only needed context** — use topic AGENTS.md to select subtopics
5. **Claim specific objectives** — narrow to session work

### When Creating Content

Apply the **context window test**: "If an agent loaded this file, would every section help them complete their current objective?" If a section helps only a different objective, it belongs in a different file.

## Worked Example: Token Narrowing

From the org_formation merge (M9 worked example):

| Level | Entity Types | Reduction |
|-------|-------------|-----------|
| Full merged ontology | 32 types | — |
| Campaign: org_formation | 22 types (CRM + Science pruned) | 32 → 22 (31%) |
| Mission: Role Architecture (M5) | 5 types | 22 → 5 (77%) |
| Objective: Draft role charters | 2 types | 5 → 2 (60%) |

## Anti-Patterns

1. **Loading entire topics.** Never `read what/context/{topic}/*` — always read the AGENTS.md first and select subtopics.
2. **Flat session intent.** A session with intent "work on the project" fails to narrow — use specific mission/objective references.
3. **Monolithic context files.** A 10,000-token context file defeats the purpose of selective loading.
4. **Missing AGENTS.md.** A directory without AGENTS.md is invisible to convergent routing — agents must guess whether to enter.
5. **Unbounded campaigns.** A campaign without phases and gates never converges.

## Sources

1. aDNA Standard v2.1 — §8.7 (75% Rule), §10 (Context Library token budgets)
2. aDNA Design Document — §3 (triad question test), §6 (session model)
3. Operational data — 126+ sessions across 5 campaigns demonstrating convergent narrowing
