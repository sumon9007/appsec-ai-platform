# Monthly Security Audit Summary

**Month:** [PLACEHOLDER — e.g., March 2026]
**Summary Date:** [PLACEHOLDER — YYYY-MM-DD]
**Auditor:** [PLACEHOLDER]
**Application:** [PLACEHOLDER]

---

## Month at a Glance

| Metric | Value |
|--------|-------|
| Domains covered | [N of 8] |
| New findings | [N] |
| Findings closed | [N] |
| Overdue findings (at month end) | [N] |
| Certificate expiry (days remaining) | [N] |
| New CVEs affecting dependencies | [N] |

---

## Domains Covered This Month

| Domain | Coverage Level | Key Activities | Status |
|--------|---------------|---------------|--------|
| Authentication | [Full / Spot-check / Not covered] | [PLACEHOLDER] | [No issues / Issues found] |
| Authorization / RBAC | [Full / Spot-check / Not covered] | [PLACEHOLDER] | [No issues / Issues found] |
| Session Management | [Full / Spot-check / Not covered] | [PLACEHOLDER] | [No issues / Issues found] |
| Input Validation | [Full / Spot-check / Not covered] | [PLACEHOLDER] | [No issues / Issues found] |
| Security Headers & TLS | [Full / Spot-check / Not covered] | [PLACEHOLDER] | [No issues / Issues found] |
| Dependencies | [Full / Spot-check / Not covered] | [PLACEHOLDER] | [No issues / Issues found] |
| Logging & Monitoring | [Full / Spot-check / Not covered] | [PLACEHOLDER] | [No issues / Issues found] |
| Misconfiguration | [Full / Spot-check / Not covered] | [PLACEHOLDER] | [No issues / Issues found] |

---

## Findings Summary

### New Findings This Month

| Finding ID | Title | Domain | Severity | Date Found | Status |
|------------|-------|--------|----------|------------|--------|
| [FIND-NNN] | [PLACEHOLDER] | [DOMAIN] | [SEVERITY] | [DATE] | Open |
| [FIND-NNN] | [PLACEHOLDER] | [DOMAIN] | [SEVERITY] | [DATE] | In Progress |

**Total new this month:** [N] | Critical: [N] | High: [N] | Medium: [N] | Low: [N] | Info: [N]

### Findings Closed This Month

| Finding ID | Title | Severity | Closed Date | Fix Evidence |
|------------|-------|----------|-------------|-------------|
| [FIND-NNN] | [PLACEHOLDER] | [SEVERITY] | [DATE] | [EVID-YYYY-MM-DD-NNN] |

**Total closed this month:** [N]

### Findings Register Snapshot (End of Month)

| Severity | Open | In Progress | Risk Accepted | Closed (All Time) |
|----------|------|-------------|---------------|-------------------|
| Critical | [N] | [N] | [N] | [N] |
| High | [N] | [N] | [N] | [N] |
| Medium | [N] | [N] | [N] | [N] |
| Low | [N] | [N] | [N] | [N] |
| Info | [N] | [N] | [N] | [N] |

---

## Key Risk Changes This Month

[PLACEHOLDER — Describe the most significant security posture changes this month:]

1. [PLACEHOLDER — e.g., "FIND-003 (High — IDOR on /api/orders) was remediated and verified. This reduces the risk of unauthorized access to order data."]
2. [PLACEHOLDER — e.g., "Two new Medium CVEs were identified in the axios dependency. Update is scheduled for next sprint."]
3. [PLACEHOLDER — e.g., "TLS certificate renewed — expiry extended to 2026-09-01."]

---

## New Features Reviewed

| Feature | Release | Security Concerns Identified? | Finding IDs |
|---------|---------|-------------------------------|-------------|
| [PLACEHOLDER — e.g., File export feature] | [v2.3.0] | [Yes / No] | [FIND-NNN or —] |
| [PLACEHOLDER] | [PLACEHOLDER] | [Yes / No] | [FIND-NNN or —] |

---

## Dependency Status

| Metric | Value |
|--------|-------|
| New CVEs affecting dependencies | [N] |
| Critical CVEs | [N] |
| High CVEs | [N] |
| Packages updated this month | [N] |
| Abandoned packages identified | [N] |

---

## Items Escalated

[PLACEHOLDER — Note any items escalated to management or product owner this month:]

- [PLACEHOLDER — e.g., "FIND-007 (Critical) escalated to CTO on YYYY-MM-DD — remediation in progress"]
- [PLACEHOLDER or "No escalations this month"]

---

## Recommendations for Next Month

[PLACEHOLDER — What should be prioritized in the coming month?]

1. [PLACEHOLDER — e.g., "Verify remediation of FIND-005 and FIND-007"]
2. [PLACEHOLDER — e.g., "Update axios to remediate CVE-2024-XXXXX"]
3. [PLACEHOLDER — e.g., "Review new admin dashboard feature scheduled for v2.4.0"]
4. [PLACEHOLDER — e.g., "Renew TLS certificate — expires in [N] days"]

---

## Risk Trend (Month over Month)

| Metric | This Month | Last Month | Trend |
|--------|-----------|-----------|-------|
| Total open findings | [N] | [N] | [Up / Down / Stable] |
| Critical + High open | [N] | [N] | [Up / Down / Stable] |
| Overdue findings | [N] | [N] | [Up / Down / Stable] |
| Remediation rate | [N closed / N total] | [N closed / N total] | [Improving / Stable / Degrading] |
| **Overall trend** | — | — | **[Improving / Stable / Degrading]** |

---

*Template: monthly-summary-template.md*
*Saved to: `audits/monthly/YYYY-MM-DD-monthly.md`*
