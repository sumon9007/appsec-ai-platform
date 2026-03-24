> This skill is for ENGAGEMENT SETUP and validation — not individual session initialization.
> For session initialization use: `/start-session`
> For automated context reading see: `src/utils/context_reader.py`

# Skill: Engagement Bootstrap

## Purpose

Initialize and validate a new or resumed audit engagement. Ensures all context files are populated, authorization is confirmed, scope is defined, and the workspace is ready before any audit activity begins.

Use this skill:
- When starting a new engagement from scratch
- When resuming an engagement after a gap in work
- When onboarding a new auditor onto an existing engagement
- Before running any domain skill or audit workflow

Do NOT use this skill as a substitute for `/start-session`. The `/start-session` command initializes individual audit sessions. This skill validates the engagement foundation that all sessions run on.

---

## Inputs Required

| Input | Source | Required? |
|-------|--------|-----------|
| Audit context | `.claude/context/audit-context.md` | Required |
| Target profile | `.claude/context/target-profile.md` | Required |
| Scope definition | `.claude/context/scope.md` | Required |
| Assumptions log | `.claude/context/assumptions.md` | Required |
| Active findings register | `audits/[engagement-id]/findings-register.md` | Required if resuming |

---

## Method

### Phase 1: Authorization Gate

1. Read `.claude/context/audit-context.md`
2. Verify Authorization Status is **CONFIRMED**. If not, halt with:
   > **AUTHORIZATION REQUIRED:** Audit activity cannot begin until Authorization Status is CONFIRMED in `.claude/context/audit-context.md`. Please confirm written authorization from an authorized party before proceeding.
3. Confirm all required fields are populated:
   - Engagement ID
   - Target URL
   - Authorizing Party (named individual + title)
   - Authorization Reference (email, ticket, or signed document)
   - Testing Mode: `Passive Only` or `Passive + Active Testing on [ENVIRONMENT]`
   - Engagement Start Date
4. Flag any missing fields as `[MISSING — must complete before proceeding]`

### Phase 2: Scope Validation

5. Read `.claude/context/scope.md`
6. Verify at least one in-scope URL or target is explicitly listed
7. Verify an out-of-scope section exists and is populated
8. Flag any scope ambiguities (e.g., "all subdomains" without explicit enumeration)
9. Read `.claude/rules/audit-scope-rules.md` — confirm scope definition meets Rule 1 and Rule 2

### Phase 3: Target Profile Review

10. Read `.claude/context/target-profile.md`
11. For each key field, determine: **confirmed**, **assumed**, or **unknown**:
    - Application name
    - Technology stack (frontend, backend, infrastructure)
    - Authentication mechanism
    - API surface and endpoints
    - Hosting / CDN / WAF presence
    - Known third-party integrations
12. Record newly identified unknowns — add ASSUM-NNN or UNK-NNN entries to `.claude/context/assumptions.md`

### Phase 4: Assumptions Audit

13. Read `.claude/context/assumptions.md`
14. Verify each entry has:
    - An assumption ID (ASSUM-NNN or UNK-NNN)
    - A status: ASSUMED / VALIDATED / INVALIDATED / UNKNOWN
    - A description of what is assumed or unknown
15. Add any new unknowns identified in Phase 3

### Phase 5: Workspace Artifact Check

16. Check `audits/` for an existing findings register for this engagement ID
17. If none exists, create one from `.claude/templates/findings-register-template.md` at:
    `audits/[engagement-id]/findings-register.md`
18. Confirm these directories exist (create if not): `evidence/raw/`, `evidence/reviewed/`, `evidence/summarized/`, `audit-runs/active/`, `audit-runs/completed/`

### Phase 6: Engagement Readiness Report

19. Produce a structured readiness summary:

```
ENGAGEMENT READINESS CHECK
--------------------------
Engagement ID:      [ID]
Target:             [URL]
Authorization:      CONFIRMED / INCOMPLETE — [missing fields]
Scope Defined:      YES / NO — [any gaps or ambiguities]
Target Profile:     COMPLETE / PARTIAL — [confirmed vs. assumed summary]
Assumptions Log:    [N] confirmed | [N] unknowns
Findings Register:  EXISTS at [path] | CREATED at [path]
Workspace Dirs:     OK | MISSING: [list]

STATUS: READY TO AUDIT / BLOCKED — [reason]
```

20. If `READY TO AUDIT`, suggest next steps:
    - Run `/start-session` to open an audit session
    - Run `/audit-full-website` or a specific `/review-*` command
    - Run a domain skill if a focused review is planned

---

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Readiness report | Displayed in session | Validation summary with gaps flagged |
| Findings register (if new) | `audits/[engagement-id]/findings-register.md` | Empty register ready for use |
| Updated assumptions log | `.claude/context/assumptions.md` | New unknowns added from profile review |

---

## Templates Used

- `.claude/templates/findings-register-template.md` — initial findings register
- `.claude/templates/audit-session-template.md` — referenced by `/start-session` which follows this skill

---

## Rules Applied

- `.claude/rules/safety-authorization-rules.md` — Rule 1 (authorization gate), Rule 5 (session record)
- `.claude/rules/audit-scope-rules.md` — Rules 1, 2 (scope confirmation before starting)

---

## Related Skills and Commands

- `/start-session` — next step after this skill passes; initializes the individual audit session
- `/audit-full-website` — full-website passive audit; run after engagement is bootstrapped
- `audit-cadence-orchestrator` — use this skill first for cadence-driven audits
- `src/utils/context_reader.py` — Python layer reads the same context files and enforces authorization gating programmatically
