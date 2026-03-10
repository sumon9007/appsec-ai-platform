# Input Validation Review Template

Documents input validation controls assessed for each endpoint or feature during the input validation audit.

**Auditor:** [PLACEHOLDER]
**Date:** [PLACEHOLDER]
**Target:** [PLACEHOLDER]
**Authorization Level:** [PLACEHOLDER — Passive review / Active testing authorized]

---

## Endpoint / Feature Review Record

Complete one section per endpoint or feature reviewed.

---

### Endpoint: [PLACEHOLDER — e.g., POST /api/users/search]

| Field | Value |
|-------|-------|
| **Endpoint** | [PLACEHOLDER — e.g., POST /api/search] |
| **HTTP Method(s)** | [PLACEHOLDER — e.g., POST] |
| **Feature** | [PLACEHOLDER — e.g., User search / Profile update / File upload] |
| **Input Type(s)** | [PLACEHOLDER — e.g., JSON body parameters: `query` (string), `limit` (integer)] |
| **User Role Required** | [PLACEHOLDER — e.g., Authenticated user / Admin] |

**Input Parameters:**

| Parameter | Type | Expected Format | Max Length | Required? |
|-----------|------|----------------|------------|-----------|
| [PLACEHOLDER — e.g., query] | [string] | [e.g., Alphanumeric + spaces] | [e.g., 255] | [Yes/No] |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

**Validation Assessment:**

| Check | Status | Notes |
|-------|--------|-------|
| Server-side validation present | [Yes / No / Unknown] | [NOTES] |
| Client-side validation present | [Yes / No] | [Note: client-side alone is insufficient] |
| Input length enforced server-side | [Yes / No / Unknown] | [NOTES] |
| Input type/format validated | [Yes / No / Unknown] | [NOTES] |
| Database queries use parameterized queries or ORM | [Yes / No / Unknown / N/A] | [NOTES] |
| HTML output is encoded | [Yes / No / Unknown / N/A] | [NOTES] |
| Input is sanitized for context (HTML, SQL, OS) | [Yes / No / Unknown] | [NOTES] |

**Observed Behavior:**
[PLACEHOLDER — Describe what was observed when submitting various inputs to this endpoint. Note any interesting error messages, timing differences, or unusual responses.]

**Risk Notes:**
[PLACEHOLDER — What injection risks apply to this endpoint based on input type and observable validation behavior?]

**Assessment:** [Low Risk / Medium Risk / High Risk / Requires Further Testing]

**Finding ID (if applicable):** [FIND-NNN or —]

---

### Endpoint: [PLACEHOLDER — e.g., POST /api/profile/update]

| Field | Value |
|-------|-------|
| **Endpoint** | [PLACEHOLDER] |
| **HTTP Method(s)** | [PLACEHOLDER] |
| **Feature** | [PLACEHOLDER] |
| **Input Type(s)** | [PLACEHOLDER] |
| **User Role Required** | [PLACEHOLDER] |

**Input Parameters:**

| Parameter | Type | Expected Format | Max Length | Required? |
|-----------|------|----------------|------------|-----------|
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

**Validation Assessment:**

| Check | Status | Notes |
|-------|--------|-------|
| Server-side validation present | [Yes / No / Unknown] | [NOTES] |
| Client-side validation present | [Yes / No] | [NOTES] |
| Input length enforced server-side | [Yes / No / Unknown] | [NOTES] |
| Input type/format validated | [Yes / No / Unknown] | [NOTES] |
| Database queries use parameterized queries or ORM | [Yes / No / Unknown / N/A] | [NOTES] |
| HTML output is encoded | [Yes / No / Unknown / N/A] | [NOTES] |

**Observed Behavior:**
[PLACEHOLDER]

**Risk Notes:**
[PLACEHOLDER]

**Assessment:** [Low Risk / Medium Risk / High Risk / Requires Further Testing]

**Finding ID (if applicable):** [FIND-NNN or —]

---

### Endpoint: File Upload — [PLACEHOLDER — e.g., POST /api/files/upload]

| Field | Value |
|-------|-------|
| **Endpoint** | [PLACEHOLDER] |
| **Feature** | File upload |
| **User Role Required** | [PLACEHOLDER] |

**File Upload Validation Assessment:**

| Check | Status | Notes |
|-------|--------|-------|
| MIME type validated server-side (not just extension) | [Yes / No / Unknown] | [NOTES] |
| File extension allowlist in place | [Yes / No / Unknown] | [NOTES] |
| File size limited | [Yes / No / Unknown] | Max: [VALUE] |
| Uploaded files stored outside web root | [Yes / No / Unknown] | [NOTES] |
| Uploaded files served with non-executable Content-Type | [Yes / No / Unknown] | [NOTES] |
| Uploaded file names sanitized / randomized | [Yes / No / Unknown] | [NOTES] |
| Dangerous file types blocked (PHP, JSP, HTML, SVG) | [Yes / No / Unknown] | [NOTES] |
| Malware scanning in place | [Yes / No / Unknown] | [NOTES] |

**Assessment:** [Low Risk / Medium Risk / High Risk]
**Finding ID (if applicable):** [FIND-NNN or —]

---

## Validation Review Summary

| Endpoint | Risk Level | Validation Status | Finding? |
|----------|-----------|-------------------|---------|
| [PLACEHOLDER] | [Low/Medium/High] | [PASS/FAIL/PARTIAL] | [FIND-NNN or —] |
| [PLACEHOLDER] | [Low/Medium/High] | [PASS/FAIL/PARTIAL] | [FIND-NNN or —] |
| [PLACEHOLDER] | [Low/Medium/High] | [PASS/FAIL/PARTIAL] | [FIND-NNN or —] |

---

*Template: validation-review-template.md*
