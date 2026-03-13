# Command: /start-session

## Objective

Initialize a new audit session record for the current engagement.

This command reads context files, confirms authorization status, and creates a populated session record in `audit-runs/active/` using the audit session template.

**Run this command at the start of every audit session before performing any review activity.**

---

## Required Inputs

Read context first:

- `.claude/context/audit-context.md` — engagement ID, authorization status, authorizing party, testing mode
- `.claude/context/target-profile.md` — application name, URL
- `.claude/context/scope.md` — in-scope targets and restrictions
- `.claude/context/assumptions.md` — active assumptions at session start

---

## Pre-Conditions

### Authorization Check

Before proceeding, verify that `.claude/context/audit-context.md` contains:

- Authorization Status: **CONFIRMED**
- Authorizing Party: a named individual with title
- Authorization Reference: a document, email, or ticket reference
- Testing Mode: clearly defined (Passive Only / Passive + Active Testing on [ENVIRONMENT])

If Authorization Status is anything other than **CONFIRMED**, halt and display:

> **AUTHORIZATION REQUIRED:** Audit activity cannot begin. Authorization Status in `.claude/context/audit-context.md` must be CONFIRMED before any audit session can start. Please confirm written authorization from an authorized party and update the context file.

### Scope Check

Verify that `.claude/context/scope.md` is populated with:

- at least one in-scope URL or target
- a defined out-of-scope section

If scope is empty, halt and request the user populate it before starting the session.

---

## Session Initialization Steps

### Step 1 — Generate Session ID

Construct the session ID using:

```
SESSION-[YYYY-MM-DD]-[NNN]
```

Where NNN is a sequential number for the day (001 for the first session of the day, 002 for the second, etc.).

Check `audit-runs/active/` and `audit-runs/completed/` for existing sessions on today's date to determine the correct sequence number.

---

### Step 2 — Determine Session Objectives

Ask the user (or infer from context) what domains or commands this session will cover.

Typical session objectives:
- completing a specific `/review-*` command
- continuing a multi-session audit
- starting a full `/audit-website` run

---

### Step 3 — Create Session Record

Create a new file at:

```
audit-runs/active/[SESSION-ID]-session.md
```

Populate it using `.claude/templates/audit-session-template.md`, filling in:

| Field | Value |
|-------|-------|
| Session ID | Generated in Step 1 |
| Session Date | Today's date (YYYY-MM-DD) |
| Start Time | Current time (HH:MM UTC) |
| End Time | [TBD — complete at end of session] |
| Auditor | [From audit-context.md or user input] |
| Audit Engagement | [Engagement ID from audit-context.md] |
| Session File Location | `audit-runs/active/[SESSION-ID]-session.md` |
| Authorization Status | CONFIRMED |
| Authorizing Party | [From audit-context.md] |
| Authorization Reference | [From audit-context.md] |
| Testing Mode | [From audit-context.md] |
| Scope Confirmed | Yes |
| Session Objectives | [From Step 2] |

Leave the following sections blank for population during the session:
- Activities Performed
- Findings Noted
- Evidence Collected
- Assumptions and Unknowns Encountered
- Items Deferred to Next Session
- Out-of-Scope Observations
- Next Steps

---

### Step 4 — Confirm Session is Active

Output a session start confirmation:

```
AUDIT SESSION STARTED
---------------------
Session ID:       [SESSION-ID]
Date:             [YYYY-MM-DD]
Target:           [Application name and URL from target-profile.md]
Testing Mode:     [Passive Only / Passive + Active Testing]
Authorization:    CONFIRMED ([Authorizing Party])
Session Record:   audit-runs/active/[SESSION-ID]-session.md

Ready to begin audit activity.
```

---

## Output

This command produces:

1. Authorization and scope pre-condition check
2. A new session record at `audit-runs/active/[SESSION-ID]-session.md`
3. Session start confirmation with key session metadata

---

## Notes

- At the end of the session, move the session file from `audit-runs/active/` to `audit-runs/completed/` and fill in the End Time and Session Status fields.
- Each audit day may have multiple sessions — the sequence number (NNN) distinguishes them.
- The session record is the running log for all activities, findings, and evidence collected during the session.