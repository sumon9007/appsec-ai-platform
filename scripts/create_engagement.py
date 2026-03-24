#!/usr/bin/env python3
"""
create_engagement.py — Scaffold a new per-engagement security audit package.

Creates a fully populated engagement directory under engagements/<ENGAGEMENT_ID>/
with pre-filled context files, a starter findings register, session memory, and
all required subdirectories.

Usage:
    python scripts/create_engagement.py AUDIT-2026-ACME-001 \\
        --target-name "Acme Corp App" \\
        --target-url "https://app.acme.com" \\
        --auditor "Jane Smith" \\
        --environment Production \\
        --auth-mode passive-only \\
        --audit-type one-off \\
        --activate

    # Preview without creating anything
    python scripts/create_engagement.py AUDIT-2026-ACME-001 \\
        --target-name "Acme Corp" --target-url "https://acme.com" \\
        --dry-run

Engagement ID format: AUDIT-YYYY-CLIENT-NNN
  YYYY   = 4-digit year (e.g. 2026)
  CLIENT = uppercase letters/digits, no spaces (e.g. ACME, DR, CLIENTA)
  NNN    = 3-digit sequence number (001, 002, ...)
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path
from textwrap import dedent


def _inline(text: str, indent: int = 8) -> str:
    """Prepare a multi-line string for safe inline interpolation inside a dedent() template.

    Python f-strings apply the template's leading whitespace only to the *first* line of a
    substituted value — subsequent lines start at column 0 regardless of the `{var}`
    position in the template.  This helper rewrites the value so every newline is followed
    by `indent` spaces, meaning dedent() will correctly remove the common prefix from all
    lines in the final output.

    Usage inside a template indented by 8 spaces:
        {_inline(some_multiline_var, 8)}   # the leading 8 spaces come from the template
    """
    pad = " " * indent
    return text.strip().replace("\n", "\n" + pad)


# ── Project root resolution ───────────────────────────────────────────────────


def _find_project_root() -> Path:
    """Walk upward from this script until a directory containing .claude/ is found."""
    for parent in Path(__file__).resolve().parents:
        if (parent / ".claude").is_dir():
            return parent
    return Path(__file__).resolve().parents[1]


PROJECT_ROOT    = _find_project_root()
ENGAGEMENTS_DIR = PROJECT_ROOT / "engagements"
ACTIVE_MD       = PROJECT_ROOT / ".claude" / "context" / "active.md"
ENV_FILE        = PROJECT_ROOT / ".env"


# ── Engagement ID validation ──────────────────────────────────────────────────

_EID_PATTERN = re.compile(r"^AUDIT-\d{4}-[A-Z0-9]+-\d{3}$")


def _validate_id(eid: str) -> None:
    if not _EID_PATTERN.match(eid):
        _die(
            f"Engagement ID '{eid}' is not valid.\n"
            "  Required format: AUDIT-YYYY-CLIENT-NNN\n"
            "  Examples: AUDIT-2026-ACME-001  AUDIT-2026-DR-002  AUDIT-2027-BANKCO-001"
        )


def _die(msg: str) -> None:
    print(f"\nERROR: {msg}\n", file=sys.stderr)
    sys.exit(1)


# ── Directory structure ───────────────────────────────────────────────────────

# All subdirectories to create under engagements/<EID>/
_DIRS = [
    "context",
    "audit-runs/active",
    "audit-runs/completed",
    "evidence/raw",
    "evidence/reviewed",
    "evidence/summarized",
    "reports/draft",
    "reports/final",
    "audits/weekly",
    "audits/monthly",
    "audits/quarterly",
    "audits/annual",
    "audits/release",
    "output",
    "memory",
]

# Directories that will be empty and need a .gitkeep placeholder
_GITKEEP_DIRS = [
    "audit-runs/completed",
    "evidence/raw",
    "evidence/reviewed",
    "evidence/summarized",
    "reports/draft",
    "reports/final",
    "audits/weekly",
    "audits/monthly",
    "audits/quarterly",
    "audits/annual",
    "audits/release",
    "output",
]


# ── Template renderers ────────────────────────────────────────────────────────


def _render_engagement_summary(eid: str, target_name: str, target_url: str,
                               auditor: str, environment: str, auth_mode: str,
                               audit_type: str, today: str) -> str:
    """Token-efficient first-read briefing. ~35 lines. Load at every session start."""
    mode_label = {
        "passive-only":   "Passive only",
        "active-staging": "Active — staging",
        "active-full":    "Active — full",
    }[auth_mode]
    type_label = {
        "one-off":      "One-off",
        "weekly":       "Weekly",
        "monthly":      "Monthly",
        "quarterly":    "Quarterly",
        "annual":       "Annual",
        "release-gate": "Release gate",
    }[audit_type]
    return dedent(f"""\
        <!-- READ THIS FIRST — compressed briefing for any Claude session -->
        # {eid}

        | Field | Value |
        |-------|-------|
        | Target | {target_name} |
        | URL | {target_url} |
        | Env | {environment} |
        | Auth | ⚠ PENDING — no audit activity permitted yet |
        | Mode | {mode_label} |
        | Type | {type_label} |
        | Auditor | {auditor} |
        | Window | [TBD] → [TBD] |
        | Created | {today} |

        ## Findings Snapshot
        | Sev | Open | Closed |
        |-----|------|--------|
        | Critical | 0 | 0 |
        | High | 0 | 0 |
        | Medium | 0 | 0 |
        | Low | 0 | 0 |
        | Info | 0 | 0 |

        ## Evidence & Reports
        - Raw evidence: 0 · Reviewed: 0 · Reports: none

        ## Blockers
        - [ ] Authorization not confirmed — update `context/audit-context.md`

        ## Next Session
        1. Set `Authorization Status: CONFIRMED` + fill authorizing party details
        2. Set testing window in `context/scope.md`
        3. Run `python scripts/run_audit.py audit headers` to start

        ## Key Decisions
        *(none yet)*

        ---
        *Updated: {today}*
    """)


def _render_audit_context(eid: str, target_name: str, target_url: str,
                          auditor: str, environment: str, auth_mode: str,
                          audit_type: str, today: str) -> str:
    """Auth gate + stable engagement metadata. ~35 lines."""
    auth_scope_map = {
        "passive-only":   "Passive review only — no active testing, no payload submission",
        "active-staging": "Active testing on staging environment only",
        "active-full":    "[TBD — specify exact environments and constraints]",
    }
    cadence_map = {
        "one-off":      "One-off",
        "weekly":       "Weekly",
        "monthly":      "Monthly",
        "quarterly":    "Quarterly",
        "annual":       "Annual",
        "release-gate": "Per-release",
    }
    return dedent(f"""\
        # Audit Context

        > **AUTH GATE** — `Authorization Status` must be `CONFIRMED` before any audit activity.

        ## Engagement
        | Field | Value |
        |-------|-------|
        | ID | {eid} |
        | Auditor | {auditor} |
        | Started | {today} |
        | Report To | [TBD] |

        ## Target
        | Field | Value |
        |-------|-------|
        | Application | {target_name} |
        | URL(s) | {target_url} |
        | Environment | {environment} |

        ## Authorization
        | Field | Value |
        |-------|-------|
        | **Status** | **PENDING** |
        | Authorized By | [TBD] |
        | Auth Date | [TBD] |
        | Reference | [TBD] |
        | Mode | {auth_scope_map[auth_mode]} |

        ## Audit Type
        | Type | Cadence | Trigger |
        |------|---------|---------|
        | {audit_type.replace("-", " ").title()} | {cadence_map[audit_type]} | [TBD] |

        ## Constraints & Special Instructions
        [NONE]

        ## Prior Engagement
        | Field | Value |
        |-------|-------|
        | Prior Audit ID | [UNKNOWN] |
        | Open Carryover Findings | [UNKNOWN] |
        | Known Changes | [UNKNOWN] |

        ---
        *Updated: {today}*
    """)


def _render_target_profile(target_name: str, target_url: str,
                            environment: str, today: str) -> str:
    """Factual application reference. Read when tech context or auth model is needed."""
    return dedent(f"""\
        # Target Profile

        > Read when: tech stack, auth model, integrations, or data sensitivity matter for a finding.

        ## Application
        | Field | Value |
        |-------|-------|
        | Name | {target_name} |
        | Purpose | [TBD] |
        | Criticality | [TBD: Critical / High / Medium / Low] |
        | Data Class | [TBD: Confidential / Internal / Public] |
        | Owner | [UNKNOWN] |
        | Version | [UNKNOWN] |

        ## Tech Stack
        | Layer | Technology |
        |-------|-----------|
        | Frontend | [UNKNOWN] |
        | Backend | [UNKNOWN] |
        | Language | [UNKNOWN] |
        | Database | [UNKNOWN] |
        | Cache / Queue | [UNKNOWN] |
        | API Style | [UNKNOWN] |

        ## Hosting
        | Field | Value |
        |-------|-------|
        | Cloud / Provider | [UNKNOWN] |
        | CDN / WAF | [UNKNOWN] |
        | Deployment | [UNKNOWN] |
        | Environment | {environment} |

        ## Auth Model
        | Field | Value |
        |-------|-------|
        | Mechanism | [UNKNOWN] |
        | IdP | [UNKNOWN] |
        | MFA | [UNKNOWN] |
        | Sessions | [UNKNOWN] |
        | Password Policy | [UNKNOWN] |

        ## User Roles
        | Role | Description |
        |------|-------------|
        | [TBD] | [TBD] |

        ## Integrations & Third Parties
        | System | Type | Data Shared | Trust |
        |--------|------|-------------|-------|
        | [TBD] | [TBD] | [TBD] | [TBD] |

        ## API Surface
        | Field | Value |
        |-------|-------|
        | Public API | [UNKNOWN] |
        | Auth | [UNKNOWN] |
        | Docs | [UNKNOWN] |

        ## Observations
        *(none yet)*

        ---
        *Updated: {today}*
    """)


def _render_scope(target_url: str, auth_mode: str, today: str) -> str:
    """Scope boundaries — pure data, no process instructions. Read when starting a domain review."""
    active_env_map = {
        "passive-only":   "None — passive review only",
        "active-staging": "Staging only",
        "active-full":    "[TBD — specify]",
    }
    prohibited_passive  = "Social engineering · DoS · Active exploitation / fuzzing / brute force"
    prohibited_active   = "Social engineering · DoS · Data destruction beyond test accounts"
    prohibited = prohibited_passive if auth_mode == "passive-only" else prohibited_active
    return dedent(f"""\
        # Scope

        > Read when: starting a domain review, classifying OOS observations, or verifying what is permitted.

        ## In-Scope Assets
        | URL / Domain | Env | Notes |
        |---|---|---|
        | {target_url} | [TBD] | Primary target |

        ### In-Scope Features
        - [TBD]

        ## Out-of-Scope
        | Item | Reason |
        |------|--------|
        | Third-party embedded services | Not owned by target |

        ### Prohibited Techniques
        {prohibited}

        ## Testing Boundaries
        | Boundary | Constraint |
        |----------|-----------|
        | Active testing env | {active_env_map[auth_mode]} |
        | Window | [TBD] → [TBD] |
        | Report due | [TBD] |
        | Data creation | [TBD] |
        | Credentials | [TBD — do not record here] |

        ## Test Accounts
        | Role | Email | Notes |
        |------|-------|-------|
        | [TBD] | [TBD] | [TBD] |

        ## Scope Change Log
        | Date | Change | Authorized By | Reference |
        |------|--------|---------------|-----------|
        | {today} | Initial scope | [TBD] | [TBD] |

        ---
        *Updated: {today}*
    """)


def _render_assumptions(today: str) -> str:
    """Working assumptions and unknowns. Read when labeling findings or assessing confidence."""
    return dedent(f"""\
        # Assumptions & Unknowns

        > Findings influenced by assumptions → label `[ASSUMED]`. Unresolved unknowns → `[UNKNOWN]`.
        > Read when: labeling a finding, assessing confidence, or checking for blockers.

        ## Working Assumptions
        | ID | Assumption | Basis | Status |
        |----|-----------|-------|--------|
        | A-001 | [TBD] | [TBD] | ASSUMED |

        ## Known Unknowns
        | ID | Unknown | Impact | Status |
        |----|---------|--------|--------|
        | U-001 | Full attack surface beyond public pages | Limits breadth | OPEN |
        | U-002 | WAF / hosting architecture | Infrastructure observations | OPEN |
        | U-003 | Remediation ownership | SLA assignment | OPEN |

        ## Client Dependencies
        | Item | Requested | Received |
        |------|-----------|----------|
        | Technical POC | {today} | PENDING |
        | Architecture docs | {today} | PENDING |
        | Prior audit report | {today} | PENDING |

        ## Validation Log
        | Date | ID | New Status | Notes |
        |------|-----|-----------|-------|
        | — | — | — | — |

        ---
        *Updated: {today}*
    """)


def _render_findings_register(eid: str, target_name: str,
                               target_url: str, today: str) -> str:
    return dedent(f"""\
        # Findings Register

        **Engagement:** {eid}
        **Target:** {target_name} ({target_url})

        This register is the single source of truth for all security findings in this engagement.

        Every confirmed finding, suspected issue, and review gap must be recorded here.

        Update this register at the end of every audit session and before generating any report.

        *Created: {today}*

        ---

        ## Findings Summary

        | Finding ID | Title | Domain | Severity | Confidence | Status |
        |------------|-------|--------|----------|------------|--------|
        | (none yet) | — | — | — | — | — |

        ---

        ## Open Findings

        *(No findings recorded yet. Findings will be appended here as the audit progresses.)*

        ---

        ## Closed Findings

        *(No findings closed yet.)*

        ---

        ## SLA Tracking

        | Severity | SLA | Open | Overdue |
        |----------|-----|------|---------|
        | Critical | 24 hours | 0 | 0 |
        | High | 7 days | 0 | 0 |
        | Medium | 30 days | 0 | 0 |
        | Low | 90 days | 0 | 0 |
        | Info | Next audit cycle | 0 | — |

        ---

        *Last updated: {today}*
    """)


def _render_readme(eid: str, target_name: str, target_url: str, auditor: str,
                   environment: str, auth_mode: str, audit_type: str, today: str) -> str:
    """File index and load order. ~25 lines. The human-facing entry point."""
    return dedent(f"""\
        # {eid} — {target_name}

        **URL:** {target_url}  |  **Env:** {environment}  |  **Mode:** {auth_mode}  |  **Type:** {audit_type}
        **Status:** Authorization PENDING  |  **Auditor:** {auditor}  |  **Created:** {today}

        ---

        ## File Index & Load Order

        > **Token-efficient load order:** `engagement-summary.md` → `MEMORY.md` → `audit-context.md` → [others as needed]

        | File | Purpose | Load When |
        |------|---------|-----------|
        | `context/engagement-summary.md` | Status, findings snapshot, next steps | **Always — load first** |
        | `memory/MEMORY.md` | Decisions, questions, session notes | **Always** |
        | `context/audit-context.md` | Auth gate, engagement metadata | **Always** |
        | `context/scope.md` | In/out-of-scope assets, permitted activities | Starting a domain review |
        | `context/target-profile.md` | Tech stack, auth model, integrations | Tech context needed |
        | `context/assumptions.md` | Working assumptions, unknowns, blockers | Labeling findings |
        | `audit-runs/active/findings-register.md` | All findings for this engagement | Reviewing / adding findings |
        | `evidence/raw/` | Collected evidence | Classifying evidence |
        | `reports/` | Draft and final reports | Report generation |

        ---
        *Updated: {today}*
    """)


def _render_memory(eid: str, target_name: str,
                   target_url: str, today: str) -> str:
    """Rolling operational memory. Update at end of each session. No static conventions — those live in rules."""
    return dedent(f"""\
        # Memory: {eid}

        **Target:** {target_name} · {target_url}  |  **Updated:** {today}

        ## State
        | Counter | Value |
        |---------|-------|
        | Findings open / closed | 0 / 0 |
        | Evidence raw / reviewed | 0 / 0 |
        | Sessions completed | 0 |
        | Reports generated | 0 |

        ## Key Decisions
        | Date | Decision | Rationale |
        |------|----------|-----------|
        | — | — | — |

        ## Open Questions
        - (none)

        ## Next Steps
        1. Confirm authorization in `context/audit-context.md`
        2. Set testing window and scope dates

        ## Session Notes
        <!-- Append at end of each session — newest first -->

        ---
        *Updated: {today}*
    """)


def _render_active_md(eid: str, target_name: str, today: str) -> str:
    return dedent(f"""\
        # Active Engagement Pointer

        This file identifies the currently active engagement. Context files, findings, and evidence for each engagement are stored under `engagements/<ENGAGEMENT_ID>/` — not in this directory.

        ---

        ## Currently Active Engagement

        | Field | Value |
        |-------|-------|
        | **Engagement ID** | {eid} |
        | **Target** | {target_name} |
        | **Engagement Directory** | `engagements/{eid}/` |

        ---

        ## How to Read Context

        For the currently active engagement, read:

        - `engagements/{eid}/context/audit-context.md`
        - `engagements/{eid}/context/target-profile.md`
        - `engagements/{eid}/context/scope.md`
        - `engagements/{eid}/context/assumptions.md`

        These are the authoritative source of truth — **not** this directory.

        ---

        ## How to Switch Engagements

        1. Update `ACTIVE_ENGAGEMENT` in your `.env` file to the new engagement ID.
        2. Update the **Currently Active Engagement** table above.
        3. Run `python scripts/run_audit.py session status` to confirm paths resolve correctly.

        To create a new engagement:
        ```bash
        python scripts/create_engagement.py AUDIT-YYYY-CLIENT-NNN \\
            --target-name "Client Name" \\
            --target-url "https://target.com" \\
            --activate
        ```

        ---

        *Last updated: {today}*
    """)


# ── Engagements index updater ─────────────────────────────────────────────────


def _update_engagements_index(eid: str, target_name: str, target_url: str,
                               today: str, dry_run: bool) -> None:
    """Append a row to the engagements/README.md engagement table."""
    index = ENGAGEMENTS_DIR / "README.md"
    if not index.exists():
        return

    content = index.read_text()
    if eid in content:
        return  # already listed

    marker = "| Engagement ID | Target | Status | Started |"
    if marker not in content:
        return  # table structure not found — don't corrupt the file

    new_row = (
        f"| {eid} | {target_name} ({target_url}) "
        f"| Active — Authorization PENDING | {today} |"
    )
    # Find the last table row and insert after it
    lines = content.splitlines()
    last_table_row = -1
    in_table = False
    for i, line in enumerate(lines):
        if marker in line:
            in_table = True
        if in_table and line.startswith("|"):
            last_table_row = i
        elif in_table and not line.startswith("|") and last_table_row >= 0:
            break  # left the table

    if last_table_row >= 0:
        lines.insert(last_table_row + 1, new_row)
        updated = "\n".join(lines) + ("\n" if content.endswith("\n") else "")
        if dry_run:
            print(f"  [UPDATE] engagements/README.md  +row for {eid}")
        else:
            index.write_text(updated)
            print(f"  Updated  engagements/README.md")


# ── .env updater ──────────────────────────────────────────────────────────────


def _update_env(eid: str, dry_run: bool) -> None:
    if not ENV_FILE.exists():
        msg = f".env not found — create it from .env.example and set ACTIVE_ENGAGEMENT={eid}"
        print(f"  {'[WARN] ' if dry_run else 'WARNING: '}{msg}")
        return

    text = ENV_FILE.read_text()
    if re.search(r"^ACTIVE_ENGAGEMENT=", text, re.MULTILINE):
        updated = re.sub(
            r"^ACTIVE_ENGAGEMENT=.*$",
            f"ACTIVE_ENGAGEMENT={eid}",
            text,
            flags=re.MULTILINE,
        )
        if dry_run:
            print(f"  [UPDATE] .env  ACTIVE_ENGAGEMENT → {eid}")
        else:
            ENV_FILE.write_text(updated)
            print(f"  Updated  .env  (ACTIVE_ENGAGEMENT={eid})")
    else:
        if dry_run:
            print(f"  [APPEND] .env  ACTIVE_ENGAGEMENT={eid}")
        else:
            with ENV_FILE.open("a") as f:
                f.write(f"\nACTIVE_ENGAGEMENT={eid}\n")
            print(f"  Updated  .env  (ACTIVE_ENGAGEMENT={eid} appended)")


# ── Main scaffold function ────────────────────────────────────────────────────


def create_engagement(
    eid: str,
    target_name: str,
    target_url: str,
    auditor: str,
    environment: str,
    auth_mode: str,
    audit_type: str,
    activate: bool,
    force: bool,
    dry_run: bool,
) -> None:
    today    = date.today().isoformat()
    eng_dir  = ENGAGEMENTS_DIR / eid
    prefix   = "[DRY RUN] " if dry_run else ""

    # ── Guard: already exists ────────────────────────────────────────────────
    if eng_dir.exists() and not force:
        _die(
            f"Engagement directory already exists: {eng_dir}\n"
            "  Use --force to overwrite."
        )

    print(f"\n{prefix}Scaffolding engagement: {eid}")
    print(f"  Target      : {target_name}")
    print(f"  URL         : {target_url}")
    print(f"  Environment : {environment}")
    print(f"  Auth mode   : {auth_mode}")
    print(f"  Audit type  : {audit_type}")
    print(f"  Auditor     : {auditor}")
    print(f"  Directory   : {eng_dir}")
    print()

    # ── Create directories ───────────────────────────────────────────────────
    if dry_run:
        for d in _DIRS:
            print(f"  [DIR]    engagements/{eid}/{d}/")
    else:
        for d in _DIRS:
            (eng_dir / d).mkdir(parents=True, exist_ok=True)
        print(f"  Created  {len(_DIRS)} directories")

    # ── Compose files ────────────────────────────────────────────────────────
    files: dict[str, str] = {
        "context/engagement-summary.md": _render_engagement_summary(
            eid, target_name, target_url, auditor, environment, auth_mode, audit_type, today
        ),
        "context/audit-context.md": _render_audit_context(
            eid, target_name, target_url, auditor, environment, auth_mode, audit_type, today
        ),
        "context/target-profile.md": _render_target_profile(
            target_name, target_url, environment, today
        ),
        "context/scope.md": _render_scope(target_url, auth_mode, today),
        "context/assumptions.md": _render_assumptions(today),
        "audit-runs/active/findings-register.md": _render_findings_register(
            eid, target_name, target_url, today
        ),
        "README.md": _render_readme(
            eid, target_name, target_url, auditor, environment, auth_mode, audit_type, today
        ),
        "memory/MEMORY.md": _render_memory(eid, target_name, target_url, today),
    }

    for d in _GITKEEP_DIRS:
        files[f"{d}/.gitkeep"] = ""

    if dry_run:
        for rel in files:
            tag = "[FILE]" if files[rel] else "[KEEP]"
            print(f"  {tag}    engagements/{eid}/{rel}")
    else:
        for rel, content in files.items():
            (eng_dir / rel).write_text(content)
        print(f"  Wrote    {len(files)} files ({len(files) - len(_GITKEEP_DIRS)} content, {len(_GITKEEP_DIRS)} .gitkeep)")

    # ── Activation ───────────────────────────────────────────────────────────
    if activate:
        print()
        if dry_run:
            print(f"  [UPDATE] .claude/context/active.md  → {eid}")
        else:
            ACTIVE_MD.write_text(_render_active_md(eid, target_name, today))
            print(f"  Updated  .claude/context/active.md")
        _update_env(eid, dry_run)

    # ── Engagement index ─────────────────────────────────────────────────────
    _update_engagements_index(eid, target_name, target_url, today, dry_run)

    # ── Summary ──────────────────────────────────────────────────────────────
    print()
    if dry_run:
        print("[DRY RUN COMPLETE] — no files written.")
        print(f"Remove --dry-run to create the engagement.")
    else:
        print(f"Engagement {eid} created successfully.")
        print()
        print("Next steps:")
        print(f"  1. Confirm authorization  →  engagements/{eid}/context/audit-context.md")
        print(f"                               Set 'Authorization Status' to CONFIRMED")
        print(f"  2. Define scope           →  engagements/{eid}/context/scope.md")
        print(f"  3. Build target profile   →  engagements/{eid}/context/target-profile.md")
        if activate:
            print(f"  4. Verify paths           →  python scripts/run_audit.py session status")
        else:
            print(f"  4. Activate engagement    →  add ACTIVE_ENGAGEMENT={eid} to .env")
            print(f"     Verify paths           →  python scripts/run_audit.py session status")
        print(f"  5. Start the audit        →  python scripts/run_audit.py audit full")
    print()


# ── CLI ───────────────────────────────────────────────────────────────────────


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="create_engagement.py",
        description=(
            "Scaffold a new per-engagement security audit package under "
            "engagements/<ENGAGEMENT_ID>/."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent("""\
            Engagement ID format:  AUDIT-YYYY-CLIENT-NNN
              YYYY    4-digit year                       (e.g. 2026)
              CLIENT  uppercase letters/digits, no spaces (e.g. ACME, BANKCO, DR)
              NNN     3-digit sequence number             (001, 002, ...)

            Examples:
              # Minimal (fills placeholders for unspecified fields)
              python scripts/create_engagement.py AUDIT-2026-ACME-001

              # Full specification
              python scripts/create_engagement.py AUDIT-2026-ACME-001 \\
                  --target-name "Acme Corp Portal" \\
                  --target-url  "https://portal.acme.com" \\
                  --auditor     "Jane Smith" \\
                  --environment Production \\
                  --auth-mode   passive-only \\
                  --audit-type  one-off \\
                  --activate

              # Active testing on staging
              python scripts/create_engagement.py AUDIT-2026-ACME-002 \\
                  --target-name "Acme Corp (Staging)" \\
                  --target-url  "https://staging.acme.com" \\
                  --auth-mode   active-staging \\
                  --audit-type  release-gate \\
                  --activate

              # Preview only
              python scripts/create_engagement.py AUDIT-2026-ACME-001 \\
                  --target-name "Acme Corp" --target-url "https://acme.com" \\
                  --dry-run
        """),
    )

    parser.add_argument(
        "engagement_id",
        metavar="ENGAGEMENT_ID",
        help="Unique engagement ID — format AUDIT-YYYY-CLIENT-NNN",
    )
    parser.add_argument(
        "--target-name",
        default="[REPLACE: Application Name]",
        metavar="NAME",
        help="Target application or client name (default: placeholder)",
    )
    parser.add_argument(
        "--target-url",
        default="[REPLACE: https://target-url]",
        metavar="URL",
        help="Primary target URL (default: placeholder)",
    )
    parser.add_argument(
        "--auditor",
        default=os.getenv("AUDIT_DEFAULT_AUDITOR", "unknown-auditor"),
        metavar="NAME",
        help=(
            "Auditor name. Defaults to AUDIT_DEFAULT_AUDITOR env var, "
            "or 'unknown-auditor' if unset."
        ),
    )
    parser.add_argument(
        "--environment",
        default="Production",
        choices=["Production", "Staging", "QA", "Development"],
        metavar="ENV",
        help="Target environment: Production|Staging|QA|Development (default: Production)",
    )
    parser.add_argument(
        "--auth-mode",
        default="passive-only",
        choices=["passive-only", "active-staging", "active-full"],
        metavar="MODE",
        help=(
            "Authorization mode: passive-only|active-staging|active-full "
            "(default: passive-only)"
        ),
    )
    parser.add_argument(
        "--audit-type",
        default="one-off",
        choices=["one-off", "weekly", "monthly", "quarterly", "annual", "release-gate"],
        metavar="TYPE",
        help=(
            "Audit type: one-off|weekly|monthly|quarterly|annual|release-gate "
            "(default: one-off)"
        ),
    )
    parser.add_argument(
        "--activate",
        action="store_true",
        help="After creating, activate this engagement: update .env and .claude/context/active.md",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing engagement directory if it already exists",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview all actions without writing any files",
    )

    return parser


def main() -> None:
    parser = _build_parser()
    args   = parser.parse_args()

    _validate_id(args.engagement_id)

    create_engagement(
        eid         = args.engagement_id,
        target_name = args.target_name,
        target_url  = args.target_url,
        auditor     = args.auditor,
        environment = args.environment,
        auth_mode   = args.auth_mode,
        audit_type  = args.audit_type,
        activate    = args.activate,
        force       = args.force,
        dry_run     = args.dry_run,
    )


if __name__ == "__main__":
    main()
