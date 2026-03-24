# Coverage Matrix — Verified

> **Last verified:** March 2026 against `src/`. Active testing is limited — most domains are passive-only unless explicitly authorized. Engineering AppSec domains (SAST, IaC, cloud) are not implemented.

This document is the authoritative coverage reference. It uses code-verified status labels only.

---

## Status Labels

| Label | Meaning |
|-------|---------|
| `Implemented` | Runnable in code today — produces findings or evidence |
| `Partial` | Code exists but coverage is limited, passive-only, or produces review gaps |
| `Skill-guided only` | Methodology defined in `.claude/skills/`; no automated execution |
| `Missing` | Not materially present — no code, no skill |

---

## OWASP WSTG Mapping

| WSTG Domain | Status | Notes |
|-------------|--------|-------|
| Information Gathering | Implemented | Passive crawler, HTML/JS inventory, tech fingerprinting via headers |
| Configuration and Deployment Management | Implemented | Headers, TLS, misconfig, dependency review, secrets scan |
| Identity Management | Missing | No username enumeration, account lifecycle, or identity workflow automation |
| Authentication Testing | Partial | Passive auth flow review exists; end-to-end authenticated validation is not complete |
| Authorization Testing | Partial | RBAC/IDOR tool exists; full multi-role active validation is limited |
| Session Management | Implemented | Cookie and JWT passive analysis; session abstractions in place |
| Input Validation Testing | Partial | Input surface analysis exists; active injection payload execution is not automated |
| Error Handling | Partial | Misconfig tool covers error disclosure; no dedicated error injection workflow |
| Weak Cryptography | Partial | TLS/certificate posture covered; application-layer crypto not reviewed |
| Business Logic | Missing | No stateful business-logic engine or abuse-case modeling |
| Client-Side Testing | Partial | HTML inventory and browser-policy header signals only; no DOM source/sink review |
| API Testing | Partial | OpenAPI/Postman spec parsing and passive API analysis; advanced abuse cases not covered |

---

## OWASP ASVS Mapping

| ASVS Area | Status | Notes |
|-----------|--------|-------|
| V1 Architecture, Design and Threat Modeling | Missing | No threat-model workflow or architecture-control verification |
| V2 Authentication | Partial | Some controls assessed passively; many depend on authenticated access or manual review |
| V3 Session Management | Implemented | JWT/cookie parsing and session abstractions cover core controls |
| V4 Access Control | Partial | RBAC/IDOR tooling exists; deep role-aware validation requires authenticated sessions |
| V5 Validation, Sanitization and Encoding | Partial | Heuristic surface analysis only; active payload execution not implemented |
| V6 Stored Cryptography | Missing | No crypto-at-rest review, key handling, or secrets storage analysis module |
| V7 Error Handling and Logging | Partial | Misconfig checks cover error disclosure; logging review is skill-guided only |
| V8 Data Protection | Partial | Transport security covered; sensitive data handling and storage review not automated |
| V9 Communications | Implemented | TLS, security headers, and HSTS enforcement all covered |
| V10 Malicious Code | Missing | No malware detection, upload abuse scanning, or anti-automation checks |
| V11 Business Logic | Missing | Not implemented |
| V12 Files and Resources | Partial | Some related checks in input validation tool; no dedicated path traversal engine |
| V13 API and Web Service | Partial | Passive and spec-oriented coverage; authenticated API abuse cases not complete |
| V14 Configuration | Implemented | Misconfiguration checks, secrets scan, security headers, dependency review |

---

## Skill and Code Alignment

### Implemented in code and supported by a skill

| Domain | Code Module | Skill |
|--------|-------------|-------|
| Security Headers and TLS | `src/tools/headers_audit.py`, `src/tools/tls_audit.py` | `.claude/skills/headers-tls-audit/` |
| Authentication Review | `src/tools/auth_audit.py` | `.claude/skills/auth-access-audit/` |
| Authorization / RBAC | `src/tools/rbac_audit.py` | `.claude/skills/rbac-audit/` |
| Session / JWT | `src/tools/session_jwt_audit.py`, `src/tools/cookie_audit.py` | `.claude/skills/session-jwt-audit/` |
| Input Validation | `src/tools/input_validation_audit.py` | `.claude/skills/input-validation-audit/` |
| Dependency Audit | `src/tools/dependency_audit.py`, `src/parsers/manifest.py` | `.claude/skills/dependency-audit/` |
| Security Misconfiguration | `src/tools/misconfig_audit.py` | `.claude/skills/security-misconfig-audit/` |
| Report Writing | `src/reporting/report_generator.py` | `.claude/skills/report-writer/` |

### Implemented in code — no dedicated skill yet

| Domain | Code Module |
|--------|-------------|
| API Security | `src/tools/api_audit.py`, `src/parsers/openapi_parser.py` |
| Secrets Scanning | `src/tools/secrets_scan.py` |
| Passive Web Crawl | `src/tools/crawler.py` |

### Skill-guided only — no automated code execution

| Domain | Skill | Gap |
|--------|-------|-----|
| Logging and Monitoring | `.claude/skills/logging-monitoring-audit/` | No collector or automated review module |
| PRD / Feature Security Review | `.claude/skills/prd-security-review/` | Design-time review only — no automation |
| Release Gate Review | `.claude/skills/release-gate-review/` | Human-in-loop decision — no automation |

### Missing — no code, no skill

| Domain |
|--------|
| SAST integration |
| IaC scanning |
| Container image scanning |
| Cloud posture checks |
| Business logic abuse modeling |
| Identity management / username enumeration |
| DOM source/sink and client-side storage review |
| Stored cryptography review |

---

## Platform Completion Estimate

Estimated maturity against a complete web application security assessment platform:

| Capability Area | Estimate |
|----------------|----------|
| Governance, authorization, and safety model | 90–95% |
| Reporting and audit artifact generation | 80–85% |
| Passive testing execution | 85–90% |
| Authenticated testing execution | 40–50% |
| Active testing execution (authorization-gated) | 20–30% |
| Engineering AppSec extensions (SAST, IaC, container, cloud) | 0–10% |
| **Overall end-to-end coverage** | **55–70%** |

> The 55–70% estimate assumes "complete" means covering passive, authenticated, active, API, and engineering AppSec domains. The platform is strong for passive assessment and reporting. Authenticated and active workflows exist as scaffolding but are not end-to-end.

---

## Recommended Next Build Order

1. Wire `SessionManager` and `CredentialStore` into auth, RBAC, session, and API audit workflows
2. Add a centralized stop-condition enforcement layer (currently per-tool, not pipeline-wide)
3. Build a minimal active probe engine with authorization gating
4. Add `src/tools/logging_audit.py` (logging/monitoring skill has no code counterpart)
5. Improve run-state tracking to capture evidence IDs and support resume semantics
6. Extend into engineering AppSec: SAST, IaC scanning
