#!/usr/bin/env bash
# setup.sh — Bootstrap Obsidian plugins and theme for adna
# Downloads 15 community plugins + Tokyo Night theme.
# Requires: curl (ships with macOS/Linux)
# Usage: ./setup.sh [--force]

set -euo pipefail

# ---------- Config ----------

VAULT_DIR="$(cd "$(dirname "$0")" && pwd)"
OBSIDIAN_DIR="$VAULT_DIR/.obsidian"
PLUGINS_DIR="$OBSIDIAN_DIR/plugins"
THEMES_DIR="$OBSIDIAN_DIR/themes"

FORCE=0
if [ "${1:-}" = "--force" ]; then
    FORCE=1
fi

# Plugin IDs and GitHub repos (parallel indexed arrays for bash 3.2 compat)
PLUGIN_IDS=(
    dataview
    templater-obsidian
    obsidian-meta-bind-plugin
    homepage
    obsidian-tasks-plugin
    obsidian-style-settings
    table-editor-obsidian
    obsidian42-brat
    notebook-navigator
    obsidian-icon-folder
    obsidian-advanced-canvas
    pretty-properties
    fold-properties-by-default
    termy
    settings-search
)
PLUGIN_REPOS=(
    blacksmithgu/obsidian-dataview
    SilentVoid13/Templater
    mProjectsCode/obsidian-meta-bind-plugin
    mirnovov/obsidian-homepage
    obsidian-tasks-group/obsidian-tasks
    mgmeyers/obsidian-style-settings
    tgrosinger/advanced-tables-obsidian
    TfTHacker/obsidian42-brat
    johansan/notebook-navigator
    FlorianWoelki/obsidian-iconize
    Developer-Mike/obsidian-advanced-canvas
    anareaty/pretty-properties
    tbergeron/obsidian-fold-properties-by-default
    ZyphrZero/Termy
    javalent/settings-search
)

THEME_REPO="tcmmichaelb139/obsidian-tokyonight"
THEME_NAME="Tokyo Night"

# ---------- Helpers ----------

info()  { printf "\033[1;34m[INFO]\033[0m  %s\n" "$1"; }
ok()    { printf "\033[1;32m[OK]\033[0m    %s\n" "$1"; }
skip()  { printf "\033[1;33m[SKIP]\033[0m  %s\n" "$1"; }
fail()  { printf "\033[1;31m[FAIL]\033[0m  %s\n" "$1"; }

# Check if a downloaded file is actually a 404 HTML page
is_valid_download() {
    local file="$1"
    if [ ! -f "$file" ]; then
        return 1
    fi
    # GitHub 404s return HTML — check first 4 bytes
    local head
    head="$(head -c 4 "$file" 2>/dev/null || true)"
    if [ "$head" = "<!DO" ] || [ "$head" = "<!do" ]; then
        return 1
    fi
    # Also reject empty files
    if [ ! -s "$file" ]; then
        return 1
    fi
    return 0
}

download_file() {
    local url="$1"
    local dest="$2"
    curl -fsSL --connect-timeout 10 --max-time 30 -o "$dest" "$url" 2>/dev/null
    if ! is_valid_download "$dest"; then
        rm -f "$dest"
        return 1
    fi
    return 0
}

# ---------- Main ----------

echo ""
echo "adna setup"
echo "=================="
echo "Vault: $VAULT_DIR"
echo ""

mkdir -p "$PLUGINS_DIR"
mkdir -p "$THEMES_DIR"

# --- Install plugins ---

PLUGIN_RESULTS=()
total=${#PLUGIN_IDS[@]}

for (( i=0; i<total; i++ )); do
    id="${PLUGIN_IDS[$i]}"
    repo="${PLUGIN_REPOS[$i]}"
    dest="$PLUGINS_DIR/$id"
    base_url="https://github.com/$repo/releases/latest/download"

    # Skip if already installed (has main.js) unless --force
    if [ "$FORCE" -eq 0 ] && [ -f "$dest/main.js" ]; then
        skip "$id (already installed)"
        PLUGIN_RESULTS+=("OK")
        continue
    fi

    mkdir -p "$dest"

    # Download main.js (required)
    if download_file "$base_url/main.js" "$dest/main.js"; then
        # Download manifest.json (required)
        if download_file "$base_url/manifest.json" "$dest/manifest.json"; then
            # Download styles.css (optional — many plugins don't have one)
            download_file "$base_url/styles.css" "$dest/styles.css" || true
            ok "$id"
            PLUGIN_RESULTS+=("OK")
        else
            rm -f "$dest/main.js"
            fail "$id (manifest.json download failed)"
            PLUGIN_RESULTS+=("FAIL")
        fi
    else
        fail "$id (main.js download failed — manual install required)"
        PLUGIN_RESULTS+=("FAIL")
    fi
done

# --- Install theme ---

echo ""
THEME_DIR="$THEMES_DIR/$THEME_NAME"
THEME_RESULT="FAIL"

if [ "$FORCE" -eq 0 ] && [ -f "$THEME_DIR/theme.css" ]; then
    skip "Theme: $THEME_NAME (already installed)"
    THEME_RESULT="OK"
else
    mkdir -p "$THEME_DIR"
    # Obsidian themes ship files in the repo root, not via GitHub Releases
    theme_url="https://raw.githubusercontent.com/$THEME_REPO/main"

    if download_file "$theme_url/theme.css" "$THEME_DIR/theme.css"; then
        if download_file "$theme_url/manifest.json" "$THEME_DIR/manifest.json"; then
            ok "Theme: $THEME_NAME"
            THEME_RESULT="OK"
        else
            fail "Theme: $THEME_NAME (manifest.json failed)"
        fi
    else
        fail "Theme: $THEME_NAME (theme.css failed)"
    fi
fi

# --- Ship curated workspace layout (clean ribbon, NN as primary sidebar) ---

if [ ! -f "$OBSIDIAN_DIR/workspace.json" ]; then
    if [ -f "$OBSIDIAN_DIR/workspace.default.json" ]; then
        cp "$OBSIDIAN_DIR/workspace.default.json" "$OBSIDIAN_DIR/workspace.json"
        ok "Workspace layout (clean sidebar)"
    else
        skip "Workspace layout (workspace.default.json missing)"
    fi
else
    skip "Workspace layout (already exists)"
fi

# ---------- Verification ----------

echo ""
echo "Verification"
echo "------------"
printf "%-35s %s\n" "Component" "Status"
printf "%-35s %s\n" "---------" "------"

for (( i=0; i<total; i++ )); do
    id="${PLUGIN_IDS[$i]}"
    status="${PLUGIN_RESULTS[$i]}"
    if [ "$status" = "OK" ]; then
        printf "%-35s \033[32m%s\033[0m\n" "$id" "OK"
    else
        printf "%-35s \033[31m%s\033[0m\n" "$id" "MISSING"
    fi
done

if [ "$THEME_RESULT" = "OK" ]; then
    printf "%-35s \033[32m%s\033[0m\n" "Theme: $THEME_NAME" "OK"
else
    printf "%-35s \033[31m%s\033[0m\n" "Theme: $THEME_NAME" "MISSING"
fi

# ---------- Summary ----------

fail_count=0
for r in "${PLUGIN_RESULTS[@]}"; do
    [ "$r" = "FAIL" ] && fail_count=$((fail_count + 1))
done
[ "$THEME_RESULT" = "FAIL" ] && fail_count=$((fail_count + 1))

echo ""
if [ "$fail_count" -eq 0 ]; then
    echo "All components installed successfully."
else
    echo "$fail_count component(s) need manual installation."
    echo "Open Obsidian → Settings → Community plugins → Browse"
fi

echo ""
echo "Optional: install Space Grotesk font from"
echo "  https://fonts.google.com/specimen/Space+Grotesk"
echo ""
echo "Open adna/ in Obsidian and enable community plugins when prompted."
