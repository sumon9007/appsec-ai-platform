# Skill: Security Misconfiguration Audit

## Purpose

Assess the application and its supporting infrastructure for security misconfigurations, insecure defaults, unnecessary exposure, and hardening gaps that could provide an attacker with information, unauthorized access, or an exploitation foothold.

---

## Inputs Required

| Input | Source | Required? |
|-------|--------|-----------|
| Target application URL(s) | `.claude/context/scope.md` | Required |
| Hosting environment details | `.claude/context/target-profile.md` | Important context |
| Authorization confirmation | `.claude/context/audit-context.md` | Required |

---

## Method

### Phase 1: Passive Reconnaissance

1. Observe information disclosed by the application without active testing:
   - HTTP response headers revealing server technology and version
   - Error messages revealing internal paths, database types, or stack traces
   - HTML source comments revealing internal information
   - `robots.txt` — does it reveal sensitive paths?
   - `sitemap.xml` — does it reference admin or sensitive paths?

2. Common file exposure check — passively request paths that commonly expose sensitive data:
   - `/.env` — environment file with secrets
   - `/.git/config` or `/.git/HEAD` — exposed git repository
   - `/backup.sql`, `/dump.sql`, `/db.sql` — database dumps
   - `/phpinfo.php` — PHP info page
   - `/server-status` — Apache server status
   - `/actuator` or `/actuator/env` — Spring Boot actuator endpoints
   - `/.DS_Store` — macOS directory metadata
   - `/web.config`, `/WEB-INF/web.xml` — application configuration

### Phase 2: Error Handling Review

3. Trigger application errors (where authorized) and assess:
   - Do error pages expose stack traces?
   - Do error pages reveal internal file paths?
   - Do error pages reveal database query details?
   - Do error pages reveal framework or library versions?
   - Is there a custom error page that conceals internal details?

4. Verify error behavior for:
   - 404 Not Found — generic or verbose?
   - 500 Internal Server Error — generic or verbose?
   - 403 Forbidden — generic or informative?
   - Authentication failure — appropriate messaging?

### Phase 3: Debug Mode Check

5. Indicators of debug mode being active:
   - Verbose stack traces in error responses
   - Debug toolbar visible in browser (Django Debug Toolbar, Laravel Debugbar)
   - Debug endpoints accessible (`/debug`, `/_debug`, `/__debug__`)
   - Logging level set to DEBUG in observable configuration
   - Development routes accessible in production (e.g., Swagger UI without authentication, phpMyAdmin)

### Phase 4: Default Credentials Check (Passive)

6. Identify any management interfaces exposed in scope:
   - Admin panels (CMS admin, database admin)
   - Development tools (phpMyAdmin, Adminer, Jupyter Notebook)
   - API documentation portals with test functionality (Swagger UI, Redoc)
   - Container/infrastructure management (Kubernetes dashboard, Portainer)

7. For any identified management interfaces:
   - Are they accessible from the internet?
   - Do they require authentication?
   - **Do not test default credentials unless explicitly authorized in writing**
   - Note as a finding if accessible without obvious authentication requirement

### Phase 5: Directory Listing

8. Check for directory listing enabled:
   - Request directories that are likely to exist: `/uploads/`, `/files/`, `/assets/`, `/static/`
   - If a file listing is returned rather than a 403/404: finding required

### Phase 6: CORS Misconfiguration

9. Review CORS configuration for critical misconfiguration:
   - `Access-Control-Allow-Origin: *` combined with `Access-Control-Allow-Credentials: true` — Critical
   - Wildcard origin with no credentials — typically Low risk
   - Reflective CORS (`origin` header value reflected in `Access-Control-Allow-Origin`) — High risk

### Phase 7: Cloud-Specific Checks (if applicable)

10. If cloud-hosted (AWS, GCP, Azure):
    - Are storage buckets/blobs publicly accessible? (Check common names: `[appname]-backup`, `[appname]-uploads`)
    - Are cloud metadata endpoints accessible from within the application? (SSRF via cloud metadata)
    - Are any cloud management interfaces exposed without MFA?

### Phase 8: Complete Hardening Checklist

11. Work through `hardening-checklist.md` systematically for all applicable items

---

## Outputs

| Output | Template | Description |
|--------|---------|-------------|
| Misconfiguration review | `misconfig-review-template.md` | Per-configuration-area findings |
| Hardening checklist | `hardening-checklist.md` | Completed checklist |
| Findings | Standard finding format | One per misconfiguration found |
| Evidence items | EVID- convention | HTTP responses, screenshots |

---

## Templates Used

- `.claude/skills/security-misconfig-audit/templates/misconfig-review-template.md`
- `.claude/skills/security-misconfig-audit/templates/hardening-checklist.md`

---

## References

- [OWASP A05:2021 — Security Misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)
- [OWASP Testing Guide — Configuration and Deployment Management Testing](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/)
- [CWE-16 — Configuration](https://cwe.mitre.org/data/definitions/16.html)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks) — relevant to the application's technology stack
