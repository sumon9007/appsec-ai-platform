"""
cli.py — Command-line entrypoints for the appsec audit workspace.
"""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from src.workflows.passive_web_audit import run_passive_web_audit


console = Console()


@click.group()
def cli() -> None:
    """Run executable audit workflows for the workspace."""


@cli.group()
def audit() -> None:
    """Execute an audit workflow."""


@audit.command("headers-tls")
@click.option(
    "--url",
    "urls",
    multiple=True,
    help="Explicit target URL to audit. Repeat for multiple targets. Defaults to .claude/context/scope.md.",
)
@click.option(
    "--register",
    "register_path",
    type=click.Path(path_type=Path),
    default=None,
    help="Optional path to the findings register Markdown file.",
)
@click.option(
    "--auditor",
    "collector",
    default=None,
    help="Override the collector/auditor name written into evidence and findings.",
)
def audit_headers_tls(urls: tuple[str, ...], register_path: Path | None, collector: str | None) -> None:
    """Run the passive Security Headers and TLS workflow."""
    try:
        summary = run_passive_web_audit(urls=urls, register_path=register_path, collector=collector)
    except RuntimeError as exc:
        raise click.ClickException(str(exc)) from exc

    console.print(
        f"[bold green]Passive audit complete[/bold green] for {len(summary.target_urls)} target(s)."
    )
    console.print(f"Findings register: {summary.register_path}")
    console.print(f"Session record: {summary.session_path}")

    table = Table(title="Findings Written")
    table.add_column("ID")
    table.add_column("Severity")
    table.add_column("Domain")
    table.add_column("Target")
    table.add_column("Title")

    for finding in summary.findings_written:
        table.add_row(
            finding["id"],
            finding["severity"],
            finding["domain"],
            finding["target"],
            finding["title"],
        )

    if summary.findings_written:
        console.print(table)
    else:
        console.print("No findings were written.")

    if summary.errors:
        console.print("[bold yellow]Errors[/bold yellow]")
        for error in summary.errors:
            console.print(f"- {error}")
