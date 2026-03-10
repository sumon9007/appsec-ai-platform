# Command: /audit-monthly

Monthly security audit with broader domain coverage including RBAC review, input validation spot-check, TLS status, and full dependency scan.

## Trigger

Invoked at the start of each month's security review cycle. Designed to take 4–8 hours. Produces a monthly summary and an updated findings register.

---

## Pre-Conditions

1. `.claude/context/audit-context.md` is populated and Authorization Status is **CONFIRMED**
2. `.claude/context/scope.md` is current
3. Weekly summaries from the past month are available for review
4. Current dependency manifests are available

---

## Steps

### Step 1: Context Load

1. Read `.claude/context/audit-context.md` — confirm authorization
2. Read `.claude/context/target-profile.md` — note any tech stack changes
3. Read `.claude/context/scope.md` — confirm scope unchanged or note any scope changes
4. Read `.claude/context/assumptions.md` — review and update any assumptions
5. Review the past month's weekly summaries from `audits/weekly/`
6. Read `.claude/rules/severity-rating-rules.md` and `.claude/rules/evidence-quality-rules.md`

### Step 2: Load Relevant Skills

Load these skills for the monthly audit:

1. `.claude/skills/headers-tls-audit/SKILL.md`
2. `.claude/skills/auth-access-audit/SKILL.md`
3. `.claude/skills/rbac-audit/SKILL.md`
4. `.claude/skills/input-validation-audit/SKILL.md`
5. `.claude/skills/dependency-audit/SKILL.md`
6. `.claude/skills/logging-monitoring-audit/SKILL.md`
7. `.claude/skills/session-jwt-audit/SKILL.md`

### Step 3: All Weekly Checks

Run all checks from `/audit-weekly`:

- Security headers review
- Authentication change review
- CVE check for new disclosures
- Log anomaly review

### Step 4: RBAC Spot-Check

Skill: `.claude/skills/rbac-audit/`
Templates: `rbac-test-matrix.md`, `idor-review-template.md`

- Review the role permission matrix for any changes since last month
- Spot-check 2–3 key endpoints for proper authorization enforcement
- Test horizontal access (IDOR) on one to two key object types
- Document any role drift or new authorization issues

### Step 5: Input Validation Spot-Check

Skill: `.claude/skills/input-validation-audit/`
Template: `validation-review-template.md`

- Select 3–5 high-risk input points (search, forms, file upload, API endpoints)
- Review validation controls for each selected input
- Note any new endpoints introduced in the past month
- Document observations in `validation-review-template.md`

### Step 6: TLS Certificate and Cipher Review

Skill: `.claude/skills/headers-tls-audit/`
Template: `tls-review-template.md`

- Full TLS review using `tls-review-template.md`
- Confirm TLS version restrictions (TLS 1.2 minimum)
- Check cipher suite configuration
- Confirm certificate validity and expiry timeline
- Check HSTS preload status

### Step 7: Full Dependency Scan

Skill: `.claude/skills/dependency-audit/`
Templates: `dependency-findings-template.md`, `vulnerable-component-review.md`

- Full review of all dependencies against CVE databases
- Categorize: Critical, High, Medium, Low, No Known CVE
- For any Critical or High CVE: complete `vulnerable-component-review.md`
- Note unmaintained packages (last release > 24 months)
- Document license risks if identified

### Step 8: New Features Security Review

- Review any new features or significant changes deployed in the past month
- Assess each new feature against the PRD security analysis guide (`.claude/docs/prd-analysis.md`)
- Note any new attack surface introduced
- Determine if any new features require a deeper domain-specific review

### Step 9: Open Findings Review

1. Review all open findings in the findings register
2. Update status for any findings that have been remediated
3. Verify evidence of fix for findings marked as closed
4. Flag any findings past their SLA deadline for escalation
5. Note findings approaching SLA deadline in the monthly summary

### Step 10: Produce Monthly Summary

1. Complete `.claude/templates/monthly-summary-template.md`
2. Save to `audits/monthly/YYYY-MM-DD-monthly.md`
3. Include: key risk changes, new issues, items escalated, remediation recommendations

---

## Outputs

| Output | Location | Template |
|--------|----------|---------|
| Monthly summary | `audits/monthly/YYYY-MM-DD-monthly.md` | `monthly-summary-template.md` |
| Updated findings register | Current findings register | `findings-register-template.md` |
| TLS review | `audit-runs/completed/` | `tls-review-template.md` |
| Dependency findings | `audit-runs/completed/` | `dependency-findings-template.md` |
| New evidence items | `evidence/raw/` | EVID- convention |

---

## Escalation

Escalate to development manager and product owner if:

- Any new Critical or High finding is identified
- Any finding has exceeded its SLA deadline without a risk acceptance on file
- Significant new attack surface was introduced without security review
