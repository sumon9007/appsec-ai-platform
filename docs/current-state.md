# Current State

> **Snapshot notice:** This document was last verified against the codebase in March 2026. It accurately reflects the Python automation layer (`src/`). The per-engagement isolation model (`engagements/<ID>/`) was introduced after this snapshot — see `engagements/README.md` and `.claude/CLAUDE.md` for the current operating model.

## Verified Implementation Summary

The repository contains a functional Python CLI with working workflows, storage, evidence writing, findings serialization, and report generation. The strongest verified areas are:

- CLI and command routing in `scripts/run_audit.py` and `src/cli.py`
- Authorization loading and enforcement
- Passive audit workflows
- Evidence and findings writing
- Report generation
- Core parsers for cookies, JWTs, manifests, HTML, and API specs

## Current Maturity

| Area | Status | Code-backed Notes |
|------|--------|-------------------|
| Governance model | Strong | `.claude/` context, rules, skills, and templates are extensive |
| CLI and workflows | Implemented | `audit`, `report`, and `session` groups are present |
| Passive assessment | Implemented | Headers, TLS, cookies, JWTs, crawl, misconfig, API spec analysis |
| Dependency and secrets review | Implemented | File-based workflows exist |
| Findings and reporting | Implemented | Findings register and draft reports are generated |
| Run-state persistence | Implemented | Single JSON run-state file is written |
| Authenticated testing support | Partial | Credential/session abstractions exist, but full workflows do not use them end-to-end |
| Active testing | Partial | Authorization gate exists; most tools remain passive or emit review gaps |
| Engineering AppSec extensions | Missing | No SAST, IaC, container, or cloud modules |

## Documentation Validation Summary

### Verified claims

- The project has a working Python automation layer.
- Typed models, a run-state store, authorization policy checks, and report generation exist.
- Passive headers/TLS, dependency review, secrets scanning, API spec parsing, and evidence-backed findings are implemented.

### Partially verified claims

- Authenticated assessment support is present in abstractions, but not fully orchestrated in primary workflows.
- RBAC, authentication, and input validation domains exist as tools, but much of their output is passive observation or review-gap guidance rather than complete active validation.
- Stop conditions are implemented in policy code, but not consistently enforced across all tools/workflows.

### Unverified claims

- Broad claims of complete OWASP domain coverage are not fully substantiated by tests or end-to-end workflow behavior.
- Resume-safe workflows are only lightly supported through one active run-state JSON file rather than robust resumable orchestration.

### Incorrect or outdated claims

- Older docs state that direct `audit auth`, `audit rbac`, and `audit input` CLI commands exist. The current CLI does not expose those commands directly.
- Existing coverage docs describe a “broad passive-through-active tool set.” The codebase is still primarily passive, with active behavior mostly deferred behind policy language and review gaps.
- The current `docs/coverage-matrix.md` overstates overall maturity relative to the implementation.

### Missing documentation for code that exists

- The current repository includes `report` and `session` CLI groups that deserve more explicit documentation.
- The existing docs underplay the significance of the report generator, run-store behavior, and the exact structure of evidence and findings output.

## Practical Completion Estimate

Assumption: “complete web application security assessment platform” means a platform with mature passive, authenticated, active, API, and engineering AppSec coverage.

On that basis, the current codebase appears roughly:

- Strong for passive assessment and reporting
- Emerging for authenticated and authorization-aware testing
- Limited for active exploitation workflows
- Minimal for engineering AppSec extensions

A practical overall estimate is roughly `55-70%` toward that target state, depending on how much weight is placed on active and engineering AppSec coverage.
