"""
input_validation_audit.py — Input validation and injection risk audit tool.

PASSIVE mode (default):
- Inventories forms and input fields from crawler data
- Notes parameters that are commonly injection-prone
- Identifies server-side rendering patterns that may indicate XSS risk
- Documents review gaps requiring active testing

ACTIVE mode (requires explicit active testing authorization):
- NOT IMPLEMENTED — active payload injection is out of scope for this module
- See safety-authorization-rules.md Rule 3

This tool produces REVIEW GAP findings for all active validation requirements.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from src.parsers.html_parser import HtmlForm, PageInventory
from src.policies.authorization import AuthorizationGrant
from src.utils.evidence_writer import write_evidence

logger = logging.getLogger(__name__)

DOMAIN = "Input Validation"
EVIDENCE_TYPE = "Tool Output"

# Parameter names commonly associated with injection vulnerabilities
_RISKY_PARAM_NAMES = {
    "query", "q", "search", "id", "user_id", "uid", "file", "path",
    "url", "redirect", "return", "next", "cmd", "command", "exec",
    "sql", "filter", "order", "sort", "page", "template", "include",
    "src", "load", "data", "input", "text", "name", "email",
}

# Input types that commonly receive user data
_USER_INPUT_TYPES = {"text", "email", "password", "search", "url", "textarea", "hidden", "number"}

# Patterns suggesting server-side rendering (not SPAs)
_SSR_PATTERNS = [
    re.compile(r"\{\{.*?\}\}", re.DOTALL),     # Handlebars / Jinja2 / Django template
    re.compile(r"<%.*?%>", re.DOTALL),          # ERB / EJS / ASP
    re.compile(r"\$\{.*?\}", re.DOTALL),        # Template literals / Thymeleaf
]


class InputValidationAudit:
    """Passive input validation and injection risk identification tool."""

    def __init__(self, collector: str, grant: Optional[AuthorizationGrant] = None) -> None:
        self._collector = collector
        self._grant = grant

    def run(self, url: str, page_inventories: List[PageInventory] = None) -> List[Dict[str, Any]]:
        """
        Assess input surfaces from crawled page data.

        page_inventories: output from Crawler.crawl() — a list of PageInventory objects.
        If None, a review gap is returned noting that crawl data is required.
        """
        logger.info("Input validation audit starting: %s", url)
        results = []

        if not page_inventories:
            results.append({
                "check": "Input Validation — No Crawl Data Available",
                "assessment": "REVIEW_GAP",
                "severity": "High",
                "confidence": "low",
                "url": url,
                "detail": (
                    "[REVIEW GAP] No page inventory data was provided. "
                    "Run the crawler first to discover forms and input fields."
                ),
                "recommendation": "Run the crawler workflow before input validation assessment.",
                "domain": DOMAIN,
                "evid_label": None,
            })
            return results

        all_forms: List[Dict] = []
        risky_params: List[Dict] = []
        total_inputs = 0

        for page in page_inventories:
            for form in page.forms:
                form_record = {
                    "page": page.url,
                    "action": form.action,
                    "method": form.method,
                    "inputs": form.inputs,
                }
                all_forms.append(form_record)

                for inp in form.inputs:
                    total_inputs += 1
                    input_name = (inp.get("name") or "").lower()
                    input_type = (inp.get("type") or "text").lower()

                    if input_name in _RISKY_PARAM_NAMES or input_type in _USER_INPUT_TYPES:
                        risky_params.append({
                            "url": page.url,
                            "form_action": form.action,
                            "method": form.method,
                            "param_name": inp.get("name", ""),
                            "param_type": input_type,
                        })

        # Write evidence
        forms_summary = "\n".join(
            f"  [{f['method']}] {f['action']} on {f['page']} — {len(f['inputs'])} input(s)"
            for f in all_forms[:20]
        ) or "  (none found)"

        risky_summary = "\n".join(
            f"  {r['param_name']} ({r['param_type']}) in {r['method']} {r['form_action']}"
            for r in risky_params[:20]
        ) or "  (none identified)"

        content = (
            f"Target: {url}\n"
            f"Pages with forms: {sum(1 for p in page_inventories if p.forms)}\n"
            f"Total forms: {len(all_forms)}\n"
            f"Total input fields: {total_inputs}\n"
            f"Risk-relevant parameters: {len(risky_params)}\n\n"
            f"Forms discovered:\n{forms_summary}\n\n"
            f"Risk-relevant parameters:\n{risky_summary}\n\n"
            "[REVIEW GAP] Active injection testing (XSS, SQLi, SSRF, command injection) "
            "requires authorized active testing. All parameters above are candidates for "
            "manual or tool-assisted active validation when authorization is confirmed."
        )

        evid_label = None
        try:
            evid_label, _ = write_evidence(
                description=f"Input surface inventory — {urlparse(url).netloc}",
                domain=DOMAIN,
                evidence_type=EVIDENCE_TYPE,
                content=content,
                collector=self._collector,
                target=url,
                observations=(
                    f"Passive input surface inventory of {url}: "
                    f"{len(all_forms)} forms, {total_inputs} inputs, "
                    f"{len(risky_params)} risk-relevant parameters identified."
                ),
            )
        except Exception as exc:
            logger.error("Could not write input validation evidence: %s", exc)

        # Produce review gap findings
        if risky_params:
            results.append({
                "check": "Input Validation — Injection-Prone Parameters Identified (Review Gap)",
                "assessment": "REVIEW_GAP",
                "severity": "High",
                "confidence": "medium",
                "url": url,
                "detail": (
                    f"{len(risky_params)} potentially injection-prone parameter(s) identified across "
                    f"{len(all_forms)} form(s). Confirmed injection vulnerabilities require active testing. "
                    f"Example parameters: {', '.join(r['param_name'] for r in risky_params[:5])}."
                ),
                "recommendation": (
                    "[REQUIRES AUTHORIZED ACTIVE TESTING] Test each identified parameter for: "
                    "reflected XSS (submit <script>), SQL injection (submit single quote), "
                    "SSRF (submit external URL), and command injection (submit shell metacharacters). "
                    "Implement input validation, output encoding, parameterized queries, "
                    "and CSP to mitigate injection risks."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })

        # File upload surface
        file_inputs = [
            r for r in risky_params
            if r["param_type"] == "file"
        ]
        if file_inputs:
            results.append({
                "check": "Input Validation — File Upload Inputs Present (Review Gap)",
                "assessment": "REVIEW_GAP",
                "severity": "High",
                "confidence": "medium",
                "url": url,
                "detail": (
                    f"{len(file_inputs)} file upload input(s) detected. "
                    "File upload abuse (malicious file upload, path traversal) requires active validation."
                ),
                "recommendation": (
                    "Validate file type server-side (not just Content-Type header). "
                    "Store uploads outside the web root. "
                    "Scan uploaded files for malware. "
                    "Restrict uploadable file extensions to an explicit allowlist."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })

        logger.info("Input validation audit complete: %s — %d finding(s)", url, len(results))
        return results
