# Cadence Domain Matrix

Reference table for the `audit-cadence-orchestrator` skill. Defines which domain skills apply at each audit cadence and the expected depth of review.

---

## Coverage Matrix

| Domain Skill | Weekly | Monthly | Quarterly | Annual |
|---|---|---|---|---|
| `headers-tls-audit` | Regression check only | Full review | Full review | Full review |
| `auth-access-audit` | Change review only | Full review | Full review | Full review |
| `session-jwt-audit` | — | Spot-check | Full review | Full review |
| `rbac-audit` | — | Spot-check | Full review | Full review |
| `input-validation-audit` | — | Spot-check | Full review | Full review |
| `security-misconfig-audit` | — | — | Full review | Full review |
| `dependency-audit` | New CVEs only (last 7 days) | Full CVE scan | Full + abandonment risk | Full + supply chain + license |
| `logging-monitoring-audit` | Anomaly check only | Coverage check | Full review | Full review |

---

## Depth Definitions

| Depth Label | Meaning |
|-------------|---------|
| **Regression check** | Compare current state to prior week's output. Flag changes only. |
| **Change review** | Identify any changes to the domain since last cycle. Assess security impact of changes only. |
| **Anomaly check** | Review alerts and logs for anomalous patterns. No structural review of logging architecture. |
| **New CVEs only** | Check advisory feeds for vulnerabilities disclosed in the past 7 days that affect the known stack. |
| **Spot-check** | Cover the 3–5 highest-risk controls in the domain. Not a full methodology pass. |
| **Coverage check** | Verify that logging infrastructure covers key security events. No deep architecture review. |
| **Full CVE scan** | Run a full dependency scan against NVD, OSV, and GitHub Security Advisories. |
| **Full review** | Complete methodology pass using the domain skill's full checklist and templates. |
| **Full + abandonment risk** | Full review plus assessment of unmaintained, abandoned, or deprecated packages. |
| **Full + supply chain** | Full + abandonment plus package signature verification, typosquatting, and supply chain indicators. |
| **Full + license** | Full + supply chain plus license compatibility review for open source dependencies. |

---

## Output Artifacts by Cadence

| Cadence | Summary Template | Report Template | Location |
|---------|-----------------|----------------|---------|
| Weekly | `weekly-summary-template.md` | — | `audits/weekly/YYYY-MM-DD-weekly.md` |
| Monthly | `monthly-summary-template.md` | — | `audits/monthly/YYYY-MM-DD-monthly.md` |
| Quarterly | `quarterly-summary-template.md` | `report-writer` skill | `audits/quarterly/` + `reports/draft/` |
| Annual | `annual-review-template.md` | `report-writer` skill (exec + technical) | `audits/annual/` + `reports/final/` |

---

## SLA and Escalation by Cadence

| Cadence | SLA Checks | Escalation Threshold |
|---------|-----------|---------------------|
| Weekly | Flag any findings past SLA | New Critical CVE, auth regression, cert < 7 days → immediate escalation |
| Monthly | Full SLA compliance summary | Unresolved High after 7 days → escalate to development manager |
| Quarterly | SLA compliance rate report | Any overdue Critical or High with no accepted risk → present to leadership |
| Annual | Full year SLA compliance analysis | Strategic presentation; all open findings must have a documented plan |
