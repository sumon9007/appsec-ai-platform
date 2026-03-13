# Reporting Prompts

Reusable reasoning helpers for generating reports and remediation plans.

---

## Generate Security Report

**Objective:** Convert the findings register into a structured technical report and executive summary.

**Python CLI:**
```bash
python scripts/run_audit.py report technical
python scripts/run_audit.py report executive
```

**Manual steps if needed:**

1. Read `audit-runs/active/findings-register.md` — validate all entries have severity, evidence refs, and recommendations.
2. Apply `.claude/rules/reporting-rules.md` — severity vocabulary, evidence references, no speculative claims.
3. Structure the technical report:
   - Overall posture statement (one sentence — mandatory)
   - Scope and methodology
   - Findings table (ID, title, domain, severity, status)
   - Full detail per finding
   - Review gaps section
   - Acceptance criteria impact
   - Prioritized next actions
4. For the executive summary: no technical terms, no CVE IDs, no header names. Plain-language risk narrative only.
5. Save to `reports/draft/` using filename convention: `YYYY-MM-DD-[type]-report.md`
6. Label as `DRAFT v0.1` until reviewed and approved.

---

## Risk Prioritization

When ordering findings for the remediation plan, apply this sequence:

1. **Critical** — list first, with 24-hour SLA noted
2. **High** — list second, with 7-day SLA noted
3. **Medium** — list third, with 30-day SLA noted
4. **Low** — list last, with 90-day SLA noted
5. **Info** — include as a separate hardening recommendations section

Within the same severity level, prioritize by:
- exploitability (can it be exploited without special conditions?)
- exposure (is it on a public-facing surface?)
- data sensitivity (does it affect sensitive or regulated data?)
- remediation effort (prefer quick wins where risk reduction is high)

---

## Generate Remediation Plan

**Objective:** Produce a structured, prioritized action plan from confirmed and suspected findings.

**Python CLI:**
```bash
python scripts/run_audit.py report remediation
```

**Manual structure:**

**Immediate Actions (Critical — within 24 hours)**
- List each Critical finding with: ID, title, recommended fix, owner

**Short-Term Actions (High — within 7 days)**
- List each High finding with: ID, title, recommended fix, owner

**Scheduled Actions (Medium — within 30 days)**
- List each Medium finding grouped by theme if possible

**Backlog Items (Low — within 90 days)**
- List each Low finding as backlog items

**Hardening Opportunities (Info)**
- Optional improvements with no SLA

Each action must have a specific, testable recommendation — not a vague instruction. Include evidence of fix requirements per `.claude/rules/remediation-rules.md`.
