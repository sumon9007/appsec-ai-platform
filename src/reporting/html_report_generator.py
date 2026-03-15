"""
html_report_generator.py — Generates beautiful, professional, self-contained HTML security audit reports.

No external CDN or font dependencies — all CSS is embedded.
Output files go in reports/draft/ with .html extension using the same naming convention as report_generator.py.

Exposes:
    generate_technical_report_html(register_path, target_name, auditor, version) -> Path
    generate_executive_summary_html(register_path, target_name, auditor, version) -> Path
    generate_remediation_plan_html(register_path, target_name) -> Path
"""

from __future__ import annotations

import logging
import math
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Dict, List, Tuple

from src.config.settings import PROJECT_ROOT
from src.reports.finding_formatter import severity_to_sla
from src.reporting.report_generator import (
    _derive_posture,
    _executive_recommendations,
    _executive_risk_summary,
    _immediate_actions,
    _parse_register,
    _review_gaps,
    _severity_order,
)

logger = logging.getLogger(__name__)

REPORTS_DRAFT_DIR = PROJECT_ROOT / "reports" / "draft"

# ---------------------------------------------------------------------------
# Color constants — used both in CSS variables and in SVG generation
# ---------------------------------------------------------------------------

_SEVERITY_COLORS: Dict[str, Tuple[str, str]] = {
    "Critical": ("#ef4444", "#2d1515"),
    "High":     ("#f97316", "#2d1d0e"),
    "Medium":   ("#eab308", "#2d2708"),
    "Low":      ("#3b82f6", "#0e1a2d"),
    "Info":     ("#6b7280", "#1a1e26"),
}

_STATUS_COLORS: Dict[str, Tuple[str, str]] = {
    "confirmed":    ("#22c55e", "#0d2e1a"),
    "review-gap":   ("#a855f7", "#1e0d2e"),
    "suspected":    ("#f97316", "#2d1d0e"),
    "mitigated":    ("#38bdf8", "#0d1f2e"),
    "accepted-risk": ("#6b7280", "#1a1e26"),
    "closed":       ("#4ade80", "#0a2e1a"),
    "open":         ("#f97316", "#2d1d0e"),
}


# ---------------------------------------------------------------------------
# SVG Donut Chart
# ---------------------------------------------------------------------------

def _svg_donut(counts: Dict[str, int]) -> str:
    """
    Generate a pure SVG donut chart for findings by severity.

    Args:
        counts: dict mapping severity label to count, e.g.
                {'Critical': 1, 'High': 2, 'Medium': 3, 'Low': 0, 'Info': 0}

    Returns:
        SVG markup string with viewBox="0 0 160 160".
    """
    cx = cy = 80
    outer_r = 70
    inner_r = 45
    order = ["Critical", "High", "Medium", "Low", "Info"]
    total = sum(counts.get(s, 0) for s in order)

    if total == 0:
        # Gray ring with "0" in center
        return (
            f'<svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg" '
            f'style="width:160px;height:160px;">'
            f'<circle cx="{cx}" cy="{cy}" r="{outer_r}" fill="none" '
            f'stroke="#2a3a4a" stroke-width="{outer_r - inner_r}"/>'
            f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="central" '
            f'fill="#94a3b8" font-size="28" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',system-ui,sans-serif" '
            f'font-weight="700">0</text>'
            f'</svg>'
        )

    def _polar(angle_deg: float, r: float) -> Tuple[float, float]:
        rad = math.radians(angle_deg - 90)
        return cx + r * math.cos(rad), cy + r * math.sin(rad)

    def _arc_path(start_deg: float, end_deg: float, color: str) -> str:
        # Clamp to avoid degenerate arcs
        if abs(end_deg - start_deg) < 0.01:
            return ""
        large = 1 if (end_deg - start_deg) > 180 else 0
        ox1, oy1 = _polar(start_deg, outer_r)
        ox2, oy2 = _polar(end_deg, outer_r)
        ix1, iy1 = _polar(end_deg, inner_r)
        ix2, iy2 = _polar(start_deg, inner_r)
        d = (
            f"M {ox1:.4f} {oy1:.4f} "
            f"A {outer_r} {outer_r} 0 {large} 1 {ox2:.4f} {oy2:.4f} "
            f"L {ix1:.4f} {iy1:.4f} "
            f"A {inner_r} {inner_r} 0 {large} 0 {ix2:.4f} {iy2:.4f} "
            f"Z"
        )
        return f'<path d="{d}" fill="{color}"/>'

    paths: List[str] = []
    current_angle = 0.0
    for severity in order:
        count = counts.get(severity, 0)
        if count == 0:
            continue
        sweep = 360.0 * count / total
        color = _SEVERITY_COLORS.get(severity, ("#6b7280", "#1a1e26"))[0]
        paths.append(_arc_path(current_angle, current_angle + sweep, color))
        current_angle += sweep

    paths_svg = "\n".join(paths)

    return (
        f'<svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg" '
        f'style="width:160px;height:160px;">'
        f'{paths_svg}'
        f'<text x="{cx}" y="{cy - 10}" text-anchor="middle" dominant-baseline="central" '
        f'fill="#e2e8f0" font-size="28" '
        f'font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',system-ui,sans-serif" '
        f'font-weight="700">{total}</text>'
        f'<text x="{cx}" y="{cy + 16}" text-anchor="middle" dominant-baseline="central" '
        f'fill="#94a3b8" font-size="11" '
        f'font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',system-ui,sans-serif">'
        f'findings</text>'
        f'</svg>'
    )


# ---------------------------------------------------------------------------
# Shared CSS
# ---------------------------------------------------------------------------

_BASE_CSS = """
:root {
  --bg:           #0a0f1e;
  --surface:      #111827;
  --surface-r:    #1a2235;
  --border:       #1e2d45;
  --text-primary: #e2e8f0;
  --text-muted:   #94a3b8;
  --accent:       #38bdf8;

  --crit-fg:   #ef4444; --crit-bg:   #2d1515;
  --high-fg:   #f97316; --high-bg:   #2d1d0e;
  --med-fg:    #eab308; --med-bg:    #2d2708;
  --low-fg:    #3b82f6; --low-bg:    #0e1a2d;
  --info-fg:   #6b7280; --info-bg:   #1a1e26;

  --ok-fg:     #22c55e; --ok-bg:     #0d2e1a;
  --gap-fg:    #a855f7; --gap-bg:    #1e0d2e;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { font-size: 15px; scroll-behavior: smooth; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text-primary);
  line-height: 1.65;
  min-height: 100vh;
}

/* ── Top sticky header ─────────────────────────────────────────────────── */
.top-bar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(17, 24, 39, 0.95);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.6rem 1.5rem;
  gap: 1rem;
}

.top-bar .bar-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.top-bar .bar-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
}

.classification-badge {
  background: #7c1d1d;
  color: #fca5a5;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 0.25rem 0.6rem;
  border-radius: 4px;
  border: 1px solid #991b1b;
}

.version-label {
  font-size: 0.75rem;
  color: var(--text-muted);
  font-weight: 500;
}

.print-btn {
  background: var(--surface-r);
  border: 1px solid var(--border);
  color: var(--text-muted);
  font-size: 0.8rem;
  padding: 0.35rem 0.8rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.print-btn:hover { background: var(--border); color: var(--text-primary); }

/* ── Main layout ───────────────────────────────────────────────────────── */
.main-wrap {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem 1.5rem 4rem;
}

/* ── Cover hero ────────────────────────────────────────────────────────── */
.cover-block {
  background: linear-gradient(135deg, #0d1b35 0%, #111827 60%, #0a0f1e 100%);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 3rem 2.5rem;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}
.cover-block::before {
  content: '';
  position: absolute;
  top: -40px; right: -40px;
  width: 200px; height: 200px;
  background: radial-gradient(circle, rgba(56,189,248,0.08) 0%, transparent 70%);
  pointer-events: none;
}

.cover-report-type {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 0.75rem;
}

.cover-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.2;
  margin-bottom: 0.5rem;
}

.cover-subtitle {
  font-size: 1rem;
  color: var(--text-muted);
  margin-bottom: 2rem;
}

.cover-meta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.cover-meta-item label {
  display: block;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 0.2rem;
}

.cover-meta-item span {
  font-size: 0.9rem;
  color: var(--text-primary);
  font-weight: 500;
}

/* ── Section structure ─────────────────────────────────────────────────── */
.section {
  margin-bottom: 2.5rem;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border);
}

.section-header h2 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: 0.02em;
}

.section-num {
  width: 28px; height: 28px;
  background: var(--surface-r);
  border: 1px solid var(--border);
  border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--accent);
  flex-shrink: 0;
}

/* ── Posture banner ────────────────────────────────────────────────────── */
.posture-banner {
  border-radius: 10px;
  padding: 1.25rem 1.5rem;
  border: 1px solid;
  margin-bottom: 2rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}
.posture-banner.posture-critical { background: #1a0505; border-color: #7f1d1d; }
.posture-banner.posture-high     { background: #1a0a02; border-color: #7c2d12; }
.posture-banner.posture-medium   { background: #1a1600; border-color: #713f12; }
.posture-banner.posture-ok       { background: #021a0a; border-color: #14532d; }

.posture-icon {
  font-size: 1.75rem;
  line-height: 1;
  flex-shrink: 0;
}

.posture-text-wrap strong {
  display: block;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 0.35rem;
}
.posture-banner.posture-critical .posture-text-wrap strong { color: #ef4444; }
.posture-banner.posture-high     .posture-text-wrap strong { color: #f97316; }
.posture-banner.posture-medium   .posture-text-wrap strong { color: #eab308; }
.posture-banner.posture-ok       .posture-text-wrap strong { color: #22c55e; }

.posture-text-wrap p {
  font-size: 0.925rem;
  color: var(--text-primary);
  line-height: 1.6;
}

/* ── Severity summary cards ────────────────────────────────────────────── */
.sev-cards {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.75rem;
  margin-bottom: 2rem;
}

@media (max-width: 700px) {
  .sev-cards { grid-template-columns: repeat(3, 1fr); }
}

.sev-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.1rem 0.75rem;
  text-align: center;
  transition: background 0.15s;
}
.sev-card:hover { background: var(--surface-r); }

.sev-card .count {
  font-size: 2.25rem;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 0.4rem;
}
.sev-card.crit .count { color: var(--crit-fg); }
.sev-card.high .count { color: var(--high-fg); }
.sev-card.med  .count { color: var(--med-fg); }
.sev-card.low  .count { color: var(--low-fg); }
.sev-card.info .count { color: var(--info-fg); }

/* ── Severity/status badges ────────────────────────────────────────────── */
.badge {
  display: inline-block;
  padding: 0.2rem 0.55rem;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  white-space: nowrap;
}
.badge-Critical { background: var(--crit-bg); color: var(--crit-fg); }
.badge-High     { background: var(--high-bg); color: var(--high-fg); }
.badge-Medium   { background: var(--med-bg);  color: var(--med-fg); }
.badge-Low      { background: var(--low-bg);  color: var(--low-fg); }
.badge-Info     { background: var(--info-bg); color: var(--info-fg); }

.badge-confirmed    { background: var(--ok-bg);   color: var(--ok-fg); }
.badge-review-gap   { background: var(--gap-bg);  color: var(--gap-fg); }
.badge-suspected    { background: var(--high-bg); color: var(--high-fg); }
.badge-mitigated    { background: #0d1f2e; color: var(--accent); }
.badge-accepted-risk{ background: var(--info-bg); color: var(--info-fg); }
.badge-closed       { background: #0a2e1a; color: #4ade80; }
.badge-open         { background: var(--high-bg); color: var(--high-fg); }

/* ── Chart + breakdown row ─────────────────────────────────────────────── */
.chart-row {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}
.chart-row .donut-wrap {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}
.chart-row .donut-wrap span {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-align: center;
}

/* ── Tables ────────────────────────────────────────────────────────────── */
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}
.data-table th {
  background: var(--surface-r);
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.75rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 0.65rem 0.9rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
}
.data-table td {
  padding: 0.65rem 0.9rem;
  border-bottom: 1px solid var(--border);
  color: var(--text-primary);
  vertical-align: middle;
}
.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover td { background: rgba(255,255,255,0.025); transition: background 0.15s; }

.table-wrap {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}

.data-table .find-id {
  font-family: 'SF Mono', 'Fira Code', 'Courier New', monospace;
  font-size: 0.8rem;
  color: var(--accent);
  white-space: nowrap;
}

/* ── Alert box (immediate actions) ────────────────────────────────────── */
.alert-box {
  background: #1a0505;
  border: 1px solid #7f1d1d;
  border-left: 4px solid var(--crit-fg);
  border-radius: 8px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 2rem;
}
.alert-box .alert-title {
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--crit-fg);
  margin-bottom: 0.75rem;
}
.alert-box ul { list-style: none; padding: 0; }
.alert-box li {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(239,68,68,0.15);
  font-size: 0.875rem;
}
.alert-box li:last-child { border-bottom: none; }
.alert-box .sla-chip {
  font-size: 0.7rem;
  background: #7f1d1d;
  color: #fca5a5;
  border-radius: 4px;
  padding: 0.15rem 0.45rem;
  font-weight: 700;
  white-space: nowrap;
  flex-shrink: 0;
}

/* ── Collapsible finding cards ─────────────────────────────────────────── */
.finding-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  margin-bottom: 0.75rem;
  overflow: hidden;
}

.finding-card details { }

.finding-card details > summary {
  list-style: none;
  cursor: pointer;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  user-select: none;
  transition: background 0.15s;
}
.finding-card details > summary:hover { background: var(--surface-r); }
.finding-card details > summary::-webkit-details-marker { display: none; }

.summary-chevron {
  margin-left: auto;
  font-size: 0.75rem;
  color: var(--text-muted);
  transition: transform 0.2s;
  flex-shrink: 0;
}
details[open] .summary-chevron { transform: rotate(90deg); }

.summary-id {
  font-family: 'SF Mono', 'Fira Code', 'Courier New', monospace;
  font-size: 0.8rem;
  color: var(--accent);
  white-space: nowrap;
  flex-shrink: 0;
}

.summary-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
  flex: 1;
  min-width: 0;
}

.finding-body {
  padding: 0 1.25rem 1.25rem;
  border-top: 1px solid var(--border);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
  margin: 1rem 0;
}

.info-cell {
  background: var(--surface-r);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.6rem 0.75rem;
}
.info-cell label {
  display: block;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 0.25rem;
}
.info-cell span {
  font-size: 0.875rem;
  color: var(--text-primary);
}

.finding-field {
  margin: 1rem 0;
}
.finding-field h4 {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 0.4rem;
}
.finding-field p {
  font-size: 0.875rem;
  color: var(--text-primary);
  line-height: 1.65;
}

/* ── Priority sections (remediation plan) ──────────────────────────────── */
.priority-section {
  border-radius: 10px;
  border: 1px solid;
  margin-bottom: 2rem;
  overflow: hidden;
}
.priority-section .prio-header {
  padding: 0.9rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.priority-section .prio-header h3 {
  font-size: 0.95rem;
  font-weight: 700;
  flex: 1;
}
.priority-section .prio-body {
  padding: 1rem 1.25rem;
}
.priority-section .prio-body ul {
  list-style: none;
  padding: 0;
}
.priority-section .prio-body li {
  padding: 0.6rem 0;
  border-bottom: 1px solid;
  font-size: 0.875rem;
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
}
.priority-section .prio-body li:last-child { border-bottom: none; }

.prio-crit { background: #120505; border-color: #7f1d1d; }
.prio-crit .prio-header { background: #1a0505; }
.prio-crit .prio-header h3 { color: var(--crit-fg); }
.prio-crit .prio-body li { border-color: rgba(239,68,68,0.15); }

.prio-high { background: #120800; border-color: #7c2d12; }
.prio-high .prio-header { background: #1a0e03; }
.prio-high .prio-header h3 { color: var(--high-fg); }
.prio-high .prio-body li { border-color: rgba(249,115,22,0.15); }

.prio-med { background: #12100000; border-color: #713f12; }
.prio-med { background: #0e0c00; border-color: #713f12; }
.prio-med .prio-header { background: #1a1600; }
.prio-med .prio-header h3 { color: var(--med-fg); }
.prio-med .prio-body li { border-color: rgba(234,179,8,0.15); }

.prio-low { background: #00050e; border-color: #1e3a5f; }
.prio-low .prio-header { background: #010b1a; }
.prio-low .prio-header h3 { color: var(--low-fg); }
.prio-low .prio-body li { border-color: rgba(59,130,246,0.15); }

/* ── Info/note boxes ───────────────────────────────────────────────────── */
.note-box {
  background: #050d1f;
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent);
  border-radius: 8px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 2rem;
}
.note-box h4 {
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 0.6rem;
}
.note-box ol {
  padding-left: 1.25rem;
  font-size: 0.875rem;
  color: var(--text-primary);
}
.note-box ol li { margin-bottom: 0.35rem; }

/* ── Methodology table ─────────────────────────────────────────────────── */
.methodology-wrap {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}

/* ── Risk domain list ──────────────────────────────────────────────────── */
.risk-list { list-style: none; padding: 0; }
.risk-list li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.6rem 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.875rem;
}
.risk-list li:last-child { border-bottom: none; }
.risk-list .domain-name {
  font-weight: 600;
  color: var(--text-primary);
  min-width: 180px;
}
.risk-list .count-chip {
  background: var(--surface-r);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 0.1rem 0.45rem;
  font-size: 0.75rem;
  color: var(--text-muted);
  font-weight: 600;
}

/* ── Recommendations list ──────────────────────────────────────────────── */
.rec-list { list-style: none; padding: 0; counter-reset: rec-counter; }
.rec-list li {
  counter-increment: rec-counter;
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.875rem;
  color: var(--text-primary);
}
.rec-list li:last-child { border-bottom: none; }
.rec-list li::before {
  content: counter(rec-counter);
  background: var(--surface-r);
  border: 1px solid var(--border);
  color: var(--accent);
  font-weight: 700;
  font-size: 0.75rem;
  width: 24px; height: 24px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  margin-top: 0.05rem;
}

/* ── Footer ────────────────────────────────────────────────────────────── */
.report-footer {
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
  color: var(--text-muted);
  flex-wrap: wrap;
  gap: 0.5rem;
}

/* ── Misc helpers ──────────────────────────────────────────────────────── */
.mono {
  font-family: 'SF Mono', 'Fira Code', 'Courier New', monospace;
  font-size: 0.8rem;
}
.text-muted { color: var(--text-muted); }
.mt1 { margin-top: 1rem; }

/* ── Print styles ──────────────────────────────────────────────────────── */
@media print {
  body { background: #fff; color: #111; }
  .top-bar { display: none; }
  .print-btn { display: none; }
  .cover-block { background: #f8fafc; border-color: #cbd5e1; color: #111; }
  .cover-title { color: #0f172a; }
  .cover-subtitle { color: #475569; }
  .cover-meta-item label { color: #64748b; }
  .cover-meta-item span { color: #0f172a; }
  .section-header h2 { color: #0f172a; }
  details { display: block; }
  details > summary { display: none; }
  .finding-body { display: block !important; padding-top: 0; }
  .data-table th { background: #f1f5f9; color: #475569; }
  .data-table td { color: #111; border-color: #e2e8f0; }
  .table-wrap, .methodology-wrap { border-color: #e2e8f0; }
  .sev-card { background: #f8fafc; border-color: #e2e8f0; }
  .finding-card { background: #fff; border-color: #e2e8f0; page-break-inside: avoid; }
  .info-cell { background: #f8fafc; border-color: #e2e8f0; }
  .info-cell label { color: #64748b; }
  .info-cell span { color: #0f172a; }
  .finding-field p { color: #111; }
  .chart-row { background: #f8fafc; border-color: #e2e8f0; }
  .note-box { background: #f0f9ff; border-color: #0ea5e9; }
  .posture-banner { background: #f8fafc !important; border-color: #cbd5e1 !important; }
  .posture-text-wrap p { color: #111; }
  .alert-box { background: #fff5f5; border-color: #fca5a5; }
  .report-footer { color: #64748b; border-color: #e2e8f0; }
}
"""


# ---------------------------------------------------------------------------
# HTML shell helpers
# ---------------------------------------------------------------------------

def _html_shell(title: str, body: str) -> str:
    """Wrap body in a complete HTML document with embedded CSS."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_esc(title)}</title>
<style>
{_BASE_CSS}
</style>
</head>
<body>
{body}
<script>
function printReport() {{ window.print(); }}
</script>
</body>
</html>"""


def _esc(text: str) -> str:
    """Minimal HTML entity escaping."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _sev_badge(severity: str) -> str:
    return f'<span class="badge badge-{_esc(severity)}">{_esc(severity)}</span>'


def _status_badge(status: str) -> str:
    css_class = status.replace(" ", "-")
    return f'<span class="badge badge-{_esc(css_class)}">{_esc(status)}</span>'


def _top_bar(report_title: str, version: str) -> str:
    return f"""<div class="top-bar">
  <span class="bar-title">{_esc(report_title)}</span>
  <div class="bar-right">
    <span class="classification-badge">Client Restricted</span>
    <span class="version-label">{_esc(version)}</span>
    <button class="print-btn" onclick="printReport()">&#x1F5A8; Print</button>
  </div>
</div>"""


def _cover_block(
    report_type_label: str,
    target_name: str,
    target_url: str,
    audit_date: str,
    auditor: str,
    classification: str,
    version: str,
) -> str:
    return f"""<div class="cover-block">
  <div class="cover-report-type">{_esc(report_type_label)}</div>
  <div class="cover-title">{_esc(target_name)}</div>
  <div class="cover-subtitle">Security Assessment Report</div>
  <div class="cover-meta-grid">
    <div class="cover-meta-item">
      <label>Report Type</label>
      <span>{_esc(report_type_label)}</span>
    </div>
    <div class="cover-meta-item">
      <label>Target</label>
      <span>{_esc(target_url or target_name)}</span>
    </div>
    <div class="cover-meta-item">
      <label>Audit Date</label>
      <span>{_esc(audit_date)}</span>
    </div>
    <div class="cover-meta-item">
      <label>Auditor</label>
      <span>{_esc(auditor or 'See engagement record')}</span>
    </div>
    <div class="cover-meta-item">
      <label>Classification</label>
      <span>{_esc(classification)}</span>
    </div>
    <div class="cover-meta-item">
      <label>Version</label>
      <span>{_esc(version)}</span>
    </div>
  </div>
</div>"""


def _posture_banner(posture: str, severity_counts: Counter) -> str:
    if severity_counts.get("Critical", 0) > 0:
        css_class = "posture-critical"
        icon = "&#x1F6A8;"
        level = "Critical Risk"
    elif severity_counts.get("High", 0) > 0:
        css_class = "posture-high"
        icon = "&#x26A0;&#xFE0F;"
        level = "High Risk"
    elif severity_counts.get("Medium", 0) > 0:
        css_class = "posture-medium"
        icon = "&#x26A0;&#xFE0F;"
        level = "Moderate Risk"
    else:
        css_class = "posture-ok"
        icon = "&#x2705;"
        level = "Low Risk"

    return f"""<div class="posture-banner {css_class}">
  <div class="posture-icon">{icon}</div>
  <div class="posture-text-wrap">
    <strong>Overall Security Posture — {_esc(level)}</strong>
    <p>{_esc(posture)}</p>
  </div>
</div>"""


def _sev_summary_cards(counts: Counter) -> str:
    cards = []
    defs = [
        ("Critical", "crit"),
        ("High",     "high"),
        ("Medium",   "med"),
        ("Low",      "low"),
        ("Info",     "info"),
    ]
    for label, css in defs:
        n = counts.get(label, 0)
        cards.append(
            f'<div class="sev-card {css}">'
            f'<div class="count">{n}</div>'
            f'{_sev_badge(label)}'
            f'</div>'
        )
    return f'<div class="sev-cards">{"".join(cards)}</div>'


def _section_header(num: int, title: str) -> str:
    return f"""<div class="section-header">
  <div class="section-num">{num}</div>
  <h2>{_esc(title)}</h2>
</div>"""


# ---------------------------------------------------------------------------
# Technical Report HTML builder
# ---------------------------------------------------------------------------

def _build_findings_table(findings: List[Dict]) -> str:
    rows = []
    for f in findings:
        rows.append(
            f"<tr>"
            f'<td><span class="find-id">{_esc(f["find_id"])}</span></td>'
            f'<td>{_esc(f.get("title", ""))}</td>'
            f'<td><span class="text-muted">{_esc(f.get("domain", ""))}</span></td>'
            f'<td>{_sev_badge(f.get("severity", "Info"))}</td>'
            f'<td><span class="text-muted">{_esc(f.get("confidence", ""))}</span></td>'
            f'<td>{_status_badge(f.get("status", "confirmed"))}</td>'
            f"</tr>"
        )
    rows_html = "\n".join(rows) if rows else (
        '<tr><td colspan="6" style="text-align:center;color:var(--text-muted);">'
        'No findings recorded.</td></tr>'
    )
    return f"""<div class="table-wrap">
<table class="data-table">
  <thead>
    <tr>
      <th>ID</th>
      <th>Title</th>
      <th>Domain</th>
      <th>Severity</th>
      <th>Confidence</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    {rows_html}
  </tbody>
</table>
</div>"""


def _build_finding_cards(findings: List[Dict]) -> str:
    cards = []
    for f in findings:
        find_id = f["find_id"]
        title = f.get("title", "Untitled")
        severity = f.get("severity", "Info")
        status = f.get("status", "confirmed")
        domain = f.get("domain", "")
        confidence = f.get("confidence", "")
        target = f.get("target", "")
        evidence = f.get("evidence", "(none)")
        observation = f.get("observation", "")
        risk = f.get("risk", "")
        recommendation = f.get("recommendation", "")
        acceptance = f.get("acceptance_criteria_mapping", "")
        sla = severity_to_sla(severity)

        cards.append(f"""<div class="finding-card">
<details>
<summary>
  <span class="summary-id">{_esc(find_id)}</span>
  {_sev_badge(severity)}
  {_status_badge(status)}
  <span class="summary-title">{_esc(title)}</span>
  <span class="summary-chevron">&#9654;</span>
</summary>
<div class="finding-body">
  <div class="info-grid">
    <div class="info-cell"><label>Domain</label><span>{_esc(domain)}</span></div>
    <div class="info-cell"><label>Confidence</label><span>{_esc(confidence)}</span></div>
    <div class="info-cell"><label>SLA</label><span>{_esc(sla)}</span></div>
    <div class="info-cell"><label>Target</label><span class="mono">{_esc(target)}</span></div>
  </div>
  <div class="finding-field">
    <h4>Evidence</h4>
    <p class="mono">{_esc(evidence)}</p>
  </div>
  <div class="finding-field">
    <h4>Observation</h4>
    <p>{_esc(observation)}</p>
  </div>
  <div class="finding-field">
    <h4>Risk</h4>
    <p>{_esc(risk)}</p>
  </div>
  <div class="finding-field">
    <h4>Recommendation</h4>
    <p>{_esc(recommendation)}</p>
  </div>
  {f'<div class="finding-field"><h4>Acceptance Criteria Mapping</h4><p>{_esc(acceptance)}</p></div>' if acceptance else ''}
</div>
</details>
</div>""")
    return "\n".join(cards) if cards else (
        '<p class="text-muted" style="padding:1rem 0;">No findings recorded.</p>'
    )


def _build_chart_row(counts: Counter, findings: List[Dict]) -> str:
    donut = _svg_donut(dict(counts))

    severities = ["Critical", "High", "Medium", "Low", "Info"]
    open_by_sev = Counter(
        f.get("severity", "Info")
        for f in findings
        if f.get("status", "") not in ("closed", "mitigated")
    )
    closed_by_sev = Counter(
        f.get("severity", "Info")
        for f in findings
        if f.get("status", "") in ("closed", "mitigated")
    )

    rows = []
    for sev in severities:
        total = counts.get(sev, 0)
        opened = open_by_sev.get(sev, 0)
        closed = closed_by_sev.get(sev, 0)
        rows.append(
            f"<tr>"
            f"<td>{_sev_badge(sev)}</td>"
            f"<td style='text-align:center;'>{total}</td>"
            f"<td style='text-align:center;color:var(--high-fg);'>{opened}</td>"
            f"<td style='text-align:center;color:var(--ok-fg);'>{closed}</td>"
            f"</tr>"
        )

    return f"""<div class="chart-row">
  <div class="donut-wrap">
    {donut}
    <span>Findings by<br>Severity</span>
  </div>
  <div style="flex:1;overflow-x:auto;">
    <table class="data-table">
      <thead>
        <tr>
          <th>Severity</th>
          <th style="text-align:center;">Total</th>
          <th style="text-align:center;">Open</th>
          <th style="text-align:center;">Closed</th>
        </tr>
      </thead>
      <tbody>
        {"".join(rows)}
      </tbody>
    </table>
  </div>
</div>"""


def _build_immediate_actions_html(critical_high: List[Dict]) -> str:
    if not critical_high:
        return (
            '<div style="padding:0.75rem 0;color:var(--ok-fg);font-size:0.875rem;">'
            '&#x2705; No Critical or High findings requiring immediate action.</div>'
        )
    items = []
    for f in critical_high:
        sla = severity_to_sla(f.get("severity", "High"))
        items.append(
            f"<li>"
            f"{_sev_badge(f.get('severity', 'High'))}"
            f'<span style="font-family:\'SF Mono\',monospace;font-size:0.8rem;color:var(--accent);">'
            f"{_esc(f['find_id'])}</span>"
            f"<span style='flex:1;'>{_esc(f.get('title', ''))}</span>"
            f'<span class="sla-chip">SLA: {_esc(sla)}</span>'
            f"</li>"
        )
    return f"""<div class="alert-box">
  <div class="alert-title">&#x26A0; Immediate Action Required</div>
  <ul>{"".join(items)}</ul>
</div>"""


def _build_review_gaps_html(findings: List[Dict]) -> str:
    gaps = [f for f in findings if f.get("status") == "review-gap"]
    if not gaps:
        return '<p class="text-muted">No review gaps recorded in this engagement.</p>'
    rows = []
    for f in gaps:
        rows.append(
            f"<tr>"
            f'<td><span class="find-id">{_esc(f["find_id"])}</span></td>'
            f"<td>{_esc(f.get('title', ''))}</td>"
            f"<td>{_esc(f.get('observation', '')[:120])}</td>"
            f"</tr>"
        )
    return f"""<div class="table-wrap">
<table class="data-table">
  <thead>
    <tr><th>ID</th><th>Area</th><th>Reason</th></tr>
  </thead>
  <tbody>{"".join(rows)}</tbody>
</table>
</div>"""


_METHODOLOGY_ROWS = [
    ("Authentication",        "Login, MFA, password policy, account lockout"),
    ("Session Management",    "Session token entropy, fixation, invalidation, JWT security"),
    ("Access Control",        "RBAC, IDOR, privilege escalation, horizontal access"),
    ("Input Validation",      "XSS, SQL injection, command injection, open redirect"),
    ("HTTP Security Headers", "HSTS, CSP, X-Frame-Options, Referrer-Policy, Permissions-Policy"),
    ("TLS Configuration",     "Protocol versions, cipher suites, certificate validity"),
    ("Cookie Security",       "Secure, HttpOnly, SameSite, expiry, scope"),
    ("Security Misconfiguration", "Debug modes, verbose errors, directory listing, admin exposure"),
    ("Dependency Security",   "Known CVEs in third-party libraries and frameworks"),
    ("Secrets Management",    "Credentials, API keys, secrets in code or config"),
    ("API Security",          "Endpoint authentication, rate limiting, schema validation"),
    ("Logging and Monitoring","Audit trail completeness, alerting coverage"),
]


def _build_methodology_table() -> str:
    rows = "".join(
        f"<tr><td><strong>{_esc(d)}</strong></td><td>{_esc(c)}</td></tr>"
        for d, c in _METHODOLOGY_ROWS
    )
    return f"""<div class="methodology-wrap">
<table class="data-table">
  <thead>
    <tr><th>Domain</th><th>Coverage</th></tr>
  </thead>
  <tbody>{rows}</tbody>
</table>
</div>"""


def _build_evidence_index(findings: List[Dict]) -> str:
    """Extract all EVID- references from findings evidence fields."""
    import re
    evid_pattern = re.compile(r"(EVID-\d{4}-\d{2}-\d{2}-\d{3}[^\s,;)]*)")
    rows = []
    for f in findings:
        evidence_text = f.get("evidence", "")
        refs = evid_pattern.findall(evidence_text)
        for ref in refs:
            rows.append(
                f"<tr>"
                f'<td><span class="mono">{_esc(ref)}</span></td>'
                f'<td><span class="find-id">{_esc(f["find_id"])}</span></td>'
                f"<td>{_esc(f.get('title', ''))}</td>"
                f"</tr>"
            )
    if not rows:
        return (
            '<p class="text-muted" style="padding:0.5rem 0;">'
            'No EVID-labeled evidence references found in findings register.</p>'
        )
    return f"""<div class="table-wrap">
<table class="data-table">
  <thead>
    <tr><th>Evidence ID</th><th>Finding</th><th>Title</th></tr>
  </thead>
  <tbody>{"".join(rows)}</tbody>
</table>
</div>"""


def _report_footer(version: str, today: str) -> str:
    return f"""<div class="report-footer">
  <span>Generated by appsec-audit-tool &mdash; {_esc(version)}</span>
  <span>Date: {_esc(today)}</span>
  <span>Classification: CLIENT RESTRICTED</span>
</div>"""


# ---------------------------------------------------------------------------
# Public API — Technical Report
# ---------------------------------------------------------------------------

def generate_technical_report_html(
    register_path: Path,
    target_name: str = "",
    auditor: str = "",
    version: str = "DRAFT v0.1",
) -> Path:
    """
    Generate a self-contained HTML technical security report.

    Returns the path to the generated .html file in reports/draft/.
    """
    REPORTS_DRAFT_DIR.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    filename = f"{today}-technical-report.html"
    report_path = REPORTS_DRAFT_DIR / filename

    findings = _parse_register(register_path)
    findings.sort(key=lambda f: _severity_order(f.get("severity", "Info")))

    severity_counts: Counter = Counter(f.get("severity", "Info") for f in findings)
    open_findings = [
        f for f in findings
        if f.get("status", "confirmed") not in ("closed", "mitigated")
    ]
    critical_high = [
        f for f in open_findings
        if f.get("severity") in ("Critical", "High")
    ]

    posture = _derive_posture(severity_counts, open_findings)
    app_name = target_name or "Target Application"
    page_title = f"Technical Security Report — {app_name}"

    body = f"""
{_top_bar(page_title, version)}
<div class="main-wrap">

  {_cover_block(
      "Technical Security Report", app_name, "",
      today, auditor, "CLIENT RESTRICTED", version
  )}

  {_posture_banner(posture, severity_counts)}

  <!-- 1. Severity summary cards -->
  <div class="section">
    {_section_header(1, "Findings Overview")}
    {_sev_summary_cards(severity_counts)}
    {_build_chart_row(severity_counts, findings)}
  </div>

  <!-- 2. Immediate actions -->
  <div class="section">
    {_section_header(2, "Immediate Actions Required")}
    {_build_immediate_actions_html(critical_high)}
  </div>

  <!-- 3. Findings table -->
  <div class="section">
    {_section_header(3, "Findings Summary Table")}
    {_build_findings_table(findings)}
  </div>

  <!-- 4. Detailed findings -->
  <div class="section">
    {_section_header(4, "Detailed Findings")}
    {_build_finding_cards(findings)}
  </div>

  <!-- 5. Review gaps -->
  <div class="section">
    {_section_header(5, "Review Gaps")}
    {_build_review_gaps_html(findings)}
  </div>

  <!-- 6. Methodology -->
  <div class="section">
    {_section_header(6, "Assessment Methodology")}
    {_build_methodology_table()}
  </div>

  <!-- 7. Evidence index -->
  <div class="section">
    {_section_header(7, "Evidence Index")}
    {_build_evidence_index(findings)}
  </div>

  {_report_footer(version, today)}

</div>
"""

    report_path.write_text(_html_shell(page_title, body), encoding="utf-8")
    logger.info("HTML technical report written: %s", report_path)
    return report_path


# ---------------------------------------------------------------------------
# Public API — Executive Summary
# ---------------------------------------------------------------------------

def _build_exec_findings_table(findings: List[Dict]) -> str:
    """Non-technical findings table: ID, description (title only), priority."""
    rows = []
    for f in sorted(findings, key=lambda x: _severity_order(x.get("severity", "Info")))[:15]:
        sev = f.get("severity", "Info")
        priority_map = {
            "Critical": "Immediate",
            "High":     "High",
            "Medium":   "Near-Term",
            "Low":      "Low",
            "Info":     "Informational",
        }
        priority = priority_map.get(sev, sev)
        rows.append(
            f"<tr>"
            f'<td><span class="find-id">{_esc(f["find_id"])}</span></td>'
            f"<td>{_esc(f.get('title', ''))}</td>"
            f"<td>{_sev_badge(sev)}</td>"
            f"<td>{_esc(priority)}</td>"
            f"</tr>"
        )
    if not rows:
        rows.append(
            '<tr><td colspan="4" style="text-align:center;color:var(--text-muted);">'
            'No findings recorded.</td></tr>'
        )
    return f"""<div class="table-wrap">
<table class="data-table">
  <thead>
    <tr>
      <th>ID</th>
      <th>Description</th>
      <th>Severity</th>
      <th>Priority</th>
    </tr>
  </thead>
  <tbody>{"".join(rows)}</tbody>
</table>
</div>"""


def _build_risk_domain_list(findings: List[Dict]) -> str:
    from collections import Counter as _Counter
    domains = _Counter(f.get("domain", "Unknown") for f in findings)
    if not domains:
        return '<p class="text-muted">No findings to summarize.</p>'
    items = []
    for domain, count in domains.most_common():
        worst_sev = min(
            (f for f in findings if f.get("domain") == domain),
            key=lambda x: _severity_order(x.get("severity", "Info")),
            default={"severity": "Info"},
        ).get("severity", "Info")
        items.append(
            f'<li>'
            f'<span class="domain-name">{_esc(domain)}</span>'
            f'<span class="count-chip">{count} finding{"s" if count != 1 else ""}</span>'
            f'<span style="margin-left:auto;">{_sev_badge(worst_sev)}</span>'
            f'</li>'
        )
    return f'<ul class="risk-list">{"".join(items)}</ul>'


def _build_exec_recommendations_html(findings: List[Dict]) -> str:
    critical = [f for f in findings if f.get("severity") == "Critical"]
    high = [f for f in findings if f.get("severity") == "High"]
    medium = [f for f in findings if f.get("severity") == "Medium"]

    items = []
    if critical:
        items.append(
            f"<li>Immediately address {len(critical)} critical security issue(s) — "
            f"action required within 24 hours.</li>"
        )
    if high:
        items.append(
            f"<li>Address {len(high)} high-priority issue(s) within 7 calendar days.</li>"
        )
    if medium:
        items.append(
            f"<li>Plan remediation for {len(medium)} medium-priority issue(s) within 30 days.</li>"
        )
    items.append("<li>Schedule a remediation verification session after fixes are deployed.</li>")
    items.append(
        "<li>Review the accompanying technical report with the engineering team "
        "for implementation guidance.</li>"
    )
    items.append(
        "<li>Assign named ownership for each identified issue with agreed target dates.</li>"
    )

    return f'<ul class="rec-list">{"".join(items)}</ul>'


def generate_executive_summary_html(
    register_path: Path,
    target_name: str = "",
    auditor: str = "",
    version: str = "DRAFT v0.1",
) -> Path:
    """
    Generate a self-contained HTML executive summary report.

    Non-technical — follows reporting-rules.md Rule 4.
    Returns the path to the generated .html file in reports/draft/.
    """
    REPORTS_DRAFT_DIR.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    filename = f"{today}-executive-summary.html"
    report_path = REPORTS_DRAFT_DIR / filename

    findings = _parse_register(register_path)
    severity_counts: Counter = Counter(f.get("severity", "Info") for f in findings)
    open_findings = [
        f for f in findings
        if f.get("status", "confirmed") not in ("closed", "mitigated")
    ]
    posture = _derive_posture(severity_counts, open_findings)

    app_name = target_name or "Target Application"
    page_title = f"Executive Summary — {app_name}"

    n_immediate = severity_counts.get("Critical", 0) + severity_counts.get("High", 0)
    n_near_term = severity_counts.get("Medium", 0)
    n_low = severity_counts.get("Low", 0) + severity_counts.get("Info", 0)

    next_steps_html = """<ul class="rec-list">
  <li>Review the detailed technical report for full finding descriptions and remediation guidance.</li>
  <li>Assign named ownership for each Critical and High finding with a confirmed remediation date.</li>
  <li>Schedule a re-test session after remediation to confirm finding closure per remediation-rules.md.</li>
  <li>Update the findings register before generating subsequent reports.</li>
</ul>"""

    disclaimer = """<div class="note-box" style="margin-top:2rem;">
  <h4>Non-Technical Disclaimer</h4>
  <ol>
    <li>This summary is prepared for senior management and does not contain technical implementation details.</li>
    <li>For technical details, refer to the accompanying Technical Report.</li>
    <li>All findings are based on evidence collected during the assessment period. Conditions may change.</li>
  </ol>
</div>"""

    body = f"""
{_top_bar(page_title, version)}
<div class="main-wrap">

  {_cover_block(
      "Executive Summary", app_name, "",
      today, auditor, "CLIENT RESTRICTED", version
  )}

  {_posture_banner(posture, severity_counts)}

  <!-- 1. Summary cards -->
  <div class="section">
    {_section_header(1, "Issues at a Glance")}
    {_sev_summary_cards(severity_counts)}
    <div class="table-wrap" style="margin-top:0.75rem;">
      <table class="data-table">
        <thead>
          <tr>
            <th>Category</th>
            <th style="text-align:center;">Count</th>
            <th>Action Required</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Requiring Immediate Action (Critical / High)</td>
            <td style="text-align:center;">{n_immediate}</td>
            <td>Within 7 days</td>
          </tr>
          <tr>
            <td>Requiring Near-Term Action (Medium)</td>
            <td style="text-align:center;">{n_near_term}</td>
            <td>Within 30 days</td>
          </tr>
          <tr>
            <td>Lower Priority (Low / Informational)</td>
            <td style="text-align:center;">{n_low}</td>
            <td>Next audit cycle</td>
          </tr>
          <tr>
            <td><strong>Total Issues Identified</strong></td>
            <td style="text-align:center;"><strong>{len(findings)}</strong></td>
            <td></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- 2. Key findings table (non-technical) -->
  <div class="section">
    {_section_header(2, "Key Findings")}
    {_build_exec_findings_table(findings)}
  </div>

  <!-- 3. Risk summary by domain -->
  <div class="section">
    {_section_header(3, "Risk Summary by Domain")}
    <div class="table-wrap" style="padding:1rem 1.25rem;">
      {_build_risk_domain_list(findings)}
    </div>
  </div>

  <!-- 4. Recommended actions -->
  <div class="section">
    {_section_header(4, "Recommended Actions")}
    <div class="table-wrap" style="padding:1rem 1.25rem;">
      {_build_exec_recommendations_html(findings)}
    </div>
  </div>

  <!-- 5. Next steps -->
  <div class="section">
    {_section_header(5, "Next Steps")}
    <div class="table-wrap" style="padding:1rem 1.25rem;">
      {next_steps_html}
    </div>
  </div>

  {disclaimer}

  {_report_footer(version, today)}

</div>
"""

    report_path.write_text(_html_shell(page_title, body), encoding="utf-8")
    logger.info("HTML executive summary written: %s", report_path)
    return report_path


# ---------------------------------------------------------------------------
# Public API — Remediation Plan
# ---------------------------------------------------------------------------

def _build_prio_section(
    css_class: str,
    label: str,
    sla: str,
    items: List[Dict],
    empty_msg: str,
) -> str:
    sla_badge = f'<span class="badge badge-{css_class.split("-")[1].capitalize()}">{_esc(sla)}</span>'

    if not items:
        body_html = f'<p style="color:var(--text-muted);font-size:0.875rem;">{_esc(empty_msg)}</p>'
    else:
        li_items = []
        for f in items:
            rec = f.get("recommendation", "")
            if len(rec) > 140:
                rec = rec[:137] + "..."
            li_items.append(
                f"<li>"
                f'<span class="find-id" style="flex-shrink:0;">{_esc(f["find_id"])}</span>'
                f'<span style="flex:1;">'
                f'<strong>{_esc(f.get("title", "Untitled"))}</strong><br>'
                f'<span style="color:var(--text-muted);font-size:0.82rem;">{_esc(rec)}</span>'
                f"</span>"
                f"</li>"
            )
        body_html = f'<ul>{"".join(li_items)}</ul>'

    return f"""<div class="priority-section {css_class}">
  <div class="prio-header">
    <h3>{_esc(label)}</h3>
    {sla_badge}
    <span style="margin-left:0.5rem;color:var(--text-muted);font-size:0.8rem;">
      {len(items)} finding{"s" if len(items) != 1 else ""}
    </span>
  </div>
  <div class="prio-body">
    {body_html}
  </div>
</div>"""


def generate_remediation_plan_html(
    register_path: Path,
    target_name: str = "",
) -> Path:
    """
    Generate a self-contained HTML remediation plan.

    Returns the path to the generated .html file in reports/draft/.
    """
    REPORTS_DRAFT_DIR.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    filename = f"{today}-remediation-plan.html"
    report_path = REPORTS_DRAFT_DIR / filename

    findings = _parse_register(register_path)
    open_findings = [
        f for f in findings
        if f.get("status", "confirmed") not in ("closed", "mitigated", "accepted-risk")
    ]
    open_findings.sort(key=lambda f: _severity_order(f.get("severity", "Info")))

    immediate  = [f for f in open_findings if f.get("severity") == "Critical"]
    short_term = [f for f in open_findings if f.get("severity") == "High"]
    near_term  = [f for f in open_findings if f.get("severity") == "Medium"]
    long_term  = [f for f in open_findings if f.get("severity") in ("Low", "Info")]

    app_name = target_name or "Target Application"
    version = "DRAFT v0.1"
    page_title = f"Remediation Plan — {app_name}"

    closure_note = """<div class="note-box">
  <h4>Closure Requirements (remediation-rules.md Rule 5)</h4>
  <ol>
    <li>The responsible team provides evidence of the fix:
        pull request or commit reference, configuration change capture (EVID-labeled),
        updated dependency manifest, or written process description.</li>
    <li>The security auditor reviews the evidence and confirms it addresses the finding.</li>
    <li>The security auditor performs a verification re-test and records the result
        as a new EVID-labeled evidence item.</li>
    <li>Both the fix evidence and re-test evidence are referenced in the finding record
        before the finding may be moved to Closed status.</li>
  </ol>
</div>"""

    body = f"""
{_top_bar(page_title, version)}
<div class="main-wrap">

  {_cover_block(
      "Remediation Plan", app_name, "",
      today, "", "CLIENT RESTRICTED", version
  )}

  <!-- Open findings summary -->
  <div class="section">
    {_section_header(1, "Open Findings Summary")}
    <div class="table-wrap" style="margin-bottom:1.5rem;">
      <table class="data-table">
        <thead>
          <tr>
            <th>Priority</th>
            <th>Severity</th>
            <th style="text-align:center;">Count</th>
            <th>SLA</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Priority 1 — Immediate</td>
            <td>{_sev_badge("Critical")}</td>
            <td style="text-align:center;">{len(immediate)}</td>
            <td>24 hours</td>
          </tr>
          <tr>
            <td>Priority 2 — Short Term</td>
            <td>{_sev_badge("High")}</td>
            <td style="text-align:center;">{len(short_term)}</td>
            <td>7 calendar days</td>
          </tr>
          <tr>
            <td>Priority 3 — Near Term</td>
            <td>{_sev_badge("Medium")}</td>
            <td style="text-align:center;">{len(near_term)}</td>
            <td>30 calendar days</td>
          </tr>
          <tr>
            <td>Priority 4 — Improvement Cycle</td>
            <td>{_sev_badge("Low")} {_sev_badge("Info")}</td>
            <td style="text-align:center;">{len(long_term)}</td>
            <td>90 calendar days</td>
          </tr>
          <tr>
            <td><strong>Total Open Findings</strong></td>
            <td></td>
            <td style="text-align:center;"><strong>{len(open_findings)}</strong></td>
            <td></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Priority sections -->
  <div class="section">
    {_section_header(2, "Remediation Actions")}

    {_build_prio_section(
        "prio-crit",
        "Priority 1 — Immediate (Critical Findings)",
        "24 hours",
        immediate,
        "No critical findings — no immediate action required.",
    )}

    {_build_prio_section(
        "prio-high",
        "Priority 2 — Short Term (High Findings)",
        "7 calendar days",
        short_term,
        "No high severity findings in this category.",
    )}

    {_build_prio_section(
        "prio-med",
        "Priority 3 — Near Term (Medium Findings)",
        "30 calendar days",
        near_term,
        "No medium severity findings in this category.",
    )}

    {_build_prio_section(
        "prio-low",
        "Priority 4 — Improvement Cycle (Low / Info Findings)",
        "90 calendar days",
        long_term,
        "No low or informational findings in this category.",
    )}
  </div>

  {closure_note}

  {_report_footer(version, today)}

</div>
"""

    report_path.write_text(_html_shell(page_title, body), encoding="utf-8")
    logger.info("HTML remediation plan written: %s", report_path)
    return report_path
