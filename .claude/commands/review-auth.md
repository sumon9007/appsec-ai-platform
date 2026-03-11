# Command: /review-auth

## Objective

Review authentication mechanisms and login-related security controls for the target website.

The goal is to identify weaknesses in authentication flow design, credential handling protections, and account protection mechanisms.

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

Use skill:

- `.claude/skills/auth-access-audit/SKILL.md`

Evidence sources:

- `evidence/raw/`
- `evidence/reviewed/`
- `evidence/summarized/`

---

## Review Scope

Evaluate authentication posture including:

- login endpoints
- password policies (if visible)
- account lockout behavior
- MFA presence indicators
- password reset flow
- session establishment indicators

---

## Audit Method

### Step 1 — Identify Authentication Entry Points

From context and evidence, identify:

- login pages
- admin login endpoints
- authentication APIs
- SSO integrations if visible

If none are visible, record review gap.

---

### Step 2 — Evaluate Login Protection

Look for evidence of:

- login attempt throttling
- account lockout mechanisms
- captcha usage
- anomaly detection indicators

If evidence does not exist, record review gap.

---

### Step 3 — Evaluate MFA Presence

Determine if:

- multi-factor authentication exists
- MFA is optional or mandatory
- privileged roles require stronger authentication

If no evidence exists, classify as review gap.

---

### Step 4 — Evaluate Password Reset Mechanism

Assess visible evidence of reset flows:

- token-based reset
- email verification
- secure reset process

Identify risky behaviors if visible such as:

- predictable reset tokens
- insecure reset links
- excessive information disclosure

---

### Step 5 — Evaluate Session Handling Indicators

Where evidence exists, review:

- session cookie attributes
- session lifetime hints
- logout behavior
- session invalidation indicators

---

### Step 6 — Identify Authentication Risk Patterns

Look for indicators of:

- weak account protection
- credential stuffing exposure
- lack of MFA
- insecure reset workflows
- session mismanagement

Only confirm issues if evidence supports them.

---

### Step 7 — Normalize Findings

Use standardized finding format.

Each finding must include:

- title
- domain (authentication)
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

Add findings and review gaps to the findings register.

Ensure:

- no duplicates
- clear severity justification
- explicit evidence references

---

### Step 9 — Update Working Audit Note

Document:

- authentication posture summary
- observed strengths
- weaknesses
- review gaps
- evidence limitations

---

## Output

This command should produce:

1. Authentication security posture summary
2. Structured findings if issues exist
3. Review gaps where visibility is insufficient
4. Updated findings register
5. Updated audit working note

---

## Guardrails

- Do not assume authentication behavior without evidence.
- Do not claim credential attacks or brute-force weaknesses without testing evidence.
- Missing MFA visibility should be marked as review gap rather than confirmed failure.