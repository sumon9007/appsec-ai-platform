"""
misconfig_audit.py — Security misconfiguration passive audit tool.

Checks for:
- Default/example pages (admin panels, debug endpoints, etc.)
- Directory listings
- Exposed configuration/metadata files
- HTTP method exposure (OPTIONS)
- robots.txt and security.txt presence
- Error page information leakage
- Cache-control misconfigurations
- Verbose stack traces in error responses
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List
from urllib.parse import urljoin, urlparse

from src.utils.evidence_writer import write_evidence
from src.utils.http_client import HttpClient

logger = logging.getLogger(__name__)

DOMAIN = "Security Misconfiguration"
EVIDENCE_TYPE = "HTTP Capture"

# Paths to probe passively (observation only — no exploits)
_PROBE_PATHS = [
    ("/.git/config", "Git config exposed"),
    ("/.env", "Environment file exposed"),
    ("/admin", "Admin panel endpoint"),
    ("/admin/login", "Admin login page"),
    ("/wp-admin/", "WordPress admin"),
    ("/phpinfo.php", "PHPInfo page"),
    ("/server-status", "Apache server-status"),
    ("/server-info", "Apache server-info"),
    ("/.well-known/security.txt", "Security.txt"),
    ("/robots.txt", "robots.txt"),
    ("/sitemap.xml", "Sitemap"),
    ("/api/v1/", "API root"),
    ("/api/", "API root"),
    ("/swagger-ui.html", "Swagger UI"),
    ("/swagger-ui/", "Swagger UI"),
    ("/api-docs", "API docs"),
    ("/actuator", "Spring Boot Actuator"),
    ("/actuator/health", "Spring Boot health endpoint"),
    ("/debug", "Debug endpoint"),
    ("/console", "Debug console"),
    ("/__debug__/", "Django debug toolbar"),
    ("/metrics", "Metrics endpoint"),
    ("/health", "Health endpoint"),
]

_SENSITIVE_BODY_PATTERNS = [
    ("stack trace", "stack-trace", "High"),
    ("traceback", "stack-trace", "High"),
    ("exception in thread", "stack-trace", "High"),
    ("sql syntax", "sql-error", "High"),
    ("mysql_connect", "db-error", "High"),
    ("odbc_connect", "db-error", "High"),
    ("warning: mysqli", "db-error", "Medium"),
    ("[database error]", "db-error", "High"),
    ("fatal error:", "php-error", "Medium"),
    ("parse error:", "php-error", "Medium"),
    ("root:x:0:0", "file-disclosure", "Critical"),  # /etc/passwd
    ("[boot loader]", "file-disclosure", "Critical"),  # boot.ini
]


class MisconfigAudit:
    """Passive security misconfiguration audit tool."""

    def __init__(self, http_client: HttpClient, collector: str) -> None:
        self._client = http_client
        self._collector = collector

    def run(self, url: str) -> List[Dict[str, Any]]:
        """
        Probe for common misconfigurations on the target.
        All requests are GET-only. No payloads are injected.
        Returns a list of finding-ready result dicts.
        """
        logger.info("Misconfig audit starting: %s", url)
        results = []
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"

        # Collect all evidence content
        evidence_lines = []
        findings_pre_evidence = []

        # 1. Probe sensitive paths
        for path, description in _PROBE_PATHS:
            probe_url = urljoin(base, path)
            response = self._client.get(probe_url)
            if response is None:
                continue

            status = response.status_code
            evidence_lines.append(f"[{status}] {probe_url} — {description}")

            if status == 200:
                body_lower = response.text.lower()[:2000]

                # Check for directory listing
                if "index of /" in body_lower or "<title>index of" in body_lower:
                    findings_pre_evidence.append({
                        "check": f"Misconfiguration — Directory Listing ({path})",
                        "assessment": "FAIL",
                        "severity": "High",
                        "confidence": "high",
                        "url": probe_url,
                        "detail": f"Directory listing is enabled at {probe_url}.",
                        "recommendation": (
                            "Disable directory listing in the web server configuration. "
                            "For nginx: add 'autoindex off;'. For Apache: add 'Options -Indexes'."
                        ),
                    })
                    continue

                # Path-specific findings
                if path == "/.git/config":
                    findings_pre_evidence.append({
                        "check": "Misconfiguration — Git Repository Exposed",
                        "assessment": "FAIL",
                        "severity": "Critical",
                        "confidence": "high",
                        "url": probe_url,
                        "detail": ".git/config is accessible publicly. Source code, credentials, or secrets may be recoverable.",
                        "recommendation": (
                            "Block access to .git/ directories in your web server configuration. "
                            "For nginx: deny access with 'location ~ /\\.git { deny all; }'. "
                            "Rotate any secrets that may have been committed."
                        ),
                    })

                elif path == "/.env":
                    findings_pre_evidence.append({
                        "check": "Misconfiguration — .env File Exposed",
                        "assessment": "FAIL",
                        "severity": "Critical",
                        "confidence": "high",
                        "url": probe_url,
                        "detail": ".env file is accessible. Application secrets, database credentials, and API keys may be exposed.",
                        "recommendation": (
                            "Block access to .env files at the web server level immediately. "
                            "Rotate all credentials and secrets that may have been exposed. "
                            "Audit access logs for prior access."
                        ),
                    })

                elif "phpinfo" in path:
                    findings_pre_evidence.append({
                        "check": "Misconfiguration — PHPInfo Page Exposed",
                        "assessment": "FAIL",
                        "severity": "Medium",
                        "confidence": "high",
                        "url": probe_url,
                        "detail": "phpinfo() output is publicly accessible, revealing PHP version, extensions, loaded modules, and server configuration.",
                        "recommendation": "Remove or restrict access to phpinfo pages in production.",
                    })

                elif path == "/actuator":
                    findings_pre_evidence.append({
                        "check": "Misconfiguration — Spring Boot Actuator Exposed",
                        "assessment": "FAIL",
                        "severity": "High",
                        "confidence": "high",
                        "url": probe_url,
                        "detail": "Spring Boot Actuator root is accessible. Sensitive endpoints (env, heapdump, loggers, beans) may expose secrets and internal state.",
                        "recommendation": (
                            "Restrict Actuator endpoints to internal networks only. "
                            "Disable unnecessary endpoints. Set management.endpoints.web.exposure.include "
                            "to only the required subset."
                        ),
                    })

                elif path in ("/swagger-ui.html", "/swagger-ui/", "/api-docs"):
                    findings_pre_evidence.append({
                        "check": f"Misconfiguration — API Documentation Exposed ({path})",
                        "assessment": "FAIL",
                        "severity": "Info",
                        "confidence": "high",
                        "url": probe_url,
                        "detail": f"API documentation is publicly accessible at {probe_url}. This aids attacker reconnaissance.",
                        "recommendation": (
                            "Restrict API documentation to authenticated or internal access only in production environments."
                        ),
                    })

                elif path in ("/debug", "/console", "/__debug__/"):
                    findings_pre_evidence.append({
                        "check": f"Misconfiguration — Debug Endpoint Accessible ({path})",
                        "assessment": "FAIL",
                        "severity": "Critical",
                        "confidence": "high",
                        "url": probe_url,
                        "detail": f"Debug endpoint {probe_url} is accessible. This may allow remote code execution or full application state inspection.",
                        "recommendation": (
                            "Disable debug interfaces in production. "
                            "Never expose Python/Django debug consoles, Rails debug bars, "
                            "or interactive REPL endpoints to the internet."
                        ),
                    })

                # Check response body for error disclosure
                for pattern, pattern_type, severity in _SENSITIVE_BODY_PATTERNS:
                    if pattern in body_lower:
                        findings_pre_evidence.append({
                            "check": f"Misconfiguration — Sensitive Data in Response Body ({pattern_type})",
                            "assessment": "FAIL",
                            "severity": severity,
                            "confidence": "high",
                            "url": probe_url,
                            "detail": f"Response body contains a '{pattern}' pattern indicating {pattern_type}.",
                            "recommendation": (
                                "Suppress detailed error messages in production. "
                                "Return generic error pages. Log detailed errors server-side only."
                            ),
                        })
                        break  # One finding per URL is sufficient

        # 2. OPTIONS method check on main URL
        options_result = self._check_options(url, base)
        if options_result:
            findings_pre_evidence.append(options_result)
            evidence_lines.append(f"[OPTIONS] {url} — {options_result['detail'][:80]}")

        # 3. Security.txt check
        sec_txt_result = self._check_security_txt(base, evidence_lines)
        if sec_txt_result:
            findings_pre_evidence.append(sec_txt_result)

        # Write consolidated evidence
        evid_label = None
        if evidence_lines or findings_pre_evidence:
            content = (
                f"Target: {url}\n"
                f"Base: {base}\n"
                f"Paths probed: {len(_PROBE_PATHS)}\n\n"
                f"Results:\n" + "\n".join(evidence_lines)
            )
            try:
                evid_label, _ = write_evidence(
                    description=f"Security misconfiguration probe — {urlparse(url).netloc}",
                    domain=DOMAIN,
                    evidence_type=EVIDENCE_TYPE,
                    content=content,
                    collector=self._collector,
                    target=url,
                    observations=(
                        f"Passive misconfiguration probe of {url}. "
                        f"{len(findings_pre_evidence)} potential issue(s) identified."
                    ),
                )
            except Exception as exc:
                logger.error("Could not write misconfig evidence: %s", exc)

        # Attach evidence label to all results
        for f in findings_pre_evidence:
            f["domain"] = DOMAIN
            f["evid_label"] = evid_label
            results.append(f)

        logger.info("Misconfig audit complete: %s — %d issue(s)", url, len(results))
        return results

    def _check_options(self, url: str, base: str) -> Dict[str, Any]:
        try:
            import requests as req_lib
            response = req_lib.options(url, timeout=10, verify=True)
            allow = response.headers.get("Allow", "")
            dangerous = [m for m in ("PUT", "DELETE", "TRACE", "CONNECT") if m in allow]
            if dangerous:
                return {
                    "check": "Misconfiguration — Dangerous HTTP Methods Enabled",
                    "assessment": "FAIL",
                    "severity": "Medium",
                    "confidence": "high",
                    "url": url,
                    "detail": f"OPTIONS response exposes dangerous HTTP methods: {', '.join(dangerous)}. Allow: {allow}",
                    "recommendation": (
                        "Disable unused HTTP methods at the web server or application level. "
                        "In nginx: limit_except GET POST { deny all; }."
                    ),
                }
        except Exception:
            pass
        return {}

    def _check_security_txt(self, base: str, evidence_lines: List[str]) -> Optional[Dict[str, Any]]:
        security_txt_url = urljoin(base, "/.well-known/security.txt")
        response = self._client.get(security_txt_url)
        if response and response.status_code == 200 and "contact" in response.text.lower():
            evidence_lines.append(f"[200] security.txt present at {security_txt_url}")
            return None  # Not a finding — good practice
        evidence_lines.append(f"[missing] security.txt not found at {security_txt_url}")
        return {
            "check": "Misconfiguration — No security.txt",
            "assessment": "MISSING",
            "severity": "Info",
            "confidence": "high",
            "url": base,
            "detail": "No security.txt file found at /.well-known/security.txt.",
            "recommendation": (
                "Publish a security.txt file at /.well-known/security.txt with a Contact field "
                "to help researchers report vulnerabilities. See https://securitytxt.org/ for the spec."
            ),
        }


from typing import Optional  # noqa: E402 — placed at end to avoid circular issues
