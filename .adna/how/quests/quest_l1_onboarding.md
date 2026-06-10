---
quest_id: quest_l1_onboarding
type: side_quest
title: "L0→L1 Compute Upgrade — Self-Service Onboarding"
difficulty: easy
estimated_token_cost: ~3K
model_requirements: "any (with shell access)"
status: active
created: 2026-03-22
updated: 2026-04-06
last_edited_by: agent_init
tags: [side_quest, onboarding, l1, compute, deployment]
---

# Quest: L0→L1 Compute Upgrade

## Objective

Upgrade your aDNA vault (L0) to an L1 compute node with JupyterHub. By the end, you'll have a working L1 node running locally and connected to the Lattice network for fleet operations and collaborative compute.

This quest walks through the user-side steps. An admin handles the provisioning — you just need to prepare your machine and provide SSH access.

## Prerequisites

- Mac with Apple Silicon (arm64) — `uname -m` should return `arm64`
- macOS 14.0+ — `sw_vers --productVersion`
- Python 3.12+ — `python3 --version`
- npm installed — `npm --version`
- ~10GB free disk space — `df -h ~`
- Ports 8000 and 8100 free — `lsof -i :8000 2>/dev/null; lsof -i :8100 2>/dev/null`

## Steps

### Phase 1: Preflight (~2 min)

Run the preflight checks and record results:

```bash
echo "=== L1 Preflight ==="
echo "Architecture: $(uname -m)"
echo "macOS: $(sw_vers --productVersion)"
echo "Python: $(python3 --version 2>&1)"
echo "npm: $(npm --version 2>&1)"
echo "Disk free: $(df -h ~ | tail -1 | awk '{print $4}')"
lsof -i :8000 2>/dev/null && echo "WARN: port 8000 in use" || echo "OK: port 8000 free"
lsof -i :8100 2>/dev/null && echo "WARN: port 8100 in use" || echo "OK: port 8100 free"
```

**If Python < 3.12**: `brew install python@3.12`
**If npm missing**: `brew install node`
**If ports in use**: identify the process with `lsof -i :<port>` and stop it.

All checks must pass before continuing.

### Phase 2: Acquire latlab (~5 min)

Choose the path that matches your access:

**Path A — Self-service GitHub clone (if you have repo access)**:
```bash
mkdir -p ~/aDNA && cd ~/aDNA
git clone https://github.com/LatticeProtocol/latlab.git
```

> If you get a 404 or permission error, ask a Lattice admin for a collaborator invite to `LatticeProtocol/latlab`, or use Path B.

Skip to **Phase 3** (Run Setup).

**Path B — Admin push via SSH (no GitHub access needed)**:

The admin pushes the code to your machine remotely. You need to:

1. **Enable Remote Login**: System Settings → General → Sharing → Remote Login → ON
   ```bash
   ssh localhost echo "SSH works"
   ```

2. **Expose SSH** — pick one:

   | Method | Command | Notes |
   |--------|---------|-------|
   | **Cloudflare Quick Tunnel** (recommended) | `brew install cloudflared && cloudflared tunnel --url ssh://localhost:22` | Zero config, temporary URL |
   | **ngrok** | `ngrok tcp 22` | Simple, raw TCP forwarding |
   | **Nebula** | `brew install nebula` + deploy cert bundle | Persistent mesh, requires admin cert bundle |

   > **Important**: Nebula cert files must be `chmod 600` (owner-only). The daemon won't start with world-readable certs.

3. **Share with your Lattice admin**: SSH access URL, your macOS username (`whoami`), and confirmation that preflight passed.

4. The admin runs:
   ```bash
   setup_l1_remote.sh <your_ssh_alias> --push-repos full
   ```

**Wait for admin confirmation** that the push completed.

### Phase 3: Run Setup (~5 min)

```bash
cd ~/aDNA/latlab
bash deploy/native/setup_l1.sh
```

This is idempotent and handles: Python venv, JupyterHub + proxy, LatLab SDK, NativeAuth config, and JupyterHub config generation.

### Phase 4: Verify Your L1 (~3 min)

```bash
# Run the health check
bash ~/aDNA/latlab/deploy/native/latlab_doctor.sh

# Start JupyterHub
bash ~/aDNA/latlab/deploy/native/latlab_start.sh
```

Open `http://127.0.0.1:8000` in your browser. You should see the JupyterHub login page.

**First login**: Use NativeAuth signup to create a local account.

### Phase 5: Register with the Lattice Network (~5 min)

Once your L1 is running, register it with the Lattice to join the network.

1. **Get a bootstrap token** from a Lattice admin (they generate it from HQ Dashboard)
2. **Register your node**:
   ```bash
   BOOTSTRAP_TOKEN="<paste token from admin>"
   ADMIN_HQ="http://<admin_node_ip>:8000"

   curl -s -X POST "$ADMIN_HQ/api/v1/nodes/register" \
     -H "Authorization: Bearer $BOOTSTRAP_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "'$(hostname -s)'",
       "tier": "L1",
       "capabilities": ["compute_cpu"]
     }'
   ```
3. **Save your credentials** — the response contains your node **DID** and **API key** (shown once)
4. **Wait for admin approval** — the admin approves your node from the HQ Dashboard
5. **Retrieve HMAC key** (after approval):
   ```bash
   curl -s -X POST "$ADMIN_HQ/api/v1/nodes/credentials" \
     -H "X-API-Key: <your_api_key>"
   ```

Your node starts at **limited trust** and can pull lattices. Trust increases as you participate.

> **Alternative**: If you have HQ Dashboard access, you can also register through the web UI at `http://127.0.0.1:8000` → Cluster page.

### Phase 6: Submit Your Result

Create a result file and submit via PR:

```bash
# From the aDNA repo
cat > how/quests/results/result_l1_onboarding_$(whoami).md << 'EOF'
---
quest_id: quest_l1_onboarding
type: quest_result
submitted_by: <your_name>
model_used: <model>
timestamp: <ISO timestamp>
status: complete
---

# Result: L1 Onboarding

## Preflight Output
<paste Phase 1 output>

## Doctor Output
<paste Phase 4 doctor output>

## Verification
- [ ] JupyterHub login page loads at http://127.0.0.1:8000
- [ ] NativeAuth signup + login works
- [ ] latlab_doctor.sh shows 0 FAIL
- [ ] Node registered with Lattice network (DID received)

## Notes
<any observations, issues encountered, or suggestions>
EOF
```

## What's Next

After completing this quest, you can continue with advanced phases from `how/skills/skill_l1_upgrade.md`:

- **Mesh connectivity**: Nebula overlay network for peer-to-peer access (Phase 2)
- **Federation relay**: Remote admin access via L2 relay (Phase 3)
- **Full compliance**: TLS + HMAC for production security (Phase 4)

## Related

- `how/skills/skill_l1_upgrade.md` — the full 4-phase upgrade guide (this quest covers Phase 1)
- `what/docs/adna_standard.md` — the aDNA knowledge architecture
- `CONTRIBUTING.md` — how to submit PRs to the aDNA repo
