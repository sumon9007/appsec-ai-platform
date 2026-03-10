# Security Misconfiguration Review Template

Documents misconfiguration findings per configuration area.

**Auditor:** [PLACEHOLDER]
**Date:** [PLACEHOLDER]
**Target:** [PLACEHOLDER]

---

## Configuration Area Review Record

Complete one section per configuration area reviewed.

---

### Area: Error Handling and Debug Mode

| Field | Value |
|-------|-------|
| **Debug Mode Active?** | [Yes / No / Unknown] |
| **Debug Toolbar Visible?** | [Yes / No / N/A] |
| **Verbose Errors on 500?** | [Yes — stack trace / Yes — internal path / No — generic message] |
| **Verbose Errors on 404?** | [Yes / No] |
| **Verbose Errors on 403?** | [Yes / No] |
| **Custom Error Pages?** | [Yes / No] |

**Observed Setting:** [PLACEHOLDER — Describe what was observed, e.g., "500 error returned a full Django stack trace revealing the internal path /home/ubuntu/app/views.py and PostgreSQL query"]

**Expected Setting:** Debug mode disabled in production; all error responses return a generic user-facing message without internal detail

**Risk:** [Critical / High / Medium / Low]

**Recommendation:** [PLACEHOLDER — e.g., "Set DEBUG=False in Django settings for the production environment. Implement a custom 500 error handler that returns a generic page without stack trace."]

**Evidence:** [EVID-YYYY-MM-DD-NNN]

**Finding ID:** [FIND-NNN or —]

---

### Area: Sensitive File Exposure

| File / Path | Accessible? | HTTP Response | Sensitivity | Finding ID |
|-------------|-------------|--------------|-------------|------------|
| `/.env` | [Yes / No] | [Status code + excerpt if accessible] | Critical | [FIND-NNN or —] |
| `/.git/config` | [Yes / No] | [Status code] | High | [FIND-NNN or —] |
| `/.git/HEAD` | [Yes / No] | [Status code] | High | [FIND-NNN or —] |
| `/backup.sql` | [Yes / No] | [Status code] | Critical | [FIND-NNN or —] |
| `/phpinfo.php` | [Yes / No / N/A] | [Status code] | High | [FIND-NNN or —] |
| `/server-status` | [Yes / No / N/A] | [Status code] | Medium | [FIND-NNN or —] |
| `/actuator/env` | [Yes / No / N/A] | [Status code] | High | [FIND-NNN or —] |
| `/actuator/health` | [Yes / No / N/A] | [Status code] | Low | [FIND-NNN or —] |
| `/.DS_Store` | [Yes / No] | [Status code] | Low | [FIND-NNN or —] |
| `/web.config` | [Yes / No / N/A] | [Status code] | High | [FIND-NNN or —] |
| `[Other]` | [Yes / No] | [Status code] | [Severity] | [FIND-NNN or —] |

---

### Area: Default Credentials and Exposed Admin Interfaces

| Interface | URL | Accessible? | Authentication Required? | Risk | Finding ID |
|-----------|-----|-------------|--------------------------|------|------------|
| Admin panel | [PLACEHOLDER] | [Yes / No] | [Yes / No] | [High/Critical] | [FIND-NNN or —] |
| Database admin (phpMyAdmin, Adminer) | [PLACEHOLDER] | [Yes / No / N/A] | [Yes / No] | [Critical] | [FIND-NNN or —] |
| API documentation (Swagger) | [PLACEHOLDER] | [Yes / No] | [Yes / No] | [Medium/High] | [FIND-NNN or —] |
| Monitoring dashboard | [PLACEHOLDER] | [Yes / No / N/A] | [Yes / No] | [High] | [FIND-NNN or —] |
| Container management | [PLACEHOLDER] | [Yes / No / N/A] | [Yes / No] | [Critical] | [FIND-NNN or —] |

**Note:** Default credential testing was [performed with authorization / not performed — passive observation only].

---

### Area: Directory Listing

| Directory | Listing Enabled? | Contents | Risk | Finding ID |
|-----------|-----------------|----------|------|------------|
| `/uploads/` | [Yes / No] | [PLACEHOLDER if yes] | High | [FIND-NNN or —] |
| `/files/` | [Yes / No] | [PLACEHOLDER if yes] | High | [FIND-NNN or —] |
| `/static/` | [Yes / No] | [PLACEHOLDER if yes] | Low | [FIND-NNN or —] |
| `/assets/` | [Yes / No] | [PLACEHOLDER if yes] | Low | [FIND-NNN or —] |
| `[Other]` | [Yes / No] | [PLACEHOLDER if yes] | [Severity] | [FIND-NNN or —] |

---

### Area: CORS Configuration

| Field | Value |
|-------|-------|
| `Access-Control-Allow-Origin` | [PLACEHOLDER — value or "not present"] |
| `Access-Control-Allow-Credentials` | [true / false / not present] |
| `Access-Control-Allow-Methods` | [PLACEHOLDER or "not present"] |
| **Assessment** | [Secure / Misconfigured — see finding] |

**Risk:** [Critical if wildcard + credentials / Low if wildcard without credentials for public data]
**Finding ID:** [FIND-NNN or —]

---

### Area: robots.txt and Sitemap Exposure

| File | Accessible? | Sensitive Paths Revealed? | Notes | Finding ID |
|------|-------------|--------------------------|-------|------------|
| `/robots.txt` | [Yes / No] | [Yes — list paths / No] | [NOTES] | [FIND-NNN or —] |
| `/sitemap.xml` | [Yes / No] | [Yes / No] | [NOTES] | [FIND-NNN or —] |

---

### Area: Information-Disclosing HTTP Headers

*(Cross-reference with headers-checklist.md)*

| Header | Value Observed | Risk |
|--------|---------------|------|
| `Server` | [PLACEHOLDER or "absent"] | [Medium if version exposed] |
| `X-Powered-By` | [PLACEHOLDER or "absent"] | [Low/Medium] |
| `X-AspNet-Version` | [PLACEHOLDER or "absent"] | [Low] |

**Finding ID (if any):** [FIND-NNN or —]

---

## Misconfiguration Review Summary

| Area | Assessment | Findings |
|------|-----------|---------|
| Error handling and debug mode | [PASS / FAIL] | [FIND-NNN or —] |
| Sensitive file exposure | [PASS / FAIL] | [FIND-NNN or —] |
| Admin interfaces | [PASS / FAIL / N/A] | [FIND-NNN or —] |
| Directory listing | [PASS / FAIL] | [FIND-NNN or —] |
| CORS | [PASS / FAIL] | [FIND-NNN or —] |
| robots.txt/sitemap | [PASS / FAIL] | [FIND-NNN or —] |
| HTTP info headers | [PASS / FAIL] | [FIND-NNN or —] |

---

*Template: misconfig-review-template.md*
