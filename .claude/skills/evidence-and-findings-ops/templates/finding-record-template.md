# Finding Record Template

Use this template to document a single finding. Copy and populate one block per finding. Add completed records to the findings register.

See `evidence-and-findings-ops` skill for classification guidance before creating a finding.

---

## Finding Record

```
Finding ID:        FIND-[NNN]
Title:             [Short, clear title — no jargon]
Domain:            [Authentication | Authorization | Session Management | Input Validation |
                    Security Headers | Dependencies | Logging | Misconfiguration | API Security]
Severity:          [Critical | High | Medium | Low | Info]
Confidence:        [high | medium | low]
Status:            [confirmed | suspected | review-gap | mitigated | accepted-risk]
Target:            [URL, endpoint, or system component]
Date Identified:   [YYYY-MM-DD]
Session:           [SESSION-YYYY-MM-DD-NNN]

Evidence:
  - EVID-[YYYY-MM-DD]-[NNN] — [brief description of what this evidence demonstrates]
  - EVID-[YYYY-MM-DD]-[NNN] — [add additional evidence items as needed]

Observation:
  [Factual description of what was observed. No speculation. If assumed, label: [ASSUMED]]

Risk:
  [What an attacker could achieve. Be specific — e.g., "An authenticated user could read
   any other user's profile by substituting their numeric ID in the /api/users/:id endpoint."]

Recommendation:
  [Specific, actionable remediation. Include implementation-level detail.
   Example: "Implement server-side ownership check on the /api/users/:id endpoint to verify
   that the authenticated user's ID matches the requested ID before returning data."]

Acceptance Criteria Mapping:
  [Which acceptance criterion does this affect? Reference from .claude/docs/acceptance-criteria.md]

References:
  [CWE-NNN, CVE-YYYY-NNNNN, OWASP link — as applicable]
```

---

## Status History

Use this section to track status changes over time:

```
[YYYY-MM-DD] Status: confirmed — Finding identified during [session/review]
[YYYY-MM-DD] Status: in-progress — Fix in development per [PR/ticket reference]
[YYYY-MM-DD] Status: mitigated — [Compensating control applied: description]
[YYYY-MM-DD] Status: closed — Fix verified via EVID-[YYYY-MM-DD]-[NNN]
```

---

## Closure Evidence

Complete when closing the finding:

```
Fix Evidence:    [PR reference | Commit hash | Config capture EVID- reference | Process doc]
Fix Description: [Brief description of what was changed]
Re-test Evidence: EVID-[YYYY-MM-DD]-[NNN] — [Description of verification performed]
Closed By:       [Auditor name]
Closed Date:     [YYYY-MM-DD]
```

---

*Template version: 1.0 | Governed by `.claude/rules/evidence-quality-rules.md` and `.claude/rules/reporting-rules.md`*
