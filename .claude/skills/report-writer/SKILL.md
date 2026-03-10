# Skill: Security Report Writer

## Purpose

Generate professional, audience-appropriate security audit reports and remediation plans from collected audit findings. Produces executive summaries for non-technical leadership, technical reports for development and security teams, and prioritized remediation plans for project management.

---

## Inputs Required

| Input | Source | Required? |
|-------|--------|-----------|
| Completed findings register | Current findings register | Required |
| Individual finding records | `audit-runs/` | Required |
| Audit context | `.claude/context/audit-context.md` | Required |
| Reporting standards | `.claude/docs/reporting-standard.md` | Required |
| Remediation standards | `.claude/docs/remediation-standard.md` | Required |

---

## Method

### Phase 1: Pre-Report Preparation

1. Read `.claude/docs/reporting-standard.md` in full
2. Read `.claude/rules/reporting-rules.md` in full
3. Read `.claude/rules/severity-rating-rules.md` and verify all findings use the standard severity vocabulary
4. Read all findings in the register — compile summary statistics:
   - Total findings by severity (Critical, High, Medium, Low, Info)
   - Findings by domain
   - Open vs. closed findings
   - Findings with missing evidence or recommendations (flag for correction before writing)
5. Identify the top 3–5 findings by impact for executive summary highlights

### Phase 2: Executive Summary

Using `executive-summary-template.md`:

6. Populate engagement metadata (target, scope, period, auditor)
7. Write a one-sentence overall security posture statement
8. Write findings summary: severity counts in a simple table
9. Summarize the top 3–5 findings in plain, non-technical language (2–3 sentences each)
10. Write recommended priorities — outcome-focused, non-technical (e.g., "Address the ability of users to access other users' account data" rather than "Fix IDOR on /api/users/:id")
11. Quality check: no HTTP headers, CVE numbers, code, stack traces, or technical jargon in the executive summary

### Phase 3: Technical Report

Using `technical-report-template.md`:

12. Populate cover page (engagement name, date, version, classification)
13. Write methodology section:
    - Audit type and cadence
    - Domains covered
    - Testing approach (passive review / active testing)
    - Tools and data sources used
14. Populate the findings summary table (all findings)
15. For each finding, write the full finding detail section:
    - Finding ID, title, severity, domain, status, date identified
    - Technical description — precise, factual, based on evidence
    - Evidence references (EVID-YYYY-MM-DD-NNN) — every finding must have at least one
    - Impact assessment — specific, what an attacker could achieve
    - Recommendation — specific, actionable, implementation-level detail
    - References (CWE, CVE, OWASP as applicable)
16. Populate appendices:
    - Methodology details
    - Tool outputs or scan results
    - Scope confirmation

### Phase 4: Remediation Plan

Using `remediation-plan-template.md`:

17. Read `.claude/docs/remediation-standard.md` for SLA requirements
18. Filter findings to open and in-progress only
19. Sort by severity (Critical first, then High, Medium, Low, Info)
20. Within each tier, sort by finding age (oldest SLA deadline first)
21. For each finding:
    - Calculate SLA deadline (date found + severity SLA)
    - Flag overdue findings
    - Provide actionable remediation action
    - Leave owner and target date fields for the development team to populate
22. Include summary statistics: total open findings, overdue count, upcoming deadlines

### Phase 5: Quality Assurance

23. Verify before finalizing:
    - Every finding in the technical report has an evidence reference
    - Every finding has a recommendation
    - The executive summary is free of technical jargon
    - Report filenames follow the YYYY-MM-DD-[type]-report.md convention
    - Version label is present
    - No sensitive evidence (credentials, PII) is included in the report body

---

## Outputs

| Output | Template | Description |
|--------|---------|-------------|
| Executive summary | `executive-summary-template.md` | Non-technical leadership report |
| Technical report | `technical-report-template.md` | Full technical detail for dev/sec teams |
| Remediation plan | `remediation-plan-template.md` | Prioritized action plan with SLA tracking |

---

## Templates Used

- `.claude/skills/report-writer/templates/executive-summary-template.md`
- `.claude/skills/report-writer/templates/technical-report-template.md`
- `.claude/skills/report-writer/templates/remediation-plan-template.md`

---

## References

- `.claude/docs/reporting-standard.md` — definitive reporting standards for this workspace
- `.claude/rules/reporting-rules.md` — enforced reporting rules
- [OWASP Testing Guide — Reporting](https://owasp.org/www-project-web-security-testing-guide/stable/5-Reporting/)
