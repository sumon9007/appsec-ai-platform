# Configuration

## Configuration Sources

The platform resolves configuration in this priority order:

1. CLI arguments (highest priority)
2. Environment variables from `.env`
3. Context files in `engagements/<ACTIVE_ENGAGEMENT>/context/`
4. Hard-coded defaults in `src/config/settings.py`

Copy `.env.example` to `.env` and populate it before running any command. Never commit `.env`.

---

## Environment Variables

### Engagement

| Variable | Default | Purpose |
|----------|---------|---------|
| `ACTIVE_ENGAGEMENT` | _(none)_ | Engagement folder name (e.g. `AUDIT-2026-CLIENT-001`). When set, all data paths resolve inside `engagements/<ACTIVE_ENGAGEMENT>/`. When unset, falls back to the legacy single-engagement layout. |

### Identity

| Variable | Default | Purpose |
|----------|---------|---------|
| `AUDIT_DEFAULT_AUDITOR` | `unknown-auditor` | Auditor display name written into evidence files, findings, and reports. Used when `--auditor` is not passed on the CLI. |

### Audit Run Defaults

| Variable | Default | Purpose |
|----------|---------|---------|
| `AUDIT_TARGET_URLS` | _(none)_ | Comma-separated list of in-scope target URLs. Used when `--url` is not passed on the CLI. |
| `AUDIT_REGISTER_PATH` | `engagements/<ID>/audit-runs/active/findings-register.md` | Path to the findings register. Used when `--register` is not passed. |
| `AUDIT_MANIFEST_PATH` | _(none)_ | Path to a dependency manifest file (`requirements.txt`, `package.json`, etc.). Used when `--manifest` is not passed. |
| `AUDIT_SPEC_PATH` | _(none)_ | Path to an OpenAPI or Postman collection spec file. Used when `--spec` is not passed. |
| `AUDIT_SCAN_PATH` | _(none)_ | Path to a directory or file for secrets scanning. Used when `--scan` is not passed. |
| `AUDIT_MAX_CRAWL_PAGES` | `30` | Maximum pages the crawler will visit per run. |

### Report Defaults

| Variable | Default | Purpose |
|----------|---------|---------|
| `AUDIT_TARGET_NAME` | _(none)_ | Target application name written into generated reports. |
| `AUDIT_REPORT_VERSION` | `DRAFT v0.1` | Report version label. Use `Final v1.0` for production-ready reports. |

### HTTP Client

| Variable | Default | Purpose |
|----------|---------|---------|
| `AUDIT_REQUEST_TIMEOUT` | `15` | HTTP request timeout in seconds. |
| `AUDIT_USER_AGENT` | `appsec-audit-tool/1.0` | User-agent string sent in all audit requests. |
| `AUDIT_MAX_REDIRECTS` | `5` | Maximum redirects to follow per request. |
| `AUDIT_SSL_VERIFY` | `true` | TLS certificate verification. Set to `false` only for staging environments with self-signed certificates. Never disable against production targets. |

### Test Credentials (Authenticated Testing)

These variables are only needed when running authenticated audit workflows. They are loaded in-memory by `CredentialStore` and never written to disk, logs, or evidence files.

The naming convention is role-based: replace `<ROLE>` with the role name in uppercase (e.g. `ADMIN`, `USER`, `READONLY`).

| Variable Pattern | Example | Purpose |
|-----------------|---------|---------|
| `AUDIT_USERNAME_<ROLE>` | `AUDIT_USERNAME_ADMIN` | Username for the test account of this role |
| `AUDIT_PASSWORD_<ROLE>` | `AUDIT_PASSWORD_ADMIN` | Password for the test account of this role |
| `AUDIT_MFA_<ROLE>` | `AUDIT_MFA_ADMIN` | TOTP secret for MFA-enabled test accounts (optional) |

Example `.env` entries for a two-role engagement:

```
AUDIT_USERNAME_ADMIN=testadmin@example.com
AUDIT_PASSWORD_ADMIN=SecureTestPassword1!
AUDIT_USERNAME_USER=testuser@example.com
AUDIT_PASSWORD_USER=SecureTestPassword2!
```

Roles with credentials configured are automatically detected by `CredentialStore.list_available_roles()`.

### External APIs

| Variable | Default | Purpose |
|----------|---------|---------|
| `OSV_API_BASE_URL` | `https://api.osv.dev/v1` | OSV.dev API base URL. No API key required. |

---

## Context Files

Each engagement has four context files in `engagements/<ENGAGEMENT_ID>/context/`. These are the primary source of truth for scope, authorization, and constraints — read by both the Python CLI and Claude commands before any audit activity begins.

| File | Purpose |
|------|---------|
| `audit-context.md` | Authorization status, audit ID, auditor, testing mode |
| `scope.md` | In-scope URLs, domains, and out-of-scope exclusions |
| `target-profile.md` | Application description, tech stack, environment type |
| `assumptions.md` | Known unknowns, evidence availability gaps, reviewer assumptions |

The `context_reader` module parses these files to extract target URLs, authorization status, testing mode, and audit ID. The scope parser uses regex-based URL extraction — scope entries must follow the format used in `engagements/_template/context/scope.md` for reliable parsing.

---

## Authorization and Scope Gating

- `policies.authorization.load_authorization()` reads `audit-context.md` and returns a typed `AuthorizationGrant`
- `policies.authorization.require_confirmed()` raises an error if the status is not `CONFIRMED` — no audit tool runs without this check passing
- `utils.context_reader.get_target_urls()` extracts in-scope URLs from `scope.md`

These gates are called at the start of every workflow. There is no way to bypass them without modifying `audit-context.md`.

---

## Secrets Handling

- Test credentials are loaded from environment variables only — never from files or code
- Credential material is held in memory and never written to disk, evidence files, or logs
- The evidence writer redacts common sensitive patterns (tokens, keys) before writing to `evidence/raw/`
- If unexpected credentials are found during an audit, stop immediately and follow the stop-condition protocol in `.claude/rules/safety-authorization-rules.md`
