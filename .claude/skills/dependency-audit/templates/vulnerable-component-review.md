# Vulnerable Component Review

Deep-dive review of a specific vulnerable component. Complete one of these for each Critical or High severity CVE finding.

**Auditor:** [PLACEHOLDER]
**Date:** [PLACEHOLDER]
**Target:** [PLACEHOLDER]

---

## Component Identity

| Field | Value |
|-------|-------|
| **Package Name** | [PLACEHOLDER — e.g., express] |
| **Package Ecosystem** | [PLACEHOLDER — e.g., npm / pip / gem / Maven / Composer] |
| **Installed Version** | [PLACEHOLDER — e.g., 4.17.1] |
| **Latest Available Version** | [PLACEHOLDER] |
| **License** | [PLACEHOLDER] |
| **Package Repository** | [PLACEHOLDER — e.g., https://www.npmjs.com/package/express] |
| **Last Release Date** | [PLACEHOLDER] |
| **Weekly Downloads** | [PLACEHOLDER — proxy for ecosystem health] |

---

## Vulnerability Details

| Field | Value |
|-------|-------|
| **CVE ID** | [PLACEHOLDER — e.g., CVE-2022-24999] |
| **CVSSv3 Score** | [PLACEHOLDER — e.g., 7.5] |
| **CVSSv3 Vector** | [PLACEHOLDER — e.g., AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H] |
| **Vulnerability Type** | [PLACEHOLDER — e.g., Prototype Pollution / ReDoS / Path Traversal / RCE] |
| **CWE** | [PLACEHOLDER — e.g., CWE-1321: Prototype Pollution] |
| **Advisory URL** | [PLACEHOLDER — link to NVD, GitHub Advisory, or vendor advisory] |
| **Disclosure Date** | [PLACEHOLDER] |
| **CISA KEV Listed** | [Yes / No] |
| **Known Exploit Available** | [Yes / No / PoC only] |
| **Exploit in the Wild** | [Yes / No / Unknown] |

**Vulnerability Description:**
[PLACEHOLDER — Describe the vulnerability in technical terms. What is the root cause? What must an attacker do to trigger it? What is the impact?]

---

## Usage Context

**How is this component used in the application?**
[PLACEHOLDER — Describe where and how the package is used. Is it a direct dependency or transitive? Is it used in production code or only in build/test tooling?]

**Is the vulnerable functionality used?**
[PLACEHOLDER — Is the specific vulnerable function/feature/code path used by this application? If yes, describe where.]

**Affected code paths (if known):**
[PLACEHOLDER — List specific endpoints, functions, or features that use the vulnerable component.]

---

## Attack Surface Assessment

**Attack Vector:** [PLACEHOLDER — Network / Adjacent / Local / Physical]

**Authentication Required:** [PLACEHOLDER — None / Low privilege / High privilege]

**User Interaction Required:** [PLACEHOLDER — None / Required]

**Is the vulnerable entry point reachable:**
- From the public internet: [Yes / No / Unknown]
- From an authenticated user: [Yes / No / Unknown]
- From a privileged user: [Yes / No / Unknown]

**Environmental factors that reduce risk:**
[PLACEHOLDER — e.g., "The application is behind a WAF that blocks requests with prototype pollution patterns", "The vulnerable endpoint is only accessible to internal network users"]

**Effective Risk Assessment:**
[PLACEHOLDER — Based on the above, what is the actual exploitability risk in this specific environment? Does the CVSSv3 score overstate or understate the risk?]

---

## Remediation Options

### Option 1: Update to Fixed Version (Recommended)

| Field | Value |
|-------|-------|
| Fixed version | [PLACEHOLDER] |
| Breaking changes expected? | [Yes / No / Unknown] |
| Migration effort | [Low / Medium / High] |
| Testing required | [PLACEHOLDER] |

### Option 2: Interim Mitigation (If Immediate Update Not Feasible)

[PLACEHOLDER — Describe any interim controls that can reduce risk without updating the dependency:]
- WAF rule to block exploit pattern: [PLACEHOLDER — possible/not possible]
- Input sanitization at application layer: [PLACEHOLDER]
- Feature disable or restriction: [PLACEHOLDER]
- Network-level control: [PLACEHOLDER]

### Option 3: Replace Component

[PLACEHOLDER — If the package is abandoned or no fix is available:]
- Alternative package: [PLACEHOLDER]
- Migration complexity: [PLACEHOLDER]

---

## Recommendation

**Recommended Action:** [PLACEHOLDER — Update / Mitigate / Replace / Risk Accept]

**Recommended Timeline:** [PLACEHOLDER — per SLA in `.claude/docs/remediation-standard.md`]

**Steps:**
1. [PLACEHOLDER — Step 1]
2. [PLACEHOLDER — Step 2]
3. [PLACEHOLDER — Step 3]

**Verification:** After updating, verify by [PLACEHOLDER — e.g., "re-running npm audit and confirming the CVE no longer appears", "re-testing the affected endpoint for the described behavior"].

---

## Evidence

| Evidence ID | Description |
|-------------|-------------|
| [EVID-YYYY-MM-DD-NNN] | [PLACEHOLDER — e.g., npm audit output showing vulnerable version] |
| [EVID-YYYY-MM-DD-NNN] | [PLACEHOLDER — e.g., package.json showing installed version] |

---

**Finding ID:** [FIND-NNN]
**Related Findings:** [PLACEHOLDER — other finding IDs related to this component]

---

*Template: vulnerable-component-review.md*
