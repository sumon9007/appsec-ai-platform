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

Before running any audit, populate the `.claude/context/` files:

| File | What to Fill In |
|------|----------------|
| `.claude/context/audit-context.md` | Audit name, date, authorization confirmation |
| `.claude/context/target-profile.md` | Application name, tech stack, roles |
| `.claude/context/scope.md` | In-scope URLs, out-of-scope exclusions |
| `.claude/context/assumptions.md` | Unknowns and assumptions going in |

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
├── .claude/                    # Claude workspace operating model
│   ├── CLAUDE.md               # Instructions for Claude Code
│   ├── context/                # Audit-specific context (fill before starting)
│   ├── docs/                   # Reference documentation and standards
│   ├── commands/               # Slash command definitions
│   ├── skills/                 # Audit skill modules with templates
│   ├── rules/                  # Enforced rules for scope, evidence, reporting
│   └── templates/              # Reusable output templates
├── scripts/                    # Runnable CLI wrappers
├── src/                        # Python automation and workflows
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
| `.claude/docs/audit-domains.md` | Domains covered and key risks per domain |
| `.claude/docs/audit-frequencies.md` | What each audit cadence covers |
| `.claude/docs/acceptance-criteria.md` | What "passing" looks like per domain |
| `.claude/docs/evidence-standard.md` | Evidence labeling and storage conventions |
| `.claude/docs/reporting-standard.md` | Report structure and severity vocabulary |
| `.claude/docs/remediation-standard.md` | SLAs and remediation requirements |

---

## Runnable Workflow

The first executable workflow currently implemented is a passive Security Headers and TLS review.

Run it with an explicit target:

```bash
python scripts/run_audit.py audit headers-tls --url https://app.example.com --auditor "Your Name"
```

Or let the runner read in-scope targets from `.claude/context/scope.md`:

```bash
python scripts/run_audit.py audit headers-tls
```

---

## Reports Portal

This repository includes a GitHub Pages report portal generated from the Markdown files in `reports/draft/` and `reports/final/`.

- Local build: `python3 scripts/build_reports_site.py`
- Generated output: `site/`
- Published path on GitHub Pages: `/reports/`
- Deployment workflow: `.github/workflows/deploy-reports-pages.yml`

To publish it, enable GitHub Pages in the repository settings and select **GitHub Actions** as the source.

---

## Coverage Matrix

For a current view of what this platform does and does not yet cover against common web application security testing expectations, see:

- `docs/coverage-matrix.md`

---

## Versioning and History

- Store completed audit outputs in `audits/[cadence]/YYYY-MM-DD-[type].md`
- Store final reports in `reports/final/YYYY-MM-DD-[type]-report.md`
- Keep findings register updated throughout the engagement

---

*This workspace is designed to be reused across multiple targets. Reset `context/` files for each new engagement.*
