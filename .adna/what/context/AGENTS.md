---
type: directory_index
created: 2026-02-17
updated: 2026-03-28
last_edited_by: agent_aria
tags: [directory_index, context]
---

# Context Library — Agent Knowledge Store

## Purpose

Curated, validated context files that agents load when they need domain expertise. The context library lives in `what/context/` as part of the knowledge layer.

## Directory Structure

```
what/context/
├── AGENTS.md                                    # This file (library protocol + topic index)
└── {topic}/                                     # One directory per validated topic
    ├── AGENTS.md                                # Topic index (subtopics, token estimates, usage notes)
    └── context_{topic}_{subtopic}.md            # One file per subtopic
```

## Agent Usage Protocol

1. **Check** `what/context/` for relevant topics before starting domain-specific tasks
2. **Read** the topic `AGENTS.md` to understand available subtopics and their token estimates
3. **Load only relevant subtopics** — budget your context window; don't load everything
4. **Cite** loaded context files in your session log (`files_modified` or activity log)
5. **If context is outdated or incomplete**, flag with `#context-update-needed`

## Context Subtypes

Context files use the `type` frontmatter field to distinguish content subtypes:

| Subtype | Purpose | Pattern |
|---------|---------|---------|
| `context_research` | Synthesized domain knowledge from external sources | Dense, citational, comprehensive |
| `context_guide` | Prescriptive component or tool guides | Step-by-step, actionable, reference-oriented |
| `context_core` | Foundational project definitions (conventions, guardrails, stack) | Concise, authoritative, rarely changing |

All subtypes coexist in `what/context/` organized by topic. The subtype informs how agents use the content, not where it lives.

Template: `how/templates/template_context.md`

## Context File Format

### Frontmatter

```yaml
---
type: context_research
topic: {topic}
subtopic: {subtopic}
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: ["source 1", "source 2"]
context_version: "1.0"
token_estimate: ~NNNN
last_edited_by: agent_{username}
tags: [context, {topic}]
# Quality evaluation (optional — added during Phase 3 review or quality audit)
# quality_score: 4.2          # composite average of 5 numeric axes
# signal_density: 4            # 1-5
# actionability: 5             # 1-5
# coverage_uniformity: 4       # 1-5
# source_diversity: 4          # 1-5
# cross_topic_coherence: 4     # 1-5
# freshness_category: stable   # volatile | stable | durable | mixed
# last_evaluated: YYYY-MM-DD
---
```

### Quality Evaluation

Context files may include quality scores from the 6-axis evaluation rubric (see `what/docs/context_quality_rubric.md`). Quality scoring is mandatory for `standard`+ effort deep research output and optional for other context files. The composite `quality_score` is the simple average of 5 numeric axes; `freshness_category` is categorical. **Floor rule**: any axis ≤ 2 flags the file for revision.

### Body Structure

```markdown
# {Topic}: {Subtopic}

## Key Principles
[3-7 core principles, most important first]

## Recommendations
[Specific, actionable recommendations with rationale]

## Examples / Snippets
[Code blocks, YAML, config examples]

## Anti-Patterns (optional)
[Common mistakes to avoid]

## Sources
[Attributed source list]
```

## Topic Index Format

Each topic directory contains an `AGENTS.md` with:

```markdown
# {Topic} — Context Index

## Overview
[1-2 sentence description of what this topic covers]

## Subtopics

| Subtopic | File | Token Estimate | Version | Sources |
|----------|------|---------------|---------|---------|
| {name} | `context_{topic}_{subtopic}.md` | ~NNNN | 1.0 | N sources |

## Total Token Budget
~NNNN tokens to load all subtopics

## Usage Notes
[When to load this topic, which tasks benefit from it, any caveats]
```

## Quality Standards

Every context file should meet these standards:

- **Self-contained** — no required external reads to be useful
- **Actionable** — instructions and recommendations, not just descriptions
- **Token-efficient** — 150-300 lines per file (~2000-4000 tokens)
- **Source-attributed** — every claim traceable to a source

## Cross-Topic Recipes

Pre-defined context assemblies for multi-disciplinary tasks. See `context_recipes.md` for the full index, 3-tier budget system, and task classification heuristic. Recipes encode known-good subtopic combinations — agents can always load subtopics manually.

## Available Topics

| Topic | Subtopics | Total Tokens | Avg Quality | Status |
|-------|-----------|-------------|-------------|--------|
| prompt_engineering | 7 | ~21,200 | 4.2 | active |
| adna_core | 10 | ~29,500 | 4.2 | active |
| lattice_basics | 2 | ~6,000 | 4.0 | active |
| object_standards | 1 | ~3,200 | 3.8 | active |
| claude_code (Claude Code runtime) | 4 | ~10,000 | — | active |

## Load/Skip Decision

**Load this directory when**:
- Starting domain-specific work and need to check whether relevant context exists
- Creating a new context topic or subtopic (follow the format and quality standards above)
- Evaluating context quality using the 6-axis rubric (see `what/docs/context_quality_rubric.md`)

**Skip when**:
- Performing routine operational work that doesn't require domain expertise
- Already loaded the specific topic's AGENTS.md and subtopics you need
- Working on missions, campaigns, or backlog without domain research needs

**Token budget awareness**: This AGENTS.md is ~1,100 tokens. Each topic has its own AGENTS.md (~300-400 tokens) with a subtopic index. Load the topic index first, then only the subtopics you need — never load an entire topic directory blindly.

**Token cost**: ~1,100 tokens (this AGENTS.md)
