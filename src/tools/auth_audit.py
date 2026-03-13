"""
auth_audit.py — Authentication review tool.

Passive observations:
- Login page characteristics (MFA prompt, account lockout signals)
- Password reset flow observation
- HTTPS enforcement on auth pages
- Information disclosure on failed login (username enumeration)

Authenticated observations (requires test account + CONFIRMED authorization):
- MFA enforcement
- Account lockout after failed attempts
- Session invalidation on logout
- Password policy signals

Active testing (e.g., brute force attempts) is NOT implemented and requires
explicit active testing authorization per safety-authorization-rules.md Rule 3.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

from src.utils.evidence_writer import write_evidence
from src.utils.http_client import HttpClient

logger = logging.getLogger(__name__)

DOMAIN = "Authentication"
EVIDENCE_TYPE = "HTTP Capture"

# Common login page paths to probe
_LOGIN_PATHS = [
    "/login", "/signin", "/sign-in", "/auth", "/auth/login",
    "/user/login", "/users/sign_in", "/account/login", "/admin/login",
    "/wp-login.php", "/wp-admin/",
]

_PASSWORD_RESET_PATHS = [
    "/forgot-password", "/reset-password", "/password/reset",
    "/auth/forgot", "/user/password/new", "/account/forgot",
]


class AuthAudit:
    """Authentication review tool — passive and authenticated observations."""

    def __init__(self, http_client: HttpClient, collector: str) -> None:
        self._client = http_client
        self._collector = collector

    def run(self, url: str) -> List[Dict[str, Any]]:
        """
        Run passive authentication observations.
        Returns finding-ready result dicts.
        """
        logger.info("Auth audit starting: %s", url)
        results = []
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"

        evidence_lines = []
        findings_pre_evidence = []

        # Find and assess login pages
        login_url_found = None
        for path in _LOGIN_PATHS:
            probe_url = urljoin(base, path)
            response = self._client.get(probe_url)
            if response is None:
                continue
            if response.status_code in (200, 301, 302):
                evidence_lines.append(f"[{response.status_code}] Login path found: {probe_url}")
                if response.status_code == 200 and "password" in response.text.lower():
                    login_url_found = probe_url
                    findings_pre_evidence.extend(
                        self._assess_login_page(response.text, probe_url, response.headers)
                    )
                    break

        if not login_url_found:
            findings_pre_evidence.append({
                "check": "Authentication — Login Page Not Found via Common Paths",
                "assessment": "REVIEW_GAP",
                "severity": "Info",
                "confidence": "low",
                "url": url,
                "detail": (
                    "[REVIEW GAP] No login page was found at common paths. "
                    "The login URL may use a non-standard path or the application may use SSO/OAuth."
                ),
                "recommendation": (
                    "Manually identify the login URL from the application and re-run "
                    "--login-path /your/login/path to assess the authentication flow."
                ),
            })

        # HTTPS check on auth pages
        if login_url_found and not login_url_found.startswith("https://"):
            findings_pre_evidence.append({
                "check": "Authentication — Login Page Not on HTTPS",
                "assessment": "FAIL",
                "severity": "Critical",
                "confidence": "high",
                "url": login_url_found,
                "detail": "The login page is served over HTTP. Credentials are transmitted in plaintext.",
                "recommendation": "Enforce HTTPS for all authentication pages. Configure HTTP→HTTPS redirects.",
            })

        # Password reset flow
        reset_url_found = None
        for path in _PASSWORD_RESET_PATHS:
            probe_url = urljoin(base, path)
            response = self._client.get(probe_url)
            if response and response.status_code == 200:
                evidence_lines.append(f"[200] Password reset found: {probe_url}")
                reset_url_found = probe_url
                break
        if not reset_url_found:
            evidence_lines.append("[not found] No password reset page at common paths")

        # Write evidence
        content = (
            f"Target: {url}\n"
            f"Login page found: {login_url_found or 'not found'}\n"
            f"Password reset found: {reset_url_found or 'not found'}\n\n"
            f"Observations:\n" + "\n".join(f"  {line}" for line in evidence_lines) + "\n\n"
            "[REVIEW GAP] The following require authenticated testing:\n"
            "  - MFA enforcement on privileged accounts (Auth-Must-Fix-1)\n"
            "  - Account lockout after repeated failures\n"
            "  - Session invalidation on logout\n"
            "  - Password strength policy enforcement\n"
            "  - Username enumeration via login response differences"
        )

        evid_label = None
        try:
            evid_label, _ = write_evidence(
                description=f"Authentication flow passive review — {urlparse(url).netloc}",
                domain=DOMAIN,
                evidence_type=EVIDENCE_TYPE,
                content=content,
                collector=self._collector,
                target=url,
                observations=(
                    f"Passive authentication review of {url}. "
                    f"Login page: {login_url_found or 'not found'}. "
                    f"Reset page: {reset_url_found or 'not found'}."
                ),
            )
        except Exception as exc:
            logger.error("Could not write auth evidence: %s", exc)

        # Add review gap for authenticated auth checks
        findings_pre_evidence.append({
            "check": "Authentication — MFA Enforcement (Review Gap)",
            "assessment": "REVIEW_GAP",
            "severity": "High",
            "confidence": "low",
            "url": login_url_found or url,
            "detail": (
                "[REVIEW GAP] MFA enforcement cannot be confirmed without an authenticated test account "
                "with admin role access. Per Auth-Must-Fix-1, MFA is required for all privileged roles."
            ),
            "recommendation": (
                "[REQUIRES AUTHENTICATED TESTING] Log in with a provided admin test account and "
                "verify MFA is enforced at step-up. Confirm MFA cannot be bypassed by direct URL access."
            ),
        })

        for f in findings_pre_evidence:
            f["domain"] = DOMAIN
            f["evid_label"] = evid_label
            results.append(f)

        logger.info("Auth audit complete: %s — %d issue(s)", url, len(results))
        return results

    def _assess_login_page(
        self, html: str, login_url: str, headers: dict
    ) -> List[Dict[str, Any]]:
        """Observe the login page for passive security signals."""
        issues = []
        html_lower = html.lower()

        # MFA presence signal
        mfa_keywords = ("otp", "one-time", "authenticator", "mfa", "2fa", "two-factor", "verification code")
        has_mfa_signal = any(kw in html_lower for kw in mfa_keywords)
        if not has_mfa_signal:
            issues.append({
                "check": "Authentication — No MFA Prompt Observed on Login Page",
                "assessment": "REVIEW_GAP",
                "severity": "High",
                "confidence": "low",
                "url": login_url,
                "detail": (
                    "No MFA-related keywords observed on the login page. "
                    "[UNKNOWN] MFA may be enforced post-credential-validation or may be absent."
                ),
                "recommendation": (
                    "[REQUIRES AUTHENTICATED TESTING] Provide admin test credentials to confirm "
                    "MFA is enforced for privileged accounts."
                ),
            })

        # CSRF token presence
        csrf_keywords = ("csrf", "_token", "csrfmiddlewaretoken", "authenticity_token")
        has_csrf = any(kw in html_lower for kw in csrf_keywords)
        if not has_csrf:
            issues.append({
                "check": "Authentication — No CSRF Token on Login Form",
                "assessment": "MISSING",
                "severity": "High",
                "confidence": "medium",
                "url": login_url,
                "detail": (
                    "No CSRF token fields detected in the login form. "
                    "This may allow cross-site request forgery of login actions."
                ),
                "recommendation": (
                    "Implement CSRF protection on login forms using synchronizer tokens "
                    "or SameSite=Strict cookies. Verify server-side validation of CSRF tokens."
                ),
            })

        # Autocomplete on password field
        if 'autocomplete="off"' not in html_lower and 'autocomplete="new-password"' not in html_lower:
            issues.append({
                "check": "Authentication — Password Field May Allow Browser Autocomplete",
                "assessment": "WEAK",
                "severity": "Low",
                "confidence": "low",
                "url": login_url,
                "detail": "No autocomplete='off' or autocomplete='new-password' detected on the login page.",
                "recommendation": (
                    "Set autocomplete='off' on the password field or use 'current-password'/'new-password' "
                    "per HTML5 spec to control browser autocomplete behavior."
                ),
            })

        return issues
