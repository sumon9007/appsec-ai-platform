# Security Headers Checklist

Complete this checklist during the HTTP security headers review.

**Auditor:** [PLACEHOLDER]
**Date:** [PLACEHOLDER]
**Target URL:** [PLACEHOLDER]
**Authorization Reference:** [PLACEHOLDER]

---

## Legend

| Assessment | Meaning |
|------------|---------|
| PRESENT — STRONG | Header present and value is well-configured |
| PRESENT — ADEQUATE | Header present and value is acceptable but could be improved |
| PRESENT — WEAK | Header present but value provides minimal protection |
| MISSING | Header is absent — finding required |
| N/A | Not applicable to this application |

---

## 1. Content-Security-Policy (CSP)

**Header Observed:**
```
[PLACEHOLDER — Paste the full CSP value here, or "NOT PRESENT"]
```

| Check | Status | Notes |
|-------|--------|-------|
| Header present | [PRESENT / MISSING] | |
| Enforcement mode (not report-only) | [YES / NO / N/A] | |
| `default-src` is restrictive (not `*`) | [YES / NO / N/A] | |
| `script-src` disallows `unsafe-inline` | [YES / NO / N/A] | |
| `script-src` disallows `unsafe-eval` | [YES / NO / N/A] | |
| `frame-ancestors` directive present | [YES / NO / N/A] | |
| `report-uri` or `report-to` configured | [YES / NO / N/A] | |

**Overall Assessment:** [STRONG / ADEQUATE / WEAK / MISSING]
**Recommendation:** [PLACEHOLDER]
**Finding ID (if any):** [FIND-NNN or —]

---

## 2. Strict-Transport-Security (HSTS)

**Header Observed:**
```
[PLACEHOLDER — e.g., "Strict-Transport-Security: max-age=31536000; includeSubDomains; preload" or "NOT PRESENT"]
```

| Check | Status | Notes |
|-------|--------|-------|
| Header present | [PRESENT / MISSING] | |
| `max-age` ≥ 15768000 (6 months) | [YES / NO / N/A] | Current value: [VALUE] |
| `includeSubDomains` present | [YES / NO] | |
| `preload` present | [YES / NO] | |
| HSTS returned on HTTPS response (not HTTP) | [YES / NO / N/A] | |

**Overall Assessment:** [STRONG / ADEQUATE / WEAK / MISSING]
**Recommendation:** [PLACEHOLDER]
**Finding ID (if any):** [FIND-NNN or —]

---

## 3. X-Content-Type-Options

**Header Observed:**
```
[PLACEHOLDER — e.g., "X-Content-Type-Options: nosniff" or "NOT PRESENT"]
```

| Check | Status | Notes |
|-------|--------|-------|
| Header present | [PRESENT / MISSING] | |
| Value is `nosniff` | [YES / NO / N/A] | |

**Overall Assessment:** [STRONG / MISSING]
**Finding ID (if any):** [FIND-NNN or —]

---

## 4. Clickjacking Protection (X-Frame-Options or CSP frame-ancestors)

**X-Frame-Options Observed:**
```
[PLACEHOLDER — e.g., "X-Frame-Options: DENY" or "NOT PRESENT"]
```

**CSP frame-ancestors Observed:**
```
[PLACEHOLDER — value from CSP header, or "NOT PRESENT in CSP"]
```

| Check | Status | Notes |
|-------|--------|-------|
| X-Frame-Options present with DENY or SAMEORIGIN | [YES / NO] | |
| OR CSP `frame-ancestors` present and restrictive | [YES / NO] | |
| At least one clickjacking protection method in place | [YES / NO] | |

**Overall Assessment:** [PROTECTED / VULNERABLE]
**Finding ID (if any):** [FIND-NNN or —]

---

## 5. Referrer-Policy

**Header Observed:**
```
[PLACEHOLDER — e.g., "Referrer-Policy: strict-origin-when-cross-origin" or "NOT PRESENT"]
```

| Check | Status | Notes |
|-------|--------|-------|
| Header present | [PRESENT / MISSING] | |
| Policy is `strict-origin-when-cross-origin` or stricter | [YES / NO] | Current value: [VALUE] |
| Policy does not use `unsafe-url` | [YES / NO] | |

**Overall Assessment:** [STRONG / ADEQUATE / WEAK / MISSING]
**Finding ID (if any):** [FIND-NNN or —]

---

## 6. Permissions-Policy

**Header Observed:**
```
[PLACEHOLDER — e.g., "Permissions-Policy: camera=(), microphone=(), geolocation=()" or "NOT PRESENT"]
```

| Check | Status | Notes |
|-------|--------|-------|
| Header present | [PRESENT / MISSING] | |
| Sensitive features restricted (camera, mic, geolocation) | [YES / NO / N/A] | |

**Overall Assessment:** [PRESENT / MISSING]
**Finding ID (if any):** [FIND-NNN or —]

---

## 7. Cache-Control (Sensitive Responses)

**Header Observed (authenticated page):**
```
[PLACEHOLDER — e.g., "Cache-Control: no-cache, no-store, must-revalidate" or value observed]
```

| Check | Status | Notes |
|-------|--------|-------|
| Authenticated/sensitive pages: caching disabled (`no-store`) | [YES / NO / UNKNOWN] | |
| Login page: caching disabled | [YES / NO] | |
| API responses with sensitive data: caching disabled | [YES / NO / UNKNOWN] | |

**Overall Assessment:** [ADEQUATE / NEEDS REVIEW]
**Finding ID (if any):** [FIND-NNN or —]

---

## 8. CORS Configuration

**Headers Observed:**
```
Access-Control-Allow-Origin: [PLACEHOLDER or "NOT PRESENT"]
Access-Control-Allow-Credentials: [PLACEHOLDER or "NOT PRESENT"]
Access-Control-Allow-Methods: [PLACEHOLDER or "NOT PRESENT"]
```

| Check | Status | Notes |
|-------|--------|-------|
| `Access-Control-Allow-Origin` is NOT `*` for credentialed requests | [PASS / FAIL / N/A] | |
| Wildcard (`*`) combined with `Allow-Credentials: true` (CRITICAL if found) | [PRESENT / NOT PRESENT] | |
| Allowed origin is an appropriate allowlist | [YES / NO / N/A] | |

**Overall Assessment:** [SECURE / MISCONFIGURED / NOT APPLICABLE]
**Finding ID (if any):** [FIND-NNN or —]

---

## 9. Information-Exposing Headers

| Header | Observed Value | Recommendation |
|--------|---------------|----------------|
| `Server` | [PLACEHOLDER or "absent"] | Should be absent or non-verbose |
| `X-Powered-By` | [PLACEHOLDER or "absent"] | Should be absent |
| `X-AspNet-Version` | [PLACEHOLDER or "absent"] | Should be absent |
| `X-AspNetMvc-Version` | [PLACEHOLDER or "absent"] | Should be absent |
| `X-Generator` | [PLACEHOLDER or "absent"] | Should be absent |

**Finding ID (if any):** [FIND-NNN or —]

---

## Headers Summary

| Header | Assessment | Finding? |
|--------|-----------|---------|
| Content-Security-Policy | [STRONG/ADEQUATE/WEAK/MISSING] | [FIND-NNN or —] |
| Strict-Transport-Security | [STRONG/ADEQUATE/WEAK/MISSING] | [FIND-NNN or —] |
| X-Content-Type-Options | [STRONG/MISSING] | [FIND-NNN or —] |
| Clickjacking Protection | [PROTECTED/VULNERABLE] | [FIND-NNN or —] |
| Referrer-Policy | [STRONG/ADEQUATE/WEAK/MISSING] | [FIND-NNN or —] |
| Permissions-Policy | [PRESENT/MISSING] | [FIND-NNN or —] |
| Cache-Control | [ADEQUATE/NEEDS REVIEW] | [FIND-NNN or —] |
| CORS | [SECURE/MISCONFIGURED/N/A] | [FIND-NNN or —] |
| Info-Exposing Headers | [CLEAN/PRESENT] | [FIND-NNN or —] |

---

*Template: headers-checklist.md*
