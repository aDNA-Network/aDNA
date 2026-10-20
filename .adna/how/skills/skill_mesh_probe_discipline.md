---
type: skill
skill_type: process
created: 2026-10-20
updated: 2026-10-20
status: active
category: network_operations
trigger: "Any reachability claim about a mesh peer — UP or DOWN — before recording, relaying, or acting on it"
last_edited_by: agent_rosetta
tags: [skill, process, mesh, probe, reachability, warmup, vantage, recovery, expected_intermittent, node_vault]
---

# skill_mesh_probe_discipline

**What this is, plainly:** before you write down that a machine on your private network is up or down, you follow
eight small rules. Each one exists because an agent once got it wrong, and the wrong answer cost more to retract
than the rule costs to follow.

**For developers:** a process skill for any agent that probes peers over a private overlay mesh (Nebula, WireGuard,
Tailscale and similar). It governs *reachability claims*, not the mesh's configuration. Fill the tokens from your
node vault at fork time:

| Token | Meaning | Where it lives |
|---|---|---|
| `{{MESH_NAME}}` | the overlay's name | your node vault's connectivity inventory (`Home.aDNA/what/inventory/`) |
| `{{MESH_CIDR}}` | the overlay's address block | same; never written into a shared or public file |
| `{{HEALTH_SURFACE}}` | where the node records host health and expected-intermittent notes | your node vault |

Examples below use RFC 5737 documentation addresses (`198.51.100.0/24`), never a real overlay address.

## The two failure modes

**1. Cold-tunnel false negative.** The first probe to an idle peer can fail while the tunnel's handshake completes.
A cold probe looks exactly like an outage.

**2. Vantage error.** "Unreachable from here" does not mean "down". A peer whose firewall admits only some sources
answers those sources and silently drops the rest, by design. On meshes with certificate groups, whether you reach a
port depends on the *probing* side's groups as well.

## The rule

1. **Warm, then measure.** Send a throwaway `ping -c2 <peer>` first, then the real measurement, e.g.
   `ping -c5 -t15 <peer>` (example form: `ping -c5 -t15 198.51.100.7`). Never conclude anything from a single cold probe.
2. **State the vantage.** Every recorded reachability fact names the machine it was measured from (`A→peer 5/5 0%`
   is not the same fact as `B→peer`). A claim without a vantage is not a fact.
3. **Cross-check before declaring DOWN.** A peer is down when it fails a warm probe **and** sibling peers answer
   from the same vantage in the same window. If the lighthouses or coordinators answer and only the target does
   not, that is evidence. If nothing answers, the problem is local.
4. **Re-probe before acting on someone else's DOWN claim.** That includes a partner's report and your own claim
   from an earlier session. Claims go stale; expect it.
5. **Bound every probe with `timeout`.** A hung host must never stall a reply to the operator.
6. **Only the far side proves access.** A grant, key or firewall rule read from the granting side is not proof.
   The receiving side's fetch or login is. This is the same sentence as rule 1 of
   [[pattern_channel_proof]]: this skill is the *probe* half, the pattern is the *proof* half.
7. **Recovery claims get the same bounds as down claims.** A warm 5/5 proves "up as of `<time>`, from `<vantage>`"
   and nothing more; on a flapping host it can land inside a brief up-window. So **(a)** never write "recovered";
   write "up as of `<time>`", just as rule 3 forbids a bare "down". **(b)** Re-read any reachability verdict
   recorded mid-session against `{{HEALTH_SURFACE}}` at session close, before it ships.
8. **Expected-intermittent is a declared posture, not a probe result.** When the operator says a host will flap
   (travel, maintenance, power work), record a dated note at `{{HEALTH_SURFACE}}`. The machinery keeps reporting;
   readers stop re-triaging. The note retires on the **named human signal** ("they say they're back"), never on a
   green probe. Rule 7 is why a green probe cannot retire it.

## Provenance (why each rule exists)

The rules were paid for in a mesh's own operational graph, one finding at a time. In order: a cold probe written
into the vault as a blocker and relayed to a partner, while the host had been up throughout; an alarm raised after
probing the wrong address (*probe the address you mean*); a session of correctly warmed probes that all read DOWN,
with the host surfacing minutes after the close (say "down as of `<time>`"); and the mirror image, a warmed probe
that read UP inside a short up-window on a flapping host, caught only by the close re-read. For months the
discipline had bounded DOWN claims while UP claims shipped unbounded. Rules 7–8 close that gap.

## Self-reference

This file shows the template's own placeholder discipline at work: the source skill names real addresses and real
machines, and this copy ships none of them. Compare `skill_l1_upgrade.md` Step 3, which lost its overlay literal in
the same release for the same reason.

## Related

- [[pattern_channel_proof]] — the proof half (who gets to say a channel works).
- [[skill_l1_upgrade]] — joins a node to the mesh; this skill governs what you claim about it afterwards.
