---
type: skill
skill_type: agent
category: infrastructure
created: 2026-05-29
updated: 2026-06-11
status: active
skill_version: 2   # v2 at campaign_lattice_home_pattern M3: vault-identity-class conditional + 5th substitution row + 3 NEW SEEDs from M2 close
last_edited_by: agent_stanley
token_estimate: ~2100
trigger: "User wants their aDNA vault to ship a terminal cold-start splash — a 5-block ASCII status surface rendered when an interactive shell opens inside the vault graph root. Also triggers when migrating from a bespoke shell startup script to the canonical [[pattern_lattice_home]] pipeline."
requirements:
  tools: [bash, awk, git, ln, sed]
  context: [target vault root, vault identity stub (MANIFEST.md or node.adna.yaml analog), how/campaigns/*/missions/ structure, how/configs/ directory writable]
  permissions: [write to vault how/configs/, optional symlink into operator user-scope (~/.zsh/conf.d/, ~/Library/Application Support/, or XDG ~/.config/)]
graduated_from: lattice-home pattern (>=3 canonical instances rubric)
tags: [skill, agent, infrastructure, lattice_home, splash, install, vault_portable, dual_gated, cmux_lift, parameterization_protocol, drift_audit, four_tier_pipeline]
---

# Skill: Lattice Home Install (vault-portable splash)

## Overview

Install the [[pattern_lattice_home]] terminal cold-start splash in any aDNA vault. Lifts a canonical `lattice`/`cmd_home` implementation (`how/configs/bin/lattice` `cmd_home()`), parameterizes it for the target vault, and wires the activation hook + idempotent install/uninstall scripts. Pure bash + awk; no runtime dependencies. Sub-second render; dual-gated (env var + graph-root walk).

The skill is **vault-agnostic** — it works for `aDNA.aDNA`, `Home.aDNA`, `Harness.aDNA`, forges, frameworks, org-vaults, or any future vault that inherits from the upstream `aDNA-Network/aDNA` base.

## When NOT to use

- The target is **not a vault** (no `MANIFEST.md` or `node.adna.yaml` analog at root → fails graph-root gate)
- The operator does **not want shell hook activation** (skip step 4 below; ship substrate only)
- The vault already has a bespoke splash → run drift-audit gate (step 6) first; migrate only if divergence > 20%
- The target shell is **fish / nu / non-interactive** → adapt step 4 to the target shell startup convention (see "Cross-shell adaptations" below)

## 6-step recipe

### Step 1 — Lift (read-only probe of a canonical instance)

Read the substrate files of a canonical instance (a vault that already ships `how/configs/bin/lattice` + its render template):

1. `bin/lattice` lines 165-290 (`cmd_home()` function — the splash render core)
2. `home/home_template.md` (fence-pair ASCII + 9 placeholders)
3. `conf.d/55-cmux-home.zsh` (activation hook + graph-root walk)
4. `bin/install.sh` (idempotent symlink installer; relevant rows: home template + conf.d hook)
5. `bin/uninstall.sh` (symmetric teardown)

Read-only — never modify the source instance. The lift IS the host vault's authoring, not a cross-vault edit. Substrate pin: capture the source instance's current `latticex.aDNA` HEAD SHA for drift-audit (step 6 below).

### Step 2 — Parameterize

Apply 4 parameter substitutions to the lifted substrate before writing into the target vault:

| Parameter | Source-instance value | Vault-agnostic placeholder | Example target value |
|---|---|---|---|
| Env var gate | `<SRC>_LATTICE` | `<VAULT_PREFIX>_LATTICE` | e.g. `HOME_LATTICE` (Home.aDNA) |
| Graph-root stub | `<src>/graph/node.adna.yaml` | `<IDENTITY_STUB>` | `MANIFEST.md`, or `Home.aDNA/MANIFEST.md` (Home.aDNA) |
| Mission grep glob | `how/campaigns/*/missions/*.md` | `<MISSION_GLOB>` | same (pattern stable across vaults) |
| Vault badge | `<src badge>` | `<VAULT_BADGE>` | `{{VAULT_BADGE}} <Vault> / {{persona}}`, `🌙 Home / Hestia` (Home.aDNA) |
| Identity probe *(v2)* | (read from `node.adna.yaml`) | `<IDENTITY_PROBE>` | `basename "$vault"` for NODE_ID + `git config user.name` for OPERATOR (aDNA-class) |

The parameterization protocol is the **single non-trivial step** in the skill. Use the [[template_lattice_home_render]] canonical template as the substitution starter — do NOT verbatim-copy the CMux template (drifts diverge if both are touched).

#### Step 2a — Vault-identity class (v2; added at campaign_lattice_home_pattern M3 from the M2 install findings)

Before substituting, classify the target vault by **how its root identity is encoded** — this determines whether the 4 substitutions above suffice or whether 3 additional adaptations apply:

| Identity class | Test | Substitutions |
|---|---|---|
| **unique-stub-class** | Vault carries a *unique* identity stub at a known path (e.g. `what/<code>/graph/node.adna.yaml`) that exists in this vault and no other (the graph-root gate keys on it) | The 4 base substitutions apply as-is; identity probe reads named fields from the stub |
| **shared-router-class** | Vault root identity is the *bare* `MANIFEST.md` — present in **every** aDNA vault (including `.adna/` + siblings) and carrying no `node_id`/`operator` fields | The 4 base substitutions **plus** the 3 adaptations below + the 5th `<IDENTITY_PROBE>` row |

For a **shared-router-class** vault, apply these 3 adaptations (surfaced when the host vault shares a workspace router):

1. **Per-vault PWD binding** — gate the graph-root walk to the binary's *own* vault root, not "any ancestor with a `MANIFEST.md`":
   ```bash
   case "$pwd_canon" in "$vault"|"$vault"/*) ;; *) return 1 ;; esac
   ```
   Without this, a vault whose `lattice` is on `PATH` (active mode) would render its badge over a *sibling* vault's mission data, because `MANIFEST.md` is universal. (Not needed for CMux-class — the unique stub is the binding.)

2. **PWD canonicalization via `realpath`** — substitute `realpath` for `cd "$PWD" && pwd -P`:
   ```bash
   pwd_canon="$(realpath "$PWD" 2>/dev/null || echo "$PWD")"
   ```
   On BSD/macOS, `cd "$PWD" && pwd -P` follows a lowercase symlink target (e.g. `adna.adna` → `aDNA.aDNA`) and masks the vault-root match. `realpath` canonicalizes both sides consistently.

3. **dirname + git-config identity probe** — derive identity without a stub:
   ```bash
   NODE_ID="$(basename "$vault")"
   OPERATOR="$(git -C "$vault" config user.name 2>/dev/null || echo '?')"
   ```
   `MANIFEST.md` carries no `node_id`/`operator` frontmatter, so do not parse it for identity; use the directory name + git config with a `?` fallback. This is the `<IDENTITY_PROBE>` 5th substitution row above.

> These 3 adaptations are the M2 NEW SEEDs. They are **conditional on shared-router-class** — a unique-stub-class vault with a unique identity stub does not need them. Record which class the target is in the vault's `STATE.md` drift notes so a future drift audit (step 6) compares like-for-like.

### Step 3 — Substrate

Create the directory tree in the target vault:

```
how/configs/
  bin/
    lattice            # main CLI; cmd_home subcommand (lifted + parameterized from the source instance)
    install.sh         # idempotent symlink installer
    uninstall.sh       # symmetric teardown
  home/
    home_template.md   # parameterized 5-block ASCII template (lifted from the source instance + per-vault badge)
  conf.d/
    55-lattice-home.zsh   # zsh interactive-shell hook; dual-gated
  runbooks/
    runbook_lattice_home_install.md   # smoke-verify + rollback procedure
```

5-6 NEW files per vault. No existing-file modifications (zero touches to `MANIFEST.md`, `CLAUDE.md`, `STATE.md`).

### Step 4 — Wire conf.d hook (operator-discretionary)

Two install modes:

- **Mode A (active)**: install symlinks both graph-local AND user-scope; `~/.zsh/conf.d/55-lattice-home.zsh` activation hook fires on every interactive zsh start; splash renders whenever cwd is inside vault graph root with `<VAULT_PREFIX>_LATTICE!=0`.
- **Mode B (passive)**: install symlinks graph-local ONLY; operator invokes `lattice home` manually; no shell hook installed.

Mode is selected at `install.sh` invocation: `install.sh --active` or `install.sh --passive` (default = passive per principle of least surprise).

### Step 5 — Smoke-verify (mandatory before commit)

10-row verify chain:

| # | Check | Expected |
|---|---|---|
| 1 | `bash -n bin/lattice && bash -n bin/install.sh && bash -n bin/uninstall.sh` | exit 0 |
| 2 | `bin/install.sh --dry-run` | symlink table populates; zero side-effects |
| 3 | `bin/install.sh --passive` (real install) | N symlinks created; idempotent re-run returns `ok` not `link` |
| 4 | `lattice home` from vault graph root | renders splash with substituted data |
| 5 | `<VAULT_PREFIX>_LATTICE=0 lattice home` | suppresses (rc=1; no output) |
| 6 | `cd /tmp && lattice home` | suppresses (rc=1; out-of-graph gate) |
| 7 | Live data check | OPEN MISSIONS row has at least one in_progress entry (if vault has active campaigns) OR `(none)` fallback |
| 8 | Capability probe | `claude-code ✓` or `claude-code ◌` (depending on `command -v claude`) |
| 9 | `bin/uninstall.sh --keep-runtime` | symlinks removed; substrate files preserved |
| 10 | Round-trip | `bin/install.sh --passive` after uninstall re-creates symlinks cleanly |

Failure on any row → fix before commit. Verify chain is the canonical exit gate for any install-class mission (per the source instance's graph-local install ADR (ADR-015 + ex_03+ex_04 precedent).

### Step 6 — Drift audit (SO-LH-1 from campaign_lattice_home_pattern)

Annually OR on operator request, run a `git diff` comparison:

```bash
diff <(awk '/^cmd_home\(\)/,/^}/' "$SRC_INSTANCE"/how/configs/bin/lattice) \
     <(awk '/^cmd_home\(\)/,/^}/' <target_vault>/how/configs/bin/lattice)
```

Divergence audit table:

| Divergence | Severity | Action |
|---|---|---|
| < 5% (only parameter substitutions) | OK | No action; pin SHA in skill frontmatter |
| 5-20% (template/glyph adjustments) | Acceptable | Document in vault's `STATE.md` "Pattern drift notes" |
| 20-40% (logic adjustments) | Flag | File operator decision: re-converge OR fork the pattern locally |
| > 40% (structural divergence) | Critical | Halt new-vault inheritance; re-evaluate whether the pattern still applies |

Drift audit prevents the splash from becoming a stale copy. The source-of-record instance carries forward improvements via this gate.

## Cross-shell adaptations

Step 4 conf.d hook is zsh-specific by default. Adapt the hook file + the install.sh user-scope symlink row for the target shell:

- **bash**: hook at `~/.bashrc.d/55-lattice-home.bash` (or append to `~/.bashrc` if no .bashrc.d convention)
- **fish**: hook at `~/.config/fish/conf.d/55-lattice-home.fish`
- **nu**: append to `~/.config/nushell/config.nu`
- **non-interactive only**: skip step 4; ship Mode B (manual `lattice home` invocation only)

## Examples

### Example 1 — worked install (shared-router-class vault)

Mission `mission_lhp_m2_adna_vault_install` (planned). Parameter substitutions:

- Env gate: `<VAULT_PREFIX>_LATTICE`
- Identity stub: `MANIFEST.md`
- Mission glob: `how/campaigns/*/missions/*.md`
- Badge: `{{VAULT_BADGE}} <Vault> / {{persona}}`

Mode: passive (operator invokes `lattice home` manually). Smoke chain 10/10 expected.

### Example 2 — Hypothetical Home.aDNA install

Parameter substitutions:

- Env gate: `HOME_LATTICE`
- Identity stub: `Home.aDNA/MANIFEST.md` (or `who/identity/identity_node.yaml`)
- Mission glob: `how/campaigns/*/missions/*.md`
- Badge: `🌙 Home / Hestia`

Operator runs install per vault adoption choice. Splash renders Hestia-flavored header on cmd zsh start at the Home.aDNA graph root.

## Anti-pattern

| What | Why it breaks |
|---|---|
| Copy the source substrate verbatim without parameterization | Drift accumulates across vaults; SO-LH-1 audit fails at first run |
| Skip step 5 verify chain | Install lands with broken bash syntax or non-idempotent symlinks; corrupts user-scope shell state |
| Force Mode A (active) without operator consent | Surprises operator with unwanted shell hook; principle of least surprise broken |
| Add features beyond the 5-block schema | Pattern drift; the [[pattern_lattice_home|pattern]] caps richness at 5 blocks |

## Cross-references

- [[pattern_lattice_home]] — the pattern this skill installs
- [[template_lattice_home_render]] — the canonical template for the parameterization in step 2
- [[idea_upstream_lattice_home_pattern]] — upstream-promotion candidate for the skill itself
- [[skill_campaign_sitrep_splash]] — sibling skill for lifecycle-variant splash render (Mission 3; LIVE)
- [[template_campaign_open_splash]] — campaign-open lifecycle template (Mission 3 D2)
- [[template_campaign_close_splash]] — campaign-close lifecycle template (Mission 3 D3)
- [[skill_upstream_contribution]] — parent workflow for filing upstream-promotion ideas
