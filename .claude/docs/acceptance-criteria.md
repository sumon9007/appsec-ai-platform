# Acceptance Criteria

Defines what "passing" means for each audit domain. Used during release gate reviews and quarterly audits to determine whether the application meets minimum security standards.

---

## How to Use This Document

- **Must-Fix:** Findings in this category must be remediated before the application can pass.
- **Advisory:** Findings are noted and tracked but do not constitute a blocker on their own. Accumulation of advisory issues may still result in a Conditional Pass.
- **Pass Threshold:** The minimum state required to issue a Pass gate decision.

---

## Domain 1: Authentication & Access Control

**Pass Threshold:**
- No Critical or High authentication findings open
- MFA is enforced or offered for all privileged accounts
- Password reset tokens are single-use and expire within 1 hour
- Login does not enumerate valid usernames via differential error messages
- Rate limiting is in place on login and password reset endpoints

**Must-Fix Items:**
- Any credential stored in plaintext or reversibly encrypted
- Authentication bypass vulnerability (any severity)
- Password reset with no expiry or reuse protection
- Admin accounts with no MFA and internet exposure

**Advisory Items:**
- MFA not offered to standard users (encouraged but not required for pass)
- Password complexity policy below NIST SP 800-63B recommendations
- Generic "invalid credentials" message not yet implemented (Medium)

---

## Domain 2: Authorization / RBAC

**Pass Threshold:**
- No Critical or High authorization findings open
- Server-side authorization checks in place for all sensitive functions
- IDOR testing reveals no unauthorized access to other users' data
- Role permission matrix matches documented design intent

**Must-Fix Items:**
- Any confirmed IDOR allowing access to another user's data
- Any vertical privilege escalation (standard user accessing admin functions)
- Authorization check performed client-side only with no server-side enforcement

**Advisory Items:**
- Missing fine-grained permissions (coarse roles where granular control would be preferable)
- Object IDs that are sequential/predictable (Low — requires IDOR confirmation to escalate)

---

## Domain 3: Session Management

**Pass Threshold:**
- No Critical or High session management findings open
- Session tokens have minimum 128 bits of entropy
- JWT: algorithm is RS256, ES256, or equivalent; `alg: none` is rejected
- JWT: `exp` claim present and enforced; lifetime ≤ 1 hour for sensitive operations
- Cookies: `HttpOnly`, `Secure`, and `SameSite=Strict` or `Lax` set on session cookies
- Session invalidated on logout (server-side, not just client-side cookie deletion)

**Must-Fix Items:**
- JWT accepting `alg: none`
- Sessions not invalidated on logout
- Session cookie missing `Secure` flag on production (HTTPS) application
- Session token with insufficient entropy (< 64 bits)

**Advisory Items:**
- Concurrent session control not enforced (Medium)
- Session timeout set to > 8 hours for standard users
- `SameSite` missing (set to default browser behavior)

---

## Domain 4: Input Validation & Injection

**Pass Threshold:**
- No Critical or High injection findings open
- All database queries use parameterized queries or ORM
- HTML output is encoded to prevent XSS
- File uploads: MIME type validated server-side; files not executed from upload directory
- No path traversal vulnerabilities found in file operations

**Must-Fix Items:**
- Any confirmed SQL injection (any severity)
- Any confirmed stored XSS in user-facing functionality
- Any confirmed command injection
- File uploads without server-side content type validation
- Path traversal allowing access to server files

**Advisory Items:**
- Reflected XSS requiring significant user interaction (Low–Medium depending on context)
- Missing Content-Security-Policy making XSS impact higher (escalated in Headers domain)
- Input length limits not enforced (Low)

---

## Domain 5: Security Headers & Transport

**Pass Threshold:**
- HTTPS enforced application-wide; no mixed content
- HSTS present with `max-age` ≥ 6 months (15768000 seconds)
- X-Content-Type-Options: `nosniff` present
- X-Frame-Options or CSP `frame-ancestors` present to prevent clickjacking
- TLS 1.2 minimum; TLS 1.0 and 1.1 disabled
- No use of known-weak cipher suites (RC4, DES, NULL)
- Certificate valid with > 30 days to expiry

**Must-Fix Items:**
- HTTP used without redirect to HTTPS
- TLS 1.0 or 1.1 enabled
- Certificate expired or expiring within 7 days
- CORS configured with `Access-Control-Allow-Origin: *` and `Access-Control-Allow-Credentials: true`

**Advisory Items:**
- Missing Content-Security-Policy (High — strongly recommended, may be must-fix in regulated environments)
- Missing Referrer-Policy (Low)
- Missing Permissions-Policy (Info)
- Certificate expiry 8–30 days out (Medium — schedule renewal)

---

## Domain 6: Dependency / Supply Chain

**Pass Threshold:**
- No Critical or High CVEs in direct dependencies with a known fix available
- No actively exploited vulnerabilities (CISA KEV listed) regardless of severity
- All production dependencies are actively maintained (last release within 24 months)

**Must-Fix Items:**
- Any dependency with a CVSS score ≥ 9.0 with a fix available
- Any dependency listed on CISA Known Exploited Vulnerabilities catalog
- Any package sourced from an untrusted or unofficial registry

**Advisory Items:**
- Medium CVEs with no fix available (track, document mitigating controls)
- Dependencies pinned to mutable `latest` tags (Medium — pin to exact versions)
- Abandoned packages with no CVEs (Low — plan replacement)

---

## Domain 7: Logging & Monitoring

**Pass Threshold:**
- Authentication events (success and failure) are logged
- Authorization failures are logged
- Admin and privileged actions are logged
- No credentials or sensitive PII appear in logs
- Log retention meets the minimum required for the application's compliance obligations
- At least one alerting rule exists for high-frequency authentication failures

**Must-Fix Items:**
- Credentials or unhashed passwords appearing in logs
- No logging of authentication events
- Log data stored without any access control

**Advisory Items:**
- Log retention below 90 days (Medium — align with compliance requirements)
- No centralized logging (Medium — increases incident response time)
- Alerting thresholds not defined or tested (Medium)
- Input anomalies not logged (Low)

---

## Domain 8: Security Misconfiguration

**Pass Threshold:**
- Debug mode disabled in production
- Verbose error messages (stack traces, internal paths) not exposed to users
- No default credentials on any accessible interface
- No unprotected admin interfaces accessible from the internet
- No sensitive files exposed (`.env`, `.git/config`, `backup.*`, `web.config`)

**Must-Fix Items:**
- Default credentials confirmed in use
- `.env` or credentials file accessible via HTTP request
- Debug mode or verbose error output in production

**Advisory Items:**
- Directory listing enabled (Medium)
- Unnecessary services running (Low–Medium)
- `robots.txt` revealing sensitive path structure (Info–Low)

---

## Overall Pass Conditions

The application passes the security audit gate when:

1. Zero Critical findings are open
2. Zero High findings are open (or all High findings have a formally accepted risk exception documented)
3. All Must-Fix items across all domains are resolved
4. No domain has more than three Medium findings newly introduced in the current release cycle

A **Conditional Pass** may be issued when:
- High findings are acknowledged with a documented remediation plan and committed deadline
- Medium findings are accepted with documented justification and tracking

A **Fail** decision is issued when:
- Any Critical finding is open without resolution
- Any Must-Fix item remains unresolved
- Authorization for the audit was not properly documented
