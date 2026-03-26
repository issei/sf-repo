---
name: flosum-source-push
description: Push local Salesforce metadata from a source folder to a Flosum repository
  branch. Use after making local changes that need to be committed back to Flosum
  version control.
metadata:
  triggers:
  - push to flosum
  - flosum source push
  - upload metadata flosum
  - commit changes flosum
  - push metadata flosum branch
---

# Flosum CLI — Push Source to a Branch

---

## Basic push

```bash
sfdx flosum:source:push \
  --sourcepath ./force-app \
  --repository <repo-name> \
  --branch <branch-name> \
  --targetusername <org-alias>
```

| Flag | Short | Description |
|---|---|---|
| `--sourcepath` | `-s` | **Required.** Path to the source folder containing Salesforce metadata |
| `--repository` | `-r` | Repository name in Flosum |
| `--branch` | `-b` | Target branch name |
| `--targetusername` | `-u` | SFDX org alias |
| `--sync` | | Delete remote components that no longer exist locally (destructive push) |
| `--custom-path` | `-c` | Use `--sourcepath` as-is without auto-appending the repo/branch path segments |
| `--debug` | `-d` | Print verbose debug output |
| `--timestamp` | `-t` | Internal: override the send timestamp (leave unset normally) |
| `--json` | | Output result as JSON |

---

## Push with sync (destructive changes)

Removes from the remote branch any components that are not present in the local source:

```bash
sfdx flosum:source:push \
  --sourcepath ./force-app \
  --repository <repo-name> \
  --branch <branch-name> \
  --targetusername <org-alias> \
  --sync
```

> ⚠️ **Warning:** `--sync` is destructive. Run `flosum:source:pull` first and diff locally before using this flag.

---

## Push a custom path

When the source folder does not follow the standard `force-app/main/default` layout:

```bash
sfdx flosum:source:push \
  --sourcepath /absolute/path/to/metadata \
  --repository <repo-name> \
  --branch <branch-name> \
  --targetusername <org-alias> \
  --custom-path
```

---

## Pre-push checklist

Run these steps before pushing to catch issues early:

```bash
# 1. Validate Apex compilation (optional but recommended)
sfdx force:source:deploy \
  --sourcepath ./force-app \
  --checkonly \
  --testlevel RunLocalTests \
  --targetusername <sandbox-alias>

# 2. Check source status
sfdx force:source:status --targetusername <sandbox-alias>

# 3. Push to Flosum branch
sfdx flosum:source:push \
  -s ./force-app \
  -r <repo-name> \
  -b <branch-name> \
  -u <org-alias> \
  --json
```

---

## CI/CD example

```bash
#!/bin/bash
set -e

ORG="flosum-ci"
REPO="MyApp"
BRANCH="${GITHUB_HEAD_REF:-feature/default}"

# Authenticate (JWT)
sfdx auth:jwt:grant \
  --alias "$ORG" \
  --clientid "$FLOSUM_CLIENT_ID" \
  --jwtkeyfile "$FLOSUM_KEY_PATH" \
  --username "$FLOSUM_USERNAME" \
  --instanceurl "$FLOSUM_INSTANCE_URL"

# Push
sfdx flosum:source:push \
  --sourcepath ./force-app \
  --repository "$REPO" \
  --branch "$BRANCH" \
  --targetusername "$ORG" \
  --json
```

---

## Troubleshooting

| Error | Fix |
|---|---|
| `Source path does not exist` | Confirm `--sourcepath` points to an existing directory |
| `Branch not found` | Create the branch first with `flosum:branch:create` |
| `Authentication error` | Re-run the `flosum-auth` skill |
| Push succeeds but no changes visible | Verify the branch name matches exactly (case-sensitive) |
