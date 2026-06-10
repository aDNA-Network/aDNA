#!/usr/bin/env bash
# governance_sync_check.sh — aDNA governance file consistency checker
# Checks template counts and version string consistency across governance files.
# Exit 0 = zero drift, Exit 1 = drift detected.

set -euo pipefail

ROOT="${1:-.}"
ERRORS=0

echo "=== aDNA Governance Sync Check ==="
echo "Root: $(cd "$ROOT" && pwd)"

# --- Template count check ---
TMPL_DIR="$ROOT/how/templates"
if [ -d "$TMPL_DIR" ]; then
    ACTUAL=$(find "$TMPL_DIR" -maxdepth 1 -name 'template_*.md' | wc -l | tr -d ' ')
    echo "Templates on disk: $ACTUAL"
    for GF in MANIFEST.md CLAUDE.md README.md; do
        GF_PATH="$ROOT/$GF"
        [ -f "$GF_PATH" ] || continue
        # Match patterns like "20 templates" or "Templates (20)"
        DOCUMENTED=$(grep -oE '([0-9]+)\s*templates|Templates?\s*\(([0-9]+)\)' "$GF_PATH" | grep -oE '[0-9]+' | head -1 || true)
        if [ -n "$DOCUMENTED" ] && [ "$DOCUMENTED" != "$ACTUAL" ]; then
            echo "  DRIFT: $GF says $DOCUMENTED templates, actual is $ACTUAL"
            ERRORS=$((ERRORS + 1))
        fi
    done
else
    echo "  WARNING: how/templates/ not found"
fi

# --- Version string check ---
echo ""
echo "Version strings:"
GOV_VERSION=""

if [ -f "$ROOT/CLAUDE.md" ]; then
    V=$(grep -E '^version:' "$ROOT/CLAUDE.md" | head -1 | sed 's/^version:[[:space:]]*//' | tr -d '"'"'"' ')
    if [ -n "$V" ]; then
        echo "  CLAUDE.md: v$V"
        GOV_VERSION="$V"
    fi
fi

if [ -f "$ROOT/CHANGELOG.md" ]; then
    V=$(grep -oE '\[v?([0-9]+\.[0-9]+)\]' "$ROOT/CHANGELOG.md" | head -1 | tr -d '[]v')
    if [ -n "$V" ]; then
        echo "  CHANGELOG.md: v$V"
        if [ -n "$GOV_VERSION" ] && [ "$V" != "$GOV_VERSION" ]; then
            echo "  DRIFT: CHANGELOG latest ($V) != CLAUDE.md ($GOV_VERSION)"
            ERRORS=$((ERRORS + 1))
        fi
    fi
fi

echo ""
if [ "$ERRORS" -eq 0 ]; then
    echo "RESULT: Zero drift"
    exit 0
else
    echo "RESULT: $ERRORS drift(s) detected"
    exit 1
fi
