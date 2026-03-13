"""
rbac_audit.py — Authorization, RBAC, and IDOR passive audit tool.

Passive observations:
- Admin/privileged paths accessible without authentication
- Role-based path patterns
- Parameter-based object references in URLs (potential IDOR)

Authenticated observations (requires authorized test accounts):
- Role matrix validation
- Horizontal privilege escalation (user A accessing user B's objects)
- Vertical privilege escalation (standard user accessing admin functions)

NOTE: IDOR exploitation (attempting to access another user's data by substituting
object IDs) is ACTIVE TESTING and requires explicit active testing authorization
per safety-authorization-rules.md Rule 3. This tool performs PASSIVE observation only.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List
from urllib.parse import urlparse

from src.utils.evidence_writer import write_evidence
from src.utils.http_client import HttpClient

logger = logging.getLogger(__name__)

DOMAIN = "Authorization"
EVIDENCE_TYPE = "HTTP Capture"

# Privileged path patterns
_PRIVILEGED_PATTERNS = [
    (re.compile(r"/admin(/|$)", re.IGNORECASE), "Admin panel"),
    (re.compile(r"/dashboard(/|$)", re.IGNORECASE), "Dashboard"),
    (re.compile(r"/management(/|$)", re.IGNORECASE), "Management interface"),
    (re.compile(r"/superuser(/|$)", re.IGNORECASE), "Superuser area"),
    (re.compile(r"/staff(/|$)", re.IGNORECASE), "Staff area"),
    (re.compile(r"/internal(/|$)", re.IGNORECASE), "Internal endpoint"),
]

# Object reference patterns (potential IDOR surface)
_OBJECT_REF_PATTERNS = [
    re.compile(r"/(?:user|account|profile|order|invoice|document|file|record)s?/(\d+)"),
    re.compile(r"[?&](?:user_?id|account_?id|id|uid|object_?id)=(\d+)"),
    re.compile(r"/api/v\d+/(?:user|resource|item)s?/([a-zA-Z0-9_-]+)"),
]


class RbacAudit:
    """Authorization and RBAC passive audit tool."""

    def __init__(self, http_client: HttpClient, collector: str) -> None:
        self._client = http_client
        self._collector = collector

    def run(self, url: str, crawl_pages: List[str] = None) -> List[Dict[str, Any]]:
        """
        Passive RBAC/authorization observations.

        crawl_pages: list of discovered URLs from the crawler to assess for
                     privileged path access and IDOR surface.
        Returns finding-ready result dicts.
        """
        logger.info("RBAC audit starting: %s", url)
        results = []
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"

        evidence_lines = []
        findings_pre_evidence = []

        pages_to_assess = crawl_pages or [url]

        # Assess each discovered URL
        privileged_unauthenticated = []
        idor_surface = []

        for page_url in pages_to_assess:
            page_path = urlparse(page_url).path

            # Privileged path check
            for pattern, label in _PRIVILEGED_PATTERNS:
                if pattern.search(page_path):
                    response = self._client.get(page_url)
                    if response and response.status_code == 200:
                        # Accessible without authentication
                        privileged_unauthenticated.append((page_url, label, response.status_code))
                        evidence_lines.append(f"[{response.status_code}] Privileged path accessible: {page_url} ({label})")
                    else:
                        status = response.status_code if response else "unreachable"
                        evidence_lines.append(f"[{status}] Privileged path (protected): {page_url} ({label})")

            # IDOR surface identification
            for pattern in _OBJECT_REF_PATTERNS:
                match = pattern.search(page_url)
                if match:
                    idor_surface.append((page_url, match.group(0)))
                    evidence_lines.append(f"[IDOR surface] Object reference in URL: {page_url}")
                    break

        # Generate findings for unauthenticated privileged access
        for priv_url, label, status_code in privileged_unauthenticated:
            findings_pre_evidence.append({
                "check": f"Authorization — Privileged Path Accessible Without Authentication ({label})",
                "assessment": "FAIL",
                "severity": "High",
                "confidence": "high",
                "url": priv_url,
                "detail": (
                    f"The {label} path at {priv_url} returned HTTP {status_code} "
                    "without requiring authentication."
                ),
                "recommendation": (
                    f"Enforce authentication and role-based access control on {priv_url}. "
                    "Verify that unauthenticated requests are redirected to the login page "
                    "or receive a 401/403 response."
                ),
            })

        # IDOR review gaps
        if idor_surface:
            idor_examples = [url for url, _ in idor_surface[:5]]
            findings_pre_evidence.append({
                "check": "Authorization — Object Reference Parameters Identified (IDOR Surface)",
                "assessment": "REVIEW_GAP",
                "severity": "High",
                "confidence": "medium",
                "url": url,
                "detail": (
                    f"Object reference patterns (numeric IDs, resource IDs) found in {len(idor_surface)} URL(s). "
                    "These are potential IDOR vectors: " + ", ".join(idor_examples[:3]) + ". "
                    "[REVIEW GAP] Confirming IDOR requires testing with a second test account — "
                    "active testing authorization required."
                ),
                "recommendation": (
                    "[REQUIRES AUTHORIZED ACTIVE TESTING] With two test accounts (A and B), "
                    "attempt to access B's object IDs while authenticated as A. "
                    "Implement server-side ownership checks for all object references. "
                    "Consider opaque/UUID identifiers instead of sequential integers."
                ),
            })

        # Blanket review gap for RBAC
        findings_pre_evidence.append({
            "check": "Authorization — Role Matrix Validation (Review Gap)",
            "assessment": "REVIEW_GAP",
            "severity": "High",
            "confidence": "low",
            "url": url,
            "detail": (
                "[REVIEW GAP] Full RBAC validation requires multiple test accounts with different roles. "
                "Vertical privilege escalation (standard user accessing admin functions) cannot be "
                "confirmed without authenticated access."
            ),
            "recommendation": (
                "[REQUIRES AUTHENTICATED TESTING] Provide test accounts for each user role. "
                "Attempt to access higher-privilege functions while authenticated as a lower-privilege role. "
                "Verify that the server enforces role checks on every sensitive endpoint, not just the UI."
            ),
        })

        # Write evidence
        content = (
            f"Target: {url}\n"
            f"Pages assessed: {len(pages_to_assess)}\n"
            f"Privileged paths accessible unauthenticated: {len(privileged_unauthenticated)}\n"
            f"IDOR surface URLs identified: {len(idor_surface)}\n\n"
            f"Observations:\n" + "\n".join(f"  {line}" for line in evidence_lines)
        )

        evid_label = None
        try:
            evid_label, _ = write_evidence(
                description=f"Authorization / RBAC passive review — {urlparse(url).netloc}",
                domain=DOMAIN,
                evidence_type=EVIDENCE_TYPE,
                content=content,
                collector=self._collector,
                target=url,
                observations=(
                    f"Passive RBAC review of {url}. "
                    f"{len(privileged_unauthenticated)} privileged path(s) accessible without authentication. "
                    f"{len(idor_surface)} potential IDOR surface URL(s) identified."
                ),
            )
        except Exception as exc:
            logger.error("Could not write RBAC evidence: %s", exc)

        for f in findings_pre_evidence:
            f["domain"] = DOMAIN
            f["evid_label"] = evid_label
            results.append(f)

        logger.info("RBAC audit complete: %s — %d issue(s)", url, len(results))
        return results
