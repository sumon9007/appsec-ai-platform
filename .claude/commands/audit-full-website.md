# /audit-full-website

## Objective

Perform a structured end-to-end website security audit for the currently defined target using the workspace context, rules, skills, templates, and available evidence.

This command acts as the main orchestrator for a full website review.

It should:
- establish the active audit state
- review the target through the relevant security lenses
- create structured findings where evidence supports them
- identify review gaps where evidence is insufficient
- update working audit artifacts
- prepare the workspace for final reporting

---

## Required Inputs

Read these first:

- `.claude/context/audit-context.md`
- `.claude/context/target-profile.md`
- `.claude/context/scope.md`
- `.claude/context/assumptions.md`

Then read and apply these rules:

- `.claude/rules/audit-scope-rules.md`
- `.claude/rules/evidence-quality-rules.md`
- `.claude/rules/severity-rating-rules.md`
- `.claude/rules/reporting-rules.md`
- `.claude/rules/safety-authorization-rules.md`

Use these skills as relevant:

- `.claude/skills/headers-tls-audit/SKILL.md`
- `.claude/skills/auth-access-audit/SKILL.md`
- `.claude/skills/rbac-audit/SKILL.md`
- `.claude/skills/input-validation-audit/SKILL.md`
- `.claude/skills/security-misconfig-audit/SKILL.md`
- `.claude/skills/logging-monitoring-audit/SKILL.md`
- `.claude/skills/dependency-audit/SKILL.md`
- `.claude/skills/report-writer/SKILL.md`

Use these templates where helpful:

- `.claude/templates/audit-session-template.md`
- `.claude/templates/findings-register-template.md`
- `.claude/templates/acceptance-criteria-checklist.md`

Review available evidence from:

- `evidence/raw/`
- `evidence/reviewed/`
- `evidence/summarized/`

Review active audit content from:

- `audits/active/`
- `audit-runs/active/`

---

## Scope of Review

This command should perform a broad, non-destructive website audit review across the following areas where evidence is available:

- security headers and transport security
- authentication entry points and controls
- session handling indicators
- role and access control indicators
- direct object reference / ownership concerns if visible
- input validation indicators
- security misconfiguration indicators
- logging and auditability visibility
- dependency/component risk if evidence exists

Do not force findings in areas where no evidence exists.

---

## Required Audit Method

Follow this sequence strictly.

### Step 1 — Read context
Read all files under `.claude/context/`.

Determine:
- target URL
- audit objective
- scope limits
- prohibited activities
- evidence availability
- current assumptions
- current review constraints

### Step 2 — Establish audit posture
State the audit posture based on context:
- non-destructive
- evidence-driven
- limited-scope
- public-only or mixed review
- authorized or limited authorization

If the scope is unclear, proceed conservatively and label gaps.

### Step 3 — Review current evidence inventory
Inspect:
- `evidence/raw/`
- `evidence/reviewed/`
- `evidence/summarized/`

Summarize:
- what evidence exists
- what evidence is missing
- what evidence is strong enough for confirmed findings
- what evidence only supports inference
- what areas remain review gaps

### Step 4 — Create or update active audit note
Create or update a working audit note in:

- `audits/active/`

The working note should include:
- target summary
- scope summary
- evidence reviewed
- review areas covered
- provisional findings
- confirmed findings
- review gaps
- next evidence needed

### Step 5 — Run review domains
Apply the relevant skills and review the target across these domains.

#### A. Headers and transport review
Assess where possible:
- HTTPS usage
- HSTS
- CSP
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy
- visible cookie security indicators
- transport and browser-facing controls

#### B. Authentication review
Assess where possible:
- login entry points
- password reset visibility
- MFA evidence
- lockout clues
- admin entry protection
- session handling clues

#### C. RBAC and access control review
Assess where possible:
- visible role boundaries
- object ownership indicators
- tenant separation indicators
- IDOR clues
- privilege escalation concerns visible from evidence

#### D. Input validation review
Assess where possible:
- user-input entry points
- validation indicators
- reflected input behavior
- unsafe error disclosure
- injection concern indicators visible from evidence

#### E. Security misconfiguration review
Assess where possible:
- exposed software identifiers
- default-like behavior
- weak browser-facing controls
- directory exposure clues
- unsafe config patterns visible from evidence

#### F. Logging and monitoring review
Assess where possible:
- security event visibility
- auditability clues
- actor/action/resource/outcome visibility
- reviewability of key events
- lack of evidence as visibility gap if applicable

#### G. Dependency/component review
Only if evidence exists:
- scanner output
- package files
- lock files
- component inventory
- known version exposure indicators

### Step 6 — Normalize findings
Every meaningful result must be categorized as one of:
- confirmed finding
- suspected issue
- review-gap
- mitigated
- accepted-risk

Each finding should include:
- title
- domain
- severity
- confidence
- evidence
- observation
- risk
- recommendation
- acceptance criteria mapping
- status
- review type

### Step 7 — Update findings register
Create or update the findings register using the workspace template.

The findings register should reflect:
- normalized findings only
- no unsupported statements
- no duplicate findings
- clear differentiation between confirmed findings and review gaps

### Step 8 — Update acceptance criteria view
Where relevant, map findings and gaps to:
- current acceptance criteria
- visible control strengths
- visible control failures
- evidence limitations

Do not mark criteria as failed unless evidence supports it.

### Step 9 — Prepare report inputs
Prepare the workspace for final reporting by summarizing:
- overall review status
- strongest confirmed issues
- highest-priority review gaps
- evidence limitations
- immediate next actions

---

## Output Requirements

The result of this command must produce or update:

### 1. Working audit note
Stored under:
- `audits/active/`

### 2. Findings register
Based on:
- `.claude/templates/findings-register-template.md`

### 3. Acceptance criteria impact view
Based on:
- `.claude/templates/acceptance-criteria-checklist.md`

### 4. Report-ready summary
A concise summary suitable for later use by:
- `/generate-report`
- `/generate-remediation-plan`

---

## Output Style

Keep the output:
- concise
- structured
- evidence-based
- professional
- practical
- reusable

Avoid:
- generic filler
- unsupported conclusions
- exaggerated severity
- speculative vulnerability claims

---

## Guardrails

- Do not invent evidence.
- Do not assume private functionality unless evidenced.
- Do not describe intrusive testing as completed unless explicitly provided.
- Treat missing visibility as a review gap, not automatically a confirmed failure.
- If the target is public-only, limit conclusions accordingly.
- If authentication or admin areas are unavailable, document the limitation clearly.

---

## Final Deliverable Shape

At the end of this command, the workspace should contain:

- an updated active audit note
- a normalized findings register
- an acceptance criteria impact view
- a concise summary of:
  - confirmed findings
  - suspected issues
  - review gaps
  - next evidence required
  - next recommended commands

Recommended next commands after this one may include:
- `/review-headers`
- `/review-auth`
- `/review-rbac`
- `/review-logging`
- `/review-dependencies`
- `/generate-report`