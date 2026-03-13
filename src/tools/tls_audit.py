"""
tls_audit.py — TLS/SSL passive audit tool.

Uses Python's stdlib ssl module to collect certificate and protocol details.
Does NOT enumerate cipher suites (requires active testing — explicitly labelled as review gap).

Severity mapping follows severity-rating-rules.md.
"""

import logging
import socket
import ssl
from datetime import datetime, timezone
from typing import Any, Dict, List
from urllib.parse import urlparse

from src.utils.evidence_writer import write_evidence

logger = logging.getLogger(__name__)

DOMAIN = "TLS / Certificate"
EVIDENCE_TYPE = "Tool Output"

# Days-to-expiry severity thresholds
_EXPIRY_THRESHOLDS = [
    (0, "Critical"),      # expired
    (7, "Critical"),      # expiring in ≤7 days
    (30, "High"),         # expiring in ≤30 days
    (90, "Medium"),       # expiring in ≤90 days
]

# Weak signature algorithms
_WEAK_SIG_ALGORITHMS = {"sha1withrsa", "md5withrsa", "md2withrsa", "sha1withecdsa"}


class TLSAudit:
    """Passive TLS certificate and protocol audit tool."""

    def __init__(self, collector: str, timeout: int = 15) -> None:
        self._collector = collector
        self._timeout = timeout

    def run(self, url: str) -> List[Dict[str, Any]]:
        """
        Connect to the target host via TLS and collect certificate/protocol details.

        Returns a list of result dicts for non-passing checks.
        """
        parsed = urlparse(url)
        hostname = parsed.hostname
        port = parsed.port or (443 if parsed.scheme == "https" else 80)

        if parsed.scheme != "https":
            logger.warning("TLS audit skipped for non-HTTPS URL: %s", url)
            return [{
                "check": "TLS — Scheme",
                "assessment": "FAIL",
                "severity": "High",
                "confidence": "high",
                "url": url,
                "detail": f"Target URL uses HTTP scheme, not HTTPS. TLS is not in use.",
                "recommendation": (
                    "Migrate the application to HTTPS. Configure HTTP→HTTPS redirects "
                    "and set HSTS to enforce HTTPS going forward."
                ),
                "domain": DOMAIN,
                "evid_label": None,
            }]

        logger.info("TLS audit starting: %s:%d", hostname, port)

        ctx = ssl.create_default_context()
        results = []

        try:
            with socket.create_connection((hostname, port), timeout=self._timeout) as sock:
                with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                    protocol = ssock.version()
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()

        except ssl.SSLCertVerificationError as exc:
            logger.error(
                "TLS certificate verification failed for %s: %s\n"
                "Remediation: The certificate may be self-signed, expired, or CN/SAN mismatch. "
                "Investigate and replace with a valid certificate from a trusted CA.",
                hostname,
                exc,
            )
            return [{
                "check": "TLS — Certificate Verification",
                "assessment": "FAIL",
                "severity": "Critical",
                "confidence": "high",
                "url": url,
                "detail": f"TLS certificate verification failed: {exc}",
                "recommendation": (
                    "Obtain and install a valid certificate from a trusted Certificate Authority. "
                    "Verify the certificate CN/SAN matches the hostname and has not expired."
                ),
                "domain": DOMAIN,
                "evid_label": None,
            }]

        except (socket.timeout, ConnectionRefusedError, OSError) as exc:
            logger.error(
                "TLS connection failed for %s:%d: %s\n"
                "Remediation: Verify the host is reachable and port %d is open.",
                hostname,
                port,
                exc,
                port,
            )
            return [{"error": str(exc), "url": url}]

        # ── Parse certificate fields ──────────────────────────────────────────
        subject = dict(x[0] for x in cert.get("subject", []))
        cn = subject.get("commonName", "unknown")
        issuer = dict(x[0] for x in cert.get("issuer", []))
        issuer_cn = issuer.get("commonName", "unknown")
        issuer_org = issuer.get("organizationName", "unknown")

        not_after_str = cert.get("notAfter", "")
        not_before_str = cert.get("notBefore", "")

        san_list = []
        for san_type, san_value in cert.get("subjectAltName", []):
            san_list.append(f"{san_type}: {san_value}")

        sig_alg = cert.get("signatureAlgorithm", "unknown")

        # ── Days to expiry ─────────────────────────────────────────────────────
        days_to_expiry = None
        not_after_parsed = None
        if not_after_str:
            try:
                not_after_parsed = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z")
                not_after_parsed = not_after_parsed.replace(tzinfo=timezone.utc)
                now = datetime.now(tz=timezone.utc)
                days_to_expiry = (not_after_parsed - now).days
            except ValueError:
                logger.warning("Could not parse certificate notAfter date: %s", not_after_str)

        # ── Build evidence content ─────────────────────────────────────────────
        evidence_content = (
            f"Host: {hostname}:{port}\n"
            f"Negotiated Protocol: {protocol}\n"
            f"Cipher Suite: {cipher[0] if cipher else 'unknown'} "
            f"(bits: {cipher[2] if cipher else 'unknown'})\n\n"
            f"Certificate Subject CN: {cn}\n"
            f"Subject Alternative Names:\n"
            + ("\n".join(f"  {s}" for s in san_list) or "  (none)")
            + f"\n\nIssuer: {issuer_cn} ({issuer_org})\n"
            f"Valid From: {not_before_str}\n"
            f"Valid Until: {not_after_str}\n"
            f"Days to Expiry: {days_to_expiry if days_to_expiry is not None else 'unknown'}\n"
            f"Signature Algorithm: {sig_alg}\n\n"
            f"[REVIEW GAP] Cipher suite enumeration requires authorized active TLS scanning "
            f"(e.g., testssl.sh or SSL Labs API). Only the negotiated cipher is shown above."
        )

        observations = (
            f"TLS connection to {hostname}:{port} successful. "
            f"Protocol: {protocol}. "
            f"Certificate expires: {not_after_str} "
            f"({days_to_expiry} days remaining)." if days_to_expiry is not None
            else f"Certificate expiry could not be determined."
        )

        evid_label, _ = write_evidence(
            description=f"TLS certificate and protocol details — {hostname}",
            domain=DOMAIN,
            evidence_type=EVIDENCE_TYPE,
            content=evidence_content,
            collector=self._collector,
            target=url,
            observations=observations,
        )

        # ── Evaluate checks ────────────────────────────────────────────────────

        # Protocol version
        weak_protocols = {"TLSv1", "TLSv1.1", "SSLv2", "SSLv3"}
        if protocol in weak_protocols:
            results.append({
                "check": "TLS — Protocol Version",
                "assessment": "WEAK",
                "severity": "Medium",
                "confidence": "high",
                "url": url,
                "detail": f"Deprecated TLS version negotiated: {protocol}.",
                "recommendation": (
                    "Disable TLS 1.0 and TLS 1.1. Support only TLS 1.2 and TLS 1.3. "
                    "Update server TLS configuration (e.g., ssl_protocols TLSv1.2 TLSv1.3 in nginx)."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })

        # Certificate expiry
        if days_to_expiry is not None:
            expiry_severity = None
            if days_to_expiry <= 0:
                expiry_severity = "Critical"
                detail = f"Certificate has EXPIRED ({abs(days_to_expiry)} days ago). {not_after_str}"
            elif days_to_expiry <= 7:
                expiry_severity = "Critical"
                detail = f"Certificate expires in {days_to_expiry} days ({not_after_str})."
            elif days_to_expiry <= 30:
                expiry_severity = "High"
                detail = f"Certificate expires in {days_to_expiry} days ({not_after_str})."
            elif days_to_expiry <= 90:
                expiry_severity = "Medium"
                detail = f"Certificate expires in {days_to_expiry} days ({not_after_str})."

            if expiry_severity:
                results.append({
                    "check": "TLS — Certificate Expiry",
                    "assessment": "FAIL",
                    "severity": expiry_severity,
                    "confidence": "high",
                    "url": url,
                    "detail": detail,
                    "recommendation": (
                        "Renew the TLS certificate before it expires. "
                        "Implement automated certificate renewal (e.g., Let's Encrypt + certbot). "
                        "Set up monitoring alerts at 30, 14, and 7 days before expiry."
                    ),
                    "domain": DOMAIN,
                    "evid_label": evid_label,
                })

        # Weak signature algorithm
        if sig_alg.lower().replace(" ", "") in _WEAK_SIG_ALGORITHMS:
            results.append({
                "check": "TLS — Weak Signature Algorithm",
                "assessment": "FAIL",
                "severity": "Critical",
                "confidence": "high",
                "url": url,
                "detail": f"Certificate uses a weak/deprecated signature algorithm: {sig_alg}.",
                "recommendation": (
                    "Replace the certificate with one signed using SHA-256 or SHA-384 "
                    "(e.g., SHA256withRSA or ECDSA with SHA-256)."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })

        # Cipher suite review gap note (always present — informational)
        results.append({
            "check": "TLS — Cipher Suite Enumeration",
            "assessment": "REVIEW_GAP",
            "severity": "Info",
            "confidence": "low",
            "url": url,
            "detail": (
                f"Only the negotiated cipher suite is visible from a passive connection: "
                f"{cipher[0] if cipher else 'unknown'}. "
                "Full cipher suite enumeration requires authorized active TLS scanning."
            ),
            "recommendation": (
                "[REQUIRES AUTHORIZED ACTIVE TESTING] Run testssl.sh or SSL Labs API "
                "to enumerate all supported cipher suites and identify weak ciphers."
            ),
            "domain": DOMAIN,
            "evid_label": evid_label,
        })

        logger.info(
            "TLS audit complete: %s — %d issue(s) found",
            url,
            len([r for r in results if r.get("severity") not in ("Info", None)]),
        )
        return results
