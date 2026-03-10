# Audit Frequencies

Defines the purpose, scope, outputs, and review responsibilities for each audit cadence supported by this workspace.

---

## Cadence Overview

| Cadence | Command | Typical Duration | Primary Purpose |
|---------|---------|-----------------|----------------|
| Weekly | `/audit-weekly` | 1–2 hours | Continuous monitoring and quick anomaly detection |
| Monthly | `/audit-monthly` | 4–8 hours | Broader review of key domains and emerging risks |
| Quarterly | `/audit-quarterly` | 1–3 days | Comprehensive audit of all domains |
| Release Gate | `/audit-release` | 2–4 hours | Pre-deployment security gate |
| Annual | `/audit-annual` | 3–5 days | Full posture review and strategic planning |

---

## Weekly Audit

**Purpose:** Provide continuous, lightweight security monitoring between deeper audits. Catch emerging issues early.

**Scope:**
- HTTP security headers — check for regressions or new missing headers
- Authentication changes — any updates to login flows, MFA, or password policy
- New CVEs — check dependency advisories for newly disclosed vulnerabilities affecting the stack
- Recent log anomalies — review any alerts or anomaly reports from the past 7 days
- Certificate expiry — check certificate validity and days-to-expiry

**Domains Covered:** Security Headers, Dependencies (CVE only), Logging (anomaly check), Authentication (change review)

**Outputs Expected:**
- Completed `.claude/templates/weekly-summary-template.md` saved to `audits/weekly/YYYY-MM-DD-weekly.md`
- Any new findings added to the findings register
- Any open findings with status changes updated in the register

**Who Reviews:** Security lead or designated reviewer. Escalate Critical/High findings immediately.

**Inputs Required:** Prior week's weekly summary (for trend comparison), dependency manifest, current headers capture.

---

## Monthly Audit

**Purpose:** Broader security review covering all key domains at a level of depth that weekly checks cannot achieve.

**Scope:**
- All weekly checks
- RBAC spot-check — verify role permissions have not drifted
- Input validation spot-check — review key endpoints for validation controls
- TLS certificate and cipher suite review
- Dependency scan — full review of all dependencies against CVE databases
- Review of any new features deployed in the past month
- Review of open findings from prior audits — verify remediation progress

**Domains Covered:** All weekly domains + RBAC, Input Validation, TLS, Dependency full scan

**Outputs Expected:**
- Completed `.claude/templates/monthly-summary-template.md` saved to `audits/monthly/YYYY-MM-DD-monthly.md`
- Updated findings register
- Any new findings documented with full evidence

**Who Reviews:** Security lead and development manager. Escalate unresolved High/Critical findings to project owner.

**Inputs Required:** Weekly summaries from the past month, current dependency manifests, findings register.

---

## Quarterly Audit

**Purpose:** Deep, comprehensive audit of all security domains. Re-evaluate acceptance criteria and overall security posture.

**Scope:**
- Full audit of all domains in `.claude/docs/audit-domains.md`
- Threat model review — has the attack surface changed significantly?
- Re-evaluation of acceptance criteria — do current standards still reflect risk tolerance?
- Review of all open findings — prioritize and confirm status
- Comparison against previous quarter's findings
- Assessment of remediation velocity (how quickly are findings being closed)
- Review of infrastructure and configuration changes in the quarter

**Domains Covered:** All 10 domains

**Outputs Expected:**
- Completed `.claude/templates/quarterly-summary-template.md` saved to `audits/quarterly/YYYY-MM-DD-quarterly.md`
- Updated findings register with trend notes
- Technical report (`reports/draft/YYYY-MM-DD-quarterly-report.md`)
- Remediation plan for any outstanding findings

**Who Reviews:** Security lead, development manager, and product owner. Present to leadership if Critical findings are present.

**Inputs Required:** All monthly summaries from the quarter, full findings register, prior quarterly report.

---

## Release Gate Audit

**Purpose:** Security checkpoint before a production release. Ensure new features do not introduce unacceptable risk and prior findings are remediated.

**Scope:**
- Review new features and changes in the release for security impact
- Check for new attack surface introduced by the release (new endpoints, new data flows, new integrations)
- Confirm all Critical and High findings from prior audits are remediated (or formally accepted with justification)
- Quick scan of new dependencies introduced in the release
- Re-verify security headers and TLS if infrastructure changes were made
- Validate that known-good security controls were not inadvertently removed or degraded

**Domains Covered:** Context-dependent on what changed in the release. At minimum: Authentication, Authorization, Input Validation, Dependencies, Headers.

**Outputs Expected:**
- Completed `.claude/templates/release-gate-template.md` saved to `audits/release/YYYY-MM-DD-v[version]-gate.md`
- Gate decision: **Pass**, **Fail**, or **Conditional Pass** (with conditions listed)
- Any new findings documented before the gate decision is made

**Who Reviews:** Security lead and development manager. Gate decision is a mandatory sign-off before deployment.

**Inputs Required:** Release changelog / diff summary, prior findings register, new dependency additions.

---

## Annual Audit

**Purpose:** Comprehensive annual security review covering all domains in depth, historical trend analysis, and strategic security planning for the next year.

**Scope:**
- Full audit of all domains at maximum depth
- Year-over-year comparison: total findings by severity, closed vs. open trends
- Domain-by-domain posture assessment
- Remediation velocity analysis — are issues being fixed within SLA?
- Review of all findings opened and closed in the year
- Evaluation of security tooling and process effectiveness
- Strategic recommendations for the coming year (tooling, training, architecture improvements)
- Third-party security assessment of critical integrations (if applicable)

**Domains Covered:** All 10 domains

**Outputs Expected:**
- Completed `.claude/templates/annual-review-template.md` saved to `audits/annual/YYYY-annual.md`
- Full executive summary report
- Full technical report
- Updated findings register
- Strategic recommendations document
- All final reports saved to `reports/final/`

**Who Reviews:** Security lead, CISO or equivalent, development leadership, product leadership. Formal sign-off required. Archive for compliance purposes.

**Inputs Required:** All quarterly summaries from the year, full historical findings register, prior annual review.
