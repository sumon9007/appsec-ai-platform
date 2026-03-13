# Findings Register

This register is the single source of truth for all security findings in this engagement.

Every confirmed finding, suspected issue, and review gap must be recorded here.

Update this register at the end of every audit session and before generating any report.

---

## Findings Summary

| Finding ID | Title | Domain | Severity | Confidence | Status |
|------------|-------|--------|----------|------------|--------|
| FIND-001 | [Title] | [Domain] | [Severity] | [Confidence] | [Status] |

---

## Finding Record Format

Each finding must use the structure below. Copy this block for every new finding.

---

### FIND-NNN

**Title:** [Short, specific description of the issue]

**Domain:** [Authentication / Authorization / Session Management / Input Validation / Security Headers / Dependencies / Logging / Misconfiguration]

**Severity:** [Critical / High / Medium / Low / Info]

**Confidence:** [high / medium / low]

**Target:** [URL, endpoint, component, or feature where the issue was observed]

**Evidence:**
- [EVID-YYYY-MM-DD-NNN — brief description of what this evidence shows]

**Observation:** [Factual description of what was observed. No speculation. Use `[ASSUMED]` or `[UNKNOWN]` labels where certainty is limited.]

**Risk:** [Explain the business or security impact. What can an attacker do? What data or function is at risk?]

**Recommendation:** [Specific, actionable remediation guidance. Not vague — name the exact control, setting, or code change required.]

**Acceptance Criteria Mapping:** [Reference the relevant must-fix or advisory item from `.claude/docs/acceptance-criteria.md`. Example: "Auth-Must-Fix-1 — MFA required for all privileged roles"]

**Status:** [confirmed / suspected / review-gap / mitigated / accepted-risk]

**Review Type:** [passive / active / document review / configuration review]

**Opened:** [YYYY-MM-DD]

**Closed:** [YYYY-MM-DD or open]

**Closure Evidence:**
- [EVID-YYYY-MM-DD-NNN — description of fix evidence reviewed]
- [EVID-YYYY-MM-DD-NNN — description of re-test result confirming remediation]

---

## Example Finding — Confirmed Issue

---

### FIND-001

**Title:** Missing Content-Security-Policy header on all application pages

**Domain:** Security Headers

**Severity:** Medium

**Confidence:** high

**Target:** https://app.example.com (all pages observed)

**Evidence:**
- EVID-2026-03-11-001 — HTTP response capture from main page showing absence of Content-Security-Policy header
- EVID-2026-03-11-002 — HTTP response capture from authenticated dashboard page confirming CSP absent in authenticated context

**Observation:** The application does not return a Content-Security-Policy header on any observed page, including the main landing page and the authenticated dashboard. No CSP was found in either the unauthenticated or authenticated response headers.

**Risk:** The absence of a CSP removes a critical browser-enforced defense against cross-site scripting (XSS) attacks. If XSS is achievable via another vulnerability, the attacker can execute arbitrary JavaScript without any browser-level restriction on resource loading, script sources, or data exfiltration.

**Recommendation:** Implement a Content-Security-Policy header for all application responses. Begin with a report-only policy to observe violations before enforcing. At minimum, restrict `default-src` to `'self'` and explicitly allowlist trusted CDN domains. Avoid `unsafe-inline` and `unsafe-eval`. Use nonces or hashes for any legitimate inline scripts.

**Acceptance Criteria Mapping:** Headers-Advisory-1 — CSP should be present and restrictive

**Status:** confirmed

**Review Type:** passive

**Opened:** 2026-03-11

**Closed:** open

**Closure Evidence:** (none — finding is open)

---

## Example Finding — Review Gap

---

### FIND-002

**Title:** MFA enforcement on privileged accounts cannot be confirmed

**Domain:** Authentication

**Severity:** [review-gap — not rated until confirmed]

**Confidence:** low

**Target:** Admin account login flow — https://app.example.com/admin/login

**Evidence:**
- EVID-2026-03-11-003 — Login page screenshot showing username/password fields only, no visible MFA prompt

**Observation:** The login page for the admin panel presents only a username and password field. No MFA prompt was observed during the session. However, MFA may be enforced after credential validation (i.e., step-up after first factor) and this could not be confirmed without authenticated test access.

`[UNKNOWN]` — MFA enforcement cannot be confirmed or refuted without an active test account with admin role access.

**Risk:** If MFA is absent on privileged accounts, a credential compromise would result in full admin access without any additional authentication barrier.

**Recommendation:** Client to confirm: (a) whether MFA is enforced for admin accounts, (b) which MFA method is in use, and (c) whether MFA can be bypassed. Auditor to perform re-test with admin test account in next session.

**Acceptance Criteria Mapping:** Auth-Must-Fix-1 — MFA required for all privileged roles

**Status:** review-gap

**Review Type:** passive

**Opened:** 2026-03-11

**Closed:** open

**Closure Evidence:** (none — pending re-test with admin test account)

---

## Register Maintenance Notes

- Do not reuse Finding IDs. Each ID is permanent for this engagement.
- Finding IDs are sequential: FIND-001, FIND-002, FIND-003...
- Closed findings remain in this register with status `closed` and closure evidence.
- Risk accepted findings remain with status `accepted-risk` and a reference to the signed risk acceptance document.
- Update the Findings Summary table at the top whenever a finding is added, updated, or closed.
