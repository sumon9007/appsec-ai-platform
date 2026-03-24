# Gap Analysis

> **Last reviewed:** March 2026. Reflects code state in `src/` and methodology state in `.claude/`.

This document describes what is missing, partially wired, or not yet automated in the platform. It is distinct from the roadmap — it describes the current gap, not the planned solution.

---

## Summary

The platform delivers strong passive assessment, structured evidence, normalized findings, and draft report generation. The primary gaps are in authenticated end-to-end workflows, active testing orchestration, and engineering AppSec extensions.

---

## Partially Wired — Code Exists but Is Not Complete

### Authenticated session workflows

`CredentialStore` and `SessionManager` exist and are functional in isolation, but the main audit workflows (`full_audit.py`, tool classes) do not yet use them end-to-end. The result is that auth, RBAC, session, and API tools run in unauthenticated mode and produce review gaps for any controls that require a logged-in session.

**Impact:** Auth, RBAC, and session findings are limited to what is observable without credentials. Controls that only surface after login (e.g. session invalidation, role boundaries, authenticated API behavior) cannot be confirmed.

### Active testing execution

The authorization and stop-condition policy layer is in place. The `AuthorizationGrant.mode` supports `ACTIVE` mode and the gating logic works. However, no tool currently executes injection payloads, brute-force sequences, or exploit chains when active mode is granted — the tools observe and flag, but do not probe.

**Impact:** Input validation, RBAC, and auth findings are passive observations only. Confirming injection vulnerabilities requires manual testing with appropriate authorization.

### Stop-condition enforcement

Stop conditions are defined as policy functions in `src/policies/stop_conditions.py` and work correctly when called. However, they are not called uniformly by every tool — enforcement depends on each tool calling the check rather than a centralized pipeline-wide safeguard.

**Impact:** A tool that doesn't call the check could continue processing after encountering sensitive data or active compromise indicators.

### Run-state and resume semantics

Run-state JSON is persisted to `audit-runs/active/` by `RunStore`. The structure tracks which findings were written per run, but there is no CLI command to resume a partially completed audit from a saved state. A failed mid-run audit must be restarted from the beginning.

**Impact:** Long audits against large sites cannot be resumed after a failure.

---

## Missing — No Implementation Present

### Engineering AppSec extensions

| Missing Capability | Notes |
|-------------------|-------|
| SAST integration | No static code analysis module or integration with Semgrep, Bandit, or similar tools |
| IaC scanning | No Terraform, CloudFormation, or Kubernetes manifest review |
| Container image scanning | No integration with Trivy, Grype, or similar |
| Cloud posture checks | No AWS/Azure/GCP configuration review |
| SBOM generation | No software bill of materials workflow |
| CI/CD security policy gates | No pipeline-native enforcement beyond documentation |

### Logging and monitoring automation

A `logging-monitoring-audit` skill exists in `.claude/skills/` with a review methodology and checklist. There is no corresponding `src/tools/logging_audit.py` module. Logging and monitoring review is skill-guided and manual only.

### Identity management testing

| Missing Capability | Notes |
|-------------------|-------|
| Username enumeration | No automated account discovery or timing-based enumeration |
| Account lifecycle review | No password reset flow, account lockout, or registration abuse testing |
| MFA bypass patterns | No automated MFA enumeration or bypass probing |

### Business logic testing

No stateful workflow engine, abuse-case modeling, or privilege-chain testing. Business logic testing requires application-specific knowledge and is not a general-purpose automation target, but no framework exists to support it even with manual guidance.

### Client-side security review

HTML inventory and security header signals (CSP, X-Frame-Options) are assessed passively. There is no DOM source/sink analysis, browser storage review, or JavaScript-specific security analysis beyond what is visible in HTTP responses.

### Stored cryptography review

No review of how the application stores or handles cryptographic keys, encrypted data at rest, or password hashing schemes.

---

## Documentation Gaps

| Gap | Detail |
|-----|--------|
| Credential env vars not in `.env.example` | `AUDIT_USERNAME_<ROLE>`, `AUDIT_PASSWORD_<ROLE>`, and `AUDIT_MFA_<ROLE>` are used by `CredentialStore` but were not documented in the environment template until March 2026 |
| ACTIVE_ENGAGEMENT not in older guides | Several older setup guides did not document the engagement isolation env var |
| `audit auth`, `audit rbac`, `audit input` commands implied but don't exist | These domain-specific CLI commands do not exist — use `audit full --tools <name>` instead |

---

## Practical Impact Statement

For external passive security assessments of web applications where only a public URL is available, the platform covers the majority of observable controls well. All transport, session, dependency, misconfiguration, and crawl-based findings can be produced without authenticated access.

For assessments requiring authenticated access, active testing, or code/infrastructure review, the platform's coverage is partial. The governance layer (rules, skills, evidence standards) applies in all cases, but automated execution is limited to what can be observed passively.
