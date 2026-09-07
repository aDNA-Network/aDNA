#!/usr/bin/env bash
# pre-push-sanitize.sh — vault publish sanitization hook
#
# Source (template-shipped reference): .adna/how/standard/hooks/pre-push-sanitize.sh
# Installed by: skill_deploy (copies to .git/hooks/pre-push)
# Used by: skill_vault_publish (runs automatically on git push)
#
# LAYER_CONTRACT_VERSION=4.3.0
#
# ---------------------------------------------------------------------------
# WHAT THIS HOOK IS FOR
#
#   It runs before a push and refuses one that would publish something the vault's own
#   governance says must not be published. It is a DISCLOSURE gate, not a secret scanner —
#   `gitleaks` covers credentials; this covers material that is not a secret and is still
#   not publishable (local-only paths, draft or confidential documents, operator-named
#   strings).
#
#   Two verdict classes:
#     FAIL — the push is refused (R1, R2, R3, R5, R7, R8).
#     WARN — the push is refused unless an operator at a terminal confirms it (R4, R6).
#
# ---------------------------------------------------------------------------
# THE RULES
#
#   R1  Local/private directory leakage ............................. FAIL
#   R2  Secret-pattern matches (redacted when reported) .............. FAIL
#   R3  Filename patterns ............................................ FAIL
#   R4  Large binary files ........................................... WARN
#   R5  Frontmatter `confidential: true` / `private: true` ........... FAIL
#   R6  Frontmatter `status: draft` .................................. WARN
#   R7  Operator-defined deny list — PATHS ........................... FAIL
#   R8  Operator-defined deny list — CONTENT ......................... FAIL
#
#   R7 reads a path deny list; R8 reads a content deny list. Both are operator-authored:
#     .adna/sanitize_deny.txt   (template default)
#     sanitize_deny.txt         (vault override)
#
# ---------------------------------------------------------------------------
# TWO DESIGN RULES THIS FILE ENFORCES ON ITSELF
#
#   1. NO EXTENSION ALLOWLISTS. A disclosure rule must decide what to scan by asking whether
#      the bytes are readable, never by asking what the filename ends in. R5/R6 previously
#      opened with `[[ "$f" == *.md ]] || continue`, which meant a file marked
#      `confidential: true` in a .yaml, a .json, or an extensionless file was pushed
#      UNSCANNED by the one rule written to stop it. An extension allowlist in a publish gate
#      FAILS OPEN. Both R5/R6 and the self-test now use `sanitize_is_text`, the same
#      "scan unless PROVABLY binary" predicate R2 already used.
#
#   2. TEST THE ACT, NOT A PROPERTY INFERRED ABOUT IT. The WARN path's no-tty guard once read
#      `if [[ -t 0 ]] || [[ ! -e /dev/tty ]]`. At push time stdin is git's ref list — a pipe,
#      never a tty — so the first arm was always false; and on macOS /dev/tty is a device node
#      that exists whether or not a terminal is attached, so the second was too. The guard
#      could never fire, and its operator-facing message never once printed. It now tests
#      whether the tty can actually be OPENED: `if ! ( : < /dev/tty ) 2>/dev/null`.
#
# ---------------------------------------------------------------------------
# SCOPE OF R8, AND WHY IT IS NARROWER THAN IT LOOKS
#
#   R8 checks THE LINES A PUSH WOULD ADD, not the whole content of every file it touches.
#   Fix-forward is the governing doctrine for already-published content: the boundary binds
#   the next write, so the count stops growing rather than shrinking. A whole-file scan would
#   refuse a push over lines that doctrine has already ruled are not to be touched, leaving
#   only remedies that are forbidden (history rewrite) or that go stale (an exemption list).
#
#   Where there is no remote history to diff against — the first push of a branch — every
#   line is new, so the whole file is scanned. Scoping this way needs no exemption mechanism,
#   which is the point: there is nothing to go stale, and no file can be permanently excused
#   in a way that would also excuse a NEW occurrence inside it.
#
# ---------------------------------------------------------------------------
# SELF-TEST
#
#   `pre-push-sanitize.sh --self-test` runs every rule against the committed fixtures in
#   how/standard/hooks/test_fixtures/ — `clean/` must produce zero findings, `dirty/` must
#   produce at least one each. Run it after ANY change to this file.
#
#   ⚠ The self-test REIMPLEMENTS R1–R6 rather than calling them, so a rule fixed here must be
#     fixed there too, and a fixture set that does not exercise a case leaves that case
#     unguarded no matter how correct the rule is. The `*.md` defect above survived for the
#     whole life of 4.0.1 because `dirty/` contained only markdown files — the harness could
#     always have caught it and was never given a case that asked.
#
# ---------------------------------------------------------------------------

set -euo pipefail

# ============================================================================
# Configuration (shared by self-test mode and push-time scan)
# ============================================================================
SANITIZE_MAX_BYTES="${SANITIZE_MAX_BYTES:-10485760}"  # 10 MiB
DENY_FILE_TEMPLATE=".adna/sanitize_deny.txt"
DENY_FILE_VAULT="sanitize_deny.txt"
# R8 — content deny list (paths deliberately parallel to R7's, so operators learn one convention)
DENY_CONTENT_TEMPLATE=".adna/sanitize_deny_content.txt"
DENY_CONTENT_VAULT="sanitize_deny_content.txt"
NULL_SHA="0000000000000000000000000000000000000000"

# Secret-pattern regexes (referenced by R2 rule + self-test fixture scan).
# ANSI-C quoting ($'...') is used so \x27 / \x22 expand to ' and " — POSIX grep -E
# does NOT interpret \xNN as hex, so legacy '...' quoting would leave them as 8 literal
# chars and silently miss any quoted secret. Surfaced by M05 S2 self-test against fixtures.
declare -a secret_patterns=(
  $'([Aa][Pp][Ii]|[Ss][Ee][Cc][Rr][Ee][Tt]|[Aa][Cc][Cc][Ee][Ss][Ss])[_-]?([Kk][Ee][Yy]|[Tt][Oo][Kk][Ee][Nn])[[:space:]]*[:=][[:space:]]*[\x27\x22]?[A-Za-z0-9_\\-]{20,}'
  $'([Gg][Ii][Tt][Hh][Uu][Bb]|[Gg][Hh])[_-]?[Tt][Oo][Kk][Ee][Nn][[:space:]]*[:=][[:space:]]*[\x27\x22]?gh[psoru]_[A-Za-z0-9]{36,}'
  $'[Oo][Pp][Ee][Nn][Aa][Ii][_-]?[Aa][Pp][Ii][_-]?[Kk][Ee][Yy][[:space:]]*[:=][[:space:]]*[\x27\x22]?sk-[A-Za-z0-9]{40,}'
  $'[Aa][Nn][Tt][Hh][Rr][Oo][Pp][Ii][Cc][_-]?[Aa][Pp][Ii][_-]?[Kk][Ee][Yy][[:space:]]*[:=][[:space:]]*[\x27\x22]?sk-ant-[A-Za-z0-9_\\-]{40,}'
  $'-----BEGIN (RSA |EC |OPENSSH |DSA |)PRIVATE KEY-----'
  $'[Aa][Ww][Ss]_[Ss][Ee][Cc][Rr][Ee][Tt]_[Aa][Cc][Cc][Ee][Ss][Ss]_[Kk][Ee][Yy][[:space:]]*[:=][[:space:]]*[\x27\x22]?[A-Za-z0-9/+=]{40}'
  $'[Ll][Aa][Tt][Ll][Aa][Bb][_-]?[Tt][Oo][Kk][Ee][Nn][[:space:]]*[:=][[:space:]]*[\x27\x22]?[A-Za-z0-9_\\-]{20,}'
)

# ---------------------------------------------------------------------------
# Shared predicates (4.3.0) — ONE definition, used by BOTH the push-time rules and the
# --self-test reimplementation.
#
# ⛔ Defined here, not inlined twice, on purpose. The defect these replace existed in two
#   places (the real R5/R6 loop and the self-test's re-implementation of it), which is how a
#   self-test can agree with itself and disagree with the rule. Two copies of a predicate are
#   two predicates.

# TEXT? — R2's predicate, adopted verbatim by R5/R6 at 4.3.0: scan unless PROVABLY binary.
# ⚠ The direction matters and is the whole finding: an allowlist ("only these extensions")
#   fails OPEN on everything it forgot; a denylist against a MEASURED property (`file --mime`
#   says binary) fails CLOSED on anything it cannot classify.
sanitize_is_text() {
  ! file --mime "$1" 2>/dev/null | grep -q 'charset=binary'
}

# Emit the YAML frontmatter block, or nothing.
#
# ⚠ ANCHORED (a filed finding). "Frontmatter" means the fence that OPENS the document; the previous
#   scan treated a `---` ANYWHERE as an opening fence, which the `*.md` test had been masking.
#   Removing that test without anchoring this would have traded a fail-OPEN for a
#   false-POSITIVE — measured: 1 phantom (a vendored minified .js with a stray `---`) against
#   8 genuine (the .base/*.template files every new vault forks from).
#
# ⛔⛔ a filed finding — THE FIRST ANCHOR WAS STRICT `NR==1` AND IT SILENTLY NARROWED COVERAGE.
#   Four governance documents carry a REFRAME BANNER as a leading blockquote before the fence
#   — a documented governance convention, a DOCUMENTED convention, not an accident:
#     what/doctrine/{charter_lighthouse,migration_doctrine}_seed.md
#     what/{architecture/architecture_forge,requirements/requirements_forge}_seed.md
#   ⇒ Under `NR==1` their frontmatter is invisible and R5/R6 stop reading them. Caught by
#   measuring the tree AFTER the change and comparing populations, not by reading the code.
#   ⛩ THAT IS THE SAME CLASS AS THE DEFECT THIS FILE IS BEING REPAIRED FOR — a predicate that
#   quietly stops examining things — introduced WHILE repairing it, in the same act, and it
#   would have shipped as a fix. It is recorded rather than smoothed because the seven
#   instances behind that discipline are all this shape.
#
#   ⇒ The preamble skipped is EXACTLY the convention: blank lines and blockquote (`>`) lines.
#   Anything else before the fence ends the scan. Measured over the whole tracked tree: this
#   recovers those 4 files and NOTHING ELSE, and the phantom .js stays excluded.
# ⛔ `|| true` IS LOAD-BEARING, AND a filed finding IS WHY. awk exits 2 when it cannot open its
#   input, and under `set -euo pipefail` the assignment `fm=$(sanitize_frontmatter "$f")`
#   propagated that straight out of the hook: exit 2, NO OUTPUT, before any Decision block.
#   Fail-safe in direction — a non-zero status blocks the push — but it is a CRASH, not a
#   VERDICT, and the two are different facts (the same distinction R8's header draws about
#   `r8_patterns=()`). An operator would have seen a bare `2` and no finding.
#   ⭐ The `*.md` test had been MASKING this: unreadable non-.md files never reached the awk.
#   Removing an allowlist exposes everything the allowlist was accidentally protecting, which
#   is an argument for removing it, not against.
#   Unreadability is reported as a FINDING by the caller, never swallowed here.
sanitize_frontmatter() {
  [[ -f "$1" && -r "$1" ]] || return 0
  awk 'BEGIN{o=0}
       !o && (/^[[:space:]]*$/ || /^>/) {next}      # documented banner/blank preamble
       !o && $0=="---" {o=1; next}                  # the opening fence
       !o {exit}                                    # anything else ⇒ no frontmatter
       o && /^---$/ {exit}                          # the closing fence
       o {print}' "$1" 2>/dev/null || true
}

# ============================================================================
# Self-test mode (called by skill_deploy post-install)
# ============================================================================
if [[ "${1:-}" == "--self-test" ]]; then
  # Resolve fixtures location: post-M03-flatten canonical first, fallback to legacy .adna/ layout
  fixtures_dir="how/standard/hooks/test_fixtures"
  [[ -d "$fixtures_dir" ]] || fixtures_dir=".adna/how/standard/hooks/test_fixtures"

  if [[ ! -d "$fixtures_dir" ]]; then
    echo "WARN: self-test skipped — fixtures not found at how/standard/hooks/test_fixtures"
    echo "WARN: (fallback .adna/how/standard/hooks/test_fixtures also missing)"
    echo "WARN: install fixtures or run a real publish to verify."
    exit 0
  fi

  echo "INFO: self-test fixtures dir: $fixtures_dir"

  # Per-file rule scan — emits one line per finding (R<N>: <rel> (<detail>)) to stdout
  check_fixture_file() {
    local f="$1"      # absolute or repo-relative path to fixture file
    local rel="$2"    # vault-relative path the fixture simulates (e.g., what/local/notes.md)

    # R1: private path leakage
    case "$rel" in
      what/local/*|how/local/*|who/operators/*|deploy/*|.publish-clone/*|.publish-clone.bak/*|private/*)
        echo "R1: $rel (private path leakage)"
        ;;
    esac

    # R3: filename patterns
    case "$(basename "$rel")" in
      .env|.env.*|id_rsa|id_ed25519|id_ecdsa|id_dsa)
        echo "R3: $rel (filename pattern: credential file)"
        ;;
      secrets|secrets.yaml|secrets.yml|secrets.json|secrets.toml|secrets.ini)
        echo "R3: $rel (filename pattern: secrets file)"
        ;;
    esac

    [[ -f "$f" ]] || return 0

    # R2: secret-pattern match (skip binary)
    if sanitize_is_text "$f"; then
      for pattern in "${secret_patterns[@]}"; do
        if grep -qE "$pattern" "$f" 2>/dev/null; then
          # Honor pragma: allowlist secret
          if ! grep -E "$pattern" "$f" 2>/dev/null | grep -qE 'pragma:[[:space:]]*allowlist[[:space:]]+secret'; then
            echo "R2: $rel (secret pattern match)"
            break
          fi
        fi
      done
    fi

    # R4: large file
    local size
    size=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f" 2>/dev/null || echo 0)
    if [[ "$size" -gt "$SANITIZE_MAX_BYTES" ]]; then
      echo "R4: $rel ($size bytes > $SANITIZE_MAX_BYTES)"
    fi

    # R5/R6: frontmatter checks — ANY text file, not just *.md (4.3.0; a filed finding).
    # ⚠ This branch is a REIMPLEMENTATION of the push-time rule below, not the rule itself
    #   (a filed finding's class). It is kept in step by sharing the predicates, and its green is
    #   SELF_TEST_ONLY — never cited as coverage for R5/R6.
    if sanitize_is_text "$f"; then
      local fm
      fm=$(sanitize_frontmatter "$f")
      if [[ -n "$fm" ]]; then
        if echo "$fm" | grep -qE '^(confidential|private)[[:space:]]*:[[:space:]]*true'; then
          echo "R5: $rel (frontmatter confidential|private: true)"
        fi
        if echo "$fm" | grep -qE '^status[[:space:]]*:[[:space:]]*draft'; then
          echo "R6: $rel (frontmatter status: draft)"
        fi
      fi
    fi
  }

  exit_code=0
  echo ""
  echo "=== Clean fixtures (expect zero findings each) ==="
  if [[ -d "$fixtures_dir/clean" ]]; then
    while IFS= read -r f; do
      rel="${f#$fixtures_dir/clean/}"
      findings=$(check_fixture_file "$f" "$rel" || true)
      if [[ -z "$findings" ]]; then
        echo "  ✓ $rel"
      else
        echo "  ❌ $rel — UNEXPECTED findings:"
        echo "$findings" | sed 's/^/      /'
        exit_code=1
      fi
    done < <(find "$fixtures_dir/clean" -type f 2>/dev/null | sort)
  else
    echo "  (no clean/ subdir)"
  fi

  echo ""
  echo "=== Dirty fixtures (expect ≥1 finding each, matching the named rule) ==="
  if [[ -d "$fixtures_dir/dirty" ]]; then
    while IFS= read -r f; do
      rel="${f#$fixtures_dir/dirty/}"
      findings=$(check_fixture_file "$f" "$rel" || true)
      if [[ -n "$findings" ]]; then
        echo "  ✓ $rel — caught:"
        echo "$findings" | sed 's/^/      /'
      else
        echo "  ❌ $rel — NO findings (rule miss; expected at least one R1-R7 finding)"
        exit_code=1
      fi
    done < <(find "$fixtures_dir/dirty" -type f 2>/dev/null | sort)
  else
    echo "  (no dirty/ subdir)"
  fi

  echo ""
  if [[ $exit_code -eq 0 ]]; then
    echo "✓ self-test PASSED (clean fixtures all CLEAN; dirty fixtures all flagged)"
  else
    echo "❌ self-test FAILED — see findings above"
  fi
  exit $exit_code
fi

# ============================================================================
# Read git push refs from stdin
# ============================================================================
declare -a ranges
while read -r local_ref local_sha remote_ref remote_sha; do
  # Skip delete operations
  [[ "$local_sha" == "$NULL_SHA" ]] && continue
  # New branch (no remote history) — compare against empty tree
  if [[ "$remote_sha" == "$NULL_SHA" ]]; then
    ranges+=("$local_sha")
  else
    ranges+=("$remote_sha..$local_sha")
  fi
done

# Empty push (nothing to check)
[[ ${#ranges[@]} -eq 0 ]] && exit 0

# ============================================================================
# Compute set of files about to be pushed
# ============================================================================
declare -a pushed_files
mapfile -t pushed_files < <(
  for range in "${ranges[@]}"; do
    if [[ "$range" == *..* ]]; then
      git diff --name-only "$range" 2>/dev/null
    else
      # New branch — list all files in the pushed commit
      git ls-tree -r --name-only "$range" 2>/dev/null
    fi
  done | sort -u
)

[[ ${#pushed_files[@]} -eq 0 ]] && exit 0

# ============================================================================
# Findings accumulators
# ============================================================================
fail_findings=()
warn_findings=()

# ============================================================================
# R1: Local/private directory leakage (FAIL)
# ============================================================================
for f in "${pushed_files[@]}"; do
  case "$f" in
    what/local/*|how/local/*|who/operators/*|deploy/*|\
    .publish-clone/*|.publish-clone.bak/*|private/*)
      fail_findings+=("R1: $f (private path leakage)")
      ;;
  esac
done

# ============================================================================
# R2: Secret-pattern matches (FAIL; redact when reporting)
# ============================================================================
# secret_patterns array is defined in the shared Configuration block above
# (referenced by both self-test mode and push-time scan).

r2_examined=0
for f in "${pushed_files[@]}"; do
  # Skip non-existing files (deleted in the push)
  [[ -f "$f" ]] || continue
  # Skip binary files
  sanitize_is_text "$f" || continue
  r2_examined=$((r2_examined + 1))
  # Skip if line contains pragma: allowlist secret
  for pattern in "${secret_patterns[@]}"; do
    while IFS=: read -r lineno content; do
      [[ -z "$lineno" ]] && continue
      # Honor pragma: allowlist secret comment
      if echo "$content" | grep -qE 'pragma:[[:space:]]*allowlist[[:space:]]+secret'; then
        continue
      fi
      # Redact: show first 4 chars of any captured group + "***"
      redacted=$(echo "$content" | grep -oE '[A-Za-z0-9_\-]{20,}' | head -1 | cut -c1-4)
      fail_findings+=("R2: ${f}:${lineno} (secret pattern match; redacted='${redacted}***')")
    done < <(grep -nE "$pattern" "$f" 2>/dev/null || true)
  done
done

# ============================================================================
# R3: Filename patterns (FAIL)
# ============================================================================
for f in "${pushed_files[@]}"; do
  case "$(basename "$f")" in
    .env|.env.*|id_rsa|id_ed25519|id_ecdsa|id_dsa)
      fail_findings+=("R3: $f (filename pattern: credential file)")
      ;;
    secrets|secrets.yaml|secrets.yml|secrets.json|secrets.toml|secrets.ini)
      fail_findings+=("R3: $f (filename pattern: secrets file)")
      ;;
  esac
  # .pem files: check content for private-key headers (handled by R2 too; cheap front-line check)
  if [[ "$f" == *.pem ]] && [[ -f "$f" ]]; then
    if grep -q "BEGIN .*PRIVATE KEY" "$f" 2>/dev/null; then
      fail_findings+=("R3: $f (filename .pem with private-key content)")
    fi
  fi
  # .netrc / .npmrc with auth tokens
  if [[ "$(basename "$f")" == ".netrc" || "$(basename "$f")" == ".npmrc" ]] && [[ -f "$f" ]]; then
    if grep -qE "(_authToken|password)[[:space:]]*=" "$f" 2>/dev/null; then
      fail_findings+=("R3: $f (filename .netrc/.npmrc with auth tokens)")
    fi
  fi
done

# ============================================================================
# R4: Large binary files (WARN)
# ============================================================================
r4_examined=0
for f in "${pushed_files[@]}"; do
  [[ -f "$f" ]] || continue
  r4_examined=$((r4_examined + 1))
  size=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f" 2>/dev/null || echo 0)
  if [[ "$size" -gt "$SANITIZE_MAX_BYTES" ]]; then
    warn_findings+=("R4: $f (size $size bytes > threshold $SANITIZE_MAX_BYTES)")
  fi
done

# ============================================================================
# R5/R6: Frontmatter confidential|private (FAIL) / status: draft (WARN)
# ============================================================================
# ⛔ 4.3.0 — THE `*.md` TEST IS GONE. It read `[[ "$f" == *.md ]] || continue`, which made a
#   DISCLOSURE rule an EXTENSION ALLOWLIST: a node marked `confidential: true` in a .yaml, a
#   .json, or an extensionless file was pushed unscanned by the one rule meant to stop it.
#   That fails OPEN. See the 4.3.0 block in this file's header for the measurement and for
#   a filed finding, the anchoring defect the extension test had been masking. Reported inbound.
r5r6_examined=0
for f in "${pushed_files[@]}"; do
  [[ -f "$f" ]] || continue
  # ⛔ FAIL-CLOSED on unreadable (a filed finding). A file the disclosure rule CANNOT READ is not a
  #   file that passed it — unmeasured is INDETERMINATE, never a green. It is
  #   reported as a finding here rather than crashing the hook two lines later.
  if [[ ! -r "$f" ]]; then
    fail_findings+=("R5/R6: $f (unreadable — cannot be checked for confidential|private; fail-closed)")
    continue
  fi
  sanitize_is_text "$f" || continue
  r5r6_examined=$((r5r6_examined + 1))
  # Extract the frontmatter block (fence must OPEN the file — a filed finding)
  fm=$(sanitize_frontmatter "$f")
  [[ -z "$fm" ]] && continue
  # R5: confidential|private = true
  if echo "$fm" | grep -qE '^(confidential|private)[[:space:]]*:[[:space:]]*true'; then
    fail_findings+=("R5: $f (frontmatter flagged confidential|private: true)")
  fi
  # R6: status: draft
  if echo "$fm" | grep -qE '^status[[:space:]]*:[[:space:]]*draft'; then
    warn_findings+=("R6: $f (frontmatter status: draft)")
  fi
done

# ============================================================================
# R7: Operator-defined deny list (FAIL)
# ============================================================================
r7_rules=0
for deny_file in "$DENY_FILE_TEMPLATE" "$DENY_FILE_VAULT"; do
  [[ -f "$deny_file" ]] || continue
  while IFS= read -r line; do
    # Skip blank lines and comments
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
    r7_rules=$((r7_rules + 1))
    if [[ "$line" =~ ^re: ]]; then
      pattern="${line#re:}"
      for f in "${pushed_files[@]}"; do
        if [[ "$f" =~ $pattern ]]; then
          fail_findings+=("R7: $f (deny regex: $pattern)")
        fi
      done
    else
      for f in "${pushed_files[@]}"; do
        if [[ "$f" == "$line"* ]]; then
          fail_findings+=("R7: $f (deny prefix: $line)")
        fi
      done
    fi
  done < "$deny_file"
done

# ============================================================================
# R8: Operator-defined CONTENT deny list (FAIL)
# ============================================================================
# Why this exists (the git-ops standard):
#   R1 and R7 are PATH rules — R7 tests "$f" in both its `re:` and prefix branches,
#   and R1 matches a fixed set of directory prefixes. R2 is a content rule but its
#   patterns are hardcoded to secrets. So the gate could express "do not publish these
#   FILES" and "do not publish these SECRETS", and could not express "do not publish
#   this STRING".
#
#   That gap is not hypothetical. A graph can publish an operator-named string — an
#   internal address, a hostname, a topology detail — many times across many files
#   spanning who/, what/ and how/. No path rule covers that set, because the rule is
#   about a STRING, not a location, and a secret scanner correctly passes it: an
#   address and a port are not secrets. R8 is the rule that can express it.
#
# Format (sanitize_deny_content.txt): one ERE per line; blanks and #-comments skipped.
# Escape hatch: the same `pragma: allowlist` marker R2 honours, on the matching line.
# Reporting: matches are REDACTED — the whole point is a hook that does not itself
# reproduce the string it is refusing to publish.
#
# FAIL-CLOSED (an undeterminable reading is a BLOCK, never a pass):
#   an unreadable file, or a pattern grep rejects, BLOCKS. A deny-list that silently
#   skips the pattern it cannot compile is worse than no deny-list, because it reports
#   green.
# ⛔ SCOPE — R8 CHECKS THE LINES THIS PUSH WOULD ADD, NOT THE WHOLE FILE (4.2.0).
#   Fix-forward doctrine rules already-published content FIX-FORWARD and explicitly does NOT
#   rewrite it. A whole-file scan therefore EXCEEDED the doctrine it enforces: it refused a
#   push over lines the doctrine had already ruled are not to be touched. Measured on a real
#   vault at the change: dozens of matching lines across dozens of files, every one already
#   published, and the pending commits added ZERO new ones. Whole-file: refused. Scoped to
#   added lines: green, with no exemption of any kind.
#
#   ⭐ This is the whole reason no allowlist file exists. The three alternatives considered
#   and DECLINED at the 2026-09-02 gate:
#     (a) a file-scoped allowlist naming those 23 files — a NEW occurrence added to any of
#         them (STATE.md above all) would then pass. A gate that reports green on the case
#         it exists to catch is the defect this vault has filed under three names.
#     (b) 70 per-line `pragma: allowlist` markers — edits published prose to satisfy a gate,
#         and the markers themselves become published content.
#     (c) ⛔ weaken the pattern until it passes. NEVER. Still refused, still named.
#   Scoping to D4's own rule needs none of them: the historical body is out of scope BY
#   DOCTRINE rather than by exemption, and there is no allowlist to go stale.
#
#   ⚠ NO REMOTE HISTORY (first push of a branch, remote_sha = NULL_SHA) ⇒ WHOLE FILE. Every
#   line is genuinely new there. That is the correct reading, not a weakened fallback.
#   ⚠ A RENAME presents as all-new and BLOCKS. Fail-safe, stated here rather than discovered.

# Emit "lineno:content" (grep -n's format) for the text this push would ADD in <file>.
r8_subject() {
  local f="$1" range
  for range in "${ranges[@]}"; do
    if [[ "$range" == *..* ]]; then
      # New-file line numbers come from the hunk header's +start; --unified=0 emits no context.
      git diff --unified=0 "$range" -- "$f" 2>/dev/null | awk '
        /^\+\+\+/ { next }
        /^@@/     { match($0, /\+[0-9]+/); n = substr($0, RSTART+1, RLENGTH-1) + 0; next }
        /^\+/     { print n ":" substr($0, 2); n++ }
      ' || true
    else
      grep -n '' "$f" 2>/dev/null || true
    fi
  done | sort -u
}

# Patterns are read and VALIDATED first, so a malformed one fails closed exactly once
# rather than once per file, and the per-file subject is computed only once.
# ⛔ `r8_patterns=()` NOT `declare -a r8_patterns`. Under `set -u` a declared-but-unassigned
#   array is UNSET, and `${#r8_patterns[@]}` then aborts the hook. Caught by the range arms:
#   the hook crashed before reaching its Decision block and exited 1 on EVERY push, including
#   clean ones and every R7 arm. ⚠ Fail-safe in direction, but it is a CRASH, not a verdict —
#   an exit code that means "the gate died" is not the same fact as "the gate refused", and
#   only the harness could tell them apart.
r8_patterns=()
for deny_file in "$DENY_CONTENT_TEMPLATE" "$DENY_CONTENT_VAULT"; do
  [[ -e "$deny_file" ]] || continue
  if [[ ! -r "$deny_file" ]]; then
    fail_findings+=("R8: $deny_file exists but is not readable (fail-closed)")
    continue
  fi
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
    # Validate the pattern BEFORE trusting a zero-match result from it. grep exits
    # 0 = matched, 1 = no match (pattern is fine), 2 = bad pattern. Only 2 is a defect,
    # and it is indistinguishable from 1 unless the code looks. `|| rc=$?` is required:
    # under `set -e` a bare grep returning 1 would kill the hook.
    rc=0
    printf '' | grep -E "$line" >/dev/null 2>&1 || rc=$?
    if [[ $rc -gt 1 ]]; then
      fail_findings+=("R8: malformed pattern in $deny_file (fail-closed): ${line:0:24}…")
      continue
    fi
    r8_patterns+=("$line")
  done < "$deny_file"
done

r8_examined=0
if [[ ${#r8_patterns[@]} -gt 0 ]]; then
  for f in "${pushed_files[@]}"; do
    [[ -f "$f" ]] || continue
    sanitize_is_text "$f" || continue
    subject="$(r8_subject "$f")"
    [[ -z "$subject" ]] && continue
    r8_examined=$((r8_examined + 1))

    # ⛔ Split "lineno:content" into a CONTENT-ONLY stream plus a parallel line-number map.
    #   The deny patterns begin with `(^|[^0-9])`. Splicing that after a "lineno:" prefix
    #   would silently change what the `^` branch can match — the pattern must see exactly
    #   the bytes of the source line and nothing else, as the whole-file scan gave it.
    declare -a subj_no=() subj_txt=()
    while IFS= read -r sl; do
      [[ -z "$sl" ]] && continue
      subj_no+=("${sl%%:*}")
      subj_txt+=("${sl#*:}")
    done <<< "$subject"
    [[ ${#subj_txt[@]} -eq 0 ]] && continue

    for pattern in "${r8_patterns[@]}"; do
      while IFS= read -r idx; do
        [[ -z "$idx" ]] && continue
        content="${subj_txt[$((idx-1))]}"
        if echo "$content" | grep -qE 'pragma:[[:space:]]*allowlist'; then
          continue
        fi
        fail_findings+=("R8: ${f}:${subj_no[$((idx-1))]} (content deny match in ADDED line; redacted)")
      done < <(printf '%s\n' "${subj_txt[@]}" | grep -nE "$pattern" 2>/dev/null | cut -d: -f1 || true)
    done
  done
fi

# ============================================================================
# Decision
# ============================================================================
if [[ ${#fail_findings[@]} -gt 0 ]]; then
  echo ""
  echo "❌ pre-push-sanitize: FAIL — push aborted"
  printf '  %s\n' "${fail_findings[@]}"
  echo ""
  echo "Remediate the findings above (or add 'pragma: allowlist secret' on false-positive secret lines), recommit, then retry."
  echo "Emergency bypass (use sparingly): git push --no-verify origin <branch>"
  exit 1
fi

if [[ ${#warn_findings[@]} -gt 0 ]]; then
  echo ""
  echo "⚠ pre-push-sanitize: WARN — borderline findings"
  printf '  %s\n' "${warn_findings[@]}"
  echo ""
  # Read prompt from tty (stdin is git's ref list).
  #
  # ⛔ a filed finding (2026-09-02) — THE PREVIOUS GUARD COULD NOT FIRE, AND WAS RIGHT BY ACCIDENT.
  #   It read:  if [[ -t 0 ]] || [[ ! -e /dev/tty ]]; then <treat WARN as FAIL>
  #     · `-t 0` tests STDIN, which at push time is git's ref list — a pipe, never a tty.
  #       The comment one line above says so. The arm is false in normal operation, always.
  #     · `! -e /dev/tty` — on macOS /dev/tty is a device node that EXISTS whether or not a
  #       controlling terminal is attached. The arm is false there too.
  #   ⇒ Both false ⇒ fall through to `read < /dev/tty` ⇒ "Device not configured" ⇒ non-zero
  #     under `set -e` ⇒ exit 1. The RIGHT VERDICT FOR THE WRONG REASON, so nothing ever
  #     revealed it, and the operator-facing message below HAD NEVER ONCE PRINTED.
  #
  #   ⛩ Found on the FIRST REAL DRIVE of this hook, minutes after it was installed for the
  #   first time (a filed finding: R1–R8 had never run on a real push). A guard that exists, reads
  #   correctly, and cannot fire is this campaign's signature class — a filed finding (R7 shipped and
  #   never ran), a filed finding (a control enforced where it is vacuous), a filed finding (fail-uninformative).
  #
  #   The test is now the ACT, not a property inferred about it: try to open the terminal.
  #   ⚠ Tested in a SUBSHELL. `exec 3</dev/tty 2>/dev/null` in this shell is wrong twice:
  #   on SUCCESS the `2>/dev/null` is an exec redirection and would silence the hook's own
  #   stderr for the rest of the run; on FAILURE the shell emits its diagnostic before the
  #   redirection applies, so the raw "Device not configured" still leaks past the message
  #   written to replace it. A subshell scopes both.
  if ! ( : < /dev/tty ) 2>/dev/null; then
    echo "INFO: no controlling terminal; treating WARN as FAIL (no operator to confirm)."
    echo "      Resolve the warning, or push from an interactive shell to confirm."
    exit 1
  fi
  read -p "Continue with push? [y/N] " yn < /dev/tty
  if [[ "$yn" =~ ^[Yy]$ ]]; then
    echo "INFO: operator confirmed; proceeding with push."
    exit 0
  else
    echo "INFO: push aborted by operator."
    exit 1
  fi
fi

# ============================================================================
# Coverage report (4.3.0) — the git-ops standard
# ============================================================================
# ⛔ THIS LINE USED TO LIE, AND SPECIFICALLY. It read:
#       clean (${#pushed_files[@]} files checked)
#   — the count of EVERY file in the push, printed as though it were every rule's coverage,
#   while R2/R5/R6/R8 each read a strict subset. An operator reading `clean (86 files checked)`
#   was told something precise and untrue about R5.
#
#   ⛩ A8 §5: *a green from an instrument is a statement ABOUT THE POPULATION IT EXAMINED, and
#   that population is reported WITH THE VERDICT, always.* A verdict whose population is
#   unstated may not be cited as coverage — so this hook could not previously be cited as R5
#   coverage at all, in any of the three vaults running it.
#
#   ⚠ Per-rule, not one number, because the populations genuinely differ and averaging them
#   would be a new way of saying the same false thing. Rules that examine every pushed path
#   (R1, R3) say so explicitly rather than being omitted — an unstated population is the
#   defect, and that does not stop being true when the number happens to be the total.
echo "✓ pre-push-sanitize: clean — ${#pushed_files[@]} files in push. Coverage by rule:"
echo "    R1 paths        ${#pushed_files[@]}/${#pushed_files[@]} (every pushed path)"
echo "    R2 secrets      ${r2_examined}/${#pushed_files[@]} (present, non-binary)"
echo "    R3 filenames    ${#pushed_files[@]}/${#pushed_files[@]} (every pushed path)"
echo "    R4 large files  ${r4_examined}/${#pushed_files[@]} (present)"
echo "    R5/R6 frontmtr  ${r5r6_examined}/${#pushed_files[@]} (present, non-binary)"
echo "    R7 deny paths   ${#pushed_files[@]}/${#pushed_files[@]} against ${r7_rules} rule(s)"
echo "    R8 deny content ${r8_examined}/${#pushed_files[@]} (present, non-binary, with added lines) against ${#r8_patterns[@]} pattern(s)"
exit 0
