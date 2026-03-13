"""
dependency_audit.py — Dependency CVE audit tool using the OSV.dev API.

Queries the OSV (Open Source Vulnerabilities) API for known vulnerabilities
in parsed package manifests. No API key required.

OSV API: https://api.osv.dev/v1/querybatch
Supports: PyPI, npm, Go, Maven, RubyGems, Packagist
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

from src.config.settings import OSV_API_BASE_URL, OSV_BATCH_SIZE, OSV_INTER_BATCH_DELAY
from src.parsers.manifest import parse_manifest
from src.utils.evidence_writer import write_evidence

logger = logging.getLogger(__name__)

DOMAIN = "Dependencies"
EVIDENCE_TYPE = "Tool Output"


class DependencyAudit:
    """Dependency vulnerability audit tool via OSV.dev API."""

    def __init__(self, collector: str, timeout: int = 30) -> None:
        self._collector = collector
        self._timeout = timeout

    def run(self, manifest_path: Path) -> List[Dict[str, Any]]:
        """
        Parse a dependency manifest and query OSV.dev for known CVEs.

        Returns a list of finding-ready result dicts, one per vulnerable package.
        """
        manifest_path = Path(manifest_path)
        logger.info("Dependency audit starting: %s", manifest_path)

        packages = parse_manifest(manifest_path)
        if not packages:
            logger.warning(
                "No packages parsed from %s. "
                "Remediation: Check the manifest format is supported and the file is populated.",
                manifest_path,
            )
            return [{
                "error": f"No packages could be parsed from {manifest_path.name}",
                "url": str(manifest_path),
            }]

        logger.info("Querying OSV.dev for %d packages from %s...", len(packages), manifest_path.name)
        vulns = self._query_osv(packages)

        if not vulns:
            logger.info("No vulnerabilities found for %s", manifest_path.name)
            self._write_evidence(manifest_path, packages, [])
            return []

        evid_label = self._write_evidence(manifest_path, packages, vulns)
        results = []

        for pkg_name, pkg_version, ecosystem, osv_vuln in vulns:
            severity, cvss = self._map_severity(osv_vuln)
            cve_ids = [a for a in osv_vuln.get("aliases", []) if a.startswith("CVE-")]
            cve_str = ", ".join(cve_ids) if cve_ids else osv_vuln.get("id", "unknown")
            summary = osv_vuln.get("summary", "No summary available")

            fixed_versions = []
            for affected in osv_vuln.get("affected", []):
                for rng in affected.get("ranges", []):
                    for ev in rng.get("events", []):
                        if "fixed" in ev:
                            fixed_versions.append(ev["fixed"])

            fix_str = ", ".join(fixed_versions) if fixed_versions else "No fix version listed — check OSV record"

            results.append({
                "check": f"Dependency Vulnerability — {pkg_name} {pkg_version}",
                "assessment": "FAIL",
                "severity": severity,
                "confidence": "high",
                "url": str(manifest_path),
                "detail": (
                    f"Package {pkg_name} {pkg_version} ({ecosystem}) has a known vulnerability: "
                    f"{cve_str} — {summary}. "
                    f"CVSS: {cvss if cvss else 'not available'}."
                ),
                "recommendation": (
                    f"Update {pkg_name} to a fixed version: {fix_str}. "
                    "Review the full OSV record and test the update in a staging environment before deploying."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })

        logger.info(
            "Dependency audit complete: %s — %d vulnerability finding(s)", manifest_path.name, len(results)
        )
        return results

    def _query_osv(
        self, packages: List[Tuple[str, str, str]]
    ) -> List[Tuple[str, str, str, Dict]]:
        """
        Query OSV.dev in batches. Returns list of (name, version, ecosystem, vuln_record).
        """
        results = []
        batches = [packages[i:i + OSV_BATCH_SIZE] for i in range(0, len(packages), OSV_BATCH_SIZE)]

        for batch_num, batch in enumerate(batches, 1):
            queries = []
            for name, version, ecosystem in batch:
                query: Dict = {"package": {"name": name, "ecosystem": ecosystem}}
                if version:
                    query["version"] = version
                queries.append(query)

            try:
                response = requests.post(
                    f"{OSV_API_BASE_URL}/querybatch",
                    json={"queries": queries},
                    timeout=self._timeout,
                )
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.ConnectionError:
                logger.error(
                    "Cannot reach OSV.dev API (batch %d/%d). "
                    "Remediation: Check network connectivity to api.osv.dev.",
                    batch_num,
                    len(batches),
                )
                break
            except requests.exceptions.Timeout:
                logger.error("OSV.dev API request timed out (batch %d/%d).", batch_num, len(batches))
                break
            except requests.exceptions.HTTPError as exc:
                logger.error("OSV.dev API HTTP error (batch %d/%d): %s", batch_num, len(batches), exc)
                break
            except Exception as exc:
                logger.error("OSV.dev API unexpected error: %s", exc)
                break

            for (name, version, ecosystem), result in zip(batch, data.get("results", [])):
                for vuln in result.get("vulns", []):
                    results.append((name, version, ecosystem, vuln))

            if batch_num < len(batches):
                time.sleep(OSV_INTER_BATCH_DELAY)

        return results

    def _map_severity(self, vuln: Dict) -> Tuple[str, Optional[str]]:
        """Map OSV severity/CVSS data to workspace severity labels."""
        cvss = None
        score = None

        for sev in vuln.get("severity", []):
            if sev.get("type") in ("CVSS_V3", "CVSS_V2"):
                cvss = sev.get("score", "")
                # Extract numeric score from vector string if present
                import re
                match = re.search(r"/AV:[^/]+.*", cvss)
                # Try to get a numeric score from the database_specific field
                break

        # Also try database_specific for numeric CVSS
        for affected in vuln.get("affected", []):
            db_specific = affected.get("database_specific", {})
            cvss_raw = db_specific.get("cvss") or db_specific.get("cvss_score")
            if cvss_raw:
                try:
                    score = float(str(cvss_raw).split("/")[0])
                    cvss = str(cvss_raw)
                except (ValueError, TypeError):
                    pass
            if score is not None:
                break

        if score is None:
            # Default to High for known CVEs with no CVSS data
            return "High", cvss

        if score >= 9.0:
            return "Critical", cvss
        if score >= 7.0:
            return "High", cvss
        if score >= 4.0:
            return "Medium", cvss
        return "Low", cvss

    def _write_evidence(
        self, manifest_path: Path, packages: List, vulns: List
    ) -> Optional[str]:
        vuln_table = "\n".join(
            f"  {name} {version} ({ecosystem}): {v.get('id', '?')} — {v.get('summary', '')[:80]}"
            for name, version, ecosystem, v in vulns
        ) or "  (none found)"

        content = (
            f"Manifest: {manifest_path}\n"
            f"Packages scanned: {len(packages)}\n"
            f"Vulnerabilities found: {len(vulns)}\n\n"
            f"Vulnerable Packages:\n{vuln_table}"
        )

        try:
            label, _ = write_evidence(
                description=f"Dependency CVE scan — {manifest_path.name}",
                domain=DOMAIN,
                evidence_type=EVIDENCE_TYPE,
                content=content,
                collector=self._collector,
                target=str(manifest_path),
                observations=(
                    f"OSV.dev API scan of {manifest_path.name} found {len(vulns)} "
                    f"vulnerability record(s) across {len(packages)} parsed packages."
                ),
            )
            return label
        except Exception as exc:
            logger.error("Could not write dependency evidence: %s", exc)
            return None
