---
type: skill
skill_type: agent
created: 2026-05-12
updated: 2026-05-12
status: active
category: onboarding
trigger: Workspace router Step 0.3 — operator accepts `LatticeHome.aDNA/` bootstrap; runs after `skill_project_fork.md` + `skill_inventory_refresh.md` to fill operator-specific fields the auto-detect engine cannot infer
last_edited_by: agent_stanley
related_skills: [skill_project_fork, skill_inventory_refresh, skill_node_health_check]
related_artifacts:
  - aDNA.aDNA/how/campaigns/campaign_adna_v2_infrastructure/missions/artifacts/m04b_obj2_skill_node_bootstrap_interview_spec.md  # source spec
  - aDNA.aDNA/how/campaigns/campaign_adna_v2_infrastructure/missions/artifacts/m04b_obj1_dynamic_ux_gap_analysis.md  # 7+2 gaps this skill closes
question_count: 19  # 5 topics × {2,5,4,3,5} questions
estimated_runtime: "4-7 minutes"  # operator-paced; defaults speed it up
operator_persona: Hestia
exit_codes: [0, 2, 3, 4]
tags: [skill, agent, onboarding, dynamic_bootstrap, interview, node_adna, hestia, hybrid_d1_b, v7_x]
---

# skill_node_bootstrap_interview

Hybrid interview that fills the **operator-specific** fields of a freshly-forked `LatticeHome.aDNA/` vault — purpose, user-info, stack overlay, hardware confirm, and lattice connections. The interview NEVER re-asks what the auto-detect engine (`skill_inventory_refresh.md`) already captured. 19 questions across 5 topics; 4-7 min runtime; Hestia voice register.

## Trigger

Invoked by the workspace router Step 0.3 flow after operator accepts `LatticeHome.aDNA/` bootstrap. This skill runs as **Step 3** of the bootstrap chain:

```
Step 1: skill_project_fork.md    → empty LatticeHome.aDNA/ from template
Step 2: skill_inventory_refresh   → auto-detect inventory_*.yaml
Step 3: skill_node_bootstrap_interview  ← THIS SKILL
Step 4: skill_node_health_check   → validate vault is healthy
```

If invoked outside this chain (e.g., re-run later by an operator who wants to revise answers), exits 2 unless preconditions §1 hold.

## Read

Before asking any question, load:

| File | Purpose |
|---|---|
| `LatticeHome.aDNA/MANIFEST.md` | Existing template values to confirm/override |
| `LatticeHome.aDNA/STATE.md` | Current operational state (preserve unrelated content) |
| `LatticeHome.aDNA/what/inventory/inventory_system.yaml` | Auto-detected machine class, GPU, languages, IDEs, frameworks (Step 2 output) |
| `LatticeHome.aDNA/what/inventory/inventory_vaults.yaml` | Existing `.aDNA/` vaults on the node (informs C1 default suggestions) |
| `LatticeHome.aDNA/who/identity/identity_node.yaml` | Current operator alias from `skill_project_fork` |
| `LatticeHome.aDNA/who/identity/identity_lattice_protocol.yaml` | LP placeholders (operator may fill C3) |
| `LatticeHome.aDNA/what/inventory/inventory_memberships.yaml` | Federation defaults (privacy-first; operator may override at C2) |
| `LatticeHome.aDNA/CLAUDE.md` | Hestia persona block — confirm voice register for prompts |
| `LatticeHome.aDNA/CHANGELOG.md` | Append v0.1 footnote at completion |

## Produce

19 operator answers written into 8 target surfaces:

| Output file | Fields | Source questions |
|---|---|---|
| `MANIFEST.md` | `purpose:` · FAIR `keywords:` (append) · FAIR `license:` (override iff C5 ≠ private) | P1, P2, C5 |
| `STATE.md` | Hestia greeting tone (subtle; affects future session greetings) | U5 |
| `who/identity/identity_node.yaml` | `operator_alias`, `role`, `git_author`, `contact`, `persona_preferences`, `machine_class`, `gpu`, `peripherals`, `default_new_vault_license` | U1-U5, H1-H3, C5 |
| `who/identity/identity_lattice_protocol.yaml` | `peer_id`, `signing_key_path`, `permission_set` (or placeholder) | C3 |
| `what/inventory/inventory_system.yaml` (overlay) | `primary_languages`, `primary_ide`, `primary_frameworks`, `services_connected` | S1-S4 |
| `what/inventory/inventory_memberships.yaml` | `subscribed_lattices`, federation overrides, `marketplace_interests` | C1, C2, C4 |
| `CLAUDE.md` | 1-sentence persona-context paragraph (after Identity & Personality, before Operating Style) | P1 excerpt |
| `CHANGELOG.md` | v0.1 footnote — interview-complete + non-default license note if applicable | (always; C5 footnote) |

**Not touched**: any partner vault · `~/aDNA/CLAUDE.md` (workspace router) · `~/aDNA/.adna/` (template) · `LatticeHome.aDNA/AGENTS.md` · `LatticeHome.aDNA/README.md` · `LatticeHome.aDNA/CHANGELOG.md` body · all node-protocol AGENTS.md stubs · all 4 node-skills · `inventory_vaults.{md,yaml}` · `inventory_memberships.md` narrative (only YAML mutates).

## Steps

1. **Verify preconditions**: `LatticeHome.aDNA/` exists (forked by `skill_project_fork.md`); `inventory_vaults.yaml` + `inventory_system.yaml` exist (auto-detected by `skill_inventory_refresh.md`). If any precondition fails → exit `2: precondition_unmet`.
2. **Greet operator in Hestia voice**: "Welcome to your new node vault. I'm Hestia — the hearth-keeper. Let me ask 19 quick questions to fill in the operator-specific fields. Most have sensible defaults; press Enter to accept. We'll be done in 4-7 minutes."
3. **Run Topic 1 (Purpose, P1-P2)** → write to `MANIFEST.md` `purpose:` + FAIR `keywords:` (append).
4. **Run Topic 2 (User-info, U1-U5)** → write to `identity_node.yaml`; reflect persona tone in `STATE.md` Hestia greeting block.
5. **Run Topic 3 (Stack, S1-S4)** → write to `inventory_system.yaml` overlay fields.
6. **Run Topic 4 (Hardware, H1-H3)** → write to `identity_node.yaml` `machine_class` / `gpu` / `peripherals`.
7. **Run Topic 5 (Connections, C1-C5)** → write to `inventory_memberships.yaml` + `identity_lattice_protocol.yaml`.
8. **Apply C5 license override**: if operator chose anything other than `private`, update `MANIFEST.md` FAIR `license:` accordingly and emit a one-line note in `CHANGELOG.md` v0.1 entry.
9. **Substitute HOME.md template `{{VARS}}`** (NEW per 2026-05-12 scope amendment): if `LatticeHome.aDNA/HOME.md` exists with `{{VARS}}` (operator forked from v7.x+ template), substitute the 8 vars from interview answers + auto-detected inventory:
   - `{{node_hostname}}` ← `hostname -s` (or operator U1 override)
   - `{{operator}}` ← interview U1
   - `{{machine_class}}` ← interview H1
   - `{{persona}}` ← `Hestia` (constant for this vault class)
   - `{{workspace_root}}` ← `pwd -P` parent (or `$LATTICE_ROOT` if set)
   - `{{vault_count}}` ← derived from `inventory_vaults.yaml` count
   - `{{named_project_count}}` ← derived from `inventory_vaults.yaml` count
   - `{{drift_count}}` ← derived from `inventory_vaults.yaml` drift section
   - Table generators (`{{vaults_table}}`, `{{named_projects_table}}`, `{{drift_table}}`): render from `inventory_vaults.yaml` rows (markdown tables grouped by aDNA class per template structure)
   - If `inventory_vaults.yaml` is empty (new operator, no other vaults yet): render gallery with only this LatticeHome.aDNA row + add a "Next Steps" section linking to `skill_project_fork.md` for the first vault fork
10. **Show summary**: all 19 answers in a single readable block; ask "Confirm and continue, or revise any?" — if revise, jump back to specific question by ID (P1/U2/S1/etc.).
11. **Commit answers**: write all file mutations atomically (track via `files_modified:` list); produce summary report.
12. **Hand off to `skill_node_health_check.md`** — run validator; if exit 0, bootstrap complete; if exit >0, surface drift to operator.

## Interview question table (19 questions × 5 topics)

Each row: question wording (operator-facing, Hestia voice) · type · default · output target · validation · branching.

### Topic 1: Purpose (2 questions)

| # | Question | Type | Default | Output | Validation | Branching |
|---|---|---|---|---|---|---|
| **P1** | "What is this node for? (1-3 sentences — e.g., 'Personal Mac for clinical research and ML experiments', 'Lab workstation for genomics pipelines', 'Edge node for sensor data collection'.)" | free-text | none (operator must answer; min 10 chars; if skipped, persists as `purpose: "unspecified"` with comment) | `MANIFEST.md` `purpose:` + 1-sentence excerpt to `CLAUDE.md` persona-context paragraph | min length 10; max 280 | — |
| **P2** | "Add 1-2 keywords for this node's primary use beyond the standard 5 (`node, inventory, lattice_membership, host_state, hestia`)? (e.g., `clinical_research`, `edge_ml`, `gamedev`, `pure_dev`)" | multi-select with free-text add (0-3) | empty (operator may skip) | `MANIFEST.md` FAIR `keywords:` (append) | snake_case; max 3 additions | — |

### Topic 2: User-info (5 questions)

| # | Question | Type | Default | Output | Validation | Branching |
|---|---|---|---|---|---|---|
| **U1** | "Confirm operator name detected from `git config user.name`: '{detected}'. Use this, or specify alternate?" | confirm-or-override | `{git config user.name}` else `${USER}` | `MANIFEST.md` `operator:` confirms; `identity_node.yaml` `operator_alias:` | non-empty | If override: capture new value |
| **U2** | "What role do you primarily play on this node?" | single-select `[data_scientist, software_engineer, researcher, clinician, student, designer, founder, devops, other]` | `software_engineer` | `identity_node.yaml` `role:` | required | If `other`: free-text |
| **U3** | "Default git author identity — same as operator '{operator}'? Or different (e.g., legal name vs. handle)?" | single-select `[same, different]` | `same` | `identity_node.yaml` `git_author:` | — | If `different`: ask for alternate in `Name <email>` format |
| **U4** | "Optional contact for cross-vault coordination memos: email / handle / leave blank for privacy default." | free-text or skip | skip | `identity_node.yaml` `contact:` (omitted if skipped) | if provided: must contain `@` or `/` | — |
| **U5** | "Hestia persona tone preference: (a) default (warm + Feynman-clear) / (b) terse / (c) formal / (d) playful." | single-select | `default` | `identity_node.yaml` `persona_preferences.tone:`; reflected in `STATE.md` greeting style | — | — |

### Topic 3: Stack (4 questions)

| # | Question | Type | Default | Output | Validation | Branching |
|---|---|---|---|---|---|---|
| **S1** | "Auto-detected programming languages on this node: `{auto_list}`. Mark your **primary** languages (the ones you actively work in; not just installed):" | multi-select from auto-detected list + free-text add | all auto-detected pre-selected | `inventory_system.yaml` `primary_languages:` overlay | ≥1 selection | — |
| **S2** | "Auto-detected IDEs / editors: `{auto_list}`. Which is your primary?" | single-select from auto-detected | first detected (Spacemacs if present, else VSCode, else Cursor, else first) | `inventory_system.yaml` `primary_ide:` overlay | required | — |
| **S3** | "Primary frameworks / toolchains? (Auto-detect found: `{from venv/package.json/Cargo.toml/...}`. Add overlay or leave as-is.)" | multi-select with free-text add | from auto-detect | `inventory_system.yaml` `primary_frameworks:` overlay | snake_case for additions | — |
| **S4** | "Cloud / service providers connected (multi-select): AWS / GCP / Azure / GitHub / HuggingFace / Anthropic API / OpenAI API / Other." | multi-select with free-text add | none (auto-detect unreliable; operator declares) | `inventory_system.yaml` `services_connected:` overlay | — | If `Other`: free-text |

### Topic 4: Hardware (3 questions)

| # | Question | Type | Default | Output | Validation | Branching |
|---|---|---|---|---|---|---|
| **H1** | "Confirm auto-detected machine class: '{detected}' (e.g., 'Apple Silicon Mac, 16-core, 64GB')." | confirm-or-override | auto-detected from `system_profiler SPHardwareDataType` (Mac) or `lscpu + free -h` (Linux) | `identity_node.yaml` `machine_class:` | non-empty | If override: capture alternate |
| **H2** | "GPU info (model + memory). Auto-detected: '{detected_or_NONE}'." | confirm-or-override or `none` | auto-detected from `system_profiler SPDisplaysDataType` (Mac) or `nvidia-smi` (Linux) | `identity_node.yaml` `gpu:` | — | If `none`: omit field |
| **H3** | "Peripherals / setup notes (multi-monitor count, external storage, anything else worth recording): free-text or skip." | free-text or skip | skip | `identity_node.yaml` `peripherals:` | max 200 chars | — |

### Topic 5: Connections (5 questions)

| # | Question | Type | Default | Output | Validation | Branching |
|---|---|---|---|---|---|---|
| **C1** | "Subscribe to any LP lattices at bootstrap? (Multi-select from known IDs, or `skip` to subscribe later via `latlab lattice pull`.)" | multi-select or skip | skip | `inventory_memberships.yaml` `subscribed_lattices:` | known lattice IDs only | — |
| **C2** | "Federate inventory observability with other nodes? (Default: NO — node-private posture.)" | yes/no | `no` (federation block stays `shareable: false / discoverable: false`) | `inventory_memberships.yaml` federation block (overrides if yes) | — | If `yes`: ask which metrics (`tool_versions`, `vault_count`, `hardware_class`, `last_health_check`) + which nodes |
| **C3** | "LP-network identity: peer-id, signing-key path, permission-set. Leave blank if not yet joined." | 3-field form or skip | skip (placeholders stay; `note: filled in when node joins LP network — TBD per LatticeProtocol release`) | `identity_lattice_protocol.yaml` `{peer_id, signing_key_path, permission_set}` | if any field provided: all 3 required | — |
| **C4** | "Marketplace categories of interest (for HOME.md gallery suggestions): `[decks, sites, video, comics, scientific_papers, code, clinical_research, design, other]`." | multi-select or skip | skip | `inventory_memberships.yaml` `marketplace_interests:` | snake_case | If `other`: free-text |
| **C5** | "Default license for new vaults you create on this node: (a) **private** / (b) Apache-2.0 / (c) MIT / (d) CC-BY-4.0 / (e) other-SPDX." | single-select | `private` (matches `MANIFEST.md` FAIR `license: private`) | `identity_node.yaml` `default_new_vault_license:` (consumed by `skill_project_fork.md`) | valid SPDX if `other` | If `other`: free-text SPDX |

**Question count check**: 2 + 5 + 4 + 3 + 5 = **19 questions across 5 topics**.

## Exit codes

| Code | Meaning | Recoverable? |
|---|---|---|
| `0` | Interview complete; all 19 questions answered (or skipped per skip-eligible rules); vault healthy after `skill_node_health_check.md` | n/a (success) |
| `2` | Precondition unmet (fork or inventory_refresh didn't run) | Yes — re-run skill_project_fork → skill_inventory_refresh, then re-invoke |
| `3` | Operator aborted mid-interview (partial state captured; resumable via re-invocation; session log flagged `#interview_partial`) | Yes — re-invoke; resume from last unanswered question |
| `4` | Write conflict (in-flight session editing one of the target files; operator must resolve) | Yes — close other session, re-invoke |

## Composition contract

| Upstream skill | Contract |
|---|---|
| `skill_project_fork.md` | MUST run first; produces empty `LatticeHome.aDNA/` with template defaults. This skill assumes the template structure is intact (CLAUDE.md, MANIFEST.md, STATE.md, AGENTS.md, README.md, HOME.md present). |
| `skill_inventory_refresh.md` | MUST run before this skill. Auto-detected values from `inventory_system.yaml` are consumed as **defaults** for S1-S4 and H1-H2. If `inventory_system.yaml` is missing, this skill falls back to live re-detection but logs `#fallback_inventory_refresh_not_run` in the session. |

| Downstream skill | Contract |
|---|---|
| `skill_node_health_check.md` | MUST run after this skill; validates all 19 written fields parse correctly (`yaml.safe_load` passes) + no required field is left as `agent_init` placeholder. |
| `skill_project_fork.md` (future invocations) | Reads `identity_node.yaml` `default_new_vault_license:` (from C5) as the default `license:` for new forks. |

## Hestia voice register

Operator-facing prompts use Hestia voice (per the node vault's `CLAUDE.md`). Reference phrases:

- **Greeting**: "Welcome to your new node vault. I'm Hestia — the hearth-keeper."
- **Confirmation**: "Got it. Noted." (terse default per U5=a)
- **Clarification**: "Let me make sure I have this right — you said `{paraphrased answer}`. Correct?"
- **Completion**: "All 19 answers captured. Running `skill_node_health_check.md` now to confirm the vault is healthy. Welcome home."
- **Error**: "Hmm, that didn't parse — `{validation_error_brief}`. Can you re-state?"

Tone presets via U5:
- (a) `default` → warm, terse, occasional Feynman-clear analogy
- (b) `terse` → no greeting fluff; pure prompts; no analogies
- (c) `formal` → "Operator," prefix; complete sentences; no contractions
- (d) `playful` → light humor; emoji-eligible (operator-opt-in only)

## Design discipline (D1=b hybrid)

The interview NEVER re-asks what `skill_inventory_refresh.md` already auto-detected. Auto-detected values surface as **confirmation prompts** or **defaults**, not re-asks. The 19 questions target exactly the 7 strict gaps + 2 overlay gaps from `m04b_obj1_dynamic_ux_gap_analysis.md`. If an answer is auto-detectable, it is NOT in this interview.

## Self-reference

This skill demonstrates the **hybrid-bootstrap principle** by *enacting* it: auto-detect what's auto-detectable, hardcode what's universal (the persona spec, the protocol stubs), interview only what's operator-specific. The 5-topic structure mirrors the 5 information dimensions an Org-Vault operator brings to any new node: identity (who am I), purpose (why this node), capabilities (what's on it), surroundings (what's it talking to), and tone (how do I prefer to interact). Written for any Org-Vault, the *structure* (5 topics, hybrid discipline, composition with fork + inventory_refresh) is identical; only the question wording shifts.

## Related

- Spec source: `aDNA.aDNA/how/campaigns/campaign_adna_v2_infrastructure/missions/artifacts/m04b_obj2_skill_node_bootstrap_interview_spec.md`
- Gap analysis: `aDNA.aDNA/how/campaigns/campaign_adna_v2_infrastructure/missions/artifacts/m04b_obj1_dynamic_ux_gap_analysis.md` (7 + 2 gaps mapped to 5 topics)
- Implementing mission: `aDNA.aDNA/how/campaigns/campaign_lattice_workspace_ux/missions/mission_lwx_01_dynamic_bootstrap_interview.md`
- Naming constraint: `aDNA.aDNA/what/decisions/adr_009_aDNA_naming_convention.md` (skill never re-asks if `node` is a valid project name — fixed by `skill_project_fork.md` constants)
- Upstream-discipline: `.adna/how/skills/skill_upstream_contribution.md`
