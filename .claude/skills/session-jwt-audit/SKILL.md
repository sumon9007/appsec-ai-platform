# Skill: Session Management and JWT Audit

## Purpose

Assess the application's session management and JSON Web Token (JWT) implementation to identify weaknesses that could allow session hijacking, token forgery, session fixation, or unauthorized access through improper session lifecycle management.

---

## Inputs Required

| Input | Source | Required? |
|-------|--------|-----------|
| Target application URL(s) | `.claude/context/scope.md` | Required |
| Authentication mechanism | `.claude/context/target-profile.md` | Required |
| Test account credentials | Provided by client | Required |
| Authorization confirmation | `.claude/context/audit-context.md` | Required |

---

## Method

### Phase 1: Session Token Identification

1. Authenticate with a test account
2. Identify how the session is maintained:
   - HTTP cookie (inspect Set-Cookie header attributes)
   - Authorization Bearer token in HTTP header
   - localStorage or sessionStorage (check browser DevTools)
   - URL parameter (session ID in URL = immediate finding)

3. Collect the session token or JWT for analysis

### Phase 2: JWT Analysis (if JWTs are in use)

4. Decode the JWT header and payload (base64url decode — not decryption, this is always safe):
   - Inspect the `alg` (algorithm) claim in the header
   - Inspect the `typ` claim
   - List all claims in the payload

5. Algorithm assessment:
   - `alg: none` — Critical finding (no signature verification)
   - `alg: HS256` — acceptable if secret is strong; check for algorithm confusion
   - `alg: RS256` or `ES256` — preferred; verify signature cannot be confused to HS256
   - Deprecated algorithms (HS384 without strong key material, RSA with 1024-bit key) — flag

6. Claims assessment:
   - `exp` (expiry) present and enforced?
   - `iat` (issued at) present?
   - `iss` (issuer) present and validated?
   - `aud` (audience) present and validated?
   - `sub` (subject) present and appropriate?
   - Are there any claims that could be manipulated by the client to escalate privileges?
   - Is sensitive data in the JWT payload unnecessarily? (JWTs are base64 encoded, not encrypted unless JWE is used)

7. Signature validation:
   - Can the signature be bypassed by changing `alg` to `none`? (Critical if yes)
   - Can the signature be bypassed by switching from RS256 to HS256 with the public key as the secret? (Critical if yes)

8. Expiry enforcement:
   - Is the `exp` claim enforced server-side?
   - What is the JWT lifetime? (Recommended: 15 minutes for sensitive operations, ≤ 1 hour for standard use)
   - Is token refresh implemented?
   - Are expired tokens rejected?

9. Token storage and transmission:
   - Where is the JWT stored in the client? (Cookie with HttpOnly = best; localStorage = higher XSS risk)
   - Is the JWT transmitted in a secure channel (HTTPS only)?
   - Is the JWT present in server logs or error messages?

### Phase 3: Cookie-Based Session Analysis

10. Inspect session cookie attributes:
    - `HttpOnly` — prevents JavaScript access (protects against XSS-based token theft)
    - `Secure` — cookie only sent over HTTPS
    - `SameSite` — `Strict` or `Lax` to prevent CSRF
    - `Domain` and `Path` — are they appropriately scoped?
    - Expiry — what is the cookie lifetime?

11. Session token entropy:
    - How long is the session ID? (Should be ≥ 128 bits / 32 hex characters)
    - Does the session ID appear predictable or sequential? (Flag for investigation)

### Phase 4: Session Lifecycle

12. Session fixation:
    - After authentication, is a new session ID/token generated? (Must be — previous ID must not continue)

13. Logout:
    - After logout, is the session token invalidated server-side?
    - Can the old token be reused after logout? (If yes, Critical finding)
    - Is the cookie cleared on logout?

14. Session timeout:
    - Is there an inactivity timeout?
    - Is there an absolute maximum session lifetime?
    - What happens when the timeout expires?

15. Concurrent sessions:
    - Can the same account have multiple active sessions?
    - Are users notified of new sessions?
    - Is there a way for users to revoke active sessions?

---

## Outputs

| Output | Template | Description |
|--------|---------|-------------|
| JWT review record | `jwt-review-template.md` | JWT header/payload analysis |
| Session control checklist | `session-control-checklist.md` | Cookie and session lifecycle |
| Findings | Standard finding format | One per identified vulnerability |
| Evidence items | EVID- convention | Token captures, cookie inspections |

---

## Templates Used

- `.claude/skills/session-jwt-audit/templates/jwt-review-template.md`
- `.claude/skills/session-jwt-audit/templates/session-control-checklist.md`

---

## References

- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [OWASP JWT Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [PortSwigger — JWT Attacks](https://portswigger.net/web-security/jwt)
- [RFC 7519 — JSON Web Token (JWT)](https://www.rfc-editor.org/rfc/rfc7519)
- [CWE-384 — Session Fixation](https://cwe.mitre.org/data/definitions/384.html)
- [CWE-613 — Insufficient Session Expiration](https://cwe.mitre.org/data/definitions/613.html)
