# CLI and Workflows

## Entry Points

- `python3 scripts/run_audit.py`
- `src/cli.py`

## CLI Groups

### `audit`

Available commands verified from the current CLI:

- `headers-tls`
- `full`
- `headers`
- `tls`
- `cookies`
- `session`
- `misconfig`
- `dependencies`
- `secrets`
- `api`

### `report`

- `technical`
- `executive`
- `remediation`

### `session`

- `status`

## Main Usage Examples

```bash
python3 scripts/run_audit.py session status
python3 scripts/run_audit.py audit full --url https://app.example.com --auditor "Analyst"
python3 scripts/run_audit.py audit full --tools headers,tls,cookies --dry-run
python3 scripts/run_audit.py audit dependencies --manifest requirements.txt
python3 scripts/run_audit.py report technical
```

## Workflow Descriptions

### `passive_web_audit.py`

This is the narrower legacy workflow.

- Requires confirmed authorization
- Resolves targets from CLI or scope context
- Runs headers and TLS tools only
- Converts tool output to findings
- Writes a session record

### `full_audit.py`

This is the main orchestration workflow.

- Loads typed authorization grant
- Requires confirmed authorization
- Resolves targets
- Optionally crawls first
- Runs a selected tool subset
- Writes findings unless `--dry-run` is set
- Writes a session record
- Persists run-state JSON

## Tool Selection in `audit full`

Supported tool identifiers:

- `headers`
- `tls`
- `cookies`
- `session`
- `misconfig`
- `auth`
- `rbac`
- `input`
- `crawl`
- `dependencies`
- `api`
- `secrets`

Doc/code mismatch:
- These tool subsets are supported by `audit full --tools ...`, but there are no separate direct `audit auth`, `audit rbac`, or `audit input` commands in the current CLI.

## Passive vs Authenticated vs Active

| Area | Current Reality |
|------|------------------|
| Passive workflows | Well represented |
| Authenticated workflows | Mostly scaffolding and review-gap support |
| Active workflows | Mostly authorization-gated intention, not full execution |

## Session Status

`python3 scripts/run_audit.py session status` reports:

- Audit ID
- Auditor
- Authorization status
- Testing mode
- Count and list of in-scope URLs
