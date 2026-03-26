---
name: flosum-snapshot
description: Create a Flosum org snapshot before a risky deployment or at a release
  milestone. Snapshots serve as rollback points. Use before promoting to UAT or Production.
metadata:
  triggers:
  - flosum snapshot
  - create flosum snapshot
  - rollback flosum
  - org snapshot flosum
  - backup flosum org
---

# Flosum CLI — Org Snapshots

A **Flosum Snapshot** captures the full metadata state of an org at a point in time and stores it in your Flosum repository. If a deployment causes issues, you can restore from the snapshot.

> **Note:** The `flosum-sfdx-plugin` does not expose a dedicated `snapshot:create` CLI command. Snapshots are managed through the **Flosum UI** or by tagging a branch state via the CLI. This skill covers both paths.

---

## Option A — Snapshot via CLI (tag the branch)

Flosum supports tagging branch states. Tag the current branch HEAD as a snapshot reference:

```bash
# 1. Pull the current org state into a local folder
sfdx flosum:source:pull \
  --repository <repo-name> \
  --branch <branch-name> \
  --targetpath ./snapshot-$(date +%Y%m%d) \
  --targetusername <org-alias>

# 2. Push it back with a timestamp tag
sfdx flosum:source:push \
  --sourcepath ./snapshot-$(date +%Y%m%d) \
  --repository <repo-name> \
  --branch <branch-name> \
  --targetusername <org-alias> \
  --tag "snapshot-$(date +%Y%m%d-%H%M)" \
  --json
```

The `--tag` flag stores a named reference that can be retrieved with `flosum:source:pull --tag <tag-name>`.

---

## Option B — Snapshot via Flosum UI

1. Navigate to **Flosum → Repositories → [Your Repo]**.
2. Select the branch to snapshot.
3. Click **Create Snapshot** (or **Tag Branch** depending on your Flosum version).
4. Provide a meaningful label, e.g. `pre-release-2024.Q4.1`.
5. Save.

---

## Restore from a snapshot

```bash
sfdx flosum:source:pull \
  --repository <repo-name> \
  --branch <branch-name> \
  --targetpath ./restore-working \
  --targetusername <org-alias> \
  --tag <snapshot-tag-name>
```

Then deploy the restored files to the target org:

```bash
sfdx force:source:deploy \
  --sourcepath ./restore-working \
  --testlevel RunLocalTests \
  --targetusername <target-org-alias>
```

---

## Pre-deployment snapshot checklist

Run this routine before every UAT or Production promotion:

```bash
#!/bin/bash
set -e

REPO="MyApp"
BRANCH="release/2024.Q4.1"
ORG="flosum-prod"
TAG="pre-deploy-$(date +%Y%m%d-%H%M)"
SNAPSHOT_DIR="./snapshots/$TAG"

mkdir -p "$SNAPSHOT_DIR"

# Pull current state
sfdx flosum:source:pull \
  -r "$REPO" \
  -b "$BRANCH" \
  -p "$SNAPSHOT_DIR" \
  -u "$ORG"

# Tag it
sfdx flosum:source:push \
  -s "$SNAPSHOT_DIR" \
  -r "$REPO" \
  -b "$BRANCH" \
  -u "$ORG" \
  --tag "$TAG" \
  --json

echo "✅ Snapshot saved: $TAG"
echo "   Restore with: sfdx flosum:source:pull -r $REPO -b $BRANCH -p ./restore -u $ORG --tag $TAG"
```

---

## Snapshot naming convention

| Scenario | Tag pattern | Example |
|---|---|---|
| Pre-deployment | `pre-deploy-YYYYMMDD-HHMM` | `pre-deploy-20241105-1430` |
| Release milestone | `release-<version>` | `release-2024.Q4.1` |
| Hotfix rollback point | `pre-hotfix-<ticket>` | `pre-hotfix-INC-7` |

---

## Troubleshooting

| Error | Fix |
|---|---|
| `--tag` flag not recognised | Verify `flosum-sfdx-plugin` version (`sfdx plugins --core`) and update if needed |
| Pull returns empty folder | The branch may not contain committed metadata — push to it first |
| Restore deployment fails | Review Apex test errors; the snapshot may include incompatible dependencies |
