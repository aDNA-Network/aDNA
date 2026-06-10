---
type: quest_result
quest_id: quest_<short_name>
date: <% tp.date.now("YYYY-MM-DD") %>
operator: <your_name_or_handle>
environment:
  model: "<model name and version>"
  os: "<OS and version>"
  vault_size: "<number of files or approximate size>"
  adna_version: "<CLAUDE.md version field>"
status: submitted
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
last_edited_by: <your_name>
tags: [quest_result]
---

# Result: <quest_id> — <date>

## Raw Data

```yaml
# Structured measurements from the quest procedure
quest_id: quest_<short_name>
measurements:
  metric_a: <value>
  metric_b: <value>
  metric_c: <value>
success: true | false
notes: "any observations"
```

## Summary

One-paragraph summary of the result. Did the quest succeed? What was the key finding?

## Observations

- Anything unexpected during execution
- Friction points or confusion in the procedure
- Suggestions for improving the quest

## Environment Details

Additional environment context that might affect results:

- **Hardware**: CPU/GPU, RAM
- **Network**: relevant if quest involves remote operations
- **Vault contents**: number of templates, context topics, custom extensions
- **Agent configuration**: any non-default settings

---

> **Privacy notice**: This file must not contain PII, API keys, credentials, or any data that could identify individuals. Only performance metrics, structural observations, and environment specifications.
