# AppSec AI Platform Coverage Matrix

This document maps the current `appsec-ai-platform` workspace against common web application security testing expectations, using OWASP WSTG and OWASP ASVS as the primary reference frames.

It is intended to answer one practical question:

**Does this platform currently cover complete web application security assessment and testing?**

**Short answer:** No, not yet.

The platform has strong governance, reporting, and passive transport-security foundations, but only a narrow portion of full web application security testing is currently executable.

---

## Current Maturity Summary

| Area | Current Status | Notes |
|------|----------------|------|
| Engagement governance | Strong | Authorization, scope, evidence, and reporting are well defined in `.claude/` |
| Passive transport security | Implemented | HTTP security headers and TLS checks are runnable |
| Reporting and evidence management | Implemented | Findings register, evidence store, session records, draft reports |
| Authentication testing | Planned only | Skill exists, no runnable implementation yet |
| Authorization / RBAC / IDOR | Planned only | Methodology exists, no executable testing yet |
| Session / JWT / cookie security | Planned only | No implemented runner yet |
| Input validation / injection testing | Planned only | No active or passive validation engine yet |
| API security testing | Missing | No API discovery/auth/schema test workflow yet |
| Dependency / supply chain testing | Planned only | No working CVE scan workflow yet |
| Logging / monitoring review | Planned only | No implemented collector or review automation |
| Security misconfiguration review | Partial | Passive surface review only, primarily headers/TLS-adjacent today |
| Authenticated testing | Missing | No test-account/session orchestration yet |
| Active testing controls | Partial | Governance rules exist; active execution layer does not |
| SAST / secrets / IaC / container / cloud checks | Missing | Outside current executable implementation |

---

## Executable Coverage Today

The following areas are currently implemented in code:

| Capability | Implementation |
|-----------|----------------|
| Passive HTTP security header assessment | `src/tools/headers_audit.py` |
| Passive TLS and certificate review | `src/tools/tls_audit.py` |
| Authorization and scope gating | `src/utils/context_reader.py` + `.claude/context/` |
| Evidence writing | `src/utils/evidence_writer.py` |
| Findings register management | `src/utils/findings_writer.py` |
| Passive audit workflow runner | `src/workflows/passive_web_audit.py` |
| CLI entrypoint | `src/cli.py` and `scripts/run_audit.py` |
| Draft reporting workflow support | `reports/`, `.claude/templates/`, `.claude/skills/report-writer/` |

---

## OWASP WSTG Mapping

Status values:

- `Implemented` = runnable in code today
- `Partial` = partially covered by workflow/rules or a narrow passive slice
- `Planned` = methodology exists in skills/docs, but no real execution layer
- `Missing` = not materially present yet

| WSTG Domain | Status | Notes |
|------------|--------|------|
| Information Gathering | Partial | Context loading exists, but no crawler, endpoint inventory, tech fingerprinting engine, or attack-surface enumeration |
| Configuration and Deployment Management Testing | Partial | Security header and TLS review implemented; broader deployment/config review missing |
| Identity Management Testing | Missing | No username enumeration, account lifecycle, or identity workflow testing |
| Authentication Testing | Planned | Methodology exists in `.claude/skills/auth-access-audit/`, but no runnable implementation |
| Authorization Testing | Planned | RBAC/IDOR skill exists, but no executable testing framework |
| Session Management Testing | Planned | Session/JWT skill exists; no runner or parser implemented |
| Input Validation Testing | Planned | Methodology exists, but no payload engine, passive parser, or validation workflow |
| Error Handling Testing | Missing | No collection or analysis workflow for error exposure or exception paths |
| Weak Cryptography Testing | Partial | TLS and certificate posture covered; application crypto/storage crypto not covered |
| Business Logic Testing | Missing | No stateful workflow modeling or abuse-case engine |
| Client-Side Testing | Partial | CSP/header observations only; no JavaScript source/sink, DOM, or storage review |
| API Testing | Missing | No OpenAPI ingestion, endpoint fuzzing, auth, schema validation, or token handling |

---

## OWASP ASVS Mapping

| ASVS Area | Status | Notes |
|----------|--------|------|
| V1 Architecture, Design and Threat Modeling | Missing | No threat-model workflow or architecture-control verification yet |
| V2 Authentication | Planned | Skill-level guidance exists, no execution layer |
| V3 Session Management | Planned | Not implemented in code yet |
| V4 Access Control | Planned | No runnable RBAC/IDOR checks yet |
| V5 Validation, Sanitization and Encoding | Planned | No input-validation engine yet |
| V6 Stored Cryptography | Missing | No review of crypto at rest, key handling, or secrets use |
| V7 Error Handling and Logging | Planned | Guidance exists, implementation missing |
| V8 Data Protection | Missing | No automated review of sensitive data handling/storage/transport beyond TLS |
| V9 Communications | Partial | Transport security posture implemented via headers/TLS checks |
| V10 Malicious Code | Missing | No malware/upload abuse scanning or anti-automation checks |
| V11 Business Logic | Missing | No business-workflow abuse modeling or validation |
| V12 Files and Resources | Missing | No file upload, path traversal, or resource access testing yet |
| V13 API and Web Service | Missing | No API security testing framework yet |
| V14 Configuration | Partial | Narrow passive hardening checks only |

---

## Skill And Code Alignment

The workspace has stronger **planned domain coverage** than **implemented coverage**.

### Defined in skills/templates, but not yet executable

| Domain | Skill Path | Execution Status |
|-------|------------|------------------|
| Authentication & Access Control | `.claude/skills/auth-access-audit/` | Planned |
| Authorization / RBAC | `.claude/skills/rbac-audit/` | Planned |
| Session / JWT | `.claude/skills/session-jwt-audit/` | Planned |
| Input Validation / Injection | `.claude/skills/input-validation-audit/` | Planned |
| Dependency Audit | `.claude/skills/dependency-audit/` | Planned |
| Logging / Monitoring | `.claude/skills/logging-monitoring-audit/` | Planned |
| Security Misconfiguration | `.claude/skills/security-misconfig-audit/` | Planned |
| Report Writing | `.claude/skills/report-writer/` | Partial, because reports are supported but still mostly template-driven |

### Implemented in code

| Domain | Code Path | Execution Status |
|-------|-----------|------------------|
| Security Headers | `src/tools/headers_audit.py` | Implemented |
| TLS / Certificate | `src/tools/tls_audit.py` | Implemented |
| Passive workflow orchestration | `src/workflows/passive_web_audit.py` | Implemented |

---

## Gap Analysis

The platform does **not** yet qualify as a complete web application security assessment platform because the following major capability groups are still absent:

### 1. Authenticated assessment

- No login/session orchestration
- No test-account handling
- No multi-role workflow support
- No per-role evidence capture

### 2. Core vulnerability testing

- No IDOR / RBAC enforcement checks
- No session fixation / cookie / JWT review engine
- No XSS / SQLi / SSRF / command injection workflows
- No file upload abuse testing
- No CSRF testing

### 3. Attack surface discovery

- No crawler
- No route inventory
- No passive API discovery
- No technology inventory beyond simple response observations

### 4. API security

- No OpenAPI or Postman collection ingestion
- No schema-aware request validation
- No auth token lifecycle testing
- No API access-control review

### 5. Broader engineering security checks

- No dependency scanner workflow
- No secrets scanning
- No SAST or IaC scanning integration
- No container or cloud posture modules
- No logging/monitoring validation automation

---

## Completion Estimate

Current implementation maturity against a practical web app assessment platform:

| Category | Approximate Completion |
|----------|------------------------|
| Governance and safety model | 80-90% |
| Reporting and audit artifacts | 70-80% |
| Executable passive testing | 25-35% |
| Executable authenticated/active testing | 0-10% |
| Overall end-to-end web app security assessment coverage | 20-30% |

---

## Recommended Roadmap

### Phase 1: Expand passive coverage

1. Add crawler and route discovery
2. Add cookie/session/JWT passive parser
3. Add broader misconfiguration checks
4. Add dependency/CVE automation

### Phase 2: Add authenticated workflows

1. Test account/session management
2. Auth flow review runner
3. RBAC and IDOR workflow engine
4. API authentication and token handling

### Phase 3: Add controlled active testing

1. Payload-safe input validation engine with authorization gates
2. XSS, SQLi, SSRF, and file upload validation workflows
3. CSRF and business-logic testing support
4. Replayable run state and approvals model

### Phase 4: Broaden AppSec platform scope

1. Secrets scanning
2. SAST integration
3. IaC scanning
4. Container and cloud posture review
5. Remediation SLA automation and trend reporting

---

## Recommended Near-Term Priorities

If the goal is to make this platform meaningfully useful as an agentic AppSec tool soon, the best next build order is:

1. Session / cookie / JWT analysis
2. Crawler and endpoint inventory
3. Authenticated request/session support
4. RBAC / IDOR workflow
5. Input validation and injection testing
6. API security workflow
7. Dependency/CVE automation

---

## Verdict

**Current verdict:** This platform does **not yet** cover complete web application security assessment and testing.

It **does** provide:

- a strong audit operating model
- safe authorization and scope controls
- structured evidence and reporting
- a real passive transport-security workflow

It **still needs** major execution coverage across authentication, authorization, sessions, input validation, APIs, dependencies, misconfiguration, and authenticated/active testing before it can be considered complete.
