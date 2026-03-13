# Models and Storage

## Typed Entities

The core dataclasses live in `src/models/entities.py`.

| Entity | Purpose |
|--------|---------|
| `Target` | Scoped audit target |
| `AuthorizationGrant` | Authorization state and mode |
| `TestAccount` | Metadata for approved test accounts |
| `Evidence` | Metadata for evidence items |
| `Finding` | Normalized security finding |
| `ControlCheck` | Single tool check result |
| `ReviewGap` | A documented area that could not be fully assessed |
| `AuditRun` | Workflow execution state |

## Enums

- `Severity`
- `Confidence`
- `FindingStatus`
- `AuthorizationMode`
- `Environment`
- `AuditRunStatus`

## Run-State Persistence

`src/storage/run_store.py` writes a JSON file to:

- `audit-runs/active/run-state.json`

Stored fields include:

- run ID
- audit ID
- auditor
- authorization state
- target list
- tools run
- findings written
- evidence written
- errors
- session path

## Evidence Schema

Evidence files are Markdown documents with:

- EVID label
- date
- collector
- type
- domain
- related finding
- description
- evidence content
- observations
- chain of custody notes

## Findings Schema

The findings register is append-only from Python.

A normalized finding contains:

- title
- domain
- severity
- confidence
- target
- evidence labels
- observation
- risk
- recommendation
- acceptance criteria
- status
- review type

## Storage Responsibilities

| Module | Responsibility |
|--------|----------------|
| `run_store.py` | Run-state JSON |
| `evidence_writer.py` | Evidence artifact write path and redaction |
| `findings_writer.py` | Findings register validation and append |

Doc/code mismatch:
- `AuditRun.evidence_written` exists in the model, but the current workflows do not appear to populate it consistently.
