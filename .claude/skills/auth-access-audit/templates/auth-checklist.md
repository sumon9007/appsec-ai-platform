# Authentication Controls Checklist

Complete this checklist during the authentication and access control review. Record the status of each control and notes on observations.

**Auditor:** [PLACEHOLDER]
**Date:** [PLACEHOLDER]
**Target:** [PLACEHOLDER]
**Authorization Reference:** [PLACEHOLDER]

---

## Legend

| Status | Meaning |
|--------|---------|
| PASS | Control is present and appropriately implemented |
| FAIL | Control is absent or improperly implemented — finding required |
| PARTIAL | Control exists but has gaps — assess severity |
| N/A | Not applicable to this application |
| UNKNOWN | Could not be determined — document as [UNKNOWN] |

---

## 1. Login Mechanism

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 1.1 | Login form submitted over HTTPS | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 1.2 | Login endpoint enforces HTTPS (no HTTP fallback) | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 1.3 | Login error messages do not distinguish username vs. password failure | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 1.4 | Login response time does not differ significantly between valid and invalid usernames | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 1.5 | Rate limiting is enforced on the login endpoint | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 1.6 | Account lockout or progressive delay after repeated failures | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 1.7 | CAPTCHA or equivalent bot protection in place | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 1.8 | Autocomplete disabled on password field | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 2. Password Policy

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 2.1 | Minimum password length ≥ 8 characters (NIST recommends 12+) | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 2.2 | Passwords checked against known breached password lists | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 2.3 | No maximum password length restriction below 64 characters | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 2.4 | Password complexity requirements (if used) are reasonable | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 2.5 | Password expiry policy is defined (or intentionally absent per NIST guidance) | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 2.6 | Password reuse restrictions are in place | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 3. Multi-Factor Authentication (MFA)

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 3.1 | MFA is available to users | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 3.2 | MFA is enforced for all admin/privileged accounts | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 3.3 | MFA codes are single-use (TOTP codes cannot be replayed) | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 3.4 | MFA codes expire within a reasonable window (≤ 30 seconds for TOTP) | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 3.5 | MFA recovery codes are generated securely and stored safely | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 3.6 | MFA cannot be disabled without re-authentication | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 3.7 | MFA enrollment requires existing authentication | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 4. Account Lockout

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 4.1 | Account lockout is triggered after a defined number of failures | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 4.2 | Lockout threshold is reasonable (e.g., 5–10 attempts) | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 4.3 | Lockout duration is appropriate (e.g., 15–30 minutes, or manual unlock) | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 4.4 | Account unlock requires identity verification (not just waiting) | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 4.5 | Lockout events are logged | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 4.6 | Lockout response does not reveal whether the account exists | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 5. Password Reset Flow

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 5.1 | Password reset tokens have high entropy (≥ 128 bits) | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 5.2 | Reset tokens are single-use (invalidated after first use) | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 5.3 | Reset tokens expire within 1 hour | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 5.4 | Reset token is NOT included in the URL (transmitted in POST body or fragment) | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 5.5 | Reset page does not reveal whether email address is registered | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 5.6 | All existing sessions are invalidated after a password reset | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 5.7 | Rate limiting enforced on password reset requests | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 6. OAuth / SSO Configuration (if applicable)

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 6.1 | OAuth `state` parameter used and validated | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 6.2 | Redirect URI validated against a strict allowlist | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 6.3 | ID token signature is validated | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 6.4 | Requested scopes follow principle of least privilege | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 6.5 | PKCE (Proof Key for Code Exchange) used for public clients | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 6.6 | OAuth tokens not stored in insecure locations (e.g., localStorage without additional controls) | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 7. Credential Storage Indicators

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 7.1 | No credential or hash visible in HTTP responses | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 7.2 | Password not transmitted in URL parameters | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 7.3 | No evidence of reversible password storage (password recovery sends original password) | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 7.4 | API keys or tokens not visible in client-side source code | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## Checklist Summary

| Section | Total Controls | PASS | FAIL | PARTIAL | N/A | UNKNOWN |
|---------|---------------|------|------|---------|-----|---------|
| 1. Login Mechanism | 8 | — | — | — | — | — |
| 2. Password Policy | 6 | — | — | — | — | — |
| 3. MFA | 7 | — | — | — | — | — |
| 4. Account Lockout | 6 | — | — | — | — | — |
| 5. Password Reset | 7 | — | — | — | — | — |
| 6. OAuth / SSO | 6 | — | — | — | — | — |
| 7. Credential Storage | 4 | — | — | — | — | — |
| **Total** | **44** | — | — | — | — | — |

---

*Template: auth-checklist.md*
