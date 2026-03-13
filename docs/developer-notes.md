# Developer Notes

## Technical Debt

- Tool output is mostly untyped dict data rather than `ControlCheck` objects.
- Stop-condition enforcement is not centralized.
- Workflows do not consistently track evidence IDs back into `AuditRun`.
- The report generator relies on regex parsing of Markdown, which is fragile.

## Refactor Opportunities

- Introduce a common typed result model for tools.
- Route all network and file-derived evidence through a common post-processing policy layer.
- Move finding normalization into a shared adapter instead of duplicating mapping logic in workflows.
- Make run-state more than a final snapshot by persisting per-step progress.

## Code/Doc Mismatches

- Existing coverage docs overstate active and authenticated maturity.
- CLI docs in older files mention commands that are not currently exposed.
- The roadmap references modules not yet present in the repository.

## Recommended Next Engineering Steps

1. Add direct CLI commands or improve docs for `audit full --tools auth|rbac|input`.
2. Wire `SessionManager` and `CredentialStore` into authenticated workflow paths.
3. Create an explicit active probe module with clear authorization checks.
4. Enforce stop conditions automatically in shared request/file handling paths.
5. Expand tests to cover `full_audit.py`, report generation, and representative tool behavior.
