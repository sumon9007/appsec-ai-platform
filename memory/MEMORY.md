# appsec-ai-platform Memory

## Project
Reusable security audit workspace for website/web app reviews. Markdown-only, environment-agnostic.

## Scaffold (created 2026-03-11)
- 69 Markdown files + 12 `.gitkeep` files across the full directory structure
- Commands registered in `commands/` — invoked as `/audit-website`, `/review-auth`, etc.
- Skills in `skills/` — each has SKILL.md + templates subdirectory
- Rules enforced from `rules/` — must be read before producing findings
- Context files in `context/` — user fills these in before running any audit

## Key Workflow
1. User fills in `context/audit-context.md`, `context/target-profile.md`, `context/scope.md`, `context/assumptions.md`
2. User runs a command (e.g. `/audit-website`, `/review-auth`)
3. Claude reads context + rules, loads relevant skill(s), applies templates, produces structured output
4. Findings go to `audit-runs/active/`, evidence to `evidence/`, reports to `reports/`

## Conventions
- Finding IDs: FIND-YYYY-MM-DD-NNN
- Evidence IDs: EVID-YYYY-MM-DD-NNN
- Severity: Critical / High / Medium / Low / Info
- Report filenames: YYYY-MM-DD-[type]-report.md
- Always label unknowns as [UNKNOWN], assumptions as [ASSUMED]
- No active exploitation without written authorization confirmed in audit-context.md
