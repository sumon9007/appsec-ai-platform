"""
stop_conditions.py — Mandatory stop conditions per safety-authorization-rules.md Rule 4.

Each function checks for a condition that requires immediate halt of audit activity.
All tools should call check_all() after collecting evidence and before proceeding.
"""

from __future__ import annotations

import logging
import re
from typing import List, Optional

logger = logging.getLogger(__name__)


class StopConditionTriggered(RuntimeError):
    """Raised when a mandatory stop condition is detected."""


# ── Sensitive data patterns ────────────────────────────────────────────────────

_SENSITIVE_PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "payment_card_visa": re.compile(r"\b4[0-9]{12}(?:[0-9]{3})?\b"),
    "payment_card_mc": re.compile(r"\b5[1-5][0-9]{14}\b"),
    "payment_card_amex": re.compile(r"\b3[47][0-9]{13}\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "plaintext_password": re.compile(r"password\s*[:=]\s*\S{8,}", re.IGNORECASE),
}

# ── Compromise indicators ──────────────────────────────────────────────────────

_COMPROMISE_INDICATORS = [
    re.compile(r"<script[^>]*>.*?(eval|document\.write|unescape)\s*\(", re.IGNORECASE | re.DOTALL),
    re.compile(r"(php|asp|jsp)\s*shell", re.IGNORECASE),
    re.compile(r"b374k|c99shell|r57shell", re.IGNORECASE),
    re.compile(r"hacked\s+by", re.IGNORECASE),
]


def check_for_sensitive_data(content: str, source_description: str) -> Optional[str]:
    """
    Scan content for unexpected sensitive data.
    Returns the type of sensitive data found, or None.
    Does NOT stop itself — caller decides whether to raise StopConditionTriggered.
    """
    for data_type, pattern in _SENSITIVE_PATTERNS.items():
        if pattern.search(content):
            logger.error(
                "STOP CONDITION: Unexpected sensitive data detected in %s — type: %s. "
                "Per safety-authorization-rules.md Rule 4: stop all activity, "
                "do not store the raw data, alert the user immediately.",
                source_description,
                data_type,
            )
            return data_type
    return None


def check_for_compromise_indicators(content: str, source_description: str) -> Optional[str]:
    """
    Scan response content for signs of active compromise (web shells, defacement).
    Returns indicator label if found, or None.
    """
    for pattern in _COMPROMISE_INDICATORS:
        match = pattern.search(content)
        if match:
            indicator = match.group(0)[:80]
            logger.error(
                "STOP CONDITION: Possible compromise indicator detected in %s — pattern: %s. "
                "Per safety-authorization-rules.md Rule 4: stop all testing, "
                "preserve evidence, alert the client immediately. Do not modify anything.",
                source_description,
                indicator,
            )
            return indicator
    return None


def check_all(content: str, source_description: str, raise_on_detection: bool = True) -> List[str]:
    """
    Run all stop condition checks against a piece of content.

    If raise_on_detection is True (default), raises StopConditionTriggered on first match.
    Returns a list of triggered condition labels (empty if none).
    """
    triggered = []

    sensitive = check_for_sensitive_data(content, source_description)
    if sensitive:
        triggered.append(f"sensitive_data:{sensitive}")

    compromise = check_for_compromise_indicators(content, source_description)
    if compromise:
        triggered.append(f"compromise_indicator")

    if triggered and raise_on_detection:
        raise StopConditionTriggered(
            f"Mandatory stop condition triggered while processing {source_description}: "
            f"{', '.join(triggered)}. "
            "Stop all audit activity. Document what was encountered. "
            "Alert the user and authorizing party. "
            "See .claude/rules/safety-authorization-rules.md Rule 4."
        )

    return triggered
