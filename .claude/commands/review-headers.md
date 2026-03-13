> **Python CLI** (primary): `python scripts/run_audit.py audit headers   # or: audit tls, audit cookies`
> This command file is a methodology reference. Run the Python CLI command above for automated execution.

# Command: /review-headers

## Objective

Review browser-facing security headers and HTTPS posture for the target website.

This command evaluates the application's visible HTTP response headers and transport security indicators to identify security weaknesses, misconfigurations, or missing protections.

This review is **non-destructive** and based only on available evidence.

---

## Required Inputs

Read context first:

- `.claude/context/audit-context.md`
- `.claude/context/target-profile.md`
- `.claude/context/scope.md`

Apply rules:

- `.claude/rules/audit-scope-rules.md`
- `.claude/rules/evidence-quality-rules.md`
- `.claude/rules/severity-rating-rules.md`
- `.claude/rules/safety-authorization-rules.md`

Use skill:

- `.claude/skills/headers-tls-audit/SKILL.md`

Evidence sources:

- `evidence/raw/`
- `evidence/reviewed/`
- `evidence/summarized/`

---

## Review Scope

This review focuses on browser security controls visible through HTTP responses.

Primary areas include:

### Transport Security
- HTTPS enforcement
- HSTS usage
- mixed content exposure indicators

### Response Security Headers

Evaluate presence and configuration of:

- `Strict-Transport-Security`
- `Content-Security-Policy`
- `X-Frame-Options`
- `X-Content-Type-Options`
- `Referrer-Policy`
- `Permissions-Policy`

### Cookie Security Indicators

Where visible:

- `Secure`
- `HttpOnly`
- `SameSite`

### Server Information Exposure

Evaluate response headers for:

- server identification
- framework disclosure
- version leakage

---

## Audit Method

### Step 1 — Read Context

Determine:

- target website URL
- scope boundaries
- allowed testing posture
- known architecture hints

If only public evidence exists, limit conclusions accordingly.

---

### Step 2 — Review Available Evidence

Search the evidence folders for:

- captured HTTP headers
- browser developer console outputs
- scanner results
- curl responses
- screenshots showing headers

Summarize:

- what headers are visible
- which controls exist
- which controls are missing
- which controls appear weak or misconfigured

---

### Step 3 — Analyze Transport Security

Assess:

- HTTPS usage consistency
- redirect from HTTP to HTTPS
- HSTS presence
- potential downgrade exposure

Classify results as:

- confirmed control
- suspected weakness
- review gap

---

### Step 4 — Analyze Response Headers

Evaluate each key header.

#### Strict-Transport-Security
Check:

- header presence
- reasonable max-age
- includeSubDomains usage if applicable

#### Content-Security-Policy
Assess:

- presence
- overly permissive policies
- unsafe-inline or unsafe-eval usage
- missing CSP entirely

#### X-Frame-Options
Evaluate clickjacking protection.

#### X-Content-Type-Options
Check for `nosniff`.

#### Referrer-Policy
Check whether referrer exposure is controlled.

#### Permissions-Policy
Check whether browser features are restricted where applicable.

---

### Step 5 — Cookie Protection Review

If cookie headers appear in evidence, check for:

- Secure flag
- HttpOnly flag
- SameSite attribute

If cookies cannot be observed, mark as **review gap**.

---

### Step 6 — Server Information Exposure

Identify possible exposure such as:

- `Server`
- `X-Powered-By`
- framework identifiers
- version indicators

Note that disclosure alone is not always a vulnerability but may increase reconnaissance value.

---

### Step 7 — Normalize Findings

Use the normalized finding structure.

Each finding should include:

- title
- domain (headers / transport)
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

### Step 8 — Update Findings Register

Update the workspace findings register using:

`.claude/templates/findings-register-template.md`

Add:

- confirmed header weaknesses
- misconfiguration findings
- review gaps

Avoid duplicate findings.

---

### Step 9 — Update Working Audit Note

Update the active audit note with:

- summary of header posture
- confirmed weaknesses
- configuration observations
- areas requiring further evidence

---

## Output

This command should produce:

1. Header security posture summary
2. Structured findings for any issues
3. Review gaps for areas lacking evidence
4. Updates to the findings register
5. Updates to the working audit note

---

## Guardrails

- Do not assume header values without evidence.
- Do not infer application behavior from header absence alone unless risk is clear.
- Missing headers should be evaluated in context, not automatically treated as critical vulnerabilities.
- If no header evidence exists, record a review gap instead of creating findings.
