# Command: /audit-annual

Annual comprehensive security review covering all domains, historical trends, posture comparison, and strategic recommendations for the coming year.

## Trigger

Invoked once per year for the annual comprehensive security posture review. Designed to take 3–5 days. Produces a complete annual review document, full technical report, executive summary, and strategic recommendations.

---

## Pre-Conditions

1. `.claude/context/audit-context.md` is populated and Authorization Status is **CONFIRMED**
2. All quarterly summaries from the year are available
3. Full historical findings register is available
4. Prior year's annual review is available for comparison

---

## Steps

### Step 1: Context Load and Historical Review

1. Read all files in `.claude/context/`
2. Read all files in `.claude/rules/`
3. Read all files in `.claude/docs/`
4. Review all quarterly summaries from the year (`audits/quarterly/`)
5. Review all monthly summaries from the year (`audits/monthly/`)
6. Review the prior year's annual review (`audits/annual/`)
7. Review the complete findings register — all findings, open and closed, for the year
8. Create audit session record: `audit-runs/active/YYYY-annual-session.md`

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

### Step 3: Full Domain Audit — Maximum Depth

Perform the deepest audit of all domains:

#### Authentication & Access Control
- Full checklist review
- In-depth review of all auth flows
- Complete MFA coverage assessment

#### Session Management & JWT
- Thorough JWT and session configuration review
- Test all session lifecycle events

#### Authorization / RBAC
- Complete role × resource matrix
- Comprehensive IDOR surface review
- Privilege escalation path analysis

#### Input Validation & Injection
- Review all major input surfaces
- Document injection test observations across all key endpoints

#### Security Headers & TLS
- Full headers and TLS review
- Historical comparison of header configuration changes

#### Dependency / Supply Chain
- Full dependency inventory
- CVE review for all direct and key transitive dependencies
- Supply chain risk assessment

#### Logging & Monitoring
- Full logging coverage review
- Log integrity and retention assessment
- Alerting configuration review

#### Security Misconfiguration
- Complete hardening checklist
- Infrastructure configuration review
- Cloud-specific security controls review (if applicable)

### Step 4: Historical Trend Analysis

Compile statistics from the year's findings register:

| Metric | Value |
|--------|-------|
| Total findings opened (year) | [CALCULATE] |
| Total findings closed (year) | [CALCULATE] |
| Findings open at year end | [CALCULATE] |
| Critical findings opened | [CALCULATE] |
| Critical findings closed within SLA | [CALCULATE] |
| High findings opened | [CALCULATE] |
| High findings closed within SLA | [CALCULATE] |
| Average time to remediation (Critical) | [CALCULATE] |
| Average time to remediation (High) | [CALCULATE] |
| Most frequently affected domain | [IDENTIFY] |
| Regression findings (previously closed, reopened) | [CALCULATE] |

### Step 5: Year-Over-Year Comparison

Compare current year against prior year's annual review:

- Has overall finding count increased or decreased?
- Has the severity distribution shifted?
- Which domains improved most?
- Which domains regressed?
- Are remediation SLAs being met more or less consistently?
- Have strategic recommendations from last year been implemented?

### Step 6: Posture Assessment Per Domain

For each domain, provide an annual posture rating:

| Domain | Posture | Trend | Notes |
|--------|---------|-------|-------|
| Authentication | [Strong / Adequate / Needs Improvement / Failing] | [Improving / Stable / Degrading] | [NOTES] |
| Authorization / RBAC | [Strong / Adequate / Needs Improvement / Failing] | [Improving / Stable / Degrading] | [NOTES] |
| Session Management | [Strong / Adequate / Needs Improvement / Failing] | [Improving / Stable / Degrading] | [NOTES] |
| Input Validation | [Strong / Adequate / Needs Improvement / Failing] | [Improving / Stable / Degrading] | [NOTES] |
| Headers & Transport | [Strong / Adequate / Needs Improvement / Failing] | [Improving / Stable / Degrading] | [NOTES] |
| Dependencies | [Strong / Adequate / Needs Improvement / Failing] | [Improving / Stable / Degrading] | [NOTES] |
| Logging & Monitoring | [Strong / Adequate / Needs Improvement / Failing] | [Improving / Stable / Degrading] | [NOTES] |
| Misconfiguration | [Strong / Adequate / Needs Improvement / Failing] | [Improving / Stable / Degrading] | [NOTES] |

### Step 7: Strategic Recommendations

Based on the full year review, produce strategic recommendations for the coming year:

- Tooling improvements (e.g., add SAST/DAST pipeline integration)
- Process improvements (e.g., threat modeling for all new features)
- Training needs (e.g., developer security training in most-affected domain)
- Architectural improvements (e.g., centralize logging, adopt secrets management)
- Compliance requirements coming due
- Areas requiring dedicated third-party penetration testing

### Step 8: Produce Annual Review and Reports

1. Complete `.claude/templates/annual-review-template.md`
2. Save to `audits/annual/YYYY-annual.md`
3. Draft technical report — `.claude/skills/report-writer/templates/technical-report-template.md`
4. Draft executive summary — `.claude/skills/report-writer/templates/executive-summary-template.md`
5. Draft remediation plan — `.claude/skills/report-writer/templates/remediation-plan-template.md`
6. Save all drafts to `reports/draft/`
7. After review and sign-off, promote final versions to `reports/final/`

---

## Outputs

| Output | Location | Template |
|--------|----------|---------|
| Annual review | `audits/annual/YYYY-annual.md` | `annual-review-template.md` |
| Technical report | `reports/final/YYYY-annual-technical-report.md` | `technical-report-template.md` |
| Executive summary | `reports/final/YYYY-annual-executive-summary.md` | `executive-summary-template.md` |
| Remediation plan | `reports/final/YYYY-annual-remediation-plan.md` | `remediation-plan-template.md` |
| Updated findings register | Current register | `findings-register-template.md` |

---

## Sign-Off Requirements

The annual review requires formal sign-off from:

- Security lead
- CISO or equivalent
- Development leadership
- Product leadership

Archive the signed annual review per compliance requirements.
