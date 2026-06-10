#!/usr/bin/env python3
"""Aggregate side-quest results from how/quests/results/*.md files.

Reference implementation for maintainers. Reads YAML frontmatter from
result files, computes per-quest statistics, and flags outliers.

Usage:
    python what/lattices/tools/aggregate_results.py
    python what/lattices/tools/aggregate_results.py --quest quest_frontmatter_comparison
    python what/lattices/tools/aggregate_results.py --help

Dependencies: Python 3.8+ stdlib only (no pip packages).
"""

import argparse
import os
import re
import statistics
import sys
from pathlib import Path


def parse_frontmatter(filepath: Path) -> dict | None:
    """Extract YAML frontmatter from a markdown file.

    Simple parser — handles the subset of YAML used in quest result
    frontmatter (scalar values, simple mappings). Does not handle
    full YAML spec (anchors, multi-line strings, etc.).
    """
    text = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None

    frontmatter = {}
    current_key = None
    current_dict = None

    for line in match.group(1).split("\n"):
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue

        # Nested key (2-space indent)
        indent_match = re.match(r"^  (\w+):\s*(.*)", line)
        if indent_match and current_key:
            if current_dict is None:
                current_dict = {}
                frontmatter[current_key] = current_dict
            key, value = indent_match.group(1), indent_match.group(2).strip()
            current_dict[key] = _parse_value(value)
            continue

        # Top-level key
        top_match = re.match(r"^(\w+):\s*(.*)", line)
        if top_match:
            current_key = top_match.group(1)
            current_dict = None
            value = top_match.group(2).strip()
            if value:
                frontmatter[current_key] = _parse_value(value)
            continue

    return frontmatter


def _parse_value(raw: str):
    """Parse a simple YAML value (string, number, boolean, quoted)."""
    if not raw:
        return None
    # Strip quotes
    if (raw.startswith('"') and raw.endswith('"')) or (
        raw.startswith("'") and raw.endswith("'")
    ):
        return raw[1:-1]
    # Booleans
    if raw.lower() in ("true", "yes"):
        return True
    if raw.lower() in ("false", "no"):
        return False
    # Numbers
    try:
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        pass
    return raw


def find_result_files(results_dir: Path) -> list[Path]:
    """Find all result markdown files in the results directory."""
    if not results_dir.exists():
        return []
    return sorted(results_dir.glob("result_*.md"))


def aggregate_by_quest(results: list[dict]) -> dict[str, list[dict]]:
    """Group results by quest_id."""
    grouped: dict[str, list[dict]] = {}
    for r in results:
        qid = r.get("quest_id", "unknown")
        grouped.setdefault(qid, []).append(r)
    return grouped


def compute_stats(values: list[float]) -> dict:
    """Compute summary statistics for a list of numeric values."""
    if not values:
        return {}
    stats = {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": round(statistics.mean(values), 2),
    }
    if len(values) >= 2:
        stats["median"] = round(statistics.median(values), 2)
        stats["stdev"] = round(statistics.stdev(values), 2)
    else:
        stats["median"] = stats["mean"]
        stats["stdev"] = 0.0
    return stats


def detect_outliers(values: list[float], threshold: float = 2.0) -> list[int]:
    """Return indices of values more than threshold standard deviations from mean."""
    if len(values) < 3:
        return []
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    if stdev == 0:
        return []
    return [i for i, v in enumerate(values) if abs(v - mean) > threshold * stdev]


def extract_numeric_fields(results: list[dict]) -> dict[str, list[float]]:
    """Extract all numeric measurement fields from environment metadata."""
    fields: dict[str, list[float]] = {}
    for r in results:
        env = r.get("environment", {})
        if isinstance(env, dict):
            for k, v in env.items():
                if isinstance(v, (int, float)):
                    fields.setdefault(k, []).append(float(v))
    return fields


def print_summary(grouped: dict[str, list[dict]]) -> None:
    """Print aggregated summary table to stdout."""
    print("=" * 70)
    print("SIDE-QUEST RESULTS AGGREGATION")
    print("=" * 70)

    if not grouped:
        print("\nNo results found.")
        return

    for quest_id, results in sorted(grouped.items()):
        print(f"\n{'─' * 70}")
        print(f"Quest: {quest_id}")
        print(f"Submissions: {len(results)}")
        print(f"{'─' * 70}")

        # Extract numeric fields from environment
        numeric = extract_numeric_fields(results)
        if numeric:
            print(f"\n  {'Metric':<30} {'Count':>6} {'Mean':>10} {'Median':>10} {'Min':>10} {'Max':>10}")
            print(f"  {'─' * 76}")
            for field, values in sorted(numeric.items()):
                stats = compute_stats(values)
                outliers = detect_outliers(values)
                flag = " (!)" if outliers else ""
                print(
                    f"  {field:<30} {stats['count']:>6} "
                    f"{stats['mean']:>10.2f} {stats['median']:>10.2f} "
                    f"{stats['min']:>10.2f} {stats['max']:>10.2f}{flag}"
                )
                if outliers:
                    print(f"    ↳ Outliers at indices: {outliers} (>{2.0}σ from mean)")
        else:
            print("\n  No numeric fields found in environment metadata.")

        # List operators
        operators = [r.get("operator", "anonymous") for r in results]
        print(f"\n  Contributors: {', '.join(str(o) for o in operators)}")

    print(f"\n{'=' * 70}")
    print(f"Total quests: {len(grouped)}  |  Total submissions: {sum(len(v) for v in grouped.values())}")
    print(f"{'=' * 70}")


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate side-quest results from how/quests/results/*.md"
    )
    parser.add_argument(
        "--quest",
        help="Filter to a specific quest_id",
        default=None,
    )
    parser.add_argument(
        "--results-dir",
        help="Path to results directory (default: how/quests/results/)",
        default=None,
    )
    args = parser.parse_args()

    # Find results directory relative to script or repo root
    if args.results_dir:
        results_dir = Path(args.results_dir)
    else:
        # Try relative to CWD first, then relative to script
        cwd_path = Path.cwd() / "how" / "quests" / "results"
        script_path = Path(__file__).parent.parent.parent / "how" / "quests" / "results"
        results_dir = cwd_path if cwd_path.exists() else script_path

    files = find_result_files(results_dir)
    if not files:
        print(f"No result files found in {results_dir}")
        print("Results should be named: result_<quest_id>_<date>_<name>.md")
        sys.exit(0)

    # Parse all results
    results = []
    for f in files:
        fm = parse_frontmatter(f)
        if fm:
            fm["_file"] = str(f)
            results.append(fm)
        else:
            print(f"Warning: could not parse frontmatter from {f}", file=sys.stderr)

    # Filter by quest if specified
    if args.quest:
        results = [r for r in results if r.get("quest_id") == args.quest]

    # Aggregate and print
    grouped = aggregate_by_quest(results)
    print_summary(grouped)


if __name__ == "__main__":
    main()
