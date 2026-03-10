# Remediation Rules

Defines the mandatory remediation timelines, escalation requirements, and evidence standards for closing findings.

---

## Rule 1: Remediation SLAs by Severity

These are the maximum allowable timelines from finding confirmation to remediation deployment:

| Severity | SLA | Measurement Start |
|----------|-----|------------------|
| **Critical** | 24 hours | From the time the finding is confirmed and communicated to the responsible team |
| **High** | 7 calendar days | From the time the finding is confirmed and communicated |
| **Medium** | 30 calendar days | From the time the finding is confirmed and communicated |
| **Low** | 90 calendar days | From the time the finding is confirmed and communicated |
| **Info** | Next scheduled audit cycle | No hard deadline |

"Confirmed" means the finding has been reviewed, evidence has been validated, and severity has been agreed. Do not start the SLA clock from the initial discovery date if there is a delay in confirmation.

---

## Rule 2: Critical Findings — Emergency Response

For any Critical finding:

1. **Immediately notify** the security lead and engineering lead upon confirmation
2. **Within 2 hours:** Assess whether the affected feature or system should be disabled as an interim measure
3. **Within 24 hours:** Deploy a fix or implement a compensating control that reduces the risk to at most High severity
4. **Within 24 hours:** Document the compensating control if an immediate full fix is not possible
5. **As soon as possible after fix:** Collect evidence of remediation and verify the fix
6. **Root cause analysis:** Document why the vulnerability existed and what process changes prevent recurrence

---

## Rule 3: Interim Mitigation for High Findings

For High findings that cannot be fully remediated within 7 days:

1. Within 48 hours of confirmation: implement and document a compensating control
2. The compensating control must demonstrably reduce the risk (document how)
3. The finding status is updated to "In Progress — Mitigated" with the compensating control described
4. Full remediation must still occur within 30 days maximum (if the 7-day SLA is missed with a compensating control in place, escalate to management)

---

## Rule 4: Risk Acceptance

When a finding cannot be remediated within the defined SLA:

- A formal risk acceptance must be documented (see `.claude/docs/remediation-standard.md` for format)
- Risk acceptance must be signed by a person with appropriate authority:
  - Critical: CISO or equivalent
  - High: Security lead + Development manager
  - Medium/Low: Security lead
- Risk acceptance is NOT the same as closing the finding
- Risk accepted findings remain in the findings register with status "Risk Accepted"
- Risk acceptance must have an expiry date — maximum 6 months
- Risk accepted findings must be re-reviewed at the next quarterly audit

---

## Rule 5: Findings Cannot Be Closed Without Evidence

A finding may only be moved to Closed status when:

1. The responsible team provides evidence of the fix:
   - Pull request or commit reference (for code changes)
   - Configuration change capture (EVID- labeled) for infrastructure changes
   - Updated dependency manifest for dependency updates
   - Written process description for process-based fixes

2. The security auditor reviews the evidence and confirms it addresses the finding

3. The security auditor performs a verification re-test (where possible) and documents the result as a new EVID- labeled evidence item

4. Both the fix evidence and re-test evidence are referenced in the finding record before closing

---

## Rule 6: Regression Findings

If a finding that was previously closed reappears in a subsequent audit:

1. It is recorded as a **new finding** with a new Finding ID
2. The new finding notes reference the original closed finding ID
3. The severity of the regression finding is escalated one level above the original severity:
   - Example: original finding was Medium → regression finding is High
4. A mandatory root cause investigation is required:
   - Why was the fix not durable?
   - What process failure allowed the regression?
5. The regression is noted in the findings register and quarterly summary as a regression event

---

## Rule 7: Findings Register Must Stay Current

The findings register must be updated:
- At the end of every audit session
- When any finding's status changes (opened, in progress, risk accepted, closed)
- When evidence of fix is received
- Before generating any report

Reports generated from a stale findings register are invalid. Confirm the register is current before producing any output document.

---

## Rule 8: SLA Reporting

At every audit cycle, report on SLA compliance:
- Number of Critical findings closed within 24 hours vs. total Critical findings
- Number of High findings closed within 7 days vs. total High findings
- Number of findings with expired risk acceptances
- Number of findings overdue with no risk acceptance

This data is reported in the quarterly summary and annual review.
