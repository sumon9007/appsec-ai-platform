"""
cookie_audit.py — Cookie security attributes passive audit tool.

Inspects Set-Cookie headers from the target URL response.
NOTE: Only cookies visible on the unauthenticated response are assessed.
Session cookies set during login are outside this passive tool's visibility.
That review gap is explicitly documented in every run.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List
from urllib.parse import urlparse

from src.parsers.cookie_parser import ParsedCookie, parse_all_set_cookie_headers
from src.utils.evidence_writer import write_evidence
from src.utils.http_client import HttpClient

logger = logging.getLogger(__name__)

DOMAIN = "Session Management"
EVIDENCE_TYPE = "HTTP Capture"


class CookieAudit:
    """Passive cookie security attributes audit tool."""

    def __init__(self, http_client: HttpClient, collector: str) -> None:
        self._client = http_client
        self._collector = collector

    def run(self, url: str) -> List[Dict[str, Any]]:
        """
        Fetch the URL and assess Set-Cookie security attributes.
        Returns a list of finding-ready result dicts.
        """
        logger.info("Cookie audit starting: %s", url)
        results = []

        response = self._client.get(url)
        if response is None:
            return [{"error": f"HTTP request failed for {url}", "url": url}]

        # Use requests' cookie jar for reliable parsing
        cookies_from_jar = []
        for cookie in response.cookies:
            cookies_from_jar.append(cookie)

        # Also parse raw Set-Cookie headers
        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        parsed_cookies = parse_all_set_cookie_headers(headers_lower)

        # Prefer the jar (more reliable) but fall back to parsed headers
        cookie_data = []
        if cookies_from_jar:
            for c in cookies_from_jar:
                from src.parsers.cookie_parser import ParsedCookie
                pc = ParsedCookie(
                    name=c.name,
                    value=(c.value or "")[:64],
                    secure=bool(c.secure),
                    httponly="httponly" in str(c._rest).lower() if hasattr(c, "_rest") else False,
                    samesite=None,
                    path=c.path or "/",
                    domain=c.domain or "",
                    expires=str(c.expires) if c.expires else None,
                )
                cookie_data.append(pc)
        else:
            cookie_data = parsed_cookies

        # Build evidence content
        raw_headers = "\n".join(
            f"Set-Cookie: {v}"
            for k, v in response.headers.items()
            if k.lower() == "set-cookie"
        ) or "No Set-Cookie headers found"

        evid_label, _ = write_evidence(
            description=f"Cookie Set-Cookie header capture — {urlparse(url).netloc}",
            domain=DOMAIN,
            evidence_type=EVIDENCE_TYPE,
            content=f"URL: {url}\nStatus: {response.status_code}\n\n{raw_headers}",
            collector=self._collector,
            target=url,
            observations=(
                f"Captured {len(cookie_data)} cookie(s) from unauthenticated response to {url}. "
                "Note: session cookies set during login flow are not visible in this passive check."
            ),
        )

        if not cookie_data:
            results.append({
                "check": "Cookie — Review Gap (no cookies on unauthenticated response)",
                "assessment": "REVIEW_GAP",
                "severity": "Info",
                "confidence": "low",
                "url": url,
                "detail": (
                    "No Set-Cookie headers observed on the unauthenticated response. "
                    "[REVIEW GAP] Session cookies set during authentication cannot be "
                    "assessed without an authenticated test account."
                ),
                "recommendation": (
                    "[REQUIRES AUTHENTICATED ACCESS] Inspect session cookies set during "
                    "login using browser DevTools or Burp Suite. Verify Secure, HttpOnly, "
                    "and SameSite attributes are set on all session cookies."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })
            return results

        for cookie in cookie_data:
            results.extend(self._assess_cookie(cookie, url, evid_label))

        logger.info("Cookie audit complete: %s — %d issue(s)", url, len(results))
        return results

    def _assess_cookie(self, cookie: ParsedCookie, url: str, evid_label: str) -> List[Dict[str, Any]]:
        issues = []
        label = f"'{cookie.name}'"
        is_session = cookie.is_session_cookie

        # Secure flag
        if not cookie.secure:
            issues.append({
                "check": f"Cookie — Missing Secure flag ({cookie.name})",
                "assessment": "MISSING",
                "severity": "High" if is_session else "Medium",
                "confidence": "high",
                "url": url,
                "detail": f"Cookie {label} is missing the Secure flag. It may be transmitted over HTTP.",
                "recommendation": f"Add the Secure attribute to the {label} cookie.",
                "domain": DOMAIN,
                "evid_label": evid_label,
            })

        # HttpOnly flag
        if not cookie.httponly:
            issues.append({
                "check": f"Cookie — Missing HttpOnly flag ({cookie.name})",
                "assessment": "MISSING",
                "severity": "High" if is_session else "Low",
                "confidence": "high",
                "url": url,
                "detail": f"Cookie {label} is missing the HttpOnly flag. It is accessible via JavaScript.",
                "recommendation": f"Add the HttpOnly attribute to the {label} cookie to prevent JavaScript access.",
                "domain": DOMAIN,
                "evid_label": evid_label,
            })

        # SameSite
        if cookie.samesite is None:
            issues.append({
                "check": f"Cookie — Missing SameSite attribute ({cookie.name})",
                "assessment": "MISSING",
                "severity": "Medium" if is_session else "Low",
                "confidence": "high",
                "url": url,
                "detail": (
                    f"Cookie {label} has no SameSite attribute. "
                    "Modern browsers default to Lax, but explicit setting is recommended."
                ),
                "recommendation": (
                    f"Set SameSite=Lax or SameSite=Strict on the {label} cookie. "
                    "Avoid SameSite=None unless cross-site access is required "
                    "(and if so, ensure Secure is also set)."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })
        elif cookie.samesite == "None" and not cookie.secure:
            issues.append({
                "check": f"Cookie — SameSite=None without Secure ({cookie.name})",
                "assessment": "FAIL",
                "severity": "Medium",
                "confidence": "high",
                "url": url,
                "detail": f"Cookie {label} has SameSite=None but is missing the Secure flag.",
                "recommendation": (
                    f"SameSite=None requires the Secure attribute per the RFC spec. "
                    f"Add Secure to the {label} cookie or change SameSite to Lax or Strict."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })

        return issues
