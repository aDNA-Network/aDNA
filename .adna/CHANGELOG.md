# Changelog

All notable changes to the aDNA knowledge architecture are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## Version Policy

aDNA tracks **two independent version numbers**:

| Track | File | Field | What it covers |
|-------|------|-------|---------------|
| **Governance** | `CLAUDE.md` | `version` (frontmatter) | Vault structure, agent protocol, safety rules, templates, skills |
| **Standard** | `what/docs/adna_standard.md` | Document title | Normative specification — triad structure, object schemas, FAIR metadata |

Both tracks use **Major.Minor** versioning (no patch level):

| Change type | Major bump | Minor bump |
|-------------|-----------|------------|
| **Governance** | Breaking changes to vault structure, CLAUDE.md format, or frontmatter schema | New features, templates, skills, context topics, non-breaking additions, corrections |
| **Standard** | Breaking changes to triad structure, object schemas, or FAIR envelope format | New sections, clarifications, federation stubs, factual fixes |

**Canonical version location**: `CLAUDE.md` frontmatter `version` field (governance track). The migration system (`how/migrations/`) uses this field for pre-flight checks.

Changelog entries are organized by **governance version** (primary heading). Standard version changes are noted within entries when they coincide.

---

## [Unreleased]

> Minor **Governance** change. **Standard track: no change.**

### Changed
- **Workspace-root default flipped `~/lattice/` → `~/aDNA/`** across all prescriptive onboarding/usage docs (README, CONTRIBUTING, STATE, quests, skills, templates, overview/pattern docs). Documentation-default flip, **not a breaking change** — `<workspace_root>` is detected (the directory containing `.adna/`), never hardcoded; any path works. Historical records (this changelog, v6→v7 upgrade guide, v5.2→v6.0 migration) intentionally keep their original `~/lattice` paths, now with forward-pointer notes.

### Added
- **`skill_workspace_path_migration.md` (NEW)**: turnkey agentic transition for operators on a legacy workspace root (e.g. `~/lattice/` → `~/aDNA/`) — symlink-shim reversibility, prefix-anchored sweep, KEEP-set invariants, anchor re-pointing, harness re-key.
- **`migrate_workspace_root.sh` (NEW)**: standalone shell companion — mechanical preflight (DRY_RUN), move + shim, proven-safe 4-form sweep, dual residue proof + KEEP-set invariant check, per-repo commit discipline; prints the by-value anchor checklist and rollback ledger. Distills the reference node's migration (gap register G1–G14).
- **Legacy workspace-root detection (Step 0)** in `how/templates/template_workspace_claude.md` — a legacy-root workspace is offered the migration once on session start; never auto-migrates.

## [v7.0] — 2026-05-18

> Major **Governance** bump. **Standard track: no change** (stays at v2.2). Ratified by ADR-011 (semver discipline) at this tag.

### Added
- **Repo flatten**: `.adna/` IS the git repo (no more `adna/.adna/` two-level structure). New clone target: `git clone https://github.com/LatticeProtocol/aDNA.git .adna` (per ADR-006; mixed-case canonical per 2026-05-18 amendment). Symlink `lattice/.adna -> adna/.adna` removed. (M03)
- **`node.aDNA/` opt-in pattern**: Local-node operational inventory vault. Persona: Hestia. Forward-reference per ADR-004 from `node.aDNA/CLAUDE.md` to `aDNA.aDNA/how/campaigns/`. (M04)
- **Cross-project routing hook** in `.adna/CLAUDE.md` §Agent Protocol §Startup Checklist (after step 9) — enables node.aDNA-aware fork routing; vault session-start agents check for `node.aDNA/` presence and route through the per-node operational vault before project-specific routing. (M04 S2; commit `e3b3bcc`)
- **`HOME.md` template** — Workspace-router HOME page with 19+ `{{...}}` placeholder substitution points (vaults_table, hostname, operator, etc.); served by `skill_node_bootstrap_interview` Step 9 substitution engine. Sandbox-validated under M-LWX-01 verification matrix (9/9 gates PASS). (M-LWX mini-campaign; closed 2026-05-13)
- **`skill_node_bootstrap_interview.md`** — 19-question hybrid bootstrap UX skill for `node.aDNA/` first-fork experience (purpose / user-info / stack / hardware / connections; ~4-7 min). Fills `MANIFEST.md` + `who/identity/identity_node.yaml` + `what/inventory/inventory_*.yaml` + `CHANGELOG.md` + HOME.md `{{VARS}}` from operator answers. (M-LWX-01; commit `8673383`)
- **5 `node_operations` skills graduated to `.adna/` template**: `skill_inventory_refresh.md` + `skill_node_credentials_audit.md` + `skill_node_health_check.md` + `skill_update_all_vaults.md` (4 graduated from `node.aDNA@411660e` at `campaign_federation_beta_planning` M-H.1.5 1b; commit `03198f8`) + `skill_node_bootstrap_interview.md` (M-LWX-01). Each carries `graduated_from`/`graduated_at`/`graduated_via` provenance frontmatter. AGENTS.md updated with `node_operations` category row.
- **`skill_vault_publish.md` (NEW)**: Vault → GitHub `git push` flow. Replaces ad-hoc `.publish-clone/` rsync workaround. (M05; ratified by ADR-010)
- **`skill_git_remote_setup.md` (NEW)**: First-time `git remote add` + `gh repo create` configuration for fresh vaults. (M05)
- **`skill_deploy.md` (NEW)**: Idempotent installer for the pre-push sanitization hook. (M05)
- **`skill_publish_tarball.md` (NEW)**: Optional offline-shipping tarball flow. (M05)
- **`skill_iii_setup.md` (NEW)**: Consumer-onboarding skill for adding an `iii/` wrapper to a new vault (federation_ref schema, `kind:` enum walkthrough, minimal vs full-extension shapes, downstream-safety check). Byte-identical to canonical at `III.aDNA/how/skills/`; backed by 5 live MB-1..MB-5 wrappers as worked precedents. (III Campaign B MB-6 publish; commit `c32930e`)
- **Pre-push sanitization hook** (LAYER_CONTRACT §4 v0.1): 7 sanitization rules (path leakage / secret patterns / filename patterns / large binaries / frontmatter confidential / frontmatter draft / operator deny list). Installed via `skill_deploy`. (M05)
- **Pre-push sanitization hook self-test fixtures + `--self-test` mode upgrade** — 8 fixtures (3 PASS-path + 5 FAIL-path covering R1 path leakage / R2 secret patterns / R3 filename patterns / R4 large binaries / R5-R7 frontmatter rules); hook `--self-test` mode upgraded from warn-and-skip stub to real validation logic (PASS 7/7). Verification-as-first-class deliverable (M05 AAR §Conceptual contributions #1). (M05 S2; commit `dfced67`)
- **`how/airlock/AIRLOCK.md` stub** at template level — entry-path index for cross-graph agent traffic. Adoption is opt-in per vault. (M03; ratified by ADR-008)
- **Naming convention codification** (ADR-009): `<name>.aDNA/` directory ↔ `<name>.aDNA.git` GitHub repo isomorphism; snake_case `<name>`; grandfathered exceptions documented. Renames are operator-discretionary; per-vault application is the v3-EC successor's scope. (ADR-009 ratified at M03 phase gate)
- **Semver discipline ADR** (ADR-011): Codifies the two-track Major.Minor-only policy already practiced in this CHANGELOG. (M06; this entry IS the first release governed by it.)
- **`template_workspace_claude.md`**: Workspace-router CLAUDE.md template extracted from the legacy outer `adna/CLAUDE.md` per ADR-007. Directly installable to `~/lattice/CLAUDE.md`. (M03)
- **CI workflow caller-usage URL update** to `LatticeProtocol/aDNA` (3 reusable workflows). (M03)
- **Template-root `.gitignore`**: Created with v7.0 exclusion set (`deploy/`, `what/local/`, `how/local/`, `who/operators/`, `dist/`, `.publish-clone/`, `.publish-clone.bak/`, `private/`, `*.dryrun.log`, `*.tar.gz`). (M03; per Obj 5 audit §5 G-1)

### Changed
- **GitHub repo rename**: `LatticeProtocol/Agentic-DNA` → `LatticeProtocol/aDNA` (per ADR-006, amended 2026-05-18 to canonicalize mixed-case form matching realized GitHub state and the `<name>.aDNA/` directory-suffix convention). GitHub URL forwarding preserves existing clones; new clones use the canonical short-name URL. Operators with lowercase remotes may update at their own cadence via `git -C ~/lattice/.adna remote set-url origin https://github.com/LatticeProtocol/aDNA.git`. (M03; ADR-006 amendment 2026-05-18 M06 S2 D1)
- **`adna/CLAUDE.md` (outer wrapper) → `template_workspace_claude.md`**: Repurposed as a template for the workspace router (per ADR-007); now lives at `.adna/how/templates/`. (M03)
- **`deploy_manifest.yaml` location**: Moved from repo root to `.github/deploy_manifest.yaml`. `sync_includes:` simplified to root-level paths post-flatten. (M03; per Obj 5 audit §3 D-1)
- **`prepare_for_onboarding.sh` location**: Moved from template root to `how/skills/l1_upgrade/` OR renamed to `prepare_for_l1_upgrade.sh` (operator-decided). The L1-specific script no longer pollutes top-level discoverability. (M03; per Obj 5 audit §4 P-1)
- **`skill_workspace_upgrade.md`**: Symlink-creation step (lines 105-113) removed; flatten path replaces it. New §Step-3-alternative: install workspace router from `template_workspace_claude.md`. (M03)
- **`skill_project_fork.md`**: Exclusion list expanded for post-flatten layout (`.git/`, `.github/`, `README.md`, `LICENSE`, `setup.sh`, `prepare_for_onboarding.sh`, `deploy_manifest.yaml`). Naming-convention warning added (per ADR-009): warn on non-conformant `<name>.aDNA/` forms. (M03)
- **`skill_lattice_publish.md`**: Light v7.0 path-drift updates only — scope unchanged (latlab CLI registry publish). (M05; per ADR-010)
- **CLAUDE.md frontmatter `version:`**: `"6.0"` → `"7.0"` (this entry is the change). `last_edited_by: agent_init` → `agent_stanley`. (M06; see Frontmatter section below)
- **Skills inventory table in `.adna/CLAUDE.md`**: expanded to reflect the v7.0 skill family — `skill_workspace_upgrade.md` row added (Issue I-2 from M01 Obj 1 §2); 5 new publish-family skills added (`skill_vault_publish`, `skill_git_remote_setup`, `skill_deploy`, `skill_publish_tarball`); `skill_iii_setup.md`; 5 `node_operations` skills (`skill_node_bootstrap_interview` + `skill_inventory_refresh` + `skill_node_credentials_audit` + `skill_node_health_check` + `skill_update_all_vaults`). (M03 + M05 + M-LWX + III MB-6 + federation_beta_planning M-H.1.5)
- **Standard track v2.2** is **unchanged**. Verified by S2 S4 reading pass (title at line 3 of `adna_standard.md` is canonical). The stale `*End of aDNA Universal Standard v2.0*` footer at line 1483 is corrected to `*End of aDNA Universal Standard v2.2*` as a one-line audit fix. (M06; per M01 Obj 6 recommendation §2-D)

### Deprecated
- **`skill_workspace_init.md`** — was already deprecated in v6.0; **formally retired** in v7.0. File preserved per Standing Order #6 (archive, never delete). (M03)
- **Outer wrapper `adna/CLAUDE.md`** — converted to `template_workspace_claude.md` per ADR-007; the "outer wrapper" pattern is no longer canonical. (M03)
- **`.publish-clone/` rsync workaround pattern** — superseded by `skill_vault_publish.md`. Vaults using it (currently only Spacemacs.aDNA) retire on adoption of the v7.0 publish flow. (M05; coordinated via Daedalus coord memo and v3 successor M05-EC.)

### Removed
- **Symlink `lattice/.adna -> adna/.adna`** at workspace root — replaced by direct `.adna/` git clone. (M03)
- **Outer `adna/` directory** at workspace root — flattened. (M03)
- **`how/standard/skills/skill_publish_lattice.md`** (Spacemacs-local rsync skill) — retired upstream-via-v7.0; per-vault retirement is v3 successor scope. (Coordinated, not removed in this campaign.)

### Fixed
- **`adna_standard.md` line 1483** — stale `*End of aDNA Universal Standard v2.0*` footer corrected to v2.2. (M06; one-line audit fix per M01 Obj 6 recommendation §2-D)
- **CI workflow caller-usage URLs** — `LatticeProtocol/Agentic-DNA/.github/workflows/...@main` → `LatticeProtocol/aDNA/.github/workflows/...@main` in all three reusable workflows. (M03; per Obj 5 audit §2 W-1)
- **`.adna/CLAUDE.md` skills inventory table** — added missing `skill_workspace_upgrade.md` row (Issue I-2 from M01 Obj 1 §2). (M03)
- **`HOME.md` inline `{{TOKEN}}` comment rephrase** — 4 inline HTML-comment lines (40/54/65/104) rephrased to plain prose so `string.replace()`-based substitution (per `skill_node_bootstrap_interview.md` Step 9) does not naively expand placeholder tokens inside documentation comments. Fixes ~4.9KB of source-bloat in sandbox-rendered HOME.md (12,977 bytes → 8,069 bytes gold parity). End-user view unchanged (HTML comments are render-invisible); source-time bloat would have inflated git history + agent-context budget on every interview-driven fork. (M-LWX-03 Finding 1 fix; commit `202c9ec`)
- **Skill path mismatch** — 4 v7.0 publish-family skills referenced pre-flatten `.adna/how/standard/hooks/...`. Post-M03-flatten, vaults are siblings of `.adna/` with vault-local hooks at `how/standard/hooks/...`. Fix: skills check canonical sibling path first, fall back to legacy `.adna/how/...` for compatibility. (M05 S2 defect; commit `dfced67`)
- **R2 secret-pattern POSIX/PCRE quote-class bug** — All 7 secret patterns used `[\x27\x22]?` for the optional quote class, but POSIX `grep -E` interprets `\xNN` literally (PCRE-only). Fix: bash ANSI-C `$'\x27\x22'` quote forms. (M05 S2 defect; commit `dfced67`)

### Security
- **Pre-push sanitization hook** (R1-R7): defense-in-depth against accidentally pushing local context, secrets, large binaries, or operator-restricted files. Installed via `skill_deploy`. Bypassable with `--no-verify` (operator-discretionary; not recommended). (M05)

### Migration
- [`upgrade_v6_to_v7.md`](how/docs/upgrade_v6_to_v7.md) (M08a finalized 2026-05-11; M06 S2 copied to canonical template destination per M08a Items Deferred #14 fold-in). Ships in v7.0 template so operators have actionable migration steps the moment they pull. Per-vault coordination memos delivered to ~17 vaults + external partners (Wilhelm Foundation, TAPP, Super League). Public announcement at GitHub release.

### Standard track
- **No change.** Standard stays at v2.2 (line 3 title canonical; line 1483 footer fix is editorial, not a version bump).

---

## [v6.0] — 2026-04-03

### Changed
- **Identity rename**: Display name `adna` → `Agentic-DNA` across all governance files, docs, and context. GitHub repo renamed to `LatticeProtocol/Agentic-DNA`.
- **Naming convention**: `Agentic-DNA` = display name, headings, repo name; `aDNA` = abbreviation in running text; `adna` lowercase preserved in protocol URIs, directory names, tags, and frontmatter topics.
- `.aDNA` directory convention: `adna_standard.md` §3.5 with RFC 2119 naming rules, `skill_project_fork.md` auto-appends `.aDNA` suffix, CLAUDE.md workspace detection uses `*.aDNA/` glob.
- Clone command updated: `git clone https://github.com/LatticeProtocol/Agentic-DNA.git adna` (local dir stays `adna/`).
- Version bump: CLAUDE.md `5.7` → `6.0`.
- `how/missions/AGENTS.md`: Mandatory AAR before `status: completed`, git-aware state verification.
- `how/campaigns/AGENTS.md`: Verifiable DG criteria, campaign AAR step, context graduation sequencing.
- CLAUDE.md: 6 standing orders + git coordination section (5 rules + truth hierarchy).
- `template_mission.md`: AAR section appended.
- `template_campaign.md`: `calibrated_sessions`, `estimation_class` fields added, campaign AAR section.
- `lattice_yaml_schema.json`: `lattice_type` enum expanded 4→7 (added `skill`, `infrastructure`, `context_set`).
- `adna_standard.md` §7.2: Required base fields updated 5→6 (added `status`).
- Template count: 20→22.

### Fixed
- `CONTRIBUTING.md`: `validate_lattice.py` → `lattice_validate.py` (correct script name).
- `CONTRIBUTING.md`: Removed reference to nonexistent `calibrate_token_estimates.sh`.
- `skill_sqlite_persistence.md`: Added `status: proposed` to frontmatter (was missing status semantics).
- `governance_agent_protocol.md`: Added `runtime: claude_code` to frontmatter for clarity.
- Count reconciliation: context library 4→5 topics, 23→27 subtopics; adna_core 10→13; skills 7→13; example lattices 14→15; standard version v2.1→v2.2 references corrected.
- `adna_validate.py`: Frontmatter MUST violations now reported as errors (were warnings).
- `canvas2lattice.py`: `_sanitize_node_id()` converts canvas UUIDs to valid lattice IDs.
- Schema/validator/spec triple divergence resolved — all three sources now agree on 7 lattice types and 6 required fields.

### Added
- `template_aar_lightweight.md` — 5-line AAR format (Worked/Didn't/Finding/Change/Follow-up).
- `template_campaign_mission.md` — campaign-linked mission template with campaign_id, exit gate, AAR.
- PR #1 integration acknowledgment (ariaxhan system_configuration contribution).

---

## [v5.7] — 2026-03-23

### Added
- `role: template` marker in `MANIFEST.md` frontmatter — distinguishes the base template from forked projects
- `how/skills/skill_project_fork.md` — dedicated skill for forking `adna/` into a new project directory
- `~/lattice/` as the canonical workspace convention for L0 nodes
- L0 compute tier in CLAUDE.md Compute Tiers table (local knowledge architecture, no compute services)
- Workspace convention diagram in CLAUDE.md Template Detection section

### Changed
- `CLAUDE.md` v5.6→v5.7: merged "First-Run Detection" + "Workspace Bootstrap Detection" into unified "Template Detection & Project Setup" flow
- `skill_onboarding.md` now runs exclusively in forked projects, never in the base template
- `skill_workspace_init.md` Step 4 delegates project creation to `skill_project_fork.md`
- All documentation updated from `~/Projects/` to `~/lattice/` as the recommended workspace root
- `README.md` Quick Start updated with `~/lattice/` clone instructions and template-aware setup flow
- `projects_folder_pattern.md` updated with `~/lattice/` as canonical workspace root and `role: template` design principle
- `workspace_claude_md.template` updated with fork preparation steps (strip `role: template`, set `agent_init`)
- `STATE.md` next steps updated with `~/lattice/` convention
- Peripheral files updated: `skill_l1_upgrade.md`, `skill_lattice_publish.md`, `tutorial_lattice_publishing.md`, `tools/AGENTS.md`, `quest_l1_onboarding.md`

### Design decisions
- `adna/` stays clean — never customized by onboarding. `git pull` always safe.
- `role: template` in MANIFEST.md is the canonical detection mechanism (explicit, git-independent)
- `~/lattice/` is a strong recommendation, not mandatory — system works in any location

---

## [v5.5] — 2026-03-20

### Added
- `VISION.md` — ecosystem vision document (decentralized frontier lab model, participation ladder)
- "Ecosystem & Vision" section in `README.md` linking to VISION.md
- `VISION.md` row in README Further Reading table

### Changed
- `CLAUDE.md` version bump: `5.4` → `5.5`
- Template counts corrected across all governance files: `17` → `20` (CLAUDE.md, MANIFEST.md, README.md, STATE.md)
- `MANIFEST.md` template table expanded with 6 missing rows (data_record, folder_note, governance, migration, side_quest, quest_result)
- `MANIFEST.md` architecture tree updated with `community/` directory
- `README.md` tree diagram updated with `community/` directory
- `STATE.md` updated to v5.5, added community infrastructure to What's Working, added v5.3-v5.5 upgrade entries

---

## [v5.4] — 2026-03-20

### Added
- `community/quests/` — side-quest experiment specifications directory
- `community/results/` — structured result submissions directory
- `community/tools/aggregate_results.py` — reference aggregation script (stdlib only)
- `community/AGENTS.md` — community directory agent guide
- `how/templates/template_side_quest.md` — quest specification template
- `how/templates/template_quest_result.md` — result submission template
- `what/docs/side_quest_guide.md` — participation guide (find, run, submit quests)
- 2 example quests: `quest_frontmatter_comparison` (medium), `quest_migration_smoke_test` (easy)
- Side-Quest Awareness section in `CLAUDE.md`

### Changed
- `CLAUDE.md` version bump: `5.3` → `5.4`
- `AGENTS.md` project structure updated with `community/` directory
- `README.md` contributing section updated with side-quest mention

---

## [v5.3] — 2026-03-20

### Added
- `how/skills/skill_upstream_contribution.md` — agentic upstream contribution protocol
- Upstream Contribution Awareness section in `CLAUDE.md`
- Upstream Contribution Awareness section in root `AGENTS.md`
- Contributing section in `README.md`

### Changed
- `CONTRIBUTING.md` revised — Agent Contribution Mode replaces static PR-Context pattern; organic discovery over structured proposals
- `CLAUDE.md` version bump: `5.2` → `5.3`
- Code of Conduct reference updated to forward-looking note (pending `CODE_OF_CONDUCT.md`)

### Removed
- Empty `community/proposals/` directory (superseded by agentic backlog pattern)
- Empty `.github/ISSUE_TEMPLATE/` directory (standard GitHub issues sufficient for now)

### Tooling (non-versioned, built in lattice-labs campaign LSU)
- `compliance_checker.py` — 10-dimension compliance scoring for vault objects (~1085 LOC)
- 4 object migration prompts: `migrate_object_{skill,module,dataset,lattice}.md`
- `migration_safety_framework.md` — git tags, worktree testing, rollback L1-L5
- `adna_validate.py` — instance conformance validator per §5.5
- `frontmatter_schema.json` — JSON Schema for frontmatter validation
- Post-LSU fixes: D9 companion content validation, MCP module_type D5 N/A

---

## [v5.2] — 2026-03-19

### Added
- `CHANGELOG.md` — centralized version history (this file)
- Version policy documenting the two-track scheme (governance + standard)
- Migration prompt cross-links in changelog entries

### Changed
- `CLAUDE.md` version bump: `5.1` → `5.2`
- `STATE.md` updated with v5.2 reference and CHANGELOG in "What's Working"

### Migration
- [`migrate_v5.1_to_v5.2.md`](how/migrations/migrate_v5.1_to_v5.2.md)

---

## [v5.1] — 2026-03-18

### Changed
- Lattice types table expanded (7 values: added `infrastructure`, `context_set`, `skill`)
- Template count corrected (10 → 17)
- Standard file paths fixed (pointed to context library instead of nonexistent standalone files)

### Fixed
- CLAUDE.md token estimate corrected (`~650` → `~2500`)
- Object standards table references corrected

### Migration
- [`migrate_v5.0_to_v5.1.md`](how/migrations/migrate_v5.0_to_v5.1.md)

### Standard
- **v2.2** — Federation stub, vault extensions, campaign system, factual fixes

---

## [v5.0] — 2026-03-17

### Added
- OODA cascade (3-level: session, mission, campaign)
- AAR protocol (5-step)
- Escalation cascade (session → mission → campaign → STATE.md)
- Context recipes (6 domain-neutral, 3-tier budgets)
- Mission class discriminator (5 types: build, investigate, design, review, operate)
- 4 new templates (AAR, strategic compass, campaign CLAUDE.md, registry)
- 2 new skills (context quality audit, context graduation)

### Changed
- Framework port from lattice-labs vault to standalone aDNA repo
- 10 adna_core subtopics (was 8) — added ooda_cascade, ontology_workshop

---

## [v4.x and earlier] — 2026-02 to 2026-03

Pre-versioned history. Key milestones (not individually versioned):

- **Lattice publishing** — `latlab lattice publish/pull/compose` CLI workflow
- **Context library** — 4 topics, 23 subtopics, ~58K tokens
- **Object standards** — module, dataset, lattice type standards hardened
- **Canvas Standard v1.0.0** — Round-Trip Protocol v1.0 (YAML authoritative)
- **Type vocabulary** — 19 canonical I/O types (Decision 10)
- **FAIR metadata** — flat↔nested envelope interconversion (Decision 11)
- **Dataset schema** — multi-cloud `.dataset.yaml` with 7 providers (Decision 12)
- **Onboarding skill** — agent-driven interactive vault setup
- **14 example lattices** — business, research, creative, biotech domains
- **Obsidian config** — Tokyo Night theme, 10 CSS snippets, 14 plugins
