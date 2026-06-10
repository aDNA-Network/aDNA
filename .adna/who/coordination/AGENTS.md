---
type: directory_index
created: 2026-02-17
updated: 2026-02-19
last_edited_by: agent_init
tags: [directory_index, coordination]
---

# Coordination Notes — Agent Protocol

## Purpose

Short-lived coordination messages between concurrent agents operating on this project. When an agent discovers something urgent that other agents should know before their next session, drop a coordination note here.

## Format

Files should be named: `note_YYYYMMDD_{topic}.md`

```yaml
---
created: YYYY-MM-DD
author: agent_{username}
urgency: info | warning | blocking
expires: YYYY-MM-DD
---

# {Topic}

Brief description of what other agents need to know.
```

## Urgency Levels

| Level | Meaning | Agent Action |
|-------|---------|--------------|
| `info` | Advisory only | Note and proceed normally |
| `warning` | Proceed with caution | Check the flagged area before modifying |
| `blocking` | Stop and consult user | Do not proceed with affected work |

## Lifecycle

1. **Create** when you discover something cross-cutting (e.g., "shared config is mid-edit", "sync issue detected")
2. **Read** on session start (part of the Agent Startup Checklist in CLAUDE.md)
3. **Delete** when the note is expired or no longer relevant
4. **No archive** — coordination notes are ephemeral, no history needed

## Rules

- Keep notes short (1-2 paragraphs)
- Set `expires` date — notes without expiry clutter the directory
- `blocking` urgency means agents should pause and consult the user
- `warning` means proceed with caution
- `info` is advisory only

## Load/Skip Decision

**Load this directory when**:
- Session startup — checking for urgent cross-agent notes (startup checklist step 5)
- Posting a coordination note after discovering something cross-cutting (sync issue, config conflict, shared work overlap)
- Cleaning up expired coordination notes

**Skip when**:
- Already checked coordination during startup and found no urgent notes
- Working in a single-agent environment with no concurrent sessions
- Mid-session and not posting a new coordination note

**Token cost**: ~400 tokens (this AGENTS.md)
