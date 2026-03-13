"""
secrets_scan.py — Basic secrets scanning tool for filesystem paths.

Scans files for patterns that indicate hardcoded secrets:
- API keys (AWS, GCP, GitHub, Stripe, etc.)
- Passwords in configuration files
- Private keys
- Generic high-entropy strings in key-value context

This tool scans LOCAL files (source code, configs) — not network responses.
It is intended for pre-commit or CI pipeline integration.

NOTE: This is a basic regex-based scanner. For production use,
consider integrating with truffleHog, detect-secrets, or GitLeaks.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

from src.utils.evidence_writer import write_evidence

logger = logging.getLogger(__name__)

DOMAIN = "Security Misconfiguration"
EVIDENCE_TYPE = "Tool Output"

# (pattern_name, severity, regex)
_SECRET_PATTERNS: List[Tuple[str, str, re.Pattern]] = [
    ("AWS Access Key ID", "Critical", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("AWS Secret Key", "Critical", re.compile(r"(?i)aws_secret_access_key\s*[=:]\s*\S{40}")),
    ("GitHub Token", "Critical", re.compile(r"gh[ps]_[a-zA-Z0-9]{36,}")),
    ("Stripe Secret Key", "Critical", re.compile(r"sk_(live|test)_[a-zA-Z0-9]{24,}")),
    ("Stripe Publishable Key", "Low", re.compile(r"pk_(live|test)_[a-zA-Z0-9]{24,}")),
    ("Private Key Block", "Critical", re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("Generic Password Assignment", "High", re.compile(
        r'(?i)(password|passwd|pwd|secret|api_?key)\s*[=:]\s*["\'](?!\s*\$\{)[^"\']{8,}["\']'
    )),
    ("Connection String with Password", "High", re.compile(
        r"(?i)(mongodb|mysql|postgresql|redis|amqp)://[^:]+:[^@]{6,}@"
    )),
    ("Generic Bearer Token", "High", re.compile(r"(?i)bearer\s+[a-zA-Z0-9\-._~+/]{40,}")),
    ("GCP Service Account Key", "Critical", re.compile(r'"type"\s*:\s*"service_account"')),
    ("Slack Token", "High", re.compile(r"xox[baprs]-[0-9a-zA-Z]{10,}")),
    ("SendGrid API Key", "High", re.compile(r"SG\.[a-zA-Z0-9\-._]{22,}\.[a-zA-Z0-9\-._]{43,}")),
]

# File extensions to scan
_SCAN_EXTENSIONS = {
    ".py", ".js", ".ts", ".java", ".go", ".rb", ".php", ".cs",
    ".env", ".yaml", ".yml", ".json", ".xml", ".properties",
    ".conf", ".config", ".ini", ".toml", ".sh", ".bash",
}

# Paths to always skip
_SKIP_PATTERNS = {
    ".git", "__pycache__", ".venv", "venv", "node_modules",
    "dist", "build", ".pytest_cache", "*.min.js",
}


class SecretsScan:
    """Basic secrets scanner for local filesystem paths."""

    def __init__(self, collector: str) -> None:
        self._collector = collector

    def run(self, scan_path: Path) -> List[Dict[str, Any]]:
        """
        Scan a file or directory for hardcoded secrets.

        Returns finding-ready result dicts for each detected pattern.
        """
        scan_path = Path(scan_path)
        logger.info("Secrets scan starting: %s", scan_path)

        if not scan_path.exists():
            logger.error("Scan path does not exist: %s", scan_path)
            return [{"error": f"Scan path not found: {scan_path}", "url": str(scan_path)}]

        files_to_scan = self._collect_files(scan_path)
        logger.info("Scanning %d files...", len(files_to_scan))

        all_findings: List[Dict] = []
        evidence_records: List[str] = []

        for file_path in files_to_scan:
            file_findings = self._scan_file(file_path)
            for pattern_name, severity, line_num, snippet in file_findings:
                all_findings.append((str(file_path), pattern_name, severity, line_num, snippet))
                evidence_records.append(
                    f"  [{severity}] {pattern_name} in {file_path}:{line_num} — {snippet[:80]}"
                )

        # Write evidence
        content = (
            f"Scan path: {scan_path}\n"
            f"Files scanned: {len(files_to_scan)}\n"
            f"Secrets detected: {len(all_findings)}\n\n"
            f"Findings:\n" + ("\n".join(evidence_records) or "  (none found)")
        )

        evid_label = None
        try:
            evid_label, _ = write_evidence(
                description=f"Secrets scan — {scan_path.name}",
                domain=DOMAIN,
                evidence_type=EVIDENCE_TYPE,
                content=content,
                collector=self._collector,
                target=str(scan_path),
                observations=(
                    f"Basic secrets scan of {scan_path}: "
                    f"{len(files_to_scan)} files scanned, "
                    f"{len(all_findings)} potential secret(s) detected."
                ),
            )
        except Exception as exc:
            logger.error("Could not write secrets evidence: %s", exc)

        # Deduplicate by (file, pattern, severity)
        results = []
        seen = set()
        for file_path, pattern_name, severity, line_num, snippet in all_findings:
            key = (file_path, pattern_name)
            if key in seen:
                continue
            seen.add(key)

            results.append({
                "check": f"Secrets — {pattern_name} Detected",
                "assessment": "FAIL",
                "severity": severity,
                "confidence": "medium",
                "url": file_path,
                "detail": (
                    f"Potential hardcoded secret ({pattern_name}) detected in {file_path} "
                    f"at line {line_num}. Pattern: {snippet[:80]}"
                ),
                "recommendation": (
                    f"Remove the hardcoded secret from {file_path}. "
                    "Rotate the exposed credential immediately. "
                    "Use environment variables or a secrets manager (e.g., HashiCorp Vault, "
                    "AWS Secrets Manager) instead of hardcoding secrets in source files. "
                    "Add this pattern to a pre-commit hook (e.g., detect-secrets, truffleHog)."
                ),
                "domain": DOMAIN,
                "evid_label": evid_label,
            })

        logger.info("Secrets scan complete: %s — %d finding(s)", scan_path, len(results))
        return results

    def _collect_files(self, path: Path) -> List[Path]:
        """Collect files to scan, respecting skip patterns."""
        if path.is_file():
            return [path] if path.suffix in _SCAN_EXTENSIONS else []

        files = []
        for f in path.rglob("*"):
            if f.is_file() and f.suffix in _SCAN_EXTENSIONS:
                if not any(skip in f.parts for skip in _SKIP_PATTERNS):
                    files.append(f)
        return files

    def _scan_file(self, file_path: Path) -> List[Tuple[str, str, int, str]]:
        """Scan a single file. Returns list of (pattern_name, severity, line_num, snippet)."""
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            logger.warning("Could not read %s: %s", file_path, exc)
            return []

        findings = []
        lines = content.splitlines()

        for pattern_name, severity, pattern in _SECRET_PATTERNS:
            for line_num, line in enumerate(lines, 1):
                if pattern.search(line):
                    # Redact the matched value in the snippet
                    snippet = pattern.sub("[REDACTED]", line).strip()
                    findings.append((pattern_name, severity, line_num, snippet))
                    break  # One finding per pattern per file

        return findings
