"""
passive_web_audit.py — Runnable passive workflow for web security quick audits.

This is the first executable slice of the broader audit workspace:
- validates authorization and scope from .claude/context/
- runs passive headers and TLS checks for each target URL
- writes evidence using existing tool helpers
- normalizes tool results into findings and appends them to the register
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from src.config.settings import AUDIT_RUNS_ACTIVE_DIR, DEFAULT_AUDITOR, DEFAULT_REGISTER_PATH
from src.tools.headers_audit import HeadersAudit
from src.tools.tls_audit import TLSAudit
from src.utils.context_reader import (
    AUTH_CONFIRMED,
    check_authorization,
    get_audit_id,
    get_auditor_name,
    get_target_urls,
    get_testing_mode,
)
from src.utils.findings_writer import append_finding
from src.utils.http_client import HttpClient


@dataclass
class WorkflowSummary:
    """Structured outcome for a passive audit run."""

    audit_id: str
    auditor: str
    testing_mode: str
    target_urls: List[str]
    register_path: Path
    session_path: Path
    findings_written: List[Dict[str, str]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def run_passive_web_audit(
    urls: Optional[Iterable[str]] = None,
    register_path: Optional[Path] = None,
    collector: Optional[str] = None,
) -> WorkflowSummary:
    """
    Run the passive headers/TLS workflow against explicit URLs or context targets.

    Raises:
        RuntimeError: authorization is not confirmed or no usable targets exist.
    """
    auth_status = check_authorization()
    if auth_status != AUTH_CONFIRMED:
        raise RuntimeError(
            "AUTHORIZATION REQUIRED: audit activity cannot begin until Authorization Status "
            "is CONFIRMED in .claude/context/audit-context.md."
        )

    target_urls = _normalize_urls(urls or get_target_urls())
    if not target_urls:
        raise RuntimeError(
            "No in-scope target URLs were found. Populate .claude/context/scope.md or pass --url."
        )

    register_path = register_path or DEFAULT_REGISTER_PATH
    auditor = collector or get_auditor_name() or DEFAULT_AUDITOR
    audit_id = get_audit_id() or "UNSPECIFIED-AUDIT-ID"
    testing_mode = get_testing_mode()

    started_at = datetime.now(tz=timezone.utc)
    findings_written: List[Dict[str, str]] = []
    errors: List[str] = []

    with HttpClient() as http_client:
        headers_audit = HeadersAudit(http_client=http_client, collector=auditor)
        tls_audit = TLSAudit(collector=auditor)

        for url in target_urls:
            tool_results = []
            tool_results.extend(headers_audit.run(url))
            tool_results.extend(tls_audit.run(url))

            for result in tool_results:
                if "error" in result:
                    errors.append(f"{url}: {result['error']}")
                    continue

                finding = _result_to_finding(result)
                finding_id = append_finding(finding=finding, register_path=register_path)
                findings_written.append(
                    {
                        "id": finding_id,
                        "title": finding["title"],
                        "severity": finding["severity"],
                        "domain": finding["domain"],
                        "evidence": ", ".join(finding["evidence_labels"]),
                        "target": finding["target"],
                    }
                )

    session_path = _write_session_record(
        audit_id=audit_id,
        auditor=auditor,
        testing_mode=testing_mode,
        target_urls=target_urls,
        findings=findings_written,
        register_path=register_path,
        started_at=started_at,
        ended_at=datetime.now(tz=timezone.utc),
        errors=errors,
    )

    return WorkflowSummary(
        audit_id=audit_id,
        auditor=auditor,
        testing_mode=testing_mode,
        target_urls=target_urls,
        register_path=register_path,
        session_path=session_path,
        findings_written=findings_written,
        errors=errors,
    )


def _normalize_urls(urls: Iterable[str]) -> List[str]:
    """Drop blanks and preserve order while deduplicating."""
    normalized: List[str] = []
    seen = set()
    for raw in urls:
        url = raw.strip()
        if not url or url in seen:
            continue
        seen.add(url)
        normalized.append(url)
    return normalized


def _result_to_finding(result: Dict[str, str]) -> Dict[str, object]:
    """Map a tool result dict into the normalized findings register structure."""
    title = f"{result['check']} on {result['url']}"
    evidence_labels = [result["evid_label"]] if result.get("evid_label") else ["NO-EVIDENCE-LABEL"]
    status = "review-gap" if result.get("assessment") == "REVIEW_GAP" else "confirmed"

    return {
        "title": title,
        "domain": result["domain"],
        "severity": result["severity"],
        "confidence": result["confidence"],
        "target": result["url"],
        "evidence_labels": evidence_labels,
        "observation": result["detail"],
        "risk": _risk_for_result(result),
        "recommendation": result["recommendation"],
        "acceptance_criteria": _acceptance_criteria_for_result(result),
        "status": status,
        "review_type": "passive",
    }


def _risk_for_result(result: Dict[str, str]) -> str:
    """Return practical risk text aligned to the observed control failure."""
    check = result["check"]

    if "Content-Security-Policy" in check:
        return "Weak or missing CSP reduces browser-enforced protection against XSS and clickjacking-related abuse."
    if "Strict-Transport-Security" in check:
        return "Without strong HSTS, users remain more exposed to protocol downgrade and first-visit HTTPS stripping risks."
    if "X-Content-Type-Options" in check:
        return "Missing nosniff allows browsers more freedom to interpret content types, which can widen script execution risk."
    if "Clickjacking Protection" in check:
        return "Pages may be frameable by an attacker-controlled site, enabling clickjacking or UI redress attacks."
    if "Referrer-Policy" in check:
        return "Sensitive URL paths or parameters may be leaked to third parties via browser referrer behavior."
    if "Permissions-Policy" in check:
        return "Browser features may be available more broadly than intended, increasing unnecessary client-side attack surface."
    if "CORS" in check:
        return "Cross-origin data access may be broader than intended, potentially exposing authenticated application data."
    if "Information Exposure" in check:
        return "Verbose technology disclosures can help attackers tailor reconnaissance and exploit selection."
    if "TLS — Scheme" in check:
        return "Traffic can be intercepted or modified in transit if HTTPS is not enforced."
    if "TLS — Protocol Version" in check:
        return "Deprecated TLS versions weaken transport security and can violate modern compliance baselines."
    if "TLS — Certificate Expiry" in check:
        return "An expired or near-expiry certificate can cause outages, trust failures, and degraded secure access."
    if "TLS — Weak Signature Algorithm" in check:
        return "Weak certificate signatures reduce trust in the authenticity and integrity of the TLS certificate chain."
    if "TLS — Cipher Suite Enumeration" in check:
        return "Cipher support breadth is unknown, so weak ciphers cannot yet be ruled out with confidence."

    return "The observed issue weakens the target's security posture and should be reviewed against the documented baseline."


def _acceptance_criteria_for_result(result: Dict[str, str]) -> str:
    """Map tool results to the closest acceptance criteria statement in the workspace."""
    check = result["check"]
    severity = result["severity"]

    if "TLS — Scheme" in check:
        return "Headers-Must-Fix-1 — HTTP used without redirect to HTTPS"
    if "TLS — Protocol Version" in check:
        return "Headers-Must-Fix-2 — TLS 1.0 or 1.1 enabled"
    if "TLS — Certificate Expiry" in check and severity == "Critical":
        return "Headers-Must-Fix-3 — Certificate expired or expiring within 7 days"
    if "TLS — Certificate Expiry" in check:
        return "Headers-Advisory-3 — Certificate expiry 8–30 days out"
    if "CORS — Wildcard Origin with Credentials" in check:
        return "Headers-Must-Fix-4 — CORS configured with Access-Control-Allow-Origin: * and Access-Control-Allow-Credentials: true"
    if "Content-Security-Policy" in check:
        return "Headers-Advisory-1 — Missing Content-Security-Policy"
    if "Referrer-Policy" in check:
        return "Headers-Advisory-2 — Missing Referrer-Policy"
    if "Permissions-Policy" in check:
        return "Headers-Advisory-3 — Missing Permissions-Policy"
    if "Strict-Transport-Security" in check:
        return "Headers-Pass-Threshold — HSTS present with max-age >= 6 months"
    if "X-Content-Type-Options" in check:
        return "Headers-Pass-Threshold — X-Content-Type-Options: nosniff present"
    if "Clickjacking Protection" in check:
        return "Headers-Pass-Threshold — X-Frame-Options or CSP frame-ancestors present"
    if "TLS — Weak Signature Algorithm" in check:
        return "Headers-Pass-Threshold — Certificate signed with a modern algorithm and trusted chain"
    if "TLS — Cipher Suite Enumeration" in check:
        return "Headers-Review-Gap — Full cipher suite validation requires authorized active TLS scanning"

    return "Headers-Pass-Threshold — Review against Security Headers & Transport baseline"


def _write_session_record(
    audit_id: str,
    auditor: str,
    testing_mode: str,
    target_urls: List[str],
    findings: List[Dict[str, str]],
    register_path: Path,
    started_at: datetime,
    ended_at: datetime,
    errors: List[str],
) -> Path:
    """Write a lightweight session record for the automated passive run."""
    AUDIT_RUNS_ACTIVE_DIR.mkdir(parents=True, exist_ok=True)

    session_date = started_at.date().isoformat()
    session_id = f"SESSION-{session_date}-{_next_session_sequence(session_date):03d}"
    session_path = AUDIT_RUNS_ACTIVE_DIR / f"{session_date}-passive-web-session.md"

    severity_counts = {key: 0 for key in ("Critical", "High", "Medium", "Low", "Info")}
    for finding in findings:
        severity_counts[finding["severity"]] = severity_counts.get(finding["severity"], 0) + 1

    finding_rows = "\n".join(
        f"| {item['id']} | {item['title']} | {item['severity']} | {item['domain']} | {item['evidence']} |"
        for item in findings
    ) or "| (none) | No new findings | n/a | n/a | n/a |"

    activity_lines = "\n".join(
        f"- Ran passive headers and TLS checks for `{url}`." for url in target_urls
    )
    if errors:
        activity_lines += "\n" + "\n".join(f"- Error recorded: {error}" for error in errors)

    session_content = f"""# Audit Session Record

## Session Header

| Field | Value |
|-------|-------|
| **Session ID** | {session_id} |
| **Session Date** | {session_date} |
| **Start Time** | {started_at.strftime("%H:%M UTC")} |
| **End Time** | {ended_at.strftime("%H:%M UTC")} |
| **Auditor** | {auditor} |
| **Audit Engagement** | {audit_id} |
| **Session File Location** | {session_path} |

## Authorization Confirmation

| Field | Value |
|-------|-------|
| **Authorization Status** | CONFIRMED |
| **Authorizing Party** | See `.claude/context/audit-context.md` |
| **Authorization Reference** | See `.claude/context/audit-context.md` |
| **Testing Mode** | {testing_mode} |
| **Scope Confirmed** | Yes |

## Session Objectives

1. Complete the passive Security Headers and TLS review for the selected targets.
2. Persist evidence and findings in the workspace outputs.

## Domain(s) Covered

| Domain | Skill Loaded | Coverage Level | Status |
|--------|-------------|---------------|--------|
| Security Headers & TLS | headers-tls-audit | Full | Complete |

## Activities Performed

{activity_lines}

## Findings Noted (Summary)

| Finding ID | Title | Severity | Domain | Evidence Collected |
|------------|-------|----------|--------|--------------------|
{finding_rows}

**Total new findings this session:** {len(findings)}
**Critical:** {severity_counts['Critical']} | **High:** {severity_counts['High']} | **Medium:** {severity_counts['Medium']} | **Low:** {severity_counts['Low']} | **Info:** {severity_counts['Info']}

## Evidence Collected

Evidence references are recorded in the findings register at `{register_path}` and the generated files under `evidence/raw/`.

## Items Deferred to Next Session

- Extend the executable workflow to additional domains beyond Security Headers & TLS.
- Review any review-gap findings that require authorized active testing or extra client evidence.

## Session Status

**Session Complete:** Yes
"""

    session_path.write_text(session_content, encoding="utf-8")
    return session_path


def _next_session_sequence(session_date: str) -> int:
    """Return the next session sequence for the provided date."""
    prefix = f"{session_date}-"
    existing = []
    for path in AUDIT_RUNS_ACTIVE_DIR.glob(f"{session_date}-*-session.md"):
        if path.name.startswith(prefix):
            existing.append(path)
    return len(existing) + 1
