# Linux Workspace Migration Decision

## Decision

For the Taiji / Wuchang AI runtime, returning the active development workspace to Linux is the correct default choice.

Windows may remain as an operation console, browser UI, VS Code host, and commercial-device control surface, but the canonical runtime workspace should be Linux / WSL / server-side Linux.

## Rationale

The current system includes Odoo, Python runtime services, LINE webhook/OAuth integration, Redis/state-window concepts, GitHub synchronization, systemd-style service operation, FastAPI/Uvicorn-style runtime, and multi-node deployment workflows. These components are naturally aligned with Linux.

## Recommended Split

| Layer | Recommended Environment | Reason |
|---|---|---|
| Runtime source of truth | Linux | Stable pathing, services, permissions, deployment parity. |
| Odoo / PostgreSQL / Redis | Linux | Native operational environment. |
| AI gateway / webhook services | Linux | Easier daemonization, logs, ports, and automation. |
| VS Code editing | Windows + Remote WSL/SSH | Keep UI convenience while editing Linux files directly. |
| Browser / LINE / Google console | Windows | Better for manual console operations. |
| Secrets | Local Linux env / secret store | Do not hard-code or commit credentials. |

## Operational Rule

Avoid editing the same project from both Windows filesystem and Linux filesystem as separate copies. Choose one canonical workspace and attach editors to it.

Preferred pattern:

```text
Windows VS Code
→ Remote WSL / Remote SSH
→ Linux workspace
→ GitHub
```

Avoid:

```text
C:\Taiji_Runtime copy
+
/home/taiji_admin/Taiji_Hub copy
+
manual file movement
```

This causes drift, path confusion, duplicate secrets, and inconsistent Git state.

## Governance Note

This migration is not only a convenience decision. It is a metric-conservation decision: one canonical runtime workspace reduces drift, improves auditability, and makes deployment behavior predictable.

## Security Note

After the recent LINE credential exposure event, Linux workspace migration should include:

1. Secret rotation.
2. Removal of hard-coded secrets.
3. `.gitignore` coverage for `.env*`, secrets, tokens, and runtime-generated files.
4. Local-only `.env.example` templates.
5. One canonical secret-loading mechanism.

## Suggested Canonical Path

```text
/home/taiji_admin/Taiji_Hub
```

or a dedicated repository path such as:

```text
/home/taiji_admin/Taiji_Hub/wuchang-ai
```

## Migration Checklist

- Confirm Linux workspace path.
- Confirm Git remote and branch.
- Move only source code, not secrets.
- Add `.gitignore` before committing.
- Convert Windows paths to configurable environment variables.
- Replace hard-coded credentials with environment variables.
- Run local tests from Linux.
- Push only clean source and documentation.

## Final Position

Linux should be the canonical development and runtime workspace. Windows should be treated as a control panel and editor surface, not the source of runtime truth.
