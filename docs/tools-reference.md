# Tools Reference

## Classification Notes

- `Passive`: observes responses or local files without intrusive payload execution
- `Authenticated-ready`: can support approved authenticated review, but may not be fully wired in workflows
- `Active-gated`: mentions or anticipates active testing but does not fully automate it today

## Tool Summary

| Tool | Mode | Purpose |
|------|------|---------|
| `headers_audit.py` | Passive | Check common HTTP security headers |
| `tls_audit.py` | Passive | Inspect certificate and negotiated TLS details |
| `crawler.py` | Passive | Discover same-host pages and page inventories |
| `cookie_audit.py` | Passive | Assess cookie flags from unauthenticated responses |
| `session_jwt_audit.py` | Passive | Detect and inspect JWTs in visible responses |
| `misconfig_audit.py` | Passive | Check disclosure and public misconfiguration signals |
| `auth_audit.py` | Passive / Authenticated-ready | Observe login/reset surfaces and auth review gaps |
| `rbac_audit.py` | Authenticated-ready / Active-gated | Review authorization patterns and likely IDOR areas |
| `input_validation_audit.py` | Passive / Active-gated | Inspect forms and identify likely validation risk areas |
| `api_audit.py` | Passive / Active-gated | Parse specs and passively flag API control issues |
| `dependency_audit.py` | Passive (file-based) | Parse manifests and query OSV |
| `secrets_scan.py` | Passive (file-based) | Scan local files for likely secrets |

## Per-Tool Notes

### Headers Audit

- Inputs: target URL, shared `HttpClient`
- Outputs: finding-ready dicts for missing or weak headers
- Evidence: raw HTTP capture written via `write_evidence()`
- Limitation: only checks headers visible from the fetched response

### TLS Audit

- Inputs: HTTPS URL
- Outputs: certificate and protocol findings, plus explicit cipher-enumeration review gap
- Evidence: TLS certificate/protocol details
- Limitation: only negotiated cipher is observed; full enumeration is not implemented

### Crawler

- Inputs: base URL and page limit
- Outputs: page inventory objects and crawl errors
- Evidence: passive route inventory
- Limitation: same-host crawling only; depends on reachable HTML

### Cookie Audit

- Inputs: target URL
- Outputs: cookie attribute findings or review-gap output
- Evidence: `Set-Cookie` capture
- Limitation: unauthenticated response only

### Session/JWT Audit

- Inputs: target URL
- Outputs: JWT weakness findings or review gaps
- Evidence: JWT observation summary
- Limitation: no signature verification; no authenticated token capture orchestration

### Misconfiguration Audit

- Inputs: target URL
- Outputs: disclosure and configuration issue findings
- Evidence: passive response and page-observation evidence
- Limitation: limited to surface-level checks

### Authentication Audit

- Inputs: target URL
- Outputs: login/reset observations and auth review gaps
- Evidence: auth-path discovery summary
- Limitation: authenticated checks are mostly described as follow-up actions

### RBAC Audit

- Inputs: target URL plus crawl pages
- Outputs: authorization review hints and access-control review gaps
- Evidence: authorization-related passive observations
- Limitation: true multi-role validation is not fully orchestrated

### Input Validation Audit

- Inputs: target URL and page inventories
- Outputs: form and parameter risk findings, often with “requires authorized active testing” guidance
- Evidence: page/form inventory evidence
- Limitation: does not deliver a full active probing engine today

### API Audit

- Inputs: URL and optional spec path
- Outputs: spec-based findings and passive API observations
- Evidence: API inventory evidence
- Limitation: active API abuse cases are not fully automated

### Dependency Audit

- Inputs: manifest path
- Outputs: one finding per vulnerable dependency
- Evidence: manifest scan summary
- Limitation: depends on parseable manifest and reachable OSV API

### Secrets Scan

- Inputs: file or directory path
- Outputs: one finding per detected secret pattern per file/pattern combination
- Evidence: file scan summary with redacted snippets
- Limitation: regex-based detection only
