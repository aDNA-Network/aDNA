---
type: ruling_record
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_edited_by: agent_{username}
tags: [ruling_record, gate]
gate_id: <gate id — e.g. dp3_intake_YYYYMMDD or v8_12_release_gate>
packet_ref: <path to the packet the operator ruled on>@<commit SHA of that packet at the sitting>
ruled_by: <operator name>
ruled_on: YYYY-MM-DD
ruled_via: chat | AskUserQuestion | ISS gate | signed document
provenance: "<how the ruling reached this file — e.g. 'operator accept-all at plan time, recorded by agent_{username}'>"
status: ruled | partial | deferred
---

# Ruling record — {gate_id}

> **Why this file exists.** A packet asks questions; an operator answers them; the answers have to land somewhere
> a later session can cite without re-reading a chat transcript. One ruling record per gate sitting, written at the
> sitting, pinned to the packet commit it answers. The ADR's own §7.7 block still carries the *decision*; this file
> carries the *sitting* — which items were put, which were taken, in what words, and which were left open.

## Items

| # | Item (as put to the operator) | Ruling (operator's words or a faithful paraphrase) | Applied at (path) | Status |
|---|---|---|---|---|
| 1 | | | | ruled / deferred / struck |
| 2 | | | | |

## Left open

- *(list anything the sitting did not rule, with who owns asking it next)*

## Placement convention (doc-only at v8.12)

- Gate sittings live under `how/gates/<gate_id>.md` in the vault that owns the gate; an ISS-rendered gate keeps its
  `.output.md` beside it. This template records the ruling; it does not render the gate.
- Pin `packet_ref` to the **commit**, not the path alone — a packet edited after the sitting is a different packet.
- `standing_grant` records (a ruling that pre-authorizes a class of later acts) and unattended-execution envelopes are
  **not** this template's job; they are scoped for their own decision records.
