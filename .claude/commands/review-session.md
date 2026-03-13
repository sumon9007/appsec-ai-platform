> **Python CLI** (primary): `python scripts/run_audit.py audit full --tools session,cookies`
> This command file is a methodology reference. Run the Python CLI command above for automated execution.

# Command: /review-session

## Objective

Review session management and JWT implementation for the target application.

The goal is to identify weaknesses in session token handling, JWT algorithm configuration, cookie attribute security, session lifecycle controls, and logout invalidation behavior.

This review is **non-destructive** and evidence-based.

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

- `.claude/skills/session-jwt-audit/SKILL.md`

Evidence sources:

- `evidence/raw/`
- `evidence/reviewed/`
- `evidence/summarized/`

---

## Review Scope

Evaluate session management posture including:

- session token type (cookie-based, JWT, localStorage)
- JWT algorithm and claims (if JWT is in use)
- cookie attribute security (HttpOnly, Secure, SameSite, scope)
- session fixation controls
- logout and token invalidation behavior
- session timeout and absolute lifetime
- token entropy and predictability indicators

---

## Audit Method

### Step 1 — Identify Session Mechanism

From context and evidence, determine:

- how the application maintains session state (cookie, JWT, URL parameter, localStorage)
- where the session token appears in captured traffic
- whether JWT or opaque session IDs are in use

If no session evidence exists, record review gap.

---

### Step 2 — Analyze JWT (if applicable)

If JWTs are in use, assess from available evidence:

- algorithm claim in JWT header (`alg` field)
  - `alg: none` → Critical finding
  - `alg: HS256` → note for key strength review
  - `alg: RS256` or `ES256` → preferred
- expiry (`exp`) claim presence and reasonable lifetime
- sensitive data unnecessarily embedded in payload
- issuer (`iss`) and audience (`aud`) claim presence

If JWTs cannot be observed, record review gap.

---

### Step 3 — Evaluate Cookie Attributes

Where Set-Cookie headers appear in evidence, assess:

- `HttpOnly` flag — prevents JavaScript access
- `Secure` flag — HTTPS-only transmission
- `SameSite` attribute — CSRF protection (`Strict` or `Lax`)
- cookie `Domain` and `Path` scope — are they appropriately restricted?
- cookie lifetime — is it session-only or persistent?

If cookies cannot be observed, mark as review gap.

---

### Step 4 — Evaluate Session Lifecycle

Assess from evidence:

- session fixation: is a new session token issued after login?
- logout: is the session invalidated server-side on logout?
- inactivity timeout: is there an observable session expiry on inactivity?
- absolute timeout: is there an enforced maximum session lifetime?

Active validation of logout invalidation requires authorized testing.

---

### Step 5 — Evaluate Token Entropy (Where Observable)

Where session tokens or JWT claims are visible in evidence:

- does the session ID appear to have sufficient randomness? (should be ≥ 128 bits)
- does the session ID appear sequential or predictable? (flag as suspected issue)

Do not assert weak entropy without observable evidence.

---

### Step 6 — Identify Session Risk Patterns

Look for indicators of:

- reusable tokens after logout
- missing HttpOnly or Secure cookie flags
- excessive JWT lifetime
- session tokens in URLs
- sensitive data exposed in JWT payload without encryption

Only confirm issues with supporting evidence.

---

### Step 7 — Normalize Findings

Use standardized finding format.

Each finding must include:

- title
- domain (session management)
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

Add findings and review gaps to the findings register at:

`.claude/templates/findings-register-template.md`

Ensure:

- no duplicates
- clear severity justification
- explicit evidence references

---

### Step 9 — Update Working Audit Note

Document:

- session management posture summary
- observed token type and mechanism
- identified weaknesses
- review gaps
- evidence limitations

---

## Output

This command should produce:

1. Session management posture summary
2. JWT assessment (if applicable)
3. Cookie security assessment
4. Structured findings for any confirmed or suspected issues
5. Review gaps where evidence is insufficient
6. Updated findings register
7. Updated audit working note

---

## Guardrails

- Do not claim token forgery is possible without JWT evidence showing `alg: none` or a clearly weak configuration.
- Absence of observed cookie flags should be a review gap if cookies were not captured in evidence.
- Do not test logout invalidation without explicit active testing authorization.
- Session token predictability requires observable evidence — do not assume without it.
