---
name: flosum-deploy
description: End-to-end Flosum deployment workflow — validate locally, push to branch,
  promote via Flosum pipeline, and verify the result. Use when deploying a feature
  branch to a sandbox or production.
metadata:
  triggers:
  - deploy flosum
  - flosum deployment
  - promote flosum branch
  - release flosum
  - flosum ci cd
  - deploy to sandbox flosum
  - deploy to production flosum
---

# Flosum CLI — Deployment Workflow

Flosum deployments follow a three-stage pattern:

```
Local changes → Push to branch → Promote via pipeline (UI or API)
```

---

## Stage 1 — Validate metadata locally

Run a check-only deployment against a sandbox **before** pushing to Flosum:

```bash
sfdx force:source:deploy \
  --sourcepath ./force-app \
  --checkonly \
  --testlevel RunLocalTests \
  --targetusername <sandbox-alias> \
  --json
```

Only proceed to Stage 2 if this exits with code `0`.

---

## Stage 2 — Pull latest, then push to Flosum branch

Always pull the latest branch state before pushing to prevent overwriting others' changes:

```bash
# 2a. Pull latest
sfdx flosum:source:pull \
  --repository <repo-name> \
  --branch <branch-name> \
  --targetpath ./force-app \
  --targetusername <flosum-alias>

# 2b. Review any conflicts / diffs locally …

# 2c. Push changes
sfdx flosum:source:push \
  --sourcepath ./force-app \
  --repository <repo-name> \
  --branch <branch-name> \
  --targetusername <flosum-alias> \
  --json
```

---

## Stage 3 — Promote via Flosum pipeline

Flosum pipeline promotion (deployment to the next environment) is managed through the **Flosum UI** or the Flosum REST API. The CLI does not expose a `pipeline:promote` command.

### Via the Flosum UI

1. Navigate to **Flosum → Pipelines**.
2. Select the pipeline that includes your repository.
3. Click **Promote** on the branch to move it to the target org stage.
4. Monitor the deployment log for errors.

### Via the Flosum REST API (headless / CI)

```bash
# Example: trigger a pipeline stage using Salesforce REST
curl -X POST \
  "$FLOSUM_INSTANCE_URL/services/apexrest/flosum/pipeline/promote" \
  -H "Authorization: Bearer $(sfdx force:org:display --targetusername <flosum-alias> --json | jq -r '.result.accessToken')" \
  -H "Content-Type: application/json" \
  -d '{
    "repositoryName": "<repo-name>",
    "branchName": "<branch-name>",
    "targetStage": "<pipeline-stage-name>"
  }'
```

> Adapt the endpoint path to match your Flosum version. Check with your Flosum admin for the exact REST endpoint.

---

## Stage 4 — Post-deployment verification

```bash
# Confirm the Apex tests pass in the target org
sfdx force:apex:test:run \
  --testlevel RunLocalTests \
  --targetusername <target-org-alias> \
  --resultformat human \
  --wait 10
```

---

## Full CI script example

```bash
#!/bin/bash
set -e

FLOSUM_ORG="flosum-ci"
TARGET_ORG="sandbox-uat"
REPO="MyApp"
BRANCH="${BRANCH_NAME:-feature/default}"

# 1. Authenticate
sfdx auth:jwt:grant \
  --alias "$FLOSUM_ORG" \
  --clientid "$FLOSUM_CLIENT_ID" \
  --jwtkeyfile "$FLOSUM_KEY_PATH" \
  --username "$FLOSUM_USERNAME" \
  --instanceurl "$FLOSUM_INSTANCE_URL"

# 2. Validate
sfdx force:source:deploy \
  --sourcepath ./force-app \
  --checkonly \
  --testlevel RunLocalTests \
  --targetusername "$TARGET_ORG"

# 3. Pull + push
sfdx flosum:source:pull -r "$REPO" -b "$BRANCH" -p ./force-app -u "$FLOSUM_ORG"
sfdx flosum:source:push -s ./force-app -r "$REPO" -b "$BRANCH" -u "$FLOSUM_ORG" --json

echo "✅ Push complete. Promote via Flosum pipeline UI or API."
```

---

## Deployment checklist

- [ ] Validation check-only passed with `RunLocalTests`
- [ ] Pulled latest branch before pushing
- [ ] No destructive changes without explicit `--sync` review
- [ ] Pipeline stage target is correct (Sandbox / UAT / Production)
- [ ] Apex test coverage ≥ 75% in target org

---

## Troubleshooting

| Error | Fix |
|---|---|
| Check-only fails | Fix the reported Apex / metadata errors before pushing |
| Push succeeds but pipeline fails | Check Flosum deployment log; may be a profile/permission issue |
| `INSUFFICIENT_ACCESS` on REST API call | Verify the Connected App profile has API access |
| Tests fail post-deploy | Run `force:apex:test:run` in the target org to get full failure details |
