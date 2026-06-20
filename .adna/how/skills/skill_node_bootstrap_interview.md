---
type: skill
skill_type: agent
created: 2026-05-12
updated: 2026-06-19
status: active
category: onboarding
trigger: Workspace router Step 0.3 — operator accepts `Home.aDNA/` bootstrap; runs after `skill_project_fork.md` + `skill_inventory_refresh.md` to fill operator-specific fields the auto-detect engine cannot infer
last_edited_by: agent_hestia
related_skills: [skill_project_fork, skill_inventory_refresh, skill_node_health_check]
related_artifacts:
  - aDNA.aDNA/how/campaigns/campaign_adna_v2_infrastructure/missions/artifacts/m04b_obj2_skill_node_bootstrap_interview_spec.md  # source spec
  - aDNA.aDNA/how/campaigns/campaign_adna_v2_infrastructure/missions/artifacts/m04b_obj1_dynamic_ux_gap_analysis.md  # 7+2 gaps this skill closes
question_count: 19  # base mode: 5 topics × {2,5,4,3,5}. Exemplar mode adds an OPTIONAL Topic 6 (theming, T1-T5) — default-driven, does not change the base 19.
estimated_runtime: "4-7 minutes"  # operator-paced; defaults speed it up (+~1 min if exemplar Topic 6 runs)
operator_persona: Hestia
exit_codes: [0, 2, 3, 4]
tags: [skill, agent, onboarding, dynamic_bootstrap, interview, node_adna, hestia, hybrid_d1_b, v7_x, exemplar_invocation, hearthstone_p4]
---

# skill_node_bootstrap_interview

Hybrid interview that fills the **operator-specific** fields of a freshly-forked `Home.aDNA/` vault — purpose, user-info, stack overlay, hardware confirm, and lattice connections. The interview NEVER re-asks what the auto-detect engine (`skill_inventory_refresh.md`) already captured. 19 questions across 5 topics; 4-7 min runtime; Hestia voice register.

When the operator opts into the **premium themed HOME** (`exemplar_mode` — chosen at the router/fork or via `skill_project_fork --exemplar-home`), an OPTIONAL **Topic 6 (theming)** runs and Step 9 materializes the exemplar bundle instead of the plain base HOME. Declining keeps the plain base `.adna/HOME.md` — exemplar is always opt-in.

> **Dev-graph canonical source (mirror established Hearthstone P4, 2026-06-19).** This is the dev-graph copy of the skill; `.adna/how/skills/skill_node_bootstrap_interview.md` is assembled from *here* by `skill_template_release` (the dev graph is the source of truth — there is no auto-sync). It was a missing mirror until P4 (the `.adna/` copy had been the only canonical version); the exemplar-invocation wiring below (Topic 6 + the Step-9 exemplar branch) is authored here and ships to `.adna/` at Hearthstone P5. **Edit here, never `.adna/`** (Workspace Standing Rule 1).

## Trigger

Invoked by the workspace router Step 0.3 flow after operator accepts `Home.aDNA/` bootstrap. This skill runs as **Step 3** of the bootstrap chain:

```
Step 1: skill_project_fork.md    → empty Home.aDNA/ from template
Step 2: skill_inventory_refresh   → auto-detect inventory_*.yaml
Step 3: skill_node_bootstrap_interview  ← THIS SKILL
Step 4: skill_node_health_check   → validate vault is healthy
```

If invoked outside this chain (e.g., re-run later by an operator who wants to revise answers), exits 2 unless preconditions §1 hold.

## Read

Before asking any question, load:

| File | Purpose |
|---|---|
| `Home.aDNA/MANIFEST.md` | Existing template values to confirm/override |
| `Home.aDNA/STATE.md` | Current operational state (preserve unrelated content) |
| `Home.aDNA/what/inventory/inventory_system.yaml` | Auto-detected machine class, GPU, languages, IDEs, frameworks (Step 2 output) |
| `Home.aDNA/what/inventory/inventory_vaults.yaml` | Existing `.aDNA/` vaults on the node (informs C1 default suggestions) |
| `Home.aDNA/who/identity/identity_node.yaml` | Current operator alias from `skill_project_fork` |
| `Home.aDNA/who/identity/identity_lattice_protocol.yaml` | LP placeholders (operator may fill C3) |
| `Home.aDNA/what/inventory/inventory_memberships.yaml` | Federation defaults (privacy-first; operator may override at C2) |
| `Home.aDNA/CLAUDE.md` | Hestia persona block — confirm voice register for prompts |
| `Home.aDNA/CHANGELOG.md` | Append v0.1 footnote at completion |

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

**Not touched**: any partner vault · `~/aDNA/CLAUDE.md` (workspace router) · `~/aDNA/.adna/` (template) · `Home.aDNA/AGENTS.md` · `Home.aDNA/README.md` · `Home.aDNA/CHANGELOG.md` body · all node-protocol AGENTS.md stubs · all 4 node-skills · `inventory_vaults.{md,yaml}` · `inventory_memberships.md` narrative (only YAML mutates).

**Exemplar mode adds** (only when `exemplar_mode == true`): the 5 Topic-6 theming answers → `identity_node.yaml` `persona_preferences.theme:` (accent triple + canvas text pair + greeting + banner), and the materialized exemplar bundle over the fork — the themed `HOME.md` (replaces the base), the `{{persona_lower}}_accent.css` + `{{persona_lower}}_canvas.css` snippets, the `what/code/` generators, the `who/assets/` + `who/curation/` skeleton, and `ONBOARDING.md`. This overlay is the same one `skill_project_fork.md` Step 4.5 performs; whichever runs first lays it down (idempotent).

## Steps

1. **Verify preconditions**: `Home.aDNA/` exists (forked by `skill_project_fork.md`); `inventory_vaults.yaml` + `inventory_system.yaml` exist (auto-detected by `skill_inventory_refresh.md`). If any precondition fails → exit `2: precondition_unmet`.
2. **Greet operator in Hestia voice**: "Welcome to your new node vault. I'm Hestia — the hearth-keeper. Let me ask 19 quick questions to fill in the operator-specific fields. Most have sensible defaults; press Enter to accept. We'll be done in 4-7 minutes."
3. **Run Topic 1 (Purpose, P1-P2)** → write to `MANIFEST.md` `purpose:` + FAIR `keywords:` (append).
4. **Run Topic 2 (User-info, U1-U5)** → write to `identity_node.yaml`; reflect persona tone in `STATE.md` Hestia greeting block.
5. **Run Topic 3 (Stack, S1-S4)** → write to `inventory_system.yaml` overlay fields.
6. **Run Topic 4 (Hardware, H1-H3)** → write to `identity_node.yaml` `machine_class` / `gpu` / `peripherals`.
7. **Run Topic 5 (Connections, C1-C5)** → write to `inventory_memberships.yaml` + `identity_lattice_protocol.yaml`.
8. **Apply C5 license override**: if operator chose anything other than `private`, update `MANIFEST.md` FAIR `license:` accordingly and emit a one-line note in `CHANGELOG.md` v0.1 entry.
8.5. **Run Topic 6 (Theming, T1-T5) — EXEMPLAR MODE ONLY** (skip entirely when `exemplar_mode == false`): collect the persona accent triple + canvas text pair + greeting + banner, each defaulting to the `SUBSTITUTIONS.md` §2 per-persona lookup so the operator can accept all defaults in one keypress. Writes `identity_node.yaml` `persona_preferences.theme:` and feeds the Step-9 exemplar profile. `exemplar_mode` normally arrives from the router/fork (`skill_project_fork --exemplar-home`, or any Home-class fork); if it did not but `Home.aDNA/HOME.md` is the themed exemplar template, offer it here ("Use the premium themed HOME — banner · §Gallery · §Topology · persona accent? Default: yes for a Home node."). Decline → `exemplar_mode = false`, plain base HOME at Step 9.
9. **Substitute HOME.md template `{{VARS}}`** (NEW 2026-05-12; exemplar branch added Hearthstone P4): if `Home.aDNA/HOME.md` exists with `{{VARS}}` (operator forked from v7.x+ template), substitute from interview answers + auto-detected inventory. **Two profiles — pick by `exemplar_mode`:**

   **(a) Base profile** — `exemplar_mode == false` (default): keep the plain base `.adna/HOME.md`; substitute the 8 base vars, tables as **markdown** grouped by aDNA class:
   - `{{node_hostname}}` ← `hostname -s` (or operator U1 override) · `{{operator}}` ← interview U1 · `{{machine_class}}` ← interview H1 · `{{persona}}` ← `Hestia` (constant for this vault class) · `{{workspace_root}}` ← `pwd -P` parent (or `$LATTICE_ROOT` if set)
   - `{{vault_count}}` / `{{named_project_count}}` / `{{drift_count}}` ← derived from `inventory_vaults.yaml` (count + drift section)
   - Table generators (`{{vaults_table}}`, `{{named_projects_table}}`, `{{drift_table}}`): render from `inventory_vaults.yaml` rows as **markdown tables** grouped by aDNA class (base template structure)
   - If `inventory_vaults.yaml` is empty (new operator, no other vaults yet): render gallery with only this Home.aDNA row + a "Next Steps" section linking to `skill_project_fork.md` for the first vault fork

   **(b) Exemplar profile** — `exemplar_mode == true` (Topic 6 ran / `--exemplar-home`): materialize `how/templates/template_node_adna_exemplar/HOME.md.template` *over* the base HOME and substitute the **full shared + theming catalog** per the bundle's `SUBSTITUTIONS.md`:
   - all base vars above **plus** `{{persona_lower}}` (derived), `{{healthy_count}}` / `{{blocked_count}}` (← `inventory_vaults.yaml` health section), `{{last_inventory_refresh}}` (← `inventory_vaults.yaml` `updated:`), `{{interview_date}}` (today), `{{last_health_check}}` (← `STATE.md` / last `skill_node_health_check`)
   - the 9 theming vars from Topic 6: `{{persona_greeting}}`, `{{banner_image}}`, `{{banner_title}}`, `{{accent_primary_hex}}` / `secondary` / `tertiary`, `{{canvas_text_strong_hex}}` / `em_hex`; `{{health_detail_note}}` defaults to the **empty string** (live-node narration field — not asked; keeps skeleton parity per SUBSTITUTIONS §parity)
   - **Callout-fold `>`-prefix profile (LOAD-BEARING — M3.4 / Hearthstone P4):** in the exemplar HOME the all-vaults index and the non-vault list live INSIDE `> [!abstract]-` / `> [!note]-` disclosure folds, so `{{vaults_table}}` and `{{named_projects_table}}` must supply **callout-body lines ONLY, each `>`-prefixed**:
     - `{{vaults_table}}` → one `> - **<Category> (n)** · [Name](../Name.aDNA/) · …` line per aDNA class (links flow from `inventory_vaults.yaml`, never hand-pasted)
     - `{{named_projects_table}}` → `> - **<group>** · [name](../path/) · …` lines for named-projects / external-deps / archived groups; or `> No named projects on this node yet.` when inventory has none
     - **Do NOT** emit a `<div class="vault-grid">` or a blank-line-bearing markdown table here — either breaks the callout open. (The base profile's grid/table is the WRONG shape for the exemplar HOME; this is the single substitution difference that most often renders incorrectly.)
   - then materialize the rest of the bundle (the `{{persona_lower}}_accent.css` + `{{persona_lower}}_canvas.css` snippets, the `what/code/` generators, the `who/assets/` + `who/curation/` skeleton, `ONBOARDING.md`) and run the first `build_topology_canvas.py` / `build_curation_cards.py` regen — identical to `skill_project_fork.md` Step 4.5 (whichever runs first lays it down; idempotent). Accent defaults: `SUBSTITUTIONS.md` §2 per-persona lookup.
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

### Topic 6: Exemplar theming (OPTIONAL — exemplar mode only; 0 questions in base mode)

Runs at Step 8.5 only when `exemplar_mode == true` (operator chose the premium themed HOME, or `skill_project_fork --exemplar-home`). Every question defaults to the persona accent lookup (`how/templates/template_node_adna_exemplar/SUBSTITUTIONS.md` §2), so accepting all defaults is one keypress. Covers the 9 exemplar theming vars + the persona pick. Does **not** count toward the base 19.

| # | Question | Type | Default | Output | Validation | Branching |
|---|---|---|---|---|---|---|
| **T1** | "Persona for this node's hearth (drives accent + greeting + CSS): default `Hestia`, or name another (e.g., Athena)?" | confirm-or-override | `Hestia` | `{{persona}}` / `{{persona_lower}}`; swaps the CLAUDE persona-accent blocks (per `skill_project_fork` Step 3.5) | non-empty | If non-Hestia **and** no `SUBSTITUTIONS.md` §2 lookup row: T2/T3 become required (operator supplies hexes) |
| **T2** | "Accent triple (primary / secondary / tertiary hex)? Default = the `{{persona}}` lookup (Hestia: `#663399` / `#f5c97a` / `#7dcfff`)." | 3-hex form or accept default | persona §2 lookup row | `{{accent_primary_hex}}` / `{{accent_secondary_hex}}` / `{{accent_tertiary_hex}}` | each matches `#[0-9a-fA-F]{6}` | — |
| **T3** | "Canvas card text pair (strong / em hex) — a near-white tinted toward your primary, and a soft pastel of it. Default = the `{{persona}}` lookup." | 2-hex form or accept default | persona §2 lookup row | `{{canvas_text_strong_hex}}` / `{{canvas_text_em_hex}}` | each matches `#[0-9a-fA-F]{6}` | — |
| **T4** | "Persona greeting — the home's one-line epigraph. Default = the persona archetype line." | free-text or accept default | persona archetype (`Tending the hearth.` for Hestia) | `{{persona_greeting}}` | max 80 chars | — |
| **T5** | "Banner image filename (drop the file into `who/assets/banners/`; a placeholder ships until you supply one) + banner title?" | 2-field or accept default | `banner_{{persona_lower}}.jpg` / `{{node_hostname}} Home` | `{{banner_image}}` / `{{banner_title}}` | filename basename; title max 60 | — |

> `{{health_detail_note}}` is **not** asked (defaults to empty — a live-node narration field filled later; keeps skeleton parity). The count-derived vars (`{{vault_count}}`, `{{healthy_count}}`, `{{blocked_count}}`, `{{drift_count}}`, `{{last_inventory_refresh}}`) come from `inventory_vaults.yaml`, not the operator.

**Question count check**: base mode = 2 + 5 + 4 + 3 + 5 = **19 questions across 5 topics**. Exemplar mode adds an OPTIONAL **Topic 6** (T1-T5, theming) — default-driven, accept-all-in-one-keypress; not counted in the base 19.

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
| `skill_project_fork.md` | MUST run first; produces empty `Home.aDNA/` with template defaults. This skill assumes the template structure is intact (CLAUDE.md, MANIFEST.md, STATE.md, AGENTS.md, README.md, HOME.md present). **Passes `exemplar_mode`** (set by its `--exemplar-home` flag or a Home-class fork) into this skill — Topic 6 + the Step-9 exemplar branch consume it. If `skill_project_fork` already ran its Step 4.5 overlay, Step 9 here is idempotent (re-substitutes the same themed HOME from the same answers). |
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
