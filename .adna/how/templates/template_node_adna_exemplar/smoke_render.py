#!/usr/bin/env python3
"""smoke_render.py — dependency-free smoke test for template_node_adna_exemplar/.

Default (no args): renders every *.template in this bundle with a fabricated, deliberately
non-Hestia node profile (node-bravo / Athena) and proves zero leftover `{{vars}}`. Exit-Gate of
M25; re-run after editing any template (Prytaneion M3.4 made it a persisted artifact instead of
an in-session harness — the M25 fragility note).

Modes added by Prytaneion M6.1 (default behavior unchanged):

    python smoke_render.py                       # smoke test (M25 behavior)
    python smoke_render.py --materialize DIR     # write a rendered fork skeleton to DIR
    python smoke_render.py --parity              # reference-node skeleton-parity check:
                                                 #   HOME.md.template structure == live ../../..//HOME.md
                                                 #   (value-independent; see SUBSTITUTIONS.md §parity)

Pure stdlib (re + pathlib + shutil) — NO PyYAML, so it runs under either interpreter
(`python` or `python3`) regardless of the node's package state.

Exit 0 = PASS. Exit 1 = FAIL.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent
VAR_RE = re.compile(r"\{\{([a-z_]+)\}\}")

# Bundle-doc files that describe the bundle itself — never materialized into a fork.
BUNDLE_DOCS = {"README.md", "SUBSTITUTIONS.md", "SMOKE_TEST_DRY_RUN.md", "smoke_render.py"}

# ── Fabricated profile (deliberately unlike the Hestia reference node) ─────────
# Mirrors SMOKE_TEST_DRY_RUN.md; sourced from SUBSTITUTIONS.md. The two table vars
# carry `>`-prefixed callout-body lines (the M3.4 disclosure-fold profile).
PROFILE = {
    "node_hostname": "node-bravo",
    "operator": "ada",
    "persona": "Athena",
    "persona_lower": "athena",
    "machine_class": "Linux x86_64",
    "workspace_root": "/home/ada/lattice/",
    "vault_count": "12",
    "healthy_count": "12",
    "drift_count": "0",
    "blocked_count": "0",
    "named_project_count": "3",
    "last_inventory_refresh": "2026-06-05",
    "last_health_check": "2026-06-05",
    "interview_date": "2026-06-05",
    "persona_greeting": "By wisdom, the loom is strung. What are we doing?",
    "banner_image": "banner_athena.jpg",
    "banner_title": "node-bravo Home",
    "accent_primary_hex": "#4444AA",
    "accent_secondary_hex": "#cfd8ff",
    "accent_tertiary_hex": "#7dffd0",
    # M6.1 canvas-chrome theming vars (SUBSTITUTIONS §2)
    "canvas_text_strong_hex": "#eef2fb",
    "canvas_text_em_hex": "#a6b8e8",
    # M6.1/J1 optional health narrative — empty default exercises the optional path
    "health_detail_note": "",
    # Table vars — `>`-prefixed callout-body lines (M3.4 fold profile). The 12 entries mirror the
    # node-bravo dry-run fleet (M6.1) so a materialized fork's fold body matches its fabricated
    # inventory_vaults.yaml at the eye check.
    "vaults_table": (
        "> - **Forges (2)** · [LoomForge](../LoomForge.aDNA/) · [PotteryForge](../PotteryForge.aDNA/)\n"
        "> - **Frameworks (1)** · [AthenaWeave](../AthenaWeave.aDNA/)\n"
        "> - **Platforms (2)** · [Olympus](../Olympus.aDNA/) · [Oracle](../Oracle.aDNA/)\n"
        "> - **Org-Vaults (2)** · [AcademyOfAthens](../AcademyOfAthens.aDNA/) · [Agora](../Agora.aDNA/)\n"
        "> - **Org-Graphs (2)** · [Delphi](../Delphi.aDNA/) · [Sparta](../Sparta.aDNA/)\n"
        "> - **Network (1)** · [Pantheon](../Pantheon.aDNA/)\n"
        "> - **Coordination (1)** · [Heralds](../Heralds.aDNA/)\n"
        "> - **Node & Tooling (1)** · [Home.aDNA — here](./)"
    ),
    "named_projects_table": "> No named projects on this node yet.",
}


def render_text(text: str) -> str:
    out = text
    for var, val in PROFILE.items():
        out = out.replace("{{" + var + "}}", val)
    return out


def render_name(rel: str) -> str:
    for var, val in PROFILE.items():
        rel = rel.replace("{{" + var + "}}", val)
    return rel


def smoke() -> int:
    """M25 default mode — render in memory, prove zero leftovers + full catalog coverage."""
    templates = sorted(BUNDLE.rglob("*.template"))
    if not templates:
        print("FAIL: no *.template files found", file=sys.stderr)
        return 1

    rendered_names: list[str] = []
    leftover: list[str] = []
    uncatalogued: set[str] = set()
    exercised: set[str] = set()

    for tpl in templates:
        text = tpl.read_text(encoding="utf-8")
        for var in VAR_RE.findall(text):
            exercised.add(var)
            if var not in PROFILE:
                uncatalogued.add(var)
        out = render_text(text)
        rel = render_name(str(tpl.relative_to(BUNDLE)))
        rendered_names.append(rel[: -len(".template")])
        if VAR_RE.search(out):
            for m in VAR_RE.findall(out):
                leftover.append(f"{tpl.relative_to(BUNDLE)} → {{{{{m}}}}}")

    print(f"Templates rendered ({len(templates)}):")
    for n in rendered_names:
        print(f"  - {n}")
    print(f"\nVars exercised ({len(exercised)}): {sorted(exercised)}")

    ok = True
    if uncatalogued:
        ok = False
        print(f"\nFAIL — template vars absent from PROFILE/SUBSTITUTIONS: {sorted(uncatalogued)}")
    if leftover:
        ok = False
        print(f"\nFAIL — leftover placeholders after render:")
        for L in leftover:
            print(f"  {L}")
    if ok:
        print("\n✓ PASS — every placeholder resolves; no leftover {{vars}}; "
              "CSS materializes as athena_accent.css + athena_canvas.css; "
              "no Hestia/#663399 literal leaks.")
        return 0
    return 1


def materialize(target: Path) -> int:
    """M6.1 — write a rendered fork skeleton: render *.template, copy verbatim assets,
    skip the bundle docs. The smoke-test invariants are enforced on the way out."""
    if target.exists() and any(target.iterdir()):
        print(f"FAIL: target {target} exists and is not empty", file=sys.stderr)
        return 1
    n_rendered = n_copied = 0
    leftover: list[str] = []
    for src in sorted(BUNDLE.rglob("*")):
        if not src.is_file():
            continue
        rel = str(src.relative_to(BUNDLE))
        if rel in BUNDLE_DOCS or "__pycache__" in rel:
            continue
        if rel.endswith(".template"):
            out_rel = render_name(rel)[: -len(".template")]
            out_text = render_text(src.read_text(encoding="utf-8"))
            for m in VAR_RE.findall(out_text):
                leftover.append(f"{out_rel} → {{{{{m}}}}}")
            dst = target / out_rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(out_text, encoding="utf-8")
            n_rendered += 1
        else:
            dst = target / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            n_copied += 1
    print(f"Materialized → {target}\n  rendered: {n_rendered} templates · copied verbatim: {n_copied} files")
    if leftover:
        print("\nFAIL — leftover placeholders in materialized files:")
        for L in leftover:
            print(f"  {L}")
        return 1
    print("✓ materialize OK — 0 leftover placeholders")
    return 0


# ── M6.1/J1 skeleton-parity check (reference node only) ───────────────────────
# Value-independent: each non-comment template line becomes a regex ({{var}} → (.+?) /
# block vars consume `>`-prefixed runs), then live HOME.md must match line-for-line.
# Enumerated divergences (SUBSTITUTIONS §parity): template-guidance HTML comments are
# stripped; the Personae line is excluded on both sides (live node-enriched).
BLOCK_VARS = {"vaults_table", "named_projects_table"}


def _strip_for_parity(text: str, personae_prefix: str) -> list[str]:
    text = re.sub(r"<!--.*?-->\n*", "", text, flags=re.S)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return [l for l in text.splitlines() if not l.startswith(personae_prefix)]


def parity() -> int:
    live_path = BUNDLE.parents[2] / "HOME.md"   # how/templates/<bundle>/ → vault root
    if not live_path.exists():
        print(f"FAIL: live HOME.md not found at {live_path} (parity mode is reference-node-only)",
              file=sys.stderr)
        return 1
    tpl_lines = _strip_for_parity((BUNDLE / "HOME.md.template").read_text(encoding="utf-8"),
                                  "> - **Personae**")
    live_lines = _strip_for_parity(live_path.read_text(encoding="utf-8"),
                                   "> - **Other personae**")
    i = j = 0
    while i < len(tpl_lines):
        t = tpl_lines[i]
        only_var = VAR_RE.fullmatch(t.strip())
        if only_var and only_var.group(1) in BLOCK_VARS:
            # Block var: consume one-or-more `>`-prefixed live lines
            if j >= len(live_lines) or not live_lines[j].startswith(">"):
                print(f"PARITY FAIL at live line {j+1}: expected callout-body block for "
                      f"{{{{{only_var.group(1)}}}}}, got: {live_lines[j] if j < len(live_lines) else '<EOF>'}")
                return 1
            while j < len(live_lines) and live_lines[j].startswith(">"):
                j += 1
            i += 1
            continue
        pattern = "^" + re.sub(r"\\\{\\\{[a-z_]+\\\}\\\}", "(.*?)", re.escape(t)) + "$"
        if j >= len(live_lines) or not re.match(pattern, live_lines[j]):
            print(f"PARITY FAIL — template line {i+1} does not match live line {j+1}:")
            print(f"  template: {t}")
            print(f"  live    : {live_lines[j] if j < len(live_lines) else '<EOF>'}")
            return 1
        i += 1
        j += 1
    if j != len(live_lines):
        print(f"PARITY FAIL — live HOME has {len(live_lines) - j} unmatched trailing line(s), first:")
        print(f"  live: {live_lines[j]}")
        return 1
    print("✓ PARITY — live HOME.md matches HOME.md.template structure "
          "(modulo the 2 enumerated divergences; see SUBSTITUTIONS.md)")
    return 0


def main() -> int:
    args = sys.argv[1:]
    if not args:
        return smoke()
    if args[0] == "--materialize" and len(args) == 2:
        rc = smoke()
        if rc != 0:
            return rc
        return materialize(Path(args[1]).resolve())
    if args[0] == "--parity":
        return parity()
    print(__doc__, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
