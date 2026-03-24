# Assumptions & Unknowns

> Findings influenced by assumptions → label `[ASSUMED]`. Unresolved unknowns → `[UNKNOWN]`.
> Read when: labeling a finding, assessing confidence, or checking for blockers.

## Working Assumptions
| ID | Assumption | Basis | Status |
|----|-----------|-------|--------|
| A-001 | Application handles confidential staff/internal data | Staff portal by nature; assumed until confirmed | ASSUMED |
| A-002 | Backend is Node.js | Confirmed by client (Wilton White, CTO) | VALIDATED |
| A-003 | Only unauthenticated surface is available for this review | No test accounts provided | ASSUMED |

## Known Unknowns
| ID | Unknown | Impact | Status |
|----|---------|--------|--------|
| U-001 | Full authenticated attack surface | Limits depth of auth, RBAC, and session reviews | OPEN |
| U-002 | WAF / CDN / hosting infrastructure | Cannot assess infrastructure-level protections | OPEN |
| U-003 | Frontend framework (React, Vue, Angular, etc.) | Limits client-side analysis depth | OPEN |
| U-004 | Database technology | Cannot assess injection risk completeness | OPEN |
| U-005 | MFA enforcement | Cannot confirm without test account | OPEN |
| U-006 | API surface and endpoints beyond what is publicly observable | May miss significant attack surface | OPEN |
| U-007 | Remediation ownership and SLA contacts | Required for finding assignment | OPEN |
| U-008 | Data classification and sensitivity of staff data | Affects severity of data exposure findings | OPEN |

## Client Dependencies
| Item | Requested | Received |
|------|-----------|----------|
| Technical POC | 2026-03-24 | PENDING |
| Architecture docs | 2026-03-24 | PENDING |
| Prior audit report | 2026-03-24 | PENDING |
| Test accounts (any role) | 2026-03-24 | NOT PROVIDED |

## Validation Log
| Date | ID | New Status | Notes |
|------|-----|-----------|-------|
| 2026-03-24 | A-002 | VALIDATED | Node.js confirmed by CTO in engagement kickoff |

---
*Updated: 2026-03-24*
