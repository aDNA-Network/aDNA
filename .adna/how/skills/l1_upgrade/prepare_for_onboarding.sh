#!/usr/bin/env bash
#
# prepare_for_onboarding.sh — Prepare this machine for L1 compute upgrade
#
# Run this BEFORE your admin provisions the node. It checks prerequisites,
# fixes common macOS gotchas, and prints a summary for your admin.
#
# Does NOT install latlab, JupyterHub, or any Lattice infrastructure.
# That is done by the admin via setup_l1_remote.sh (push model) or by
# a future self-service installer.
#
# Usage:
#   ./prepare_for_onboarding.sh           Run all checks
#   ./prepare_for_onboarding.sh --dry-run Show what would be checked
#   ./prepare_for_onboarding.sh --help    Show this help
#
# What it does:
#   1. Checks macOS version and architecture
#   2. Bootstraps .zshenv with Homebrew PATH (if missing)
#   3. Checks Python >= 3.12
#   4. Checks npm availability
#   5. Checks disk space >= 10GB free
#   6. Checks ports 8000 and 8100 availability
#   7. Fixes npm cache ownership (if root-owned)
#   8. Prints summary block for admin
#
# What it does NOT do:
#   - Install any software (except .zshenv PATH fix)
#   - Write credentials or secrets
#   - Start services or daemons
#   - Require sudo or root access
#

set -euo pipefail

# ── Colors ───────────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ── Logging ──────────────────────────────────────────────────────────────

pass_count=0
warn_count=0
fail_count=0

log_pass() { echo -e "${GREEN}[PASS]${NC} $*"; pass_count=$((pass_count + 1)); }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; warn_count=$((warn_count + 1)); }
log_fail() { echo -e "${RED}[FAIL]${NC} $*"; fail_count=$((fail_count + 1)); }
log_info() { echo -e "${BLUE}[INFO]${NC} $*"; }

# ── Argument Parsing ─────────────────────────────────────────────────────

DRY_RUN=false
case "${1:-}" in
    --dry-run) DRY_RUN=true ;;
    --help|-h)
        head -35 "$0" | tail -34
        exit 0
        ;;
esac

echo ""
echo "  aDNA L1 Pre-Flight Check"
echo "  ========================"
echo ""

if $DRY_RUN; then
    echo -e "${YELLOW}DRY RUN — showing checks without executing${NC}"
    echo ""
    echo "  1. Check macOS version and architecture"
    echo "  2. Bootstrap .zshenv with Homebrew PATH"
    echo "  3. Check Python >= 3.12"
    echo "  4. Check npm availability"
    echo "  5. Check disk space >= 10GB free"
    echo "  6. Check ports 8000, 8100 availability"
    echo "  7. Fix npm cache ownership if root-owned"
    echo "  8. Print admin summary block"
    echo ""
    exit 0
fi

# ── Check 1: macOS version and architecture ──────────────────────────────

os_type=$(uname -s)
if [[ "$os_type" != "Darwin" ]]; then
    log_warn "Not macOS (detected: ${os_type}). This script is designed for macOS but checks may still apply."
else
    arch=$(uname -m)
    macos_ver=$(sw_vers -productVersion 2>/dev/null || echo "unknown")
    if [[ "$arch" == "arm64" ]]; then
        log_pass "macOS ${macos_ver} (${arch})"
    else
        log_warn "macOS ${macos_ver} (${arch}) — arm64 (Apple Silicon) recommended"
    fi
fi

# ── Check 2: .zshenv Homebrew PATH ──────────────────────────────────────

if [[ -f /opt/homebrew/bin/brew ]]; then
    if [[ -f "$HOME/.zshenv" ]] && grep -q 'brew shellenv' "$HOME/.zshenv"; then
        log_pass ".zshenv has Homebrew PATH"
    else
        log_info "Creating .zshenv with Homebrew PATH..."
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> "$HOME/.zshenv"
        log_pass ".zshenv bootstrapped with Homebrew PATH"
    fi
    # Source it for this session
    eval "$(/opt/homebrew/bin/brew shellenv)"
elif command -v brew &>/dev/null; then
    log_pass "Homebrew available (non-standard location)"
else
    log_warn "Homebrew not found. Install from https://brew.sh"
fi

# ── Check 3: Python >= 3.12 ─────────────────────────────────────────────

MIN_PYTHON="3.12"
py_found=false
for cmd in python3.13 python3.12 python3; do
    if command -v "$cmd" &>/dev/null; then
        py_ver=$("$cmd" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "0.0")
        py_ok=$("$cmd" -c "
import sys
min_parts = '${MIN_PYTHON}'.split('.')
cur_parts = '${py_ver}'.split('.')
print('yes' if (int(cur_parts[0]), int(cur_parts[1])) >= (int(min_parts[0]), int(min_parts[1])) else 'no')
" 2>/dev/null || echo "no")
        if [[ "$py_ok" == "yes" ]]; then
            log_pass "Python ${py_ver} (>= ${MIN_PYTHON}) at $(command -v "$cmd")"
            py_found=true
            break
        fi
    fi
done
if ! $py_found; then
    log_fail "Python >= ${MIN_PYTHON} not found. Install: brew install python@3.13"
fi

# ── Check 4: npm ────────────────────────────────────────────────────────

if command -v npm &>/dev/null; then
    npm_ver=$(npm --version 2>/dev/null || echo "unknown")
    log_pass "npm ${npm_ver}"
else
    log_fail "npm not found. Install: brew install node"
fi

# ── Check 5: Disk space ────────────────────────────────────────────────

MIN_DISK_GB=10
if [[ "$os_type" == "Darwin" ]]; then
    disk_free_gb=$(df -g / | tail -1 | awk '{print $4}')
else
    disk_free_gb=$(df -BG / | tail -1 | awk '{print $4}' | tr -d 'G')
fi
if [[ "$disk_free_gb" -ge "$MIN_DISK_GB" ]]; then
    log_pass "Disk: ${disk_free_gb}GB free (>= ${MIN_DISK_GB}GB)"
else
    log_fail "Disk: ${disk_free_gb}GB free (< ${MIN_DISK_GB}GB required)"
fi

# ── Check 6: Port availability ──────────────────────────────────────────

for port in 8000 8100; do
    if lsof -i ":${port}" -sTCP:LISTEN >/dev/null 2>&1; then
        log_warn "Port ${port} already in use"
    else
        log_pass "Port ${port} available"
    fi
done

# ── Check 7: npm cache ownership ────────────────────────────────────────

npm_cache_dir="${NPM_CONFIG_CACHE:-$HOME/.npm}"
if [[ -d "$npm_cache_dir" ]]; then
    root_files=$(find "$npm_cache_dir" -maxdepth 2 -user root 2>/dev/null | head -1)
    if [[ -n "$root_files" ]]; then
        log_info "Fixing npm cache ownership (root-owned files detected)..."
        export NPM_CONFIG_CACHE="$HOME/.npm-cache"
        mkdir -p "$NPM_CONFIG_CACHE"
        log_pass "NPM_CONFIG_CACHE set to ${NPM_CONFIG_CACHE} (avoids root-owned cache)"
    else
        log_pass "npm cache ownership OK"
    fi
else
    log_pass "npm cache clean (no cache directory yet)"
fi

# ── Summary ─────────────────────────────────────────────────────────────

echo ""
echo "  ────────────────────────────────────"
echo -e "  ${GREEN}${pass_count} PASS${NC}  ${YELLOW}${warn_count} WARN${NC}  ${RED}${fail_count} FAIL${NC}"
echo "  ────────────────────────────────────"

if [[ $fail_count -gt 0 ]]; then
    echo ""
    echo -e "  ${RED}Fix the FAIL items above before proceeding.${NC}"
fi

# ── Admin Summary Block ─────────────────────────────────────────────────

echo ""
echo "  ╔══════════════════════════════════════════════════════════════╗"
echo "  ║  ADMIN SUMMARY — Copy this block to your admin             ║"
echo "  ╠══════════════════════════════════════════════════════════════╣"
printf "  ║  Hostname:  %-47s ║\n" "$(hostname)"
printf "  ║  Username:  %-47s ║\n" "$(whoami)"
printf "  ║  Arch:      %-47s ║\n" "$(uname -m)"
printf "  ║  macOS:     %-47s ║\n" "$(sw_vers -productVersion 2>/dev/null || echo 'N/A')"

# IP addresses
for ip in $(ifconfig 2>/dev/null | grep 'inet ' | grep -v 127.0.0.1 | awk '{print $2}' | head -2); do
    printf "  ║  IP:        %-47s ║\n" "$ip"
done

# SSH pubkey (if exists)
for keyfile in "$HOME/.ssh/id_ed25519.pub" "$HOME/.ssh/id_rsa.pub"; do
    if [[ -f "$keyfile" ]]; then
        key_short=$(awk '{print $1 " " substr($2,1,20) "..." " " $3}' "$keyfile")
        printf "  ║  SSH Key:   %-47s ║\n" "$key_short"
        break
    fi
done

printf "  ║  Checks:    %-47s ║\n" "${pass_count} pass, ${warn_count} warn, ${fail_count} fail"
echo "  ╚══════════════════════════════════════════════════════════════╝"
echo ""
