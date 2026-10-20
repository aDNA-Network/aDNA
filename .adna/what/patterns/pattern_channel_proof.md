---
type: pattern
created: 2026-10-04
updated: 2026-10-20
status: accepted
pattern_category: operational
applies_to: [coordination, credentials, federation, deploys, all_categories]
graduation: "n=3 instances across 2 graphs at adoption (2026-10-04); shipped in the template at v8.13"
last_edited_by: agent_rosetta
tags: [pattern, channel_proof, agent_scope, credentials, coordination, consuming_side]
---

# pattern_channel_proof — the consuming side proves a channel, never the provisioning side

> **Plain-language version first**: when you set up a way for someone to reach you — a shared drop-box, a key that lets a script log in, a deploy that puts a page on the web — the act of *setting it up* tells you almost nothing about whether it *works for the party that has to use it*. Only that party, actually using it, proves it. A read-back from your own side ("I granted the key", "the deploy returned 0", "the drop-box is live") is evidence that *you did something*, not that *they can*. The rule: **a channel is unproven until the party that must use it has used it**, and an agent must never go hunting outside its permission scope to make a channel work that was never proven for it.

## Problem

Channels get declared live by the side that provisions them. The provisioning side has every signal that says "done" — the key was minted, the ACL was granted, the directory was created, the deploy command exited 0 — and none of the signals that say "usable by the consumer": is the key *selectable* from where the consumer runs? does the consumer's process see the granted entry? does the alias serve the new bytes? The pattern was adopted after three incidents in two graphs, each paid for after a close had already called the channel live:

- a kit named a git drop-box its **primary** transmit channel and the close called it live; the first non-interactive agent to drive it could not, because the key it needed sat outside the agent's permission scope, correctly. The channel was provisioned, not proven;
- a pre-push secret-scan hook was installed and self-tested, yet resolved the wrong config file for five weeks; nobody knew until the first push that needed the right allowlist was blocked. Installed is not proven;
- a deploy was declared done on the deploy command's exit code. A deploy is proven by a probe of the live alias after the deploy, never by the command that pushed it. Same theorem, deploy costume.

The grant form of this rule is the older one: *a read-back from the granting side is not proof of access*. The channel form is the same theorem, and it is the one that keeps costing a ceremony its primary path.

## Solution

Four rules; the first is the pattern, the other three are what it implies.

1. **The consuming side proves a channel.** A channel (a credential grant, a drop-box, a mesh route, a deploy alias, a mailbox) moves from *provisioned* to *proven* only on a dated record of **the party that must use it having used it** — a real read, a real write, a real fetch, from the vantage it will actually run from. A read-back, a self-test, or an exit code on the provisioning side leaves it *provisioned*.
2. **Name the state honestly.** Any artifact that names a channel names its state: `provisioned` or `proven` (+ by whom, when, from where). "Primary" and "live" are not states; a kit that calls an unproven channel primary has told its reader something it does not know.
3. **Scope is a wall, not a hint.** An agent that finds a channel unusable from inside its permission scope **stops and reports**; it does not look for the credential, key or path that would make it work. What sits outside the scope was put there on purpose. *An agent must not hunt for credentials outside its permission scope.*
4. **The proof is as wide as the probe.** A proven channel is proven for *that* consumer, *that* vantage, *that* day. A second consumer, a second node, or a rotation re-opens the question: a negative result is only as wide as the command that produced it, and every absence assertion names its surface.

## When to Use

Any time a close, a kit, a memo or a STATE row is about to say that a channel *is live* — before the sentence is written. Specifically at: credential onboarding, drop-box or inbox conventions, mesh/route reachability (`how/skills/skill_mesh_probe_discipline.md` is the *probe* half; this is the *proof* half), deploys, and any federation seam where one vault provisions what another consumes.

## Example: This Template

The template ships its own instance of the trap. `how/standard/hooks/pre-push-sanitize.sh` carries a `--self-test` with `clean/` and `dirty/` fixtures. A green self-test is the *provisioning* side's read-back: it proves the hook's rules match its fixtures. It does not prove that your pushes run through the hook. That is proven only when a real push from your vault is scanned, and a planted control in that push is refused. Until then, call the hook *installed*, not *protecting*.

## Anti-Pattern

- A close that says *"the channel went live today"* on the strength of the provisioning side's commands.
- A kit that names a channel *primary* with no consumer record behind it.
- An agent that, finding a key unselectable, goes looking in `~/.ssh` for the one that would work.
- A proof carried forward past a rotation, a new consumer, or a new vantage without re-running.

## Related

- `how/skills/skill_mesh_probe_discipline.md` — the probe half: what you may claim about a peer's reachability, and from where.
- `how/skills/skill_node_credentials_audit.md` — the grant form, applied to a node's credentials.
- `how/standard/hooks/pre-push-sanitize.sh` — the example above.
