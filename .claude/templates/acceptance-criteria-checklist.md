# Acceptance Criteria Checklist

Used during release gate reviews and quarterly audits to determine if the application meets minimum security standards for each domain.

**Application:** [PLACEHOLDER]
**Assessment Date:** [PLACEHOLDER — YYYY-MM-DD]
**Assessor:** [PLACEHOLDER]
**Audit Type:** [PLACEHOLDER — Quarterly / Release Gate]

---

## How to Use

For each domain, work through the criteria and mark Pass, Fail, or N/A. Record the finding ID for any Fail items. A domain FAILS the acceptance check if any Must-Fix item is marked Fail.

Reference: `.claude/docs/acceptance-criteria.md` for full definitions and thresholds.

---

## Domain 1: Authentication & Access Control

| Criteria | Status | Finding ID | Notes |
|----------|--------|------------|-------|
| No Critical or High authentication findings open | [PASS / FAIL] | [FIND-NNN or —] | |
| MFA enforced for all privileged/admin accounts | [PASS / FAIL / N/A] | [FIND-NNN or —] | |
| Password reset tokens are single-use and expire ≤ 1 hour | [PASS / FAIL / UNKNOWN] | [FIND-NNN or —] | |
| Login does not enumerate valid usernames | [PASS / FAIL] | [FIND-NNN or —] | |
| Rate limiting on login and password reset endpoints | [PASS / FAIL] | [FIND-NNN or —] | |

**Domain 1 Result:** [PASS / FAIL]
**Must-Fix items failing:** [List FIND-NNN or "None"]

---

## Domain 2: Authorization / RBAC

| Criteria | Status | Finding ID | Notes |
|----------|--------|------------|-------|
| No Critical or High authorization findings open | [PASS / FAIL] | [FIND-NNN or —] | |
| Server-side authorization checks present on sensitive functions | [PASS / FAIL] | [FIND-NNN or —] | |
| IDOR testing reveals no unauthorized cross-user data access | [PASS / FAIL] | [FIND-NNN or —] | |
| Role permissions match documented design intent | [PASS / FAIL / UNKNOWN] | [FIND-NNN or —] | |

**Domain 2 Result:** [PASS / FAIL]
**Must-Fix items failing:** [List FIND-NNN or "None"]

---

## Domain 3: Session Management

| Criteria | Status | Finding ID | Notes |
|----------|--------|------------|-------|
| No Critical or High session findings open | [PASS / FAIL] | [FIND-NNN or —] | |
| Session token entropy ≥ 128 bits | [PASS / FAIL / UNKNOWN] | [FIND-NNN or —] | |
| JWT algorithm is RS256, ES256, or equivalent (not `alg: none`) | [PASS / FAIL / N/A] | [FIND-NNN or —] | |
| JWT `exp` claim present and enforced | [PASS / FAIL / N/A] | [FIND-NNN or —] | |
| Session cookies: HttpOnly, Secure, SameSite flags present | [PASS / FAIL] | [FIND-NNN or —] | |
| Session invalidated on logout (server-side) | [PASS / FAIL] | [FIND-NNN or —] | |

**Domain 3 Result:** [PASS / FAIL]
**Must-Fix items failing:** [List FIND-NNN or "None"]

---

## Domain 4: Input Validation & Injection

| Criteria | Status | Finding ID | Notes |
|----------|--------|------------|-------|
| No Critical or High injection findings open | [PASS / FAIL] | [FIND-NNN or —] | |
| Database queries use parameterized queries or ORM | [PASS / FAIL / UNKNOWN] | [FIND-NNN or —] | |
| HTML output encoded to prevent XSS | [PASS / FAIL / UNKNOWN] | [FIND-NNN or —] | |
| File uploads: MIME type validated server-side | [PASS / FAIL / N/A] | [FIND-NNN or —] | |
| No path traversal vulnerabilities found | [PASS / FAIL] | [FIND-NNN or —] | |

**Domain 4 Result:** [PASS / FAIL]
**Must-Fix items failing:** [List FIND-NNN or "None"]

---

## Domain 5: Security Headers & Transport

| Criteria | Status | Finding ID | Notes |
|----------|--------|------------|-------|
| HTTPS enforced application-wide; no mixed content | [PASS / FAIL] | [FIND-NNN or —] | |
| HSTS present with max-age ≥ 15768000 | [PASS / FAIL] | [FIND-NNN or —] | |
| X-Content-Type-Options: nosniff present | [PASS / FAIL] | [FIND-NNN or —] | |
| Clickjacking protection present (X-Frame-Options or CSP frame-ancestors) | [PASS / FAIL] | [FIND-NNN or —] | |
| TLS 1.2 minimum; TLS 1.0 and 1.1 disabled | [PASS / FAIL] | [FIND-NNN or —] | |
| Certificate valid with > 30 days to expiry | [PASS / FAIL] | [FIND-NNN or —] | |
| CORS not configured with wildcard + credentials | [PASS / FAIL] | [FIND-NNN or —] | |

**Domain 5 Result:** [PASS / FAIL]
**Must-Fix items failing:** [List FIND-NNN or "None"]

---

## Domain 6: Dependency / Supply Chain

| Criteria | Status | Finding ID | Notes |
|----------|--------|------------|-------|
| No Critical CVEs with fix available in direct dependencies | [PASS / FAIL] | [FIND-NNN or —] | |
| No actively exploited vulnerabilities (CISA KEV) regardless of severity | [PASS / FAIL] | [FIND-NNN or —] | |
| All production dependencies actively maintained (release within 24 months) | [PASS / FAIL] | [FIND-NNN or —] | |

**Domain 6 Result:** [PASS / FAIL]
**Must-Fix items failing:** [List FIND-NNN or "None"]

---

## Domain 7: Logging & Monitoring

| Criteria | Status | Finding ID | Notes |
|----------|--------|------------|-------|
| Authentication events (success and failure) are logged | [PASS / FAIL / UNKNOWN] | [FIND-NNN or —] | |
| Authorization failures are logged | [PASS / FAIL / UNKNOWN] | [FIND-NNN or —] | |
| Admin actions are logged | [PASS / FAIL / UNKNOWN] | [FIND-NNN or —] | |
| No credentials or PII inadvertently in logs | [PASS / FAIL / UNKNOWN] | [FIND-NNN or —] | |
| Log retention meets minimum compliance requirement | [PASS / FAIL / UNKNOWN] | [FIND-NNN or —] | |
| Alerting on high-frequency authentication failures | [PASS / FAIL / UNKNOWN] | [FIND-NNN or —] | |

**Domain 7 Result:** [PASS / FAIL]
**Must-Fix items failing:** [List FIND-NNN or "None"]

---

## Domain 8: Security Misconfiguration

| Criteria | Status | Finding ID | Notes |
|----------|--------|------------|-------|
| Debug mode disabled in production | [PASS / FAIL] | [FIND-NNN or —] | |
| Verbose error messages not exposed to users | [PASS / FAIL] | [FIND-NNN or —] | |
| No default credentials on any accessible interface | [PASS / FAIL] | [FIND-NNN or —] | |
| No unprotected admin interfaces from internet | [PASS / FAIL] | [FIND-NNN or —] | |
| No sensitive files accessible (.env, .git, backup.*) | [PASS / FAIL] | [FIND-NNN or —] | |

**Domain 8 Result:** [PASS / FAIL]
**Must-Fix items failing:** [List FIND-NNN or "None"]

---

## Overall Acceptance Decision

| Domain | Result |
|--------|--------|
| 1. Authentication | [PASS / FAIL] |
| 2. Authorization / RBAC | [PASS / FAIL] |
| 3. Session Management | [PASS / FAIL] |
| 4. Input Validation | [PASS / FAIL] |
| 5. Headers & Transport | [PASS / FAIL] |
| 6. Dependencies | [PASS / FAIL] |
| 7. Logging & Monitoring | [PASS / FAIL] |
| 8. Misconfiguration | [PASS / FAIL] |

**Overall Gate Decision:** [PASS / CONDITIONAL PASS / FAIL]

**Conditions (if Conditional Pass):**
[PLACEHOLDER — List conditions that must be met]

**Rationale:**
[PLACEHOLDER — Brief explanation of the gate decision]

**Assessed By:** [PLACEHOLDER]
**Date:** [PLACEHOLDER]

---

*Template: acceptance-criteria-checklist.md*
*Reference: .claude/docs/acceptance-criteria.md*
