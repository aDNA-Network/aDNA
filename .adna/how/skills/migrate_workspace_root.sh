#!/usr/bin/env bash
# migrate_workspace_root.sh — transition an aDNA workspace root (default: ~/lattice -> ~/aDNA)
#
# Materialized 2026-06-10 (aDNALabs Session D) from the Operation Homecoming cutover that moved
# the reference node, folding the post-move gap register G1-G14 + the Session-C verified sweep
# machinery (aDNALabs.aDNA/what/migration/aar_operation_homecoming_postmove_20260609.md).
# Agentic companion: how/skills/skill_workspace_path_migration.md (drives the same transition
# inside an agent session and handles the harness re-key this script cannot).
#
# Safe by construction:
#   - prefix-anchored rewrites only: <abs-root>/, ~/<root>/, $HOME/<root>/, ${HOME}/<root>/
#     (+ the same four as bare refs before a terminator). The KEEP-set — dotted ~/.<root>,
#     <root>://, did:<root>:, dash/underscore/dot names like <root>-labs or <root>.bak — is
#     untouched by construction AND invariant-counted pre/post.
#   - reversible at every step via the symlink shim; rollback one-liners printed at the end.
#   - excludes: .adna/ (template clone — flips via upstream PR, never locally), _archive/ +
#     Archive.aDNA/ (archives keep history verbatim), .git internals, venvs, node_modules,
#     plus an optional KEEP-PROSE ledger (files that DOCUMENT the transform and must keep
#     old-root literals — list them in <root>/.migration_keep_prose, one relative path per line).
#
# The ONE step a script cannot safely do is the agent-harness realpath re-key (project/memory
# dirs keyed on the old absolute path) — guidance is printed; the companion skill automates it.
#
# Usage:
#   migrate_workspace_root.sh                  # interactive; detects root, prompts for target
#   NEW_ROOT=~/aDNA migrate_workspace_root.sh  # preset target
#   DRY_RUN=1 migrate_workspace_root.sh        # preflight report only — nothing moves or changes
#   ASSUME_YES=1 ...                           # skip confirmations (operator-supervised runs)
set -euo pipefail
export LC_ALL=C   # BSD sed/grep abort on non-UTF8 bytes without this (fleet hygiene rule)

# ---------- 0. detect OLD_ROOT = nearest ancestor containing .adna/ ----------
find_workspace_root() { local d="${1:-$PWD}"; while [ "$d" != "/" ]; do [ -d "$d/.adna" ] && { echo "$d"; return 0; }; d="$(dirname "$d")"; done; return 1; }
OLD_ROOT="$(find_workspace_root "$PWD")" || { echo "ERROR: no .adna/ found above $PWD — run from inside an aDNA workspace." >&2; exit 1; }
DEFAULT_NEW="$HOME/aDNA"
if [ -z "${NEW_ROOT:-}" ]; then
  if [ "${ASSUME_YES:-0}" = "1" ] || [ "${DRY_RUN:-0}" = "1" ]; then NEW_ROOT="$DEFAULT_NEW"
  else read -r -p "New workspace root [$DEFAULT_NEW]: " NEW_ROOT; NEW_ROOT="${NEW_ROOT:-$DEFAULT_NEW}"; fi
fi
case "$NEW_ROOT" in "~"*) NEW_ROOT="$HOME${NEW_ROOT#"~"}";; esac
OB="$(basename "$OLD_ROOT")"; NB="$(basename "$NEW_ROOT")"
export OLD_ROOT NEW_ROOT OB NB

EXCLUDE_DIRS=(.git .adna _archive Archive.aDNA .venv venv node_modules site-packages __pycache__)
GREP_EX=(); for d in "${EXCLUDE_DIRS[@]}"; do GREP_EX+=("--exclude-dir=$d"); done

confirm() { [ "${ASSUME_YES:-0}" = "1" ] && return 0; read -r -p "$1 [y/N] " a; [ "$a" = "y" ]; }
re_escape() { printf '%s' "$1" | sed 's/[][\.|$(){}?+*^]/\\&/g'; }   # literal string -> safe ERE
OA_RE="$(re_escape "$OLD_ROOT")"; OB_RE="$(re_escape "$OB")"
# the four prefix-anchored forms, as one ERE alternation (literal-escaped)
FORMS_RE="($OA_RE|~/$OB_RE|\\\$HOME/$OB_RE|\\\$\\{HOME\\}/$OB_RE)"
# a genuine ref = a form NOT followed by a name-continuation char (-,_,.,alnum) — so
# <root>-labs, <root>_backup, <root>.bak are never matched; <root>/ and bare <root>" are.
NONNAME="[^-_.[:alnum:]]"

# ---------- helpers (enumeration + proofs; precise — zero false positives on dash/dot names) ----------
list_hit_files() {  # text files (binaries skipped) containing a genuine old-root ref; dir symlinks not followed
  local root="$1"
  grep -rIlE "${GREP_EX[@]}" -e "${FORMS_RE}${NONNAME}" -e "${FORMS_RE}\$" -- "$root" 2>/dev/null \
    | filter_keep_prose "$root" || true
}
filter_keep_prose() {  # drop KEEP-PROSE-ledger paths (files that document the transform)
  local root="$1" kp="$1/.migration_keep_prose" tmp
  if [ -f "$kp" ]; then
    tmp="$(mktemp "${TMPDIR:-/tmp}/keep_prose.XXXXXX")"
    awk -v r="$root" 'NF && $0 !~ /^#/ {print r "/" $0}' "$kp" > "$tmp"
    grep -vxFf "$tmp" || true
    rm -f "$tmp"
  else
    cat
  fi
}
keepset_counts() {  # KEEP-set invariant tokens — these counts must be IDENTICAL pre/post sweep
  local root="$1" tok
  for tok in "/.$OB" "$OB://" "did:$OB:" "$OB-"; do
    printf '%s %s\n' "$tok" "$(grep -rIoF "${GREP_EX[@]}" -e "$tok" -- "$root" 2>/dev/null | wc -l | tr -d ' ')"
  done
}
list_repos_inner_first() {  # every git repo under root (incl. nested), deepest first — per-REPO discipline (G8)
  find "$1" \( -name .git \( -type d -o -type f \) \) \
    -not -path '*/_archive/*' -not -path '*/Archive.aDNA/*' -not -path '*/node_modules/*' 2>/dev/null \
    | sed 's|/\.git$||' | awk '{print gsub(/\//,"/"), $0}' | sort -rn | cut -d' ' -f2-
}

# ---------- 1. preflight report ----------
echo ">> OLD_ROOT=$OLD_ROOT  ->  NEW_ROOT=$NEW_ROOT"
[ "$OLD_ROOT" = "$NEW_ROOT" ] && { echo "Already at $NEW_ROOT."; exit 0; }
if [ -e "$NEW_ROOT" ] && [ "${DRY_RUN:-0}" != "1" ]; then echo "ERROR: $NEW_ROOT already exists." >&2; exit 1; fi

echo ">> Quiesce first: close Obsidian/IDEs on this tree; stop vault daemons (TaskForge bridge,"
echo "   federation receivers, launchd/systemd units that cwd into the workspace)."
echo ">> NOTE: dotted substrate (~/.$OB and friends) is OUTSIDE the workspace and does NOT move (G13)."

echo ">> Dirty git repos (pre-existing dirt gets an isolating checkpoint commit before any sweep, G10):"
DIRTY=0
while IFS= read -r repo; do
  if [ -n "$(git -C "$repo" status --porcelain 2>/dev/null)" ]; then echo "   dirty: $repo"; DIRTY=$((DIRTY+1)); fi
done < <(list_repos_inner_first "$OLD_ROOT")
[ "$DIRTY" -eq 0 ] && echo "   (none)"

echo ">> Python venvs under the root (pyvenv.cfg + shebangs hardcode the old abs path -> recreate after move):"
find "$OLD_ROOT" -maxdepth 5 -name pyvenv.cfg -not -path '*/_archive/*' 2>/dev/null | sed 's|/pyvenv.cfg$||; s|^|   |' || true

echo ">> Old-root reference surface (text files with a genuine ref; KEEP-PROSE-filtered):"
HITS="$(list_hit_files "$OLD_ROOT" | wc -l | tr -d ' ')"; echo "   $HITS files"
echo ">> KEEP-set invariant baseline (must be byte-identical post-sweep):"
keepset_counts "$OLD_ROOT" | sed 's/^/   /'

if [ "${DRY_RUN:-0}" = "1" ]; then echo ">> DRY_RUN — preflight only; nothing moved or edited. Re-run without DRY_RUN=1 to execute."; exit 0; fi
confirm ">> Proceed with the move?" || exit 0

# ---------- 2. backups (indices + best-effort snapshot; the bulk is moved, not copied) ----------
TS="$(date +%Y%m%d%H%M)"
BASEFILE="$(mktemp "${TMPDIR:-/tmp}/keepset_base.XXXXXX")"; keepset_counts "$OLD_ROOT" > "$BASEFILE"
( cd "$(dirname "$OLD_ROOT")" && \
  find "$OB" -maxdepth 2 \( -name CLAUDE.md -o -name STATE.md -o -name MANIFEST.md -o -name .migration_keep_prose \) -print0 2>/dev/null \
  | tar --null -czf "$HOME/aDNA_migration_backup_${OB}_${TS}.tgz" -T - ) 2>/dev/null || true
echo ">> index backup: ~/aDNA_migration_backup_${OB}_${TS}.tgz"
if [ "$(uname)" = "Darwin" ] && command -v tmutil >/dev/null 2>&1; then
  tmutil localsnapshot >/dev/null 2>&1 && echo ">> APFS local snapshot taken (rollback asset)" || true
fi

# ---------- 3. pre-sweep checkpoint commits (isolate pre-existing dirt from the sweep diff, G10) ----------
if [ "$DIRTY" -gt 0 ] && confirm ">> Checkpoint-commit the $DIRTY dirty repo(s) before sweeping?"; then
  while IFS= read -r repo; do
    if [ -n "$(git -C "$repo" status --porcelain 2>/dev/null)" ]; then
      git -C "$repo" add -A && git -C "$repo" commit --no-verify -q -m "pre-sweep checkpoint (workspace-root migration $OB -> $NB)" || true
      echo "   checkpointed: $repo"
    fi
  done < <(list_repos_inner_first "$OLD_ROOT")
fi

# ---------- 4. the move + back-compat shim (keeps every un-swept ref valid mid-transition) ----------
mv "$OLD_ROOT" "$NEW_ROOT"
ln -s "$NEW_ROOT" "$OLD_ROOT"
echo ">> moved; shim up: $OLD_ROOT -> $NEW_ROOT (everything still resolves; fully reversible)"

# ---------- 5. the sweep — perl with \Q..\E literal-quoting (portable; no BSD/GNU sed -i divergence) ----------
# Four prefix-anchored slash forms + the same four as bare refs before a terminator.
# The bare-form terminator class deliberately EXCLUDES name-continuation chars (- _ . alnum):
# <root>.bak / <root>_backup / <root>-labs are DIFFERENT objects and are never rewritten. It is
# also narrower than the grep NONNAME class — anything grep finds that perl declines to rewrite
# (e.g. exotic punctuation) surfaces in the residue proof for manual disposition. Conservative
# beats silent corruption.
PERL_PROG=$(cat <<'PERLEOF'
my $oa=$ENV{OLD_ROOT}; my $na=$ENV{NEW_ROOT}; my $ob=$ENV{OB}; my $nb=$ENV{NB};
my $t = qr{(?=["'`,;)\]\}><:\s]|$)};
s{\Q$oa\E/}{$na/}g;
s{~/\Q$ob\E/}{~/$nb/}g;
s{\$HOME/\Q$ob\E/}{\$HOME/$nb/}g;
s{\$\{HOME\}/\Q$ob\E/}{\${HOME}/$nb/}g;
s{\Q$oa\E$t}{$na}g;
s{~/\Q$ob\E$t}{~/$nb}g;
s{\$HOME/\Q$ob\E$t}{\$HOME/$nb}g;
s{\$\{HOME\}/\Q$ob\E$t}{\${HOME}/$nb}g;
PERLEOF
)
SWEPT=0
while IFS= read -r f; do
  if perl -pi -e "$PERL_PROG" -- "$f" 2>/dev/null; then SWEPT=$((SWEPT+1)); else echo "   WARN: sweep failed on $f" >&2; fi
done < <(list_hit_files "$NEW_ROOT")
echo ">> swept $SWEPT files (precise grep prefilter; untouched files keep their mtimes)"

# ---------- 6. remove auto-generated git hooks that embed old paths (re-install per repo) ----------
while IFS= read -r repo; do
  for hook in "$repo"/.git/hooks/*; do
    [ -f "$hook" ] || continue
    if grep -qF -e "$OLD_ROOT" -- "$hook" 2>/dev/null; then
      rm -f "$hook"; echo "   removed stale hook: $hook (re-run 'pre-commit install' there)"
    fi
  done
done < <(list_repos_inner_first "$NEW_ROOT")

# ---------- 7. proofs — dual residue + KEEP-set invariant (G12; value-checks, never prose-checks, G9) ----------
echo ">> RESIDUE PROOF (catch-all text grep, all extensions, excludes + KEEP-PROSE subtracted):"
RES="$(list_hit_files "$NEW_ROOT")"
if [ -n "$RES" ]; then
  echo "$RES" | sed 's/^/   RESIDUE: /'
  echo "   ^ disposition each (often exotic-punctuation contexts the conservative sweep declined);"
  echo "     rewrite by hand, or add transform-documentation files to .migration_keep_prose."
else
  echo "   ZERO residue outside excludes + KEEP-PROSE ledger."
fi
echo ">> KEEP-set invariant (pre vs post — ANY drift means a mis-refactor; investigate before continuing):"
POSTFILE="$(mktemp "${TMPDIR:-/tmp}/keepset_post.XXXXXX")"; keepset_counts "$NEW_ROOT" > "$POSTFILE"
if diff "$BASEFILE" "$POSTFILE" >/dev/null 2>&1; then
  echo "   INVARIANT HOLDS (byte-identical):"; sed 's/^/     /' "$POSTFILE"
else
  echo "   *** KEEP-SET DRIFT DETECTED ***"; diff "$BASEFILE" "$POSTFILE" | sed 's/^/     /' || true
  echo "   Roll back the sweep commits (or restore the snapshot) and investigate before proceeding."
fi

# ---------- 8. per-REPO sweep commits (inner/nested repos first, G8; tracked files only) ----------
if confirm ">> Commit the sweep per-repo now (git add -u; nested repos first)?"; then
  while IFS= read -r repo; do
    if [ -n "$(git -C "$repo" status --porcelain 2>/dev/null | grep -v '^??')" ]; then
      git -C "$repo" add -u && git -C "$repo" commit --no-verify -q -m "workspace-root migration sweep: $OB -> $NB (prefix-anchored, KEEP-set invariant verified)" || true
      echo "   committed: $repo"
    fi
  done < <(list_repos_inner_first "$NEW_ROOT")
fi

# ---------- 9. what remains (the parts a generic script must NOT guess at) ----------
cat <<EOF

>> MECHANICAL MIGRATION DONE — shim up at $OLD_ROOT. The tree works TODAY via the shim, which is
   exactly why unfinished anchors hide: "still resolves" is indistinguishable from "fixed" until
   the shim drops (Homecoming G-finding). Close these out, verifying each BY VALUE (G9), then drop it:

   1. AGENT-HARNESS RE-KEY (the one step a script can't safely do): your agent's project/memory/
      plan dirs are keyed on the old realpath (e.g. ~/.claude/projects/-...-$OB-*). Rename them
      -$OB- -> -$NB- (test on a COPY first; merge if a twin -$NB- key already exists), sweep memory
      + plan files, and RE-CHECK after the next session exit — a live harness can clobber the
      re-key when it closes (G5). The companion skill_workspace_path_migration automates this.
   2. ANCHORS BY VALUE — read each one and confirm the new path is REALLY there (never trust prose):
        - shell: ~/.zshrc + ~/.zshenv exports/sources (G3)
        - ~/.gitconfig include.path — git drops missing includes SILENTLY (G4)
        - launchd/systemd units: ~/Library/LaunchAgents/*.plist | systemd user units (G2)
        - editor/IDE state: ~/.spacemacs, VS Code workspace files, Obsidian obsidian.json vault
          registrations (every vault re-registered on the new path)
        - daemon venv SYMLINKS (e.g. ~/.bridge/venv -> old root) — repoint after recreating venvs (G1)
   3. RECREATE the venvs listed in preflight (python -m venv + reinstall) — shebangs/pyvenv.cfg
      hardcode absolute paths; a venv "working" through the shim is a false pass.
   4. RESTART every daemon to FRESH PIDs (launchctl kickstart -k / systemctl restart) and re-run
      health checks — processes started pre-move hold old inodes/cwd and false-pass (G11).
   5. VERIFY: re-run the residue grep; re-check the KEEP-set invariant; run your stack's battery
      (daemons healthy, topology/build checks, git status clean everywhere).
   6. DROP THE SHIM: rm "$OLD_ROOT" — then re-run the battery once more, shim-free.

   ROLLBACK LEDGER:
     - any time pre-drop (nuclear): rm "$OLD_ROOT" && mv "$NEW_ROOT" "$OLD_ROOT"  (+ reverse any re-key)
     - sweep only: per-repo git revert of the sweep commits (checkpoints isolated pre-existing dirt)
     - post-drop soft-landing: ln -s "$NEW_ROOT" "$OLD_ROOT"  (one-liner, instant)
     - backups: ~/aDNA_migration_backup_${OB}_${TS}.tgz + the APFS/Time Machine snapshot (if taken)
EOF
