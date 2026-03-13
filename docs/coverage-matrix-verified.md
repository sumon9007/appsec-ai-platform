# Coverage Matrix Verified

This document validates the platform’s claimed coverage against the current codebase.

## Verification Categories

- `Implemented in code`
- `Partial`
- `Documented but unverified`
- `Missing`

## Verified WSTG Mapping

| WSTG Domain | Status | Notes |
|------------|--------|------|
| Information Gathering | Implemented in code | Passive crawler and HTML inventory exist |
| Configuration and Deployment Management | Implemented in code | Headers, TLS, misconfig, dependency review, secrets scan |
| Identity Management | Missing | No dedicated identity lifecycle or enumeration module |
| Authentication Testing | Partial | Passive auth review exists; fully authenticated validation is not end-to-end |
| Authorization Testing | Partial | RBAC tool exists, but full multi-role active validation is limited |
| Session Management | Implemented in code | Cookie and JWT passive analysis plus session abstractions |
| Input Validation Testing | Partial | Input review logic exists; active probing engine is not complete |
| Error Handling | Partial | Misconfig checks likely cover disclosure; no dedicated workflow |
| Weak Cryptography | Partial | TLS coverage exists; application crypto is not covered |
| Business Logic | Missing | No stateful business-logic engine |
| Client-Side Testing | Partial | HTML inventory and browser-policy signals only |
| API Testing | Partial | Spec parsing and passive API analysis exist; advanced abuse cases remain limited |

## Verified ASVS Mapping

| ASVS Area | Status | Notes |
|----------|--------|------|
| V1 Architecture, Design and Threat Modeling | Missing | No threat-model workflow |
| V2 Authentication | Partial | Some controls assessed, many remain review-gap dependent |
| V3 Session Management | Implemented in code | JWT/cookie parsing and session abstractions |
| V4 Access Control | Partial | Tooling exists, but deep role-aware validation is limited |
| V5 Validation, Sanitization and Encoding | Partial | Heuristic coverage only |
| V6 Stored Cryptography | Missing | No crypto-at-rest review module |
| V7 Error Handling and Logging | Partial | Logging skill exists, automation is not present |
| V8 Data Protection | Partial | Transport and some evidence-safety controls exist |
| V9 Communications | Implemented in code | TLS and header controls are covered |
| V10 Malicious Code | Missing | No malware/upload abuse automation |
| V11 Business Logic | Missing | Not implemented |
| V12 Files and Resources | Partial | Some related checks exist, no dedicated traversal/resource engine |
| V13 API and Web Service | Partial | Passive/API-spec oriented coverage |
| V14 Configuration | Implemented in code | Misconfiguration and supporting checks exist |

## Existing Docs vs Code

### Implemented in code

- Headers/TLS
- Dependency audit
- Secrets scan
- Evidence writer
- Findings writer
- Report generation
- Run-state persistence

### Partial

- Authentication
- RBAC/IDOR
- Input validation
- API security
- Authenticated orchestration
- Active testing controls

### Documented but unverified

- Full broad active-testing coverage
- Mature resumable workflow handling
- Practical completeness across most OWASP domains

### Missing

- SAST
- IaC scanning
- container scanning
- cloud posture
- business-logic modeling
- identity-management testing
