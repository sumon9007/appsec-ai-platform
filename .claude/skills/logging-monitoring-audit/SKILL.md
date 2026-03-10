# Skill: Logging and Monitoring Audit

## Purpose

Assess the application's logging and monitoring implementation to determine whether security-relevant events are captured, log data is protected and retained appropriately, PII is not inadvertently exposed in logs, and alerting is configured to detect anomalous activity.

---

## Inputs Required

| Input | Source | Required? |
|-------|--------|-----------|
| Target application description | `.claude/context/target-profile.md` | Required |
| Log access or log samples | Provided by client | Strongly recommended |
| Logging infrastructure details | `.claude/context/target-profile.md` | If known |
| Authorization confirmation | `.claude/context/audit-context.md` | Required |

If log access is not available:
- Document as `[UNKNOWN]`
- Assess logging based on observable application behavior and client-provided information
- Note limitations in findings

---

## Method

### Phase 1: Logging Architecture Review

1. Identify the logging infrastructure:
   - Where are logs stored? (Local files, centralized log management, cloud logging, SIEM)
   - What services produce logs? (Application server, web server, database, authentication service)
   - Are logs aggregated in a single location?
   - Who has access to read logs?
   - Who has access to delete or modify logs?

2. Identify the logging framework:
   - Application-level logging framework (e.g., Winston, Logback, Python logging, Serilog)
   - Log format (JSON structured logs vs. unstructured text)
   - Log levels in use (DEBUG, INFO, WARN, ERROR)

### Phase 2: Event Coverage Assessment

Using `logging-checklist.md`, assess whether each security-relevant event type is logged.

3. Authentication events:
   - Successful login
   - Failed login (with reason category — not the specific attempted credential)
   - Logout
   - Password change
   - Password reset request and completion
   - MFA enrollment, removal, and failure
   - Account lockout

4. Authorization events:
   - Access denied (401/403 responses) — logged with user ID, endpoint, timestamp
   - Authorization bypass attempts
   - Admin actions — all operations with acting user identity

5. Data events:
   - Bulk data access or export
   - Sensitive data access
   - Data modification of critical records
   - Account creation and deletion

6. System events:
   - Application errors and unhandled exceptions
   - Configuration changes
   - Service startup and shutdown
   - Integration failures

### Phase 3: Log Quality Assessment

7. For each event type identified as being logged, assess log record quality:
   - **Who:** Is the user identifier (user ID, session ID) always present?
   - **What:** Is the action/event type clearly recorded?
   - **When:** Is there an accurate timestamp with timezone?
   - **Where:** Is the source IP address recorded?
   - **Result:** Is the outcome (success/failure) recorded?
   - **Context:** Is relevant context included (e.g., affected resource ID)?

### Phase 4: PII and Sensitive Data Review

8. If log samples are available, review for inadvertent sensitive data:
   - Passwords or password hashes
   - Authentication tokens, session IDs, API keys
   - Credit card numbers, bank accounts
   - PII (full names, emails, phone numbers, addresses) beyond what is operationally necessary
   - Health or medical data
   - Private encryption keys or certificates

**IMPORTANT:** If credentials or secrets are found in logs, stop and escalate per `.claude/rules/safety-authorization-rules.md`.

### Phase 5: Log Integrity and Retention

9. Integrity controls:
   - Are logs stored in a write-once or append-only system?
   - Are logs shipped to a separate, isolated system (separate from the application server)?
   - Are log access and modification events themselves logged?
   - Is there evidence of tamper detection?

10. Retention:
    - What is the hot retention period? (Logs immediately accessible)
    - What is the cold/archive retention period?
    - Does retention meet compliance obligations? (Common requirements: 90 days–1 year hot, 1–7 years archive)

### Phase 6: Alerting and Monitoring

11. Review alerting configuration:
    - Is there alerting on high-frequency authentication failures? (Brute force detection)
    - Is there alerting on account lockout events?
    - Is there alerting on anomalous data access? (Unusual volume or off-hours access)
    - Is there alerting on authorization failures from a single user?
    - Is there alerting on application errors above a threshold?
    - What is the alert delivery mechanism and response team?
    - When were alerting thresholds last reviewed/tested?

---

## Outputs

| Output | Template | Description |
|--------|---------|-------------|
| Logging checklist | `logging-checklist.md` | Coverage assessment |
| Log review record | `audit-log-review-template.md` | Findings from log sample review |
| Logging findings | Standard finding format | One record per identified gap |
| Evidence items | EVID- convention | Log extracts, configuration screenshots |

---

## Templates Used

- `.claude/skills/logging-monitoring-audit/templates/logging-checklist.md`
- `.claude/skills/logging-monitoring-audit/templates/audit-log-review-template.md`

---

## References

- [OWASP A09:2021 — Security Logging and Monitoring Failures](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [CWE-778 — Insufficient Logging](https://cwe.mitre.org/data/definitions/778.html)
- [CWE-532 — Insertion of Sensitive Information into Log File](https://cwe.mitre.org/data/definitions/532.html)
- [NIST SP 800-92 — Guide to Computer Security Log Management](https://csrc.nist.gov/publications/detail/sp/800-92/final)
