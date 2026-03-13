# Troubleshooting

## Common Failure Modes

### Authorization errors

Symptom:
- Workflow exits with an authorization error

Check:
- `.claude/context/audit-context.md`
- `Authorization Status` must be `CONFIRMED`

### No targets found

Symptom:
- Workflow reports no in-scope targets

Check:
- `.claude/context/scope.md`
- `--url` arguments
- `AUDIT_TARGET_URLS` in `.env`

### No findings written

Possible reasons:

- The tool found no failing conditions
- `--dry-run` was used
- A file-based tool returned no issues
- A tool emitted review gaps only

### Dependency audit returns nothing

Check:

- manifest format is supported
- manifest file exists
- network connectivity to OSV API is available

### Report generation produces sparse output

Check:

- findings register exists
- findings match the expected Markdown structure
- findings include evidence and required fields

### Tests do not run

Check:

- `pytest` is installed in your environment

## Operational Caveats

- Some domains described in docs are more aspirational than fully automated.
- Several tools rely on passive observation and cannot confirm deeper issues without credentials or stronger authorization.
- Findings and report generation are Markdown-structure sensitive.
