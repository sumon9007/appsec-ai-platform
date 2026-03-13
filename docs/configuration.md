# Configuration

## Configuration Sources

The project resolves configuration in this order:

1. CLI arguments
2. Environment variables from `.env`
3. Some fallback values from `.claude/context/`
4. Hard-coded defaults in `src/config/settings.py`

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `AUDIT_DEFAULT_AUDITOR` | Default auditor name |
| `AUDIT_TARGET_URLS` | Comma-separated default targets |
| `AUDIT_REGISTER_PATH` | Findings register path |
| `AUDIT_MANIFEST_PATH` | Default dependency manifest path |
| `AUDIT_SPEC_PATH` | Default OpenAPI/Postman spec path |
| `AUDIT_SCAN_PATH` | Default secrets scan path |
| `AUDIT_MAX_CRAWL_PAGES` | Crawl limit |
| `AUDIT_TARGET_NAME` | Report target name |
| `AUDIT_REPORT_VERSION` | Report version label |
| `AUDIT_REQUEST_TIMEOUT` | HTTP timeout |
| `AUDIT_USER_AGENT` | HTTP user agent |
| `AUDIT_MAX_REDIRECTS` | Max redirects |
| `AUDIT_SSL_VERIFY` | TLS verification toggle |
| `OSV_API_BASE_URL` | OSV API base URL |

## Context Files

The `.claude/context/` files act as engagement metadata:

- `audit-context.md` holds authorization status, audit ID, and testing mode.
- `scope.md` holds in-scope targets and boundaries.
- `target-profile.md` and `assumptions.md` support human review context.

## Secrets Handling

- Test credentials are loaded from environment variables only.
- Credential material is intended to stay in memory.
- Evidence writer redacts some sensitive patterns before storage.

Doc/code mismatch:
- The environment template does not currently document role-based credential environment variables used by `CredentialStore`, such as `AUDIT_USERNAME_ADMIN` and `AUDIT_PASSWORD_ADMIN`.

## Authorization and Scope Handling

- `context_reader.check_authorization()` is the basic authorization gate.
- `policies.authorization.load_authorization()` converts free-text authorization scope into typed modes.
- `get_target_urls()` extracts in-scope URLs from `scope.md`.

Needs verification:
- The scope parser is intentionally simple and regex-based; very custom scope formatting may not parse as expected.
