---
type: artifact
artifact_type: upgrade_guide
campaign: campaign_adna_v2_infrastructure
mission: mission_adna_infra_planning_01
objective: 8
target_missions:
  - M08a  # ships this guide pre-flatten; copies it to .adna/how/docs/upgrade_v6_to_v7.md after flatten
  - M08b  # finalizes (dates the v7.0 tag entry; collects propagation receipts)
created: 2026-05-08
updated: 2026-05-11
status: finalized  # M01: status: complete (artifact authored). M08a Session 2 2026-05-11: status: finalized (cross-reference closure + dual-audience pass + §13 update; ready for M06 tag-date fill + M08b post-flatten copy).
finalized: 2026-05-11
last_edited_by: agent_stanley
tags: [artifact, mission_deliverable, m01, obj8, upgrade_guide, v6_to_v7, dual_audience, migration_runbook, m08a, m08b, airlock_amendment, naming_convention_amendment, finalized]
related_artifacts:
  - m01_obj0_ecosystem_matrix.md           # source: 19-vault inventory + per-change blast radius + external operators
  - m01_obj1_current_state.md              # source: current Governance v6.0 baseline
  - m01_obj2_migration_runbook.md          # source: M03 mechanics this guide narrates
  - m01_obj3_node_adna_design.md           # source: node.aDNA new-pattern description
  - m01_obj4_publish_naming_adr.md         # source: publish-skill family rename rationale
  - m01_obj5_github_minimalism_audit.md    # source: GitHub-side changes (deploy_manifest move + workflow URL fixes)
  - m01_obj6_semver_discipline_adr.md      # source: why v7.0 is Major Governance (Standard track unchanged)
  - m01_obj6_version_bump_checklist.md     # source: §1 pre-populated CHANGELOG v7.0 entry — this guide narrates it
  - m01_obj7_repo_review_audit_findings.md # source: §11 action summary; severity buckets feed "what changes" list
  - skill_lattice_publish_rewrite_spec.md  # source: publish-skill family spec
  - skill_git_remote_setup_spec.md         # source: NEW skill spec
  - pre_push_hook_spec.md                  # source: pre-push hook spec
related_decisions:
  - adr_004_campaign_home_stays_in_adna_adna.md
  - adr_005_three_way_vault_boundary.md
  - adr_006_github_repo_rename_to_adna.md  # repo rename narrative §3.5
  - adr_007_outer_adna_claude_md_disposition.md  # outer-wrapper retirement §3.4
  - adr_009_aDNA_naming_convention.md      # status: proposed; ratifies at M07 close — this guide's naming-going-forward §
  # ADR-008 (airlock stub, M03; this guide's optional airlock §) + ADR-010 (publish-naming, M05; this guide's publish-skill §) + ADR-011 (semver discipline, M06) — forward-references; resolve as their target missions ship.
---

# Upgrading from aDNA v6 to v7

> **Workspace-root note (2026-06)**: this guide predates the `~/aDNA/` workspace-root default and describes an already-installed `~/lattice/` workspace — its historical paths are intentionally unchanged. New installs default to `~/aDNA/`; legacy roots migrate via `how/skills/skill_workspace_path_migration.md` (agentic) or `how/skills/migrate_workspace_root.sh` (shell).

> **Deliverable 23 of M01** (per [[../mission_adna_infra_planning_01.md|mission_adna_infra_planning_01]] §Deliverables row 23 — re-numbered from "12" in original mission spec to avoid collision with Obj 7's deliverables 12a/12b authored at S2 S4). M08a destination after flatten: `.adna/how/docs/upgrade_v6_to_v7.md`. Pre-flatten draft path: this artifact. M08a publishes the same content to `adna-docs.vercel.app/learn/upgrade-v6-to-v7` so external operators can discover it without `.adna/` clone access.
>
> **Status**: finalized for publication (M08a Session 2, 2026-05-11). v7.0 tag date is left as `YYYY-MM-DD` until M06 fires the tag — M08b updates this guide with the actual date once `git tag v7.0` lands. Operation Rosetta Phase 8 authors the MDX page at `adna-docs.vercel.app/learn/upgrade-v6-to-v7`; this prose is publication-ready as-is (see [[m08a_upgrade_guide_publication_log.md|publication log]] §3 for MDX-readiness check).

---

## §0 What is changing

aDNA v7.0 is the first Major **Governance** bump since the standard's track-split (per [[m01_obj6_semver_discipline_adr.md|ADR-011]]). It tightens the repo structure, modernizes the publish workflow, and codifies a few patterns that have already emerged in practice. **The aDNA Standard track is not changing** — it stays at v2.2 (the canonical title at line 3 of `adna_standard.md`; a stale `v2.0` footer at line 1483 is corrected as a one-line audit fix). If you only consume the Standard, no action is required of you in v7.0.

If you operate an aDNA vault — whether you cloned the template last month, last year, or you're a partner organization running it under your own GitHub namespace — this guide is the migration path. It walks through what breaks, what's new, and what is purely additive. Two breaking changes need a migration step (the repo flatten and the publish-skill rewrite). Everything else is pull-based: you `git pull` your `.adna/` clone when you're ready, and the new patterns become available without forcing your hand.

The core principle of this version bump: **existing operators can stay on v6 indefinitely.** v7.0 is non-coercive. We landed it because the gains (cleaner clone path, real GitHub `git push` instead of an rsync workaround, opt-in observability + cross-vault coordination patterns) are worth one migration cycle. We are not deprecating v6 vaults that don't move. The successor campaign [[../../campaign_adna_v3_ecosystem_compliance/campaign_adna_v3_ecosystem_compliance.md|`campaign_adna_v3_ecosystem_compliance`]] handles per-vault v7.0 application across all 19 active ecosystem vaults; renames and deeper compliance work happen there at each operator's pace.

---

## §1 At-a-glance change summary

| Change | Class | Action required | Mission |
|---|---|---|---|
| Repo flatten — `adna/.adna/` → `.adna/` direct clone | **Breaking** | One-time, two-command migration | M03 |
| Publish-skill family rewrite — rsync → `git push` | **Breaking** | One-time per vault: `skill_git_remote_setup` + `skill_deploy` | M05 |
| `node.aDNA/` opt-in pattern | New (additive) | None unless you want it | M04 |
| `LatticeScope.aDNA` observability project | New (additive) | None unless you want it | M10 + successor sub-campaign |
| Governance `v7.0` tag | Pull-based | `git pull` your `.adna/` clone when ready | M06 |
| GitHub repo rename `Agentic-DNA` → `adna` | Pull-based | None (GitHub URL forwarding handles it); optional `git remote set-url` | M06 (with M03) |
| `deploy_manifest.yaml` → `.github/deploy_manifest.yaml` | Pull-based | None | M03 |
| Optional airlock-pattern adoption (per ADR-008) | New (opt-in) | None unless your vault does cross-vault work | (template stub in M03) |
| Naming convention `<name>.aDNA/` ↔ `<name>.aDNA.git` (per ADR-009) | Codification (no force) | None for existing vaults; new vaults conform | M07 close |

**Scope at a glance**: 2 breaking changes need migration steps. 5 non-breaking pull-based changes need nothing. 4 new patterns are opt-in.

---

## §2 Breaking change 1 — Repo flatten (M03)

### What changes

The `adna/` repo no longer contains a hidden `.adna/` directory inside itself. Instead, **the cloned repo IS the `.adna/` directory.** That collapses one level of nesting. Per [[adr_006_github_repo_rename_to_adna.md|ADR-006]], the GitHub repo is also renamed `Agentic-DNA` → `adna` to match — so the new clone command becomes a clean one-liner.

| Before (v6) | After (v7) |
|---|---|
| `~/lattice/adna/.adna/...` (template lives at `adna/.adna/`) | `~/lattice/.adna/...` (template lives directly at `.adna/`) |
| `~/lattice/.adna -> adna/.adna` (symlink at workspace root) | No symlink — `.adna/` is a real directory |
| `git clone https://github.com/LatticeProtocol/Agentic-DNA.git` (clones two levels) | `git clone https://github.com/LatticeProtocol/adna.git .adna` (single step) |

### Why

The two-level structure (`adna/.adna/`) had two roles fused together: an "outer wrapper" with a documentation-style README + LICENSE, and the actual `.adna/` template inside. This was a workaround from the era when GitHub couldn't host a repo whose name started with a dot. That constraint no longer applies, and the wrapper added friction every time someone explored the repo, set up onboarding, or wrote a path reference. Per [[adr_007_outer_adna_claude_md_disposition.md|ADR-007]], the outer wrapper retires; its useful content (the workspace-router CLAUDE.md template) becomes a regular template file (`template_workspace_claude.md`) inside the flattened repo.

### Migration — fresh clone (recommended)

The cleanest path is to re-clone fresh. Vault contents are not affected by the flatten — only the workspace root.

```bash
cd ~/lattice
rm -f .adna                    # remove the symlink
rm -rf adna                    # remove the legacy outer wrapper
git clone https://github.com/LatticeProtocol/adna.git .adna
ls -la .adna/                  # verify: how/, what/, who/, .git/, .github/ all visible at top level
```

### Migration — in-place (if you have local changes in `adna/`)

```bash
cd ~/lattice
rm .adna                       # remove the symlink
mv adna/.adna .adna_new        # extract the inner directory
mv adna/.git .adna_new/.git    # if .git lives at the outer level (older clones)
rm -rf adna                    # discard the outer wrapper
mv .adna_new .adna             # rename to the canonical location
cd .adna
git remote set-url origin https://github.com/LatticeProtocol/adna.git
git pull --ff-only             # sync to v7.0
```

The full mechanics — including rollback steps and 13 verification checks — are in [[m01_obj2_migration_runbook.md|m01_obj2_migration_runbook.md]] §3-§5.

### What stays the same

- Vault contents (`*.aDNA/` directories) are untouched. Vaults sit alongside `.adna/`, not inside it.
- Cross-vault tools (Obsidian, agents, scripts) that hard-code `adna/.adna/` paths break. Most don't — but find-and-replace `adna/.adna/` → `.adna/` if any of yours do.
- Existing tags (`v6.0`, etc.) continue to point at the pre-flatten history. Operators can stay on v6.0 by checking out the v6.0 tag.

---

## §3 Breaking change 2 — Publish-skill family rewrite (M05)

### What changes

The vault publish flow moves from a brittle `.publish-clone/` rsync workaround to **standard `git push origin main`**. The change introduces five publish-related skills (kept + new) plus a pre-push sanitization hook installed by an installer skill.

| Skill | v6 status | v7 status | What it does |
|---|---|---|---|
| `skill_lattice_publish.md` | Existed (latlab CLI registry publish) | **Kept** — light path-drift edits only; scope unchanged | Publishes `.lattice.yaml` objects to the registry via `latlab` CLI |
| `skill_vault_publish.md` | — | **NEW** — replaces the rsync workaround | Vault → GitHub via `git push`; first-use checks remote + hook |
| `skill_git_remote_setup.md` | — | **NEW** | First-time `git remote add origin` + `gh repo create`; ADR-009 naming-convention lint |
| `skill_deploy.md` | — | **NEW** | Idempotent installer for the pre-push sanitization hook (`.git/hooks/pre-push`) |
| `skill_publish_tarball.md` | — | **NEW (optional)** | Offline-shipping tarball flow for vaults that can't push to GitHub |

### Why

Spacemacs.aDNA filed a backlog idea (May 2026) noting that its `skill_publish_lattice` was rsync-ing the vault into a `.publish-clone/` directory and pushing from *there* — because the vault itself had no configured git origin. The fix was wrong to apply only at the consumer level: every vault's publish skill copy inherits the same shape, so 8 of 19 active vaults were one missing-remote away from the same workaround. Per [[m01_obj4_publish_naming_adr.md|ADR-010 recommendation]], the fix lands at the template level — and `skill_lattice_publish.md` keeps its scope (registry publish via latlab) while a new `skill_vault_publish.md` covers the GitHub-push flow.

The rewrite is co-signed in [[../../../../who/coordination/coord_2026_05_08_publish_rewrite.md|the Daedalus coord memo]] (Rosetta + Daedalus) — that exchange is **also the campaign's first cross-graph airlock-pattern exercise** and is the prototype this guide's per-vault coord memo template (deliverable 24, [[m01_obj8_per_vault_coord_memo_template.md|m01_obj8_per_vault_coord_memo_template.md]]) inherits from.

### Migration — per vault (one-time)

For each vault whose remote is **not** configured (7 vaults: Spacemacs, VideoForge, III, VAASLattice, zeta, RareHarness, strategic_interface_protocol — and 1 with a non-standard local-path remote: LPWhitepaper):

```bash
cd ~/lattice/<vault>.aDNA
# Run the new skill — sets up GitHub origin + creates the repo if needed
~/.adna/how/skills/skill_git_remote_setup.md   # invoked via your agent

# Then install the pre-push sanitization hook
~/.adna/how/skills/skill_deploy.md             # invoked via your agent

# Confirm
git remote -v                                  # should show origin → github.com/LatticeProtocol/<vault>.aDNA.git
ls .git/hooks/pre-push                         # should exist
```

For each vault that **already** has a proper origin (10 vaults: aDNA, science_stanley, SiteForge, wga, CanvasForge, context_commons, ComfyForge, SuperLeague + Wilhelm-Foundation × 2):

```bash
cd ~/lattice/<vault>.aDNA
# Just adopt the rewritten publish skill + install the hook
~/.adna/how/skills/skill_deploy.md             # idempotent; safe to re-run
# That's it. Use git push as you normally would; the new skill_vault_publish.md is your reference.
```

### Spacemacs.aDNA-specific cleanup (after the rewrite is in use)

Spacemacs has a `.publish-clone/` directory left over from the rsync workaround. Once one publish cycle confirms the new flow works, retire it:

```bash
cd ~/lattice/Spacemacs.aDNA
rm -rf .publish-clone .publish-clone.bak
# Mark Spacemacs.aDNA/how/standard/skills/skill_publish_lattice.md as status: deprecated
# (preserve the file per Standing Order #6; just flip the status field)
```

The full handshake (Daedalus's commitments at co-sign) is documented in [[../../../../who/coordination/coord_2026_05_08_publish_rewrite.md|the publish-rewrite coord memo]] §4.

### Pre-push hook — what it actually does

The pre-push hook (per [[pre_push_hook_spec.md|pre_push_hook_spec.md]] LAYER_CONTRACT §4 v0.1) runs 7 sanitization rules before each push:

| Rule | What it blocks |
|---|---|
| R1 | Path leakage (absolute `/Users/...`, `/home/...` paths in tracked files) |
| R2 | Secret patterns (API keys, JWT, OAuth tokens, AWS keys) |
| R3 | Filename patterns (`*.env`, `.npmrc`, `id_rsa`, `secrets.yaml`) |
| R4 | Large binaries (>10MB) without explicit allow-list |
| R5 | Frontmatter `confidential: true` |
| R6 | Frontmatter `draft: true` |
| R7 | Operator-defined deny list (per-vault `.publish-deny.txt`) |

The hook is bypassable with `--no-verify` (operator-discretionary; not recommended). Run `skill_deploy --self-test` to verify all 7 rules fire on a synthetic test vault.

---

## §4 New patterns (opt-in, additive)

### `node.aDNA/` — local node operational inventory

`node.aDNA/` is a new template-level pattern (per [[m01_obj3_node_adna_design.md|m01_obj3_node_adna_design.md]]) for operators who want a **per-machine inventory vault**: what software is installed, what compute resources exist (L1 GPU, etc.), what's running where, what credentials are configured, what was changed when. Persona: **Hestia** — the steady home that hosts the data.

Adoption is purely opt-in. Vaults that don't bootstrap a `node.aDNA/` are unaffected. The forward-reference from `node.aDNA/CLAUDE.md` to `aDNA.aDNA/how/campaigns/` (per [[adr_004_campaign_home_stays_in_adna_adna.md|ADR-004]]) is the only cross-vault hook — and it's a documentation pointer, not a runtime dependency.

To bootstrap (post-M04):

```bash
cd ~/lattice
~/.adna/how/skills/skill_node_adna_bootstrap.md   # invoked via your agent (M04 ships this skill)
```

The skill creates `node.aDNA/` at the workspace root with the full Hestia structure (`who/operators/`, `what/inventory/`, `what/identity/`, `how/sessions/`, etc.) and updates the workspace router (`~/lattice/CLAUDE.md`) with a Project Discovery row entry.

### `LatticeScope.aDNA/` — open-source observability platform

`LatticeScope.aDNA/` is a new Platform.aDNA project (per the same lineage as RareHarness) for **context/token observability across distributed agentic workflows**. Persona: **Prometheus** — gives operators visibility into context cost, foresight to predict budget exhaustion. The project pairs a governance vault (`LatticeScope.aDNA/`) with a sibling code repo (`latticescope/`) implementing a local SQLite collector + report templates + (later) a federation API.

LatticeScope is **seeded** in this campaign (M10 produces the planning campaign doc). Vault construction and runtime ship in a successor sub-campaign. No action is required of operators in v7.0; if you're interested in early adoption, watch [[../../../../STATE.md|STATE.md]] and the M10 mission for the campaign doc.

The architecture and 10-dim compliance pre-check are in mission spec §Obj 10 (lines 641–722). The token-measurement protocol that feeds LatticeScope's collector schema is **this campaign's Obj 9 deliverable** ([[m01_obj9_token_measurement_protocol.md|m01_obj9_token_measurement_protocol.md]]).

---

## §5 Non-breaking changes (just `git pull`)

### `v7.0` Governance tag

The v7.0 tag lands when M06 ships. Adoption is pull-based: next time you run `git -C .adna pull`, you receive the v7.0 entry in `CHANGELOG.md`. There is no push mechanism. You can stay on v6.0 indefinitely by simply not pulling. Per [[m01_obj6_semver_discipline_adr.md|ADR-011]], v7.0 is a Major **Governance** bump (not Major Standard) — the Standard track is unchanged at v2.2.

### GitHub repo rename `Agentic-DNA` → `adna`

GitHub preserves URL forwarding from old repo names indefinitely after rename, so existing clones keep working without intervention. New clones use the canonical short URL. To refresh a local clone's origin:

```bash
cd ~/lattice/.adna
git remote set-url origin https://github.com/LatticeProtocol/adna.git
```

This is cosmetic, not functional. Per [[adr_006_github_repo_rename_to_adna.md|ADR-006]].

### `deploy_manifest.yaml` → `.github/deploy_manifest.yaml`

The deploy manifest moves to `.github/` so it lives alongside other GitHub-relevant files (workflows, issue templates). `sync_includes:` paths are simplified post-flatten. If you don't run the deploy workflow yourself, this is invisible to you. If you do, the new path is the only thing that changes — no schema changes.

### Other minor moves (per [[m01_obj7_repo_review_audit_findings.md|Obj 7 audit findings]])

- `prepare_for_onboarding.sh` moves out of the template root (to `how/skills/l1_upgrade/` or renamed `prepare_for_l1_upgrade.sh`; operator-decided per audit §4 P-1). Discoverability fix.
- `skill_workspace_init.md` is formally retired (was already deprecated in v6.0). File is preserved per Standing Order #6.
- CI workflow caller-usage URLs update (`Agentic-DNA` → `adna` in 3 reusable workflows).
- A template-root `.gitignore` is created with the v7.0 exclusion set (`deploy/`, `what/local/`, `how/local/`, `who/operators/`, `dist/`, `.publish-clone/`, `.publish-clone.bak/`, `private/`, `*.dryrun.log`, `*.tar.gz`).

---

## §6 Validation runbook

After running the migration, verify your vault is clean. The recommended sequence is `skill_health_check` (M07 ships this skill, building on the audit pattern in [[m01_obj7_repo_review_audit_findings.md|m01_obj7_repo_review_audit_findings.md]]). If you can't wait for M07, the manual checks are:

| Check | Command | Expected |
|---|---|---|
| Workspace root has `.adna/` (not `adna/`) | `ls -la ~/lattice/.adna && ! test -d ~/lattice/adna` | `.adna/` exists; `adna/` does not |
| `.adna/` is a real directory (not a symlink) | `test -d ~/lattice/.adna -a ! -L ~/lattice/.adna` | true |
| `.adna/` clones from canonical repo | `cd ~/lattice/.adna && git remote -v` | `origin → github.com/LatticeProtocol/adna.git` |
| Template version is v7.0 | `grep '^version:' ~/lattice/.adna/CLAUDE.md` | `version: "7.0"` |
| CHANGELOG has v7.0 entry | `grep '## \[v7.0\]' ~/lattice/.adna/CHANGELOG.md` | match |
| Standard track is v2.2 (unchanged) | `head -3 ~/lattice/.adna/what/docs/adna_standard.md \| tail -1` | title says `v2.2` |
| For each vault: remote configured | `cd <vault> && git remote -v` | `origin → github.com/<org>/<vault>.git` |
| For each vault: pre-push hook installed | `ls <vault>/.git/hooks/pre-push` | exists |
| Vaults: `--self-test` passes on hook | `<vault>/.git/hooks/pre-push --self-test` | exit 0 |
| Try a `skill_project_fork` dry-run | `~/.adna/how/skills/skill_project_fork.md --dry-run` | succeeds; no path errors |

If any check fails, see [[m01_obj2_migration_runbook.md|m01_obj2_migration_runbook.md]] §6 (rollback procedures) or open an issue at `github.com/LatticeProtocol/adna`.

---

## §7 Optional: adopt the airlock pattern *(amendment 2026-05-08)*

v7.0 enables (but does not force) a `how/airlock/` directory in each vault. The airlock pattern is a **vault-agnostic cross-vault coordination surface** for cross-graph agent traffic — when an external agent enters your vault from a different context graph, the airlock is the entry-path index that orients them.

The pattern was matured in three vaults (`III.aDNA/how/airlock/AIRLOCK.md` is canonical; `VideoForge.aDNA/how/airlock/AIRLOCK.md` is the reference Forge airlock; `CanvasForge.aDNA` exercised it during the May 2026 Forge work). v7.0 ships a small stub at the template level (`/.adna/how/airlock/AIRLOCK.md`) per [[m01_obj7_repo_review_audit_findings.md|ADR-008]] (drafted by M03; ratified at M03 phase gate). `skill_project_fork.md` copies the stub into new projects automatically.

### When to adopt

- Your vault routinely receives cross-vault requests (handoffs from another vault's agents).
- Your vault is a Forge that produces artifacts other vaults consume.
- Your vault is a Platform with partner-org integrations.
- Your vault is part of a campaign with mirror coordination memos in another vault.

### When to skip

- Your vault is a single-operator project with no cross-vault traffic.
- You're not yet sure what the airlock is for. (You can adopt later — purely additive.)

### How to adopt (existing v7.0 vault)

```bash
cd ~/lattice/<vault>.aDNA
mkdir -p how/airlock
cp ~/.adna/how/airlock/AIRLOCK.md how/airlock/AIRLOCK.md
# Edit AIRLOCK.md — fill in your vault's persona, entry paths, version contract
```

The successor campaign [[../../campaign_adna_v3_ecosystem_compliance/campaign_adna_v3_ecosystem_compliance.md|`campaign_adna_v3_ecosystem_compliance`]]'s M05-EC mission walks per-vault airlock adoption across the ecosystem. Operators can adopt earlier on their own schedule.

---

## §8 Naming convention going forward *(amendment 2026-05-08)*

v7.0 codifies the **`<name>.aDNA/` directory ↔ `<name>.aDNA.git` GitHub repo** isomorphism per [[adr_009_aDNA_naming_convention.md|ADR-009]] (status: proposed; ratifies at M07 close). The convention:

1. **Directory name** is `<name>.aDNA/` where `<name>` is snake_case (lowercase letters, digits, underscores; no hyphens).
2. **GitHub repo name** matches the directory name exactly: `<name>.aDNA.git`.
3. **Display name** (titles, docs, marketing) is unconstrained — `Lattice Labs`, `World Genome Academy`, etc. are fine. The convention applies to filesystem and GitHub identifiers, not branding.
4. **Path-style local remotes** are permitted (per the `LPWhitepaper.aDNA` precedent — `origin-whitepaper` → local path).

### What this means for existing vaults

**Renames are operator-discretionary.** v7.0 does **not** force any existing vault to rename. Four classes of grandfathered exceptions are explicitly documented (per ADR-009 §3):

| Exception class | Examples | What's permitted |
|---|---|---|
| Hyphen-flat repos | `science-stanley-adna`, `wga-adna`, `context-commons-adna`, `LAStartupLattice` | Stay as-is; rename if/when operator chooses |
| No-remote vaults | Spacemacs, VideoForge, III, VAASLattice, zeta, RareHarness, strategic_interface_protocol | Apply the convention when first wiring the remote (M05) |
| Path-style local remote | LPWhitepaper | Stay as-is |
| Template repo | `Agentic-DNA` → `adna` | Already renamed per ADR-006 (the v7.0 reference case) |

### What this means for new vaults

**Forced.** `skill_project_fork.md` lints for naming-convention conformance and warns on non-conformant names. Operators can override with explicit acknowledgment, but the path of least resistance is the conforming form.

### What this means for partners (Wilhelm Foundation, TAPP, Super League)

**Operator-discretionary.** Per [[m01_obj0_ecosystem_matrix.md|m01_obj0_ecosystem_matrix.md]] §3, external operators inherit the convention as a recommendation, not a requirement. `Wilhelm-Foundation/rare-archive-vault` and `Wilhelm-Foundation/WilhelmAI` already conform; TAPP-side and Super League-side names are partner-decided. Per-vault application is the v3 successor's `M04-EC` mission scope.

---

## §9 What this campaign does *not* change

To be explicit about scope:

- **The aDNA Standard track is unchanged.** Standard stays at v2.2. The 14 base-ontology entity types, the triad (WHO/WHAT/HOW), the lattice/module/dataset object model, the FAIR metadata block — all the same. If you only consume the Standard, you are unaffected.
- **No vault content changes.** v7.0 does not modify any `*.aDNA/` vault's contents. The only directory affected by the flatten is `~/lattice/` (workspace root).
- **No forced renames.** ADR-009 codifies the naming convention but explicitly grandfathers existing non-conformant names.
- **No AGENTS.md migration.** AGENTS.md files in your vault stay exactly as they are.
- **Operation Rosetta site (`adna-docs.vercel.app`) is not affected** by v7.0 (other than gaining this upgrade guide as a new page). The site remains on Phases 0-7 of `campaign_rosetta`.

---

## §10 Where to get help

| Channel | Use it for |
|---|---|
| GitHub issues — `github.com/LatticeProtocol/adna` | Migration bugs, broken paths, audit-finding follow-ups |
| GitHub release notes — `github.com/LatticeProtocol/adna/releases/v7.0` | What landed, dated, with verification |
| Per-vault coord memos (delivered to your vault's `who/coordination/`) | Vault-specific migration steps for your operator. For the v7.0 rollout, look for `coord_2026_05_09_v7_<vault_snake>.md` — 17 memos rendered at M08a Session 1 (13 LP-internal `status: ready`; 4 partner-affiliated `status: draft` held by `delivery_held_until`). |
| `adna-docs.vercel.app/learn/upgrade-v6-to-v7` | This guide as a public web page |
| Mission file `mission_adna_infra_planning_01.md` | Original spec; the why behind every change |
| AAR for M01 (after S2 S6/S7) | Lessons from the planning phase; what was deferred |
| AAR for M03/M05/M06/M07/M08a/M08b | Mission-by-mission outcomes; gotchas; verifications |

For external operators (Wilhelm Foundation, TAPP, Super League): a per-partner coord memo is delivered alongside the v7.0 announcement covering organization-specific implications (Apache-2.0/CC-BY-4.0 licensing per WilhelmAI ADR 002, cross-federation attribution for Strategos/SIL, v0.1 → v1.0 trajectory for SuperLeague). See [[m01_obj8_per_vault_coord_memo_template.md|the per-vault coord memo template]] for the structure each memo follows. The four partner-affiliated drafts — [[../../../../who/coordination/coord_2026_05_09_v7_rarearchive.md|RareArchive]], [[../../../../who/coordination/coord_2026_05_09_v7_wilhelmai.md|WilhelmAI]], [[../../../../who/coordination/coord_2026_05_09_v7_superleague.md|SuperLeague]], and [[../../../../who/coordination/coord_2026_05_09_v7_strategic_interface_protocol.md|strategic_interface_protocol]] — remain `status: draft` with `delivery_held_until` markers until operator gates open (Wilhelm × 2 honor WilhelmAI ADR 010 publication-timing).

---

## §11 Self-reference + dual-audience (Standing Orders #7 + #8)

**Self-reference**: This guide IS a v6→v7 migration that was authored *while the host vault is still on v6*. The artifact path itself (`how/campaigns/campaign_adna_v2_infrastructure/missions/artifacts/m01_obj8_upgrade_guide_v6_to_v7.md`) reflects v6 conventions — `aDNA.aDNA/how/campaigns/` is canonical for the campaign-home pattern per [[adr_004_campaign_home_stays_in_adna_adna.md|ADR-004]] which itself was promoted to `accepted` at S2 S1 of this same mission. The guide ships its own destination path (`.adna/how/docs/upgrade_v6_to_v7.md`) — that path doesn't exist *yet* because M03 hasn't shipped. The artifact's own M08a step (copy this file into the post-flatten location) is part of the change this guide describes. The guide narrates the campaign that produces it.

**Dual-audience**:

- **Developer reads** §2 (migration commands), §3 (per-vault `skill_git_remote_setup` invocation), §6 (validation table). Direct, actionable, with file paths and exact commands.
- **Newcomer reads** §0 (the why), §1 (at-a-glance summary), §4 (what's new and optional), §9 (what doesn't change). Plain language, no required prior context, every concept defined or linked on first use.

Both reads land at the same conclusion: **v7.0 is non-coercive; you can stay on v6 indefinitely; the gains are worth one migration cycle when you're ready.**

---

## §12 Cross-references

| Reference | Used by | Direction |
|---|---|---|
| [[../mission_adna_infra_planning_01.md|mission_adna_infra_planning_01.md]] §Obj 8 + §Obj 11 | Source spec | spec → this doc |
| [[m01_obj0_ecosystem_matrix.md|m01_obj0_ecosystem_matrix.md]] §3 + §4 | External operators + per-change blast radius | upstream |
| [[m01_obj2_migration_runbook.md|m01_obj2_migration_runbook.md]] | M03 mechanics; rollback steps; verification harness | upstream |
| [[m01_obj3_node_adna_design.md|m01_obj3_node_adna_design.md]] | `node.aDNA/` design (§4 source) | upstream |
| [[m01_obj4_publish_naming_adr.md|m01_obj4_publish_naming_adr.md]] | Publish-skill family rationale (§3 source) | upstream |
| [[m01_obj5_github_minimalism_audit.md|m01_obj5_github_minimalism_audit.md]] | Non-breaking changes (§5 source) | upstream |
| [[m01_obj6_semver_discipline_adr.md|m01_obj6_semver_discipline_adr.md]] | Why v7.0 = Major Governance, Standard unchanged (§0) | upstream |
| [[m01_obj6_version_bump_checklist.md|m01_obj6_version_bump_checklist.md]] | §1 CHANGELOG v7.0 entry — this guide's narrative | upstream |
| [[m01_obj7_repo_review_audit_findings.md|m01_obj7_repo_review_audit_findings.md]] | §11 action summary feeds §5 minor moves | upstream |
| [[m01_obj8_per_vault_coord_memo_template.md|m01_obj8_per_vault_coord_memo_template.md]] | Per-vault coord memo structure | sibling |
| [[m01_obj9_token_measurement_protocol.md|m01_obj9_token_measurement_protocol.md]] | Feeds LatticeScope collector (§4 LatticeScope mention) | sibling |
| [[../../../../who/coordination/coord_2026_05_08_publish_rewrite.md|coord_2026_05_08_publish_rewrite.md]] | Daedalus handshake; airlock-pattern prototype | upstream |
| [[../../../../what/decisions/adr_004_campaign_home_stays_in_adna_adna.md|ADR-004]] | Campaign home rationale | upstream (`accepted`) |
| [[../../../../what/decisions/adr_005_three_way_vault_boundary.md|ADR-005]] | Vault category boundary | upstream (`accepted`) |
| [[../../../../what/decisions/adr_006_github_repo_rename_to_adna.md|ADR-006]] | Repo rename (§5 source) | upstream (proposed; M03 ratifies) |
| [[../../../../what/decisions/adr_007_outer_adna_claude_md_disposition.md|ADR-007]] | Outer-wrapper retirement (§2 source) | upstream (proposed; M03 ratifies) |
| [[../../../../what/decisions/adr_009_aDNA_naming_convention.md|ADR-009]] | Naming convention (§8 source) | upstream (proposed; M07 close ratifies) |
| ADR-008 (forward-reference) | Airlock template stub (§7) | M03 drafts; M03 phase gate ratifies |
| ADR-010 (forward-reference) | Publish-naming codification | M05 drafts; M05 close ratifies |
| ADR-011 (forward-reference) | Semver discipline | M06 drafts; v7.0 tag ratifies |
| [[../../campaign_adna_v3_ecosystem_compliance/campaign_adna_v3_ecosystem_compliance.md|campaign_adna_v3_ecosystem_compliance]] | Per-vault application; opens at v2 P3 | downstream (planned) |

---

## §13 Status

**Finalized for publication** (M08a Session 2, 2026-05-11). Cross-reference closure complete (§10 points operators at the rendered 2026-05-09 coord-memo filename pattern + names the 4 partner-affiliated drafts held by `delivery_held_until`). Dual-audience pass run per [[../../../../how/skills/skill_dual_audience_review.md|skill_dual_audience_review.md]] — verdict recorded in [[m08a_upgrade_guide_publication_log.md|m08a_upgrade_guide_publication_log.md]]. Frontmatter `status: complete → finalized`; `updated: 2026-05-11`; `finalized: 2026-05-11`.

**Still pending** (not finalized by Session 2 — owners named):
- The `YYYY-MM-DD` placeholder for the v7.0 tag throughout (§5 + this section's earlier `> Status` note + frontmatter implied tag context) — **M06 fills at tag time**.
- Copy to `.adna/how/docs/upgrade_v6_to_v7.md` post-flatten — **M08b owns** (after M03 lands the flatten).
- Publish as MDX at `adna-docs.vercel.app/learn/upgrade-v6-to-v7` — **Operation Rosetta Phase 8** owns (the publication log §3 documents the MDX-readiness check).
- Post-tag receipts and tag date update — **M08b owns**.

**Forward-references**: M06 (tag-date fill), M08b (post-flatten copy + tag-date + receipts), Operation Rosetta Phase 8 (MDX authoring) consume this guide. Findings already cited in [[aar_m01_planning.md|M01 AAR]] (S2 S6 — mission close). M08a Session 2 finalization edits logged in [[m08a_upgrade_guide_publication_log.md|publication log]].
