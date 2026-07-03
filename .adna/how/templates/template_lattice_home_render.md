---
type: template
template_class: lattice_home_render
status: active
persona: rosetta   # vault-agnostic; instances re-persona per host vault
created: 2026-05-29
updated: 2026-06-11
last_edited_by: agent_stanley
provenance: "Lattice Home render template — canonical ASCII fence-pair with {{PLACEHOLDER}} markers; lift-and-parameterize per skill_lattice_home_install."
tags: [template, lattice_home, splash, ascii_render, fence_pair_extract, vault_agnostic, placeholder_spec, fallback_discipline, semantic_role_styling]
---

# Lattice Home Render Template (vault-agnostic)

> Drop-in substrate for the [[skill_lattice_home_install]] install recipe. Verbatim 5-block ASCII fence-pair below; bash `cmd_home` extracts the block via `awk '/^```$/{flag=!flag; next} flag'`, substitutes `{{PLACEHOLDER}}` markers via parameter expansion, prints to stdout. No runtime dependencies beyond bash + awk.

## Render (template — placeholders `{{LIKE_THIS}}`)

```
╭─ {{NODE_ID}} · {{OPERATOR}} ─────────────────────── {{VAULT_BADGE}} ─╮
│  {{BRANCH}}    {{UPSTREAM_STATUS}}    {{VAULT_STATUS}}
├──────────────────────────────────────────────────────────────────────┤
│  OPEN MISSIONS
{{OPEN_MISSIONS}}
│
│  RECENT
{{RECENT}}
│
│  CAPABILITY
│    providers: {{PROVIDERS}}    mcp: {{MCP_STATUS}}
│    theme tier: {{THEME_TIER}}    graphics: {{GRAPHICS_STATUS}}
├──────────────────────────────────────────────────────────────────────┤
│  SPC   g graph · m mission · t theme · p promote · b browser · ?
╰──────────────────────────────────────────────────────────────────────╯
```

The bottom line is an **idle command-tree-ready prompt** — ornamental at splash time; wired to actual keystrokes by a per-vault TUI (out of scope for the splash itself; CMux ships it at ex_05).

## Placeholder spec

| Placeholder | Source | Fallback when missing |
|---|---|---|
| `{{NODE_ID}}` | vault identity stub (`MANIFEST.md` / `node.adna.yaml` / equivalent) | `?` |
| `{{OPERATOR}}` | vault identity stub | `?` |
| `{{VAULT_BADGE}}` | vault-specific per [[skill_lattice_home_install]] step 2 parameter substitution | `🧬 lattice` (generic) |
| `{{BRANCH}}` | `git branch --show-current` (cwd-relative) | `(detached or no repo)` |
| `{{UPSTREAM_STATUS}}` | `git rev-list --left-right --count @{u}...HEAD` | `local-only` (no remote) |
| `{{VAULT_STATUS}}` | `git status --porcelain` count | `✓ vault clean` or `⚠ N uncommitted` |
| `{{OPEN_MISSIONS}}` | `grep -lE "^status: (planned\|in_progress\|active)$"` on vault's mission glob | `│    (none)` |
| `{{RECENT}}` | `grep -lE "^status: completed$"` on vault's mission glob; mtime-sort last 3 | `│    (none)` |
| `{{PROVIDERS}}` | `command -v <agent-cli>` per vault's agent stack | `claude-code ◌` |
| `{{MCP_STATUS}}` | cheap probe or literal placeholder | `(probe → TBD)` |
| `{{THEME_TIER}}` | cheap probe or literal placeholder | `(probe → TBD)` |
| `{{GRAPHICS_STATUS}}` | cheap probe or literal placeholder | `(probe → TBD)` |

## Glyph vocabulary

| Class | Glyphs |
|---|---|
| Mission state | `▶ open · ✓ closed · ⏸ deferred · ⚠ blocked · ⊘ rejected` |
| Run state | `● running · ◌ pending · ✓ done · ✗ failed · ◐ partial` |
| Vault badge | per host vault (e.g., `{{VAULT_BADGE}} <Vault> / {{persona}}`, `🌙 Home / Hestia`) |

**Font fallback**: if the operator's terminal lacks Unicode coverage, glyphs degrade to `[*]/[ ]/[X]`. Render emits the primary glyph by default.

## Styling — semantic roles only (zero hex literals)

Reference roles from the host vault's `what/inventory/inventory_palette.md` (or equivalent). The template contains **zero hex literals**.

| Role | Element |
|---|---|
| `bg_window` | base / box outer fill |
| `bg_raised` | hero block + section separators |
| `fg_primary` | text body |
| `fg_muted` | dates, log entries |
| `accent_primary` | nav headings (`OPEN MISSIONS` · `RECENT` · `CAPABILITY` · `SPC`) |
| `accent_amber` | `⚠` blocked / uncommitted |
| `accent_coral` | `✗` failed |
| `accent_needs_you` | reserved per vault's "single red light" invariant |

The role-to-hex resolution happens at the host vault's `conf.d/30-<vault>-env.zsh` (single source-of-record per vault).

## OPEN MISSIONS / RECENT row form

Each row inside `{{OPEN_MISSIONS}}` and `{{RECENT}}` blocks follows the indented form:

```
│    ▶ <mission_slug>          # OPEN MISSIONS (open glyph)
│    ✓ <mission_slug>    <date>   # RECENT (closed glyph + date)
```

Bash substitution produces the multi-line block (handled by `cmd_home` per the bash-substitution discipline; see [[skill_lattice_home_install]] step 2).

## Activation gate

Splash renders **only** when both gates pass (per [[pattern_lattice_home]] §Dual-gated activation):

1. `<VAULT_PREFIX>_LATTICE` env var unset or non-zero (default ON)
2. Graph-root walk resolves vault identity stub up CWD chain

Out-of-graph cwd + explicit env=0 both suppress (non-zero exit; silent stdout).

## Cross-references

- [[pattern_lattice_home]] — the pattern this template implements
- [[skill_lattice_home_install]] — the install skill that consumes this template + applies parameter substitution
