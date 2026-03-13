"""
headers_audit.py — HTTP Security Headers passive audit tool.

Checks for the presence and quality of security response headers.
All requests are GET-only (passive review). No payloads injected.

Severity mapping follows severity-rating-rules.md and acceptance-criteria.md.
"""

import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from src.utils.evidence_writer import write_evidence
from src.utils.http_client import HttpClient

logger = logging.getLogger(__name__)

# ── Header check definitions ──────────────────────────────────────────────────

def _check_hsts(headers: Dict[str, str]) -> Dict[str, Any]:
    hsts = headers.get("strict-transport-security", "")
    if not hsts:
        return {
            "check": "Strict-Transport-Security (HSTS)",
            "assessment": "MISSING",
            "severity": "Medium",
            "confidence": "high",
            "detail": "HSTS header is absent. Browsers will not enforce HTTPS connections.",
            "recommendation": (
                "Add the Strict-Transport-Security header with a max-age of at least 15768000 "
                "(6 months). Example: Strict-Transport-Security: max-age=31536000; "
                "includeSubDomains; preload"
            ),
        }
    issues = []
    max_age = 0
    for part in hsts.split(";"):
        part = part.strip()
        if part.lower().startswith("max-age="):
            try:
                max_age = int(part.split("=", 1)[1])
            except ValueError:
                pass
    if max_age < 15768000:
        issues.append(f"max-age={max_age} is below the recommended minimum of 15768000 (6 months)")
    if "includesubdomains" not in hsts.lower():
        issues.append("includeSubDomains directive is absent")
    if "preload" not in hsts.lower():
        issues.append("preload directive is absent (optional but recommended)")

    if issues:
        return {
            "check": "Strict-Transport-Security (HSTS)",
            "assessment": "WEAK",
            "severity": "Low",
            "confidence": "high",
            "detail": f"HSTS header present but weak: {'; '.join(issues)}. Value: {hsts}",
            "recommendation": (
                "Strengthen HSTS: set max-age to at least 31536000, add includeSubDomains, "
                "and consider adding preload for HSTS preload list eligibility."
            ),
        }
    return {
        "check": "Strict-Transport-Security (HSTS)",
        "assessment": "STRONG",
        "severity": None,
        "confidence": "high",
        "detail": f"HSTS header present and strong: {hsts}",
        "recommendation": None,
    }


def _check_csp(headers: Dict[str, str]) -> Dict[str, Any]:
    csp = headers.get("content-security-policy", "")
    csp_ro = headers.get("content-security-policy-report-only", "")

    if not csp and not csp_ro:
        return {
            "check": "Content-Security-Policy (CSP)",
            "assessment": "MISSING",
            "severity": "Medium",
            "confidence": "high",
            "detail": "No Content-Security-Policy header found.",
            "recommendation": (
                "Implement a Content-Security-Policy header. Start with a report-only policy "
                "to observe violations before enforcing. At minimum restrict default-src to "
                "'self'. Avoid 'unsafe-inline' and 'unsafe-eval'."
            ),
        }

    active = csp or csp_ro
    mode = "report-only" if not csp else "enforcing"
    issues = []
    if "'unsafe-inline'" in active:
        issues.append("'unsafe-inline' present — allows inline script/style execution")
    if "'unsafe-eval'" in active:
        issues.append("'unsafe-eval' present — allows eval() and similar dynamic code execution")
    if "frame-ancestors" not in active and "x-frame-options" not in headers:
        issues.append("frame-ancestors directive absent (clickjacking protection incomplete)")

    if not csp and csp_ro:
        issues.append(f"Policy is in report-only mode — not enforcing")

    if issues:
        return {
            "check": "Content-Security-Policy (CSP)",
            "assessment": "WEAK",
            "severity": "Medium" if not csp else "Low",
            "confidence": "high",
            "detail": f"CSP present ({mode}) but has weaknesses: {'; '.join(issues)}. Value: {active[:300]}",
            "recommendation": (
                "Review and tighten CSP: remove 'unsafe-inline' (use nonces or hashes), "
                "remove 'unsafe-eval', add frame-ancestors directive. Transition report-only "
                "policies to enforcing mode."
            ),
        }
    return {
        "check": "Content-Security-Policy (CSP)",
        "assessment": "ADEQUATE",
        "severity": None,
        "confidence": "medium",
        "detail": f"CSP present ({mode}): {active[:300]}",
        "recommendation": None,
    }


def _check_xcto(headers: Dict[str, str]) -> Dict[str, Any]:
    xcto = headers.get("x-content-type-options", "")
    if xcto.strip().lower() != "nosniff":
        return {
            "check": "X-Content-Type-Options",
            "assessment": "MISSING" if not xcto else "WEAK",
            "severity": "Low",
            "confidence": "high",
            "detail": f"X-Content-Type-Options is {'absent' if not xcto else 'not set to nosniff (value: ' + xcto + ')'}.",
            "recommendation": "Add the header: X-Content-Type-Options: nosniff",
        }
    return {
        "check": "X-Content-Type-Options",
        "assessment": "PASS",
        "severity": None,
        "confidence": "high",
        "detail": "X-Content-Type-Options: nosniff is present.",
        "recommendation": None,
    }


def _check_clickjacking(headers: Dict[str, str]) -> Dict[str, Any]:
    xfo = headers.get("x-frame-options", "")
    csp = headers.get("content-security-policy", "")
    has_frame_ancestors = "frame-ancestors" in csp

    if not xfo and not has_frame_ancestors:
        return {
            "check": "Clickjacking Protection (X-Frame-Options / CSP frame-ancestors)",
            "assessment": "MISSING",
            "severity": "Medium",
            "confidence": "high",
            "detail": "Neither X-Frame-Options nor CSP frame-ancestors directive found.",
            "recommendation": (
                "Add X-Frame-Options: DENY (or SAMEORIGIN if framing by same origin is needed), "
                "or add frame-ancestors 'none' to your CSP. Prefer the CSP approach for new deployments."
            ),
        }
    if xfo and xfo.upper() not in ("DENY", "SAMEORIGIN"):
        return {
            "check": "Clickjacking Protection (X-Frame-Options / CSP frame-ancestors)",
            "assessment": "WEAK",
            "severity": "Low",
            "confidence": "high",
            "detail": f"X-Frame-Options value '{xfo}' is not DENY or SAMEORIGIN.",
            "recommendation": "Set X-Frame-Options to DENY or SAMEORIGIN.",
        }
    return {
        "check": "Clickjacking Protection (X-Frame-Options / CSP frame-ancestors)",
        "assessment": "PASS",
        "severity": None,
        "confidence": "high",
        "detail": f"Clickjacking protection present. X-Frame-Options: {xfo or 'not set (CSP frame-ancestors present)'}",
        "recommendation": None,
    }


def _check_referrer_policy(headers: Dict[str, str]) -> Dict[str, Any]:
    rp = headers.get("referrer-policy", "")
    if not rp:
        return {
            "check": "Referrer-Policy",
            "assessment": "MISSING",
            "severity": "Low",
            "confidence": "high",
            "detail": "Referrer-Policy header is absent. Browser default behaviour applies.",
            "recommendation": (
                "Add Referrer-Policy: strict-origin-when-cross-origin or no-referrer "
                "to prevent leaking the full URL in referrer headers to third parties."
            ),
        }
    weak_values = ("unsafe-url", "no-referrer-when-downgrade")
    if rp.lower() in weak_values:
        return {
            "check": "Referrer-Policy",
            "assessment": "WEAK",
            "severity": "Low",
            "confidence": "high",
            "detail": f"Referrer-Policy is set to a permissive value: {rp}",
            "recommendation": (
                "Use a more restrictive Referrer-Policy such as 'strict-origin-when-cross-origin' "
                "or 'no-referrer'."
            ),
        }
    return {
        "check": "Referrer-Policy",
        "assessment": "PASS",
        "severity": None,
        "confidence": "high",
        "detail": f"Referrer-Policy: {rp}",
        "recommendation": None,
    }


def _check_permissions_policy(headers: Dict[str, str]) -> Dict[str, Any]:
    pp = headers.get("permissions-policy", "")
    if not pp:
        return {
            "check": "Permissions-Policy",
            "assessment": "MISSING",
            "severity": "Low",
            "confidence": "high",
            "detail": "Permissions-Policy header is absent.",
            "recommendation": (
                "Add a Permissions-Policy header to restrict access to browser features "
                "(e.g., camera, microphone, geolocation). Example: "
                "Permissions-Policy: camera=(), microphone=(), geolocation=()"
            ),
        }
    return {
        "check": "Permissions-Policy",
        "assessment": "PASS",
        "severity": None,
        "confidence": "medium",
        "detail": f"Permissions-Policy header present. Manual review recommended to assess policy scope: {pp[:200]}",
        "recommendation": None,
    }


def _check_cors(headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    acao = headers.get("access-control-allow-origin", "")
    acac = headers.get("access-control-allow-credentials", "").lower()
    if acao == "*" and acac == "true":
        return {
            "check": "CORS — Wildcard Origin with Credentials",
            "assessment": "VULNERABLE",
            "severity": "Critical",
            "confidence": "high",
            "detail": (
                "Access-Control-Allow-Origin: * is set alongside "
                "Access-Control-Allow-Credentials: true. "
                "This combination allows any origin to make credentialed cross-origin requests."
            ),
            "recommendation": (
                "Remove the wildcard origin. Explicitly allowlist trusted origins. "
                "Access-Control-Allow-Credentials: true must never be combined with a wildcard origin."
            ),
        }
    if acao == "*":
        return {
            "check": "CORS — Wildcard Origin",
            "assessment": "WEAK",
            "severity": "Info",
            "confidence": "high",
            "detail": "Access-Control-Allow-Origin: * — all origins permitted for non-credentialed requests.",
            "recommendation": (
                "Review whether a wildcard CORS policy is intentional. "
                "If the API is not public, restrict to known trusted origins."
            ),
        }
    return None


def _check_information_exposure(headers: Dict[str, str]) -> List[Dict[str, Any]]:
    results = []
    for header_name in ("x-powered-by", "x-aspnet-version", "x-aspnetmvc-version"):
        value = headers.get(header_name, "")
        if value:
            results.append({
                "check": f"Information Exposure — {header_name}",
                "assessment": "FAIL",
                "severity": "Low",
                "confidence": "high",
                "detail": f"Header '{header_name}: {value}' reveals technology stack information.",
                "recommendation": f"Remove or suppress the {header_name} response header in your server/framework configuration.",
            })
    server = headers.get("server", "")
    if server and any(kw in server.lower() for kw in ("apache/", "nginx/", "iis/", "express", "php")):
        results.append({
            "check": "Information Exposure — Server header with version",
            "assessment": "FAIL",
            "severity": "Low",
            "confidence": "high",
            "detail": f"Server header reveals detailed software version: {server}",
            "recommendation": "Configure the server to suppress version information in the Server header.",
        })
    return results


# ── Main tool class ───────────────────────────────────────────────────────────

class HeadersAudit:
    """Passive HTTP security headers audit tool."""

    DOMAIN = "Security Headers"
    EVIDENCE_TYPE = "HTTP Capture"

    def __init__(self, http_client: HttpClient, collector: str) -> None:
        self._client = http_client
        self._collector = collector

    def run(self, url: str) -> List[Dict[str, Any]]:
        """
        Fetch the URL and evaluate security response headers.

        Returns a list of result dicts (one per check with a non-passing assessment).
        Each dict contains all data needed to write evidence and optionally a finding.
        """
        logger.info("Headers audit starting: %s", url)
        results = []

        response = self._client.get(url)
        if response is None:
            logger.error(
                "Headers audit skipped for %s — HTTP request failed. "
                "Remediation: Verify the URL is reachable and SSL configuration is correct.",
                url,
            )
            return [{"error": f"HTTP request failed for {url}", "url": url}]

        # Normalise header names to lowercase for consistent lookup
        headers = {k.lower(): v for k, v in response.headers.items()}

        # Collect redirect chain summary for evidence
        redirect_chain = []
        for r in response.history:
            redirect_chain.append(f"{r.status_code} {r.url} → {r.headers.get('Location', '?')}")
        redirect_summary = "\n".join(redirect_chain) if redirect_chain else "No redirects"

        # Format raw headers for evidence content
        raw_headers = "\n".join(f"{k}: {v}" for k, v in response.headers.items())
        evidence_content = (
            f"Request URL: {url}\n"
            f"Final URL: {response.url}\n"
            f"Status: {response.status_code}\n\n"
            f"Redirect Chain:\n{redirect_summary}\n\n"
            f"Response Headers:\n{raw_headers}"
        )

        # Write one evidence file for the full header capture
        evid_label, _ = write_evidence(
            description=f"HTTP response headers capture — {urlparse(url).netloc}",
            domain=self.DOMAIN,
            evidence_type=self.EVIDENCE_TYPE,
            content=evidence_content,
            collector=self._collector,
            target=url,
            observations=(
                f"Full response headers captured from {url} for security header analysis. "
                f"Status: {response.status_code}. "
                f"Redirects: {len(response.history)}."
            ),
        )

        # Run all checks
        checks = [
            _check_hsts(headers),
            _check_csp(headers),
            _check_xcto(headers),
            _check_clickjacking(headers),
            _check_referrer_policy(headers),
            _check_permissions_policy(headers),
        ]

        cors_result = _check_cors(headers)
        if cors_result:
            checks.append(cors_result)

        checks.extend(_check_information_exposure(headers))

        # Filter to non-passing results only and attach evidence label
        for check in checks:
            if check.get("assessment") not in ("PASS", "STRONG", "ADEQUATE"):
                check["url"] = url
                check["evid_label"] = evid_label
                check["domain"] = self.DOMAIN
                results.append(check)

        logger.info(
            "Headers audit complete: %s — %d issue(s) found",
            url,
            len(results),
        )
        return results
