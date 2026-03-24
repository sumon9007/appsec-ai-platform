# Project Structure

## Repository Tree

```text
appsec-ai-platform/
├── README.md
├── gettingstarted.md
├── .env.example
├── requirements.txt
├── setup.sh
│
├── .claude/                        ← Global intelligence layer (shared across engagements)
│   ├── CLAUDE.md                   ← Operating model and governance rules
│   ├── context/
│   │   └── active.md               ← Pointer to the active engagement
│   ├── commands/                   ← Slash command definitions
│   ├── docs/                       ← Governance documentation
│   ├── rules/                      ← Audit safety, evidence, severity, and reporting rules
│   ├── skills/                     ← Domain-specific review intelligence and templates
│   └── templates/                  ← Normalized output structures
│
├── engagements/                    ← Per-engagement working data (all audit data lives here)
│   ├── _template/                  ← Blank template — copy to start a new engagement
│   └── AUDIT-YYYY-CLIENT-NNN/
│       ├── context/                ← Scope, authorization, target profile, assumptions
│       ├── audit-runs/
│       │   ├── active/             ← Findings register, session records, run-state
│       │   └── completed/          ← Archived session files
│       ├── evidence/
│       │   ├── raw/                ← Evidence as collected
│       │   ├── reviewed/           ← Evidence confirmed as valid
│       │   └── summarized/         ← Redacted evidence ready for reports
│       ├── reports/
│       │   ├── draft/              ← Generated draft reports
│       │   └── final/              ← Approved final reports
│       └── audits/                 ← Cadence audit records (weekly, monthly, quarterly, etc.)
│
├── src/                            ← Python automation layer
│   ├── auth/                       ← Test credential handling
│   ├── config/                     ← Settings resolved from .env
│   ├── models/                     ← Typed entities (Finding, Evidence, AuditRun, Target)
│   ├── parsers/                    ← Cookie, JWT, HTML, OpenAPI, manifest parsers
│   ├── policies/                   ← Authorization mode and stop-condition enforcement
│   ├── reporting/                  ← HTML and Markdown report generators
│   ├── reports/                    ← Finding formatter utilities
│   ├── session/                    ← Authenticated session management
│   ├── storage/                    ← Run-state persistence
│   ├── tools/                      ← Domain audit tools (one per assessment domain)
│   ├── utils/                      ← Evidence writer, findings writer, context reader
│   └── workflows/                  ← Full audit and passive web audit orchestrators
│
├── scripts/
│   ├── run_audit.py                ← Primary CLI entry point
│   ├── create_engagement.py        ← Engagement bootstrap tool
│   └── build_reports_site.py       ← HTML report site builder
│
├── tests/                          ← Unit test suite
├── docs/                           ← Extended documentation
├── site_assets/                    ← Source CSS for HTML report site
└── static/                         ← Source HTML pages for report site
```

---

## Directory Roles

| Path | Purpose |
|------|---------|
| `.claude/context/active.md` | Pointer to the active engagement ID |
| `.claude/rules/` | Governance rules — evidence quality, scope, severity, safety, reporting |
| `.claude/skills/` | Domain review methodology and templates (loaded by Claude commands) |
| `.claude/templates/` | Normalized output structures for findings, reports, and sessions |
| `engagements/_template/` | Blank engagement scaffold — copy this to start a new engagement |
| `engagements/<ID>/context/` | Per-engagement source of truth for scope, authorization, and target profile |
| `engagements/<ID>/audit-runs/active/` | Findings register, session records, run-state JSON |
| `engagements/<ID>/evidence/raw/` | Evidence files as collected (EVID-YYYY-MM-DD-NNN format) |
| `engagements/<ID>/reports/draft/` | Generated draft reports |
| `src/workflows/` | Orchestration logic — calls tools in sequence, writes findings |
| `src/tools/` | Individual domain audit tools |
| `src/parsers/` | Non-network parsers — manifest, JWT, HTML, OpenAPI, cookie |
| `src/storage/` | Persisted run-state JSON for resumable workflows |
| `src/reporting/` | Markdown and HTML report generation |
| `src/policies/` | Authorization gate and stop-condition enforcement |
| `scripts/` | User-facing CLI entry points |

---

## Key Files

| File | Role |
|------|------|
| `scripts/run_audit.py` | Primary CLI — entry point for all audit commands |
| `scripts/create_engagement.py` | Bootstrap a new engagement from the template |
| `src/cli.py` | CLI command definitions and routing |
| `src/workflows/full_audit.py` | Main orchestration workflow — runs all tool subsets |
| `src/workflows/passive_web_audit.py` | Legacy focused passive workflow (headers + TLS only) |
| `src/config/settings.py` | All configuration resolved from `.env` and defaults |
| `src/utils/context_reader.py` | Reads scope, authorization, and target URLs from context files |
| `src/utils/evidence_writer.py` | Writes EVID-labeled evidence files |
| `src/utils/findings_writer.py` | Appends normalized findings to the register |
| `src/reporting/report_generator.py` | Produces technical, executive, and remediation reports |
| `src/policies/authorization.py` | Authorization mode enforcement — blocks without CONFIRMED status |
| `src/policies/stop_conditions.py` | Safety halt conditions for sensitive data discovery |
| `.env.example` | Configuration template — copy to `.env`, never commit `.env` |
| `.claude/CLAUDE.md` | Full operating model, workflow rules, and governance reference |
