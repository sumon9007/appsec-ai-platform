# Session Control Checklist

Assesses session management controls for cookie-based and token-based sessions.

**Auditor:** [PLACEHOLDER]
**Date:** [PLACEHOLDER]
**Target:** [PLACEHOLDER]
**Session Mechanism:** [PLACEHOLDER — Cookie-based sessions / JWT / Both]

---

## Legend

| Status | Meaning |
|--------|---------|
| PASS | Control is present and appropriately implemented |
| FAIL | Control is absent or improperly implemented — finding required |
| PARTIAL | Control exists but has gaps |
| N/A | Not applicable |
| UNKNOWN | Could not be determined |

---

## 1. Session Token / ID Properties

| # | Control | Status | Observed Value | Notes | Finding ID |
|---|---------|--------|---------------|-------|------------|
| 1.1 | Session token is ≥ 128 bits of entropy | [STATUS] | [OBSERVED] | [NOTES] | [FIND-NNN or —] |
| 1.2 | Session token is not predictable or sequential | [STATUS] | [OBSERVED] | [NOTES] | [FIND-NNN or —] |
| 1.3 | Session token is not exposed in URL parameters | [STATUS] | [OBSERVED] | [NOTES] | [FIND-NNN or —] |
| 1.4 | Session token is not logged in server logs | [STATUS] | [UNKNOWN] | [NOTES] | [FIND-NNN or —] |

---

## 2. Cookie Flags (If Session Uses Cookies)

| # | Cookie Flag | Status | Observed Value | Notes | Finding ID |
|---|------------|--------|---------------|-------|------------|
| 2.1 | `HttpOnly` flag present on session cookie | [STATUS] | [Yes / No] | Prevents JS access to cookie | [FIND-NNN or —] |
| 2.2 | `Secure` flag present on session cookie | [STATUS] | [Yes / No] | Prevents cookie over HTTP | [FIND-NNN or —] |
| 2.3 | `SameSite` attribute present | [STATUS] | [Strict / Lax / None / Absent] | Strict or Lax recommended | [FIND-NNN or —] |
| 2.4 | `SameSite=None` used with `Secure` | [STATUS] | [N/A / Yes / No] | Required if SameSite=None | [FIND-NNN or —] |
| 2.5 | Cookie `Domain` appropriately scoped | [STATUS] | [OBSERVED] | Not overly broad | [FIND-NNN or —] |
| 2.6 | Cookie `Path` appropriately scoped | [STATUS] | [OBSERVED] | [NOTES] | [FIND-NNN or —] |
| 2.7 | Cookie does not persist beyond session unless intended | [STATUS] | [Expires: OBSERVED] | [NOTES] | [FIND-NNN or —] |

---

## 3. Session Timeout

| # | Control | Status | Observed / Stated Value | Notes | Finding ID |
|---|---------|--------|------------------------|-------|------------|
| 3.1 | Inactivity timeout is configured | [STATUS] | [OBSERVED] | [NOTES] | [FIND-NNN or —] |
| 3.2 | Inactivity timeout ≤ 30 minutes for sensitive applications | [STATUS] | [OBSERVED] | [NOTES] | [FIND-NNN or —] |
| 3.3 | Absolute maximum session lifetime is configured | [STATUS] | [OBSERVED] | [NOTES] | [FIND-NNN or —] |
| 3.4 | Expired sessions result in redirect to login (not error) | [STATUS] | [OBSERVED] | [NOTES] | [FIND-NNN or —] |

---

## 4. Session Fixation Prevention

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 4.1 | New session token issued upon successful authentication | [STATUS] | Pre-auth token must not continue as authenticated token | [FIND-NNN or —] |
| 4.2 | Pre-authentication session ID is invalidated after login | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 5. Logout Behavior

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 5.1 | Logout invalidates the session server-side (not just client) | [STATUS] | Old token unusable after logout | [FIND-NNN or —] |
| 5.2 | Session cookie is cleared on logout | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 5.3 | Old session token is rejected if replayed post-logout | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 5.4 | Logout clears session from all storage locations | [STATUS] | localStorage, sessionStorage, cookies | [FIND-NNN or —] |

---

## 6. Concurrent Session Control

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 6.1 | Concurrent session policy is defined | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 6.2 | Users can view active sessions | [STATUS] | Optional but recommended | [FIND-NNN or —] |
| 6.3 | Users can revoke active sessions | [STATUS] | Optional but recommended | [FIND-NNN or —] |
| 6.4 | New login notifies user of new session (if relevant for risk level) | [STATUS] | Optional for high-value applications | [FIND-NNN or —] |

---

## 7. Session Management Post-Password Change

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 7.1 | All sessions invalidated after a password change | [STATUS] | Prior sessions should not remain valid | [FIND-NNN or —] |
| 7.2 | All sessions invalidated after a password reset | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## Checklist Summary

| Section | Controls | PASS | FAIL | PARTIAL | N/A | UNKNOWN |
|---------|----------|------|------|---------|-----|---------|
| 1. Token Properties | 4 | — | — | — | — | — |
| 2. Cookie Flags | 7 | — | — | — | — | — |
| 3. Session Timeout | 4 | — | — | — | — | — |
| 4. Session Fixation | 2 | — | — | — | — | — |
| 5. Logout Behavior | 4 | — | — | — | — | — |
| 6. Concurrent Sessions | 4 | — | — | — | — | — |
| 7. Post-Password Change | 2 | — | — | — | — | — |
| **Total** | **27** | — | — | — | — | — |

---

*Template: session-control-checklist.md*
