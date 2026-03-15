"""
cli.py — Command-line entrypoints for the appsec-ai-platform.

All commands enforce the authorization gate before running any audit activity.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from src.config import settings as _settings
from src.workflows.passive_web_audit import run_passive_web_audit

console = Console()


def _print_findings_table(findings: list) -> None:
    if not findings:
        console.print("[dim]No findings written.[/dim]")
        return
    table = Table(title="Findings Written", show_lines=False)
    table.add_column("ID", style="bold")
    table.add_column("Sev", style="bold red")
    table.add_column("Domain")
    table.add_column("Target", max_width=40)
    table.add_column("Title", max_width=60)
    for f in findings:
        sev = f.get("severity", "?")
        color = {"Critical": "red", "High": "red1", "Medium": "yellow", "Low": "green", "Info": "blue"}.get(sev, "white")
        table.add_row(f["id"], f"[{color}]{sev}[/{color}]", f.get("domain", ""), f.get("target", ""), f.get("title", ""))
    console.print(table)


def _print_errors(errors: list) -> None:
    if errors:
        console.print("\n[bold yellow]Errors / Warnings[/bold yellow]")
        for e in errors:
            console.print(f"  [yellow]•[/yellow] {e}")


# ── Shared options ────────────────────────────────────────────────────────────
# Defaults fall back to .env / AUDIT_* environment variables via settings.

_url_option = click.option(
    "--url", "urls", multiple=True,
    help=(
        "Target URL(s) to audit. Repeat for multiple targets. "
        "Falls back to AUDIT_TARGET_URLS env var, then scope.md."
    ),
)
_register_option = click.option(
    "--register", "register_path", type=click.Path(path_type=Path),
    default=None,
    help="Path to findings register Markdown file. Falls back to AUDIT_REGISTER_PATH env var.",
)
_auditor_option = click.option(
    "--auditor", "collector", default=None,
    help="Auditor name written into evidence and findings. Falls back to AUDIT_DEFAULT_AUDITOR env var.",
)
_dry_run_option = click.option(
    "--dry-run", is_flag=True, default=False,
    help="Collect evidence but do not write findings to the register.",
)


def _resolve_urls(urls: tuple):
    """Return CLI urls if provided, else fall back to AUDIT_TARGET_URLS, else None (→ scope.md)."""
    return tuple(urls) or tuple(_settings.DEFAULT_TARGET_URLS) or None


# ── CLI root ───────────────────────────────────────────────────────────────────

@click.group()
@click.option("--debug", is_flag=True, default=False, help="Enable debug logging.")
def cli(debug: bool) -> None:
    """appsec-ai-platform — Structured security audit CLI."""
    level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s")


# ── audit group ───────────────────────────────────────────────────────────────

@cli.group()
def audit() -> None:
    """Execute security audit workflows."""


@audit.command("headers-tls")
@_url_option
@_register_option
@_auditor_option
def audit_headers_tls(urls, register_path, collector):
    """Passive Security Headers and TLS review (legacy single-domain command)."""
    try:
        summary = run_passive_web_audit(urls=_resolve_urls(urls), register_path=register_path, collector=collector)
    except RuntimeError as exc:
        raise click.ClickException(str(exc)) from exc
    console.print(f"[bold green]Complete[/bold green] — {len(summary.target_urls)} target(s)")
    console.print(f"Register: {summary.register_path}")
    _print_findings_table(summary.findings_written)
    _print_errors(summary.errors)


@audit.command("full")
@_url_option
@_register_option
@_auditor_option
@_dry_run_option
@click.option("--manifest", "manifest_path", type=click.Path(path_type=Path),
              default=None,
              help="Path to dependency manifest (requirements.txt, package.json, etc.). Falls back to AUDIT_MANIFEST_PATH env var.")
@click.option("--spec", "spec_path", type=click.Path(path_type=Path),
              default=None,
              help="Path to OpenAPI or Postman spec file. Falls back to AUDIT_SPEC_PATH env var.")
@click.option("--scan", "scan_path", type=click.Path(path_type=Path),
              default=None,
              help="Path to directory or file for secrets scanning. Falls back to AUDIT_SCAN_PATH env var.")
@click.option("--max-pages", default=None, type=int,
              help="Maximum pages for the passive crawler. Falls back to AUDIT_MAX_CRAWL_PAGES env var.")
@click.option("--tools", default=None,
              help="Comma-separated tool subset: headers,tls,cookies,session,misconfig,auth,rbac,input,crawl,dependencies,api,secrets")
def audit_full(urls, register_path, collector, dry_run, manifest_path, spec_path, scan_path, max_pages, tools):
    """Run the full multi-domain passive audit workflow."""
    from src.workflows.full_audit import run_full_audit
    tool_list = [t.strip() for t in tools.split(",")] if tools else None
    try:
        summary = run_full_audit(
            urls=_resolve_urls(urls),
            register_path=register_path,
            collector=collector,
            manifest_path=manifest_path or _settings.DEFAULT_MANIFEST_PATH,
            spec_path=spec_path or _settings.DEFAULT_SPEC_PATH,
            scan_path=scan_path or _settings.DEFAULT_SCAN_PATH,
            tools=tool_list,
            max_crawl_pages=max_pages if max_pages is not None else _settings.DEFAULT_MAX_CRAWL_PAGES,
            dry_run=dry_run,
        )
    except RuntimeError as exc:
        raise click.ClickException(str(exc)) from exc

    prefix = "[dim](dry-run)[/dim] " if dry_run else ""
    console.print(f"{prefix}[bold green]Full audit complete[/bold green] — {len(summary.target_urls)} target(s)")
    console.print(f"Register: {summary.register_path}")
    if summary.session_path:
        console.print(f"Session:  {summary.session_path}")
    _print_findings_table(summary.findings_written)
    _print_errors(summary.errors)


@audit.command("headers")
@_url_option
@_register_option
@_auditor_option
@_dry_run_option
def audit_headers(urls, register_path, collector, dry_run):
    """Security headers audit only."""
    from src.workflows.full_audit import run_full_audit
    try:
        summary = run_full_audit(urls=_resolve_urls(urls), register_path=register_path, collector=collector,
                                 tools=["headers"], dry_run=dry_run)
    except RuntimeError as exc:
        raise click.ClickException(str(exc)) from exc
    console.print("[bold green]Headers audit complete[/bold green]")
    _print_findings_table(summary.findings_written)
    _print_errors(summary.errors)


@audit.command("tls")
@_url_option
@_register_option
@_auditor_option
@_dry_run_option
def audit_tls(urls, register_path, collector, dry_run):
    """TLS/certificate audit only."""
    from src.workflows.full_audit import run_full_audit
    try:
        summary = run_full_audit(urls=_resolve_urls(urls), register_path=register_path, collector=collector,
                                 tools=["tls"], dry_run=dry_run)
    except RuntimeError as exc:
        raise click.ClickException(str(exc)) from exc
    console.print("[bold green]TLS audit complete[/bold green]")
    _print_findings_table(summary.findings_written)
    _print_errors(summary.errors)


@audit.command("cookies")
@_url_option
@_register_option
@_auditor_option
@_dry_run_option
def audit_cookies(urls, register_path, collector, dry_run):
    """Cookie security attributes audit."""
    from src.workflows.full_audit import run_full_audit
    try:
        summary = run_full_audit(urls=_resolve_urls(urls), register_path=register_path, collector=collector,
                                 tools=["cookies"], dry_run=dry_run)
    except RuntimeError as exc:
        raise click.ClickException(str(exc)) from exc
    console.print("[bold green]Cookie audit complete[/bold green]")
    _print_findings_table(summary.findings_written)
    _print_errors(summary.errors)


@audit.command("session")
@_url_option
@_register_option
@_auditor_option
@_dry_run_option
def audit_session(urls, register_path, collector, dry_run):
    """Session management and JWT passive audit."""
    from src.workflows.full_audit import run_full_audit
    try:
        summary = run_full_audit(urls=_resolve_urls(urls), register_path=register_path, collector=collector,
                                 tools=["session"], dry_run=dry_run)
    except RuntimeError as exc:
        raise click.ClickException(str(exc)) from exc
    console.print("[bold green]Session/JWT audit complete[/bold green]")
    _print_findings_table(summary.findings_written)
    _print_errors(summary.errors)


@audit.command("misconfig")
@_url_option
@_register_option
@_auditor_option
@_dry_run_option
def audit_misconfig(urls, register_path, collector, dry_run):
    """Security misconfiguration passive audit."""
    from src.workflows.full_audit import run_full_audit
    try:
        summary = run_full_audit(urls=_resolve_urls(urls), register_path=register_path, collector=collector,
                                 tools=["misconfig"], dry_run=dry_run)
    except RuntimeError as exc:
        raise click.ClickException(str(exc)) from exc
    console.print("[bold green]Misconfiguration audit complete[/bold green]")
    _print_findings_table(summary.findings_written)
    _print_errors(summary.errors)


@audit.command("dependencies")
@click.option("--manifest", "manifest_path", type=click.Path(path_type=Path), default=None,
              help="Path to dependency manifest. Falls back to AUDIT_MANIFEST_PATH env var.")
@_register_option
@_auditor_option
@_dry_run_option
def audit_dependencies(manifest_path, register_path, collector, dry_run):
    """Dependency CVE audit using OSV.dev."""
    from src.workflows.full_audit import run_full_audit
    resolved = manifest_path or _settings.DEFAULT_MANIFEST_PATH
    if not resolved:
        raise click.UsageError("--manifest is required (or set AUDIT_MANIFEST_PATH in .env).")
    try:
        summary = run_full_audit(register_path=register_path, collector=collector,
                                 manifest_path=resolved, tools=["dependencies"],
                                 urls=["file://manifest"], dry_run=dry_run)
    except RuntimeError as exc:
        raise click.ClickException(str(exc)) from exc
    console.print("[bold green]Dependency audit complete[/bold green]")
    _print_findings_table(summary.findings_written)
    _print_errors(summary.errors)


@audit.command("secrets")
@click.option("--scan", "scan_path", type=click.Path(path_type=Path), default=None,
              help="Path to scan for hardcoded secrets. Falls back to AUDIT_SCAN_PATH env var.")
@_register_option
@_auditor_option
@_dry_run_option
def audit_secrets(scan_path, register_path, collector, dry_run):
    """Secrets scan for hardcoded credentials and API keys."""
    from src.workflows.full_audit import run_full_audit
    resolved = scan_path or _settings.DEFAULT_SCAN_PATH
    if not resolved:
        raise click.UsageError("--scan is required (or set AUDIT_SCAN_PATH in .env).")
    try:
        summary = run_full_audit(register_path=register_path, collector=collector,
                                 scan_path=resolved, tools=["secrets"],
                                 urls=["file://secrets-scan"], dry_run=dry_run)
    except RuntimeError as exc:
        raise click.ClickException(str(exc)) from exc
    console.print("[bold green]Secrets scan complete[/bold green]")
    _print_findings_table(summary.findings_written)
    _print_errors(summary.errors)


@audit.command("api")
@_url_option
@click.option("--spec", "spec_path", type=click.Path(path_type=Path), default=None,
              help="Path to OpenAPI or Postman spec file.")
@_register_option
@_auditor_option
@_dry_run_option
def audit_api(urls, spec_path, register_path, collector, dry_run):
    """API security assessment."""
    from src.workflows.full_audit import run_full_audit
    try:
        summary = run_full_audit(urls=_resolve_urls(urls), register_path=register_path, collector=collector,
                                 spec_path=spec_path or _settings.DEFAULT_SPEC_PATH,
                                 tools=["api"], dry_run=dry_run)
    except RuntimeError as exc:
        raise click.ClickException(str(exc)) from exc
    console.print("[bold green]API audit complete[/bold green]")
    _print_findings_table(summary.findings_written)
    _print_errors(summary.errors)


# ── report group ──────────────────────────────────────────────────────────────

@cli.group()
def report() -> None:
    """Generate audit reports from the findings register."""


_format_option = click.option(
    "--format", "output_format",
    type=click.Choice(["md", "html"], case_sensitive=False),
    default="md",
    show_default=True,
    help="Output format: md (Markdown) or html (self-contained HTML).",
)


@report.command("technical")
@click.option("--register", "register_path", type=click.Path(path_type=Path),
              default=None, help="Path to findings register. Falls back to AUDIT_REGISTER_PATH env var.")
@click.option("--target", "target_name", default=None, help="Target application name. Falls back to AUDIT_TARGET_NAME env var.")
@click.option("--auditor", default=None, help="Auditor name. Falls back to AUDIT_DEFAULT_AUDITOR env var.")
@click.option("--version", default=None, help="Report version label. Falls back to AUDIT_REPORT_VERSION env var.")
@_format_option
def report_technical(register_path, target_name, auditor, version, output_format):
    """Generate a draft technical security report."""
    reg = register_path or _settings.DEFAULT_REGISTER_PATH
    if output_format == "html":
        from src.reporting.html_report_generator import generate_technical_report_html
        path = generate_technical_report_html(
            reg,
            target_name=target_name or _settings.DEFAULT_TARGET_NAME,
            auditor=auditor or _settings.DEFAULT_AUDITOR,
            version=version or _settings.DEFAULT_REPORT_VERSION,
        )
    else:
        from src.reporting.report_generator import generate_technical_report
        path = generate_technical_report(
            reg,
            target_name=target_name or _settings.DEFAULT_TARGET_NAME,
            auditor=auditor or _settings.DEFAULT_AUDITOR,
            version=version or _settings.DEFAULT_REPORT_VERSION,
        )
    console.print(f"[bold green]Technical report written:[/bold green] {path}")


@report.command("executive")
@click.option("--register", "register_path", type=click.Path(path_type=Path), default=None,
              help="Path to findings register. Falls back to AUDIT_REGISTER_PATH env var.")
@click.option("--target", "target_name", default=None,
              help="Target application name. Falls back to AUDIT_TARGET_NAME env var.")
@click.option("--version", default=None,
              help="Report version label. Falls back to AUDIT_REPORT_VERSION env var.")
@_format_option
def report_executive(register_path, target_name, version, output_format):
    """Generate a non-technical executive summary report."""
    reg = register_path or _settings.DEFAULT_REGISTER_PATH
    if output_format == "html":
        from src.reporting.html_report_generator import generate_executive_summary_html
        path = generate_executive_summary_html(
            reg,
            target_name=target_name or _settings.DEFAULT_TARGET_NAME,
            version=version or _settings.DEFAULT_REPORT_VERSION,
        )
    else:
        from src.reporting.report_generator import generate_executive_summary
        path = generate_executive_summary(
            reg,
            target_name=target_name or _settings.DEFAULT_TARGET_NAME,
            version=version or _settings.DEFAULT_REPORT_VERSION,
        )
    console.print(f"[bold green]Executive summary written:[/bold green] {path}")


@report.command("remediation")
@click.option("--register", "register_path", type=click.Path(path_type=Path), default=None,
              help="Path to findings register. Falls back to AUDIT_REGISTER_PATH env var.")
@click.option("--target", "target_name", default=None,
              help="Target application name. Falls back to AUDIT_TARGET_NAME env var.")
@_format_option
def report_remediation(register_path, target_name, output_format):
    """Generate a prioritized remediation plan."""
    reg = register_path or _settings.DEFAULT_REGISTER_PATH
    if output_format == "html":
        from src.reporting.html_report_generator import generate_remediation_plan_html
        path = generate_remediation_plan_html(reg, target_name=target_name or _settings.DEFAULT_TARGET_NAME)
    else:
        from src.reporting.report_generator import generate_remediation_plan
        path = generate_remediation_plan(reg, target_name=target_name or _settings.DEFAULT_TARGET_NAME)
    console.print(f"[bold green]Remediation plan written:[/bold green] {path}")


# ── session group ─────────────────────────────────────────────────────────────

@cli.group()
def session() -> None:
    """Manage audit session state."""


@session.command("status")
def session_status():
    """Show current audit context and authorization status."""
    from src.policies.authorization import load_authorization
    from src.utils.context_reader import get_audit_id, get_auditor_name, get_target_urls
    grant = load_authorization()
    urls = get_target_urls()
    audit_id = get_audit_id() or "(not set)"
    auditor = get_auditor_name() or "(not set)"

    console.print(f"\n[bold]Audit Context Status[/bold]")
    console.print(f"  Audit ID:        {audit_id}")
    console.print(f"  Auditor:         {auditor}")
    status_color = "green" if grant.is_confirmed else "red"
    console.print(f"  Authorization:   [{status_color}]{grant.status}[/{status_color}]")
    console.print(f"  Testing Mode:    {grant.mode.value}")
    console.print(f"  In-scope URLs:   {len(urls)}")
    for u in urls:
        console.print(f"    - {u}")
    console.print()
