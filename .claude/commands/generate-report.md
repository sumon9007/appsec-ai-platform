# Command: /generate-report

Generate a security audit report from the active findings. Produces both an executive summary and a technical report.

## Trigger

Invoked when the user wants to produce a formal security report from collected findings. Can be run at any point during or after an audit.

---

## Pre-Conditions

1. At least one finding is recorded in the findings register
2. All findings have evidence references (EVID- labels)
3. `.claude/context/audit-context.md` is populated for engagement metadata

---

## Steps

### Step 1: Load Report Writer Skill

Load: `.claude/skills/report-writer/SKILL.md`

Read all templates:
- `.claude/skills/report-writer/templates/executive-summary-template.md`
- `.claude/skills/report-writer/templates/technical-report-template.md`

Read reporting standards:
- `.claude/docs/reporting-standard.md`
- `.claude/rules/reporting-rules.md`
- `.claude/rules/severity-rating-rules.md`

### Step 2: Read All Active Findings

1. Read the current findings register
2. Read all individual finding records in `audit-runs/active/` or `audit-runs/completed/`
3. Compile: total findings by severity (Critical, High, Medium, Low, Info)
4. Identify: top 3–5 most impactful findings for the executive summary
5. Confirm: every finding has a severity label, evidence reference, and recommendation

If any finding is missing required fields, flag it before proceeding.

### Step 3: Apply Severity Ratings Review

- Review each finding's severity against `.claude/rules/severity-rating-rules.md`
- Confirm no severity label deviates from the defined vocabulary
- If any finding severity appears inconsistent with the criteria, note it for review
- Do not change severity without documented justification

### Step 4: Draft Executive Summary

Using `executive-summary-template.md`:

1. Populate engagement overview: target, scope, audit period, auditor
2. Write findings summary: count by severity
3. Summarize top risks in plain, non-technical language (2–3 sentences per top finding)
4. State the overall security posture in a single clear sentence
5. List 3–5 recommended priorities (non-technical, outcome-focused)
6. Review: no HTTP headers, code samples, CVE numbers, or technical jargon

Save draft to: `reports/draft/YYYY-MM-DD-[type]-executive-summary.md`

### Step 5: Draft Technical Report

Using `technical-report-template.md`:

1. Populate cover page fields (engagement name, date, version, classification)
2. Write methodology section — how was the audit conducted, which domains covered, tools used
3. Populate the findings summary table (all findings: ID, title, severity, domain, status)
4. Write a full finding detail section for each finding:
   - Finding ID, title, severity, domain
   - Description of the vulnerability
   - Evidence references (EVID- labels)
   - Impact assessment
   - Recommendation with actionable remediation steps
   - References (CWE, OWASP, CVE as applicable)
5. Populate appendices: tool outputs, configuration extracts, methodology notes

Save draft to: `reports/draft/YYYY-MM-DD-[type]-technical-report.md`

### Step 6: Quality Review

Before finalizing, verify:

- [ ] All findings are included in both the executive summary (summarized) and technical report (full detail)
- [ ] No finding is missing an evidence reference
- [ ] No finding lacks a recommendation
- [ ] Executive summary contains no technical jargon or raw evidence
- [ ] Technical report contains exact EVID- references for all findings
- [ ] Report filename follows `YYYY-MM-DD-[type]-report.md` convention
- [ ] Overall posture statement is present in executive summary
- [ ] Report version is labeled (e.g., "DRAFT v0.1")

### Step 7: Promote to Final (When Approved)

After review and sign-off by the security lead:
1. Copy from `reports/draft/` to `reports/final/`
2. Update version label to "Final"
3. Record final report path in `.claude/context/audit-context.md` under Audit Session Log

---

## Outputs

| Output | Location | Template |
|--------|----------|---------|
| Executive summary (draft) | `reports/draft/YYYY-MM-DD-[type]-executive-summary.md` | `executive-summary-template.md` |
| Technical report (draft) | `reports/draft/YYYY-MM-DD-[type]-technical-report.md` | `technical-report-template.md` |

---

## Related Commands

- `/generate-remediation-plan` — Generate a prioritized remediation plan from the findings register
