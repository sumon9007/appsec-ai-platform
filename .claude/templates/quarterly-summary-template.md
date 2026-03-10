# Quarterly Security Audit Summary

**Quarter:** [PLACEHOLDER — e.g., Q1 2026 (January–March 2026)]
**Summary Date:** [PLACEHOLDER — YYYY-MM-DD]
**Auditor:** [PLACEHOLDER]
**Application:** [PLACEHOLDER]
**Audit Period:** [PLACEHOLDER — e.g., 2026-01-01 to 2026-03-31]

---

## Quarter at a Glance

| Metric | This Quarter | Last Quarter | Change |
|--------|-------------|-------------|--------|
| New findings | [N] | [N] | [+N / -N] |
| Findings closed | [N] | [N] | [+N / -N] |
| Critical findings | [N] | [N] | [+N / -N] |
| High findings | [N] | [N] | [+N / -N] |
| Overdue findings (end of quarter) | [N] | [N] | [+N / -N] |
| SLA compliance — Critical | [N%] | [N%] | [+N% / -N%] |
| SLA compliance — High | [N%] | [N%] | [+N% / -N%] |

---

## Domain Coverage Report

| Domain | Coverage | Key Changes | New Findings | Posture |
|--------|---------|-------------|-------------|---------|
| Authentication & Access Control | [Full] | [PLACEHOLDER] | [N] | [Strong / Adequate / Needs Improvement] |
| Authorization / RBAC | [Full] | [PLACEHOLDER] | [N] | [Strong / Adequate / Needs Improvement] |
| Session Management | [Full] | [PLACEHOLDER] | [N] | [Strong / Adequate / Needs Improvement] |
| Input Validation | [Full] | [PLACEHOLDER] | [N] | [Strong / Adequate / Needs Improvement] |
| Security Headers & Transport | [Full] | [PLACEHOLDER] | [N] | [Strong / Adequate / Needs Improvement] |
| Dependency / Supply Chain | [Full] | [PLACEHOLDER] | [N] | [Strong / Adequate / Needs Improvement] |
| Logging & Monitoring | [Full] | [PLACEHOLDER] | [N] | [Strong / Adequate / Needs Improvement] |
| Security Misconfiguration | [Full] | [PLACEHOLDER] | [N] | [Strong / Adequate / Needs Improvement] |

---

## Findings Comparison — This Quarter vs. Last Quarter

### New Findings (Opened This Quarter)

| Finding ID | Title | Domain | Severity | Date Found | Status |
|------------|-------|--------|----------|------------|--------|
| [FIND-NNN] | [PLACEHOLDER] | [DOMAIN] | [SEVERITY] | [DATE] | [STATUS] |
| [FIND-NNN] | [PLACEHOLDER] | [DOMAIN] | [SEVERITY] | [DATE] | [STATUS] |

**Total new this quarter:** [N] | Critical: [N] | High: [N] | Medium: [N] | Low: [N] | Info: [N]

### Findings Closed This Quarter

| Finding ID | Title | Severity | Closed Date | Closed Within SLA? |
|------------|-------|----------|-------------|-------------------|
| [FIND-NNN] | [PLACEHOLDER] | [SEVERITY] | [DATE] | [Yes / No] |

**Total closed this quarter:** [N] | Within SLA: [N] | Outside SLA: [N]

### Aging Open Findings

Findings that remained open throughout the quarter:

| Finding ID | Title | Severity | Date Found | Age (Days) | SLA Status |
|------------|-------|----------|------------|------------|------------|
| [FIND-NNN] | [PLACEHOLDER] | [SEVERITY] | [DATE] | [N] | [Overdue / Within SLA] |

---

## Quarterly Findings Register Snapshot

| Severity | Open | In Progress | Risk Accepted | Closed This Quarter | Total Closed |
|----------|------|-------------|---------------|---------------------|--------------|
| Critical | [N] | [N] | [N] | [N] | [N] |
| High | [N] | [N] | [N] | [N] | [N] |
| Medium | [N] | [N] | [N] | [N] | [N] |
| Low | [N] | [N] | [N] | [N] | [N] |
| Info | [N] | [N] | [N] | [N] | [N] |

---

## Acceptance Criteria Re-Evaluation

Reference: `.claude/docs/acceptance-criteria.md`

| Domain | Pass Threshold Met? | Notes |
|--------|-------------------|-------|
| Authentication | [Yes / No] | [NOTES] |
| Authorization / RBAC | [Yes / No] | [NOTES] |
| Session Management | [Yes / No] | [NOTES] |
| Input Validation | [Yes / No] | [NOTES] |
| Headers & Transport | [Yes / No] | [NOTES] |
| Dependencies | [Yes / No] | [NOTES] |
| Logging & Monitoring | [Yes / No] | [NOTES] |
| Misconfiguration | [Yes / No] | [NOTES] |

**Are acceptance criteria still appropriate for current risk level?** [Yes / No — recommend update]
**Proposed changes to acceptance criteria:** [PLACEHOLDER or "None"]

---

## Threat Model Review

**Has the attack surface changed significantly this quarter?** [Yes / No]

Changes observed:
- [PLACEHOLDER — e.g., "New file export feature introduced a new data exfiltration risk vector"]
- [PLACEHOLDER — e.g., "New third-party payment integration added to scope"]
- [PLACEHOLDER or "No significant changes"]

---

## Trend Analysis

[PLACEHOLDER — Narrative trend analysis:]

- **Authentication:** [PLACEHOLDER — e.g., "Authentication controls remain strong. No new findings. Prior High finding (FIND-001) was remediated."]
- **Dependencies:** [PLACEHOLDER — e.g., "Dependency risk is elevated — 3 new Medium CVEs identified. Remediation velocity is adequate."]
- **Overall posture:** [PLACEHOLDER — e.g., "Security posture has improved from last quarter. All Critical findings resolved within SLA."]

---

## Strategic Notes

[PLACEHOLDER — Broader observations and recommendations not tied to specific findings:]

- [PLACEHOLDER — e.g., "Consider implementing a dependency update automation tool (Dependabot, Renovate) to reduce lag between CVE disclosure and remediation"]
- [PLACEHOLDER — e.g., "Logging coverage gaps suggest structured logging should be a priority in the next quarter"]
- [PLACEHOLDER — e.g., "Recommend developer security training on secure session management — 3 of 5 new findings in this domain"]

---

## Next Quarter Planned Focus

| Priority | Area | Rationale |
|----------|------|-----------|
| 1 | [PLACEHOLDER] | [PLACEHOLDER] |
| 2 | [PLACEHOLDER] | [PLACEHOLDER] |
| 3 | [PLACEHOLDER] | [PLACEHOLDER] |

---

*Template: quarterly-summary-template.md*
*Saved to: `audits/quarterly/YYYY-MM-DD-quarterly.md`*
