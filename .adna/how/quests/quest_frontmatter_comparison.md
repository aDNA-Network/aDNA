---
quest_id: quest_frontmatter_comparison
type: side_quest
title: "Frontmatter Format Comparison — Flat vs Nested FAIR"
difficulty: medium
estimated_token_cost: ~2K
model_requirements: "any"
status: active
created: 2026-03-20
updated: 2026-03-20
last_edited_by: agent_init
tags: [side_quest, frontmatter, fair, token-efficiency]
---

# Quest: Frontmatter Format Comparison

## Objective

Compare two frontmatter formats for FAIR metadata — **flat** (all fields at root level) vs **nested** (grouped under a `fair:` block) — and measure which format consumes fewer tokens, produces more reliable agent output, and parses more cleanly.

## Prerequisites

- aDNA vault version: v5.0 or later
- Model: any (record which model you use)
- Vault state: fresh clone of the adna repo
- Estimated time: 15-20 minutes
- Estimated token cost: ~2K tokens

## Procedure

1. **Setup** — Clone a fresh copy of the adna repo. Locate an example lattice file in `what/lattices/examples/` that has a `fair:` block.

2. **Format A (nested)** — Copy the file. Keep the existing nested FAIR format:
   ```yaml
   fair:
     license: MIT
     creators: [Name]
     keywords: [tag1, tag2]
   ```
   Ask your agent: "Read this lattice file and summarize its FAIR metadata." Record the token count for the prompt + response.

3. **Format B (flat)** — Create a second copy. Flatten the FAIR fields to root level:
   ```yaml
   fair_license: MIT
   fair_creators: [Name]
   fair_keywords: [tag1, tag2]
   ```
   Ask your agent the same question with the flat-format file. Record the token count.

4. **Parse test** — For each format, ask the agent: "Extract the license, creators, and keywords from this file's frontmatter and return them as a JSON object." Record whether the extraction is correct for each format.

5. **Collect** — Fill in the measurements below.

## Expected Output

```yaml
# Paste this into your result file's Raw Data section
quest_id: quest_frontmatter_comparison
measurements:
  nested_prompt_tokens: <value>
  nested_response_tokens: <value>
  flat_prompt_tokens: <value>
  flat_response_tokens: <value>
  nested_parse_correct: true | false
  flat_parse_correct: true | false
  nested_total_tokens: <value>
  flat_total_tokens: <value>
  token_difference_pct: <value>  # (flat - nested) / nested * 100
success: true
notes: "any observations about agent behavior differences"
```

## Submission Instructions

1. Fork the [Agentic-DNA repo](https://github.com/LatticeProtocol/adna) (or use your existing fork)
2. Create a result file: `how/quests/results/result_frontmatter_comparison_<YYYYMMDD>_<your_name>.md`
3. Use the [quest result template](../../how/templates/template_quest_result.md) for the file format
4. Fill in all required sections — especially the Raw Data YAML block
5. Open a PR to the `main` branch with title: `result: quest_frontmatter_comparison — <your_name>`
6. **Privacy**: Do not include PII, API keys, or sensitive data. Only performance metrics and structural observations.
