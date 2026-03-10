# Release Security Gate

**Application:** [PLACEHOLDER]
**Release Version:** [PLACEHOLDER — e.g., v2.4.0]
**Gate Date:** [PLACEHOLDER — YYYY-MM-DD]
**Assessor:** [PLACEHOLDER]
**Authorization Reference:** [PLACEHOLDER]

---

## Gate Decision

> **GATE DECISION: [PASS / CONDITIONAL PASS / FAIL]**

This release [may / may not / may conditionally] proceed to production deployment based on the security review findings below.

---

## Release Summary

| Field | Value |
|-------|-------|
| **Release Version** | [PLACEHOLDER] |
| **Deployment Target** | [PLACEHOLDER — Production / Staging] |
| **Planned Deploy Date** | [PLACEHOLDER] |
| **New Features in Release** | [N features reviewed] |
| **New Dependencies Added** | [N packages] |
| **Infrastructure Changes** | [Yes / No] |
| **Prior Findings Addressed** | [N of N open High/Critical] |

---

## New Features Security Review

| Feature | Attack Surface Introduced | Findings | Risk Level |
|---------|--------------------------|----------|------------|
| [PLACEHOLDER — e.g., User file export] | [PLACEHOLDER — e.g., New data export endpoint, authorization required] | [FIND-NNN or "None"] | [Low/Medium/High] |
| [PLACEHOLDER] | [PLACEHOLDER] | [FIND-NNN or "None"] | [Low/Medium/High] |

**New findings from release review:**

| Finding ID | Title | Severity | Domain | Status |
|------------|-------|----------|--------|--------|
| [FIND-NNN] | [PLACEHOLDER] | [SEVERITY] | [DOMAIN] | Open |

**Total new findings from release:** [N] | Critical: [N] | High: [N] | Medium: [N] | Low: [N]

---

## New Attack Surface Assessment

[PLACEHOLDER — Describe any new attack surface introduced by this release:]

- New endpoints: [PLACEHOLDER — list or "None"]
- New parameters/inputs: [PLACEHOLDER or "None"]
- New integrations: [PLACEHOLDER or "None"]
- Changes to authentication or session handling: [PLACEHOLDER or "None"]
- Infrastructure changes: [PLACEHOLDER or "None"]

---

## New Dependencies Review

| Package | Version | CVE(s) | Action Required |
|---------|---------|--------|----------------|
| [PLACEHOLDER] | [PLACEHOLDER] | [CVE-XXXX or "None"] | [PLACEHOLDER or "No action required"] |

---

## Prior Findings Remediation Status

Review of all open Critical and High findings from prior audits:

| Finding ID | Title | Severity | Required for Pass? | Status | Fix Evidence |
|------------|-------|----------|-------------------|--------|-------------|
| [FIND-NNN] | [PLACEHOLDER] | Critical | **Yes** | [Closed / Open — BLOCKS RELEASE] | [EVID-NNN or "Pending"] |
| [FIND-NNN] | [PLACEHOLDER] | High | **Yes** | [Closed / Risk Accepted] | [EVID-NNN] |
| [FIND-NNN] | [PLACEHOLDER] | Medium | No | [Open] | — |

**All Critical findings closed:** [Yes / No — if No, this is an automatic FAIL]
**All High findings closed or risk-accepted:** [Yes / No]

---

## Security Controls Regression Check

Verify that known-good controls have not regressed:

| Control | Status Before Release | Status After Release | Regression? |
|---------|----------------------|---------------------|-------------|
| Security headers (HSTS, CSP, etc.) | [PASS] | [PASS / FAIL] | [No / YES — FINDING REQUIRED] |
| Authentication controls | [PASS] | [PASS / FAIL] | [No / YES] |
| TLS/Certificate | [PASS] | [PASS / FAIL] | [No / YES] |
| Rate limiting | [PASS] | [PASS / FAIL] | [No / YES] |

---

## Gate Decision Rationale

### Pass Criteria Met?

| Criterion | Met? |
|-----------|------|
| Zero Critical findings open | [Yes / No] |
| Zero High findings open without risk acceptance | [Yes / No] |
| No Must-Fix items from this release review | [Yes / No] |
| No security control regressions | [Yes / No] |

### Gate Decision: [PASS / CONDITIONAL PASS / FAIL]

**Justification:**
[PLACEHOLDER — Brief narrative explanation of the gate decision]

**Conditions (if Conditional Pass):**
[PLACEHOLDER — List specific conditions that must be met, e.g.:]
- [e.g., "FIND-012 (High) must be remediated within 7 days of deployment and verified by security lead"]
- [e.g., "Dependency CVE-2025-XXXXX must be addressed in the next patch release (v2.4.1) within 7 days"]

**If FAIL:**
[PLACEHOLDER — List the specific blockers that must be resolved before re-evaluation]
- [e.g., "FIND-011 (Critical — authentication bypass) must be fixed and verified before release"]

---

## Sign-Off

This gate decision requires sign-off from:

| Role | Name | Decision | Date |
|------|------|----------|------|
| Security Lead | [PLACEHOLDER] | [Approved / Rejected] | [DATE] |
| Development Manager | [PLACEHOLDER] | [Approved / Rejected] | [DATE] |
| Product Owner (if FAIL) | [PLACEHOLDER] | [Acknowledged] | [DATE] |

---

*Template: release-gate-template.md*
*Saved to: `audits/release/YYYY-MM-DD-v[VERSION]-gate.md`*
