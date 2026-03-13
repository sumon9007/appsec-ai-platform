# Project Structure

## Important Repository Tree

```text
appsec-ai-platform/
├── README.md
├── .env.example
├── requirements.txt
├── .claude/
│   ├── CLAUDE.md
│   ├── commands/
│   ├── context/
│   ├── docs/
│   ├── prompts/
│   ├── rules/
│   ├── skills/
│   └── templates/
├── docs/
├── scripts/
│   ├── run_audit.py
│   └── build_reports_site.py
├── src/
│   ├── auth/
│   ├── config/
│   ├── models/
│   ├── parsers/
│   ├── policies/
│   ├── reporting/
│   ├── reports/
│   ├── session/
│   ├── storage/
│   ├── tools/
│   ├── utils/
│   └── workflows/
├── tests/
├── audit-runs/
├── evidence/
├── reports/
└── audits/
```

## Directory Roles

| Path | Purpose |
|------|---------|
| `.claude/context/` | Engagement-specific source of truth |
| `.claude/rules/` | Audit safety, evidence, severity, and reporting rules |
| `.claude/skills/` | Human-guided domain review instructions and templates |
| `scripts/` | User-facing script entrypoints |
| `src/workflows/` | Orchestration logic |
| `src/tools/` | Individual domain tools |
| `src/parsers/` | Non-network parsers and extractors |
| `src/storage/` | Persisted run metadata |
| `src/reporting/` | Report generation |
| `audit-runs/active/` | Active findings register, sessions, run-state |
| `evidence/raw/` | Raw evidence artifacts |
| `reports/draft/` | Generated draft reports |

## Key Files

| File | Why It Matters |
|------|----------------|
| `src/cli.py` | Main CLI surface |
| `src/workflows/full_audit.py` | Broadest workflow |
| `src/workflows/passive_web_audit.py` | Legacy focused passive workflow |
| `src/utils/context_reader.py` | Reads scope and authorization inputs |
| `src/utils/evidence_writer.py` | Writes evidence artifacts |
| `src/utils/findings_writer.py` | Appends normalized findings |
| `src/reporting/report_generator.py` | Produces technical, executive, and remediation reports |
