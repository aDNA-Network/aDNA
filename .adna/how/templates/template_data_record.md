---
type: <% await tp.system.prompt("Type (customer|partner|contact|hardware|module|dataset|lattice):") %>
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
status: active
last_edited_by: agent_<username>
tags: []
---

# <% tp.file.title %>

## Overview

Brief description of this record.

## Details

Key attributes and relationships.

## Links

- Related records: [[]]
- Context: [[]]

## Notes

<% tp.file.cursor() %>
