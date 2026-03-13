"""
full_audit.py — Full multi-domain passive audit workflow.

Orchestrates all passive audit tools in sequence for a target URL.
Covers: headers, TLS, cookies, session/JWT, misconfig, auth, RBAC,
        input validation, dependencies (optional), API (optional), secrets (optional).

Respects the authorization gate — will not run without CONFIRMED authorization.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from src.config.settings import AUDIT_RUNS_ACTIVE_DIR, DEFAULT_AUDITOR, DEFAULT_REGISTER_PATH
from src.models.entities import AuthorizationGrant
from src.policies.authorization import load_authorization, require_confirmed
from src.storage.run_store import complete_run, fail_run, new_run
from src.tools.api_audit import ApiAudit
from src.tools.auth_audit import AuthAudit
from src.tools.cookie_audit import CookieAudit
from src.tools.crawler import Crawler
from src.tools.dependency_audit import DependencyAudit
from src.tools.headers_audit import HeadersAudit
from src.tools.input_validation_audit import InputValidationAudit
from src.tools.misconfig_audit import MisconfigAudit
from src.tools.rbac_audit import RbacAudit
from src.tools.secrets_scan import SecretsScan
from src.tools.session_jwt_audit import SessionJwtAudit
from src.tools.tls_audit import TLSAudit
from src.utils.context_reader import get_audit_id, get_auditor_name, get_target_urls, get_testing_mode
from src.utils.findings_writer import append_finding
from src.utils.http_client import HttpClient

logger = logging.getLogger(__name__)


@dataclass
class FullAuditSummary:
    """Structured result of a full audit run."""
    audit_id: str
    auditor: str
    target_urls: List[str]
    tools_run: List[str]
    findings_written: List[Dict] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    register_path: Optional[Path] = None
    session_path: Optional[Path] = None


def run_full_audit(
    urls: Optional[Iterable[str]] = None,
    register_path: Optional[Path] = None,
    collector: Optional[str] = None,
    manifest_path: Optional[Path] = None,
    spec_path: Optional[Path] = None,
    scan_path: Optional[Path] = None,
    tools: Optional[List[str]] = None,
    max_crawl_pages: int = 30,
    dry_run: bool = False,
) -> FullAuditSummary:
    """
    Run the full passive audit workflow.

    tools: subset of tool names to run (default: all passive tools)
           options: headers, tls, cookies, session, misconfig, auth, rbac,
                    input, crawl, dependencies, api, secrets
    dry_run: collect evidence but do not write findings to register.
    """
    grant = load_authorization()
    require_confirmed(grant)

    target_urls = list(urls or get_target_urls())
    if not target_urls:
        raise RuntimeError(
            "No in-scope target URLs found. Populate .claude/context/scope.md or pass --url."
        )

    register_path = register_path or DEFAULT_REGISTER_PATH
    auditor = collector or get_auditor_name() or DEFAULT_AUDITOR
    audit_id = get_audit_id() or "UNSPECIFIED"

    all_tools = tools or ["headers", "tls", "cookies", "session", "misconfig", "auth", "rbac", "input", "crawl"]
    if manifest_path and "dependencies" not in all_tools:
        all_tools.append("dependencies")
    if spec_path and "api" not in all_tools:
        all_tools.append("api")
    if scan_path and "secrets" not in all_tools:
        all_tools.append("secrets")

    summary = FullAuditSummary(
        audit_id=audit_id,
        auditor=auditor,
        target_urls=target_urls,
        tools_run=all_tools,
        register_path=register_path,
    )

    # Initialize run state
    from src.models.entities import Target
    targets = [Target(url=u) for u in target_urls]
    run = new_run(audit_id=audit_id, auditor=auditor, authorization=grant, targets=targets)

    try:
        with HttpClient() as http_client:
            for url in target_urls:
                logger.info("==> Starting full audit for: %s", url)
                crawl_pages = []

                # Crawl first (feeds downstream tools)
                if "crawl" in all_tools:
                    logger.info("  [crawl] Passive crawl...")
                    crawler = Crawler(http_client=http_client, collector=auditor, max_pages=max_crawl_pages)
                    crawl_result = crawler.crawl(url)
                    crawl_pages = [p.url for p in crawl_result.pages]
                    page_inventories = crawl_result.pages
                    for err_url, err_msg in crawl_result.errors.items():
                        summary.errors.append(f"crawl:{err_url}: {err_msg}")
                else:
                    page_inventories = []

                tool_results = []

                if "headers" in all_tools:
                    logger.info("  [headers] Security headers audit...")
                    tool_results.extend(HeadersAudit(http_client=http_client, collector=auditor).run(url))

                if "tls" in all_tools:
                    logger.info("  [tls] TLS/certificate audit...")
                    tool_results.extend(TLSAudit(collector=auditor).run(url))

                if "cookies" in all_tools:
                    logger.info("  [cookies] Cookie audit...")
                    tool_results.extend(CookieAudit(http_client=http_client, collector=auditor).run(url))

                if "session" in all_tools:
                    logger.info("  [session] Session/JWT audit...")
                    tool_results.extend(SessionJwtAudit(http_client=http_client, collector=auditor).run(url))

                if "misconfig" in all_tools:
                    logger.info("  [misconfig] Misconfiguration audit...")
                    tool_results.extend(MisconfigAudit(http_client=http_client, collector=auditor).run(url))

                if "auth" in all_tools:
                    logger.info("  [auth] Authentication audit...")
                    tool_results.extend(AuthAudit(http_client=http_client, collector=auditor).run(url))

                if "rbac" in all_tools:
                    logger.info("  [rbac] Authorization/RBAC audit...")
                    tool_results.extend(
                        RbacAudit(http_client=http_client, collector=auditor).run(url, crawl_pages=crawl_pages)
                    )

                if "input" in all_tools:
                    logger.info("  [input] Input validation audit...")
                    tool_results.extend(
                        InputValidationAudit(collector=auditor).run(url, page_inventories=page_inventories)
                    )

                if "api" in all_tools:
                    logger.info("  [api] API audit...")
                    tool_results.extend(ApiAudit(http_client=http_client, collector=auditor).run(url, spec_path=spec_path))

                # Write findings
                for result in tool_results:
                    if "error" in result:
                        summary.errors.append(f"{result.get('url', url)}: {result['error']}")
                        continue
                    if not dry_run:
                        finding = _result_to_finding(result)
                        try:
                            find_id = append_finding(finding=finding, register_path=register_path)
                            summary.findings_written.append({
                                "id": find_id,
                                "title": finding["title"],
                                "severity": finding["severity"],
                                "domain": finding["domain"],
                                "target": finding["target"],
                            })
                            run.findings_written.append(find_id)
                        except ValueError as exc:
                            logger.warning("Could not write finding: %s", exc)
                            summary.errors.append(str(exc))

            # Dependency audit (file-based, not per-URL)
            if "dependencies" in all_tools and manifest_path:
                logger.info("  [dependencies] Dependency CVE audit...")
                dep_results = DependencyAudit(collector=auditor).run(manifest_path)
                for result in dep_results:
                    if "error" in result:
                        summary.errors.append(f"dependencies: {result['error']}")
                        continue
                    if not dry_run:
                        finding = _result_to_finding(result)
                        try:
                            find_id = append_finding(finding=finding, register_path=register_path)
                            summary.findings_written.append({
                                "id": find_id,
                                "title": finding["title"],
                                "severity": finding["severity"],
                                "domain": finding["domain"],
                                "target": finding["target"],
                            })
                        except ValueError as exc:
                            summary.errors.append(str(exc))

            # Secrets scan (filesystem-based)
            if "secrets" in all_tools and scan_path:
                logger.info("  [secrets] Secrets scan...")
                secrets_results = SecretsScan(collector=auditor).run(scan_path)
                for result in secrets_results:
                    if "error" in result:
                        summary.errors.append(f"secrets: {result['error']}")
                        continue
                    if not dry_run:
                        finding = _result_to_finding(result)
                        try:
                            find_id = append_finding(finding=finding, register_path=register_path)
                            summary.findings_written.append({
                                "id": find_id,
                                "title": finding["title"],
                                "severity": finding["severity"],
                                "domain": finding["domain"],
                                "target": finding["target"],
                            })
                        except ValueError as exc:
                            summary.errors.append(str(exc))

        # Write session record
        summary.session_path = _write_session(summary, grant)
        complete_run(run)

    except Exception as exc:
        logger.error("Full audit failed: %s", exc)
        fail_run(run, str(exc))
        raise

    return summary


def _result_to_finding(result: Dict) -> Dict:
    """Map a tool result dict to a normalized finding dict."""
    status = "review-gap" if result.get("assessment") in ("REVIEW_GAP",) else "confirmed"
    if result.get("assessment") == "WEAK":
        status = "suspected"

    return {
        "title": result.get("check", "Unnamed finding"),
        "domain": result.get("domain", "Unknown"),
        "severity": result.get("severity", "Info"),
        "confidence": result.get("confidence", "medium"),
        "target": result.get("url", ""),
        "evidence_labels": [result["evid_label"]] if result.get("evid_label") else ["NO-EVIDENCE"],
        "observation": result.get("detail", ""),
        "risk": _infer_risk(result),
        "recommendation": result.get("recommendation", "Review and remediate this finding."),
        "acceptance_criteria": result.get("acceptance_criteria", "Review against security baseline"),
        "status": status,
        "review_type": "passive",
    }


def _infer_risk(result: Dict) -> str:
    domain = result.get("domain", "")
    severity = result.get("severity", "")
    check = result.get("check", "")

    risk_map = {
        "Security Headers": "The observed control weakness reduces browser-enforced protections.",
        "TLS / Certificate": "Weak transport security exposes traffic to interception or tampering.",
        "Session Management": "Session control weaknesses may allow session hijacking or fixation.",
        "Authentication": "Authentication gaps may allow unauthorized access to the application.",
        "Authorization": "Authorization weaknesses may allow privilege escalation or data exposure.",
        "Input Validation": "Unvalidated inputs may be exploitable for injection attacks.",
        "Dependencies": "Known vulnerable components may be exploitable by attackers.",
        "Security Misconfiguration": "Misconfigurations may expose sensitive data or admin interfaces.",
        "API Security": "API control gaps may allow unauthorized data access or manipulation.",
    }
    return risk_map.get(domain, "This issue weakens the application security posture.")


def _write_session(summary: FullAuditSummary, grant: AuthorizationGrant) -> Optional[Path]:
    """Write a session record for the full audit run."""
    AUDIT_RUNS_ACTIVE_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(tz=timezone.utc).date().isoformat()
    session_path = AUDIT_RUNS_ACTIVE_DIR / f"{today}-full-audit-session.md"

    severity_counts = {}
    for f in summary.findings_written:
        sev = f["severity"]
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    finding_rows = "\n".join(
        f"| {f['id']} | {f['title'][:50]} | {f['severity']} | {f['domain']} |"
        for f in summary.findings_written
    ) or "| (none) | No new findings | n/a | n/a |"

    content = f"""# Full Audit Session Record

| Field | Value |
|-------|-------|
| **Session Date** | {today} |
| **Auditor** | {summary.auditor} |
| **Audit ID** | {summary.audit_id} |
| **Authorization** | CONFIRMED |
| **Authorization Mode** | {grant.mode.value} |

## Targets

{chr(10).join(f'- {u}' for u in summary.target_urls)}

## Tools Run

{chr(10).join(f'- {t}' for t in summary.tools_run)}

## Findings Written

| Finding ID | Title | Severity | Domain |
|------------|-------|----------|--------|
{finding_rows}

**Total:** {len(summary.findings_written)} | Critical: {severity_counts.get('Critical', 0)} | High: {severity_counts.get('High', 0)} | Medium: {severity_counts.get('Medium', 0)} | Low: {severity_counts.get('Low', 0)} | Info: {severity_counts.get('Info', 0)}

## Errors

{chr(10).join(f'- {e}' for e in summary.errors) or '(none)'}

## Register

{summary.register_path}
"""
    session_path.write_text(content, encoding="utf-8")
    return session_path
