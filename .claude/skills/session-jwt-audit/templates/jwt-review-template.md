# JWT Review Template

Documents the analysis of a JSON Web Token used by the application.

**Auditor:** [PLACEHOLDER]
**Date:** [PLACEHOLDER]
**Target:** [PLACEHOLDER]
**JWT Source:** [PLACEHOLDER — e.g., Authorization header Bearer token / Cookie: access_token]

---

## JWT Structure

### Header (Decoded)

```json
[PLACEHOLDER — Paste the decoded JWT header here]
```

| Claim | Value | Assessment |
|-------|-------|------------|
| `alg` | [PLACEHOLDER] | See algorithm assessment below |
| `typ` | [PLACEHOLDER — e.g., JWT] | Expected: JWT |
| Other | [PLACEHOLDER] | [NOTES] |

### Payload (Decoded)

```json
[PLACEHOLDER — Paste the decoded JWT payload here]
```

| Claim | Value | Assessment |
|-------|-------|------------|
| `sub` (subject) | [PLACEHOLDER or ABSENT] | User identifier present? |
| `iss` (issuer) | [PLACEHOLDER or ABSENT] | Validated by server? |
| `aud` (audience) | [PLACEHOLDER or ABSENT] | Validated by server? |
| `exp` (expiry) | [PLACEHOLDER or ABSENT] | See expiry assessment |
| `iat` (issued at) | [PLACEHOLDER or ABSENT] | |
| `nbf` (not before) | [PLACEHOLDER or ABSENT] | |
| `jti` (JWT ID) | [PLACEHOLDER or ABSENT] | Unique token ID — supports revocation |
| Custom claims | [PLACEHOLDER — list any non-standard claims] | Any privilege claims that could be manipulated? |

**Sensitive Data in Payload:**
[PLACEHOLDER — Note any sensitive data present in the payload. JWTs are base64 encoded, not encrypted. Any user seeing their own JWT can decode the payload. Note if sensitive fields like password, raw PII, or internal system details appear.]

---

## Algorithm Assessment

| Field | Value |
|-------|-------|
| **Algorithm in Use** | [PLACEHOLDER — e.g., RS256 / HS256 / ES256] |

| Scenario | Risk | Status |
|----------|------|--------|
| Algorithm is `none` | Critical | [PRESENT / NOT PRESENT] |
| Algorithm is RS256/ES256 (asymmetric) | Preferred | [YES / NO] |
| Algorithm is HS256 (symmetric) | Acceptable if strong secret | [YES / NO] |
| Algorithm confusion attack possible (RS256 → HS256 with public key) | Critical if yes | [TESTED / NOT TESTED / UNKNOWN] |
| Deprecated algorithm in use (MD5, SHA-1 based) | High | [YES / NO] |

**Algorithm Assessment:** [PASS / FAIL]
**Finding ID (if any):** [FIND-NNN or —]

---

## Expiry and Lifetime Assessment

| Field | Value | Assessment |
|-------|-------|------------|
| `exp` claim present | [Yes / No] | Must be present — Missing = High finding |
| `exp` enforced server-side | [Yes / No / Unknown] | Must be enforced — Not enforced = High finding |
| Token lifetime | [PLACEHOLDER — e.g., 1 hour / 24 hours / no expiry] | See threshold below |
| Refresh token in use | [Yes / No / Unknown] | |

**Lifetime Thresholds:**
- Access tokens: ≤ 15 minutes recommended; ≤ 1 hour acceptable; > 1 hour = Medium finding; no expiry = High finding
- Refresh tokens: Should have a finite lifetime and be rotated on use

**Expiry Assessment:** [PASS / FAIL]
**Finding ID (if any):** [FIND-NNN or —]

---

## Signature Validation Assessment

| Test | Status | Notes |
|------|--------|-------|
| Token with modified payload rejected | [Yes / No / Not Tested] | Basic signature validation |
| Token with `alg: none` rejected | [Yes / No / Not Tested] | Critical control |
| Algorithm confusion attempt rejected | [Yes / No / Not Tested] | RS256 → HS256 with public key |

**Signature Assessment:** [PASS / FAIL / UNKNOWN]
**Finding ID (if any):** [FIND-NNN or —]

---

## Token Storage Assessment

| Field | Value | Assessment |
|-------|-------|------------|
| Storage location | [PLACEHOLDER — e.g., HttpOnly Cookie / localStorage / sessionStorage / Memory] | |
| `HttpOnly` flag (if cookie) | [Yes / No / N/A] | Must be HttpOnly if in cookie |
| `Secure` flag (if cookie) | [Yes / No / N/A] | Must be Secure in production |
| `SameSite` attribute (if cookie) | [PLACEHOLDER or N/A] | Strict or Lax recommended |
| Token in URL (any endpoint?) | [Yes / No] | Must never appear in URL |
| Token in server logs | [Yes / No / Unknown] | Should not be logged |

**Storage Assessment:** [PASS / FAIL]
**Finding ID (if any):** [FIND-NNN or —]

---

## Token Rotation and Revocation

| Field | Value |
|-------|-------|
| Token rotation on refresh | [Yes / No / Unknown] |
| Token revocation mechanism | [PLACEHOLDER — e.g., Token blacklist / Short expiry only / None known] |
| Tokens invalidated on logout | [Yes / No / Unknown] |
| Tokens invalidated on password change | [Yes / No / Unknown] |

**Revocation Assessment:** [PASS / FAIL / UNKNOWN]
**Finding ID (if any):** [FIND-NNN or —]

---

## JWT Review Summary

| Area | Assessment | Finding ID |
|------|-----------|------------|
| Algorithm | [PASS / FAIL] | [FIND-NNN or —] |
| Expiry enforcement | [PASS / FAIL] | [FIND-NNN or —] |
| Signature validation | [PASS / FAIL / UNKNOWN] | [FIND-NNN or —] |
| Token storage | [PASS / FAIL] | [FIND-NNN or —] |
| Revocation | [PASS / FAIL / UNKNOWN] | [FIND-NNN or —] |
| Sensitive data in payload | [PASS / CONCERN] | [FIND-NNN or —] |

---

**Evidence:**
- [EVID-YYYY-MM-DD-NNN — decoded JWT header and payload (sanitized of test credentials)]

---

*Template: jwt-review-template.md*
