---
name: flosum-branch
description: Create a new Flosum branch, clone an existing branch to local, or inspect
  branches inside a repository. Use for feature branch workflows, hotfix branching,
  and release branching.
metadata:
  triggers:
  - create flosum branch
  - clone flosum branch
  - new branch flosum
  - flosum branch management
  - list flosum branches
---

# Flosum CLI — Branch Management

---

## Create a new branch

Creates a new branch inside a Flosum repository (remote):

```bash
sfdx flosum:branch:create \
  --repository <repo-name> \
  --branch <new-branch-name> \
  --targetpath ./local-branch \
  --targetusername <org-alias>
```

| Flag | Description |
|---|---|
| `-r` / `--repository` | Repository name (required) |
| `-b` / `--branch` | New branch name (required) |
| `-p` / `--targetpath` | Local folder to initialise with branch content (required) |
| `-s` / `--default-structure` | Auto-create `force-app/main/default` folder structure |
| `-u` / `--targetusername` | SFDX org alias (required) |
| `--json` | Output as JSON |

### Naming conventions

Adopt a consistent naming pattern so Devin can identify branch purpose automatically:

| Type | Pattern | Example |
|---|---|---|
| Feature | `feature/<ticket>-<slug>` | `feature/ABC-42-lead-conversion` |
| Hotfix | `hotfix/<ticket>-<slug>` | `hotfix/INC-7-null-pointer` |
| Release | `release/<version>` | `release/2024.Q4.1` |

---

## Clone an existing branch

Downloads an existing Flosum branch to a local directory:

```bash
sfdx flosum:branch:clone \
  --repository <repo-name> \
  --branch <branch-name> \
  --targetpath ./local-branch \
  --targetusername <org-alias>
```

Same flags as `branch:create` apply. Use `--default-structure` if the local folder is empty.

---

## List branches

Flosum does not expose a standalone `branch:list` CLI command. Use the repository list to identify branches, or query the Flosum org via SOQL:

```bash
sfdx force:data:soql:query \
  --query "SELECT Id, Name, Branch_Name__c FROM FlosumRepository__c WHERE Name = '<repo-name>'" \
  --targetusername <org-alias>
```

> **Tip:** Branch names are also visible in the Flosum UI under the repository record.

---

## After creating / cloning a branch

Pull the latest metadata into the local folder:

```bash
sfdx flosum:source:pull \
  --repository <repo-name> \
  --branch <branch-name> \
  --targetpath ./local-branch \
  --targetusername <org-alias>
```

See the `flosum-source-pull` skill for full pull options.

---

## Typical feature branch workflow

```bash
# 1. Create branch from the Flosum UI or CLI
sfdx flosum:branch:create \
  -r "MyApp" \
  -b "feature/ABC-42-lead-conversion" \
  -p ./feature-branch \
  -u flosum-dev \
  --default-structure

# 2. Pull current state
sfdx flosum:source:pull \
  -r "MyApp" \
  -b "feature/ABC-42-lead-conversion" \
  -p ./feature-branch \
  -u flosum-dev

# 3. Make changes locally …

# 4. Push changes back
sfdx flosum:source:push \
  -s ./feature-branch \
  -r "MyApp" \
  -b "feature/ABC-42-lead-conversion" \
  -u flosum-dev

# 5. Merge via the Flosum UI (PR / merge request)
```

---

## Troubleshooting

| Error | Fix |
|---|---|
| `Branch already exists` | Use `branch:clone` to download the existing branch |
| `Repository not found` | Run `flosum:repository:list` to verify the exact repo name |
| `Target path not empty` | Provide a new empty folder or delete the existing one |
