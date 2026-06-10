---
type: context_guide
topic: adna_core
subtopic: context_engineering
created: 2026-02-20
updated: 2026-03-18
sources: ["aDNA Standard v2.1 (§10)", "Context Quality Rubric v1.0", "Context library AGENTS.md", "prompt_engineering/signal_to_token operational patterns"]
context_version: "1.0"
token_estimate: ~1000
last_edited_by: agent_init
tags: [context, adna_core, context_engineering, quality, token_budget]
quality_score: 4.4
signal_density: 5
actionability: 5
coverage_uniformity: 4
source_diversity: 3
cross_topic_coherence: 4
freshness_category: stable
last_evaluated: 2026-02-20
---

# aDNA Core: Context Engineering Guide

## Key Principles

1. **Context files are agent fuel.** The context library (`what/context/`) is the single location for curated, validated knowledge that agents load before domain work. Every context file exists to help an agent make better decisions or produce better output.

2. **Three subtypes serve different purposes.**

| Subtype | Purpose | Token Density | Update Cadence |
|---------|---------|---------------|----------------|
| `context_research` | Synthesized domain knowledge from external sources | Dense, citational | When sources update |
| `context_guide` | Prescriptive how-to guides | Step-by-step, actionable | When procedures change |
| `context_core` | Foundational project definitions | Concise, authoritative | Rarely |

3. **Token budget is the primary constraint.** Files should be 150-300 lines (~2,000-4,000 tokens). Load only needed subtopics. Never load an entire topic directory.

4. **Every claim must be traceable.** The `sources` frontmatter field lists all sources. In-body references link claims to specific sources.

## How to Write a Context File

### Step 1: Choose Subtype and Scope

| If the content... | Use | Scope Rule |
|-------------------|-----|-----------|
| Synthesizes external research | `context_research` | One research question per file |
| Prescribes how to do something | `context_guide` | One procedure/workflow per file |
| Defines foundational conventions | `context_core` | One conceptual unit per file |

### Step 2: Write the Body

Follow this structure:

```markdown
# {Topic}: {Subtopic}

## Key Principles
[3-7 core principles, most important first. Tables over prose.]

## Recommendations
[Specific, actionable items with rationale. Decision tables preferred.]

## Examples / Snippets
[Code blocks, YAML, config examples. Show, don't tell.]

## Anti-Patterns (optional)
[Common mistakes to avoid with specific consequences.]

## Sources
[Attributed source list with enough detail to verify.]
```

### Step 3: Apply Quality Standards

Every context file must be:
- **Self-contained** — no required external reads to be useful
- **Actionable** — instructions and recommendations, not just descriptions
- **Token-efficient** — 150-300 lines per file
- **Source-attributed** — every claim traceable

### Step 4: Score Against Quality Rubric

| Axis | Score Range | What It Measures |
|------|-----------|------------------|
| Signal density | 1-5 | Fraction of tokens that are decision-relevant |
| Actionability | 1-5 | Can agent produce concrete output from this? |
| Coverage uniformity | 1-5 | Balanced depth across sections |
| Source diversity | 1-5 | Distribution across vendor/academic/practitioner/community/original |
| Cross-topic coherence | 1-5 | No conflicts with related files |
| Freshness half-life | Categorical | volatile / stable / durable / mixed |

**Composite** = average of 5 numeric axes. Target: 3.5+. **Floor rule**: any axis ≤ 2 flags for revision.

## Topic Organization

### Directory Structure

```
what/context/
├── AGENTS.md                              # Library index + topic table
└── {topic}/
    ├── AGENTS.md                          # Subtopic index + usage guide
    └── context_{topic}_{subtopic}.md      # One file per subtopic
```

### Topic AGENTS.md Must Include

| Section | Purpose |
|---------|---------|
| Overview | 1-2 sentence topic description |
| Subtopic table | File, token estimate, version, source count |
| Total token budget | Cost of loading everything |
| Usage by task | Task → recommended subtopic mappings |
| Load/Skip decision | When to load vs. skip this topic |

## Format Selection Guide

| Content Type | Best Format | Why |
|-------------|-------------|-----|
| Comparisons | Decision tables | Side-by-side, scannable |
| Procedures | Numbered steps | Sequential, unambiguous |
| Rules | Constraint tables | Structured, queryable |
| Examples | Code blocks with annotations | Directly executable |
| Principles | Numbered list | Priority-ordered, memorable |
| Taxonomies | Hierarchical tables | Classification at a glance |

## Context Composition System

Beyond individual files, the context library supports **cross-topic assembly recipes** — named, pre-defined combinations of subtopics for multi-disciplinary tasks.

| Concept | Description |
|---------|-------------|
| **Recipe** | A named list of subtopics to load together, with a token budget |
| **Three tiers** | Minimal (<5K), Standard (<12K), Full (all subtopics) |
| **Task classification** | Keyword matching to suggest the right recipe |
| **Recipe creation** | Identify pattern → list subtopics → calculate budget → add to index |

Recipe index: `what/context/context_recipes.md`. Load it when starting a task that spans multiple context topics.

## Anti-Patterns

1. **Prose-heavy context.** Tables deliver 3-5× more information per token than prose paragraphs. Default to tables.
2. **Missing AGENTS.md.** A topic without an index file is invisible to agents following the loading protocol.
3. **Monolithic files.** Split files >4,000 tokens into subtopics.
4. **Single-source context.** Source diversity ≤ 2 triggers the floor rule — diversify.
5. **Background preamble.** "In the rapidly evolving field of..." wastes tokens. Start with the first principle.
6. **Redundant coverage.** If two files cover the same concept, add a scope note distinguishing them.

## Sources

1. aDNA Standard v2.1 — §10 (Context Library structure, subtypes, token budgets)
2. Context Quality Rubric v1.0 — 6-axis evaluation framework with calibration
3. Context library AGENTS.md — library protocol and quality standards
4. Operational patterns from prompt_engineering/signal_to_token — format selection, token efficiency
