---
name: flosum-setup
description: Install and verify all prerequisites for the flosum-sfdx-plugin. Use
  this before any other Flosum CLI skill or when setting up a fresh machine/CI environment.
metadata:
  triggers:
  - setup flosum
  - install flosum plugin
  - configure flosum cli
  - flosum prerequisites
---

# Flosum CLI — Setup & Prerequisites

Use this skill to install `flosum-sfdx-plugin` and validate the environment before running any other Flosum CLI command.

---

## Step 1 — Verify Node.js (18+)

```bash
node --version
```

If the version is below 18, install the LTS release:

```bash
# macOS (Homebrew)
brew install node

# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

## Step 2 — Install or update Salesforce CLI

```bash
npm install -g sfdx-cli
sfdx --version
```

Expected output example: `sfdx-cli/7.x.x …`

---

## Step 3 — Install flosum-sfdx-plugin

```bash
npm install -g flosum-sfdx-plugin
```

Verify the plugin is registered:

```bash
sfdx plugins --core
```

Look for `flosum-sfdx-plugin` in the list.

---

## Step 4 — Confirm available Flosum commands

```bash
sfdx flosum --help
```

Expected top-level topics:

| Topic | Purpose |
|---|---|
| `flosum:auth` | Org authentication |
| `flosum:repository` | Repository operations |
| `flosum:branch` | Branch management |
| `flosum:source` | Push / pull metadata |

---

## Step 5 — Smoke test (optional)

```bash
sfdx flosum:repository:list --json --targetusername <your-org-alias>
```

A successful JSON response confirms the plugin is working end-to-end.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `command not found: sfdx` | Re-run `npm install -g sfdx-cli` and reload the shell |
| `flosum` topic missing from `sfdx --help` | Re-run `npm install -g flosum-sfdx-plugin` |
| Permission errors on global install | Use `sudo npm install -g …` or configure npm prefix |
| Plugin version conflict | `npm install -g flosum-sfdx-plugin@latest` to force update |
