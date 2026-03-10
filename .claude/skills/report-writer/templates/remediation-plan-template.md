# Security Remediation Plan

**Application:** [PLACEHOLDER]
**Plan Date:** [PLACEHOLDER — YYYY-MM-DD]
**Plan Version:** [PLACEHOLDER — e.g., v1.0]
**Based on Audit:** [PLACEHOLDER — Audit ID and type]
**Prepared By:** [PLACEHOLDER]
**Plan Owner:** [PLACEHOLDER — Development manager or security lead]

---

## Plan Overview

| Metric | Value |
|--------|-------|
| Total open findings | [N] |
| Critical (24-hour SLA) | [N] |
| High (7-day SLA) | [N] |
| Medium (30-day SLA) | [N] |
| Low (90-day SLA) | [N] |
| Overdue findings | [N] |
| Risk-accepted findings | [N] |

---

## SLA Reference

| Severity | SLA | Escalation |
|----------|-----|-----------|
| Critical | 24 hours from identification | Immediate — CISO / Senior management |
| High | 7 days | Development manager + Product owner |
| Medium | 30 days | Next sprint planning |
| Low | 90 days | Next quarterly backlog |
| Info | Next audit cycle | — |

---

## Critical Findings — Action Required Within 24 Hours

| Finding ID | Title | Date Found | SLA Deadline | Status | Owner | Verification Method |
|------------|-------|------------|-------------|--------|-------|---------------------|
| [FIND-NNN] | [PLACEHOLDER] | [DATE] | [DATE] | [Open / In Progress] | [PLACEHOLDER] | [PLACEHOLDER] |

### FIND-NNN: [Finding Title]

**Action Required:** [PLACEHOLDER — Specific remediation action]

**Implementation Guidance:** [PLACEHOLDER — How to fix this specifically]

**Verification:** [PLACEHOLDER — How to confirm the fix is complete, e.g., "Re-test the endpoint and confirm 403 is returned for cross-user access attempts"]

**Interim Mitigation (if full fix not immediately possible):** [PLACEHOLDER — Compensating control to apply immediately]

**Owner:** [PLACEHOLDER]
**Target Date:** [PLACEHOLDER — SLA deadline]
**Status:** [Open / In Progress / Completed]
**Fix Evidence:** [PLACEHOLDER — to be filled when remediated: PR/commit reference, EVID- label]

---

## High Findings — Action Required Within 7 Days

| Finding ID | Title | Date Found | SLA Deadline | Overdue? | Status | Owner | Target Date |
|------------|-------|------------|-------------|----------|--------|-------|-------------|
| [FIND-NNN] | [PLACEHOLDER] | [DATE] | [DATE] | [Yes/No] | [Open] | [PLACEHOLDER] | [DATE] |
| [FIND-NNN] | [PLACEHOLDER] | [DATE] | [DATE] | [Yes/No] | [In Progress] | [PLACEHOLDER] | [DATE] |

### FIND-NNN: [Finding Title]

**Action Required:** [PLACEHOLDER]

**Implementation Guidance:** [PLACEHOLDER]

**Verification:** [PLACEHOLDER]

**Owner:** [PLACEHOLDER]
**Target Date:** [PLACEHOLDER]
**Status:** [Open / In Progress]
**Fix Evidence:** [PLACEHOLDER — to be filled when remediated]

---

## Medium Findings — Action Required Within 30 Days

| Finding ID | Title | Date Found | SLA Deadline | Overdue? | Status | Owner | Target Date |
|------------|-------|------------|-------------|----------|--------|-------|-------------|
| [FIND-NNN] | [PLACEHOLDER] | [DATE] | [DATE] | [Yes/No] | [Open] | [PLACEHOLDER] | [DATE] |
| [FIND-NNN] | [PLACEHOLDER] | [DATE] | [DATE] | [Yes/No] | [Open] | [PLACEHOLDER] | [DATE] |
| [FIND-NNN] | [PLACEHOLDER] | [DATE] | [DATE] | [Yes/No] | [Open] | [PLACEHOLDER] | [DATE] |

### FIND-NNN: [Finding Title]

**Action Required:** [PLACEHOLDER]

**Implementation Guidance:** [PLACEHOLDER]

**Verification:** [PLACEHOLDER]

**Owner:** [PLACEHOLDER]
**Target Date:** [PLACEHOLDER]
**Status:** [Open]
**Fix Evidence:** [PLACEHOLDER — to be filled when remediated]

---

## Low Findings — Action Required Within 90 Days

| Finding ID | Title | Date Found | SLA Deadline | Status | Owner | Target Date |
|------------|-------|------------|-------------|--------|-------|-------------|
| [FIND-NNN] | [PLACEHOLDER] | [DATE] | [DATE] | [Open] | [PLACEHOLDER] | [DATE] |
| [FIND-NNN] | [PLACEHOLDER] | [DATE] | [DATE] | [Open] | [PLACEHOLDER] | [DATE] |

---

## Informational Findings — Review at Next Audit Cycle

| Finding ID | Title | Notes |
|------------|-------|-------|
| [FIND-NNN] | [PLACEHOLDER] | [PLACEHOLDER] |

---

## Risk Acceptance Register

Findings where remediation within SLA is not feasible and risk has been formally accepted:

| Finding ID | Title | Severity | Accepted By | Acceptance Date | Expiry Date | Compensating Control |
|------------|-------|----------|-------------|----------------|-------------|---------------------|
| [FIND-NNN] | [PLACEHOLDER] | [SEVERITY] | [NAME / TITLE] | [DATE] | [DATE] | [PLACEHOLDER] |

---

## Overdue Findings

Findings that have exceeded their SLA deadline and have no risk acceptance on file. These require immediate attention:

| Finding ID | Title | Severity | SLA Deadline | Days Overdue | Escalation Required |
|------------|-------|----------|-------------|-------------|---------------------|
| [FIND-NNN] | [PLACEHOLDER] | [SEVERITY] | [DATE] | [N] | [Yes — [Escalation path]] |

---

## Verification Process

When a finding is remediated:

1. Developer/owner updates ticket and provides fix evidence (PR, commit, config change, etc.)
2. Security lead reviews fix evidence
3. Security lead performs verification re-test in appropriate environment
4. Re-test result is documented as a new EVID- evidence item
5. Finding status is updated to Closed in the findings register
6. Close date is recorded

---

## Plan Review Schedule

| Review Date | Reviewer | Purpose |
|-------------|----------|---------|
| [DATE +7d] | Security lead | Critical and High findings status check |
| [DATE +30d] | Security lead + Dev manager | Full plan review |
| [DATE — next audit] | Security lead | Pre-audit plan status review |

---

*Remediation plan prepared by: [PLACEHOLDER] | Version: [PLACEHOLDER] | Date: [PLACEHOLDER]*
