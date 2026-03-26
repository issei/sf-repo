---
name: flosum-repo
description: List Flosum repositories and clone a repository (or a specific branch)
  to a local directory. Use before branch or source operations when working with a
  repo for the first time.
metadata:
  triggers:
  - list flosum repositories
  - clone flosum repo
  - flosum repository
  - clone repository flosum
---

# Flosum CLI — Repository Operations

---

## List repositories

Returns all repositories available in the Flosum org:

```bash
sfdx flosum:repository:list \
  --targetusername <org-alias> \
  --json
```

The JSON output contains each repository's `name` and internal Salesforce `id`. **Note the repository name exactly** — it is required for all subsequent branch and source commands.

---

## Clone a repository (default branch)

Clones the repository's default/master branch into a local target folder:

```bash
sfdx flosum:repository:clone \
  --repository <repo-name> \
  --targetpath ./local-repo \
  --targetusername <org-alias>
```

| Flag | Description |
|---|---|
| `-r` / `--repository` | Repository name (required) |
| `-p` / `--targetpath` | Local destination folder (required) |
| `-u` / `--targetusername` | SFDX org alias (required) |
| `--default-structure` | Auto-create the standard `force-app/main/default` folder layout |
| `--json` | Output as JSON (useful in CI) |

---

## Clone a specific branch directly

To clone a specific branch instead of the default, use `flosum:branch:clone`:

```bash
sfdx flosum:branch:clone \
  --repository <repo-name> \
  --branch <branch-name> \
  --targetpath ./local-branch \
  --targetusername <org-alias>
```

See the `flosum-branch` skill for full branch management options.

---

## Recommended post-clone steps

After cloning, validate that the Salesforce DX project structure is intact:

```bash
# 1. Confirm sfdx-project.json exists
ls ./local-repo/sfdx-project.json

# 2. (Optional) scan for metadata issues
sfdx force:source:status --targetusername <org-alias>
```

---

## Full example

```bash
# 1. List repos to confirm the name
sfdx flosum:repository:list -u flosum-dev --json

# 2. Clone the desired repo
sfdx flosum:repository:clone \
  -r "MyApp" \
  -p ./myapp \
  -u flosum-dev \
  --default-structure

# 3. Enter the directory
cd ./myapp
```

---

## Troubleshooting

| Error | Fix |
|---|---|
| `Repository not found` | Run `repository:list` and copy the exact name |
| `Target path already exists` | Use a new folder name or delete the existing one first |
| `Authentication error` | Run the `flosum-auth` skill first |
