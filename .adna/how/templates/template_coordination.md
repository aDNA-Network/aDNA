---
type: coordination
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
author: agent_<username>
from_persona:            # optional (ADR-061) — the persona that wrote it
from_vault: <Name>.aDNA  # REQUIRED (ADR-061) — the vault it was sent from: the one value a recipient can resolve on disk
authority:               # optional (ADR-061) — the ruling or grant the send was made under
urgency: info | warning | blocking
expires: YYYY-MM-DD
last_edited_by: agent_<username>
tags: [coordination]
---

# Topic

Brief description of what other agents need to know.
