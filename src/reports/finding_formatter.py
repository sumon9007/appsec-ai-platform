"""
finding_formatter.py — Pure formatting functions for findings and the register.

No file I/O here — only string construction.
Format matches .claude/templates/findings-register-template.md exactly.
"""

from datetime import date
from typing import List


def format_finding_block(
    find_id: str,
    title: str,
    domain: str,
    severity: str,
    confidence: str,
    target: str,
    evidence_labels: List[str],
    observation: str,
    risk: str,
    recommendation: str,
    acceptance_criteria: str,
    status: str,
    review_type: str,
    opened: str,
    closed: str = "open",
) -> str:
    """Return a normalized finding Markdown block."""
    evidence_lines = "\n".join(f"- {label}" for label in evidence_labels)

    return f"""
---

### {find_id}

**Title:** {title}

**Domain:** {domain}

**Severity:** {severity}

**Confidence:** {confidence}

**Target:** {target}

**Evidence:**
{evidence_lines}

**Observation:** {observation}

**Risk:** {risk}

**Recommendation:** {recommendation}

**Acceptance Criteria Mapping:** {acceptance_criteria}

**Status:** {status}

**Review Type:** {review_type}

**Opened:** {opened}

**Closed:** {closed}

**Closure Evidence:** (none — finding is open)

"""


def format_register_header() -> str:
    """Return the skeleton header for a new findings register file."""
    today = date.today().isoformat()
    return f"""# Findings Register

This register is the single source of truth for all security findings in this engagement.

Every confirmed finding, suspected issue, and review gap must be recorded here.

Update this register at the end of every audit session and before generating any report.

*Created: {today} by appsec-audit-tool*

---

## Findings Summary

| Finding ID | Title | Domain | Severity | Confidence | Status |
|------------|-------|--------|----------|------------|--------|

---

"""


def severity_to_sla(severity: str) -> str:
    """Map a severity label to its remediation SLA string per remediation-rules.md."""
    mapping = {
        "Critical": "24 hours",
        "High": "7 calendar days",
        "Medium": "30 calendar days",
        "Low": "90 calendar days",
        "Info": "Next scheduled audit cycle",
    }
    return mapping.get(severity, "Unknown")
