---
type: reference
title: "Context Quality Evaluation Rubric"
created: 2026-02-19
updated: 2026-02-19
context_version: "1.0"
last_edited_by: agent_init
tags: [reference, quality, context-engineering, rubric]
banner: "who/assets/banners/banner_mission.jpg"
icon: clipboard-list
---

# Context Quality Evaluation Rubric

## Purpose

Systematic quality evaluation framework for context library objects. Provides a 6-axis quantitative rubric that gates all context files — any file scoring ≤ 2 on any axis is flagged for revision regardless of composite score. Applied during Phase 3 review (mandatory for `standard`+ effort) and during periodic quality audits.

## Evaluation Axes

### 1. Signal Density (1-5)

**Definition**: Fraction of tokens that are decision-relevant — i.e., removing the token would reduce an agent's ability to make a correct recommendation or produce useful output.

| Score | Descriptor | Example |
|-------|-----------|---------|
| 1 | **Mostly filler.** >50% of content is hedging, preamble, repetition, or background that doesn't inform decisions. | "When it comes to GPU cluster architecture, there are several important considerations to keep in mind..." |
| 2 | Significant filler. 30-50% of tokens add no decision value. Prose-heavy with buried insights. | Background paragraphs explaining well-known concepts before getting to novel analysis. |
| 3 | **Moderate density.** Some filler but most paragraphs carry useful information. Tables mixed with narrative. | A guide that alternates between useful recommendations and verbose explanations of obvious points. |
| 4 | High density. <15% filler. Tables, structured lists, and concise paragraphs dominate. Minimal hedging. | Context file using table-first format with brief connecting prose. Each sentence carries weight. |
| 5 | **Every sentence carries weight.** Token removal would degrade output quality. Decision tables, structured data, precise claims. Zero filler. | The GPU cluster table in signal_to_token.md: 3 rows × 4 columns encoding 12 data points in ~40 tokens. |

**Worked example (score 2 vs 4)**:
- *Score 2*: A context file on federation patterns that opens with 200 tokens explaining "what federation means in general distributed systems" before reaching aDNA-specific content.
- *Score 4*: The same topic opening with a decision table: "Federation capability | Schema requirement | Example" — every token maps to a design decision.

### 2. Actionability (1-5)

**Definition**: Can an agent use this context to produce concrete, specific output — or is it background knowledge only?

| Score | Descriptor | Example |
|-------|-----------|---------|
| 1 | **Awareness only.** Describes a domain but provides no guidance an agent can act on. | "Machine learning is a broad field with many applications..." |
| 2 | General awareness with some direction. Identifies categories but no specific actions. | "You should consider performance, cost, and reliability when choosing infrastructure." |
| 3 | **Moderate actionability.** Contains recommendations but requires agent interpretation. Some concrete guidance mixed with general advice. | "Use XML tags for structural boundaries" — actionable but still needs context about when/how. |
| 4 | High actionability. Specific recommendations with rationale. Format selection guides, decision trees, threshold values. | "Default to standard effort for most queries. Minimal for simple lookups; exhaustive for critical decisions." — directly maps to a parameter choice. |
| 5 | **Directly executable.** Decision tables, format selection guides, threshold matrices that an agent can apply without interpretation. | The Format Selection Guide table in signal_to_token.md: 7 content types → 7 format choices → 7 rationales. Agent can look up its content type and get the answer. |

**Worked example (score 2 vs 4)**:
- *Score 2*: "Ontology design should balance simplicity with expressiveness" — true but an agent can't derive a specific action.
- *Score 4*: "Use flat schemas with discriminator fields (e.g., `type: customer|partner|contact`) instead of deep hierarchies. Apply the question test: if asking 'is X a Y?' feels unnatural, the classification is wrong." — specific design rules an agent can execute.

### 3. Coverage Uniformity (1-5)

**Definition**: Balanced depth across sections — are all declared topics covered proportionally, or does one section dominate while others are thin?

| Score | Descriptor | Example |
|-------|-----------|---------|
| 1 | **One section dominates.** >60% of tokens in one section; other sections are stubs or missing. | A "security best practices" file where 80% covers authentication and authorization gets 2 sentences. |
| 2 | Significant imbalance. One section has 2-3× the depth of others without proportional importance. | |
| 3 | **Moderate balance.** Minor imbalances but all declared sections have substantive content. Some sections could use expansion. | Most sections have 3-5 points; one has 8 and another has 2. The imbalance is noticeable but not severe. |
| 4 | Good balance. Sections are proportional to their importance. No stubs. Minor depth differences justified by topic weight. | |
| 5 | **Even depth, proportional to importance.** Every section has depth matching its significance. No section feels rushed or padded. | signal_to_token.md: Key Principles (7 items), Recommendations (3 sub-sections), Examples (2 comparisons), Anti-Patterns (6 items), Sources (5). Balanced across all standard sections. |

### 4. Source Diversity (1-5)

**Definition**: Distribution of evidence across source types. Over-reliance on a single source type is a quality risk — vendor docs may be biased, academic papers may lag practice, community sources may lack rigor.

| Source Types | Examples |
|-------------|---------|
| Vendor/official docs | Anthropic docs, AWS whitepapers, framework docs |
| Academic/research | Papers, preprints, textbooks |
| Industry practitioner | Blog posts by practitioners, conference talks, case studies |
| Community/empirical | GitHub discussions, Stack Overflow, community benchmarks |
| Original analysis | First-hand operational experience, internal measurements |

| Score | Descriptor | Example |
|-------|-----------|---------|
| 1 | **Single source.** Entire file derives from one source or one source type. | A context file paraphrasing a single Anthropic blog post. |
| 2 | Limited diversity. 2 source types, but one provides >70% of claims. | Vendor docs + one academic paper, but the vendor docs drive everything. |
| 3 | **Moderate diversity.** 2-3 source types with reasonable balance. No single type >60%. | 3 vendor docs + 2 academic papers. Coverage adequate but narrow source types. |
| 4 | Good diversity. 3-4 source types, none providing >40% of claims. Multiple perspectives represented. | signal_to_token.md: Anthropic official (2), Anthropic blog (1), academic preprint (1), operational experience (1). 4 source types, balanced. |
| 5 | **Excellent diversity.** 4+ source types, none >40%. Cross-validated claims from independent sources. Vendor, academic, practitioner, and empirical perspectives all present. | |

### 5. Freshness Half-Life (Categorical)

**Definition**: How quickly do the majority of claims in this file become stale? This is a categorical assessment, not a numeric score — it describes the content's temporal character rather than its current quality.

| Category | Timeframe | Typical Content | Review Cadence |
|----------|-----------|----------------|---------------|
| **Volatile** | <1 year | Market share, pricing, benchmark rankings, API parameters, model capabilities | Quarterly review |
| **Stable** | 1-3 years | Architecture patterns, protocol designs, framework best practices, organizational processes | Annual review |
| **Durable** | 3+ years | Fundamental principles, mathematical frameworks, regulatory structures, design axioms | Review on major paradigm shifts |
| **Mixed** | Varies | File contains claims across multiple freshness categories | Tag individual sections; review at volatile cadence |

**Assessment guidance**: Read the file's claims and ask "which of these will be wrong in 12 months?" If >30% of claims are volatile, the file is volatile or mixed. If most claims are design principles or mathematical frameworks, the file is durable.

### 6. Cross-Topic Coherence (1-5)

**Definition**: Does this file contradict, redundantly overlap with, or complement related files in the same topic or adjacent topics?

| Score | Descriptor | Example |
|-------|-----------|---------|
| 1 | **Conflicts with related files.** Contains claims that directly contradict other context files. Definitions or recommendations are inconsistent. | One file recommends XML for all structure; another recommends markdown for everything, with no reconciliation. |
| 2 | Notable inconsistencies or substantial redundancy. >20% overlap with a sibling file without clear differentiation. | Two files in the same topic both cover "format selection" with conflicting guidance. |
| 3 | **Minor overlap or slight inconsistencies.** Some repeated content across files but no outright contradictions. Differentiation is mostly clear. | Two files both mention "tables beat prose" but from different angles; slight redundancy, no conflict. |
| 4 | Good coherence. Files complement each other with minimal overlap. Cross-references are accurate. Each file has a distinct scope. | signal_to_token.md and convergence_model.md: distinct scopes (formatting vs. ontology structure) with complementary principles and accurate cross-references. |
| 5 | **Perfect complementarity.** Files partition the topic cleanly. No redundancy. Cross-references are bidirectional and accurate. Reading related files together produces strictly additive knowledge. | |

**Assessment method**: For each file being scored, identify the 2-3 most related files (same topic or adjacent). Check for: (a) contradictory claims, (b) redundant coverage >10%, (c) missing cross-references where they'd help, (d) terminology consistency.

---

## Composite Score

**Formula**: Simple average of the 5 numeric axes (signal density, actionability, coverage uniformity, source diversity, cross-topic coherence).

```
quality_score = (signal_density + actionability + coverage_uniformity + source_diversity + cross_topic_coherence) / 5
```

Freshness half-life is categorical and not included in the numeric average — it is recorded separately as `freshness_category`.

### Floor Rule

**If any numeric axis scores ≤ 2, the file is flagged for revision regardless of composite score.** A file scoring 5/5/5/1/5 (composite 4.2) still fails — source diversity of 1 means single-source risk that could invalidate the entire file.

### Score Interpretation

| Composite | Rating | Action |
|-----------|--------|--------|
| 4.5 - 5.0 | Excellent | File as-is. Exemplary reference. |
| 3.5 - 4.4 | Good | File with minor improvements noted. |
| 2.5 - 3.4 | Adequate | File with improvement plan. Prioritize lowest-scoring axes. |
| 1.5 - 2.4 | Needs work | Revise before filing. Multiple axes need improvement. |
| 1.0 - 1.4 | Unacceptable | Re-research or re-synthesize from scratch. |

---

## Scoring Procedure

### During Phase 3 Review (mandatory for `standard`+ effort)

1. **Read the context file** in full
2. **Identify 2-3 related files** for cross-topic coherence assessment
3. **Score each axis** using the descriptors above — record the score and a 1-sentence justification
4. **Compute composite** — apply floor rule check
5. **Record in frontmatter** — add quality fields (see scoring template)
6. **Include in review brief** — the Quality Scorecard section

### During Periodic Audit

Same procedure, but also:
- Check freshness against current date — volatile files >6 months old need re-evaluation
- Compare scores against topic averages — outlier low scores indicate revision candidates

---

## Frontmatter Integration

Quality scores are recorded in context file frontmatter:

```yaml
# Quality evaluation (added by M2 rubric)
quality_score: 4.2          # composite average of 5 numeric axes
signal_density: 4            # 1-5
actionability: 5             # 1-5
coverage_uniformity: 4       # 1-5
source_diversity: 4          # 1-5
cross_topic_coherence: 4     # 1-5
freshness_category: stable   # volatile | stable | durable | mixed
last_evaluated: 2026-02-19   # date of last quality evaluation
```

These fields are optional in the context file schema — they are added during Phase 3 review or retrospective quality audits.

---

## Calibration Appendix

Baseline calibration against 3 existing context files, establishing scoring reference points.

### Calibration File 1: `context_prompt_engineering_signal_to_token.md` (adna)

**Profile**: M1 research output. High-quality, decision-relevant tables, multiple source types.

| Axis | Score | Justification |
|------|-------|--------------|
| Signal density | 5 | Every section delivers decision-relevant content. Format Selection Guide table is maximally dense. The high/low density comparison example demonstrates the principle it teaches. Zero filler. |
| Actionability | 5 | Format Selection Guide (7 content types → format → rationale), Token Efficiency Tactics (5 specific actions), Context Window Management (budget percentages). Agent can execute directly from these tables. |
| Coverage uniformity | 4 | 7 Key Principles, 3 Recommendation subsections, 2 Examples, 6 Anti-Patterns, 5 Sources — well-balanced. Minor: Examples section is slightly thinner than others (2 comparisons vs. 5-7 items elsewhere). |
| Source diversity | 4 | 5 sources across 3 types: Anthropic official docs (3), Anthropic blog (1), academic preprint (1). Strong vendor representation; one academic paper provides independent validation. Would benefit from a practitioner/community source for a 5. |
| Cross-topic coherence | 5 | Distinct scope (formatting optimization) that complements convergence_model (structural optimization) without overlap. Referenced by convergence_model as foundation. Terminology consistent across topic. |
| Freshness | stable | Core principles (XML tags, tables-over-prose, progressive disclosure) are stable design patterns. Claude-specific formatting guidance is model-generation-specific but stable within the Claude 4 era. Minor volatile elements (specific token counts, model behavior details). |

**Composite**: (5 + 5 + 4 + 4 + 5) / 5 = **4.6** — Excellent

### Calibration File 2: `context_prompt_engineering_convergence_model.md` (adna)

**Profile**: M1 original articulation. Novel framework with operational backing but fewer external sources.

| Axis | Score | Justification |
|------|-------|--------------|
| Signal density | 4 | The Analogy Table and Worked Example are maximally dense. Design Implications section is highly actionable. The mathematical framing paragraphs in Key Principles are slightly denser on abstraction than necessary — a few sentences could be tightened without losing meaning. |
| Actionability | 4 | "Designing for Convergence" table (6 decisions × convergent/divergent), "Design Implications" (5 numbered rules), "When to Use It" (4 bullet applications). Strong, but the mathematical framing sections require interpretation before application — not as directly executable as signal_to_token's tables. |
| Coverage uniformity | 5 | 6 Key Principles, Analogy Table, Worked Example (detailed token narrowing), Designing for Convergence table, Projection Sequence (4 steps), Design Implications (5 items), Anti-Patterns (6 items), When to Use It (4 bullets), 3 Sources. Comprehensive and balanced — every section has substance. |
| Source diversity | 2 | 3 sources, but dominated by original articulation (primary) + 1 Anthropic source + 1 internal spec. No academic, practitioner, or community validation. The framework is largely first-principles; external validation would strengthen it but the novelty limits available sources. |
| Cross-topic coherence | 5 | Explicitly builds on signal_to_token (formatting) and ontology_design (structure). Distinct scope — the structural/mathematical lens rather than formatting or entity design. Dependency chain documented in topic AGENTS.md. |
| Freshness | durable | Mathematical framework, design principles, structural decomposition patterns. These are paradigm-level abstractions unlikely to change within 3+ years. The worked token-count example may need updating as vault grows, but the principles hold. |

**Composite**: (4 + 4 + 5 + 2 + 5) / 5 = **4.0** — Good

**Floor rule triggered**: Source diversity = 2. Despite a strong composite, this file should be flagged for source diversity improvement. Recommendation: in a future pass, cross-reference against published knowledge graph / ontology decomposition literature to add academic validation.

### Calibration File 3: `context_deep_research_methodology.md` (vault)

**Profile**: Older file, different production method (not M1 research). Describes the deep research process itself.

| Axis | Score | Justification |
|------|-------|--------------|
| Signal density | 3 | Key Principles (6 items) are well-structured. Recommendations (4 items) are concise and actionable. However, "Detailed Analysis" section contains explanatory prose that mostly restates the principles in longer form ("Why Orchestrator-Worker?" largely repeats Principle 1). ~20-25% redundancy between sections. |
| Actionability | 3 | Recommendations are moderately actionable ("Default to standard effort", "Use sub-agents for source dispatch"). But the file describes a process rather than providing decision tables. An agent reading this knows *what* deep research is but would need the full skill directory to *execute* it. The Comparison Table (Context Engine vs Deep Research) is the most actionable element. |
| Coverage uniformity | 3 | Key Principles and Recommendations are solid. Detailed Analysis has 2 subsections + 1 comparison table — adequate but thin compared to the 6 principles. Sources section is minimal (3 sources, no URLs for 2 of them). Missing: effort level details, iteration budgets, output format specs. |
| Source diversity | 2 | 3 sources, all in-family: 2 Anthropic + 1 internal. No academic, practitioner, or community sources. The process is internally designed, which limits external source availability, but related work on multi-agent research patterns exists in academic literature. |
| Cross-topic coherence | 4 | Distinct scope (methodology overview) that complements the full deep_research skill directory without contradiction. Slight risk: claims about "bounded iteration" and "effort scaling" are general here but detailed in the skill files — an agent loading both gets some redundancy. No outright conflicts. |
| Freshness | stable | Process design patterns and orchestrator-worker topology are stable. Effort level design is process-specific and changes with the skill, not with external factors. Anthropic source references are 2025-era and still current. |

**Composite**: (3 + 3 + 3 + 2 + 4) / 5 = **3.0** — Adequate

**Floor rule triggered**: Source diversity = 2. File should be flagged for source diversity improvement and for signal density/coverage tightening. The Detailed Analysis section's redundancy with Key Principles is the main density drag.

### Calibration Summary

| File | Signal | Action | Coverage | Sources | Coherence | Freshness | Composite | Floor |
|------|--------|--------|----------|---------|-----------|-----------|-----------|-------|
| signal_to_token | 5 | 5 | 4 | 4 | 5 | stable | **4.6** | Pass |
| convergence_model | 4 | 4 | 5 | 2 | 5 | durable | **4.0** | **FAIL** (sources) |
| deep_research_methodology | 3 | 3 | 3 | 2 | 4 | stable | **3.0** | **FAIL** (sources) |

**Calibration observations**:
1. **Scores are differentiated** — the rubric produces meaningful spread (3.0 to 4.6), not clustering around 4. This is desirable.
2. **Source diversity is the systemic weak axis** — both lower-scoring files fail on sources. This reflects the reality that many context files are synthesized from limited source types. The rubric correctly identifies this as a quality risk.
3. **Signal density correlates with format** — files using tables as primary format (signal_to_token) score higher than prose-heavy files (deep_research_methodology). This aligns with the signal-to-token principles themselves.
4. **The floor rule works** — convergence_model has a strong composite (4.0) but the source diversity = 2 correctly flags a real weakness. Without the floor rule, this file would pass unchallenged.
5. **Freshness categorization is useful** — volatile/stable/durable provides actionable review scheduling information beyond the numeric scores.
