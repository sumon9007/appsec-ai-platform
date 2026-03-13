# AppSec AI Platform

`appsec-ai-platform` is a Python-based security audit workspace for authorized, evidence-driven web application assessments. It combines a runnable CLI and workflow engine in [`src/`](/home/suruz/claude-workspace/01-PROJECTS/appsec-ai-platform/src) with a governance layer in [`.claude/`](/home/suruz/claude-workspace/01-PROJECTS/appsec-ai-platform/.claude) for scope, authorization, evidence quality, reporting, and audit templates.

The current implementation is strongest in passive assessment and report generation. It includes runnable checks for headers, TLS, cookies, session/JWT observations, passive crawling, misconfiguration review, dependency review, API spec analysis, and local secrets scanning. It also includes scaffolding for authenticated testing support, authorization enforcement, and run-state persistence.

## Start Here

- Docs index: [docs/README.md](/home/suruz/claude-workspace/01-PROJECTS/appsec-ai-platform/docs/README.md)
- Current state: [docs/current-state.md](/home/suruz/claude-workspace/01-PROJECTS/appsec-ai-platform/docs/current-state.md)
- CLI and workflows: [docs/cli-and-workflows.md](/home/suruz/claude-workspace/01-PROJECTS/appsec-ai-platform/docs/cli-and-workflows.md)
- Coverage validation: [docs/coverage-matrix-verified.md](/home/suruz/claude-workspace/01-PROJECTS/appsec-ai-platform/docs/coverage-matrix-verified.md)
- Roadmap alignment: [docs/roadmap-alignment.md](/home/suruz/claude-workspace/01-PROJECTS/appsec-ai-platform/docs/roadmap-alignment.md)

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 scripts/run_audit.py session status
python3 scripts/run_audit.py audit full --dry-run
```

Before running any workflow, populate and verify:

- [audit-context.md](/home/suruz/claude-workspace/01-PROJECTS/appsec-ai-platform/.claude/context/audit-context.md)
- [scope.md](/home/suruz/claude-workspace/01-PROJECTS/appsec-ai-platform/.claude/context/scope.md)
- [target-profile.md](/home/suruz/claude-workspace/01-PROJECTS/appsec-ai-platform/.claude/context/target-profile.md)
- [assumptions.md](/home/suruz/claude-workspace/01-PROJECTS/appsec-ai-platform/.claude/context/assumptions.md)

## Main Commands

```bash
python3 scripts/run_audit.py audit full
python3 scripts/run_audit.py audit headers
python3 scripts/run_audit.py audit tls
python3 scripts/run_audit.py audit cookies
python3 scripts/run_audit.py audit session
python3 scripts/run_audit.py audit misconfig
python3 scripts/run_audit.py audit dependencies --manifest requirements.txt
python3 scripts/run_audit.py audit secrets --scan src/
python3 scripts/run_audit.py audit api --url https://target.example --spec openapi.yaml
python3 scripts/run_audit.py report technical
python3 scripts/run_audit.py report executive
python3 scripts/run_audit.py report remediation
```

## Safety

This repository is for lawful, authorized, defensive security review only.

- Authorization must be confirmed before audit activity begins.
- Passive review is the default mode.
- Active testing requires explicit documented authorization.
- Findings must be evidence-backed.
- Stop conditions apply if sensitive data or compromise indicators are detected.

See:

- [docs/project-overview.md](/home/suruz/claude-workspace/01-PROJECTS/appsec-ai-platform/docs/project-overview.md)
- [docs/auth-session-policies.md](/home/suruz/claude-workspace/01-PROJECTS/appsec-ai-platform/docs/auth-session-policies.md)
