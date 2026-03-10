# IDOR Review Template

Documents Insecure Direct Object Reference (IDOR) test cases for each object type reviewed during the authorization audit.

**Auditor:** [PLACEHOLDER]
**Date:** [PLACEHOLDER]
**Target:** [PLACEHOLDER]
**Authorization Reference:** [PLACEHOLDER]

**AUTHORIZATION REQUIRED:** Active IDOR testing requires explicit authorization. Document authorization status here before proceeding: [PLACEHOLDER — Confirmed / Passive review only]

---

## What is an IDOR?

An IDOR vulnerability occurs when an application uses user-controlled references (IDs, UUIDs, slugs, file names) to access objects, and fails to verify that the requesting user is authorized to access that specific object.

**Example:** A user with ID 123 can access `/api/users/456/documents` and retrieve another user's documents.

---

## IDOR Test Case Record

Complete one section per object type tested.

---

### Object Type: [PLACEHOLDER — e.g., User Profile]

| Field | Value |
|-------|-------|
| **Test Case ID** | IDOR-001 |
| **Object Type** | [PLACEHOLDER — e.g., User Profile] |
| **Endpoint** | [PLACEHOLDER — e.g., GET /api/users/{id}/profile] |
| **Vulnerable Parameter** | [PLACEHOLDER — e.g., `id` path parameter] |
| **Parameter Format** | [PLACEHOLDER — Sequential integer / UUID / Hash / Other] |
| **Guessable/Predictable?** | [PLACEHOLDER — Yes / No / Partially] |
| **Test Account Used** | [PLACEHOLDER — Role and account identifier] |
| **Reference Object Owner** | [PLACEHOLDER — Account of the resource being accessed] |

**Test Description:**
[PLACEHOLDER — Describe the test: e.g., "Using Account A (user ID 100), attempt to retrieve the profile of Account B (user ID 101) by modifying the `id` parameter in the GET /api/users/{id}/profile request."]

**Expected Behavior:**
[PLACEHOLDER — What should happen: e.g., "Application should return 403 Forbidden or 404 Not Found when Account A attempts to access Account B's profile."]

**Observed Behavior:**
[PLACEHOLDER — What actually happened: e.g., "Application returned 200 OK with Account B's full profile data, including email, phone number, and address."]

**Result:** [PASS / FAIL / NOT TESTED]

**Risk Rating:** [Critical / High / Medium / Low]

**Risk Justification:**
[PLACEHOLDER — Why this risk rating: e.g., "Any user can access any other user's PII including email, phone, and physical address."]

**Evidence:**
- [EVID-YYYY-MM-DD-NNN — description]

**Recommendation:**
[PLACEHOLDER — e.g., "Implement server-side ownership check: verify that the authenticated user's ID matches the requested resource owner before returning data. Alternatively, scope object queries to the authenticated user's context."]

---

### Object Type: [PLACEHOLDER — e.g., Order / Transaction]

| Field | Value |
|-------|-------|
| **Test Case ID** | IDOR-002 |
| **Object Type** | [PLACEHOLDER — e.g., Order] |
| **Endpoint** | [PLACEHOLDER — e.g., GET /api/orders/{orderId}] |
| **Vulnerable Parameter** | [PLACEHOLDER — e.g., `orderId` path parameter] |
| **Parameter Format** | [PLACEHOLDER — Sequential integer / UUID / Other] |
| **Guessable/Predictable?** | [PLACEHOLDER — Yes / No] |
| **Test Account Used** | [PLACEHOLDER] |
| **Reference Object Owner** | [PLACEHOLDER] |

**Test Description:**
[PLACEHOLDER]

**Expected Behavior:**
[PLACEHOLDER]

**Observed Behavior:**
[PLACEHOLDER]

**Result:** [PASS / FAIL / NOT TESTED]

**Risk Rating:** [Critical / High / Medium / Low]

**Risk Justification:**
[PLACEHOLDER]

**Evidence:**
- [EVID-YYYY-MM-DD-NNN — description]

**Recommendation:**
[PLACEHOLDER]

---

### Object Type: [PLACEHOLDER — e.g., Uploaded File]

| Field | Value |
|-------|-------|
| **Test Case ID** | IDOR-003 |
| **Object Type** | [PLACEHOLDER — e.g., User-uploaded document] |
| **Endpoint** | [PLACEHOLDER — e.g., GET /files/{fileId}] |
| **Vulnerable Parameter** | [PLACEHOLDER] |
| **Parameter Format** | [PLACEHOLDER] |
| **Guessable/Predictable?** | [PLACEHOLDER] |

**Test Description:**
[PLACEHOLDER]

**Expected Behavior:**
[PLACEHOLDER]

**Observed Behavior:**
[PLACEHOLDER]

**Result:** [PASS / FAIL / NOT TESTED]

**Risk Rating:** [Critical / High / Medium / Low]

**Evidence:**
- [EVID-YYYY-MM-DD-NNN — description]

**Recommendation:**
[PLACEHOLDER]

---

## IDOR Summary

| Test Case | Object Type | Endpoint | Result | Severity | Finding ID |
|-----------|-------------|----------|--------|----------|------------|
| IDOR-001 | [PLACEHOLDER] | [PLACEHOLDER] | [PASS/FAIL] | [SEVERITY] | [FIND-NNN or —] |
| IDOR-002 | [PLACEHOLDER] | [PLACEHOLDER] | [PASS/FAIL] | [SEVERITY] | [FIND-NNN or —] |
| IDOR-003 | [PLACEHOLDER] | [PLACEHOLDER] | [PASS/FAIL] | [SEVERITY] | [FIND-NNN or —] |

---

## Attack Surface Notes

[PLACEHOLDER — Additional observations about the IDOR attack surface beyond specific test cases:]

- ID guessability assessment: [PLACEHOLDER — e.g., "Object IDs are sequential integers starting at 1, making enumeration trivial"]
- Endpoints not tested (out of scope or insufficient authorization): [PLACEHOLDER]
- Endpoints that appear to have correct ownership enforcement: [PLACEHOLDER]

---

*Template: idor-review-template.md*
