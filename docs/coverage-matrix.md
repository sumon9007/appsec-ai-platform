# AppSec AI Platform Coverage Matrix

This document maps the current `appsec-ai-platform` workspace against common web application security testing expectations, using OWASP WSTG and OWASP ASVS as the primary reference frames.

It is intended to answer one practical question:

**Does this platform currently cover complete web application security assessment and testing?**

**Short answer:** Not yet — but Phases 1 through 3 are substantially complete.

The platform has strong governance, reporting, and a broad passive-through-active tool set. The remaining gaps are primarily in active-testing orchestration, authenticated multi-role workflows, and engineering AppSec extensions (SAST, IaC, container).

Last updated: 2026-03-13

---

## Current Maturity Summary

| Area | Current Status | Notes |
|------|----------------|------|
| Engagement governance | Strong | Authorization, scope, evidence, and reporting are well defined in `.claude/` |
| Core platform and persistence | Implemented | Typed models, run-state storage, policies, and CLI are in place |
| Passive transport security | Implemented | HTTP security headers and TLS checks are runnable |
| Crawler and route discovery | Implemented | `src/tools/crawler.py` — public endpoint enumeration |
| Cookie and session analysis | Implemented | `src/tools/cookie_audit.py`, `src/tools/session_jwt_audit.py` |
| JWT parsing and review | Implemented | `src/parsers/jwt_parser.py` |
| Dependency / CVE review | Implemented | `src/tools/dependency_audit.py`, `src/parsers/manifest.py` |
| Security misconfiguration review | Implemented | `src/tools/misconfig_audit.py` |
| Authentication review | Implemented | `src/tools/auth_audit.py`, `src/auth/credential_store.py` |
| RBAC and IDOR review | Implemented | `src/tools/rbac_audit.py` |
| Input validation / injection checks | Implemented | `src/tools/input_validation_audit.py` |
| API security assessment | Implemented | `src/tools/api_audit.py`, `src/parsers/openapi_parser.py` |
| Secrets scanning | Implemented | `src/tools/secrets_scan.py` |
| Authenticated session orchestration | Implemented | `src/session/session_manager.py` |
| Reporting and evidence management | Implemented | `src/reporting/report_generator.py`, findings register, evidence store, session records |
| Full audit workflow orchestration | Implemented | `src/workflows/full_audit.py` |
| Active testing controls and stop conditions | Implemented | `src/policies/authorization.py`, `src/policies/stop_conditions.py` |
| SAST integration | Missing | Outside current executable implementation |
| IaC scanning | Missing | Outside current executable implementation |
| Container / cloud posture | Missing | Outside current executable implementation |
| Identity management testing | Missing | No username enumeration or account lifecycle automation |
| Business logic testing | Missing | No stateful workflow abuse engine |

---

## Executable Coverage Today

The following areas are currently implemented in code:

| Capability | Implementation |
|-----------|----------------|
| Passive HTTP security header assessment | `src/tools/headers_audit.py` |
| Passive TLS and certificate review | `src/tools/tls_audit.py` |
| Public route and endpoint discovery | `src/tools/crawler.py` |
| Cookie attribute and security review | `src/tools/cookie_audit.py` |
| Session and JWT passive analysis | `src/tools/session_jwt_audit.py` |
| JWT parsing | `src/parsers/jwt_parser.py` |
| Dependency manifest review and CVE lookup | `src/tools/dependency_audit.py`, `src/parsers/manifest.py` |
| Security misconfiguration checks | `src/tools/misconfig_audit.py` |
| Authentication flow review | `src/tools/auth_audit.py` |
| RBAC and IDOR review | `src/tools/rbac_audit.py` |
| Input validation and injection checks | `src/tools/input_validation_audit.py` |
| API security assessment | `src/tools/api_audit.py`, `src/parsers/openapi_parser.py` |
| Secrets and credential scanning | `src/tools/secrets_scan.py` |
| HTML parsing and JS inventory | `src/parsers/html_parser.py` |
| Authenticated test credential handling | `src/auth/credential_store.py` |
| Authenticated session management | `src/session/session_manager.py` |
| Authorization mode enforcement | `src/policies/authorization.py` |
| Safety stop conditions | `src/policies/stop_conditions.py` |
| Core typed entities | `src/models/entities.py` |
| Run-state persistence | `src/storage/run_store.py` |
| Report generation | `src/reporting/report_generator.py` |
| Passive audit workflow | `src/workflows/passive_web_audit.py` |
| Full multi-domain audit workflow | `src/workflows/full_audit.py` |
| Authorization and scope gating | `src/utils/context_reader.py` + `.claude/context/` |
| Evidence writing | `src/utils/evidence_writer.py` |
| Findings register management | `src/utils/findings_writer.py` |
| CLI entrypoint | `src/cli.py` and `scripts/run_audit.py` |

---

## OWASP WSTG Mapping

Status values:

- `Implemented` = runnable in code today
- `Partial` = partially covered by workflow/rules or a narrow passive slice
- `Planned` = methodology exists in skills/docs, but no real execution layer
- `Missing` = not materially present yet

| WSTG Domain | Status | Notes |
|------------|--------|------|
| Information Gathering | Implemented | Crawler, endpoint inventory, tech fingerprinting via headers/response analysis — full attack-surface enumeration supported |
| Configuration and Deployment Management Testing | Implemented | Security headers, TLS, misconfiguration checks, secrets scan, dependency review |
| Identity Management Testing | Missing | No username enumeration, account lifecycle, or identity workflow testing |
| Authentication Testing | Implemented | Auth flow review, MFA presence, login behavior, lockout, session invalidation |
| Authorization Testing | Implemented | RBAC/IDOR review with horizontal and vertical access checks |
| Session Management Testing | Implemented | Cookie/session/JWT parsing and review, session manager |
| Input Validation Testing | Implemented | Input validation and injection check workflow in place; active payload execution requires explicit authorization |
| Error Handling Testing | Partial | Misconfiguration tool covers verbose error/stack trace leakage; no dedicated error-injection workflow |
| Weak Cryptography Testing | Partial | TLS/certificate posture fully covered; application crypto/storage crypto not covered |
| Business Logic Testing | Missing | No stateful workflow modeling or abuse-case engine |
| Client-Side Testing | Partial | CSP/header observations and HTML/JS inventory; no DOM source/sink or browser storage review engine |
| API Testing | Implemented | OpenAPI ingestion, API auth review, access-control checks, token handling |

---

## OWASP ASVS Mapping

| ASVS Area | Status | Notes |
|----------|--------|------|
| V1 Architecture, Design and Threat Modeling | Missing | No threat-model workflow or architecture-control verification yet |
| V2 Authentication | Implemented | Auth audit tool covers MFA, password policy, lockout, and session invalidation |
| V3 Session Management | Implemented | Cookie/JWT parsers and session audit tool in place |
| V4 Access Control | Implemented | RBAC and IDOR review workflow operational |
| V5 Validation, Sanitization and Encoding | Implemented | Input validation tool covers injection classes; active exploit execution requires authorization |
| V6 Stored Cryptography | Missing | No automated review of crypto-at-rest, key handling, or secrets storage patterns |
| V7 Error Handling and Logging | Partial | Misconfiguration tool covers error disclosure; full logging review is skill-guided only |
| V8 Data Protection | Partial | Transport security implemented; sensitive data handling/storage review not automated |
| V9 Communications | Implemented | TLS/certificate posture, security headers, HSTS enforcement all covered |
| V10 Malicious Code | Missing | No malware/upload abuse scanning or anti-automation checks |
| V11 Business Logic | Missing | No business-workflow abuse modeling or validation |
| V12 Files and Resources | Partial | File upload patterns reviewed in input validation tool; no dedicated path traversal or resource-access engine |
| V13 API and Web Service | Implemented | OpenAPI/Postman ingestion, API auth and access-control review, schema checks |
| V14 Configuration | Implemented | Misconfiguration tool, secrets scan, security headers, dependency review |

---

## Skill And Code Alignment

### Implemented in code and supported by skills

| Domain | Code Path | Skill Path |
|-------|-----------|------------|
| Security Headers and TLS | `src/tools/headers_audit.py`, `src/tools/tls_audit.py` | `.claude/skills/headers-tls-audit/` |
| Authentication and Access Control | `src/tools/auth_audit.py` | `.claude/skills/auth-access-audit/` |
| Authorization / RBAC | `src/tools/rbac_audit.py` | `.claude/skills/rbac-audit/` |
| Session / JWT | `src/tools/session_jwt_audit.py`, `src/tools/cookie_audit.py` | `.claude/skills/session-jwt-audit/` |
| Input Validation / Injection | `src/tools/input_validation_audit.py` | `.claude/skills/input-validation-audit/` |
| Dependency Audit | `src/tools/dependency_audit.py` | `.claude/skills/dependency-audit/` |
| Security Misconfiguration | `src/tools/misconfig_audit.py` | `.claude/skills/security-misconfig-audit/` |
| API Security | `src/tools/api_audit.py` | — |
| Secrets Scanning | `src/tools/secrets_scan.py` | — |
| Report Writing | `src/reporting/report_generator.py` | `.claude/skills/report-writer/` |

### Defined in skills/docs only — not yet automated in code

| Domain | Notes |
|-------|-------|
| Logging and Monitoring | Skill exists in `.claude/skills/logging-monitoring-audit/`; no collector or automated review |
| Business Logic Testing | No workflow present |
| Identity Management | No enumeration or account lifecycle automation |

---

## Remaining Gap Analysis

The platform is **substantially functional** for passive through controlled-active assessment. The remaining material gaps are:

### 1. Engineering AppSec extensions

- No SAST integration
- No IaC scanning
- No container image scanning
- No cloud posture checks

### 2. Authenticated active testing orchestration

- Active injection payloads require authorization-gated execution
- The authorization and stop-condition policy layer is in place; orchestrated multi-step active attack chains are not yet wired end-to-end

### 3. Specialized testing areas

- Identity management (username enumeration, account lifecycle)
- Business logic abuse cases
- DOM source/sink and client-side storage review
- Stored crypto and key-handling review
- Logging/monitoring automation

---

## Completion Estimate

Current implementation maturity against a practical web app assessment platform:

| Category | Approximate Completion |
|----------|------------------------|
| Governance and safety model | 90-95% |
| Reporting and audit artifacts | 80-85% |
| Executable passive testing | 85-90% |
| Executable authenticated testing | 70-80% |
| Executable active testing (authorization-gated) | 60-70% |
| Engineering AppSec extensions (SAST, IaC, container) | 0-10% |
| Overall end-to-end web app security assessment coverage | 65-75% |

---

## Recommended Next Priorities

Based on current gaps, the recommended next build order is:

1. Logging/monitoring automation (`src/tools/logging_audit.py`)
2. End-to-end active testing orchestration (wiring authorization gates to payload execution)
3. Secrets scanning integration with SAST tooling
4. IaC scanning module
5. Container and cloud posture checks
6. Business logic workflow support

---

## Verdict

**Current verdict:** This platform **substantially covers** passive and authenticated web application security assessment, and has working implementations across the majority of OWASP WSTG and ASVS domains.

It **does** provide:

- a strong audit operating model
- safe authorization and scope controls
- structured evidence and reporting
- passive transport, session, dependency, and misconfiguration workflows
- authenticated assessment with credential and session handling
- RBAC/IDOR, input validation, API security, and secrets scanning tools
- full multi-domain workflow orchestration

It **still needs**:

- engineering AppSec extensions (SAST, IaC, container, cloud)
- end-to-end active testing orchestration
- logging/monitoring automation
- identity management and business logic coverage
- client-side DOM and stored crypto review

Before it can be described as a complete application security platform.
