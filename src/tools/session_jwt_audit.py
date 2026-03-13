"""
session_jwt_audit.py — Session management and JWT passive audit tool.

Checks for:
- JWT tokens in response headers, cookies, and body (passive detection)
- Algorithm weaknesses (none, weak HMAC)
- Expiry configuration
- Sensitive data in JWT payload
- Session cookie best practices (delegates cookie attribute checks to cookie_audit.py)

This tool is PASSIVE — it observes tokens in responses without injecting anything.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List
from urllib.parse import urlparse

from src.parsers.jwt_parser import ParsedJWT, decode_jwt, find_jwts_in_text
from src.utils.evidence_writer import write_evidence
from src.utils.http_client import HttpClient

logger = logging.getLogger(__name__)

DOMAIN = "Session Management"
EVIDENCE_TYPE = "HTTP Capture"


class SessionJwtAudit:
    """Passive session management and JWT analysis tool."""

    def __init__(self, http_client: HttpClient, collector: str) -> None:
        self._client = http_client
        self._collector = collector

    def run(self, url: str) -> List[Dict[str, Any]]:
        """
        Fetch the URL and scan for JWT tokens in headers, cookies, and response body.
        Returns finding-ready result dicts for any issues found.
        """
        logger.info("Session/JWT audit starting: %s", url)
        results = []

        response = self._client.get(url)
        if response is None:
            return [{"error": f"HTTP request failed for {url}", "url": url}]

        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        jwts_found: List[ParsedJWT] = []
        jwt_sources: List[str] = []

        # Check Authorization header
        auth_header = headers_lower.get("authorization", "")
        if auth_header.lower().startswith("bearer "):
            token = auth_header.split(" ", 1)[1]
            parsed = decode_jwt(token)
            jwts_found.append(parsed)
            jwt_sources.append("Authorization response header")

        # Check cookies
        for cookie in response.cookies:
            token_like = cookie.value or ""
            if token_like.count(".") == 2 and token_like.startswith("eyJ"):
                parsed = decode_jwt(token_like)
                jwts_found.append(parsed)
                jwt_sources.append(f"Cookie: {cookie.name}")

        # Check response body (limited to first 10KB for performance)
        body_snippet = response.text[:10240]
        for token in find_jwts_in_text(body_snippet):
            parsed = decode_jwt(token)
            jwts_found.append(parsed)
            jwt_sources.append("Response body")

        # Evidence
        evidence_content = (
            f"URL: {url}\nStatus: {response.status_code}\n\n"
            f"JWT tokens detected: {len(jwts_found)}\n"
            f"Sources: {', '.join(jwt_sources) if jwt_sources else 'none'}\n\n"
        )
        if jwts_found:
            for i, (jwt, source) in enumerate(zip(jwts_found, jwt_sources), 1):
                evidence_content += (
                    f"JWT {i} (from {source}):\n"
                    f"  Algorithm: {jwt.algorithm}\n"
                    f"  Header: {jwt.header}\n"
                    f"  Payload keys: {list(jwt.payload.keys())}\n"
                    f"  Expired: {jwt.is_expired}\n"
                    f"  Sensitive claims: {jwt.sensitive_claim_names}\n\n"
                )

        evid_label, _ = write_evidence(
            description=f"Session / JWT analysis — {urlparse(url).netloc}",
            domain=DOMAIN,
            evidence_type=EVIDENCE_TYPE,
            content=evidence_content,
            collector=self._collector,
            target=url,
            observations=(
                f"Passive JWT scan of {url}. "
                f"{len(jwts_found)} JWT token(s) detected in response headers, cookies, or body. "
                "Note: tokens visible on unauthenticated responses only."
            ),
        )

        if not jwts_found:
            results.append({
                "check": "Session/JWT — Review Gap (no tokens on unauthenticated response)",
                "assessment": "REVIEW_GAP",
                "severity": "Info",
                "confidence": "low",
                "url": url,
                "detail": (
                    "No JWT tokens observed in the unauthenticated response. "
                    "[REVIEW GAP] JWTs issued during authenticated sessions require "
                    "review with a test account."
                ),
                "recommendation": (
                    "[REQUIRES AUTHENTICATED ACCESS] After logging in, capture the JWT token "
                    "and validate: algorithm (avoid 'none' and HS256), expiry (exp claim), "
                    "sensitive data in payload, and rotation on logout."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })
            return results

        # Assess each found JWT
        for jwt, source in zip(jwts_found, jwt_sources):
            results.extend(self._assess_jwt(jwt, source, url, evid_label))

        logger.info("Session/JWT audit complete: %s — %d issue(s)", url, len(results))
        return results

    def _assess_jwt(
        self, jwt: ParsedJWT, source: str, url: str, evid_label: str
    ) -> List[Dict[str, Any]]:
        issues = []

        if jwt.parse_error:
            issues.append({
                "check": f"JWT — Parse error ({source})",
                "assessment": "REVIEW_GAP",
                "severity": "Info",
                "confidence": "low",
                "url": url,
                "detail": f"JWT from {source} could not be fully parsed: {jwt.parse_error}",
                "recommendation": "Manually inspect the token structure.",
                "domain": DOMAIN,
                "evid_label": evid_label,
            })
            return issues

        # Algorithm: none
        if jwt.alg_is_none:
            issues.append({
                "check": f"JWT — Algorithm 'none' ({source})",
                "assessment": "VULNERABLE",
                "severity": "Critical",
                "confidence": "high",
                "url": url,
                "detail": (
                    f"JWT from {source} uses algorithm 'none'. "
                    "This means the token has no signature and cannot be verified. "
                    "Any client can forge a token with arbitrary claims."
                ),
                "recommendation": (
                    "Reject JWTs with alg: none on the server side. "
                    "Use RS256 or ES256 for production tokens. "
                    "Validate the algorithm explicitly against an allowlist."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })

        # Algorithm: weak HS256
        elif jwt.algorithm.upper() == "HS256":
            issues.append({
                "check": f"JWT — Weak Algorithm HS256 ({source})",
                "assessment": "WEAK",
                "severity": "Medium",
                "confidence": "medium",
                "url": url,
                "detail": (
                    f"JWT from {source} uses HS256 (symmetric HMAC). "
                    "This requires the same secret on issuer and verifier. "
                    "Weak secrets are susceptible to brute-force attacks."
                ),
                "recommendation": (
                    "Prefer RS256 or ES256 (asymmetric) for service-to-service JWTs. "
                    "If HS256 is used, ensure the secret is at least 256 bits of entropy "
                    "and is rotated regularly."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })

        # Expiry
        if jwt.is_expired:
            issues.append({
                "check": f"JWT — Token Expired ({source})",
                "assessment": "FAIL",
                "severity": "High",
                "confidence": "high",
                "url": url,
                "detail": f"JWT from {source} has an expired expiry claim (exp).",
                "recommendation": "Ensure server-side validation rejects expired tokens.",
                "domain": DOMAIN,
                "evid_label": evid_label,
            })
        elif "exp" not in jwt.payload:
            issues.append({
                "check": f"JWT — Missing Expiry Claim ({source})",
                "assessment": "MISSING",
                "severity": "High",
                "confidence": "high",
                "url": url,
                "detail": f"JWT from {source} has no 'exp' claim. The token never expires.",
                "recommendation": (
                    "Always set the 'exp' claim. Use short-lived tokens (15 min to 1 hour) "
                    "with refresh token rotation for session continuity."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })

        # Sensitive data in payload
        if jwt.has_sensitive_claims:
            issues.append({
                "check": f"JWT — Sensitive Data in Payload ({source})",
                "assessment": "FAIL",
                "severity": "Medium",
                "confidence": "medium",
                "url": url,
                "detail": (
                    f"JWT from {source} payload contains potentially sensitive claim names: "
                    f"{jwt.sensitive_claim_names}. "
                    "JWT payloads are base64-encoded but NOT encrypted — they are readable by anyone."
                ),
                "recommendation": (
                    "Do not store sensitive data (passwords, PII, secrets) in JWT payloads. "
                    "If sensitive data must be in a token, use JWE (JSON Web Encryption) "
                    "rather than plain JWT."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })

        return issues
