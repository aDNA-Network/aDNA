# Security & Disclosure

aDNA is an open standard and a set of plain-Markdown, local-first knowledge vaults. The project
ships no runtime service by default. Even so, we take coordinated disclosure seriously — here is
how to report a vulnerability and what to expect.

The human-readable version of this policy lives at <https://adna.network/security/>.

## Reporting a vulnerability

**Please report privately — do not open a public issue for a security problem.**

Open a private report through GitHub Security Advisories on this repository:
<https://github.com/aDNA-Network/aDNA/security/advisories/new>

If you cannot use GitHub Security Advisories, open a minimal public issue saying only
"security report — please open a private channel" (with no details), and a maintainer will
follow up privately. Where you can, include the affected file, route, or script, steps to
reproduce, and the impact you foresee.

## Scope

**In scope:** the published standard and templates (the `.adna/` tree, skills, governance
templates); the website tooling and build scripts in the site's source repository; and any
workflow the repository executes (CI, the gate harness).

**Out of scope:** third-party tools the standard composes with (Obsidian, Claude Code, git
hosts) — report those to their own maintainers; and self-managed deployments or private vaults
you run on your own infrastructure.

## What to expect

- **Acknowledgement** — we aim to acknowledge a report within a few business days.
- **Assessment** — we confirm the issue, determine severity and affected versions, and keep you
  updated.
- **Coordinated disclosure** — we agree a disclosure timeline with you and credit you in the
  advisory unless you prefer to remain anonymous.

There is no bug bounty program. Credit and thanks are real; payment is not currently offered.
