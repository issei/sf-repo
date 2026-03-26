---
name: flosum-auth
description: Authenticate an SFDX org that is connected to Flosum. Run this before
  any repository, branch, or source operation. Covers both interactive browser login
  and CI/CD non-interactive flows.
metadata:
  triggers:
  - authenticate flosum
  - login flosum org
  - flosum auth
  - connect flosum org
---

# Flosum CLI — Authenticate an Org

Flosum CLI reuses SFDX org authentication. An org that is already authenticated in SFDX can immediately be used with any `sfdx flosum:*` command via its alias.

---

## Option A — Interactive (browser) login

Best for developer workstations:

```bash
sfdx auth:web:login \
  --alias flosum-org \
  --instanceurl https://your-flosum-instance.my.salesforce.com
```

A browser window opens. Log in with your Flosum org credentials.

---

## Option B — JWT Bearer Flow (CI/CD / headless)

Required for pipelines, Devin, and servers that cannot open a browser.

### Prerequisites

1. A **Connected App** in the target org with the certificate uploaded.
2. A private key file (`.key`) on the machine.

### Command

```bash
sfdx auth:jwt:grant \
  --alias flosum-prod \
  --clientid <connected-app-consumer-key> \
  --jwtkeyfile /path/to/server.key \
  --username admin@yourorg.com \
  --instanceurl https://your-flosum-instance.my.salesforce.com
```

Use environment variables in CI to avoid hard-coding secrets:

```bash
sfdx auth:jwt:grant \
  --alias flosum-prod \
  --clientid "$FLOSUM_CLIENT_ID" \
  --jwtkeyfile "$FLOSUM_KEY_PATH" \
  --username "$FLOSUM_USERNAME" \
  --instanceurl "$FLOSUM_INSTANCE_URL"
```

---

## Option C — SFDX Auth URL (token-based handoff)

Useful when sharing auth between machines:

```bash
# Export on source machine
sfdx auth:sfdxurl:store --sfdxurlfile ./auth.url --alias flosum-org

# Import on target machine
sfdx auth:sfdxurl:authorize --sfdxurlfile ./auth.url --alias flosum-org
```

---

## Verify authentication

```bash
sfdx auth:list
```

Confirm the alias and the instance URL appear in the table.

Test Flosum connectivity specifically:

```bash
sfdx flosum:repository:list \
  --targetusername flosum-org \
  --json
```

A JSON array of repositories confirms full end-to-end access.

---

## Manage authenticated orgs

```bash
# Show details for one org
sfdx org:display --targetusername flosum-org

# Log out / remove an alias
sfdx auth:logout --targetusername flosum-org --noprompt
```

---

## Environment variable reference

| Variable | Usage |
|---|---|
| `SFDX_USE_GENERIC_UNIX_KEYCHAIN` | Set to `true` in Linux CI to bypass OS keyring |
| `FLOSUM_CLIENT_ID` | Connected App consumer key |
| `FLOSUM_KEY_PATH` | Path to JWT private key |
| `FLOSUM_USERNAME` | Org login username |
| `FLOSUM_INSTANCE_URL` | Org instance URL |

---

## Troubleshooting

| Error | Fix |
|---|---|
| `INVALID_SESSION_ID` | Token expired — re-authenticate |
| `IP restricted` | Add the runner IP to the Connected App trusted IPs |
| `ERROR running auth:jwt:grant` | Verify the certificate in the Connected App matches the private key |
