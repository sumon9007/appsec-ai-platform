> This skill provides the methodology intelligence for release gate reviews.
> For the orchestration command reference, see: `.claude/commands/audit-release.md`

# Skill: Release Gate Review

## Purpose

Perform a structured pre-release security review. Determines whether a release is safe to deploy by assessing new attack surface introduced by the release, verifying prior finding remediation, checking for security control regressions, and issuing a formal gate decision.

Use this skill:
- Before every production release
- When a release includes security-relevant changes (new features, auth changes, dependency updates, infrastructure changes)
- When the release touches domains that have open findings

Do NOT use this skill for recurring cadence reviews — use `audit-cadence-orchestrator` instead.

---

## Inputs Required

| Input | Source | Required? |
|-------|--------|-----------|
| Release changelog or diff summary | Development team | Required |
| New dependencies introduced | Development team | Required |
| Release version number | Development team | Required |
| Current findings register | `audits/[engagement-id]/findings-register.md` | Required |
| Acceptance criteria | `.claude/docs/acceptance-criteria.md` | Required |
| Audit context | `.claude/context/audit-context.md` | Required |
| PRD or feature specs (if available) | Development team or `docs/` | Recommended |

---

## Method

### Phase 1: Pre-Gate Setup

1. Read `.claude/context/audit-context.md` — confirm authorization is CONFIRMED
2. Read `.claude/docs/acceptance-criteria.md` — internalize pass/fail criteria before reviewing
3. Read `.claude/rules/remediation-rules.md` — internalize SLA rules and blocker conditions
4. Read `.claude/rules/severity-rating-rules.md` — note automatic escalation rules (regressions escalate one level)
5. Open the current findings register — note all open Critical and High findings and their SLA status
6. Create a session record at `audit-runs/active/YYYY-MM-DD-v[VERSION]-release-session.md`

### Phase 2: Release Scope Analysis

Analyze the release changelog. Build a scope map using `templates/release-scope-analysis.md`:

| Change | Type | Security Risk | Domains Affected |
|--------|------|--------------|-----------------|
| [Change description] | New feature / Bug fix / Dependency / Config | High / Medium / Low / None | [domains] |

Flag any changes that:
- Accept new user input without described validation → `input-validation-audit`
- Introduce new file handling (upload, rendering) → `input-validation-audit`
- Add new API endpoints without described authentication → `auth-access-audit`, `rbac-audit`
- Modify existing authorization logic or role definitions → `rbac-audit`
- Add new third-party integrations → `security-misconfig-audit`, `dependency-audit`
- Change session handling, token issuance, or JWT configuration → `session-jwt-audit`
- Modify security headers, CORS, or CSP configuration → `headers-tls-audit`
- Add or update packages → `dependency-audit`
- Modify infrastructure, cloud config, or deployment scripts → `security-misconfig-audit`

### Phase 3: Domain-Selective Security Review

Load only the domain skills relevant to what changed in this release.

**Always load for any release:**
- `headers-tls-audit` — verify header configuration has not regressed
- `auth-access-audit` — verify authentication controls are unchanged (or review intentional changes)

**Load conditionally based on Phase 2 scope map:**
- `input-validation-audit` — if new inputs or file handling introduced
- `rbac-audit` — if new endpoints, role changes, or authorization logic modified
- `session-jwt-audit` — if session or token handling changed
- `dependency-audit` — if new or updated packages present
- `security-misconfig-audit` — if infrastructure or configuration changed

For each loaded skill, focus only on the changed surface area. Run the full skill checklist only if the release broadly affects that domain.

Record all findings and evidence using the `evidence-and-findings-ops` skill.

### Phase 4: New Feature Security Review

For each new feature in the release that has a PRD or description:

Apply `.claude/docs/prd-analysis.md` steps:
- What new attack surface does this feature introduce?
- What data flows are created or modified?
- What trust boundaries are crossed?
- Are there implicit security requirements not described in the spec?

Document security concerns as:
- `confirmed` findings: if evidence from the live release demonstrates the issue
- `suspected` findings: if inferred from feature description without live evidence — label confidence clearly
- `review-gap`: if the feature cannot be adequately assessed from available information

If the release includes a new PRD, run `prd-security-review` skill as a sub-step.

### Phase 5: Prior Findings Remediation Gate Check

Review all open Critical and High findings in the findings register:

For each open finding:
- **Fixed in this release?** → Request fix evidence. Verify. Update findings register via `evidence-and-findings-ops`
- **Has accepted risk exception with valid expiry?** → Confirm per `.claude/rules/remediation-rules.md` Rule 4 (must be signed, within expiry)
- **Past SLA with no exception?** → Flag as gate blocker

Automatic gate blockers:
- Any open Critical finding with no resolution and no accepted risk on file
- Any Must-Fix item identified during this review that is unresolved

### Phase 6: Security Controls Regression Check

Verify known-good controls have not been accidentally removed or degraded:
- Security headers still present and correctly configured (headers-tls-audit)
- Authentication controls unchanged (unless part of this release)
- Session management controls unchanged (unless part of this release)
- Rate limiting still active on key endpoints
- Previously passing checklist items from last audit still pass

Any regression is a new finding. Per `.claude/rules/severity-rating-rules.md` escalation rules: regressions escalate severity one level above the original finding's severity.

### Phase 7: Gate Decision

**Pass** — all of the following are true:
- Zero open Critical findings (no exceptions)
- Zero open High findings without accepted risk on file
- No Must-Fix items from this release review
- No security control regressions

**Conditional Pass** — all of the following are true:
- No Critical findings
- High findings have documented, signed risk acceptances with remediation deadlines
- Medium findings tracked and documented
- All conditions for the conditional pass explicitly listed in the gate document

**Fail** — any of the following are true:
- Any Critical finding open without resolution or accepted risk
- Any Must-Fix item from this review unresolved
- Evidence of active exploitation of a known finding
- Security control regression that introduces a new Critical or High finding

### Phase 8: Gate Document

1. Complete `.claude/templates/release-gate-template.md`
2. Save to `audits/release/YYYY-MM-DD-v[VERSION]-gate.md`
3. State gate decision clearly: **PASS / CONDITIONAL PASS / FAIL**
4. If Conditional Pass: list all conditions explicitly
5. Update findings register with any new findings or status changes

**Gate sign-off required from:** Security lead + Development manager. Product owner required for Fail decisions.

---

## Outputs

| Output | Template | Location |
|--------|---------|---------|
| Release gate document | `release-gate-template.md` | `audits/release/YYYY-MM-DD-v[VERSION]-gate.md` |
| Release scope analysis | `release-scope-analysis.md` | Within session record |
| New findings | `findings-register-template.md` | `audits/[engagement-id]/findings-register.md` |
| New evidence | EVID- convention | `evidence/raw/` |

---

## Templates Used

- `.claude/skills/release-gate-review/templates/release-scope-analysis.md`
- `.claude/templates/release-gate-template.md`
- `.claude/templates/findings-register-template.md`
- `.claude/docs/acceptance-criteria.md`

---

## Rules Applied

- `.claude/rules/safety-authorization-rules.md` — Rule 1 (authorization gate)
- `.claude/rules/remediation-rules.md` — Rules 1, 2, 4, 5, 6
- `.claude/rules/severity-rating-rules.md` — automatic escalation for regressions
- `.claude/rules/audit-scope-rules.md` — Rules 1, 2

---

## Related Skills and Commands

- `/audit-release` — `.claude/commands/audit-release.md` (orchestration command reference)
- `prd-security-review` — run for new features in the release that have PRDs
- `evidence-and-findings-ops` — use to record and store all findings from this review
- `engagement-bootstrap` — run before the first release gate session for an engagement
- All domain skills — selectively invoked based on the release scope analysis in Phase 2
