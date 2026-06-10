---
type: context_research
topic: prompt_engineering
subtopic: mermaid_best_practices
created: 2026-02-19
updated: 2026-04-03
sources: ["Mermaid.js docs", "Obsidian Forum — Mermaid rendering", "Anthropic — Context Engineering"]
context_version: "1.1"
token_estimate: ~700
last_edited_by: agent_init
tags: [context, prompt_engineering]
quality_score: 4.0
signal_density: 5
actionability: 4
coverage_uniformity: 4
source_diversity: 3
cross_topic_coherence: 4
freshness_category: stable
last_evaluated: 2026-04-03
---

# Prompt Engineering: Mermaid Diagram Best Practices

For Mermaid syntax reference, see [mermaid.js.org/syntax](https://mermaid.js.org/syntax/).

## Key Principles

1. **One concept per diagram.** Split by concern. A system overview, data flow, and ER model = three diagrams.
2. **Match type to information.** Flowchart for process logic, Sequence for temporal/API flows, ER for relationships, State for lifecycle, Architecture for topology. Full type catalog: [mermaid.js.org/syntax](https://mermaid.js.org/syntax/).
3. **Design for the most constrained target.** GitHub and Obsidian render differently; optimize for both.
4. **Agents over-complicate.** Always set explicit node limits and diagram type in prompts.

## aDNA Diagram Type Recommendations

| Document Type | Primary | Secondary |
|--------------|---------|-----------|
| Ontology / entity relationships | ER | Class |
| Campaign/mission execution flow | Flowchart | State |
| Agent cold-start chain | Sequence | Flowchart |
| Pipeline stage progression | State | Flowchart |
| System architecture | Architecture | Flowchart + subgraphs |

## Complexity Limits

**Rule of thumb:** Under 20 nodes and 25 edges for reliable cross-platform rendering.

| Target | Max Nodes | Gotchas |
|--------|----------|---------|
| GitHub | ~30 | No zoom/pan; diagram must read at default size. Cached renders may lag in PRs. Light/dark theme — avoid color dependence. |
| Obsidian | ~20-25 | Crops in reading view. CSS fix: `.mermaid svg { max-width: 100%; }`. Bundled Mermaid version may lag upstream. |

## Agent Prompt Template

```
Create a Mermaid [type] diagram showing [specific concept].
Keep it under 15 nodes. Use descriptive 2-3 word labels.
Direction: [TB/LR]. Include a brief text description above the diagram.
```

- Specify diagram type explicitly — agents default to flowcharts
- Set node count limits — agents include every entity otherwise
- Request domain terminology labels, not generic names

## Anti-Patterns

- **Kitchen-sink diagram** — 50+ nodes; unreadable everywhere. Split by concern.
- **Flowcharts for everything** — use sequence/state/ER when they fit better.
- **Missing context** — no surrounding text explaining the diagram's purpose.
- **Over-styled** — custom themes break across render targets. Keep styling minimal.
- **Unconstrained agent generation** — technically correct but too complex to be useful.

## Sources

- [Mermaid.js Syntax Reference](https://mermaid.js.org/syntax/) — canonical syntax docs for all diagram types
- [Obsidian Mermaid Rendering Limits](https://forum.obsidian.md/t/mermaid-js-diagram-unreadable-due-to-large-size/23769) — size constraints, CSS workarounds
- [Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic (2025)
