# Command: /review-misconfig

## Objective

Review the application and its supporting infrastructure for security misconfigurations, insecure defaults, unnecessary exposure, and hardening gaps.

The goal is to identify configuration weaknesses that could provide an attacker with information disclosure, unauthorized access, or an exploitation foothold — without relying on active exploit techniques.

This review is primarily **passive** and evidence-based.

---

## Required Inputs

Read context:

- `.claude/context/audit-context.md`
- `.claude/context/target-profile.md`
- `.claude/context/scope.md`
- `.claude/context/assumptions.md`

Apply rules:

- `.claude/rules/evidence-quality-rules.md`
- `.claude/rules/audit-scope-rules.md`
- `.claude/rules/severity-rating-rules.md`
- `.claude/rules/safety-authorization-rules.md`

Use skill:

- `.claude/skills/security-misconfig-audit/SKILL.md`

Evidence sources:

- `evidence/raw/`
- `evidence/reviewed/`
- `evidence/summarized/`

---

## Review Scope

Evaluate misconfiguration posture including:

- technology and version disclosure in HTTP headers and error pages
- common sensitive file exposure (`.env`, `.git`, backup files, config files)
- debug mode indicators and development tooling exposure
- management interface accessibility and authentication requirement
- directory listing configuration
- CORS policy misconfiguration
- cloud-specific exposure risks (if applicable)
- verbose error handling behavior

---

## Audit Method

### Step 1 — Passive Reconnaissance

From available evidence, observe what the application discloses without active testing:

- server and framework identification in HTTP response headers (`Server`, `X-Powered-By`)
- stack traces or internal path references in visible error responses
- HTML source code comments revealing internal information
- technology hints in `robots.txt` or `sitemap.xml`

Record all observed disclosures. Assess risk in context — disclosure alone is not always a high-severity finding.

---

### Step 2 — Sensitive File Exposure Check

Assess whether any of the following common sensitive paths are accessible or referenced in evidence:

- `/.env` — environment file with secrets
- `/.git/config` or `/.git/HEAD` — exposed source control repository
- `/backup.sql`, `/dump.sql` — database exports
- `/phpinfo.php` — PHP configuration page
- `/server-status` — Apache status endpoint
- `/actuator` or `/actuator/env` — Spring Boot actuator
- `/.DS_Store` — macOS directory metadata
- `/web.config` or `/WEB-INF/web.xml` — application configuration files

If any of these paths returned content in captured evidence, this is a finding.

If these paths were not tested, record as review gap if they are in scope.

---

### Step 3 — Error Handling Assessment

From observed error responses in evidence:

- do 404, 500, or 403 error pages expose stack traces?
- do error pages reveal internal file paths, database query details, or framework versions?
- is there a custom error page that suppresses internal details?

Verbose error messages that expose internal structure are a finding (typically Medium or Low depending on content).

---

### Step 4 — Debug Mode Indicators

Identify indicators of debug mode in production:

- visible debug toolbars (Django Debug Toolbar, Laravel Debugbar)
- debug-level endpoints accessible without authentication (`/debug`, `/_debug`)
- development routes or tools accessible (Swagger UI without authentication, phpMyAdmin)
- verbose logging level visible in application responses

Debug mode in production is a finding (typically Medium to High depending on exposure).

---

### Step 5 — Management Interface Exposure

Identify any management or administrative interfaces accessible in scope:

- CMS or admin panels
- database administration tools (phpMyAdmin, Adminer)
- API documentation with test functionality (Swagger UI)
- container or infrastructure management interfaces

For identified interfaces:

- is the interface accessible from the internet without VPN or IP restriction?
- does it require authentication before access?

**Do not test default credentials unless explicitly authorized in writing.**

Accessible management interfaces are a finding — at minimum Medium severity.

---

### Step 6 — Directory Listing

From evidence or observable responses:

- do any directories return a file listing instead of a 403 or 404?
- is directory listing enabled on upload directories, static asset directories, or application directories?

Directory listing enabled on any path containing potentially sensitive files is a finding.

---

### Step 7 — CORS Misconfiguration

From captured HTTP responses in evidence:

- is `Access-Control-Allow-Origin: *` combined with `Access-Control-Allow-Credentials: true`? → Critical finding
- is the `Access-Control-Allow-Origin` header reflecting the request `Origin` value dynamically? → High finding
- is CORS configured too broadly for the application's intended use?

---

### Step 8 — Cloud-Specific Checks (if applicable)

If the application is cloud-hosted (from `target-profile.md`):

- are storage buckets or blob containers publicly accessible? (infer from common naming patterns if direct access exists in evidence)
- are cloud metadata endpoints referenced in observable application behavior? (SSRF via cloud metadata concern)
- are cloud management portals accessible without MFA requirement indicated?

Record as suspected or review gap if evidence is insufficient.

---

### Step 9 — Complete Hardening Checklist

Work through the hardening areas in:

`.claude/skills/security-misconfig-audit/templates/hardening-checklist.md`

Record pass, fail, or review-gap for each applicable item.

---

### Step 10 — Normalize Findings

Use standardized finding format.

Each finding must include:

- title
- domain (misconfiguration)
- severity
- confidence
- evidence
- observation
- risk
- recommendation
- acceptance criteria mapping
- status
- review type

---

### Step 11 — Update Findings Register

Add findings and review gaps to:

`.claude/templates/findings-register-template.md`

Ensure:

- no duplicates
- clear severity justification
- explicit evidence references

---

### Step 12 — Update Working Audit Note

Document:

- misconfiguration posture summary
- identified exposures and weaknesses
- management interfaces observed
- review gaps where evidence is insufficient

---

## Output

This command should produce:

1. Misconfiguration posture summary
2. Sensitive file exposure assessment
3. Error handling and debug mode findings
4. Management interface exposure assessment
5. CORS assessment
6. Hardening checklist completion
7. Structured findings for all confirmed issues
8. Review gaps where evidence is insufficient
9. Updated findings register
10. Updated audit working note

---

## Guardrails

- Do not test default credentials unless explicitly authorized in writing.
- Server technology disclosure is not automatically a high-severity finding — assess in context.
- Out-of-scope cloud storage or third-party services must be labeled `[OUT OF SCOPE — NOT TESTED]`.
- Sensitive file exposure findings must be supported by direct access evidence — do not assume files are accessible without confirmation.
- CORS misconfiguration severity depends on credential sharing configuration — assess carefully.
