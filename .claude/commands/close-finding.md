# Command: /close-finding

## Objective

Close a finding in the findings register once remediation has been verified.

A finding may only be marked as `closed` when:

1. Fix evidence has been provided (pull request, config change, dependency update, or process change)
2. A re-test has been performed (where possible) and the finding is confirmed resolved
3. Both the fix evidence and re-test evidence are referenced as EVID- labeled items

**A finding must never be closed without evidence. No exceptions.**

---

## Required Inputs

The user must provide:

- **Finding ID** — e.g., `FIND-003`
- **Fix evidence reference** — an EVID- labeled evidence item describing what was fixed and how (e.g., pull request, config screenshot, dependency manifest diff)
- **Re-test evidence reference** — an EVID- labeled evidence item confirming the fix was verified (e.g., new HTTP response showing header present, updated package version confirmed)
- **Closure date** — YYYY-MM-DD

Also read:

- `.claude/templates/findings-register-template.md` — to locate and update the finding record

---

## Pre-Conditions

### Evidence Validation

Before closing, confirm:

1. The fix evidence item exists in `evidence/reviewed/` or `evidence/summarized/` with the stated EVID- ID
2. The re-test evidence item exists and clearly demonstrates the finding condition is no longer present
3. The fix evidence is dated after the finding was opened

If either evidence item is missing, halt and respond:

> **CLOSURE BLOCKED:** Finding [FIND-NNN] cannot be closed without both fix evidence and re-test evidence. Provide EVID- labeled evidence items for both before proceeding.

---

## Closure Steps

### Step 1 — Locate the Finding

Open `.claude/templates/findings-register-template.md`.

Locate the finding block for the stated Finding ID.

Verify:
- the finding is in `confirmed`, `suspected`, or `mitigated` status (not already closed or accepted-risk)
- the Finding ID matches the requested ID

---

### Step 2 — Review Fix Evidence

Read the fix evidence description.

Verify the fix evidence:
- relates directly to the finding's identified weakness
- represents a real remediation action (not just documentation or acknowledgement)
- is appropriately labeled (EVID-YYYY-MM-DD-NNN)

---

### Step 3 — Review Re-Test Evidence

Read the re-test evidence description.

Verify the re-test evidence:
- was collected after the fix was applied
- directly demonstrates the finding condition is resolved
- is labeled with an EVID- ID

---

### Step 4 — Update the Finding Record

In the findings register, update the finding block:

- **Status:** `closed`
- **Closed:** [closure date provided]
- **Closure Evidence:**
  - [EVID fix reference — description]
  - [EVID re-test reference — description]

Update the Findings Summary table at the top of the register to reflect the `closed` status.

---

### Step 5 — Regression Check

Check whether this finding was previously closed in a prior engagement or audit cycle.

If this is a re-opened finding (previously closed, now re-discovered):

- note this in the finding record as `[REGRESSION — originally closed [date]]`
- severity of this closure does not apply retroactively to the regression finding
- ensure the regression was handled as a new finding with escalated severity per `.claude/rules/remediation-rules.md`

---

### Step 6 — Confirm Closure

Output a closure confirmation:

```
FINDING CLOSED
--------------
Finding ID:        [FIND-NNN]
Title:             [Finding title]
Severity:          [Severity]
Closed:            [YYYY-MM-DD]
Fix Evidence:      [EVID-YYYY-MM-DD-NNN]
Re-test Evidence:  [EVID-YYYY-MM-DD-NNN]
Status:            closed

Findings register updated.
```

---

## Output

This command produces:

1. Pre-condition check (evidence validation)
2. Updated finding record in the findings register with `closed` status and closure evidence
3. Updated Findings Summary table
4. Closure confirmation

---

## Notes

- Do not close a finding based on a developer's verbal or written assurance alone — physical evidence of the fix and re-test is required.
- If a full re-test is not possible (e.g., staging environment is unavailable), the finding status may be set to `mitigated` with documented compensating control evidence, not `closed`.
- Risk accepted findings use `/accept-risk` status handling — do not use this command for risk acceptance.
- Once closed, a Finding ID is retired. If the same issue reappears, it becomes a new finding with a new ID, noted as a regression.