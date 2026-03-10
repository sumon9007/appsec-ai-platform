# Reporting Standard

Defines the structure, vocabulary, and conventions for all security audit reports produced by this workspace.

---

## Report Types

| Type | Template | Audience | Typical Length |
|------|---------|----------|---------------|
| Executive Summary | `.claude/skills/report-writer/templates/executive-summary-template.md` | Leadership, non-technical stakeholders | 1–2 pages |
| Technical Report | `.claude/skills/report-writer/templates/technical-report-template.md` | Development team, security team | Variable — one section per finding |
| Remediation Plan | `.claude/skills/report-writer/templates/remediation-plan-template.md` | Development team, project managers | Variable — one row per finding |
| Weekly Summary | `.claude/templates/weekly-summary-template.md` | Security team, dev lead | 1 page |
| Monthly Summary | `.claude/templates/monthly-summary-template.md` | Security and development leads | 2–3 pages |
| Quarterly Summary | `.claude/templates/quarterly-summary-template.md` | Security lead, management | 3–5 pages |
| Release Gate | `.claude/templates/release-gate-template.md` | Dev lead, security lead, product owner | 1–2 pages |
| Annual Review | `.claude/templates/annual-review-template.md` | CISO, leadership, full team | Comprehensive |

---

## Severity Vocabulary

All findings must use exactly one of these severity labels. No other labels are permitted.

| Severity | Definition | Typical Response |
|----------|-----------|-----------------|
| **Critical** | Immediate exploitation risk. Data breach, full system compromise, or equivalent impact is possible without special preconditions. | Immediate action required. Notify stakeholders. Block release if in release gate. |
| **High** | Significant security control failure. Exploitation is likely with limited effort. Impact is substantial (significant data exposure, account takeover, privilege escalation). | Fix within 7 days. Escalate to management. May block release. |
| **Medium** | Meaningful security weakness. Exploitation requires specific conditions or user interaction. Impact is moderate. | Fix within 30 days. Track in findings register. |
| **Low** | Minor issue with limited direct impact. May contribute to a multi-step attack chain. | Fix within 90 days. Include in next scheduled remediation cycle. |
| **Info** | Observation of interest. No direct security risk identified. May indicate an area for improvement or a control gap worth monitoring. | Review in next audit cycle. No urgent action required. |

---

## Finding Format

Each finding in the technical report must follow this structure:

```
### [FIND-NNN] Finding Title

| Field | Value |
|-------|-------|
| Finding ID | FIND-NNN |
| Title | [Finding title] |
| Severity | Critical / High / Medium / Low / Info |
| Domain | [Audit domain] |
| Status | Open / In Progress / Closed |
| Date Identified | YYYY-MM-DD |

**Description:**
[Clear, technical description of the vulnerability or weakness. Explain what the issue is and where it was observed. Avoid speculation.]

**Evidence:**
[Reference to evidence item(s): EVID-YYYY-MM-DD-NNN]

**Impact:**
[What could an attacker achieve by exploiting this? Be specific. Reference the data, accounts, or functionality at risk.]

**Recommendation:**
[Actionable remediation guidance. Be specific about the implementation change required. Reference standards or guidance where applicable (e.g., OWASP, NIST, CWE).]

**References:**
- [CWE / CVE / OWASP reference where applicable]
```

---

## Finding Numbering

Finding IDs follow the format `FIND-NNN` where NNN is a sequential number within the engagement:

- `FIND-001`, `FIND-002`, ... `FIND-099`, `FIND-100`
- Numbers are assigned in the order findings are recorded
- Do not reuse or re-assign finding IDs once assigned
- Closed findings retain their ID — do not remove closed findings from the register

---

## Report Filename Convention

All reports must be saved using this naming convention:

```
YYYY-MM-DD-[type]-report.md
```

Examples:
- `2026-03-11-weekly-report.md`
- `2026-03-15-quarterly-technical-report.md`
- `2026-03-15-quarterly-executive-summary.md`
- `2026-Q1-annual-review.md`

Draft reports: `reports/draft/YYYY-MM-DD-[type]-report.md`
Final reports: `reports/final/YYYY-MM-DD-[type]-report.md`

---

## Executive Summary Standards

The executive summary is for non-technical leadership and must:

- Be written in plain English without technical jargon
- Not include HTTP headers, code samples, or technical configuration details
- Summarize findings by severity count (e.g., "2 Critical, 3 High, 7 Medium")
- State the overall risk posture in a single clear sentence
- Include recommended priorities without technical implementation detail
- Include the audit scope and period at the top
- Be no longer than 2 pages

**Prohibited in executive summaries:**
- Raw HTTP requests or responses
- Stack traces or log excerpts
- CVE numbers (reference "known vulnerable component" instead)
- Speculation about exploitation that is not evidenced

---

## Technical Report Standards

The technical report is for the development and security teams and must:

- Include a complete findings table (all findings in the engagement)
- Include a full finding detail section for each finding
- Reference all evidence items by label (EVID-YYYY-MM-DD-NNN)
- Include methodology description
- Include appendices for tool outputs, scan results, or configuration details
- Be accurate — do not simplify or editorialize the technical details

---

## Prohibited Practices

- Do not include speculative findings — every finding must have evidence
- Do not use severity labels outside the defined vocabulary (e.g., "Severe", "Informational" — use the exact labels above)
- Do not include recommendation for findings without a specific, actionable remediation step
- Do not publish raw evidence containing PII or credentials in final reports
- Do not omit the evidence reference from any finding
- Do not skip the executive summary for formal reports delivered to clients or leadership
