---
name: flosum-source-pull
description: Pull Salesforce metadata from a Flosum repository branch to a local directory.
  Use when starting work on a branch, syncing local changes with remote, or retrieving
  tagged snapshots.
metadata:
  triggers:
  - pull from flosum
  - flosum source pull
  - download metadata flosum
  - sync local flosum
  - retrieve flosum branch
---

# Flosum CLI — Pull Source from a Branch

---

## Basic pull

```bash
sfdx flosum:source:pull \
  --repository <repo-name> \
  --branch <branch-name> \
  --targetpath ./force-app \
  --targetusername <org-alias>
```

| Flag | Short | Description |
|---|---|---|
| `--repository` | `-r` | **Required.** Repository name in Flosum |
| `--branch` | `-b` | **Required.** Branch to pull from |
| `--targetpath` | `-p` | **Required.** Local destination folder |
| `--targetusername` | `-u` | SFDX org alias |
| `--clean` | | Delete local files not present on the remote branch before pulling |
| `--tag` | `-t` | Pull a specific tagged snapshot instead of HEAD |
| `--debug` | `-d` | Print verbose debug output |
| `--json` | | Output result as JSON |

---

## Pull and clean (overwrite local)

Removes local metadata not present in the branch before downloading — useful for a fresh sync:

```bash
sfdx flosum:source:pull \
  --repository <repo-name> \
  --branch <branch-name> \
  --targetpath ./force-app \
  --targetusername <org-alias> \
  --clean
```

> ⚠️ Commit or stash any local changes before using `--clean` to avoid data loss.

---

## Pull a tagged snapshot

Flosum supports tagging branch states (similar to Git tags). Pull a specific tag with:

```bash
sfdx flosum:source:pull \
  --repository <repo-name> \
  --branch <branch-name> \
  --targetpath ./force-app \
  --targetusername <org-alias> \
  --tag <tag-name>
```

---

## Workflow: start working on a branch

```bash
# 1. Ensure the branch exists (clone if not local yet)
sfdx flosum:branch:clone \
  -r <repo-name> \
  -b <branch-name> \
  -p ./work \
  -u <org-alias>

# 2. Pull the latest state
sfdx flosum:source:pull \
  -r <repo-name> \
  -b <branch-name> \
  -p ./work \
  -u <org-alias> \
  --json

# 3. Make your changes locally …

# 4. Push back (see flosum-source-push skill)
```

---

## Workflow: refresh before pushing

Always pull before pushing to catch conflicts early:

```bash
sfdx flosum:source:pull \
  -r <repo-name> \
  -b <branch-name> \
  -p ./force-app \
  -u <org-alias>

# Review diffs, resolve manually if needed, then push
sfdx flosum:source:push \
  -s ./force-app \
  -r <repo-name> \
  -b <branch-name> \
  -u <org-alias>
```

---

## Troubleshooting

| Error | Fix |
|---|---|
| `Branch not found` | Verify with `flosum:repository:list` and `flosum:branch:clone` |
| `Target path permission denied` | Check write permissions on the target directory |
| Empty pull (no files) | Confirm the branch has committed metadata in Flosum |
| `Authentication error` | Re-run the `flosum-auth` skill |
