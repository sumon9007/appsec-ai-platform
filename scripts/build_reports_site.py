#!/usr/bin/env python3
"""
Build a static GitHub Pages site for markdown reports.

Outputs:
- index.html redirect at site root
- /reports/ landing page
- /reports/draft/*.html and /reports/final/*.html rendered from markdown
"""

from __future__ import annotations

import html
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "reports"
ASSETS_DIR = PROJECT_ROOT / "site_assets"
OUTPUT_DIR = PROJECT_ROOT / "site"


@dataclass
class ReportPage:
    source_path: Path
    audience: str
    title: str
    report_date: str
    version: str
    classification: str
    summary: str
    slug: str
    html_body: str

    @property
    def output_path(self) -> Path:
        return OUTPUT_DIR / "reports" / self.audience / f"{self.slug}.html"

    @property
    def href(self) -> str:
        return f"./{self.audience}/{self.slug}.html"


def main() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    (OUTPUT_DIR / "reports" / "draft").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "reports" / "final").mkdir(parents=True, exist_ok=True)

    _copy_assets()
    reports = _load_reports()
    _write_root_redirect()
    _write_reports_index(reports)
    for report in reports:
        _write_report_page(report)


def _copy_assets() -> None:
    shutil.copytree(ASSETS_DIR, OUTPUT_DIR / "assets")


def _load_reports() -> List[ReportPage]:
    reports: List[ReportPage] = []
    for audience in ("draft", "final"):
        for path in sorted((REPORTS_DIR / audience).glob("*.md")):
            markdown = path.read_text(encoding="utf-8")
            reports.append(_parse_report(path, audience, markdown))
    return reports


def _parse_report(path: Path, audience: str, markdown: str) -> ReportPage:
    title = _first_heading(markdown) or path.stem.replace("-", " ").title()
    report_date = _extract_bold_field(markdown, "Report Date") or _infer_date_from_filename(path.name)
    version = _extract_bold_field(markdown, "Version") or "Unspecified"
    classification = _extract_bold_field(markdown, "CLASSIFICATION") or "Unspecified"
    summary = _extract_summary(markdown) or "Security report"
    slug = path.stem
    html_body = _markdown_to_html(markdown)
    return ReportPage(
        source_path=path,
        audience=audience,
        title=title,
        report_date=report_date,
        version=version,
        classification=classification,
        summary=summary,
        slug=slug,
        html_body=html_body,
    )


def _write_root_redirect() -> None:
    content = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta http-equiv="refresh" content="0; url=./reports/" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Reports Portal Redirect</title>
    <link rel="canonical" href="./reports/" />
  </head>
  <body>
    <p>Redirecting to <a href="./reports/">reports</a>...</p>
  </body>
</html>
"""
    (OUTPUT_DIR / "index.html").write_text(content, encoding="utf-8")
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")


def _write_reports_index(reports: Iterable[ReportPage]) -> None:
    reports = list(reports)
    draft_cards = "\n".join(_report_card(report) for report in reports if report.audience == "draft")
    final_cards = "\n".join(_report_card(report) for report in reports if report.audience == "final")
    if not draft_cards:
        draft_cards = '<p class="empty-state">No draft reports published yet.</p>'
    if not final_cards:
        final_cards = '<p class="empty-state">No final reports published yet.</p>'

    payload = [
        {
            "title": report.title,
            "audience": report.audience,
            "report_date": report.report_date,
            "version": report.version,
            "classification": report.classification,
            "summary": report.summary,
            "href": report.href,
        }
        for report in reports
    ]

    content = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Reports Portal</title>
    <meta name="description" content="Security audit report portal for published workspace reports." />
    <link rel="stylesheet" href="../assets/reports.css" />
  </head>
  <body>
    <div class="site-shell">
      <aside class="sidebar">
        <div>
          <p class="eyebrow">AppSec AI Platform</p>
          <h1>Reports Portal</h1>
          <p class="lede">A polished GitHub Pages view for audit drafts, final reports, and supporting delivery artifacts, restyled to align with the Diversified Robotic visual language.</p>
        </div>
        <div class="sidebar-panel">
          <p class="panel-label">Theme</p>
          <p class="panel-value">Diversified Night</p>
          <p class="panel-note">Dark gradient surfaces, electric blue accents, and glass-like panels adapted from the public site styling.</p>
        </div>
        <div class="sidebar-panel">
          <p class="panel-label">Published Sets</p>
          <ul class="stat-list">
            <li><span>Draft</span><strong>{sum(1 for report in reports if report.audience == "draft")}</strong></li>
            <li><span>Final</span><strong>{sum(1 for report in reports if report.audience == "final")}</strong></li>
            <li><span>Total</span><strong>{len(reports)}</strong></li>
          </ul>
        </div>
      </aside>
      <main class="content">
        <header class="page-header">
          <div>
            <p class="eyebrow">GitHub Pages</p>
            <h2>Published Security Reports</h2>
            <p class="page-copy">Use this portal to review current report drafts, share final write-ups, and keep client delivery material cleanly accessible under <code>/reports/</code>.</p>
          </div>
          <label class="search-box">
            <span>Search</span>
            <input id="report-search" type="search" placeholder="Find a report by title or date" />
          </label>
        </header>
        <section class="report-section">
          <div class="section-heading">
            <p class="eyebrow">Working Material</p>
            <h3>Draft Reports</h3>
          </div>
          <div class="card-grid" data-group="draft">
            {draft_cards}
          </div>
        </section>
        <section class="report-section">
          <div class="section-heading">
            <p class="eyebrow">Delivery Material</p>
            <h3>Final Reports</h3>
          </div>
          <div class="card-grid" data-group="final">
            {final_cards}
          </div>
        </section>
      </main>
    </div>
    <script>
      const reports = {json.dumps(payload)};
      const searchInput = document.getElementById("report-search");
      const cards = [...document.querySelectorAll(".report-card")];
      searchInput.addEventListener("input", (event) => {{
        const query = event.target.value.trim().toLowerCase();
        cards.forEach((card) => {{
          const haystack = card.dataset.search;
          card.style.display = !query || haystack.includes(query) ? "" : "none";
        }});
      }});
    </script>
  </body>
</html>
"""
    (OUTPUT_DIR / "reports" / "index.html").write_text(content, encoding="utf-8")


def _report_card(report: ReportPage) -> str:
    search_text = " ".join(
        [
            report.title,
            report.report_date,
            report.version,
            report.classification,
            report.summary,
        ]
    ).lower()
    return f"""
      <article class="report-card" data-search="{html.escape(search_text)}">
        <div class="card-topline">
          <span class="badge badge-{report.audience}">{html.escape(report.audience.title())}</span>
          <span class="meta">{html.escape(report.report_date)}</span>
        </div>
        <h4>{html.escape(report.title)}</h4>
        <p class="summary">{html.escape(report.summary)}</p>
        <dl class="card-meta">
          <div><dt>Version</dt><dd>{html.escape(report.version)}</dd></div>
          <div><dt>Classification</dt><dd>{html.escape(report.classification)}</dd></div>
        </dl>
        <a class="card-link" href="{html.escape(report.href)}">Open report</a>
      </article>
    """


def _write_report_page(report: ReportPage) -> None:
    report.output_path.parent.mkdir(parents=True, exist_ok=True)
    back_href = "../index.html"
    content = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{html.escape(report.title)}</title>
    <meta name="description" content="{html.escape(report.summary)}" />
    <link rel="stylesheet" href="../../assets/reports.css" />
  </head>
  <body class="report-page">
    <div class="report-shell">
      <header class="report-header">
        <a class="back-link" href="{back_href}">Back to reports</a>
        <div class="report-hero">
          <div>
            <p class="eyebrow">{html.escape(report.audience.title())} report</p>
            <h1>{html.escape(report.title)}</h1>
            <p class="page-copy">{html.escape(report.summary)}</p>
          </div>
          <dl class="hero-meta">
            <div><dt>Date</dt><dd>{html.escape(report.report_date)}</dd></div>
            <div><dt>Version</dt><dd>{html.escape(report.version)}</dd></div>
            <div><dt>Classification</dt><dd>{html.escape(report.classification)}</dd></div>
          </dl>
        </div>
      </header>
      <main class="markdown-frame">
        <article class="markdown-body">
          {report.html_body}
        </article>
      </main>
    </div>
  </body>
</html>
"""
    report.output_path.write_text(content, encoding="utf-8")


def _first_heading(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def _extract_bold_field(markdown: str, label: str) -> str:
    pattern = re.compile(rf"\*\*{re.escape(label)}:\*\*\s*(.+)")
    match = pattern.search(markdown)
    return match.group(1).strip() if match else ""


def _extract_summary(markdown: str) -> str:
    posture_match = re.search(r"Overall security posture statement:\s*(.+)", markdown)
    if posture_match:
        return posture_match.group(1).strip()

    overall_section_match = re.search(r"\*\*The.+?\*\*", markdown, re.DOTALL)
    if overall_section_match:
        return overall_section_match.group(0).strip("* ").strip()

    return _first_nonempty_paragraph(markdown)


def _first_nonempty_paragraph(markdown: str) -> str:
    paragraphs = []
    current: List[str] = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped:
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue
        if (
            stripped.startswith("#")
            or stripped.startswith("|")
            or stripped.startswith("*")
            or stripped.startswith("-")
            or re.match(r"^\d+\.\s", stripped)
        ):
            continue
        current.append(stripped)
    if current:
        paragraphs.append(" ".join(current))
    for paragraph in paragraphs:
        looks_like_toc = paragraph.count("[") >= 2 and paragraph.count("]") >= 2
        if paragraph.startswith("**") or looks_like_toc:
            continue
        if len(paragraph) >= 40 and not re.match(r"^[0-9.\s\[\]\(\)#:-]+$", paragraph):
            return paragraph
    for paragraph in paragraphs:
        if not paragraph.startswith("**"):
            return paragraph
    return ""


def _infer_date_from_filename(filename: str) -> str:
    match = re.match(r"(\d{4}-\d{2}-\d{2})-", filename)
    return match.group(1) if match else "Unspecified"


def _markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    blocks: List[str] = []
    paragraph: List[str] = []
    bullet_items: List[str] = []
    ordered_items: List[str] = []
    table_lines: List[str] = []
    code_lines: List[str] = []
    in_code = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(part.strip() for part in paragraph).strip()
            if text:
                blocks.append(f"<p>{_inline(text)}</p>")
            paragraph = []

    def flush_bullets() -> None:
        nonlocal bullet_items
        if bullet_items:
            items = "".join(f"<li>{_inline(item)}</li>" for item in bullet_items)
            blocks.append(f"<ul>{items}</ul>")
            bullet_items = []

    def flush_ordered() -> None:
        nonlocal ordered_items
        if ordered_items:
            items = "".join(f"<li>{_inline(item)}</li>" for item in ordered_items)
            blocks.append(f"<ol>{items}</ol>")
            ordered_items = []

    def flush_table() -> None:
        nonlocal table_lines
        if not table_lines:
            return
        rows = [_split_table_row(line) for line in table_lines if line.strip()]
        if len(rows) >= 2 and _is_separator_row(rows[1]):
            header = rows[0]
            body = rows[2:]
        else:
            header = rows[0]
            body = rows[1:]
        head_html = "".join(f"<th>{_inline(cell)}</th>" for cell in header)
        body_html = "".join(
            "<tr>" + "".join(f"<td>{_inline(cell)}</td>" for cell in row) + "</tr>"
            for row in body
        )
        blocks.append(
            "<div class=\"table-wrap\"><table><thead><tr>"
            + head_html
            + "</tr></thead><tbody>"
            + body_html
            + "</tbody></table></div>"
        )
        table_lines = []

    def flush_code() -> None:
        nonlocal code_lines
        if code_lines:
            code = html.escape("\n".join(code_lines))
            blocks.append(f"<pre><code>{code}</code></pre>")
            code_lines = []

    for line in lines:
        stripped = line.rstrip("\n")

        if stripped.startswith("```"):
            flush_paragraph()
            flush_bullets()
            flush_ordered()
            flush_table()
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(stripped)
            continue

        if not stripped.strip():
            flush_paragraph()
            flush_bullets()
            flush_ordered()
            flush_table()
            continue

        if stripped.startswith("|"):
            flush_paragraph()
            flush_bullets()
            flush_ordered()
            table_lines.append(stripped)
            continue

        flush_table()

        if stripped == "---":
            flush_paragraph()
            flush_bullets()
            flush_ordered()
            blocks.append("<hr />")
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading_match:
            flush_paragraph()
            flush_bullets()
            flush_ordered()
            level = len(heading_match.group(1))
            text = _inline(heading_match.group(2).strip())
            blocks.append(f"<h{level}>{text}</h{level}>")
            continue

        ordered_match = re.match(r"^\d+\.\s+(.*)$", stripped)
        if ordered_match:
            flush_paragraph()
            flush_bullets()
            ordered_items.append(ordered_match.group(1).strip())
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            flush_ordered()
            bullet_items.append(stripped[2:].strip())
            continue

        paragraph.append(stripped)

    flush_paragraph()
    flush_bullets()
    flush_ordered()
    flush_table()
    flush_code()
    return "\n".join(blocks)


def _split_table_row(line: str) -> List[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _is_separator_row(row: List[str]) -> bool:
    return all(cell and set(cell) <= {"-", ":"} for cell in row)


def _inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    return escaped


if __name__ == "__main__":
    main()
