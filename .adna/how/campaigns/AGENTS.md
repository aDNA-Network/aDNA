---
type: directory_index
created: 2026-02-17
updated: 2026-04-03
last_edited_by: agent_init
tags: [directory_index, campaign]
---

# Campaigns

Multi-mission initiatives that coordinate large-scale work toward strategic goals.

## Purpose

Campaigns sit above missions in the work hierarchy. Where a mission decomposes a single large task into session-sized objectives, a campaign coordinates multiple missions toward a strategic goal. Campaigns provide:

- **Strategic framing** — a named initiative with clear goals, phases, and exit criteria
- **Mission sequencing** — dependency ordering across missions with phase gates
- **Planning integration** — R&D→PRD→RFC pipeline artifacts as campaign inputs
- **Progress tracking** — phase-level checkpoints and risk registers
- **Closeout rigor** — cross-system validation and follow-up campaign scoping

## Hierarchy

```
Campaign (strategic initiative, 10-40 sessions)
├── Phase (logical grouping of missions)
│   ├── Mission (multi-session task, 1-5 sessions each)
│   │   ├── Objective (session-sized unit of work)
│   │   └── Objective
│   └── Mission
│       └── Objective
└── Phase
    └── Mission
        └── Objective
```

## Directory Structure

```
how/campaigns/
├── AGENTS.md                           # This file (protocol)
└── campaign_<name>/                    # One directory per campaign
    ├── campaign_<name>.md              # Master campaign document
    ├── missions/                       # Campaign missions (containment model)
    │   ├── mission_<name>.md
    │   └── mission_<name>.md
    └── ...                             # Supporting documents
```

Campaign missions live **inside their campaign directory** at `how/campaigns/campaign_<name>/missions/`. This containment model keeps campaign-scoped missions co-located with their campaign.

Standalone missions (not part of any campaign) live in `how/missions/`.

## Campaign Master Document Format

**Directory**: `how/campaigns/campaign_<name>/`
**Filename**: `campaign_<name>.md`

See `how/templates/template_campaign.md` for the full template.

Optional: A **strategic compass** (`who/governance/` or project root) can define 3-7 immutable principles that all campaigns must align to. Template: `template_strategic_compass.md`. When a compass exists, verify campaign alignment before activation.

Key frontmatter fields:

```yaml
---
campaign_id: campaign_<name>
type: campaign
title: "Human-readable campaign title"
owner: <username>
status: planning | active | completed | abandoned
phase_count: <N>
mission_count: <N>
estimated_sessions: "<range>"
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_edited_by: agent_<username>
strategic_compass: <optional — link to strategic compass document>
---
```

## Lifecycle

### 1. Planning

1. Identify a strategic initiative that requires multiple coordinated missions
2. Create R&D→PRD→RFC planning artifacts through `how/pipelines/prd_rfc/` (optional but recommended)
3. Create campaign directory at `how/campaigns/campaign_<name>/`
4. Write campaign master document using `template_campaign.md`
5. Set `status: planning`

### 2. Activation

1. Get user approval on campaign scope, phases, and mission sequence
2. Create mission files in `how/campaigns/campaign_<name>/missions/` with `campaign_id` field
3. Set campaign `status: active`
4. Begin Mission 0 (infrastructure/setup) if defined

### 3. Execution

1. Execute missions in dependency order
2. **Phase gates**: verify exit criteria before advancing to next phase. Gates should have verifiable criteria — quantified where possible, not subjective assessments. Present completion evidence to the user before advancing.
3. Update campaign master document with progress after each mission
4. Checkpoint reviews at phase boundaries
5. Risk register updates as issues surface

### 4. Mission AAR (After-Action Review)

On mission completion, execute this 5-step protocol:

1. **Verify deliverables** — check outputs against acceptance criteria. Count validated/total.
2. **Update tracking** — set mission `status: completed`, update campaign phase counter.
3. **Gap analysis** — log issues and debt to `how/missions/artifacts/{campaign}_{mission}_aar.md` using `template_aar.md`. Include scorecard table.
4. **Readiness assessment** — GO / NO-GO for next mission with rationale. If NO-GO: create remediation mission, insert into campaign sequence, flag with `#needs-human`.
5. **Report AAR summary** — render scorecard, gaps, debt, and recommendation to user.

### 5. Completion

1. Final validation mission (cross-system coherence)
2. Fill **Completion Summary** in campaign master document (Deliverables, Descoped, Key Findings, Scope Changes, Follow-Up)
3. Append a **Campaign AAR** — same 5-line format as mission AARs (`how/templates/template_aar_lightweight.md`). Summarize at campaign level: what worked across all missions, what didn't, key finding, process change, follow-up.
4. **Context graduation** (AFTER summary + AAR, BEFORE status:completed) — run `skill_context_graduation` to promote reusable campaign knowledge to context library
5. Set `status: completed`
6. Scope follow-up campaigns if applicable
7. Update `how/STATE.md`

### Git-Aware State Verification

Before updating campaign status fields (`status`, `phase`):
1. Run `git pull` to ensure you have the latest state
2. If the file was modified since your last read, re-read it before writing
3. After updating status, commit promptly — status changes are coordination signals

### 6. Reopen

Before resuming a **dormant** campaign (one paused long enough that its recorded state may have drifted), run a
**re-orientation pass** — never a blind resume. A dormant campaign's `status`/`phase` frontmatter drifts; in a
busy fleet its scope is often delivered piecemeal by sibling tracks, and its terminal target may already have
shipped under another banner.

1. **Diff the terminal target against the release CHANGELOG.** If the campaign's `tag_target_at_close` /
   terminal milestone already appears in the release log, the campaign may be *terminal* — run closeout (§5),
   not resumption.
2. **Diff each open phase/mission against sibling closures.** Mark each unit delivered-elsewhere / superseded /
   still-open.
3. **Re-validate the plan's external dependencies.** Contracts naming other vaults/personas may reference
   archived or renamed entities — re-resolve each against current routing.
4. **Trust the mission files + closures + CHANGELOG over the campaign frontmatter** (truth hierarchy: git HEAD >
   closures > frontmatter fields).
5. **Produce a decision-ready reconciliation ledger + an operator gate** before executing any remaining work.

The pass either resumes execution against a corrected plan or — commonly — reveals the campaign is already at
its finish line, turning a nominal multi-session resume into an honest closeout. *(Graduated from a real reopen
where a stale "P0 open" frontmatter masked a campaign whose terminal target had already shipped under a
sibling's banner; the reconciliation collapsed a nominal 60–80-session resume into a ~2-session closeout.)*

### 7. Abandonment

1. Set `status: abandoned` with rationale
2. Note which missions completed, which were dropped
3. File backlog ideas for any salvageable work

## Relationship to Other Systems

| System | Relationship |
|--------|-------------|
| **Missions** (`how/missions/`) | Standalone missions live in `how/missions/`. Campaign missions live in `how/campaigns/campaign_<name>/missions/`. |
| **Sessions** (`how/sessions/`) | Sessions execute mission objectives. Sessions reference both mission and campaign. |
| **Pipelines** (`how/pipelines/`) | R&D→PRD→RFC pipeline produces planning artifacts that feed campaign design. |
| **Context Library** (`what/context/`) | Campaigns may create or consume context topics. |
| **Backlog** (`how/backlog/`) | Campaigns graduate from backlog ideas. Completed campaigns may generate new backlog ideas. |
| **STATE.md** (`how/STATE.md`) | Active campaigns tracked in operational state. |

## Verification Rubric

Three verification levels ensure campaign quality:

**Per-mission**: SITREP filed, AAR produced with scorecard, deliverables validated, files committed.

**Per-phase**: All mission AARs are GO, phase exit criteria met (user approval required), scope changes documented.

**Campaign-level**: Cross-file coherence (AGENTS.md references), token budget measured, template/skill indexes complete, context graduation run, STATE.md updated.

See `template_campaign.md` verification section for the full checklist tables.

## Campaign CLAUDE.md

For campaigns that will be executed by multiple agents or span many sessions, create a per-campaign `CLAUDE.md` in the campaign directory. Template: `template_campaign_claude.md`. This enables delegation by providing: campaign identity, quick start, key files, standing orders, and context loading instructions.

## Rules

- **One campaign master document per initiative** — the master document is the single source of truth
- **Campaign missions live inside the campaign** — at `how/campaigns/campaign_<name>/missions/`
- **Standalone missions live in `how/missions/`** — only for missions not part of a campaign
- **Phase gates are human gates** — never auto-advance between campaign phases without user review
- **Campaign scope is mutable** — add, reorder, or remove missions as needed, but document scope changes
- **Subsumption** — when a campaign absorbs an existing mission, set the original mission's status to `subsumed`
- **Archive, don't delete** — campaign documents are permanent records even after completion
- **Recon beats the charter** — a campaign/plan charter carries counts, named items, and assumed governance that read as facts but are **planning estimates**. Before each destructive/structural op, the executor: (1) re-derives ground truth over the live-ref + consumer surface (estimates run ~3× low); (2) re-verifies each target/absorber's own ratified governance (CLAUDE.md + ADRs + active campaigns) — the charter may predate or contradict it; (3) surfaces material deltas at the entry gate (> ~20% count divergence · governance conflict · surprise live work) **before** proceeding; (4) records the delta so the next op inherits truth, not the stale estimate. The charter is a hypothesis; recon is the test.

## Load/Skip Decision

**Load this directory when**:
- Creating or planning a new multi-mission campaign initiative
- Checking active campaign status (startup checklist step 7)
- Reviewing phase gates before advancing a campaign to the next phase
- Closing a campaign — writing completion summary, scoping follow-up work

**Skip when**:
- Working within a specific campaign mission (load the mission file directly)
- Performing routine session work not tied to campaign planning or review
- Already know the campaign directory path and are drilling into a specific campaign

**Token cost**: ~1,100 tokens (this AGENTS.md)
