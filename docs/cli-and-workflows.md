# CLI and Workflows

## Entry Points

| File | Role |
|------|------|
| `scripts/run_audit.py` | Primary user-facing CLI entry point |
| `src/cli.py` | CLI command definitions (Click groups and commands) |

---

## CLI Command Groups

### `audit`

| Command | Description |
|---------|-------------|
| `audit full` | Run all passive audit tools in sequence against one or more target URLs |
| `audit headers` | HTTP security headers audit only |
| `audit tls` | TLS and certificate audit only |
| `audit cookies` | Cookie attribute audit only |
| `audit session` | Session token and JWT audit only |
| `audit misconfig` | Security misconfiguration checks only |
| `audit dependencies` | Dependency CVE audit from a manifest file |
| `audit secrets` | Secrets and credential scan from a local directory |
| `audit api` | API security audit from an OpenAPI/Postman spec |
| `audit headers-tls` | Combined headers and TLS audit |

### `report`

| Command | Description |
|---------|-------------|
| `report technical` | Generate a technical findings report from the register |
| `report executive` | Generate a non-technical executive summary |
| `report remediation` | Generate a prioritized remediation plan |

### `session`

| Command | Description |
|---------|-------------|
| `session status` | Show current authorization, auditor, and in-scope URL configuration |

---

## Common Usage Examples

```bash
# Check authorization and target configuration
python scripts/run_audit.py session status

# Full passive audit
python scripts/run_audit.py audit full --url https://app.example.com --auditor "Analyst"

# Run a subset of tools
python scripts/run_audit.py audit full --tools headers,tls,cookies --url https://app.example.com

# Full audit with all file-based tools
python scripts/run_audit.py audit full \
  --url https://app.example.com \
  --manifest requirements.txt \
  --spec openapi.yaml \
  --scan src/

# Dry run — collect evidence but do not write findings
python scripts/run_audit.py audit full --dry-run --url https://app.example.com

# Dependency audit only
python scripts/run_audit.py audit dependencies --manifest requirements.txt

# Generate all reports
python scripts/run_audit.py report technical
python scripts/run_audit.py report executive
python scripts/run_audit.py report remediation
```

---

## `audit full` Tool Selection

The `--tools` flag accepts a comma-separated list of tool identifiers. When omitted, all passive URL-based tools run by default.

| Identifier | Tool | Input Required |
|------------|------|---------------|
| `headers` | HTTP security headers | Target URL |
| `tls` | TLS and certificate check | Target URL (HTTPS) |
| `cookies` | Cookie attribute review | Target URL |
| `session` | Session token and JWT review | Target URL |
| `misconfig` | Security misconfiguration | Target URL |
| `auth` | Authentication flow review | Target URL |
| `rbac` | Authorization and IDOR review | Target URL (crawl data helps) |
| `input` | Input validation surfaces | Target URL + crawl data |
| `crawl` | Passive page discovery | Target URL |
| `dependencies` | Dependency CVE lookup | `--manifest` file |
| `api` | API security review | `--spec` file + Target URL |
| `secrets` | Secrets and credential scan | `--scan` directory |

> **Note:** `auth`, `rbac`, and `input` are only available via `audit full --tools <name>`. There are no standalone `audit auth`, `audit rbac`, or `audit input` commands in the current CLI.

---

## Workflow Descriptions

### `passive_web_audit.py`

The original focused workflow — runs headers and TLS checks only.

- Requires `Authorization Status: CONFIRMED`
- Resolves targets from CLI or `context/scope.md`
- Runs `HeadersAudit` and `TLSAudit` only
- Converts tool output to findings and writes a session record

Use this for quick header/TLS-only reviews.

### `full_audit.py`

The main orchestration workflow — runs all applicable tools.

- Requires `Authorization Status: CONFIRMED`
- Resolves targets from CLI or context
- Optionally crawls first to feed downstream tools (`rbac`, `input`)
- Runs all selected tool subsets in sequence
- Writes findings to the register (unless `--dry-run`)
- Writes a session record and persists run-state JSON

Execution order within a single URL pass:

```
crawl → headers → tls → cookies → session → misconfig → auth → rbac → input → api
```

File-based tools (`dependencies`, `secrets`) run after all URL passes complete.

---

## Passive vs Authenticated vs Active

| Mode | Current Reality |
|------|----------------|
| Passive workflows | Fully implemented — all URL-based tools run without test credentials |
| Authenticated workflows | Scaffolding exists (`CredentialStore`, `SessionManager`) but not wired into primary workflows end-to-end |
| Active testing | Authorization gate is in place; orchestrated active payload execution is not yet implemented |

For audit domains that require authenticated access or active validation, the tools produce **review gaps** — structured observations noting what could not be confirmed without further testing.
