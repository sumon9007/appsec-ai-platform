# Analysis Prompts

Reusable reasoning helpers for domain-specific security analysis.

---

## Headers and TLS Analysis

**Objective:** Evaluate HTTP security headers and TLS configuration for the target.

**Review:**
- Strict-Transport-Security (HSTS max-age, includeSubDomains, preload)
- Content-Security-Policy (directives, unsafe-inline, unsafe-eval, wildcards)
- X-Frame-Options (DENY or SAMEORIGIN)
- X-Content-Type-Options (nosniff)
- Referrer-Policy (strict-origin or stricter)
- Permissions-Policy (unnecessary features disabled)
- TLS version (1.2 minimum, 1.3 preferred)
- Certificate validity, expiry, chain

**Output per issue:** header name, observed value or absence, risk, severity, remediation.

**Python CLI:** `python scripts/run_audit.py audit headers` and `audit tls`

---

## Authentication Analysis

**Objective:** Analyze the authentication model of the target application.

**Review:**
- Login flow and error messaging (enumerate usernames?)
- Password reset flow (token expiry, one-time use, account oracle)
- MFA presence and coverage (admin accounts, all roles)
- Account lockout and rate limiting
- Session cookie security on login
- Admin access protection

**Output:** confirmed observations, suspected weaknesses, review gaps — each with confidence label.

**Python CLI:** `python scripts/run_audit.py audit full --tools auth`

---

## RBAC and Authorization Analysis

**Objective:** Assess role-based access control and IDOR exposure.

**Review:**
- Role definitions and privilege levels
- Horizontal access control (can User A access User B's objects?)
- Vertical escalation (can standard user reach admin functions?)
- Object reference predictability (sequential IDs, GUIDs, URL parameters)
- API endpoint enforcement (same checks on API as on UI)

**Output:** test matrix with role × resource combinations, confirmed findings, review gaps.

**Python CLI:** `python scripts/run_audit.py audit full --tools rbac`

---

## Input Validation Analysis

**Objective:** Assess input validation posture and injection risk surface.

**Review:**
- Input fields accepting HTML/script content (XSS surface)
- SQL/NoSQL query construction with user input
- File upload handling and validation
- URL/path parameters used in server-side operations (SSRF, path traversal)
- Server-side template injection indicators

**Output:** injection surface map, confirmed passive findings, areas requiring active validation.

**Python CLI:** `python scripts/run_audit.py audit full --tools input`

---

## Dependency Analysis

**Objective:** Identify known CVEs and supply chain risks in third-party dependencies.

**Review:**
- All direct and transitive dependencies in manifest files
- CVE matches via OSV.dev
- Package maintenance status (last release, open issues, abandonment indicators)
- License risks

**Output:** CVE findings with CVSS score, severity, affected version, fixed version, exploitability context.

**Python CLI:** `python scripts/run_audit.py audit dependencies --manifest requirements.txt`

---

## Logging and Monitoring Analysis

**Objective:** Assess whether the application logs security-relevant events at sufficient quality.

**Review:**
- Authentication events (login success/failure, logout, MFA events)
- Authorization failures (403s, access denied)
- Input validation failures and suspicious inputs
- Admin actions and privilege changes
- PII in logs (must be absent or masked)
- Log integrity and retention

**Output:** coverage assessment per event category, gaps, recommendations.

**Note:** No Python tool yet — manual review required.
