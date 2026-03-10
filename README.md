# AppSec AI Platform — Security Audit Workspace

A reusable, structured workspace for conducting professional security audits of websites and web applications. Designed for use with Claude Code as the AI-assisted audit engine.

---

## Purpose

This workspace provides a repeatable, evidence-based framework for security auditing. It includes:

- Structured audit commands (invoked as `/command-name`)
- Reusable audit skills with checklists and finding templates
- Strict rules for scope, evidence quality, reporting, and authorization
- Templates for every output artifact — plans, sessions, findings, reports

---

## Quick-Start Workflow

### 1. Set Up Context

Before running any audit, populate the context files:

| File | What to Fill In |
|------|----------------|
| `context/audit-context.md` | Audit name, date, authorization confirmation |
| `context/target-profile.md` | Application name, tech stack, roles |
| `context/scope.md` | In-scope URLs, out-of-scope exclusions |
| `context/assumptions.md` | Unknowns and assumptions going in |

### 2. Choose Your Audit Command

| Command | Use When |
|---------|----------|
| `/audit-website` | Full audit of a website or web application |
| `/audit-weekly` | Weekly quick check (headers, auth, CVEs) |
| `/audit-monthly` | Monthly broader review |
| `/audit-quarterly` | Deep quarterly audit of all domains |
| `/audit-release` | Pre-release security gate |
| `/audit-annual` | Annual comprehensive posture review |

### 3. Run Focused Reviews (Optional)

Use these commands to drill into specific domains:

- `/review-auth` — Authentication and access control
- `/review-rbac` — Role-based access control and IDOR
- `/review-logging` — Logging and monitoring coverage
- `/review-dependencies` — Dependency and supply chain review
- `/review-headers` — HTTP security headers and TLS

### 4. Generate Outputs

- `/generate-report` — Produce executive and technical report
- `/generate-remediation-plan` — Produce prioritized remediation plan

---

## Folder Layout

```
./
├── README.md                   # This file
├── CLAUDE.md                   # Instructions for Claude Code
├── context/                    # Audit-specific context (fill before starting)
├── docs/                       # Reference documentation and standards
├── commands/                   # Slash command definitions
├── skills/                     # Audit skill modules with templates
├── rules/                      # Enforced rules for scope, evidence, reporting
├── templates/                  # Reusable output templates
├── audits/                     # Completed audit outputs by cadence
│   ├── weekly/
│   ├── monthly/
│   ├── quarterly/
│   ├── release/
│   └── annual/
├── audit-runs/                 # Active and completed audit session records
│   ├── active/
│   └── completed/
├── evidence/                   # Collected evidence artifacts
│   ├── raw/                    # Unprocessed evidence
│   ├── reviewed/               # Verified and annotated evidence
│   └── summarized/             # Evidence summaries referenced in reports
└── reports/                    # Final and draft reports
    ├── draft/
    └── final/
```

---

## Key Principles

- **Evidence-first:** No finding is recorded without evidence. See `rules/evidence-quality-rules.md`.
- **Scope-bound:** Testing never exceeds the defined scope. See `rules/audit-scope-rules.md`.
- **Authorization required:** Active testing requires written authorization. See `rules/safety-authorization-rules.md`.
- **Consistent severity:** All findings rated using the standard vocabulary. See `rules/severity-rating-rules.md`.
- **Template-driven outputs:** All reports, plans, and registers use defined templates.

---

## Reference Documents

| Document | Purpose |
|----------|---------|
| `docs/audit-domains.md` | Domains covered and key risks per domain |
| `docs/audit-frequencies.md` | What each audit cadence covers |
| `docs/acceptance-criteria.md` | What "passing" looks like per domain |
| `docs/evidence-standard.md` | Evidence labeling and storage conventions |
| `docs/reporting-standard.md` | Report structure and severity vocabulary |
| `docs/remediation-standard.md` | SLAs and remediation requirements |

---

## Versioning and History

- Store completed audit outputs in `audits/[cadence]/YYYY-MM-DD-[type].md`
- Store final reports in `reports/final/YYYY-MM-DD-[type]-report.md`
- Keep findings register updated throughout the engagement

---

*This workspace is designed to be reused across multiple targets. Reset `context/` files for each new engagement.*
