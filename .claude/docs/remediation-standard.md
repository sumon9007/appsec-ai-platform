# Remediation Standard

Defines remediation priority tiers, SLA expectations per severity level, and the evidence required to close a finding.

---

## Remediation SLA by Severity

| Severity | Fix Deadline | Escalation if Missed | Interim Mitigation Required? |
|----------|-------------|---------------------|------------------------------|
| **Critical** | Within 24 hours of confirmation | Immediate escalation to CISO / senior management | Yes — mitigating control or feature disable required immediately |
| **High** | Within 7 days of confirmation | Escalate to development manager and product owner | Yes — compensating control documented within 48 hours |
| **Medium** | Within 30 days of confirmation | Raise at next scheduled review | Recommended — risk acceptance form if not mitigated |
| **Low** | Within 90 days of confirmation | Raise at next quarterly audit | Optional — at team discretion |
| **Info** | Next scheduled audit cycle | Note in next cycle's review | Not required |

---

## Remediation Priority Tiers

### Tier 1 — Emergency (Critical)

Findings that require immediate action regardless of release schedule or sprint planning.

**Criteria:** CVSS ≥ 9.0, or immediate exploitation risk, or active exploitation confirmed.

**Process:**
1. Immediately notify security lead and engineering lead
2. Assess whether the affected feature or system should be disabled until fixed
3. Implement emergency patch or interim mitigation within 24 hours
4. Deploy fix with expedited review process
5. Verify fix and collect evidence of remediation
6. Document root cause and add to lessons-learned register

### Tier 2 — High Priority (High)

Findings that must be fixed within the current sprint or the next sprint at the latest.

**Criteria:** CVSS 7.0–8.9, or significant control failure likely exploitable.

**Process:**
1. Create a ticket in the issue tracker with High priority label
2. Assign to a responsible developer
3. Document interim compensating control within 48 hours
4. Fix delivered within 7 days
5. Security review of the fix before deployment
6. Verify fix and collect evidence of remediation

### Tier 3 — Standard (Medium)

Findings that should be prioritized within the current month's backlog.

**Criteria:** CVSS 4.0–6.9, or meaningful weakness requiring conditions to exploit.

**Process:**
1. Create a ticket in the issue tracker
2. Include in the next sprint planning
3. Fix delivered within 30 days
4. Standard code review process
5. Verify fix in testing environment

### Tier 4 — Low Priority (Low)

Findings addressed in the normal security improvement backlog.

**Criteria:** CVSS 0.1–3.9, or minor issue with limited exploitability.

**Process:**
1. Log in the findings register
2. Include in quarterly backlog grooming
3. Fix within 90 days or formally accepted with justification

### Tier 5 — Informational (Info)

Observations reviewed and addressed at the team's discretion in the next audit cycle.

---

## Risk Acceptance

When a finding cannot be remediated within the SLA, a formal risk acceptance must be documented:

| Field | Value |
|-------|-------|
| Finding ID | [FIND-NNN] |
| Severity | [Severity] |
| Risk Accepted By | [Name and title of accepting party] |
| Acceptance Date | [YYYY-MM-DD] |
| Justification | [Why remediation within SLA is not feasible] |
| Compensating Controls | [What mitigating controls are in place] |
| Review Date | [Date by which the risk acceptance will be reviewed] |
| Accepted Risk Expiry | [Date after which this acceptance expires and must be renewed] |

Risk acceptance does not close a finding. The finding remains open until remediated. The finding status is updated to "Risk Accepted" with the acceptance record attached.

---

## Evidence of Fix Requirements

A finding may only be closed when the following conditions are met:

### Required Evidence of Remediation

| Fix Type | Evidence Required |
|----------|-----------------|
| Code change | Pull request / commit reference + code review approval |
| Configuration change | Before/after configuration capture (EVID- labeled) |
| Dependency update | Updated dependency manifest showing fixed version |
| Server setting change | HTTP response or tool output confirming the change (EVID- labeled) |
| Process change | Written description of the new process + manager sign-off |

### Verification Steps

1. Auditor reviews the evidence of fix
2. Auditor re-tests the finding in the appropriate environment (staging or production)
3. Re-test result is captured as a new evidence item (EVID- labeled, noted as "re-test")
4. Finding status is updated to Closed with the fix evidence reference and re-test evidence reference
5. Close date is recorded in the findings register

### Verification Evidence Labeling

Re-test evidence is labeled identically to standard evidence but with a note in the description:

```
EVID-2026-04-01-005-retest-FIND-003-hsts-now-present.md
```

---

## Remediation Tracking

All findings must be tracked in the findings register (`.claude/templates/findings-register-template.md`) with:

- Current status: **Open / In Progress / Risk Accepted / Closed**
- Assignee
- Target remediation date (SLA deadline)
- Actual close date (when closed)
- Fix evidence reference(s)

The findings register is the single source of truth for finding status. Do not close findings in reports without updating the register.

---

## Recurring Findings

If a finding that was previously closed reappears in a subsequent audit, it is treated as a **regression**:

1. A new Finding ID is assigned (the old ID is not re-opened)
2. The new finding references the original finding in its Notes field
3. The severity of a regression may be escalated one level (e.g., Low → Medium) to reflect the repeat nature
4. The root cause analysis from the prior remediation should be reviewed to understand why the regression occurred
