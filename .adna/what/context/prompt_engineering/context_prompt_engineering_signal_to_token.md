---
type: context_research
topic: prompt_engineering
subtopic: signal_to_token
created: 2026-02-19
updated: 2026-03-18
sources: ["Anthropic — Effective Context Engineering for AI Agents", "Anthropic — Claude 4 Best Practices", "Anthropic — Use XML Tags to Structure Prompts", "Anthropic — Prompting Long Context", "Preprints.org — Prompt Engineering for Structured Data (2025)"]
context_version: "1.0"
token_estimate: ~1500
last_edited_by: agent_init
tags: [context, prompt_engineering]
quality_score: 4.6
signal_density: 5
actionability: 5
coverage_uniformity: 4
source_diversity: 4
cross_topic_coherence: 5
freshness_category: stable
last_evaluated: 2026-02-19
---

# Prompt Engineering: Signal-to-Token Optimization

## Key Principles

1. **Context is a finite attention budget.** The engineering problem is finding "the smallest set of high-signal tokens that maximize the likelihood of some desired outcome." Every token competes for model attention — treat context as a precious, finite resource.

2. **XML tags outperform markdown for structural boundaries.** Claude was specifically trained with XML tags in input and output. XML provides unambiguous start/end delimiters that reduce parsing errors. Markdown saves ~15% tokens but at the cost of structural clarity. Use XML for separation of concerns (`<instructions>`, `<context>`, `<examples>`), markdown for content within those sections.

3. **Tables beat prose for decision-relevant data.** Structured formats (tables, key-value pairs, bulleted lists) deliver higher signal density than narrative paragraphs for factual content. Decision framework tables were the highest-value output format in our deep research smoke test. Default to "table-first, prose-second" for data-heavy content.

4. **Just-in-time context beats pre-loading.** Instead of loading all data upfront, maintain lightweight identifiers (file paths, stored queries, links) and use tools to dynamically load data at runtime. Claude Code exemplifies this — agents use targeted queries and tool calls to explore without loading full objects.

5. **Progressive disclosure mirrors human cognition.** Let agents discover context incrementally through file hierarchies, naming conventions, and timestamps. Pre-load only static reference materials (CLAUDE.md, AGENTS.md); everything else should be on-demand.

6. **Information placement affects recall.** In long contexts (70K+ tokens), critical instructions should be placed at the end of the prompt. Answers positioned at the beginning or middle benefit from scratchpad techniques. Use in-context examples drawn from the document itself (5 examples > 2; generic examples provide no benefit).

7. **Compaction preserves signal across sessions.** When approaching context limits, summarize conversation contents while preserving architectural decisions and unresolved issues. Tool result clearing is the "safest, lightest-touch" compaction. Balance recall (capture everything) against precision (eliminate noise).

## Recommendations

### Format Selection Guide

| Content Type | Best Format | Rationale |
|-------------|------------|-----------|
| Structural boundaries | XML tags | Trained behavior; unambiguous delimiters |
| Headings within sections | Markdown `##` | Readable, lightweight, familiar |
| Factual data / comparisons | Tables | Highest signal density per token |
| Step-by-step procedures | Numbered lists | Clear ordering, easy to reference |
| Configuration / schemas | YAML or JSON blocks | Machine-parseable, self-documenting |
| Narrative explanation | Short paragraphs | When relationships between concepts matter |
| Enumerations | Bulleted lists | When order doesn't matter |

### Token Efficiency Tactics

- **Eliminate hedging language.** "It should be noted that..." adds zero signal. State facts directly.
- **Use abbreviations in tables.** Column headers and repeated terms can be shortened after first definition.
- **Cut redundancy across sections.** If a fact appears in Key Principles, don't restate it in Recommendations.
- **Prefer specific data over general claims.** "72% gross margin (3% ↑ from Q1)" is more useful and barely longer than "margins improved significantly."
- **Frontmatter as structured metadata.** YAML frontmatter is token-efficient for classification, routing, and filtering — agents can read it without loading the full file.

### Context Window Management

- **Pre-load** (~5-10% of budget): CLAUDE.md, AGENTS.md files, task-specific schema/templates
- **Just-in-time** (~60-80%): File contents, search results, tool outputs loaded as needed
- **Reserve** (~10-20%): Working space for agent reasoning and output generation
- **Compaction trigger**: Summarize when nearing limits; preserve decisions and unresolved items; discard redundant tool outputs

### Claude-Specific Formatting

- Use XML tags for section boundaries: `<instructions>`, `<context>`, `<examples>`, `<formatting>`
- Nest tags for hierarchy: `<outer><inner></inner></outer>`
- Refer to tags by name: "Using the data in `<contract>` tags..."
- Combine XML structure with markdown content inside tags
- Match prompt formatting style to desired output style — markdown-heavy prompts produce markdown-heavy responses

## Examples

### High-Density Context File (Good)

```markdown
## GPU Cluster Architecture

| Tier | Interconnect | Use Case | Bandwidth |
|------|-------------|----------|-----------|
| L1 (Edge) | PCIe 5.0 | Inference | 64 GB/s |
| L2 (Regional) | InfiniBand HDR | Training | 200 Gb/s |
| L3 (Cloud) | InfiniBand NDR | Large-scale | 400 Gb/s |

Key constraint: InfiniBand dominates HPC (71% TOP500) while Ethernet leads commodity AI training.
```

### Low-Density Equivalent (Bad)

```markdown
When it comes to GPU cluster architecture, there are several important considerations
to keep in mind. At the edge tier (L1), the typical interconnect technology used is
PCIe 5.0, which provides bandwidth of approximately 64 GB/s and is primarily used for
inference workloads. Moving up to the regional tier (L2), organizations typically
deploy InfiniBand HDR interconnects...
```

The table version is ~40% fewer tokens with the same information content.

## Anti-Patterns

- **Bloated tool descriptions.** If humans can't pick the right tool from descriptions, agents will struggle more. Keep tool descriptions self-contained, non-overlapping, and purpose-specific.
- **Exhaustive edge-case documentation.** Provide canonical examples, not comprehensive lists. Examples are "pictures worth a thousand words" — quality over quantity.
- **Anti-laziness prompts on Claude 4.6.** Instructions like "be thorough" or "think carefully" amplify already-proactive behavior and can cause runaway thinking loops. Remove these; use the `effort` parameter instead.
- **Aggressive pre-loading.** Loading entire corpora into context wastes budget. Use file paths and tool calls to explore on demand.
- **Vague altitude instructions.** Avoid both brittle if-else logic and vague guidance. Strike balance with specificity that guides behavior while remaining flexible for model heuristics.
- **Overly aggressive compaction.** Summarizing too aggressively causes subtle context loss. Preserve architectural decisions and unresolved issues explicitly.

## Sources

- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic (2025). Core framework: signal-to-noise optimization, just-in-time context, compaction, sub-agent architectures.
- [Prompting Best Practices — Claude 4](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) — Anthropic (2025). Model-specific guidance: XML tags, effort parameter, anti-laziness, formatting control.
- [Use XML Tags to Structure Prompts](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags) — Anthropic. Tag naming, nesting, parseability, worked examples.
- [Prompt Engineering for Long Context](https://www.anthropic.com/news/prompting-long-context) — Anthropic (2024). Information placement, scratchpad technique, in-context examples at scale.
- [Prompt Engineering for Structured Data: A Comparative Evaluation](https://www.preprints.org/manuscript/202506.1937) — Preprints.org (2025). Token efficiency: CSV/simple prefixes lowest cost; JSON/YAML highest accuracy; format-model interaction effects.
