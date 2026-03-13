# Command: /review-input-validation

## Objective

Review the application's input validation posture and injection risk exposure across in-scope endpoints and features.

The goal is to assess the attack surface for injection vulnerabilities (SQL, XSS, command injection, path traversal, SSRF, file upload abuse) based on observable application behavior and available evidence.

**Active injection payload testing requires explicit written authorization.** In passive review mode, this command assesses the attack surface and visible validation behaviors only.

This review is **evidence-based**. Findings require supporting observations.

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

- `.claude/skills/input-validation-audit/SKILL.md`

Evidence sources:

- `evidence/raw/`
- `evidence/reviewed/`
- `evidence/summarized/`

---

## Review Scope

Evaluate input validation posture including:

- all user-controlled input points (forms, URL parameters, headers, JSON body fields)
- server-side validation presence and adequacy
- output encoding for reflected values (XSS surface)
- file upload controls
- path traversal risk indicators
- SSRF-vulnerable parameter patterns
- error handling verbosity (injection feedback)

---

## Audit Method

### Step 1 — Map the Input Surface

From context and evidence, identify:

- HTML form fields (login, search, profile, upload, contact)
- URL query parameters and path parameters
- JSON/XML request body fields
- Cookie values used in application logic
- Any WebSocket or API-driven input surfaces

Prioritize high-risk inputs:
- search and filter fields (SQL injection risk)
- URL and redirect parameters (open redirect, SSRF)
- file upload fields (malicious file, path traversal)
- fields rendered back in HTML responses (XSS risk)

If the input surface cannot be enumerated from evidence, record review gap.

---

### Step 2 — Assess Visible Validation Behavior

From available evidence, observe:

- does the application accept input that should be rejected (no type or length validation)?
- are error messages verbose, revealing internal details (database errors, stack traces, file paths)?
- does the application appear to use parameterized queries or an ORM? (infer from tech stack in target-profile)
- are there differences in response behavior that suggest validation gaps?

Do not infer vulnerabilities solely from technology stack — require observable evidence.

---

### Step 3 — Assess XSS Exposure

Identify observable output points where user input is reflected in HTML:

- search result pages reflecting the query
- error pages echoing user-supplied input
- user profile fields visible to other users
- comment or message features

Assess:

- is HTML encoding applied to reflected values? (observable from page source or response)
- is a Content-Security-Policy in place to limit XSS impact?

If input cannot be submitted in passive mode, document surface as attack surface observation.

---

### Step 4 — Assess File Upload (if in scope)

If file upload functionality is in scope, evaluate from evidence:

- MIME type validation controls (observable from application behavior or documentation)
- file size restrictions
- storage location of uploaded files (web-accessible vs. isolated)
- dangerous file type acceptance indicators

Record review gap if file upload cannot be assessed without active testing.

---

### Step 5 — Assess Path Traversal Risk

For endpoints that reference files or resources by name:

- can the path component be manipulated to access files outside the intended directory?
- are `../` or URL-encoded traversal sequences visible as potential attack vectors?

Note as attack surface observation in passive mode if testing is not authorized.

---

### Step 6 — Assess SSRF Risk

For endpoints that accept URLs, external resource references, or webhook targets:

- can these parameters be directed to internal network resources?
- is there an observable allowlist or validation of accepted domains?

Record as suspected issue with low confidence if active SSRF testing is not authorized.

---

### Step 7 — Active Injection Testing (Authorized Mode Only)

**AUTHORIZATION REQUIRED:** Only perform this step if active testing authorization is explicitly confirmed in `.claude/context/audit-context.md`.

In authorized testing mode, make controlled observations per:

- `.claude/skills/input-validation-audit/templates/injection-test-notes.md`

Observe behavior with:

- SQL metacharacters: `'`, `"`, `;`, `--`
- HTML metacharacters: `<`, `>`, `"`
- Path traversal: `../`, `..\`
- Template syntax: `{{`, `${`, `<%`

Record behavioral observations only — do not perform exploitation.

---

### Step 8 — Normalize Findings

Use standardized finding format.

Each finding must include:

- title
- domain (input validation)
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

### Step 9 — Update Findings Register

Add findings and review gaps to the findings register at:

`.claude/templates/findings-register-template.md`

Ensure:

- no duplicates
- clear severity justification
- explicit evidence references

---

### Step 10 — Update Working Audit Note

Document:

- input surface coverage
- validation posture summary
- identified weaknesses
- areas requiring authorized active testing
- review gaps

---

## Output

This command should produce:

1. Input surface map summary
2. Validation posture assessment per surface
3. Structured findings for confirmed or suspected issues
4. Attack surface observations for passive-mode-only assessments
5. Review gaps where active testing authorization is required
6. Updated findings register
7. Updated audit working note

---

## Guardrails

- Do not confirm injection vulnerabilities without evidence of application response to relevant input.
- In passive mode, do not submit test payloads — document surface observations and require authorized testing.
- Verbose error messages are evidence but do not automatically confirm exploitable injection.
- XSS findings require observable reflection of user input without encoding — infer with care.
- File upload risks should be labeled as suspected or review gap if direct testing was not performed.
