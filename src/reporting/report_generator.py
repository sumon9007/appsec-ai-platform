"""
report_generator.py — Generates draft technical and executive reports from the findings register.

Output format follows reporting-rules.md and reporting-standard.md.
All generated reports are placed in reports/draft/ with correct filename convention.
"""

from __future__ import annotations

import logging
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from src.config.settings import PROJECT_ROOT
from src.reports.finding_formatter import severity_to_sla

logger = logging.getLogger(__name__)

REPORTS_DRAFT_DIR = PROJECT_ROOT / "reports" / "draft"
REPORTS_FINAL_DIR = PROJECT_ROOT / "reports" / "final"

_FINDING_PATTERN = re.compile(
    r"### (FIND-\d+)\n(.*?)(?=### FIND-|\Z)", re.DOTALL
)
_FIELD_PATTERN = re.compile(r"\*\*([^*]+):\*\*\s*(.+?)(?=\n\*\*|\Z)", re.DOTALL)


def _parse_register(register_path: Path) -> List[Dict[str, str]]:
    """Parse all findings from a findings register Markdown file."""
    if not register_path.exists():
        logger.error("Findings register not found: %s", register_path)
        return []

    content = register_path.read_text(encoding="utf-8")
    findings = []

    for match in _FINDING_PATTERN.finditer(content):
        find_id = match.group(1)
        body = match.group(2)
        finding = {"find_id": find_id}
        for field_match in _FIELD_PATTERN.finditer(body):
            key = field_match.group(1).strip().lower().replace(" ", "_")
            value = field_match.group(2).strip()
            finding[key] = value
        findings.append(finding)

    return findings


def _severity_order(severity: str) -> int:
    order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4}
    return order.get(severity, 99)


def generate_technical_report(
    register_path: Path,
    target_name: str = "",
    auditor: str = "",
    report_type: str = "technical",
    version: str = "DRAFT v0.1",
) -> Path:
    """
    Generate a draft technical report from the findings register.

    Returns the path to the generated report file.
    Follows report filename convention: YYYY-MM-DD-[type]-report.md
    """
    REPORTS_DRAFT_DIR.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    filename = f"{today}-{report_type}-report.md"
    report_path = REPORTS_DRAFT_DIR / filename

    findings = _parse_register(register_path)
    if not findings:
        logger.warning("No findings parsed from %s — report will have empty findings section.", register_path)

    # Sort by severity
    findings.sort(key=lambda f: _severity_order(f.get("severity", "Info")))

    # Count by severity
    severity_counts: Counter = Counter(f.get("severity", "Info") for f in findings)
    open_findings = [f for f in findings if f.get("status", "confirmed") not in ("closed", "mitigated")]
    critical_high = [f for f in open_findings if f.get("severity") in ("Critical", "High")]

    # Overall posture
    posture = _derive_posture(severity_counts, open_findings)

    # Build findings section
    findings_blocks = []
    for f in findings:
        sla = severity_to_sla(f.get("severity", "Info"))
        block = f"""### {f['find_id']} — {f.get('title', 'Untitled')}

| Field | Value |
|-------|-------|
| **Domain** | {f.get('domain', '')} |
| **Severity** | {f.get('severity', '')} |
| **Confidence** | {f.get('confidence', '')} |
| **Status** | {f.get('status', '')} |
| **SLA** | {sla} |
| **Target** | {f.get('target', '')} |

**Evidence:** {f.get('evidence', '(see findings register)')}

**Observation:** {f.get('observation', '')}

**Risk:** {f.get('risk', '')}

**Recommendation:** {f.get('recommendation', '')}

**Acceptance Criteria Mapping:** {f.get('acceptance_criteria_mapping', '')}

---
"""
        findings_blocks.append(block)

    findings_section = "\n".join(findings_blocks) if findings_blocks else "*No findings recorded in register.*"

    # Summary table
    summary_rows = "\n".join(
        f"| {f['find_id']} | {f.get('title', '')[:60]} | {f.get('severity', '')} | {f.get('status', '')} |"
        for f in findings
    ) or "| — | No findings | — | — |"

    report_content = f"""# Security Assessment Technical Report
## {target_name or 'Target Application'}

**Version:** {version}
**Date:** {today}
**Auditor:** {auditor or 'See engagement record'}
**Report Type:** Technical
**Findings Register:** {register_path}

---

## Overall Security Posture

{posture}

---

## Findings Summary

| Finding ID | Title | Severity | Status |
|------------|-------|----------|--------|
{summary_rows}

**Total Findings:** {len(findings)}
**Critical:** {severity_counts.get('Critical', 0)} | **High:** {severity_counts.get('High', 0)} | **Medium:** {severity_counts.get('Medium', 0)} | **Low:** {severity_counts.get('Low', 0)} | **Info:** {severity_counts.get('Info', 0)}

---

## Immediate Actions Required

{_immediate_actions(critical_high) if critical_high else '*No Critical or High findings requiring immediate action.*'}

---

## Detailed Findings

{findings_section}

---

## Review Gaps

The following areas could not be fully assessed in this review and require follow-up:

{_review_gaps(findings)}

---

## Scope

*See `.claude/context/scope.md` for the full engagement scope.*

---

## Evidence Index

All evidence referenced in this report is stored in `evidence/` under the EVID-YYYY-MM-DD-NNN labeling convention.

---

*Generated by appsec-audit-tool | {version}*
"""

    report_path.write_text(report_content, encoding="utf-8")
    logger.info("Technical report written: %s", report_path)
    return report_path


def generate_executive_summary(
    register_path: Path,
    target_name: str = "",
    auditor: str = "",
    version: str = "DRAFT v0.1",
) -> Path:
    """
    Generate a non-technical executive summary report.

    Follows reporting-rules.md Rule 4 — no technical details, CVEs, or raw headers.
    """
    REPORTS_DRAFT_DIR.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    filename = f"{today}-executive-summary.md"
    report_path = REPORTS_DRAFT_DIR / filename

    findings = _parse_register(register_path)
    severity_counts: Counter = Counter(f.get("severity", "Info") for f in findings)
    open_findings = [f for f in findings if f.get("status", "confirmed") not in ("closed", "mitigated")]
    posture = _derive_posture(severity_counts, open_findings)

    exec_finding_rows = "\n".join(
        f"| {f['find_id']} | {f.get('title', '')[:60]} | {f.get('severity', '')} |"
        for f in sorted(findings, key=lambda x: _severity_order(x.get("severity", "Info")))[:10]
    ) or "| — | No findings | — |"

    report_content = f"""# Security Assessment Executive Summary
## {target_name or 'Target Application'}

**Version:** {version}
**Date:** {today}
**Report Type:** Executive Summary

---

## Overall Security Posture

{posture}

---

## Key Findings Summary

| Finding | Description | Priority |
|---------|-------------|----------|
{exec_finding_rows}

**Total Issues Identified:** {len(findings)}
**Requiring Immediate Action:** {severity_counts.get('Critical', 0) + severity_counts.get('High', 0)}
**Requiring Near-Term Action:** {severity_counts.get('Medium', 0)}
**Lower Priority:** {severity_counts.get('Low', 0) + severity_counts.get('Info', 0)}

---

## Risk Summary

{_executive_risk_summary(findings)}

---

## Recommended Actions

{_executive_recommendations(findings)}

---

## Next Steps

1. Review the detailed technical report for full finding descriptions and remediation guidance.
2. Assign ownership for each Critical and High finding with a remediation timeline.
3. Schedule a re-test session after remediation to confirm finding closure.

---

*This summary is prepared for senior management and does not contain technical implementation details.
For technical details, refer to the accompanying Technical Report.*

*Generated by appsec-audit-tool | {version}*
"""

    report_path.write_text(report_content, encoding="utf-8")
    logger.info("Executive summary written: %s", report_path)
    return report_path


def generate_remediation_plan(register_path: Path, target_name: str = "") -> Path:
    """Generate a prioritized remediation plan from the findings register."""
    REPORTS_DRAFT_DIR.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    filename = f"{today}-remediation-plan.md"
    report_path = REPORTS_DRAFT_DIR / filename

    findings = _parse_register(register_path)
    open_findings = [f for f in findings if f.get("status", "confirmed") not in ("closed", "mitigated", "accepted-risk")]
    open_findings.sort(key=lambda f: _severity_order(f.get("severity", "Info")))

    immediate = [f for f in open_findings if f.get("severity") == "Critical"]
    short_term = [f for f in open_findings if f.get("severity") == "High"]
    medium_term = [f for f in open_findings if f.get("severity") == "Medium"]
    long_term = [f for f in open_findings if f.get("severity") in ("Low", "Info")]

    def _section(title: str, items: List[Dict], sla: str) -> str:
        if not items:
            return f"### {title}\n\n*No findings in this category.*\n"
        rows = "\n".join(
            f"- **{f['find_id']}** — {f.get('title', 'Untitled')}: {f.get('recommendation', '')[:120]}"
            for f in items
        )
        return f"### {title}\n\n**SLA:** {sla}\n\n{rows}\n"

    content = f"""# Remediation Plan
## {target_name or 'Target Application'}

**Date:** {today}
**Open Findings:** {len(open_findings)}

---

## Priority 1 — Immediate (Critical findings)

{_section('Immediate Actions', immediate, '24 hours')}

---

## Priority 2 — Short Term (High findings)

{_section('Short-Term Fixes', short_term, '7 calendar days')}

---

## Priority 3 — Near Term (Medium findings)

{_section('Near-Term Improvements', medium_term, '30 calendar days')}

---

## Priority 4 — Improvement Cycle (Low / Info findings)

{_section('Next Audit Cycle', long_term, '90 calendar days')}

---

## Closure Requirements

Per `remediation-rules.md` Rule 5, findings may only be closed when:
1. Evidence of the fix is provided (PR/commit, config change capture, updated manifest)
2. The security auditor reviews and confirms the fix
3. A re-test evidence item (EVID-labeled) is recorded

---

*Generated by appsec-audit-tool*
"""

    report_path.write_text(content, encoding="utf-8")
    logger.info("Remediation plan written: %s", report_path)
    return report_path


def _derive_posture(severity_counts: Counter, open_findings: List[Dict]) -> str:
    if severity_counts.get("Critical", 0) > 0:
        return (
            "The application has critical security weaknesses that require immediate remediation "
            "before continued production operation can be recommended."
        )
    if severity_counts.get("High", 0) > 2:
        return (
            "The application has significant security control failures. "
            "Multiple High severity findings indicate structural weaknesses requiring prompt attention."
        )
    if severity_counts.get("High", 0) > 0:
        return (
            "The application has meaningful security weaknesses. "
            "High severity findings require remediation within the defined SLA."
        )
    if severity_counts.get("Medium", 0) > 0:
        return (
            "The application maintains an adequate security baseline with no Critical or High findings. "
            "Medium severity findings represent improvement opportunities that should be addressed "
            "within 30 days."
        )
    return (
        "The application demonstrates a strong security baseline. "
        "All identified findings are low priority or informational."
    )


def _immediate_actions(critical_high: List[Dict]) -> str:
    lines = []
    for f in critical_high:
        sla = severity_to_sla(f.get("severity", "High"))
        lines.append(f"- **{f['find_id']}** [{f.get('severity')}] {f.get('title', '')} — SLA: {sla}")
    return "\n".join(lines)


def _review_gaps(findings: List[Dict]) -> str:
    gaps = [f for f in findings if f.get("status") == "review-gap"]
    if not gaps:
        return "*No review gaps recorded.*"
    return "\n".join(
        f"- **{f['find_id']}** — {f.get('title', '')}: {f.get('observation', '')[:100]}"
        for f in gaps
    )


def _executive_risk_summary(findings: List[Dict]) -> str:
    domains = Counter(f.get("domain", "Unknown") for f in findings)
    if not domains:
        return "*No findings to summarize.*"
    lines = []
    for domain, count in domains.most_common():
        sev = max(
            (f for f in findings if f.get("domain") == domain),
            key=lambda x: _severity_order(x.get("severity", "Info")),
            default={},
        ).get("severity", "Info")
        lines.append(f"- **{domain}**: {count} finding(s), highest severity: {sev}")
    return "\n".join(lines)


def _executive_recommendations(findings: List[Dict]) -> str:
    critical = [f for f in findings if f.get("severity") == "Critical"]
    high = [f for f in findings if f.get("severity") == "High"]
    recs = []
    if critical:
        recs.append(f"1. **Immediately** address {len(critical)} critical security issue(s) — within 24 hours.")
    if high:
        recs.append(f"{'2' if critical else '1'}. Address {len(high)} high-priority issue(s) within 7 days.")
    recs.append(f"{'3' if (critical or high) else '1'}. Schedule a remediation verification session after fixes are deployed.")
    recs.append(f"{'4' if (critical or high) else '2'}. Review full technical report with engineering team for implementation guidance.")
    return "\n".join(recs)
