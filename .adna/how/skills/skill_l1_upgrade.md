---
type: skill
skill_type: agent
created: 2026-03-21
updated: 2026-05-11
status: active
category: deployment
trigger: "User asks about compute, L1, JupyterHub, or 'upgrade to L1'"
last_edited_by: agent_stanley
tags: [skill, deployment, l1, compute, upgrade]
preflight_script: how/skills/l1_upgrade/prepare_for_onboarding.sh  # added M03 Session 2 B2 per Operator Decision 1 Option A (script relocated from outer adna/ to its skill home)

requirements:
  tools: [bash, file_read, file_write]
  context: ["CLAUDE.md", "MANIFEST.md"]
  permissions: ["run shell commands", "write config files"]
---

# Skill: L1 Compute Upgrade

## Overview

Phased upgrade path from an aDNA vault (L0) to an L1 compute node with JupyterHub. Each phase is self-contained — the user gets value at every stop. An agent reads this skill and executes each phase interactively, confirming before each step.

**Outcome**: JupyterHub running locally → mesh connectivity → federation relay → full compliance.

**Pre-flight script** (added M03 Session 2 — campaign_adna_v2_infrastructure v7.0): `how/skills/l1_upgrade/prepare_for_onboarding.sh` checks macOS version + Homebrew PATH + Python ≥ 3.12 + npm + disk space + port availability before any L1 install steps. Run as the first thing inside Phase 1 (or as a standalone pre-check by the operator). The script lives co-located with this skill per ADR-006/ADR-007 + Obj 5 P-1 directory-move resolution (operator-discretionary location chosen at M03 S2 entry).

## Workspace Awareness

If this aDNA vault is part of a multi-project workspace (a workspace-level CLAUDE.md exists at the parent directory):

1. **Before Phase 1**: Check the workspace CLAUDE.md's `compute_tier` field. If it already says `L1`, confirm with the user whether they want to re-run the upgrade or are upgrading a different project.
2. **After Phase 1 completes**: Update the workspace CLAUDE.md's `compute_tier` from `L0` to `L1`. Note the presence of `latlab/` as a workspace peer.
3. **After Phase 2 completes**: Update the workspace CLAUDE.md to note mesh connectivity status.
4. **After Phase 3 completes**: Update the workspace CLAUDE.md to note federation relay access.

If no workspace CLAUDE.md exists at the parent, skip these updates silently.

**Workspace layout**: After L1 upgrade, `latlab/` should live as a peer directory to this vault (e.g., `~/aDNA/latlab/`), not inside it. The admin push or self-service install places repos at the workspace level.

## Trigger

User mentions compute participation, L1, JupyterHub, or asks "how do I run workloads?" in an aDNA vault context.

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `target_phase` | No | 1 | Which phase to reach (1-4). Most users start at Phase 1. |

---

## Phase 1 — Local L1 (~10 min, zero network dependency)

**Goal**: JupyterHub running at `http://127.0.0.1:8000` on the local machine.

### Step 1: Preflight Checks

Run each check and report results before proceeding:

```bash
# Architecture
uname -m  # Must be arm64

# macOS version
sw_vers --productVersion  # 14.0+ recommended

# Python
python3 --version  # ≥3.12 required

# npm (for JupyterHub configurable-http-proxy)
npm --version  # Any recent version

# Disk space
df -h ~  # Need ~10GB free

# Port availability
lsof -i :8000 2>/dev/null && echo "WARN: port 8000 in use" || echo "OK: port 8000 free"
lsof -i :8100 2>/dev/null && echo "WARN: port 8100 in use" || echo "OK: port 8100 free"
```

**If Python < 3.12**: `brew install python@3.12` (Homebrew, not system Python).
**If npm missing**: `brew install node`.
**If ports in use**: Identify the process (`lsof -i :8000`) and ask user whether to stop it.

### Step 2: Acquire latlab Repository

The `latlab` repo contains all deployment scripts and the LatLab SDK. It is a private repo hosted at `LatticeProtocol/latlab`.

Pick the path that matches your access level:

**Path A — Self-service GitHub clone (recommended if you have repo access)**:
```bash
mkdir -p ~/aDNA && cd ~/aDNA
git clone https://github.com/LatticeProtocol/latlab.git
ls latlab/deploy/native/setup_l1.sh && echo "latlab acquired" || echo "clone failed"
```

If you have a GitHub SSH key configured:
```bash
git clone git@github.com:LatticeProtocol/latlab.git
```

> **Note**: Requires GitHub access to the `LatticeProtocol/latlab` private repo. Ask a Lattice admin for a collaborator invite if you get a 404 or permission error.

**Path B — Admin push via SSH (no GitHub access needed on your machine)**:
An admin pushes latlab to the target machine using:
```bash
# Run by admin on their machine:
setup_l1_remote.sh <target_ssh_alias> --push-repos full
```

This rsyncs the latlab repo to `~/aDNA/latlab/` on the target.

**If latlab is already present** (admin previously pushed or already cloned):
```bash
ls ~/aDNA/latlab/deploy/native/setup_l1.sh && echo "latlab present" || echo "latlab not found"
```

If present, pull latest before running setup:
```bash
cd ~/aDNA/latlab && git pull
```

**If no access via either path**: Ask a Lattice admin for a GitHub collaborator invite to `LatticeProtocol/latlab`, or arrange an admin SSH push (Path B).

### Step 3: Run Setup

```bash
cd ~/aDNA/latlab
bash deploy/native/setup_l1.sh
```

This script is idempotent and handles:
- Python venv creation at `~/.latlab/venv/`
- JupyterHub + configurable-http-proxy installation
- LatLab SDK installation (extensions, HQ dashboard)
- NativeAuth configuration
- JupyterHub config generation

### Step 4: Verify

```bash
bash ~/aDNA/latlab/deploy/native/latlab_doctor.sh
```

All checks should show PASS or WARN. No FAIL is acceptable.

### Step 5: Start JupyterHub

```bash
bash ~/aDNA/latlab/deploy/native/latlab_start.sh
```

### Step 6: Confirm

Open `http://127.0.0.1:8000` in a browser. You should see the JupyterHub login page.

**First login**: Use NativeAuth signup to create a local account. `allow_all = True` is the default for L1 — any created account can log in.

**Phase 1 complete.** The user now has a working L1 compute node with local-only access. Continue to Step 7 to register with the Lattice network, or stop here if standalone operation is sufficient.

### Step 7: Register with the Lattice Network (API-first onboarding)

Once JupyterHub is running, register this node with the Lattice admin to join the network. This uses the API-first progressive trust onboarding flow.

**What you need from the admin**:
- A **bootstrap JWT token** — the admin generates this from the HQ Dashboard (`POST /api/admin/nodes/bootstrap-tokens`)

**Register your node**:
```bash
# The admin provides the bootstrap token
BOOTSTRAP_TOKEN="<paste token from admin>"

# Register with the admin's L1/L2 HQ endpoint
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

This returns your node's **DID** (decentralized identifier) and **API key**. Save both — the API key is shown only once.

**After registration**:
1. The admin approves your node (`POST /api/admin/nodes/{did}/approve`)
2. Once approved, retrieve your HMAC credential: `POST /api/v1/nodes/credentials` with your API key
3. Your node starts at **limited trust** (trust score ~0.35) — you can pull lattices and read, but not publish
4. Trust upgrades happen as you participate in the network (verified → full trust)

> **Self-service users (Path A)**: If you cloned latlab yourself, you can also register through the HQ Dashboard web UI at `http://127.0.0.1:8000` after login — navigate to the Cluster page.

**Phase 1 complete.** Continue to Phase 2 for mesh connectivity, or operate as an API-connected node over the public internet.

---

## Phase 2 — Mesh Connectivity (~5 min, Nebula cert bundle required)

**Goal**: Peer-to-peer connectivity to all Lattice nodes via Nebula overlay mesh.

**Prerequisite**: Lattice admin provides a Nebula certificate bundle (ca.crt, node.crt, node.key, config.yml).

### Step 1: Install Nebula

```bash
brew install nebula
```

### Step 2: Deploy Certificate Bundle

```bash
sudo mkdir -p /opt/homebrew/etc/nebula/pki
sudo cp ~/nebula/pki/{ca.crt,<node_name>.crt,<node_name>.key} /opt/homebrew/etc/nebula/pki/
sudo cp ~/nebula/config.yml /opt/homebrew/etc/nebula/config.yml
sudo chmod 700 /opt/homebrew/etc/nebula/pki
sudo chmod 600 /opt/homebrew/etc/nebula/pki/*
sudo chmod 600 /opt/homebrew/etc/nebula/config.yml
```

### Step 3: Start Nebula and Verify

```bash
# Start the daemon
sudo /opt/homebrew/bin/nebula -config /opt/homebrew/etc/nebula/config.yml &

# Verify lighthouse connectivity
ping -c 2 10.42.0.1
```

Report the assigned overlay IP (10.42.0.x — shown in config.yml) to the Lattice admin for state file registration.

### Step 4: Install Persistent Daemon

```bash
sudo cp ~/nebula/net.defined.nebula.plist /Library/LaunchDaemons/
sudo launchctl load /Library/LaunchDaemons/net.defined.nebula.plist
```

**Phase 2 complete.** The node is now reachable from any other node on the Lattice mesh. JupyterHub is still local-only (listening on 127.0.0.1) — this is intentional for security.

---

## Phase 3 — Federation Relay (~10 min, admin action required)

**Goal**: Admin can reach this node through the L2 relay via SSH tunnel, enabling remote management and fleet operations.

### Step 1: Generate SSH Deploy Key

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_latlab -C "latlab-deploy@$(hostname -s)"
cat ~/.ssh/id_ed25519_latlab.pub
```

Send the public key to the Lattice admin (Slack, email, or coordination file in vault).

### Step 2: Admin Actions (performed by admin)

The admin will:
1. Install the pubkey on the L2 relay (`authorized_keys`)
2. Allocate a relay port (convention: 22222 + node_index)
3. Confirm the port assignment

### Step 3: Configure SSH

Once the admin confirms the port, add to `~/.ssh/config`:

```
Host latlab-relay
    HostName <l2_nebula_ip_or_hostname>
    User <l2_username>
    IdentityFile ~/.ssh/id_ed25519_latlab
    ServerAliveInterval 30
    ServerAliveCountMax 3
```

Test connectivity:
```bash
ssh latlab-relay echo "Relay connection OK"
```

### Step 4: Set Up Persistent Reverse Tunnel

Create a launchd agent for persistent reverse tunnel to L2:

```bash
# The admin provides the allocated port (e.g., 22224)
RELAY_PORT=22224

cat > ~/Library/LaunchAgents/com.lattice.tunnel.plist << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.lattice.tunnel</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/ssh</string>
        <string>-N</string>
        <string>-R</string>
        <string>RELAY_PORT:localhost:22</string>
        <string>latlab-relay</string>
    </array>
    <key>KeepAlive</key>
    <true/>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>/tmp/lattice-tunnel.err</string>
</dict>
</plist>
PLIST

# Replace placeholder with actual port
sed -i '' "s/RELAY_PORT/$RELAY_PORT/" ~/Library/LaunchAgents/com.lattice.tunnel.plist

launchctl load ~/Library/LaunchAgents/com.lattice.tunnel.plist
```

### Step 5: Verify Relay Access

Admin confirms they can reach the node:
```bash
# Admin runs from their machine:
ssh -p <RELAY_PORT> <l2_host> echo "Reverse tunnel working"
```

**Phase 3 complete.** The admin can now reach this node through the L2 relay for fleet operations, updates, and troubleshooting.

---

## Phase 4 — Full Compliance (reference)

**Goal**: Production-grade security with NGINX TLS, HMAC signing, and trust enforcement.

This phase follows the Tier 2+ checklists in `skill_node_onboarding.md` (in your operational vault). The key additions:

1. **NGINX TLS** on port 8443 — self-signed cert via `generate_certs.sh`
2. **HMAC key** distributed via `secrets.json` — shared secret for object integrity
3. **Trust enforcement** set to `soft_enforce` — federation validates signatures
4. **OAuth token TTL** set to 24h — session expiry for security
5. **Connection event logging** — audit trail for compliance

**Estimated time**: ~30 minutes with admin assistance.

Refer to `skill_node_onboarding` in your operational vault for the complete Tier 2 and Tier 3 checklists.

---

## Gotchas

Hard-won lessons from fleet deployments:

### SSH PATH on macOS
SSH non-interactive commands only source `~/.zshenv`, NOT `.zprofile` or `.zshrc`. If admin will manage this node via SSH, create `~/.zshenv`:
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshenv
echo 'export PATH="$HOME/.latlab/venv/bin:$PATH"' >> ~/.zshenv
```

### Nebula Certificate Permissions
Cert files at `/opt/homebrew/etc/nebula/pki/` must be `chmod 600` (owner-only read). Nebula will refuse to start if certs are world-readable. The pki directory itself should be `chmod 700`.

### NGINX Config Paths (Phase 4)
On macOS with Homebrew, NGINX config is at `/opt/homebrew/etc/nginx/`, NOT `/etc/nginx/`. All deploy scripts account for this, but manual config edits need the correct path.

### Stale SSH Tunnel Sockets
If a tunnel dies ungracefully, the relay port may stay bound. On the L2 relay:
```bash
fuser -k <port>/tcp  # e.g., fuser -k 22224/tcp
```

### NativeAuth `allow_all`
L1 nodes default to `allow_all = True` in NativeAuth config. This means any NativeAuth-created account can log in. This is intentional for development nodes. For production/partner nodes, set `allow_all = False` and manage the allowed users list.

### Port 8100 (CHP Proxy)
JupyterHub's configurable-http-proxy listens on port 8100 (API) in addition to 8000 (public). Both must be free at startup.

---

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| JupyterHub running | Service | Local compute at `http://127.0.0.1:8000` |
| Nebula connected | Network | Mesh connectivity to Lattice overlay (10.42.0.x) |
| SSH relay tunnel | Network | Admin access via L2 relay |
| TLS + HMAC (Phase 4) | Security | Production compliance |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `setup_l1.sh` fails at venv | Wrong Python version or Homebrew conflict | Verify `python3 --version` ≥3.12, check `which python3` points to Homebrew |
| Port 8000 in use | Another service or stale Hub process | `lsof -i :8000`, kill the process, or use `latlab_stop.sh` |
| `latlab_doctor.sh` shows FAIL | Missing dependency or config | Read the FAIL message — doctor explains what's wrong and how to fix |
| Nebula fails to start | Bad cert permissions or wrong config path | Verify `chmod 600` on cert files, check `/opt/homebrew/etc/nebula/config.yml` exists |
| SSH tunnel won't connect | Firewall, wrong port, or stale socket | Check `fuser <port>/tcp` on relay, verify SSH config |
| NativeAuth login rejected | `allow_all = False` | Check JupyterHub config: `c.NativeAuthenticator.allow_all` |

## Related

- **aDNA Standard**: `what/docs/adna_standard.md` — the knowledge architecture this node extends
- **Machine Setup**: `skill_machine_setup.md` (operational vault) — base machine provisioning
- **Node Onboarding**: `skill_node_onboarding.md` (operational vault) — compliance tier checklists
- **Fleet Administration**: `skill_fleet_administration.md` (operational vault) — admin-side fleet ops
