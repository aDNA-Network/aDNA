---
type: coordination
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
author: agent_<username>
from_persona:            # optional (ADR-061) — the persona that wrote it
from_vault: <Name>.aDNA  # REQUIRED (ADR-061) — the vault it was sent from: the one value a recipient can resolve on disk
authority:               # optional (ADR-061) — the ruling or grant the send was made under
to: <Name>.aDNA          # the recipient vault (persona optional, e.g. "<persona> (<Name>.aDNA)") — what a peer's queue probe matches
reply_to: who/coordination/inbox/   # where a reply should land in the sender's vault
status: staged           # staged = written, NOT sent · delivered = copied into the recipient's inbox (stamp AFTER the copy, then re-sync the delivered copy)
delivered_on:            # set with status: delivered
urgency: info | warning | blocking
expires: YYYY-MM-DD
last_edited_by: agent_<username>
tags: [coordination]
---

# Topic

Brief description of what other agents need to know.
