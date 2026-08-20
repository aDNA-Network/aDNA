# Contributing to aDNA

This repository is the **clone-and-run image**: clone it, open it with an agent, and you have the aDNA
standard, its skills, and its templates ready to use. The standard itself lives in
[`.adna/`](.adna/).

This page is the front door. It routes you; it does not repeat the detail.

**By taking part you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).**

---

## Pick your route

| What you have | Where it goes |
|---|---|
| A bug — a dead link, a broken template, a schema that doesn't match the docs | [Bug report](https://github.com/aDNA-Network/aDNA/issues/new?template=bug_report.md) |
| A question | [Open an issue](https://github.com/aDNA-Network/aDNA/issues) and say it's a question, or ask in the [community space](https://community.adna.network) |
| A fix, an improvement, a new template or pattern | A pull request — see [the full guide](.adna/CONTRIBUTING.md) |
| **A change to what the standard requires of a conforming vault** | The **proposal process** — see below |

Most contributions are the middle two rows. The proposal process exists for the last one, and using it
for anything else just slows your change down.

## Changing the standard

Normative changes — anything that alters what a conforming vault MUST, SHOULD, or MAY do — go through
numbered **aDNA Enhancement Proposals (AEPs)**.

- Read the process: **[adna.network/community/proposals](https://adna.network/community/proposals/)**
- The process itself is [AEP-1](https://adna.network/community/proposals/aep-1/), which was filed
  through the process it describes.
- File one by opening a [change proposal](https://github.com/aDNA-Network/aDNA/issues/new?template=change_proposal.md)
  and saying that the change is normative.

Three things worth knowing before you file:

1. **Numbers are permanent.** A proposal that gets rejected keeps its number and stays in the public
   archive. You can read what this project turned down.
2. **Only a human ratifies.** No proposal is accepted without a named person and a date.
3. **`final` means enforced**, not agreed. A proposal is only called final once a check in aDNA's own
   tooling fails when the rule is violated.

## AI-assisted contributions

**Welcome, and disclosed.** Agents may draft proposals and open pull requests. Every proposal carries a
field naming the agent that drafted it, if one did — this is a required field, not a convention.

This is not a concession; it is how the project already works. aDNA is a standard for making project
knowledge navigable by agents, and most of its own documentation was drafted by one and ratified by a
person. Saying so is more useful than pretending otherwise.

What we ask: say that an agent was involved, and check the output before you send it. An unreviewed
agent PR is the same problem as an unreviewed human PR, and it arrives faster.

## The full guide

Setup, style, file naming, frontmatter rules, the review conventions, and how agents route upstream
suggestions — all of it is in **[`.adna/CONTRIBUTING.md`](.adna/CONTRIBUTING.md)**, alongside the
standard it describes. That file is the source; this one is the signpost, so the two cannot drift.
