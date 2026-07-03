---
type: ratification_record
title: "Ratification Ceremony — {gate, e.g. P4 → P5}"
status: active
gate: "{P4 → P5}"
ratifier: "{Named human operator/authority — e.g. Stanley, Founding Architect}"
ratified_date: <% tp.date.now("YYYY-MM-DD") %>
ratifying_session: session_{username}_...
ratifying_commit: "{SHA}"
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
last_edited_by: agent_<username>
tags: [ratification_record, decision, ceremony]
---

# Ratification Ceremony — {gate}

> The instrument of the standard's **§7.7 Decision-Record Ratification Discipline**. Use this record for an
> **N-ADRs-at-once ceremony** (a phase gate that ratifies several decisions in one motion); a single ADR's
> ratification lives in that ADR's own `## Ratification` block (`template_adr.md`). One schema, two entry
> points — the ceremony record below is the N-at-once variant of the per-ADR block.
>
> **Agents author; operators ratify** (§7.7 rule 1). An agent MAY fully draft this record with every ADR
> pre-filled at `status: proposed`; only the *named operator* may advance status to `accepted`/`ratified`
> at the gate. The four ratification fields (ratifier · gate/reference · date · scope) are structure the
> agent fills; their *truth* is the operator's, attested at the gate.

## 1. Ceremony header

| Field | Value |
|-------|-------|
| **Gate** | {e.g. P4 → P5} |
| **Ratifier** (named operator/authority) | {e.g. Stanley, Founding Architect} — an agent/persona may appear only as **author/steward**, never as ratifier |
| **Gate / reference** | {verifiable pointer to the discrete event: AskUserQuestion lane and/or approved-plan file id · ratifying `session_id` · ratifying commit SHA} |
| **Ratification date** | {YYYY-MM-DD — distinct from authored/created dates} |
| **Scope of authority** | {exactly what this ceremony authorizes: these ADRs only, or a named downstream program} |

## 2. ADR roster (dependency order)

Every decision this ceremony ratifies, listed in dependency order. Each row's status advances
`proposed → accepted` only here, at the gate.

| # | ADR | Prior status | Ratified status | Signed by | Notes / pending co-signs |
|---|-----|--------------|-----------------|-----------|--------------------------|
| 1 | adr_NNN_short_title | proposed | accepted | {operator} | {none · or: seams stay doctrine until co-sign from `<persona>` lands} |
| 2 | adr_NNN_short_title | proposed | accepted | {operator} | |

> **Pending co-signs keep seams non-operative** (the ADR-043 precedent): the decision binds at ratification,
> but any seam it opens stays *doctrine* until the named co-signs land. Record every such pending co-sign in
> the Notes column so the seam's operative status is auditable.

## 3. No-contradiction invariants discovered

Cross-phase invariants that surfaced *at* ratification (the "late constitutional invariants" class — a
decision that only became visible once several ADRs were read together). List each, with the ADRs it spans.

- {invariant} — spans ADR-NNN + ADR-NNN.

## 4. Constitutional carry-forward

Explicit language for how the ratified set propagates into subsequent phases / campaigns — what downstream
work now MUST assume, and what remains open.

- {carry-forward clause}

## 5. Persona ratification status

Confirms the campaign's persona survived all falsification tests through ratification (or records the
correction if it did not).

- {persona} — {survives / adjusted at gate: …}

## Self-reference (Standing Order #8)

This record is itself the discipline it enforces: the standard teaches that decisions are operator-ratified
governance events (§7.7), and the ceremony that ratifies a batch of them is recorded in exactly this
operator-attested instrument. An agent authored the draft; the operator's signature at the gate is what
makes it binding.
