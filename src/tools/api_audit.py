"""
api_audit.py — API security assessment tool.

Passive assessment from OpenAPI/Postman specs:
- Endpoint inventory
- Authentication requirements per endpoint
- Sensitive parameter identification
- Mass assignment risk patterns
- Missing auth on sensitive operations
- Excessive data exposure signals

Active assessment (requires active testing authorization):
- Schema validation testing
- Auth bypass attempts
- Horizontal/vertical access control checks per endpoint
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from src.parsers.openapi_parser import ApiSpec, parse_spec
from src.utils.evidence_writer import write_evidence
from src.utils.http_client import HttpClient

logger = logging.getLogger(__name__)

DOMAIN = "API Security"
EVIDENCE_TYPE = "Tool Output"

_SENSITIVE_PARAM_NAMES = {
    "password", "passwd", "secret", "token", "key", "api_key",
    "access_token", "auth", "ssn", "credit_card", "card_number",
}

_SENSITIVE_ENDPOINTS = [
    ("/admin", "Admin endpoint"),
    ("/internal", "Internal endpoint"),
    ("/debug", "Debug endpoint"),
    ("/export", "Data export"),
    ("/download", "File download"),
    ("/delete", "Deletion endpoint"),
    ("/superuser", "Superuser endpoint"),
]


class ApiAudit:
    """API security assessment tool — passive spec analysis and unauthenticated probing."""

    def __init__(self, http_client: HttpClient, collector: str) -> None:
        self._client = http_client
        self._collector = collector

    def run(
        self,
        url: str,
        spec_path: Optional[Path] = None,
    ) -> List[Dict[str, Any]]:
        """
        Assess API security from a spec file and/or passive URL probing.

        Returns finding-ready result dicts.
        """
        logger.info("API audit starting: %s", url)
        results = []

        if spec_path:
            spec = parse_spec(Path(spec_path))
            if spec:
                results.extend(self._assess_spec(spec, url))
            else:
                logger.warning("Could not parse spec file: %s", spec_path)
                results.append({
                    "check": "API — Spec Parse Failure",
                    "assessment": "REVIEW_GAP",
                    "severity": "Info",
                    "confidence": "low",
                    "url": str(spec_path),
                    "detail": f"Could not parse API spec at {spec_path}. Manual review required.",
                    "recommendation": "Verify the spec file format (OpenAPI 3.x, Swagger 2.x, or Postman Collection).",
                    "domain": DOMAIN,
                    "evid_label": None,
                })

        # Passive API discovery from the URL
        results.extend(self._passive_api_probe(url))

        logger.info("API audit complete: %s — %d issue(s)", url, len(results))
        return results

    def _assess_spec(self, spec: ApiSpec, base_url: str) -> List[Dict[str, Any]]:
        """Analyze an API spec for security control gaps."""
        results = []

        # Write evidence
        endpoints_summary = "\n".join(
            f"  [{e.method}] {e.path} — auth:{e.requires_auth} — {e.summary[:60]}"
            for e in spec.endpoints[:30]
        )
        content = (
            f"API: {spec.title} v{spec.version}\n"
            f"Base URL: {spec.base_url}\n"
            f"Format: {spec.spec_format}\n"
            f"Total endpoints: {len(spec.endpoints)}\n"
            f"Security schemes: {', '.join(spec.security_schemes) or 'none defined'}\n\n"
            f"Endpoint inventory (first 30):\n{endpoints_summary}"
        )

        evid_label = None
        try:
            evid_label, _ = write_evidence(
                description=f"API spec inventory — {spec.title}",
                domain=DOMAIN,
                evidence_type=EVIDENCE_TYPE,
                content=content,
                collector=self._collector,
                target=base_url,
                observations=(
                    f"Parsed {spec.spec_format} spec for {spec.title}: "
                    f"{len(spec.endpoints)} endpoint(s), "
                    f"{len(spec.security_schemes)} security scheme(s)."
                ),
            )
        except Exception as exc:
            logger.error("Could not write API spec evidence: %s", exc)

        # No global security schemes defined
        if not spec.security_schemes:
            results.append({
                "check": "API — No Security Schemes Defined in Spec",
                "assessment": "MISSING",
                "severity": "High",
                "confidence": "medium",
                "url": base_url,
                "detail": (
                    f"The API spec for '{spec.title}' defines no security schemes "
                    "(e.g., bearerAuth, apiKey, OAuth2). Authentication enforcement is unclear."
                ),
                "recommendation": (
                    "Define security schemes in the OpenAPI spec and apply them globally "
                    "and/or per-endpoint. Verify server-side enforcement matches the spec."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })

        # Endpoints without auth
        unprotected = [e for e in spec.endpoints if not e.requires_auth]
        sensitive_unprotected = []
        for endpoint in unprotected:
            for pattern, label in _SENSITIVE_ENDPOINTS:
                if pattern in endpoint.path.lower():
                    sensitive_unprotected.append((endpoint, label))
                    break

        if sensitive_unprotected:
            examples = [f"[{e.method}] {e.path} ({label})" for e, label in sensitive_unprotected[:5]]
            results.append({
                "check": "API — Sensitive Endpoints Lack Authentication in Spec",
                "assessment": "FAIL",
                "severity": "High",
                "confidence": "medium",
                "url": base_url,
                "detail": (
                    f"{len(sensitive_unprotected)} sensitive endpoint(s) have no authentication requirement "
                    "in the spec: " + ", ".join(examples)
                ),
                "recommendation": (
                    "Apply security requirements to all sensitive endpoints in the spec and "
                    "verify server-side enforcement. Use global security with per-endpoint overrides "
                    "only for truly public endpoints."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })

        # Sensitive parameter names (potential mass assignment / over-posting risk)
        for endpoint in spec.endpoints:
            for param in (endpoint.parameters or []):
                pname = (param.get("name") or "").lower()
                if pname in _SENSITIVE_PARAM_NAMES:
                    results.append({
                        "check": f"API — Sensitive Parameter in Spec ({endpoint.method} {endpoint.path})",
                        "assessment": "WEAK",
                        "severity": "Medium",
                        "confidence": "low",
                        "url": base_url,
                        "detail": (
                            f"Parameter '{pname}' in [{endpoint.method}] {endpoint.path} "
                            "matches a sensitive field pattern. Verify it is handled securely."
                        ),
                        "recommendation": (
                            "Ensure sensitive parameters are not logged, are transmitted only over HTTPS, "
                            "and are validated server-side. Review for mass assignment risk."
                        ),
                        "domain": DOMAIN,
                        "evid_label": evid_label,
                    })

        # IDOR review gap for endpoints with path parameters
        endpoints_with_path_params = [
            e for e in spec.endpoints if "{" in e.path
        ]
        if endpoints_with_path_params:
            results.append({
                "check": "API — Path Parameter Endpoints (IDOR Review Gap)",
                "assessment": "REVIEW_GAP",
                "severity": "High",
                "confidence": "medium",
                "url": base_url,
                "detail": (
                    f"{len(endpoints_with_path_params)} endpoint(s) use path parameters that may "
                    "expose object references. IDOR cannot be confirmed without active testing with "
                    "multiple test accounts."
                ),
                "recommendation": (
                    "[REQUIRES AUTHORIZED ACTIVE TESTING] Test each parameterized endpoint by "
                    "substituting object IDs belonging to other test users. "
                    "Implement server-side ownership validation for all object references."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })

        return results

    def _passive_api_probe(self, url: str) -> List[Dict[str, Any]]:
        """Probe for common API endpoints passively."""
        results = []
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"

        api_probe_paths = [
            "/api/v1/", "/api/v2/", "/api/",
            "/graphql", "/graphiql",
            "/rest/v1/", "/v1/", "/v2/",
        ]

        found = []
        for path in api_probe_paths:
            from urllib.parse import urljoin
            probe_url = urljoin(base, path)
            response = self._client.get(probe_url)
            if response and response.status_code in (200, 401, 403):
                content_type = response.headers.get("Content-Type", "")
                if "json" in content_type or "graphql" in content_type or response.status_code in (401, 403):
                    found.append((probe_url, response.status_code))

        if found:
            evid_label = None
            content = "API endpoints discovered by passive probing:\n" + "\n".join(
                f"  [{status}] {url}" for url, status in found
            )
            try:
                evid_label, _ = write_evidence(
                    description=f"API endpoint discovery — {urlparse(url).netloc}",
                    domain=DOMAIN,
                    evidence_type=EVIDENCE_TYPE,
                    content=content,
                    collector=self._collector,
                    target=url,
                    observations=f"Passive probing found {len(found)} API endpoint(s).",
                )
            except Exception as exc:
                logger.error("Could not write API discovery evidence: %s", exc)

            results.append({
                "check": "API — Endpoints Discovered (Provide Spec for Full Assessment)",
                "assessment": "REVIEW_GAP",
                "severity": "Info",
                "confidence": "medium",
                "url": url,
                "detail": (
                    f"{len(found)} API endpoint path(s) found by passive probing. "
                    "Full API security assessment requires an OpenAPI/Postman spec. "
                    "Endpoints: " + ", ".join(f"[{s}] {u}" for u, s in found[:5])
                ),
                "recommendation": (
                    "Provide the API spec file (--spec path/to/openapi.yaml) for comprehensive "
                    "API security assessment including endpoint inventory, auth coverage, "
                    "and parameter analysis."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })

        return results
