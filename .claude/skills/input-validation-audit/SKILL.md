> **Reference Guide** — This skill documents the methodology. For automated execution, run:
> `python scripts/run_audit.py audit full --tools input`
> Use this skill to interpret tool output, conduct manual review steps, or guide authorized active testing.

# Skill: Input Validation and Injection Risk Audit

## Purpose

Assess whether the application properly validates, sanitizes, and encodes user-supplied input to prevent injection attacks, including SQL injection, cross-site scripting (XSS), command injection, path traversal, and server-side request forgery (SSRF).

---

## Inputs Required

| Input | Source | Required? |
|-------|--------|-----------|
| Target application URL(s) | `.claude/context/scope.md` | Required |
| In-scope endpoints and features | `.claude/context/scope.md` | Required |
| Authorization confirmation | `.claude/context/audit-context.md` | Required |
| Tech stack (framework, DB type) | `.claude/context/target-profile.md` | Important context |

**AUTHORIZATION REQUIRED:** Active injection testing (submitting payloads) requires explicit written authorization. In passive review mode, assess the attack surface and observable validation behaviors only.

---

## Method

### Phase 1: Input Surface Mapping

1. Identify all user-controlled input points:
   - HTML form fields (text, email, password, textarea, hidden fields, file upload)
   - URL query parameters (`?search=value`)
   - URL path parameters (`/users/123`, `/files/report.pdf`)
   - HTTP headers (User-Agent, Referer, X-Forwarded-For, custom headers)
   - JSON/XML request body parameters
   - Cookie values
   - WebSocket messages (if applicable)

2. Prioritize high-risk input types:
   - Search and filter fields (SQL injection risk)
   - URL/redirect parameters (open redirect, SSRF)
   - File upload (malicious file, path traversal)
   - Template rendering fields (template injection)
   - Fields used in system commands (command injection)
   - Fields used in LDAP queries (LDAP injection)

### Phase 2: Server-Side Validation Assessment

3. For each identified input point, assess:
   - Is validation performed server-side? (Client-side only = not sufficient)
   - Is input length limited on the server?
   - Is input type validated (accepts only expected format)?
   - Is input sanitized or encoded before use?
   - For database queries: are parameterized queries or ORMs in use? (observable via framework/stack)

4. Observe application behavior with unexpected input:
   - Does the application return verbose errors revealing internal structure?
   - Does the application accept input that should be rejected?
   - Are there differences in response times or behavior that suggest processing differences?

### Phase 3: Cross-Site Scripting (XSS) Surface

5. Identify output points where user input is reflected in HTML responses:
   - Search results reflecting the search query
   - User profile fields displayed to other users
   - Error messages that include user input
   - Comments, posts, or user-generated content

6. Assess encoding:
   - Is HTML encoding applied to all reflected values?
   - Are JavaScript contexts separately handled (JS encoding vs. HTML encoding)?
   - Is a Content-Security-Policy in place to mitigate XSS impact?

### Phase 4: File Upload Security

7. If file upload is in scope:
   - Is the file's MIME type validated server-side? (Not just the extension)
   - Is the file size limited?
   - Is the uploaded file stored with a non-guessable name?
   - Is the upload directory outside the web root, or are uploaded files not directly executed?
   - Are dangerous file types (PHP, JSP, ASP, HTML, SVG with scripts) blocked?
   - Are files scanned for malware? (Ideally)

### Phase 5: Path Traversal and File Access

8. For endpoints that reference files:
   - Can path components be manipulated to access files outside the intended directory?
   - Are `../` sequences and URL-encoded equivalents blocked?

### Phase 6: Server-Side Request Forgery (SSRF)

9. For endpoints that accept URLs or server-side fetch targets:
   - Can the URL be pointed to internal network resources? (169.254.x.x, 10.x.x.x, localhost)
   - Is there a URL allowlist in place?

### Phase 7: Injection Test Observations (Authorized Testing Only)

**AUTHORIZATION REQUIRED:** These steps require explicit authorization for active testing.

10. In authorized testing mode, make controlled injection test observations per `injection-test-notes.md`:
    - Observe behavior with SQL metacharacters: `'`, `"`, `;`, `--`
    - Observe behavior with HTML metacharacters: `<`, `>`, `"`
    - Observe behavior with path traversal: `../`, `..\`
    - Observe behavior with template syntax: `{{`, `${`, `<%`
    - Record behavior only — do not perform exploitation

---

## Outputs

| Output | Template | Description |
|--------|---------|-------------|
| Validation review per endpoint | `validation-review-template.md` | Input surface and validation assessment |
| Injection test observations | `injection-test-notes.md` | Observations from testing (authorized mode only) |
| Findings | Standard finding format | One per identified vulnerability |
| Evidence items | EVID- convention | Response captures, error messages observed |

---

## Templates Used

- `.claude/skills/input-validation-audit/templates/validation-review-template.md`
- `.claude/skills/input-validation-audit/templates/injection-test-notes.md`

---

## References

- [OWASP A03:2021 — Injection](https://owasp.org/Top10/A03_2021-Injection/)
- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [CWE-89 — SQL Injection](https://cwe.mitre.org/data/definitions/89.html)
- [CWE-79 — Cross-Site Scripting](https://cwe.mitre.org/data/definitions/79.html)
