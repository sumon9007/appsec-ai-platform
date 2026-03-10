# Command: /audit-weekly

Focused weekly security check covering headers, auth changes, new CVEs in dependencies, and recent log anomalies.

## Trigger

Invoked at the start of each week's security monitoring cycle. Designed to be lightweight (1–2 hours) and repeatable. Produces a weekly summary for trend tracking.

---

## Pre-Conditions

1. `.claude/context/audit-context.md` is populated and Authorization Status is **CONFIRMED**
2. `.claude/context/scope.md` is current
3. Prior week's weekly summary is available for comparison (if not the first run)

---

## Steps

### Step 1: Context Load

1. Read `.claude/context/audit-context.md` — confirm authorization
2. Read `.claude/context/scope.md` — confirm boundaries unchanged
3. Read `.claude/rules/safety-authorization-rules.md`
4. Read `.claude/rules/audit-scope-rules.md`
5. Review prior week's weekly summary from `audits/weekly/` (if available) for trend context

### Step 2: Load Relevant Skills

Load these skills for the weekly audit:

1. `.claude/skills/headers-tls-audit/SKILL.md`
2. `.claude/skills/auth-access-audit/SKILL.md`
3. `.claude/skills/dependency-audit/SKILL.md`
4. `.claude/skills/logging-monitoring-audit/SKILL.md`

### Step 3: Security Headers Check

Skill: `.claude/skills/headers-tls-audit/`
Template: `.claude/skills/headers-tls-audit/templates/headers-checklist.md`

- Check HTTP response headers for the primary application URL
- Note any regressions (headers present last week but now missing)
- Note any new headers added since last check
- Check certificate expiry — flag if < 30 days remaining
- Document any changes or new issues with EVID- references

### Step 4: Authentication Change Review

Skill: `.claude/skills/auth-access-audit/`
Template: `.claude/skills/auth-access-audit/templates/auth-checklist.md`

- Review any known changes to authentication flows in the past week
- Check login and password reset endpoints for behavioral changes
- Note any new login error messages that may enable enumeration
- Confirm MFA configuration unchanged

### Step 5: Dependency CVE Check

Skill: `.claude/skills/dependency-audit/`

- Review dependency advisories published in the past 7 days for the known tech stack
- Cross-reference against the application's known dependencies (from `.claude/context/target-profile.md`)
- Flag any newly disclosed CVE affecting a direct dependency (Critical or High)
- Document new CVEs in `.claude/skills/dependency-audit/templates/dependency-findings-template.md` if they apply

### Step 6: Log Anomaly Review

Skill: `.claude/skills/logging-monitoring-audit/`

- Review any security alerts or anomaly reports from the past 7 days (if log access is available)
- Note patterns: unusual login failure spikes, unexpected 403/401 patterns, large data exports
- Document any anomalies observed
- If log access is not available, note as `[UNKNOWN — log review not performed this week]`

### Step 7: Findings Update

1. Review the current findings register
2. Update any findings whose status has changed this week
3. Add any new findings discovered during the weekly checks
4. Note which previously open findings are past their SLA deadline

### Step 8: Produce Weekly Summary

1. Complete `.claude/templates/weekly-summary-template.md`
2. Save to `audits/weekly/YYYY-MM-DD-weekly.md`
3. Note overall risk trend vs. prior week: Improving / Stable / Degrading

---

## Outputs

| Output | Location | Template |
|--------|----------|---------|
| Weekly summary | `audits/weekly/YYYY-MM-DD-weekly.md` | `weekly-summary-template.md` |
| Updated findings register | Current findings register | `findings-register-template.md` |
| New evidence items | `evidence/raw/` | EVID- convention |

---

## Escalation

If any of the following are discovered during a weekly check, escalate immediately:

- New Critical CVE affecting a direct dependency
- Authentication bypass or regression observed
- Certificate expiry within 7 days
- Anomalous log pattern suggesting active attack or breach
