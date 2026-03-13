"""
findings_writer.py — Appends normalized finding blocks to the findings register.

The register is append-only from Python. Severity changes, status updates,
and closures are human-review operations handled via Claude commands.

Finding format matches .claude/templates/findings-register-template.md exactly.
"""

import logging
import re
from datetime import date
from pathlib import Path
from typing import Optional

from src.config.settings import (
    DEFAULT_REGISTER_PATH,
    VALID_CONFIDENCES,
    VALID_SEVERITIES,
    VALID_STATUSES,
)
from src.reports.finding_formatter import format_finding_block, format_register_header

logger = logging.getLogger(__name__)


def _ensure_register_exists(register_path: Path) -> None:
    """Create the findings register file from the template skeleton if absent."""
    register_path.parent.mkdir(parents=True, exist_ok=True)
    if not register_path.exists():
        register_path.write_text(format_register_header(), encoding="utf-8")
        logger.info("Created new findings register at %s", register_path)


def next_find_id(register_path: Path) -> str:
    """
    Determine the next FIND-NNN ID by scanning the register file.

    Reads existing ### FIND-NNN headings and returns the next sequential ID.
    """
    if not register_path.exists():
        return "FIND-001"

    content = register_path.read_text(encoding="utf-8")
    existing = re.findall(r"### FIND-(\d+)", content)
    if not existing:
        return "FIND-001"

    max_num = max(int(n) for n in existing)
    return f"FIND-{max_num + 1:03d}"


def _append_summary_row(register_path: Path, finding: dict, find_id: str) -> None:
    """Insert a one-line summary row into the Findings Summary table."""
    content = register_path.read_text(encoding="utf-8")
    summary_row = (
        f"| {find_id} | {finding['title']} | {finding['domain']} | "
        f"{finding['severity']} | {finding['confidence']} | {finding['status']} |\n"
    )

    marker = "|------------|-------|--------|----------|------------|--------|\n"
    if marker not in content:
        logger.warning(
            "Findings summary table marker not found in %s; summary row for %s not inserted.",
            register_path,
            find_id,
        )
        return

    updated = content.replace(marker, marker + summary_row, 1)
    register_path.write_text(updated, encoding="utf-8")


def append_finding(
    finding: dict,
    register_path: Optional[Path] = None,
) -> str:
    """
    Validate and append a normalized finding block to the findings register.

    Required finding dict keys:
        title, domain, severity, confidence, target, evidence_labels,
        observation, risk, recommendation, acceptance_criteria,
        status, review_type

    Optional:
        opened (defaults to today), closed (defaults to "open")

    Returns:
        The assigned Finding ID string (e.g., "FIND-003").

    Raises:
        ValueError — if required fields are missing or values are invalid.
    """
    if register_path is None:
        register_path = DEFAULT_REGISTER_PATH

    # ── Validate required fields ──────────────────────────────────────────────
    required = [
        "title", "domain", "severity", "confidence", "target",
        "evidence_labels", "observation", "risk", "recommendation",
        "acceptance_criteria", "status", "review_type",
    ]
    missing = [k for k in required if k not in finding or not finding[k]]
    if missing:
        raise ValueError(f"Finding is missing required fields: {missing}")

    severity = finding["severity"]
    if severity not in VALID_SEVERITIES:
        raise ValueError(
            f"Invalid severity '{severity}'. Must be one of: {sorted(VALID_SEVERITIES)}"
        )

    status = finding["status"]
    if status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid status '{status}'. Must be one of: {sorted(VALID_STATUSES)}"
        )

    confidence = finding["confidence"]
    if confidence not in VALID_CONFIDENCES:
        raise ValueError(
            f"Invalid confidence '{confidence}'. Must be one of: {sorted(VALID_CONFIDENCES)}"
        )

    # ── Assign ID and defaults ────────────────────────────────────────────────
    _ensure_register_exists(register_path)
    find_id = next_find_id(register_path)

    opened = finding.get("opened") or date.today().isoformat()
    closed = finding.get("closed") or "open"

    # ── Format and append ─────────────────────────────────────────────────────
    block = format_finding_block(
        find_id=find_id,
        title=finding["title"],
        domain=finding["domain"],
        severity=severity,
        confidence=confidence,
        target=finding["target"],
        evidence_labels=finding["evidence_labels"],  # list of strings
        observation=finding["observation"],
        risk=finding["risk"],
        recommendation=finding["recommendation"],
        acceptance_criteria=finding["acceptance_criteria"],
        status=status,
        review_type=finding["review_type"],
        opened=opened,
        closed=closed,
    )

    with register_path.open("a", encoding="utf-8") as f:
        f.write(block)

    _append_summary_row(register_path, finding, find_id)

    logger.info(
        "Finding appended: %s — %s [%s] to %s",
        find_id,
        finding["title"],
        severity,
        register_path,
    )
    return find_id
