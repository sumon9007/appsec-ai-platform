# Audit Session Record

Records the activities and findings of a single audit session. Complete at the start and end of each session.

---

## Session Header

| Field | Value |
|-------|-------|
| **Session ID** | [PLACEHOLDER — e.g., SESSION-2026-03-11-001] |
| **Session Date** | [PLACEHOLDER — YYYY-MM-DD] |
| **Start Time** | [PLACEHOLDER — HH:MM UTC] |
| **End Time** | [PLACEHOLDER — HH:MM UTC] |
| **Auditor** | [PLACEHOLDER] |
| **Audit Engagement** | [PLACEHOLDER — Audit ID from audit-context.md] |
| **Session File Location** | [PLACEHOLDER — path to this file] |

---

## Authorization Confirmation

**Complete this section at the start of every session before any activity begins.**

| Field | Value |
|-------|-------|
| **Authorization Status** | [PLACEHOLDER — CONFIRMED / NOT CONFIRMED — halt if not confirmed] |
| **Authorizing Party** | [PLACEHOLDER — Name and title] |
| **Authorization Reference** | [PLACEHOLDER — Email ref, document ID, ticket number] |
| **Testing Mode** | [PLACEHOLDER — Passive Only / Passive + Active Testing on [ENVIRONMENT]] |
| **Scope Confirmed** | [PLACEHOLDER — Yes / No — confirm .claude/context/scope.md is populated] |

---

## Session Objectives

[PLACEHOLDER — What does this session aim to accomplish?]

1. [PLACEHOLDER — e.g., Complete the security headers and TLS review]
2. [PLACEHOLDER — e.g., Begin authentication flow review]
3. [PLACEHOLDER — e.g., Review dependency manifests for CVEs]

---

## Domain(s) Covered

| Domain | Skill Loaded | Coverage Level | Status |
|--------|-------------|---------------|--------|
| [PLACEHOLDER — e.g., Security Headers & TLS] | [headers-tls-audit] | [Full / Spot-check] | [Complete / Partial / Deferred] |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

---

## Activities Performed

[PLACEHOLDER — Narrative or bullet-point summary of activities performed during the session:]

- [PLACEHOLDER — e.g., Reviewed HTTP response headers for the main application URL and login page]
- [PLACEHOLDER — e.g., Ran SSL Labs assessment on the target domain]
- [PLACEHOLDER — e.g., Reviewed provided package.json for known CVEs]
- [PLACEHOLDER — e.g., Inspected session cookies in authenticated state using browser DevTools]

---

## Findings Noted (Summary)

New findings identified during this session:

| Finding ID | Title | Severity | Domain | Evidence Collected |
|------------|-------|----------|--------|--------------------|
| [FIND-NNN] | [PLACEHOLDER] | [SEVERITY] | [DOMAIN] | [EVID-YYYY-MM-DD-NNN] |
| [FIND-NNN] | [PLACEHOLDER] | [SEVERITY] | [DOMAIN] | [EVID-YYYY-MM-DD-NNN] |

**Total new findings this session:** [N]
**Critical:** [N] | **High:** [N] | **Medium:** [N] | **Low:** [N] | **Info:** [N]

---

## Evidence Collected

| Evidence ID | Type | Domain | Description | Storage Location |
|-------------|------|--------|-------------|-----------------|
| [EVID-YYYY-MM-DD-NNN] | [Type] | [Domain] | [PLACEHOLDER] | `evidence/raw/[filename]` |
| [EVID-YYYY-MM-DD-NNN] | [Type] | [Domain] | [PLACEHOLDER] | `evidence/raw/[filename]` |

**Total evidence items collected this session:** [N]

---

## Assumptions and Unknowns Encountered

[PLACEHOLDER — Note any new assumptions made or unknowns encountered during this session. Update .claude/context/assumptions.md accordingly.]

| Type | Description | Impact |
|------|-------------|--------|
| [ASSUMED] | [PLACEHOLDER] | [PLACEHOLDER] |
| [UNKNOWN] | [PLACEHOLDER — e.g., Could not determine log retention period — client to provide] | [PLACEHOLDER] |

---

## Items Deferred to Next Session

[PLACEHOLDER — What was not completed this session and should be picked up next time?]

- [PLACEHOLDER — e.g., RBAC and IDOR testing — requires additional test account credentials]
- [PLACEHOLDER — e.g., Log review — awaiting log sample from client]

---

## Out-of-Scope Observations

[PLACEHOLDER — Note any out-of-scope issues observed passively. Do not investigate further.]

- `[OUT OF SCOPE — NOT TESTED]` [PLACEHOLDER — Brief description of out-of-scope observation]

---

## Next Steps

[PLACEHOLDER — What should happen after this session?]

1. [PLACEHOLDER — e.g., Investigate FIND-005 further once active testing authorization confirmed]
2. [PLACEHOLDER — e.g., Request dependency manifest from client]
3. [PLACEHOLDER — e.g., Begin RBAC review in next session]
4. [PLACEHOLDER — e.g., Update findings register with all new findings]

---

## Session Status

**Session Complete:** [Yes / Partial — see deferred items]

*Move this file from `audit-runs/active/` to `audit-runs/completed/` when the session is complete.*

---

*Template: audit-session-template.md*
