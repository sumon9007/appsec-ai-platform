# Command: /audit-quarterly

Deep quarterly audit of all security domains, including threat model review, acceptance criteria re-evaluation, and comprehensive findings comparison.

## Trigger

Invoked at the start of each quarter's comprehensive security review. Designed to take 1–3 days. Produces a quarterly summary, updated findings register, and draft technical report.

---

## Pre-Conditions

1. `.claude/context/audit-context.md` is populated and Authorization Status is **CONFIRMED**
2. `.claude/context/scope.md` is current and signed off
3. Monthly summaries from the past quarter are available
4. Full findings register from the prior quarter is available

---

## Steps

### Step 1: Context Load and Preparation

1. Read all files in `.claude/context/`
2. Read all files in `.claude/rules/`
3. Review all monthly summaries from the past quarter (`audits/monthly/`)
4. Review the prior quarterly summary (`audits/quarterly/`)
5. Review the current findings register — note all open findings and their ages
6. Create a new audit session record: `audit-runs/active/YYYY-MM-DD-quarterly-session.md`

### Step 2: Load All Audit Skills

Load all skill SKILL.md files:

1. `.claude/skills/auth-access-audit/SKILL.md`
2. `.claude/skills/rbac-audit/SKILL.md`
3. `.claude/skills/session-jwt-audit/SKILL.md`
4. `.claude/skills/input-validation-audit/SKILL.md`
5. `.claude/skills/headers-tls-audit/SKILL.md`
6. `.claude/skills/dependency-audit/SKILL.md`
7. `.claude/skills/logging-monitoring-audit/SKILL.md`
8. `.claude/skills/security-misconfig-audit/SKILL.md`
9. `.claude/skills/report-writer/SKILL.md`

### Step 3: Threat Model Review

- Has the attack surface changed significantly this quarter?
- Are there new user roles, integrations, or data flows not in the prior threat model?
- Update `.claude/docs/prd-analysis.md` with any new features analyzed this quarter
- Note any new threat scenarios that should inform audit focus

### Step 4: Full Domain Audit — All Domains

Perform a thorough review of all domains (deeper than monthly):

#### 4.1 Security Headers & TLS (Full)
Skill: `.claude/skills/headers-tls-audit/` — use both templates

#### 4.2 Authentication & Access Control (Full)
Skill: `.claude/skills/auth-access-audit/` — complete full checklist, not just spot-check

#### 4.3 Session Management & JWT (Full)
Skill: `.claude/skills/session-jwt-audit/` — review all session handling end-to-end

#### 4.4 Authorization / RBAC (Full)
Skill: `.claude/skills/rbac-audit/` — complete full role × resource matrix

#### 4.5 Input Validation & Injection (Broad)
Skill: `.claude/skills/input-validation-audit/` — review all major input surfaces

#### 4.6 Security Misconfiguration (Full)
Skill: `.claude/skills/security-misconfig-audit/` — complete full hardening checklist

#### 4.7 Dependency / Supply Chain (Full)
Skill: `.claude/skills/dependency-audit/` — complete dependency inventory + CVE review

#### 4.8 Logging & Monitoring (Full)
Skill: `.claude/skills/logging-monitoring-audit/` — complete logging checklist + log review

### Step 5: Acceptance Criteria Re-Evaluation

1. Load `.claude/docs/acceptance-criteria.md`
2. For each domain, assess whether the application currently meets the defined pass threshold
3. Note any domains where the application falls below the minimum pass threshold
4. Note any acceptance criteria that should be updated based on changes in the threat landscape or the application

### Step 6: Findings Compilation and Comparison

1. Compile all new findings from this quarter's audit
2. Compare against prior quarter's findings:
   - Which prior findings have been closed? (positive trend)
   - Which prior findings remain open? (aging findings — escalate if past SLA)
   - Are any closed findings recurring? (regression — escalate severity)
3. Calculate remediation velocity: % of High/Critical findings closed within SLA
4. Update the full findings register with all new, updated, and closed findings

### Step 7: Draft Quarterly Summary and Reports

1. Complete `.claude/templates/quarterly-summary-template.md`
2. Save to `audits/quarterly/YYYY-MM-DD-quarterly.md`
3. Load `.claude/skills/report-writer/SKILL.md`
4. Draft technical report using `.claude/skills/report-writer/templates/technical-report-template.md`
5. Draft executive summary using `.claude/skills/report-writer/templates/executive-summary-template.md`
6. Generate remediation plan using `.claude/skills/report-writer/templates/remediation-plan-template.md`
7. Save all drafts to `reports/draft/`

### Step 8: Session Close

1. Update audit session record with findings summary
2. Move session file to `audit-runs/completed/`

---

## Outputs

| Output | Location | Template |
|--------|----------|---------|
| Quarterly summary | `audits/quarterly/YYYY-MM-DD-quarterly.md` | `quarterly-summary-template.md` |
| Updated findings register | Current register | `findings-register-template.md` |
| Technical report (draft) | `reports/draft/` | `technical-report-template.md` |
| Executive summary (draft) | `reports/draft/` | `executive-summary-template.md` |
| Remediation plan | `reports/draft/` | `remediation-plan-template.md` |

---

## Escalation

Present to engineering and product leadership if:

- Overall security posture has degraded since last quarter
- Any Critical findings remain open
- Remediation velocity is below acceptable threshold (< 80% of High findings closed within SLA)
- New Critical threat scenarios have emerged that require architectural review
