# Findings Register

This register is the single source of truth for all security findings in this engagement.

Every confirmed finding, suspected issue, and review gap must be recorded here.

Update this register at the end of every audit session and before generating any report.

*Created: 2026-03-13 by appsec-audit-tool*

---

## Findings Summary

| Finding ID | Title | Domain | Severity | Confidence | Status |
|------------|-------|--------|----------|------------|--------|
| FIND-004 | TLS — Cipher Suite Enumeration on https://diversifiedrobotic.com/ | TLS / Certificate | Info | low | review-gap |
| FIND-003 | Information Exposure — x-powered-by on https://diversifiedrobotic.com/ | Security Headers | Low | high | confirmed |
| FIND-002 | Permissions-Policy on https://diversifiedrobotic.com/ | Security Headers | Low | high | confirmed |
| FIND-001 | Content-Security-Policy (CSP) on https://diversifiedrobotic.com/ | Security Headers | Medium | high | confirmed |

---


---

### FIND-001

**Title:** Content-Security-Policy (CSP) on https://diversifiedrobotic.com/

**Domain:** Security Headers

**Severity:** Medium

**Confidence:** high

**Target:** https://diversifiedrobotic.com/

**Evidence:**
- EVID-2026-03-13-001

**Observation:** No Content-Security-Policy header found.

**Risk:** Weak or missing CSP reduces browser-enforced protection against XSS and clickjacking-related abuse.

**Recommendation:** Implement a Content-Security-Policy header. Start with a report-only policy to observe violations before enforcing. At minimum restrict default-src to 'self'. Avoid 'unsafe-inline' and 'unsafe-eval'.

**Acceptance Criteria Mapping:** Headers-Advisory-1 — Missing Content-Security-Policy

**Status:** confirmed

**Review Type:** passive

**Opened:** 2026-03-13

**Closed:** open

**Closure Evidence:** (none — finding is open)


---

### FIND-002

**Title:** Permissions-Policy on https://diversifiedrobotic.com/

**Domain:** Security Headers

**Severity:** Low

**Confidence:** high

**Target:** https://diversifiedrobotic.com/

**Evidence:**
- EVID-2026-03-13-001

**Observation:** Permissions-Policy header is absent.

**Risk:** Browser features may be available more broadly than intended, increasing unnecessary client-side attack surface.

**Recommendation:** Add a Permissions-Policy header to restrict access to browser features (e.g., camera, microphone, geolocation). Example: Permissions-Policy: camera=(), microphone=(), geolocation=()

**Acceptance Criteria Mapping:** Headers-Advisory-3 — Missing Permissions-Policy

**Status:** confirmed

**Review Type:** passive

**Opened:** 2026-03-13

**Closed:** open

**Closure Evidence:** (none — finding is open)


---

### FIND-003

**Title:** Information Exposure — x-powered-by on https://diversifiedrobotic.com/

**Domain:** Security Headers

**Severity:** Low

**Confidence:** high

**Target:** https://diversifiedrobotic.com/

**Evidence:**
- EVID-2026-03-13-001

**Observation:** Header 'x-powered-by: Next.js' reveals technology stack information.

**Risk:** Verbose technology disclosures can help attackers tailor reconnaissance and exploit selection.

**Recommendation:** Remove or suppress the x-powered-by response header in your server/framework configuration.

**Acceptance Criteria Mapping:** Headers-Pass-Threshold — Review against Security Headers & Transport baseline

**Status:** confirmed

**Review Type:** passive

**Opened:** 2026-03-13

**Closed:** open

**Closure Evidence:** (none — finding is open)


---

### FIND-004

**Title:** TLS — Cipher Suite Enumeration on https://diversifiedrobotic.com/

**Domain:** TLS / Certificate

**Severity:** Info

**Confidence:** low

**Target:** https://diversifiedrobotic.com/

**Evidence:**
- EVID-2026-03-13-002

**Observation:** Only the negotiated cipher suite is visible from a passive connection: TLS_AES_256_GCM_SHA384. Full cipher suite enumeration requires authorized active TLS scanning.

**Risk:** Cipher support breadth is unknown, so weak ciphers cannot yet be ruled out with confidence.

**Recommendation:** [REQUIRES AUTHORIZED ACTIVE TESTING] Run testssl.sh or SSL Labs API to enumerate all supported cipher suites and identify weak ciphers.

**Acceptance Criteria Mapping:** Headers-Review-Gap — Full cipher suite validation requires authorized active TLS scanning

**Status:** review-gap

**Review Type:** passive

**Opened:** 2026-03-13

**Closed:** open

**Closure Evidence:** (none — finding is open)

