# Architecture

## System Architecture

The repository has two major layers:

1. Governance layer in `.claude/`
2. Execution layer in `src/` plus `scripts/run_audit.py`

The governance layer defines audit rules, context files, standards, templates, and human-guided review skills. The execution layer performs automated evidence collection, finding normalization, run-state writing, and report generation.

## Major Components

| Component | Responsibility |
|----------|----------------|
| `scripts/run_audit.py` | Thin wrapper that loads and invokes the Click CLI |
| `src/cli.py` | Command definitions for audit, report, and session operations |
| `src/config/settings.py` | `.env` and environment-backed configuration |
| `src/workflows/` | High-level audit orchestration |
| `src/tools/` | Domain-specific audit checks |
| `src/parsers/` | Structured extraction from cookies, HTML, JWTs, manifests, and API specs |
| `src/models/entities.py` | Core dataclasses and enums |
| `src/policies/` | Authorization and stop-condition policy logic |
| `src/utils/` | Context reading, HTTP client, evidence writer, findings writer |
| `src/storage/run_store.py` | JSON run-state persistence |
| `src/reporting/report_generator.py` | Draft report generation |

## Execution Flow

### Main workflow path

1. User runs `python3 scripts/run_audit.py ...`
2. `src/cli.py` resolves CLI options and defaults from `settings.py`
3. Workflow loads authorization and target context from `.claude/context/`
4. Workflow executes one or more tools
5. Tools optionally write evidence to `evidence/raw/`
6. Workflow maps tool results into normalized findings
7. Findings are appended to `audit-runs/active/findings-register.md`
8. Session and run-state records are written under `audit-runs/active/`
9. Reports can later be generated into `reports/draft/`

## Data Flow

### Context and trust boundaries

- Inputs come from CLI arguments, `.env`, `.claude/context/`, network responses, and local files.
- Authorization trust is rooted in `.claude/context/audit-context.md`.
- Scope trust is rooted in `.claude/context/scope.md`.
- Tool outputs are normalized as plain dicts, then written through shared writers.

### Evidence lifecycle

1. Tool collects response or file-based data
2. `write_evidence()` assigns an `EVID-YYYY-MM-DD-NNN` label
3. Sensitive patterns are redacted before write
4. Evidence is stored in `evidence/raw/`
5. Findings reference one or more evidence labels

### Findings lifecycle

1. Workflow receives tool results
2. Workflow converts result dicts to normalized findings
3. `append_finding()` validates vocabulary and assigns `FIND-NNN`
4. The finding is appended to the findings register and summary table

### Reporting lifecycle

1. Report command reads the findings register
2. Markdown blocks are parsed by regex
3. Severity counts and summaries are built
4. Draft reports are written to `reports/draft/`

## Trust and Safety Boundaries

- Authorization must be confirmed before workflows proceed.
- Active testing is gated by `require_active_testing()`.
- Stop-condition detectors exist for sensitive data and compromise indicators.

Doc/code mismatch:
- Stop-condition checks are not uniformly called by every tool despite the policy docstring stating they should be.

## Resumability

The platform writes a single run-state file: `audit-runs/active/run-state.json`.

Needs verification:
- The code persists run state, but does not yet expose a resume command or a robust restart/recovery mechanism.
