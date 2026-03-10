# Command: /audit-release

Pre-release security gate check. Reviews new features for security impact, checks for new attack surface, and confirms prior findings are remediated before deployment.

## Trigger

Invoked before any production release. Must be completed and produce a Pass or Conditional Pass before deployment proceeds. A Fail result blocks the release.

---

## Pre-Conditions

1. `.claude/context/audit-context.md` is populated and Authorization Status is **CONFIRMED**
2. Release version number and changelog are provided
3. Current findings register is available
4. Any new dependencies added in this release are identified

---

## Steps

### Step 1: Context Load

1. Read `.claude/context/audit-context.md` — confirm release version and authorization
2. Read `.claude/context/scope.md` — confirm scope unchanged
3. Read `.claude/docs/acceptance-criteria.md` — internalize pass/fail criteria
4. Read `.claude/rules/severity-rating-rules.md` and `.claude/rules/remediation-rules.md`
5. Review the current findings register — note all open Critical and High findings
6. Create audit session record: `audit-runs/active/YYYY-MM-DD-v[VERSION]-release-session.md`

### Step 2: Load Relevant Skills

Load skills relevant to the features changed in this release:

- Always load: `.claude/skills/auth-access-audit/SKILL.md`, `.claude/skills/headers-tls-audit/SKILL.md`
- If new data flows or inputs: `.claude/skills/input-validation-audit/SKILL.md`
- If RBAC or role changes: `.claude/skills/rbac-audit/SKILL.md`
- If new packages added: `.claude/skills/dependency-audit/SKILL.md`
- If infrastructure changes: `.claude/skills/security-misconfig-audit/SKILL.md`

### Step 3: New Feature Security Review

For each new feature or significant change in this release:

1. Review the feature description (from changelog or PRD)
2. Apply PRD security analysis framework (`.claude/docs/prd-analysis.md`):
   - What new attack surface is introduced?
   - What data flows are created or modified?
   - What trust boundaries are crossed?
3. Document security concerns per feature using the relevant skill templates
4. Assign preliminary severity to any concerns found

**Note any features that:**
- Accept new user input without described validation
- Introduce new file handling
- Add new API endpoints without described authentication
- Modify existing authorization logic
- Add new third-party integrations
- Change session or token handling

### Step 4: New Attack Surface Check

- List all new endpoints, parameters, and features introduced in this release
- For each: confirm authentication and authorization controls are described and appear implemented
- Check new dependencies introduced in the release for known CVEs (`.claude/skills/dependency-audit/`)
- If infrastructure changes: re-check headers and TLS configuration (`.claude/skills/headers-tls-audit/`)

### Step 5: Prior Findings Remediation Status

1. Review all open Critical and High findings in the findings register
2. For each: confirm fix status with the development team
3. Request evidence of fix for any findings marked as remediated in this release
4. Document evidence references for verified fixes
5. Any Critical finding that is not remediated and has no accepted risk exception = automatic Fail

### Step 6: Security Controls Regression Check

Verify that known-good controls have not been accidentally removed or degraded:

- Security headers still present and correctly configured
- Authentication controls unchanged (unless intentionally modified as part of this release)
- Session management controls unchanged
- Rate limiting still active on key endpoints
- Known-passing checklist items from last audit still pass

### Step 7: Gate Decision

Based on the review:

**Pass:** All of the following are true:
- Zero open Critical findings (no exceptions)
- Zero open High findings with no risk acceptance on file
- No Must-Fix items identified during this release review
- No security control regressions

**Conditional Pass:** All of the following are true:
- No Critical findings
- High findings have a documented risk acceptance with a remediation deadline
- Medium findings are documented and tracked
- Any conditions for the conditional pass are explicitly stated in the gate document

**Fail:** Any of the following are true:
- Any Critical finding open without resolution
- Any Must-Fix item from this release review unresolved
- Active exploitation of a known finding detected

### Step 8: Produce Release Gate Document

1. Complete `.claude/templates/release-gate-template.md`
2. Save to `audits/release/YYYY-MM-DD-v[VERSION]-gate.md`
3. Record gate decision clearly: **PASS / CONDITIONAL PASS / FAIL**
4. If Conditional Pass: list all conditions that must be met post-release
5. Update findings register with any new findings

---

## Outputs

| Output | Location | Template |
|--------|----------|---------|
| Release gate document | `audits/release/YYYY-MM-DD-v[VERSION]-gate.md` | `release-gate-template.md` |
| Updated findings register | Current register | `findings-register-template.md` |
| New evidence items | `evidence/raw/` | EVID- convention |

---

## Gate Decision Authority

The gate decision must be reviewed and signed off by:

- Security lead
- Development manager
- Product owner (for Fail decisions)

A Fail decision means the release does not proceed until issues are resolved and the gate is re-run.
