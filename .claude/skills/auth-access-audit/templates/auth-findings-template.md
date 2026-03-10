# Authentication Finding Record

Use this template for each finding identified during the authentication and access control audit. One record per finding.

---

## Finding Record

| Field | Value |
|-------|-------|
| **Finding ID** | [PLACEHOLDER — e.g., FIND-001] |
| **Title** | [PLACEHOLDER — e.g., "Login endpoint does not implement rate limiting"] |
| **Severity** | [PLACEHOLDER — Critical / High / Medium / Low / Info] |
| **Domain** | Authentication & Access Control |
| **Status** | Open |
| **Date Identified** | [YYYY-MM-DD] |
| **Identified By** | [PLACEHOLDER — Auditor name] |

---

## Description

[PLACEHOLDER — Clear, factual description of the vulnerability or weakness. Describe what was observed, where it was found, and why it constitutes a security issue. Do not speculate beyond what the evidence demonstrates.]

---

## Evidence

| Evidence ID | Description | Location |
|-------------|-------------|---------|
| [EVID-YYYY-MM-DD-NNN] | [PLACEHOLDER — What the evidence shows] | `evidence/raw/[filename]` |
| [EVID-YYYY-MM-DD-NNN] | [PLACEHOLDER] | `evidence/raw/[filename]` |

---

## Reproduction Steps

[PLACEHOLDER — Step-by-step instructions to reproduce the finding:]

1. [PLACEHOLDER — Step 1]
2. [PLACEHOLDER — Step 2]
3. [PLACEHOLDER — Step 3]
4. [PLACEHOLDER — Observed result]

---

## Impact

[PLACEHOLDER — What could an attacker achieve by exploiting this finding? Be specific about:]
- **Confidentiality impact:** [PLACEHOLDER — e.g., "An attacker could enumerate valid email addresses"]
- **Integrity impact:** [PLACEHOLDER — e.g., "Attacker could gain unauthorized access to accounts"]
- **Availability impact:** [PLACEHOLDER — e.g., "Brute force could lock out legitimate users"]

---

## Recommendation

[PLACEHOLDER — Specific, actionable remediation guidance. Include implementation details where possible.]

**Recommended action:**
- [PLACEHOLDER — Primary recommended fix, e.g., "Implement rate limiting of 5 attempts per 15 minutes per IP on the /login endpoint"]
- [PLACEHOLDER — Secondary recommendation if applicable]

**Reference guidance:**
- [PLACEHOLDER — e.g., OWASP Authentication Cheat Sheet, NIST SP 800-63B]

---

## References

- [PLACEHOLDER — CWE-xxx: [CWE Title]]
- [PLACEHOLDER — OWASP reference]

---

## Remediation Tracking

| Field | Value |
|-------|-------|
| Assigned To | [PLACEHOLDER] |
| Target Fix Date | [PLACEHOLDER — SLA deadline per `.claude/docs/remediation-standard.md`] |
| Fix Evidence | [PLACEHOLDER — to be completed when remediated] |
| Close Date | [PLACEHOLDER] |
| Status | Open |

---

*Template: auth-findings-template.md*
