# Reporting

## Findings Register

The primary working findings store is:

- `audit-runs/active/findings-register.md`

`append_finding()`:

- validates required fields
- validates severity, confidence, and status vocabulary
- assigns the next `FIND-NNN`
- updates the summary table
- appends the detailed Markdown finding block

## Evidence Store

Evidence is written to:

- `evidence/raw/`

The writer:

- assigns `EVID-YYYY-MM-DD-NNN`
- redacts some sensitive patterns
- writes a standardized Markdown evidence record

## Session Records

Workflows write Markdown session records into:

- `audit-runs/active/`

Current session record types include:

- passive web session
- full audit session

## Report Generation Flow

Commands:

- `report technical`
- `report executive`
- `report remediation`

The report generator:

1. Parses the findings register by regex
2. Sorts and counts findings
3. Produces draft Markdown reports in `reports/draft/`

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Findings register | `audit-runs/active/findings-register.md` |
| Run-state | `audit-runs/active/run-state.json` |
| Session records | `audit-runs/active/*.md` |
| Raw evidence | `evidence/raw/` |
| Draft reports | `reports/draft/` |

## Operational Caveat

Needs verification:
- Report parsing depends on the current Markdown structure of the findings register. Structural changes to finding formatting could break report generation.
