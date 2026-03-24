# Skill: Audit Cadence Orchestrator

## Purpose

Select and orchestrate the correct audit workflow for a given cadence (weekly, monthly, quarterly, or annual). Determines which domain skills to invoke, at what depth, and which output artifacts to produce — based on the cadence type and current engagement state.

Use this skill when:
- Starting any recurring audit cycle
- Deciding which domain skills apply at a given audit frequency
- Determining the appropriate depth and output for a cadence review
- Building a consistent, repeatable audit schedule

Do NOT use this skill for release gate reviews — use `release-gate-review` instead.
Do NOT use this skill for ad hoc domain reviews — invoke the domain skill directly.

---

## Inputs Required

| Input | Source | Required? |
|-------|--------|-----------|
| Cadence type | User or scheduler | Required |
| Audit context | `.claude/context/audit-context.md` | Required |
| Scope | `.claude/context/scope.md` | Required |
| Findings register | `audits/[engagement-id]/findings-register.md` | Required |
| Prior cadence output | `audits/[weekly|monthly|quarterly|annual]/` | Strongly recommended |
| Cadence specification | `.claude/docs/audit-frequencies.md` | Required |

---

## Cadence Domain Matrix

See `references/cadence-domain-matrix.md` for the full matrix. Summary:

| Domain Skill | Weekly | Monthly | Quarterly | Annual |
|---|---|---|---|---|
| `headers-tls-audit` | Regression check | Full | Full | Full |
| `auth-access-audit` | Change review | Full | Full | Full |
| `session-jwt-audit` | — | Spot-check | Full | Full |
| `rbac-audit` | — | Spot-check | Full | Full |
| `input-validation-audit` | — | Spot-check | Full | Full |
| `security-misconfig-audit` | — | — | Full | Full |
| `dependency-audit` | New CVEs only | Full scan | Full + abandonment | Full + supply chain |
| `logging-monitoring-audit` | Anomaly check | Coverage check | Full | Full |

---

## Method

### Phase 1: Pre-Cadence Checks

1. Run `engagement-bootstrap` skill (or verify it has been run) — confirm authorization and scope are valid
2. Read `.claude/docs/audit-frequencies.md` — load the full specification for the selected cadence
3. Read the findings register — note all open findings and SLA status (per `.claude/rules/remediation-rules.md`)
4. Load the prior cadence output from `audits/[cadence]/` for trend comparison
   - If no prior output exists: record `BASELINE RUN — no prior period for comparison`

### Phase 2: Cadence-Specific Orchestration

#### Weekly Cadence

**Command reference:** `.claude/commands/audit-weekly.md`
**Duration target:** 1–2 hours

Skills to load and depth:
- `headers-tls-audit` — regression check: have any headers regressed since last week? Is certificate expiry < 30 days?
- `auth-access-audit` — change review: any updates to login, password reset, or MFA flows?
- `dependency-audit` — CVE sweep only: any new CVEs in the past 7 days affecting the known stack?
- `logging-monitoring-audit` — anomaly check: any alerts or anomalous patterns in the past 7 days?

Expected depth: Shallow sweep. Flag changes; do not perform deep analysis unless a change triggers a concern.

Output template: `.claude/templates/weekly-summary-template.md`
Output location: `audits/weekly/YYYY-MM-DD-weekly.md`

Escalate immediately if:
- New Critical CVE affecting a direct dependency
- Authentication regression observed
- Certificate expiry within 7 days
- Log pattern suggesting active attack or breach

#### Monthly Cadence

**Command reference:** `.claude/commands/audit-monthly.md`
**Duration target:** 4–8 hours

Skills to load and depth:
- All weekly skills at full depth
- `session-jwt-audit` — spot-check: cookie attributes, JWT algorithm, session timeout
- `rbac-audit` — spot-check: role permission drift, any new endpoints without authorization
- `input-validation-audit` — spot-check: key input endpoints, recent feature additions

Also review: all new features deployed in the past month; open findings for remediation progress.

Output template: `.claude/templates/monthly-summary-template.md`
Output location: `audits/monthly/YYYY-MM-DD-monthly.md`

#### Quarterly Cadence

**Command reference:** `.claude/commands/audit-quarterly.md`
**Duration target:** 1–3 days

Skills to load: all 9 domain skills at full depth (see matrix above).

Additional activities:
- Threat model review: has the attack surface changed significantly since last quarter?
- Acceptance criteria re-evaluation: read `.claude/docs/acceptance-criteria.md` — do standards still reflect risk tolerance?
- Remediation velocity analysis: are findings being closed within SLA?
- Comparison against prior quarterly report: changes in finding count by severity

Load `report-writer` skill to produce technical report and remediation plan.

Output templates:
- `.claude/templates/quarterly-summary-template.md`
- Technical report via `report-writer` skill

Output locations:
- `audits/quarterly/YYYY-MM-DD-quarterly.md`
- `reports/draft/YYYY-MM-DD-quarterly-report.md`

#### Annual Cadence

**Command reference:** `.claude/commands/audit-annual.md`
**Duration target:** 3–5 days

Skills to load: all quarterly activities plus deeper pass on each domain.

Additional activities:
- Year-over-year trend analysis: compare all 4 quarterly reports
- Full dependency supply chain review (not just CVEs — also abandonment, license, signature)
- Strategic recommendations: tooling, training, architecture changes for the coming year
- Review of all findings closed during the year — were closures valid and durable?
- Evaluation of security process effectiveness (SLA compliance rate, regression count)

Load `report-writer` skill for full executive summary and technical report.

Output locations:
- `audits/annual/YYYY-annual.md`
- `reports/final/YYYY-annual-technical-report.md`
- `reports/final/YYYY-annual-executive-summary.md`

### Phase 3: Findings Register Updates

After any cadence audit:
1. Add new findings to the register (via `evidence-and-findings-ops` skill)
2. Update status of findings that changed during this cadence
3. Flag all findings past their SLA deadline
4. For quarterly and annual: produce a remediation plan via `report-writer`

### Phase 4: Cadence Summary

Produce the appropriate summary document including:
- Risk trend vs. prior period: **Improving / Stable / Degrading**
- New findings this cycle (count by severity: Critical, High, Medium, Low, Info)
- Findings closed this cycle (count)
- SLA compliance rate (findings closed within SLA / total findings due)
- Overall posture statement (one sentence, per `.claude/rules/reporting-rules.md` Rule 10)

---

## Outputs

| Output | Template | Location |
|--------|---------|---------|
| Weekly summary | `weekly-summary-template.md` | `audits/weekly/YYYY-MM-DD-weekly.md` |
| Monthly summary | `monthly-summary-template.md` | `audits/monthly/YYYY-MM-DD-monthly.md` |
| Quarterly summary | `quarterly-summary-template.md` | `audits/quarterly/YYYY-MM-DD-quarterly.md` |
| Quarterly draft report | via `report-writer` | `reports/draft/` |
| Annual review | `annual-review-template.md` | `audits/annual/YYYY-annual.md` |
| Annual final reports | via `report-writer` | `reports/final/` |

---

## Rules Applied

- `.claude/rules/safety-authorization-rules.md` — Rule 1 (authorization gate on every cadence)
- `.claude/rules/audit-scope-rules.md` — Rule 1 (scope confirmation before starting)
- `.claude/rules/remediation-rules.md` — Rule 8 (SLA reporting per cadence)
- `.claude/rules/reporting-rules.md` — Rule 10 (posture statement required)

---

## Related Skills and Commands

- `engagement-bootstrap` — run before the first cadence to validate context
- `evidence-and-findings-ops` — use during each cadence to record findings and evidence
- `report-writer` — use for quarterly and annual report generation
- `release-gate-review` — separate skill for pre-release reviews (not cadence-driven)
- All 9 domain skills — selectively invoked per the cadence domain matrix
