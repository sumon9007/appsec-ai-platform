# Audit Domains

Defines all security audit domains covered by this workspace. Each domain includes a description, key risks, the skill used to audit it, and the relevant OWASP reference.

---

## Overview

| # | Domain | Skill | OWASP Category |
|---|--------|-------|----------------|
| 1 | Authentication & Access Control | `auth-access-audit` | A07:2021 |
| 2 | Authorization / RBAC | `rbac-audit` | A01:2021 |
| 3 | Session Management | `session-jwt-audit` | A02:2021 |
| 4 | Input Validation & Injection | `input-validation-audit` | A03:2021 |
| 5 | Security Headers & Transport | `headers-tls-audit` | A05:2021 / A02 |
| 6 | Dependency / Supply Chain | `dependency-audit` | A06:2021 |
| 7 | Logging & Monitoring | `logging-monitoring-audit` | A09:2021 |
| 8 | Security Misconfiguration | `security-misconfig-audit` | A05:2021 |
| 9 | API Security | Cross-domain | A01, A03, A07 |
| 10 | Cryptography & Data Protection | Cross-domain | A02:2021 |

---

## Domain 1: Authentication & Access Control

**Description:** Reviews whether the application properly verifies user identity and restricts access to authenticated users only.

**Key Risks:**
- Weak or bypassable login mechanisms
- Missing or optional MFA on privileged accounts
- Insecure password reset flows (predictable tokens, no expiry)
- Credential stuffing exposure due to missing rate limiting
- Account enumeration via differential error messages
- Default or unchanged credentials on admin interfaces

**Skill:** `.claude/skills/auth-access-audit/`

**OWASP Reference:** [A07:2021 — Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

---

## Domain 2: Authorization / Role-Based Access Control (RBAC)

**Description:** Reviews whether the application enforces appropriate access controls for each user role and prevents unauthorized access to resources or functions.

**Key Risks:**
- Broken access control — horizontal privilege escalation (IDOR)
- Vertical privilege escalation — accessing admin functions as a standard user
- Missing server-side authorization checks (relying on client-side UI hiding)
- Insecure direct object references (predictable or guessable resource IDs)
- Role permission matrix deviating from design intent
- Missing function-level access control

**Skill:** `.claude/skills/rbac-audit/`

**OWASP Reference:** [A01:2021 — Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

---

## Domain 3: Session Management

**Description:** Reviews how the application manages user sessions and authentication tokens from login through logout.

**Key Risks:**
- JWT with weak algorithms (e.g., `alg: none`, RS256→HS256 confusion)
- Missing JWT expiry (`exp` claim) or insufficient expiry window
- Session tokens with low entropy (guessable)
- Missing `HttpOnly`, `Secure`, or `SameSite` cookie flags
- Sessions not invalidated on logout
- Concurrent session abuse
- Session fixation

**Skill:** `.claude/skills/session-jwt-audit/`

**OWASP Reference:** [A02:2021 — Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/), [A07:2021](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

---

## Domain 4: Input Validation & Injection

**Description:** Reviews whether the application validates, sanitizes, and encodes user-supplied input to prevent injection attacks.

**Key Risks:**
- SQL Injection (SQLi)
- Cross-Site Scripting (Reflected, Stored, DOM-based XSS)
- Command injection
- XML/XXE injection
- Path traversal / local file inclusion
- Server-Side Request Forgery (SSRF)
- Template injection
- Mass assignment / parameter pollution

**Skill:** `.claude/skills/input-validation-audit/`

**OWASP Reference:** [A03:2021 — Injection](https://owasp.org/Top10/A03_2021-Injection/)

---

## Domain 5: Security Headers & Transport Layer Security

**Description:** Reviews the HTTP response headers and TLS configuration to ensure secure transport and browser-level protections are in place.

**Key Risks:**
- Missing Content-Security-Policy (CSP) — XSS amplification
- Missing Strict-Transport-Security (HSTS) — downgrade attacks
- Missing X-Content-Type-Options — MIME sniffing attacks
- Clickjacking via missing X-Frame-Options or CSP `frame-ancestors`
- Outdated TLS versions (TLS 1.0, 1.1) or weak cipher suites
- Expired or self-signed certificates
- CORS misconfiguration — credential leakage to untrusted origins
- Missing Referrer-Policy — leaking sensitive URL parameters

**Skill:** `.claude/skills/headers-tls-audit/`

**OWASP Reference:** [A05:2021 — Security Misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)

---

## Domain 6: Dependency & Supply Chain Security

**Description:** Reviews third-party libraries, packages, and dependencies for known vulnerabilities, abandonment risk, and supply chain concerns.

**Key Risks:**
- Known CVEs in direct or transitive dependencies
- Outdated packages with security patches not applied
- Unmaintained packages with no upstream security support
- Dependency confusion / namespace squatting attacks
- Malicious packages substituted in the supply chain
- License risk (copyleft in commercial products)
- Pinning to mutable tags or branches

**Skill:** `.claude/skills/dependency-audit/`

**OWASP Reference:** [A06:2021 — Vulnerable and Outdated Components](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)

---

## Domain 7: Logging & Monitoring

**Description:** Reviews whether the application generates sufficient security-relevant logs, protects log integrity, and has alerting in place for anomalous events.

**Key Risks:**
- Missing logs for authentication events (login success/failure, logout)
- Missing logs for authorization failures
- Missing logs for admin and privileged actions
- PII or credentials inadvertently logged
- Logs stored without integrity protection (no append-only mechanism)
- Insufficient retention (logs rotated before incident detection)
- No alerting on high-frequency failures or anomalous patterns
- Logs inaccessible to security team in a timely manner

**Skill:** `.claude/skills/logging-monitoring-audit/`

**OWASP Reference:** [A09:2021 — Security Logging and Monitoring Failures](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)

---

## Domain 8: Security Misconfiguration

**Description:** Reviews the application and infrastructure configuration for insecure defaults, unnecessary exposure, and hardening gaps.

**Key Risks:**
- Debug mode enabled in production
- Verbose error messages exposing stack traces or internal paths
- Directory listing enabled on web server
- Default credentials on admin panels or management interfaces
- Unnecessary services, ports, or features enabled
- Permissive CORS policy (`Access-Control-Allow-Origin: *` with credentials)
- Exposed `.env`, `.git`, `backup`, or configuration files
- Overly permissive cloud storage bucket policies

**Skill:** `.claude/skills/security-misconfig-audit/`

**OWASP Reference:** [A05:2021 — Security Misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)

---

## Domain 9: API Security

**Description:** Cross-domain review covering API-specific risks including authentication, input validation, rate limiting, and data exposure via API endpoints.

**Key Risks:**
- Broken Object Level Authorization (BOLA/IDOR) on API endpoints
- Broken Function Level Authorization (admin API endpoints accessible to users)
- Excessive data exposure (APIs returning full objects when partial data suffices)
- Lack of rate limiting or throttling on API endpoints
- Missing API authentication on sensitive endpoints
- Insecure API versioning leaving deprecated endpoints active

**Skill:** Combination of `auth-access-audit`, `rbac-audit`, `input-validation-audit`

**OWASP Reference:** [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x00-header/)

---

## Domain 10: Cryptography & Data Protection

**Description:** Reviews whether sensitive data is properly protected at rest and in transit, and whether cryptographic implementations are sound.

**Key Risks:**
- Sensitive data transmitted over HTTP (unencrypted)
- Passwords stored in plaintext or with weak hashing (MD5, SHA-1 without salt)
- Encryption keys hardcoded in source code or configuration files
- Use of deprecated cryptographic algorithms (DES, RC4, MD5)
- Missing encryption for sensitive data at rest (database fields, file storage)
- Weak random number generation for security-sensitive values (tokens, session IDs)

**Skill:** Combination of `headers-tls-audit`, `session-jwt-audit`

**OWASP Reference:** [A02:2021 — Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
