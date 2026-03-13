"""
evidence_writer.py — Writes EVID-labeled evidence files to evidence/raw/.

Evidence file format follows .claude/docs/evidence-standard.md exactly.
Sensitive data patterns are detected and redacted before writing.
"""

import logging
import re
from datetime import date
from pathlib import Path
from typing import Optional

from src.config.settings import EVIDENCE_RAW_DIR

logger = logging.getLogger(__name__)

# Patterns that indicate sensitive data that must be redacted
_SENSITIVE_PATTERNS = [
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),  # private keys
    re.compile(r"Bearer\s+[A-Za-z0-9\-._~+/]{20,}"),                # Bearer tokens
    re.compile(r"Authorization:\s*Bearer\s+\S+", re.IGNORECASE),     # Auth header
    re.compile(r"\b4[0-9]{12}(?:[0-9]{3})?\b"),                     # Visa card
    re.compile(r"\b5[1-5][0-9]{14}\b"),                              # MasterCard
    re.compile(r"\b3[47][0-9]{13}\b"),                               # Amex
]

_REDACTION_MARKER = "[REDACTED — sensitive data detected by evidence writer]"


def _redact_sensitive(content: str) -> tuple[str, bool]:
    """
    Scan content for sensitive patterns and redact matches.
    Returns (redacted_content, was_redacted).
    """
    redacted = False
    for pattern in _SENSITIVE_PATTERNS:
        if pattern.search(content):
            content = pattern.sub(_REDACTION_MARKER, content)
            redacted = True
    return content, redacted


def next_evid_label(today: Optional[str] = None) -> str:
    """
    Determine the next EVID label for today's date by scanning evidence/raw/.

    Scans existing files each call so the sequence is correct even after
    partial runs or manually written evidence files.
    """
    if today is None:
        today = date.today().isoformat()

    EVIDENCE_RAW_DIR.mkdir(parents=True, exist_ok=True)

    prefix = f"EVID-{today}-"
    existing_nums = []

    for f in EVIDENCE_RAW_DIR.iterdir():
        if f.name.startswith(prefix):
            # Extract the NNN portion
            rest = f.name[len(prefix):]
            num_str = rest.split("-")[0]
            if num_str.isdigit():
                existing_nums.append(int(num_str))

    next_num = max(existing_nums, default=0) + 1
    return f"EVID-{today}-{next_num:03d}"


def write_evidence(
    description: str,
    domain: str,
    evidence_type: str,
    content: str,
    collector: str,
    target: str,
    observations: str,
    related_finding: str = "PENDING",
    today: Optional[str] = None,
) -> tuple[str, Path]:
    """
    Write a single EVID-labeled evidence file to evidence/raw/.

    Returns:
        (label, file_path) — the assigned EVID label and the written file path.
    """
    if today is None:
        today = date.today().isoformat()

    label = next_evid_label(today)

    # Redact sensitive data before writing
    safe_content, was_redacted = _redact_sensitive(content)
    if was_redacted:
        logger.warning(
            "Sensitive data pattern detected in evidence content for %s. "
            "Affected values have been redacted. Review %s manually before promoting to reviewed/.",
            label,
            EVIDENCE_RAW_DIR,
        )

    # Derive a slug from the description for the filename
    slug = re.sub(r"[^a-z0-9]+", "-", description.lower()).strip("-")[:60]
    filename = f"{label}-{slug}.md"
    file_path = EVIDENCE_RAW_DIR / filename

    file_content = f"""# Evidence: {label}

**Label:** {label}
**Date Collected:** {today}
**Collector:** {collector}
**Type:** {evidence_type}
**Domain:** {domain}
**Related Finding:** {related_finding}

---

## Description

{description}

---

## Evidence Content

```
{safe_content}
```

---

## Observations

{observations}

---

## Chain of Custody Notes

Collected automatically by appsec-audit-tool. Target: {target}.
{"NOTE: One or more values were redacted by the evidence writer — review raw source before promoting." if was_redacted else "No sensitive data redactions applied."}
"""

    file_path.write_text(file_content, encoding="utf-8")
    logger.info("Evidence written: %s → %s", label, file_path.name)
    return label, file_path
