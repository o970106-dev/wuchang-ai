# LINE Secret Exposure Incident Record

## Status

A LINE client secret was pasted into an AI conversation and must be treated as exposed.

## Affected Material

- Organization: 新北市三重區五常社區發展協會
- Runtime path referenced by user code: `C:\Taiji_Runtime`
- Code pattern: Python script writing `.env.<org_name>` and `org_mapping.json`

The exposed secret value is intentionally not reproduced in this repository record.

## Required Action

1. Rotate the LINE client secret in the LINE Developers Console immediately.
2. Delete or overwrite any local `.env.*` files containing the old secret.
3. Ensure `.gitignore` blocks runtime secrets and generated environment files.
4. Replace hard-coded credentials with environment variables.
5. Store only non-secret mapping metadata in `org_mapping.json`.
6. Add a local-only template such as `.env.example` without real credentials.

## Safer Runtime Design

Secrets must remain outside Git history. The runtime should read credentials from process environment variables or a local secret store.

Allowed in Git:

```text
LINE_CLIENT_ID=<placeholder>
LINE_REDIRECT_URI=<placeholder>
```

Not allowed in Git:

```text
LINE_CLIENT_SECRET=<real secret>
```

## Recommended Environment Variables

```text
LINE_CLIENT_ID
LINE_CLIENT_SECRET
LINE_AUTH_URL
LINE_TOKEN_URL
LINE_VERIFY_URL
LINE_REDIRECT_URI
```

## Governance Note

This is a metric-hazard event because credential exposure changes the trust boundary of the LINE OAuth integration. Any deployment using the exposed credential should be treated as compromised until rotation is completed and confirmed.
