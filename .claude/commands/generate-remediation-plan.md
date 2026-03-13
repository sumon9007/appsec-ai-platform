> **Python CLI** (primary): `python scripts/run_audit.py report remediation`
> This command file is a methodology reference. Run the Python CLI command above for automated execution.

# Command: /generate-remediation-plan

## Objective

Generate a prioritized remediation plan for the current target based on confirmed findings, supported suspected issues, and clearly identified review gaps.

This command should convert audit results into practical actions for engineering and security stakeholders.

The remediation plan must be:
- evidence-based
- prioritized
- realistic
- concise
- suitable for execution planning

---

## Required Inputs

Read context first:

- `.claude/context/audit-context.md`
- `.claude/context/target-profile.md`
- `.claude/context/scope.md`
- `.claude/context/assumptions.md`

Read rules:

- `.claude/rules/evidence-quality-rules.md`
- `.claude/rules/severity-rating-rules.md`
- `.claude/rules/remediation-rules.md`
- `.claude/rules/reporting-rules.md`

Use skill:

- `.claude/skills/report-writer/SKILL.md`

Read current audit state from:

- `audits/active/`
- `audit-runs/active/`
- `reports/draft/`
- `evidence/reviewed/`
- `evidence/summarized/`

Read supporting templates:

- `.claude/templates/findings-register-template.md`
- `.claude/templates/acceptance-criteria-checklist.md`

Write output to:

- `reports/draft/`

---

## Remediation Plan Purpose

The remediation plan should answer:

- what needs to be fixed first
- what can be improved next
- what needs further validation before action
- what longer-term control improvements are recommended

It should help teams move from findings to action.

---

## Required Remediation Structure

The remediation plan should include:

### 1. Title
Use a clear title such as:
- Security Remediation Plan – [Application Name]
- Website Audit Remediation Plan – [Target Name]

### 2. Overview
Provide a short overview covering:
- what the plan is based on
- scope of the plan
- limitations of current evidence
- how priorities were determined

### 3. Prioritization Logic
State that prioritization is based on:
- severity
- exploitability
- business impact
- exposure
- confidence in evidence
- dependency on further validation

### 4. Immediate Actions
Include the highest-priority actions that should be addressed first.

These typically map to:
- Critical findings
- High findings
- highly exposed weaknesses
- core browser-facing control failures
- urgent validation tasks

### 5. Short-Term Improvements
Include meaningful improvements that should be planned soon but are not immediate emergency items.

These may include:
- Medium findings
- control hardening
- visibility improvements
- policy improvements
- strengthening defenses around observed weaknesses

### 6. Strategic Improvements
Include longer-term actions such as:
- architecture improvements
- process improvements
- broader control maturity
- recurring review improvements
- logging and evidence maturity

### 7. Validation Tasks
Include specific tasks required to validate:
- review gaps
- suspected issues
- inaccessible control areas
- assumptions that materially affect risk

### 8. Ownership Suggestions
Where useful, suggest likely ownership categories such as:
- application engineering
- platform team
- security team
- operations team
- architecture / governance

Do not invent named people unless provided in context.

### 9. Recommended Sequence
Provide a practical order of execution:
- first
- next
- after validation
- strategic follow-up

### 10. Conclusion
Close with a short summary of the most important next steps.

---

## Audit Method

### Step 1 — Read Current Audit Results
Review:
- findings register
- draft report if present
- acceptance criteria impact
- working audit notes
- reviewed evidence summaries

Separate:
- confirmed findings
- suspected issues
- review gaps

---

### Step 2 — Filter for Actionable Items
Use only items that justify planning action.

Confirmed findings should drive direct remediation items.

Suspected issues should either:
- become conditional remediation items
- or become validation tasks

Review gaps should become:
- evidence collection tasks
- validation tasks
- visibility improvement tasks

---

### Step 3 — Prioritize
Prioritize based on:
- severity
- exploitability
- exposure
- business impact
- confidence
- control dependency

Do not prioritize only by count.

---

### Step 4 — Write Immediate Actions
Create a concise list of actions that should happen first.

For each item include:
- issue summary
- why it matters
- recommended action
- likely owner category
- urgency

---

### Step 5 — Write Short-Term Improvements
Create practical hardening and improvement actions.

These should help reduce medium-risk weaknesses and improve resilience.

---

### Step 6 — Write Strategic Improvements
Capture longer-horizon recommendations that improve control maturity.

Examples may include:
- better evidence collection
- stronger secure design patterns
- improved recurring review workflows
- improved logging or dependency governance

Keep recommendations grounded in the current audit.

---

### Step 7 — Write Validation Tasks
For review gaps and suspected issues, define:
- what must be checked
- why it matters
- what evidence is needed
- what team should help validate

This section is important and should not be skipped.

---

### Step 8 — Write Remediation File
Write the remediation plan to:

- `reports/draft/`

Use a clear file name such as:
- `reports/draft/security-remediation-plan.md`

---

## Output Requirements

The remediation plan must be:
- practical
- prioritized
- concise
- evidence-based
- suitable for engineering follow-up
- suitable for stakeholder review

---

## Guardrails

- Do not recommend actions for unsupported findings as if they are confirmed.
- Do not invent owners by person name.
- Do not create vague recommendations like "improve security" without specific action.
- Do not ignore validation tasks for review gaps.
- Do not over-prioritize low-confidence issues without explanation.

---

## Final Deliverable

The result of this command should be:

1. A draft remediation plan under `reports/draft/`
2. A concise summary of:
   - highest-priority immediate actions
   - most important validation tasks
   - strategic improvements worth planning
