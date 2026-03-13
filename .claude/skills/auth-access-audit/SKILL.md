> **Reference Guide** — This skill documents the methodology. For automated execution, run:
> `python scripts/run_audit.py audit full --tools auth`
> Use this skill to interpret tool output, conduct manual review steps, or guide authorized active testing.

# Skill: Authentication and Access Control Audit

## Purpose

Assess the authentication mechanisms and access control implementations of a web application to identify weaknesses that could allow unauthorized access, account takeover, credential theft, or privilege abuse.

---

## Inputs Required

Before running this skill, ensure the following are available:

| Input | Source | Required? |
|-------|--------|-----------|
| Target application URL(s) | `.claude/context/scope.md` | Required |
| Authentication method(s) | `.claude/context/target-profile.md` | Required |
| Known user roles | `.claude/context/target-profile.md` | Required |
| Test account credentials (at least one role) | Provided separately by client | Required for active testing |
| Authorization confirmation | `.claude/context/audit-context.md` | Required |
| Identity provider details | `.claude/context/target-profile.md` | If SSO/OAuth in use |

---

## Method

### Phase 1: Reconnaissance (Passive)

1. Identify all authentication entry points:
   - Login page URL
   - Registration page URL
   - Password reset / forgot password URL
   - OAuth/SAML initiation endpoints
   - API authentication endpoints

2. Identify session management mechanism:
   - Cookie-based sessions (inspect cookie names and flags)
   - JWT tokens (inspect Authorization header or cookie)
   - OAuth access tokens

3. Review observable security indicators:
   - Is HTTPS enforced on auth endpoints?
   - Are cookie flags visible? (HttpOnly, Secure, SameSite)
   - Does the login form use autocomplete? (autocomplete="off" on password field)

### Phase 2: Authentication Mechanism Assessment

Work through the `auth-checklist.md` systematically:

4. Test login error messaging:
   - Do error messages differ for "username not found" vs "wrong password"? (Enumeration risk)
   - Is the response time significantly different between valid and invalid usernames? (Timing oracle)

5. Assess rate limiting:
   - Is the login endpoint rate-limited?
   - Is the password reset endpoint rate-limited?
   - Is there a CAPTCHA or progressive delay mechanism?

6. Assess MFA:
   - Is MFA enforced, optional, or absent?
   - If optional: is it enforced for admin accounts?
   - Are MFA codes single-use?
   - Is there a recovery mechanism that bypasses MFA? (Backup codes, SMS fallback)

7. Assess password reset:
   - What is the token length/entropy? (Should be ≥ 128 bits)
   - Is the token single-use? (Can it be reused after reset?)
   - Does the token expire? (Should expire within 1 hour)
   - Is the token transmitted in the URL? (Risk of Referer header leakage)
   - Does the reset page reveal whether an email is registered?

8. Assess OAuth/SSO configuration (if applicable):
   - Is the `state` parameter present and validated? (CSRF protection)
   - Is the redirect_uri validated against an allowlist?
   - Is the ID token signature verified?
   - What scopes are requested? (Principle of least privilege)

### Phase 3: Credential and Storage Assessment

9. Look for observable indicators of credential handling:
   - Is any credential or hash visible in HTTP responses?
   - Is the password transmitted in a POST body (acceptable) vs URL parameter (not acceptable)?
   - Is there any indication that passwords might be stored reversibly? (e.g., "password recovery" via email showing the actual password)

### Phase 4: Session Initiation

10. After successful authentication:
    - Is a new session token generated? (Prevents session fixation)
    - What are the properties of the new token? (Entropy, length, predictability)
    - Hand off session/JWT details to `session-jwt-audit` skill for deeper review

---

## Outputs

| Output | Template | Description |
|--------|---------|-------------|
| Completed auth checklist | `auth-checklist.md` | Record of all controls reviewed |
| Authentication findings | `auth-findings-template.md` | One record per finding identified |
| Evidence items | EVID- convention | HTTP captures, screenshots, tool outputs |

---

## Templates Used

- `.claude/skills/auth-access-audit/templates/auth-checklist.md`
- `.claude/skills/auth-access-audit/templates/auth-findings-template.md`

---

## References

- [OWASP Testing Guide — Authentication Testing](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/04-Authentication_Testing/)
- [OWASP A07:2021 — Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
- [NIST SP 800-63B — Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [CWE-287 — Improper Authentication](https://cwe.mitre.org/data/definitions/287.html)
- [CWE-640 — Weak Password Recovery](https://cwe.mitre.org/data/definitions/640.html)
