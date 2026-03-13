"""
jwt_parser.py — Passive JWT decode and analysis (no signature verification).

Decodes JWT header and payload for audit observations only.
Signature verification is intentionally NOT performed — this is a passive review tool.

Key audit observations:
- Algorithm claims (none, weak algorithms)
- Expiry (exp claim)
- Issued-at / not-before
- Subject / issuer claims
- Sensitive data in payload
"""

from __future__ import annotations

import base64
import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_JWT_PATTERN = re.compile(
    r"eyJ[A-Za-z0-9_-]+\."   # header (base64url starting with eyJ)
    r"[A-Za-z0-9_-]*\."       # payload
    r"[A-Za-z0-9_-]*"         # signature
)

_SENSITIVE_CLAIM_PATTERNS = [
    re.compile(r"password", re.IGNORECASE),
    re.compile(r"secret", re.IGNORECASE),
    re.compile(r"ssn", re.IGNORECASE),
    re.compile(r"credit_card", re.IGNORECASE),
]

_WEAK_ALGORITHMS = {"none", "hs256"}   # none = critical; hs256 = weak by modern standards


@dataclass
class ParsedJWT:
    raw: str                              # full JWT token (may be truncated)
    header: Dict[str, Any] = field(default_factory=dict)
    payload: Dict[str, Any] = field(default_factory=dict)
    algorithm: str = ""
    is_expired: Optional[bool] = None
    days_until_expiry: Optional[int] = None
    has_sensitive_claims: bool = False
    sensitive_claim_names: List[str] = field(default_factory=list)
    parse_error: Optional[str] = None

    @property
    def alg_is_none(self) -> bool:
        return self.algorithm.lower() == "none"

    @property
    def alg_is_weak(self) -> bool:
        return self.algorithm.lower() in _WEAK_ALGORITHMS


def _b64_decode(data: str) -> bytes:
    """Base64url decode with padding."""
    padded = data + "=" * (4 - len(data) % 4)
    return base64.urlsafe_b64decode(padded)


def decode_jwt(token: str) -> ParsedJWT:
    """
    Decode a JWT token without verifying the signature.
    Returns a ParsedJWT with parsed header and payload.
    """
    # Truncate stored value for evidence safety
    jwt = ParsedJWT(raw=token[:20] + "...[TRUNCATED]")

    parts = token.strip().split(".")
    if len(parts) != 3:
        jwt.parse_error = f"Invalid JWT format — expected 3 parts, got {len(parts)}"
        return jwt

    try:
        jwt.header = json.loads(_b64_decode(parts[0]))
        jwt.algorithm = jwt.header.get("alg", "unknown")
    except Exception as exc:
        jwt.parse_error = f"Could not decode JWT header: {exc}"
        return jwt

    try:
        jwt.payload = json.loads(_b64_decode(parts[1]))
    except Exception as exc:
        jwt.parse_error = f"Could not decode JWT payload: {exc}"
        return jwt

    # Expiry analysis
    exp = jwt.payload.get("exp")
    if exp is not None:
        try:
            exp_dt = datetime.fromtimestamp(int(exp), tz=timezone.utc)
            now = datetime.now(tz=timezone.utc)
            delta = exp_dt - now
            jwt.is_expired = delta.total_seconds() < 0
            jwt.days_until_expiry = delta.days
        except (ValueError, OSError):
            pass

    # Sensitive claim detection
    for claim_name, claim_value in jwt.payload.items():
        for pattern in _SENSITIVE_CLAIM_PATTERNS:
            if pattern.search(claim_name) or (
                isinstance(claim_value, str) and pattern.search(claim_value)
            ):
                jwt.has_sensitive_claims = True
                if claim_name not in jwt.sensitive_claim_names:
                    jwt.sensitive_claim_names.append(claim_name)

    return jwt


def find_jwts_in_text(text: str) -> List[str]:
    """Extract all JWT-like strings from a block of text (e.g., a response body)."""
    return _JWT_PATTERN.findall(text)
