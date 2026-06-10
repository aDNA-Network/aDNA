---
quest_id: quest_<short_name>
type: side_quest
title: "Human-readable quest title"
difficulty: easy | medium | hard
estimated_token_cost: ~<N>K
model_requirements: "any | opus | sonnet | specific model notes"
status: active
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
last_edited_by: agent_<username>
tags: [side_quest]
---

# Quest: <Title>

## Objective

What this quest measures or tests. One clear sentence stating the question this experiment answers.

## Prerequisites

- aDNA vault version: v5.x or later
- Model: any / specific model requirements
- Vault state: fresh clone / existing vault / specific setup
- Estimated time: <N> minutes
- Estimated token cost: ~<N>K tokens

## Procedure

Follow these steps exactly. Each step should be unambiguous — an agent should be able to execute them without interpretation.

1. **Setup** — Describe initial state
2. **Execute** — The experiment steps
3. **Collect** — What data to record
4. **Cleanup** — Any teardown needed (optional)

## Expected Output

Describe the structured data the participant should collect. Use this YAML template:

```yaml
# Paste this into your result file's Raw Data section
quest_id: quest_<short_name>
measurements:
  metric_a: <value>
  metric_b: <value>
  metric_c: <value>
success: true | false
notes: "any observations"
```

## Submission Instructions

1. Fork the [Agentic-DNA repo](https://github.com/LatticeProtocol/adna) (or use your existing fork)
2. Create a result file: `how/quests/results/result_<quest_id>_<YYYYMMDD>_<your_name>.md`
3. Use the [quest result template](../how/templates/template_quest_result.md) for the file format
4. Fill in all required sections — especially the Raw Data YAML block
5. Open a PR to the `main` branch with title: `result: <quest_id> — <your_name>`
6. **Privacy**: Do not include PII, API keys, or sensitive data. Only performance metrics and structural observations.
