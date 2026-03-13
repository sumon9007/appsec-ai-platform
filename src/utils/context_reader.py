"""
context_reader.py — Parses the .claude/context/ markdown files.

The authorization gate is the single most important function here.
No audit activity may proceed unless check_authorization() returns "CONFIRMED".
"""

import logging
import re
from pathlib import Path
from typing import List, Optional

from src.config.settings import CONTEXT_DIR

logger = logging.getLogger(__name__)

# Authorization status values
AUTH_CONFIRMED = "CONFIRMED"
AUTH_NOT_CONFIRMED = "NOT_CONFIRMED"
AUTH_MISSING = "MISSING"


def _read_file(path: Path) -> Optional[str]:
    """Read a context file. Returns None if the file is missing."""
    if not path.exists():
        logger.warning("Context file not found: %s", path)
        return None
    return path.read_text(encoding="utf-8")


def _extract_table_value(content: str, field_name: str) -> Optional[str]:
    """
    Extract the value column from a Markdown table row matching field_name.

    Matches rows like:  | Authorization Status | CONFIRMED |
    Case-insensitive on the field name, strips surrounding whitespace.
    """
    pattern = re.compile(
        r"^\|\s*" + re.escape(field_name) + r"\s*\|\s*(.+?)\s*\|",
        re.IGNORECASE | re.MULTILINE,
    )
    match = pattern.search(content)
    if match:
        return match.group(1).strip()
    return None


def check_authorization() -> str:
    """
    Read audit-context.md and return the authorization status.

    Returns:
        "CONFIRMED"      — authorization is confirmed, audit may proceed
        "NOT_CONFIRMED"  — file exists but authorization is not CONFIRMED
        "MISSING"        — file is absent or Authorization Status field not found
    """
    audit_context_path = CONTEXT_DIR / "audit-context.md"
    content = _read_file(audit_context_path)

    if content is None:
        logger.error(
            "audit-context.md not found at %s. "
            "Remediation: Create and populate this file before running any audit.",
            audit_context_path,
        )
        return AUTH_MISSING

    value = _extract_table_value(content, "Authorization Status")

    if value is None:
        logger.error(
            "Authorization Status field not found in audit-context.md. "
            "Remediation: Ensure the Authorization table row exists and "
            "is populated with CONFIRMED / PENDING / NOT CONFIRMED."
        )
        return AUTH_MISSING

    # Strip placeholder markers
    if "[PLACEHOLDER" in value.upper() or not value:
        return AUTH_NOT_CONFIRMED

    if value.upper() == "CONFIRMED":
        return AUTH_CONFIRMED

    return AUTH_NOT_CONFIRMED


def get_audit_id() -> Optional[str]:
    """Return the Audit ID from audit-context.md."""
    content = _read_file(CONTEXT_DIR / "audit-context.md")
    if content is None:
        return None
    return _extract_table_value(content, "Audit ID")


def get_auditor_name() -> Optional[str]:
    """Return the Auditor Name(s) from audit-context.md."""
    content = _read_file(CONTEXT_DIR / "audit-context.md")
    if content is None:
        return None
    return _extract_table_value(content, "Auditor Name(s)")


def get_target_urls() -> List[str]:
    """
    Parse in-scope target URLs from scope.md.

    Looks for lines under an "In-Scope" section that begin with
    a URL scheme (http:// or https://) or bullet items containing a URL.
    Returns an empty list if the file is missing or no URLs are found.
    """
    scope_path = CONTEXT_DIR / "scope.md"
    content = _read_file(scope_path)

    if content is None:
        logger.warning(
            "scope.md not found. "
            "Remediation: Populate .claude/context/scope.md with in-scope URLs before auditing."
        )
        return []

    urls: List[str] = []
    url_pattern = re.compile(r"https?://[^\s\|\]\"'<>]+")

    in_scope_section = False
    for line in content.splitlines():
        stripped = line.strip().lower()
        if "in-scope" in stripped or "in scope" in stripped:
            in_scope_section = True
        if in_scope_section and ("out-of-scope" in stripped or "out of scope" in stripped):
            break
        if in_scope_section:
            found = url_pattern.findall(line)
            urls.extend(found)

    # Deduplicate while preserving order
    seen = set()
    unique_urls = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)

    if not unique_urls:
        logger.warning(
            "No in-scope URLs found in scope.md. "
            "Remediation: Add target URLs under the In-Scope section of .claude/context/scope.md."
        )

    return unique_urls


def get_testing_mode() -> str:
    """Return the Scope of Authorization value (e.g., 'Passive review only')."""
    content = _read_file(CONTEXT_DIR / "audit-context.md")
    if content is None:
        return "Passive review only"
    value = _extract_table_value(content, "Scope of Authorization")
    return value or "Passive review only"
