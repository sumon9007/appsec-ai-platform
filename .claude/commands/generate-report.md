> **Python CLI** (primary): `python scripts/run_audit.py report technical   # also: report executive`
> This command file is a methodology reference. Run the Python CLI command above for automated execution.

# Command: /generate-report

## Objective

Generate a structured security audit report from the current findings register — both a technical report and a non-technical executive summary.

---

## Pre-Conditions

1. `audit-runs/active/findings-register.md` is populated and current.
2. All findings have severity, confidence, status, evidence references, and recommendations.
3. Authorization status in `.claude/context/audit-context.md` is CONFIRMED.

---

## Steps

### Step 1: Read Context

1. Read `.claude/context/audit-context.md` — confirm audit ID, target, auditor
2. Read `.claude/context/target-profile.md` — confirm application name and scope
3. Read `.claude/context/scope.md` — confirm what was and was not tested
4. Read `.claude/rules/reporting-rules.md` — apply all output standards

### Step 2: Validate the Findings Register

1. Read `audit-runs/active/findings-register.md`
2. Check:
   - All findings have a valid severity (Critical / High / Medium / Low / Info)
   - All findings have at least one EVID- reference
   - No duplicate Finding IDs
   - All open findings have a recommendation
3. Note any validation gaps — do not fabricate missing data

### Step 3: Generate Technical Report

Use `.claude/skills/report-writer/SKILL.md` and `.claude/templates/` to produce:

- Report metadata (version, date, auditor, target)
- Overall security posture statement (one sentence — mandatory)
- Scope summary
- Methodology summary
- Findings table (ID, title, domain, severity, status)
- Full finding detail for each confirmed and suspected finding
- Review gaps section
- Acceptance criteria impact (see `.claude/docs/acceptance-criteria.md`)
- Prioritized next actions

Save to: `reports/draft/YYYY-MM-DD-technical-report.md` — label DRAFT v0.1

### Step 4: Generate Executive Summary

Non-technical language only. Do not include HTTP header names, CVE IDs, code snippets, IP addresses, or framework-specific terms.

Include:
- Overall risk posture in plain language
- Finding counts by severity
- Top 3 issues in business-impact terms
- Key actions and timelines

Save to: `reports/draft/YYYY-MM-DD-executive-summary.md` — label DRAFT v0.1

---

## Output

- `reports/draft/YYYY-MM-DD-technical-report.md`
- `reports/draft/YYYY-MM-DD-executive-summary.md`
