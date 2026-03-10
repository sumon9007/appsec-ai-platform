# Security Hardening Checklist

Comprehensive checklist for assessing security hardening controls.

**Auditor:** [PLACEHOLDER]
**Date:** [PLACEHOLDER]
**Target:** [PLACEHOLDER]

---

## Legend

| Status | Meaning |
|--------|---------|
| PASS | Control properly implemented |
| FAIL | Control absent or improperly implemented |
| PARTIAL | Implemented with gaps |
| N/A | Not applicable |
| UNKNOWN | Could not determine |

---

## 1. Application Debug Mode

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 1.1 | Debug mode is disabled in production | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 1.2 | No debug toolbar or development panels visible | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 1.3 | Debug endpoints not accessible (/__debug__, /console, etc.) | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 2. Error Verbosity

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 2.1 | Application errors do not expose stack traces to end users | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 2.2 | Application errors do not expose internal file paths | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 2.3 | Application errors do not expose database query details | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 2.4 | Custom error pages in place for 404, 403, 500 | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 2.5 | Framework/library versions not exposed in error messages | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 3. Directory Listing

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 3.1 | Directory listing disabled on web server | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 3.2 | Upload directories not browseable | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 3.3 | Static asset directories not browseable | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 4. Default and Hardcoded Credentials

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 4.1 | No default credentials in use on any admin interface | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 4.2 | No hardcoded credentials in observable configuration | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 4.3 | API keys not present in client-side source code | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 4.4 | `.env` file not accessible via HTTP request | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 5. Exposed Admin Interfaces

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 5.1 | Admin panel accessible only from authorized IPs or VPN | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 5.2 | Database admin tools (phpMyAdmin, Adminer) not accessible from internet | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 5.3 | API documentation (Swagger) protected by authentication in production | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 5.4 | Container management interfaces not accessible from internet | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 5.5 | Server monitoring dashboards not accessible from internet | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 6. Sensitive File Exposure

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 6.1 | `.env` returns 403/404 | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 6.2 | `.git/` directory returns 403/404 | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 6.3 | Backup files (*.sql, *.bak, *.tar.gz) not accessible | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 6.4 | phpinfo() pages not accessible | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 6.5 | Framework-specific config files not accessible (web.config, etc.) | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 6.6 | Cloud metadata endpoint not exposed via SSRF vector | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 7. CORS Policy

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 7.1 | `Access-Control-Allow-Origin` is not wildcard (`*`) for credentialed requests | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 7.2 | CORS origin allowlist is restrictive and appropriate | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 7.3 | Wildcard (`*`) with `Access-Control-Allow-Credentials: true` is NOT present | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 8. robots.txt and Sitemap

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 8.1 | `robots.txt` does not reveal sensitive admin or internal paths | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 8.2 | `sitemap.xml` does not reveal sensitive internal paths | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 9. Information Disclosure Headers

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 9.1 | `Server` header absent or non-verbose | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 9.2 | `X-Powered-By` header absent | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 9.3 | `X-AspNet-Version` and `X-AspNetMvc-Version` absent | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 10. Unnecessary Services and Features

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 10.1 | Only required HTTP methods are allowed (e.g., TRACE disabled) | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 10.2 | Unused application features are disabled | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 10.3 | File upload not enabled if not required by the application | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## Hardening Checklist Summary

| Section | Controls | PASS | FAIL | PARTIAL | N/A | UNKNOWN |
|---------|----------|------|------|---------|-----|---------|
| 1. Debug Mode | 3 | — | — | — | — | — |
| 2. Error Verbosity | 5 | — | — | — | — | — |
| 3. Directory Listing | 3 | — | — | — | — | — |
| 4. Default Credentials | 4 | — | — | — | — | — |
| 5. Admin Interfaces | 5 | — | — | — | — | — |
| 6. Sensitive Files | 6 | — | — | — | — | — |
| 7. CORS Policy | 3 | — | — | — | — | — |
| 8. robots.txt/Sitemap | 2 | — | — | — | — | — |
| 9. Info Headers | 3 | — | — | — | — | — |
| 10. Unnecessary Services | 3 | — | — | — | — | — |
| **Total** | **37** | — | — | — | — | — |

---

*Template: hardening-checklist.md*
