#!/usr/bin/env python3
"""aDNA Instance Validator — checks conformance per §5.5 of the aDNA Universal Standard v2.2.

Usage:
    python adna_validate.py <path>                     # Validate instance at path
    python adna_validate.py <path> --level standard    # Check specific level
    python adna_validate.py <path> --governance        # Run governance sync checks
    python adna_validate.py <path> --verbose           # Detailed output
    python adna_validate.py <path> --json              # Machine-readable JSON output
"""
import argparse
import json
import os
import re
import sys

import yaml

# ---------------------------------------------------------------------------
# Conformance requirements per §5.5
# ---------------------------------------------------------------------------

STARTER_GOV_FILES = ["CLAUDE.md", "MANIFEST.md", "README.md"]
STARTER_DIRS = [
    "what/context",
    "how/missions",
    "how/sessions",
    "how/templates",
    "who/coordination",
    "who/governance",
]
TRIAD_DIRS = ["what", "how", "who"]

STANDARD_GOV_FILES = ["STATE.md", "AGENTS.md"]
STANDARD_AGENTS_DIRS = ["what", "how", "who"]
STANDARD_RECOMMENDED_DIRS = [
    "what/decisions",
    "how/backlog",
    "how/sessions/active",
    "how/sessions/history",
]

REQUIRED_FRONTMATTER = ["type", "created", "updated", "status", "last_edited_by", "tags"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _resolve_root(path):
    """Detect bare vs embedded triad and return (root, triad_prefix)."""
    if os.path.isdir(os.path.join(path, ".agentic", "what")):
        return path, ".agentic"
    return path, ""


def _parse_frontmatter(filepath):
    """Extract YAML frontmatter from a markdown file. Returns dict or None."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except (OSError, UnicodeDecodeError):
        return None
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None


def _find_md_files(root, triad_prefix):
    """Yield all .md files inside the triad directories."""
    for leg in TRIAD_DIRS:
        leg_path = os.path.join(root, triad_prefix, leg) if triad_prefix else os.path.join(root, leg)
        if not os.path.isdir(leg_path):
            continue
        for dirpath, _, filenames in os.walk(leg_path):
            for fn in filenames:
                if fn.endswith(".md"):
                    yield os.path.join(dirpath, fn)


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

class ValidationResult:
    def __init__(self):
        self.errors = []     # MUST violations
        self.warnings = []   # SHOULD violations
        self.info = []       # informational
        self.level = None    # determined conformance level

    @property
    def passed(self):
        return len(self.errors) == 0

    def as_dict(self):
        return {
            "passed": self.passed,
            "level": self.level,
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info,
        }


def check_starter(root, prefix, result):
    """Check Level 1 (Starter) conformance."""
    # Governance files
    for gf in STARTER_GOV_FILES:
        if not os.path.isfile(os.path.join(root, gf)):
            result.errors.append(f"Starter: missing governance file '{gf}'")

    # Triad directories
    for td in TRIAD_DIRS:
        p = os.path.join(root, prefix, td) if prefix else os.path.join(root, td)
        if not os.path.isdir(p):
            result.errors.append(f"Starter: missing triad directory '{td}/'")

    # Required subdirectories
    for sd in STARTER_DIRS:
        p = os.path.join(root, prefix, sd) if prefix else os.path.join(root, sd)
        if not os.path.isdir(p):
            result.errors.append(f"Starter: missing required directory '{sd}/'")

    # Frontmatter on content files
    fm_errors = 0
    total_files = 0
    for fp in _find_md_files(root, prefix):
        total_files += 1
        fm = _parse_frontmatter(fp)
        rel = os.path.relpath(fp, root)
        if fm is None:
            fm_errors += 1
            result.errors.append(f"Frontmatter: missing or unparseable in '{rel}'")
            continue
        for field in REQUIRED_FRONTMATTER:
            if field not in fm:
                fm_errors += 1
                result.errors.append(f"Frontmatter: missing required field '{field}' in '{rel}'")

    result.info.append(f"Scanned {total_files} content files, {fm_errors} frontmatter issues")


def check_standard(root, prefix, result):
    """Check Level 2 (Standard) conformance — assumes Starter already checked."""
    for gf in STANDARD_GOV_FILES:
        if not os.path.isfile(os.path.join(root, gf)):
            result.errors.append(f"Standard: missing governance file '{gf}'")

    for ad in STANDARD_AGENTS_DIRS:
        p = os.path.join(root, prefix, ad, "AGENTS.md") if prefix else os.path.join(root, ad, "AGENTS.md")
        if not os.path.isfile(p):
            result.errors.append(f"Standard: missing '{ad}/AGENTS.md'")

    for rd in STANDARD_RECOMMENDED_DIRS:
        p = os.path.join(root, prefix, rd) if prefix else os.path.join(root, rd)
        if not os.path.isdir(p):
            result.warnings.append(f"Standard: recommended directory '{rd}/' not found")


def check_full(root, prefix, result):
    """Check Level 3 (Full) conformance — assumes Standard already checked."""
    # Context library with topic dirs
    ctx = os.path.join(root, prefix, "what/context") if prefix else os.path.join(root, "what/context")
    if os.path.isdir(ctx):
        topic_dirs = [d for d in os.listdir(ctx) if os.path.isdir(os.path.join(ctx, d))]
        if not topic_dirs:
            result.errors.append("Full: what/context/ has no topic subdirectories")
        else:
            has_agents = any(os.path.isfile(os.path.join(ctx, td, "AGENTS.md")) for td in topic_dirs)
            if not has_agents:
                result.errors.append("Full: no topic directory in what/context/ has AGENTS.md")
    else:
        result.errors.append("Full: what/context/ directory missing")

    # Ontology artifact
    onto = os.path.join(root, prefix, "what/ontology.md") if prefix else os.path.join(root, "what/ontology.md")
    if not os.path.isfile(onto):
        result.errors.append("Full: missing what/ontology.md")

    # Template compliance — check templates dir has files
    tmpl = os.path.join(root, prefix, "how/templates") if prefix else os.path.join(root, "how/templates")
    if os.path.isdir(tmpl):
        templates = [f for f in os.listdir(tmpl) if f.endswith(".md") and f.startswith("template_")]
        result.info.append(f"Found {len(templates)} templates in how/templates/")
    else:
        result.errors.append("Full: how/templates/ directory missing")


def determine_level(root, prefix):
    """Determine the highest conformance level the instance passes."""
    for level_name, checker in [("full", check_full), ("standard", check_standard), ("starter", check_starter)]:
        pass  # we check bottom-up

    # Check starter
    r = ValidationResult()
    check_starter(root, prefix, r)
    if not r.passed:
        return None, r

    # Check standard
    r2 = ValidationResult()
    r2.errors = list(r.errors)
    r2.warnings = list(r.warnings)
    r2.info = list(r.info)
    check_standard(root, prefix, r2)
    standard_errors = [e for e in r2.errors if e not in r.errors]

    # Check full
    r3 = ValidationResult()
    r3.errors = list(r2.errors)
    r3.warnings = list(r2.warnings)
    r3.info = list(r2.info)
    check_full(root, prefix, r3)
    full_errors = [e for e in r3.errors if e not in r2.errors]

    if not full_errors and not standard_errors:
        r3.level = "full"
        return "full", r3
    elif not standard_errors:
        r2.level = "standard"
        return "standard", r2
    else:
        r.level = "starter"
        return "starter", r


# ---------------------------------------------------------------------------
# Governance sync checks (--governance flag)
# ---------------------------------------------------------------------------

def check_governance_sync(root, result):
    """Check governance file consistency: template counts, version strings."""
    # Template count
    tmpl_dir = os.path.join(root, "how", "templates")
    if os.path.isdir(tmpl_dir):
        actual = len([f for f in os.listdir(tmpl_dir) if f.endswith(".md") and f.startswith("template_")])
        # Check documented counts
        for gf in ["MANIFEST.md", "CLAUDE.md", "README.md"]:
            gf_path = os.path.join(root, gf)
            if not os.path.isfile(gf_path):
                continue
            with open(gf_path, "r") as f:
                content = f.read()
            # Look for patterns like "20 templates" or "Templates (20)"
            for m in re.finditer(r"(\d+)\s*templates|Templates?\s*\((\d+)\)", content):
                documented = int(m.group(1) or m.group(2))
                if documented != actual:
                    result.errors.append(
                        f"Governance drift: {gf} says {documented} templates, actual count is {actual}"
                    )

    # Version string consistency
    versions_found = {}
    claude_path = os.path.join(root, "CLAUDE.md")
    if os.path.isfile(claude_path):
        fm = _parse_frontmatter(claude_path)
        if fm and "version" in fm:
            versions_found["CLAUDE.md (frontmatter)"] = str(fm["version"])

    readme_path = os.path.join(root, "README.md")
    if os.path.isfile(readme_path):
        with open(readme_path, "r") as f:
            for line in f:
                m = re.search(r"Version\s+(\d+\.\d+)", line)
                if m:
                    versions_found["README.md"] = m.group(1)
                    break

    changelog_path = os.path.join(root, "CHANGELOG.md")
    if os.path.isfile(changelog_path):
        with open(changelog_path, "r") as f:
            for line in f:
                m = re.search(r"\[v?(\d+\.\d+)\]", line)
                if m:
                    versions_found["CHANGELOG.md (latest)"] = m.group(1)
                    break

    if versions_found:
        gov_versions = {k: v for k, v in versions_found.items() if "standard" not in k.lower()}
        unique = set(gov_versions.values())
        if len(unique) > 1:
            details = ", ".join(f"{k}={v}" for k, v in gov_versions.items())
            result.warnings.append(f"Version note: governance versions differ across files ({details})")
        result.info.append(f"Versions found: {versions_found}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="aDNA Instance Validator (§5.5)")
    parser.add_argument("path", help="Path to aDNA instance root")
    parser.add_argument("--level", choices=["starter", "standard", "full"],
                        help="Check specific conformance level (default: auto-detect)")
    parser.add_argument("--governance", action="store_true",
                        help="Run governance sync checks (template counts, version strings)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Detailed output")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        print(f"Error: '{root}' is not a directory", file=sys.stderr)
        sys.exit(2)

    root, prefix = _resolve_root(root)

    if args.governance:
        result = ValidationResult()
        check_governance_sync(root, result)
        if args.json:
            print(json.dumps(result.as_dict(), indent=2))
        else:
            if result.errors:
                print("GOVERNANCE SYNC: DRIFT DETECTED")
                for e in result.errors:
                    print(f"  ERROR: {e}")
            else:
                print("GOVERNANCE SYNC: Zero drift")
            for w in result.warnings:
                print(f"  WARNING: {w}")
            if args.verbose:
                for i in result.info:
                    print(f"  INFO: {i}")
        sys.exit(0 if result.passed else 1)

    if args.level:
        result = ValidationResult()
        check_starter(root, prefix, result)
        if args.level in ("standard", "full"):
            check_standard(root, prefix, result)
        if args.level == "full":
            check_full(root, prefix, result)
        result.level = args.level
    else:
        _, result = determine_level(root, prefix)

    if args.json:
        print(json.dumps(result.as_dict(), indent=2))
        sys.exit(0 if result.passed else 1)

    # Human-readable output
    level_label = result.level.capitalize() if result.level else "NONE"
    if result.passed:
        print(f"{level_label} conformance, all checks pass")
    else:
        print(f"FAILED — does not meet Starter conformance")

    if result.errors or args.verbose:
        for e in result.errors:
            print(f"  ERROR: {e}")
    if args.verbose:
        for w in result.warnings:
            print(f"  WARNING: {w}")
        for i in result.info:
            print(f"  INFO: {i}")

    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
