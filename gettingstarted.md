# Getting Started — AppSec AI Platform

A practical guide to setting up and running your first security audit with this workspace.

---

## Overview

`appsec-ai-platform` is a Python-based security audit workspace for authorized, evidence-driven web application assessments. It has two layers:

- **Python CLI** (`src/` + `scripts/`) — runnable audit tools and workflows
- **Claude governance layer** (`.claude/`) — scope, authorization, evidence quality, and reporting standards

Before running anything, you need to confirm authorization and configure your audit context. This guide walks through both.

---

## Prerequisites

- Python 3.10+
- Network access (for live HTTP/TLS checks and CVE lookups)
- A writable local workspace
- Written authorization from the target system owner

---

## 1. Install Dependencies

```bash
cd /path/to/appsec-ai-platform

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Verify the install:

```bash
python3 scripts/run_audit.py session status
```

---

## 2. Configure Environment

Copy the example env file and populate it:

```bash
cp .env.example .env
```

Key variables to set in `.env`:

| Variable | Purpose |
|----------|---------|
| `AUDIT_TARGET_URLS` | Comma-separated list of in-scope URLs |
| `AUDITOR_NAME` | Your name as it appears in reports |
| `FINDINGS_REGISTER_PATH` | Path to your findings register file |
| `MANIFEST_PATH` | Path to dependency manifest (e.g. `requirements.txt`) |
| `SECRETS_SCAN_PATH` | Directory to scan for secrets |
| `API_SPEC_PATH` | Path to OpenAPI spec file (optional) |

---

## 3. Create or Load an Engagement

All per-engagement data (context, evidence, findings, reports) lives under `engagements/<ENGAGEMENT_ID>/`.

### Create a new engagement

```bash
python scripts/create_engagement.py
```

Or copy the template manually:

```bash
cp -r engagements/_template engagements/AUDIT-YYYY-CLIENT-NNN
```

Then update `ACTIVE_ENGAGEMENT=AUDIT-YYYY-CLIENT-NNN` in your `.env` file.

### Populate the four context files

These files must be completed before any audit activity can begin. Find them at `engagements/<ENGAGEMENT_ID>/context/`:

**`audit-context.md`** — Set `Authorization Status: CONFIRMED` and record:
- Authorizing party name and title
- Authorization date
- Reference to authorization document (email, ticket, signed scope agreement)
- Testing mode: `Passive Only` or `Passive + Active Testing on [ENVIRONMENT]`

**`scope.md`** — Define:
- In-scope URLs, domains, and endpoints
- Out-of-scope items (subdomains, third-party services, internal systems)

**`target-profile.md`** — Describe the target:
- Application name and purpose
- Technology stack (if known)
- Authentication model
- Environment type (production, staging, QA)

**`assumptions.md`** — List assumptions, known unknowns, and evidence availability gaps.

> **Authorization check:** If `audit-context.md` does not have `Authorization Status: CONFIRMED`, the CLI and Claude workflows will halt.

---

## 4. Run a Session Status Check

Verify your configuration is complete before starting:

```bash
python3 scripts/run_audit.py session status
```

This reports:

- Audit ID
- Auditor name
- Authorization status
- Testing mode
- In-scope URL count and list

---

## 5. Run Your First Audit

### Dry run (no findings written)

```bash
python3 scripts/run_audit.py audit full --dry-run
```

### Full passive audit

```bash
python3 scripts/run_audit.py audit full
```

### Targeted domain checks

```bash
# HTTP security headers and TLS
python3 scripts/run_audit.py audit headers
python3 scripts/run_audit.py audit tls

# Cookies and session tokens
python3 scripts/run_audit.py audit cookies
python3 scripts/run_audit.py audit session

# Security misconfiguration
python3 scripts/run_audit.py audit misconfig

# Dependency review
python3 scripts/run_audit.py audit dependencies --manifest requirements.txt

# Local secrets scan
python3 scripts/run_audit.py audit secrets --scan src/

# API specification review
python3 scripts/run_audit.py audit api --spec openapi.yaml
```

### Run a specific tool subset

```bash
python3 scripts/run_audit.py audit full --tools headers,tls,cookies
```

Supported tool identifiers: `headers`, `tls`, `cookies`, `session`, `misconfig`, `auth`, `rbac`, `input`, `crawl`, `dependencies`, `api`, `secrets`

---

## 6. Generate Reports

Once findings are written to the register, generate reports:

```bash
# Technical report (for engineers)
python3 scripts/run_audit.py report technical

# Executive summary (non-technical)
python3 scripts/run_audit.py report executive

# Prioritized remediation plan
python3 scripts/run_audit.py report remediation
```

Reports are written to `engagements/<ENGAGEMENT_ID>/reports/draft/`.

---

## 7. Using Claude Commands (Intelligence Layer)

If you are working interactively with Claude Code, use the slash commands instead of (or alongside) the Python CLI:

| Task | Command |
|------|---------|
| Start a new session | `/start-session` |
| Full structured audit | `/audit-full-website` |
| Headers and TLS review | `/review-headers` |
| Authentication review | `/review-auth` |
| Session and JWT review | `/review-session` |
| RBAC and IDOR review | `/review-rbac` |
| Input validation review | `/review-input-validation` |
| Misconfiguration review | `/review-misconfig` |
| Dependency review | `/review-dependencies` |
| Generate report | `/generate-report` |
| Generate remediation plan | `/generate-remediation-plan` |
| Close a finding | `/close-finding` |

Claude commands always read the context files first before executing.

---

## 8. Workspace Layout

```
appsec-ai-platform/
├── .claude/
│   ├── context/          # Pointer to active engagement (active.md)
│   ├── commands/         # Slash command definitions (global)
│   ├── rules/            # Governance rules (evidence, scope, severity, safety)
│   ├── skills/           # Domain-specific review intelligence (global)
│   └── templates/        # Normalized output templates (global)
├── engagements/          # All per-engagement working data
│   ├── _template/        # Blank template — copy to start a new engagement
│   └── AUDIT-YYYY-CLIENT-NNN/
│       ├── context/      # Scope, authorization, target profile, assumptions
│       ├── audit-runs/   # Session records and findings register
│       │   ├── active/
│       │   └── completed/
│       ├── evidence/     # raw/, reviewed/, summarized/
│       ├── reports/      # draft/, final/
│       └── audits/       # weekly/, monthly/, quarterly/, release/, annual/
├── src/                  # Python automation layer
│   ├── tools/            # Domain audit tools (headers, tls, cookies, etc.)
│   ├── workflows/        # full_audit.py, passive_web_audit.py
│   ├── models/           # Typed entities: Finding, Evidence, AuditRun
│   ├── policies/         # Authorization and stop condition enforcement
│   ├── parsers/          # Cookie, JWT, HTML, OpenAPI, manifest parsers
│   ├── reporting/        # Report generator
│   └── utils/            # Evidence writer, findings writer, context reader
├── scripts/
│   ├── run_audit.py      # Primary CLI entry point
│   └── create_engagement.py  # Engagement bootstrap tool
├── tests/                # Unit tests
├── docs/                 # Extended documentation
└── requirements.txt
```

---

## 9. Safety Reminders

- **Authorization first.** No audit activity without `Authorization Status: CONFIRMED` in `audit-context.md`.
- **Passive by default.** Active testing (injection payloads, IDOR testing, brute force) requires explicit documented authorization.
- **Production is passive only** unless explicitly stated otherwise in scope.
- **Stop conditions apply.** The platform halts if unexpected sensitive data (credentials, PCI, PHI, private keys) or indicators of active compromise are discovered.
- **Evidence required.** No confirmed finding without an `EVID-YYYY-MM-DD-NNN` labeled evidence item.

---

## 10. Next Steps

- [docs/project-overview.md](docs/project-overview.md) — platform purpose and design
- [docs/cli-and-workflows.md](docs/cli-and-workflows.md) — full CLI reference
- [docs/architecture.md](docs/architecture.md) — module architecture
- [docs/configuration.md](docs/configuration.md) — all configuration options
- [docs/troubleshooting.md](docs/troubleshooting.md) — common issues
- [.claude/CLAUDE.md](.claude/CLAUDE.md) — full operating model and governance rules
