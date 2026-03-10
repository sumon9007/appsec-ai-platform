# RBAC Test Matrix

Maps roles against resources and records expected vs. observed permissions for each combination.

**Auditor:** [PLACEHOLDER]
**Date:** [PLACEHOLDER]
**Target:** [PLACEHOLDER]
**Authorization Reference:** [PLACEHOLDER]

---

## Permission Legend

| Symbol | Meaning |
|--------|---------|
| R | Read / View |
| W | Write / Create |
| U | Update / Edit |
| D | Delete |
| FULL | Full access (R + W + U + D) |
| NONE | No access |
| OWN | Access to own records only |
| — | Not applicable |

## Test Result Legend

| Result | Meaning |
|--------|---------|
| PASS | Observed permission matches expected |
| FAIL | Observed permission differs from expected |
| NOT TESTED | Could not test — document reason |
| [UNKNOWN] | Unable to determine |

---

## Role Definitions

| Role | Description | Typical Permissions |
|------|-------------|---------------------|
| [PLACEHOLDER — e.g., Admin] | [PLACEHOLDER] | [PLACEHOLDER — e.g., FULL on all resources] |
| [PLACEHOLDER — e.g., Manager] | [PLACEHOLDER] | [PLACEHOLDER] |
| [PLACEHOLDER — e.g., User] | [PLACEHOLDER] | [PLACEHOLDER — e.g., OWN on profile, R on products] |
| [PLACEHOLDER — e.g., Read-Only] | [PLACEHOLDER] | [PLACEHOLDER — e.g., R only on permitted resources] |

---

## Test Matrix

### Resource: User Accounts / Profiles

| Action | Admin | Manager | User | Read-Only | Expected Behavior | Result | Evidence | Notes |
|--------|-------|---------|------|-----------|------------------|--------|---------|-------|
| View own profile | FULL | FULL | FULL | R | Own profile visible | [PASS/FAIL] | [EVID-] | [NOTES] |
| Edit own profile | FULL | FULL | U | NONE | Own profile editable | [PASS/FAIL] | [EVID-] | [NOTES] |
| View other user's profile | FULL | R | NONE | NONE | Other profiles not accessible to User | [PASS/FAIL] | [EVID-] | [NOTES] |
| Edit other user's profile | FULL | NONE | NONE | NONE | Blocked for non-admin | [PASS/FAIL] | [EVID-] | [NOTES] |
| Delete user account | FULL | NONE | NONE | NONE | Admin only | [PASS/FAIL] | [EVID-] | [NOTES] |
| Change user role | FULL | NONE | NONE | NONE | Admin only | [PASS/FAIL] | [EVID-] | [NOTES] |

### Resource: [PLACEHOLDER — e.g., Application Data / Content]

| Action | Admin | Manager | User | Read-Only | Expected Behavior | Result | Evidence | Notes |
|--------|-------|---------|------|-----------|------------------|--------|---------|-------|
| [PLACEHOLDER — e.g., View records] | [FULL] | [R] | [OWN] | [R] | [PLACEHOLDER] | [PASS/FAIL] | [EVID-] | [NOTES] |
| [PLACEHOLDER — e.g., Create record] | [FULL] | [W] | [W] | [NONE] | [PLACEHOLDER] | [PASS/FAIL] | [EVID-] | [NOTES] |
| [PLACEHOLDER — e.g., Edit record] | [FULL] | [U] | [OWN] | [NONE] | [PLACEHOLDER] | [PASS/FAIL] | [EVID-] | [NOTES] |
| [PLACEHOLDER — e.g., Delete record] | [FULL] | [D] | [NONE] | [NONE] | [PLACEHOLDER] | [PASS/FAIL] | [EVID-] | [NOTES] |

### Resource: Administrative Functions

| Action | Admin | Manager | User | Read-Only | Expected Behavior | Result | Evidence | Notes |
|--------|-------|---------|------|-----------|------------------|--------|---------|-------|
| Access admin dashboard | FULL | NONE | NONE | NONE | Admin only | [PASS/FAIL] | [EVID-] | [NOTES] |
| View system configuration | FULL | NONE | NONE | NONE | Admin only | [PASS/FAIL] | [EVID-] | [NOTES] |
| Modify system configuration | FULL | NONE | NONE | NONE | Admin only | [PASS/FAIL] | [EVID-] | [NOTES] |
| View all users | FULL | R | NONE | NONE | Admin/Manager | [PASS/FAIL] | [EVID-] | [NOTES] |
| Export data (bulk) | FULL | R | NONE | NONE | Admin/Manager only | [PASS/FAIL] | [EVID-] | [NOTES] |

### Resource: API Endpoints

| Endpoint | Method | Admin | Manager | User | Read-Only | Expected Auth | Result | Evidence | Notes |
|----------|--------|-------|---------|------|-----------|--------------|--------|---------|-------|
| [PLACEHOLDER — e.g., /api/admin/users] | GET | FULL | NONE | NONE | NONE | Admin JWT | [PASS/FAIL] | [EVID-] | [NOTES] |
| [PLACEHOLDER — e.g., /api/users/:id] | GET | FULL | R | OWN | OWN | User JWT | [PASS/FAIL] | [EVID-] | [NOTES] |
| [PLACEHOLDER — e.g., /api/users/:id] | PUT | FULL | U | OWN | NONE | User JWT | [PASS/FAIL] | [EVID-] | [NOTES] |
| [PLACEHOLDER] | [METHOD] | [PERM] | [PERM] | [PERM] | [PERM] | [AUTH] | [PASS/FAIL] | [EVID-] | [NOTES] |

---

## Matrix Summary

| Role | Total Tests | PASS | FAIL | NOT TESTED | Failure Rate |
|------|-------------|------|------|------------|-------------|
| Admin | [N] | [N] | [N] | [N] | [%] |
| Manager | [N] | [N] | [N] | [N] | [%] |
| User | [N] | [N] | [N] | [N] | [%] |
| Read-Only | [N] | [N] | [N] | [N] | [%] |

---

## Key Failures

Record any FAIL results here for quick reference:

| Finding ID | Role | Resource | Action | Description |
|------------|------|----------|--------|-------------|
| [FIND-NNN] | [ROLE] | [RESOURCE] | [ACTION] | [DESCRIPTION] |

---

*Template: rbac-test-matrix.md*
