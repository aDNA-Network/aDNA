---
type: context
subtype: seed_terminal_intent
created: 2026-05-31
updated: 2026-06-08
status: active
last_edited_by: agent_seshat
tags: [obsidian, seed, terminal, obsidian-terminal, profiles, materialized_m05]
---

# Seed intent — `terminal` (polyipseity obsidian-terminal) CLI profiles

> **MATERIALIZED (M05, 2026-06-08).** A concrete reference now ships alongside this note: **`data.json`** (this dir) — the verified v3.25.0 config (7 platform defaults + the 5 universal aDNA profiles), authored on the `Home.aDNA` pilot and operator-verified ("Claude Code launches `claude`"). This note stays the **version-agnostic intent of record** (archive-never-delete): the `data.json` schema is plugin-version-specific, so per-vault authoring still **merges these profiles into the target's own installed default** rather than blindly copying the reference. Executable authoring tool: **[`what/code/author_terminal_profiles.py`](../../../../code/author_terminal_profiles.py)** (version-guarded, idempotent; `--with-home` adds the Home-only profile).

> **Why a note, not just a `data.json`:** the obsidian-terminal `data.json` profile schema is plugin-version-specific. To avoid shipping a config a future plugin major rejects, profiles are **authored against the installed plugin version** at the operator-restart gate (read the plugin's default `data.json` after install → merge these profiles in). The shipped `data.json` is the v3.25.0 reference; `author_terminal_profiles.py` refuses on a terminal **major** skew unless `--force`.

Replaces the retired `termy` preset-CLI experience. Each profile = an integrated terminal that launches an agent CLI in the vault root, zsh login shell, follow-theme on.

## Profiles — UNIVERSAL (5; shipped in the seed `data.json`)

| id | Name | Launches | args (verified v3.25.0) | Notes |
|---|---|---|---|---|
| `claude-code` | Claude Code | `claude` | `["-l","-i","-c","claude"]` | primary |
| `codex` | Codex CLI | `codex` | `["-l","-i","-c","codex"]` | |
| `opencode` | OpenCode | `opencode` | `["-l","-i","-c","opencode"]` | |
| `gemini` | Gemini CLI | `gemini` | `["-l","-i","-c","gemini"]` | |
| `shell` | Shell | (login zsh) | `["--login"]` | plain terminal, no CLI |

## Profile — NODE-LOCAL (Home only; NOT in the universal seed)

| id | Name | Launches | args | Notes |
|---|---|---|---|---|
| `claude-home` | Claude · Home (Hestia) | `claude` in `~/aDNA/Home.aDNA` w/ work-session prompt | `["-l","-i","-c","cd ~/aDNA/Home.aDNA && claude 'Please read the Claude.md and get ready for a work session.'"]` | "jump to node governance" from any vault — claude loads `Home.aDNA/CLAUDE.md` (Hestia) + the workspace router, then auto-orients. **Operator decision 2026-06-08: Home-only**, authored via `author_terminal_profiles.py --with-home`; the `~/aDNA/Home.aDNA` path is a node-convention (not portable to the universal seed). |

## Settings (intent)

- `executable`: `/bin/zsh` (darwin); login shell so `~/.zshrc` exports (incl. brokered env-vars) are present.
- `args`: launch the CLI via `-l -i -c "<cli>"` (login+interactive so `~/.zprofile`+`~/.zshrc` load); `shell` = `--login` (no command).
- `cwd`: the plugin sets cwd at spawn (= active vault root); **there is no per-profile cwd field** — a fixed directory (e.g. claude-home → Home.aDNA) is baked into the command via `cd … &&`.
- `defaultProfile`: left `null` (a new terminal opens the platform integrated default = plain login shell; the named profiles are picked via command/ribbon).
- Appearance: **follow Obsidian theme**. Surfaces: command palette + ribbon; not status bar (mirrors the prior termy posture).

## Materialization (skill_obsidian_seed + author_terminal_profiles.py)

1. `reseed_runner.py` installs the obsidian-terminal **binary** (copy-from-donor / release) and flags the installed version (`terminal_version` in its report); it does **not** write the terminal `data.json`.
2. At the operator-restart gate (Obsidian closed on the target), run **`author_terminal_profiles.py <target>/.obsidian/plugins/terminal/data.json [--with-home] [--write]`** — it reads the plugin's default `data.json`, MERGES the 5 universal profiles (idempotent; `--with-home` adds `claude-home`), refuses on a terminal major-version skew unless `--force`, JSON-validates, writes.
3. Operator restart → confirm profiles appear + a profile launches `claude`.
