# Injection Test Notes

Documents manual injection review observations. For use only when active testing is explicitly authorized.

**AUTHORIZATION REQUIRED:** This template is for use only when active injection testing is authorized in `.claude/context/audit-context.md`. Do not perform active injection testing in passive review mode.

**Auditor:** [PLACEHOLDER]
**Date:** [PLACEHOLDER]
**Target:** [PLACEHOLDER]
**Authorization Reference:** [PLACEHOLDER — Reference to authorization in audit-context.md]
**Authorization Scope:** [PLACEHOLDER — e.g., "Active testing on staging environment only"]

---

## Testing Approach

This document records observations made during manual injection review. For each tested input vector:
- The input payload used is recorded for documentation purposes only
- Observations are factual — what the application did, not what might theoretically occur
- Any concerning observation is flagged as requiring a formal finding with full evidence

---

## Test Observations

### Vector: SQL Injection — [PLACEHOLDER — Endpoint and Parameter]

| Field | Value |
|-------|-------|
| **Endpoint** | [PLACEHOLDER — e.g., GET /api/users?id=] |
| **Parameter** | [PLACEHOLDER — e.g., `id` query parameter] |
| **Injection Type Tested** | SQL Injection |
| **Test Payloads Used** | [PLACEHOLDER — e.g., `'`, `1'--`, `1 OR 1=1`] |

**Behavior Observed:**
[PLACEHOLDER — Describe exactly what the application returned. E.g., "Input of `'` returned a 500 error with a PostgreSQL stack trace. Input of `1 OR 1=1` returned all user records. Input of `1` returned one user record."]

**Indicators of Concern:**
- [ ] Database error messages returned in response
- [ ] Response content changes based on logic injected
- [ ] Response timing differs significantly between payloads
- [ ] Stack trace reveals database type and version

**Verdict:** [Confirmed Vulnerable / Indicators Present / Not Vulnerable / Inconclusive]

**Evidence:**
- [EVID-YYYY-MM-DD-NNN — description]

**Finding ID:** [FIND-NNN or — if no finding]

---

### Vector: Cross-Site Scripting (XSS) — [PLACEHOLDER — Endpoint and Parameter]

| Field | Value |
|-------|-------|
| **Endpoint** | [PLACEHOLDER — e.g., GET /search?q=] |
| **Parameter** | [PLACEHOLDER — e.g., `q` query parameter (reflected in response)] |
| **Injection Type Tested** | Reflected XSS |
| **Test Payloads Used** | [PLACEHOLDER — e.g., `<script>alert(1)</script>`, `"><img src=x onerror=alert(1)>`] |

**Behavior Observed:**
[PLACEHOLDER — Describe what happened. E.g., "Search term is reflected in the page source without encoding. The payload `<script>` appeared verbatim in the HTML source, but a Content-Security-Policy blocked execution. The payload `"><img src=x` caused a parsing disruption visible in the DOM."]

**Indicators of Concern:**
- [ ] User input reflected verbatim in HTML response without encoding
- [ ] Payload breaks out of HTML attribute context
- [ ] No Content-Security-Policy present to limit impact
- [ ] Stored XSS: payload persists and is served to other users

**Verdict:** [Confirmed Vulnerable / Indicators Present / Mitigated by CSP / Not Vulnerable / Inconclusive]

**Evidence:**
- [EVID-YYYY-MM-DD-NNN — description]

**Finding ID:** [FIND-NNN or —]

---

### Vector: Path Traversal — [PLACEHOLDER — Endpoint and Parameter]

| Field | Value |
|-------|-------|
| **Endpoint** | [PLACEHOLDER — e.g., GET /api/files/{filename}] |
| **Parameter** | [PLACEHOLDER — e.g., `filename` path parameter] |
| **Injection Type Tested** | Path Traversal |
| **Test Payloads Used** | [PLACEHOLDER — e.g., `../../../etc/passwd`, `..%2F..%2Fetc%2Fpasswd`] |

**Behavior Observed:**
[PLACEHOLDER — E.g., "Request for `../../../etc/passwd` returned a 400 Bad Request. URL-encoded variant returned the same. No file content appeared in responses."]

**Indicators of Concern:**
- [ ] Traversal sequences not stripped or rejected
- [ ] Different response behavior for valid vs. traversal paths (timing or content)
- [ ] File content returned or partially returned

**Verdict:** [Confirmed Vulnerable / Not Vulnerable / Inconclusive]

**Evidence:**
- [EVID-YYYY-MM-DD-NNN — description]

**Finding ID:** [FIND-NNN or —]

---

### Vector: Command Injection — [PLACEHOLDER — Endpoint and Parameter]

| Field | Value |
|-------|-------|
| **Endpoint** | [PLACEHOLDER] |
| **Parameter** | [PLACEHOLDER] |
| **Injection Type Tested** | Command Injection |
| **Test Payloads Used** | [PLACEHOLDER — e.g., `test; id`, `test && whoami`] |

**Behavior Observed:**
[PLACEHOLDER]

**Indicators of Concern:**
- [ ] Response includes system command output
- [ ] Timing differences suggest command execution (blind injection)
- [ ] Unusual error messages referencing system functions

**Verdict:** [Confirmed Vulnerable / Indicators Present / Not Vulnerable / Inconclusive]

**Evidence:**
- [EVID-YYYY-MM-DD-NNN]

**Finding ID:** [FIND-NNN or —]

---

### Vector: Template Injection — [PLACEHOLDER — Endpoint and Parameter]

| Field | Value |
|-------|-------|
| **Endpoint** | [PLACEHOLDER] |
| **Parameter** | [PLACEHOLDER] |
| **Injection Type Tested** | Server-Side Template Injection (SSTI) |
| **Test Payloads Used** | [PLACEHOLDER — e.g., `{{7*7}}`, `${7*7}`, `<%= 7*7 %>`] |

**Behavior Observed:**
[PLACEHOLDER — E.g., "Input of `{{7*7}}` was reflected as `49` in the response, indicating the payload was evaluated by the template engine."]

**Verdict:** [Confirmed Vulnerable / Indicators Present / Not Vulnerable / Inconclusive]

**Evidence:**
- [EVID-YYYY-MM-DD-NNN]

**Finding ID:** [FIND-NNN or —]

---

## Injection Test Summary

| Vector | Endpoint | Result | Severity | Finding ID |
|--------|----------|--------|----------|------------|
| SQL Injection | [PLACEHOLDER] | [Vulnerable/Not Vulnerable/Inconclusive] | [SEVERITY] | [FIND-NNN or —] |
| Reflected XSS | [PLACEHOLDER] | [Vulnerable/Mitigated/Not Vulnerable] | [SEVERITY] | [FIND-NNN or —] |
| Path Traversal | [PLACEHOLDER] | [Vulnerable/Not Vulnerable] | [SEVERITY] | [FIND-NNN or —] |
| Command Injection | [PLACEHOLDER] | [Vulnerable/Not Vulnerable] | [SEVERITY] | [FIND-NNN or —] |
| Template Injection | [PLACEHOLDER] | [Vulnerable/Not Vulnerable] | [SEVERITY] | [FIND-NNN or —] |

---

*Template: injection-test-notes.md*
