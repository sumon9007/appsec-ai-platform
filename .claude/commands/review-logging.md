# Command: /review-logging

Focused review of logging and monitoring coverage. Loads the logging-monitoring-audit skill and guides through event coverage assessment, log integrity review, alerting configuration, retention policy, and PII-in-logs check.

## Trigger

Invoked when the user wants to perform a targeted review of logging and monitoring controls. Can be run standalone or as part of a broader audit workflow.

---

## Pre-Conditions

1. `.claude/context/audit-context.md` is populated and Authorization Status is **CONFIRMED**
2. Log access or log samples are available (or noted as unavailable)
3. `.claude/context/target-profile.md` identifies logging infrastructure (if known)

---

## Steps

### Step 1: Context Load

1. Read `.claude/context/audit-context.md` — confirm authorization and note if log access is available
2. Read `.claude/context/target-profile.md` — note logging infrastructure, SIEM if present
3. Read `.claude/context/assumptions.md` — note any logging-related unknowns
4. Read `.claude/rules/safety-authorization-rules.md`

### Step 2: Load Skill

Load: `.claude/skills/logging-monitoring-audit/SKILL.md`

Read:
- `.claude/skills/logging-monitoring-audit/templates/logging-checklist.md`
- `.claude/skills/logging-monitoring-audit/templates/audit-log-review-template.md`

### Step 3: Event Coverage Review

Using `logging-checklist.md`, assess whether the following events are logged:

#### Authentication Events
- Successful login — is it logged with: user ID, timestamp, IP address, user agent?
- Failed login — is failure reason logged? (Is PII like the attempted username logged?)
- Logout — is explicit logout logged?
- Password change — logged with user ID and timestamp?
- Password reset initiation and completion — logged?
- MFA enrollment and removal — logged?
- Account lockout — logged with trigger detail?

#### Authorization Events
- Access denied (401/403 responses) — logged with endpoint, user, timestamp?
- Privilege escalation attempts — logged?
- Admin action — all admin operations logged with acting user ID?

#### Data Events
- Sensitive data access (bulk export, download) — logged?
- Data modification of sensitive records — logged?
- Account creation and deletion — logged?

#### System Events
- Application errors and exceptions — logged?
- Configuration changes — logged?
- Service startup and shutdown — logged?

#### Input Anomalies
- Malformed input patterns — logged?
- Input validation failures — logged?
- Unusually large payloads — logged?

### Step 4: Log Storage and Integrity Review

- Where are logs stored? (Local filesystem, centralized SIEM, cloud logging service)
- Are logs protected against modification? (Append-only, write-once storage, log shipping to separate system)
- Is log access controlled — who can view, modify, or delete logs?
- Are logs replicated or backed up?
- What is the log retention period?
  - Recommended minimum: 90 days hot, 1 year cold (depending on compliance requirements)

### Step 5: PII and Sensitive Data in Logs

Review log samples (if available) for inadvertent sensitive data inclusion:

- Are passwords or credentials ever logged? (Even hashed passwords should not appear)
- Are full payment card numbers or bank account numbers present?
- Are authentication tokens, session IDs, or API keys logged?
- Are sensitive query parameters included in request logs?
- Are health or medical data fields present?

**IMPORTANT:** If credentials or sensitive secrets are found in logs, stop and escalate per `.claude/rules/safety-authorization-rules.md`.

### Step 6: Alerting Configuration Review

- Is there alerting on high-frequency authentication failures? (Brute force detection)
- Is there alerting on anomalous data access patterns? (e.g., bulk exports)
- Is there alerting on unauthorized access attempts?
- What is the alert delivery mechanism? (Email, PagerDuty, Slack, SIEM rule)
- Have alerting thresholds been tuned? (Not too noisy, not too silent)
- When was the last time alerts were tested?

### Step 7: Log Review (If Log Samples Available)

Using `audit-log-review-template.md`, review provided log samples:

- What event types are present?
- What gaps in coverage are evident?
- Are log entries properly structured (timestamp, user, action, result)?
- Any suspicious patterns in the sample period?
- Evidence of tamper or log gaps?

### Step 8: Document Findings

For each logging or monitoring weakness:
- Record in findings register
- Assign Finding ID and severity
- Reference evidence items

---

## Outputs

| Output | Location | Template |
|--------|----------|---------|
| Logging checklist | `audit-runs/active/` | `logging-checklist.md` |
| Log review record | `audit-runs/active/` | `audit-log-review-template.md` |
| Logging findings | Findings register | Standard finding format |
| Evidence items | `evidence/raw/` | EVID- convention |
