# AppSec AI Platform — Security Audit Workspace

A reusable, structured workspace for conducting professional security audits of websites and web applications. Designed for use with Claude Code as the AI-assisted audit engine.

---

## Purpose

This workspace provides a repeatable, evidence-based framework for security auditing. It includes:

- Structured audit commands (invoked as `/command-name`)
- Reusable audit skills with checklists and finding templates
- Strict rules for scope, evidence quality, reporting, and authorization
- Templates for every output artifact — plans, sessions, findings, reports
- A Python automation layer for runnable passive, authenticated, and active testing workflows

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
| `/audit-full-website` | Comprehensive full-domain audit with all checks |
| `/audit-weekly` | Weekly quick check (headers, auth, CVEs) |
| `/audit-monthly` | Monthly broader review |
| `/audit-quarterly` | Deep quarterly audit of all domains |
| `/audit-release` | Pre-release security gate |
| `/audit-annual` | Annual comprehensive posture review |

### 3. Run Focused Reviews (Optional)

Use these commands to drill into specific domains:

- `/review-auth` — Authentication and access control
- `/review-session` — Session management and JWT security
- `/review-rbac` — Role-based access control and IDOR
- `/review-input-validation` — Input validation and injection risks
- `/review-misconfig` — Security misconfiguration
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
├── docs/                       # Platform documentation and roadmap
│   ├── coverage-matrix.md      # Current capability coverage vs OWASP WSTG/ASVS
│   └── full-platform-roadmap.md
├── scripts/                    # Runnable CLI wrappers
├── src/                        # Python automation and workflows
│   ├── auth/                   # Credential store and auth lifecycle
│   ├── cli.py                  # CLI entrypoint
│   ├── config/                 # Configuration loading
│   ├── models/                 # Typed entities (Target, Finding, Evidence, etc.)
│   ├── parsers/                # Cookie, JWT, HTML, OpenAPI, manifest parsers
│   ├── policies/               # Authorization and stop-condition enforcement
│   ├── reporting/              # Executive/technical/remediation report generation
│   ├── session/                # Session manager and authenticated request handling
│   ├── storage/                # Run-state persistence
│   ├── tools/                  # Domain-specific audit tools
│   ├── utils/                  # Context reader, evidence writer, findings writer
│   └── workflows/              # Orchestration — passive and full audit workflows
├── tests/                      # Unit and integration tests
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

## Python Automation Layer

The platform includes a growing Python automation layer for executable audit workflows.

### Current Tools (`src/tools/`)

| Tool | Domain |
|------|--------|
| `headers_audit.py` | HTTP security headers |
| `tls_audit.py` | TLS and certificate review |
| `crawler.py` | Public route and endpoint discovery |
| `cookie_audit.py` | Cookie attribute and security review |
| `session_jwt_audit.py` | Session and JWT passive analysis |
| `dependency_audit.py` | Dependency manifest and CVE review |
| `misconfig_audit.py` | Security misconfiguration checks |
| `auth_audit.py` | Authentication flow review |
| `rbac_audit.py` | RBAC and IDOR review |
| `input_validation_audit.py` | Input validation and injection checks |
| `api_audit.py` | API security assessment |
| `secrets_scan.py` | Secrets and credential scanning |

### Platform Modules

| Module | Purpose |
|--------|---------|
| `src/models/entities.py` | Typed core entities (Target, Finding, Evidence, AuditRun) |
| `src/storage/run_store.py` | Run-state persistence |
| `src/policies/authorization.py` | Authorization mode enforcement |
| `src/policies/stop_conditions.py` | Safety stop conditions |
| `src/parsers/` | Cookie, JWT, HTML, OpenAPI, manifest parsers |
| `src/auth/credential_store.py` | Secure test credential handling |
| `src/session/session_manager.py` | Authenticated session management |
| `src/reporting/report_generator.py` | Report generation |
| `src/workflows/passive_web_audit.py` | Passive audit workflow orchestration |
| `src/workflows/full_audit.py` | Full multi-domain audit orchestration |

### Running Audits

Run a passive headers and TLS audit:

```bash
python scripts/run_audit.py audit headers-tls --url https://app.example.com --auditor "Your Name"
```

Run a full passive audit against all in-scope targets from context:

```bash
python scripts/run_audit.py audit passive
```

Run the full multi-domain audit workflow:

```bash
python scripts/run_audit.py audit full --url https://app.example.com --auditor "Your Name"
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

## Coverage

For the current capability coverage against OWASP WSTG and ASVS, see:

- [docs/coverage-matrix.md](docs/coverage-matrix.md)

For the full build roadmap and phased delivery plan, see:

- [docs/full-platform-roadmap.md](docs/full-platform-roadmap.md)

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

## Versioning and History

- Store completed audit outputs in `audits/[cadence]/YYYY-MM-DD-[type].md`
- Store final reports in `reports/final/YYYY-MM-DD-[type]-report.md`
- Keep findings register updated throughout the engagement

---

*This workspace is designed to be reused across multiple targets. Reset `context/` files for each new engagement.*
