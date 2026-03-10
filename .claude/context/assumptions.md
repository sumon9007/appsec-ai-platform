# Assumptions and Unknowns

Documents assumptions made at the start of the engagement and unknowns to be validated as the audit progresses.

**ASSUMPTION:** All items in this file represent information that has not been independently verified. Claude Code will label any finding influenced by an assumption with `[ASSUMED]`.

---

## How to Use This File

- Add assumptions as they arise — before and during the audit
- Validate assumptions when possible and update the Status column
- Unknowns that cannot be resolved should remain labeled `[UNKNOWN]` in all affected findings
- Review this file at the start of each audit session

---

## Assumptions About the Application

| ID | Assumption | Basis | Status | Impact if Wrong |
|----|-----------|-------|--------|----------------|
| ASSUM-001 | [PLACEHOLDER — e.g., The application uses HTTPS exclusively in production] | [e.g., Client stated] | [ASSUMED / VALIDATED / INVALIDATED] | [e.g., Transport security findings may be inaccurate] |
| ASSUM-002 | [PLACEHOLDER — e.g., All user-facing forms perform server-side validation] | [e.g., Assumed standard practice] | [ASSUMED] | [e.g., Input validation findings may be incomplete] |
| ASSUM-003 | [PLACEHOLDER — e.g., The admin panel is only accessible from internal IP ranges] | [e.g., Client documentation] | [ASSUMED] | [e.g., Admin exposure risk may be underestimated] |
| ASSUM-004 | [PLACEHOLDER — e.g., Test accounts have equivalent functionality to real accounts] | [e.g., Client confirmed] | [ASSUMED] | [e.g., RBAC test results may not reflect production behavior] |
| ASSUM-005 | [PLACEHOLDER] | [PLACEHOLDER] | [ASSUMED] | [PLACEHOLDER] |

---

## Assumptions About the Environment

| ID | Assumption | Basis | Status | Impact if Wrong |
|----|-----------|-------|--------|----------------|
| ASSUM-ENV-001 | [PLACEHOLDER — e.g., Staging environment mirrors production configuration] | [e.g., Client stated] | [ASSUMED] | [e.g., Findings on staging may not apply to production] |
| ASSUM-ENV-002 | [PLACEHOLDER — e.g., Third-party integrations are not in scope] | [e.g., Scope agreement] | [VALIDATED] | [e.g., N/A — confirmed out of scope] |
| ASSUM-ENV-003 | [PLACEHOLDER] | [PLACEHOLDER] | [ASSUMED] | [PLACEHOLDER] |

---

## Known Unknowns

Items that are explicitly unknown and require validation or acknowledgment before relying on related findings.

| ID | Unknown | Why It Matters | Resolution Plan | Status |
|----|---------|---------------|-----------------|--------|
| UNK-001 | [PLACEHOLDER — e.g., Complete list of API endpoints] | [e.g., Cannot assess full attack surface without it] | [e.g., Request API documentation from client] | [UNKNOWN / RESOLVED] |
| UNK-002 | [PLACEHOLDER — e.g., Whether logging is centralized or per-service] | [e.g., Affects logging audit methodology] | [e.g., Ask technical lead] | [UNKNOWN] |
| UNK-003 | [PLACEHOLDER — e.g., Password hashing algorithm used] | [e.g., Affects credential security assessment] | [e.g., Review source code or ask developer] | [UNKNOWN] |
| UNK-004 | [PLACEHOLDER — e.g., Whether MFA is enforced for all admin accounts] | [e.g., Critical for admin access risk rating] | [e.g., Test with provided admin test account] | [UNKNOWN] |
| UNK-005 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [UNKNOWN] |

---

## Dependencies on Target Team Cooperation

Items that require action or information from the target application team to complete or validate.

| Item | Owner | Requested Date | Received Date | Notes |
|------|-------|---------------|---------------|-------|
| [PLACEHOLDER — e.g., API documentation / OpenAPI spec] | [PLACEHOLDER — e.g., Backend team] | [DATE] | [DATE or PENDING] | [PLACEHOLDER] |
| [PLACEHOLDER — e.g., Architecture diagram] | [PLACEHOLDER] | [DATE] | [PENDING] | [PLACEHOLDER] |
| [PLACEHOLDER — e.g., Test account credentials] | [PLACEHOLDER] | [DATE] | [DATE] | [PLACEHOLDER] |
| [PLACEHOLDER — e.g., Recent dependency manifest (package.json / requirements.txt)] | [PLACEHOLDER] | [DATE] | [PENDING] | [PLACEHOLDER] |
| [PLACEHOLDER — e.g., Log sample from past 30 days] | [PLACEHOLDER] | [DATE] | [PENDING] | [PLACEHOLDER] |
| [PLACEHOLDER — e.g., Previous audit report or pen test findings] | [PLACEHOLDER] | [DATE] | [PENDING] | [PLACEHOLDER] |

---

## Assumption Validation Log

Record when assumptions are validated or invalidated during the audit:

| Date | Assumption / Unknown ID | Validated By | New Status | Notes |
|------|------------------------|-------------|------------|-------|
| [DATE] | [ID] | [AUDITOR] | [VALIDATED / INVALIDATED] | [NOTES] |

---

*Last updated: [PLACEHOLDER — Date]*
