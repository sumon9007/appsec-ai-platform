# Audit Log Review Template

Documents findings from reviewing a sample of audit log data from the application.

**Auditor:** [PLACEHOLDER]
**Date:** [PLACEHOLDER]
**Target:** [PLACEHOLDER]
**Log Sample Period:** [PLACEHOLDER — e.g., 2026-02-01 to 2026-03-01]
**Log Source:** [PLACEHOLDER — e.g., Centralized SIEM, AWS CloudWatch, Application log files]
**Volume Reviewed:** [PLACEHOLDER — e.g., ~5,000 log entries, last 30 days]

---

## Log Sample Acquisition

| Field | Value |
|-------|-------|
| How was the sample obtained? | [PLACEHOLDER — e.g., Exported from SIEM, provided as CSV, direct log access] |
| Sample size | [PLACEHOLDER — number of entries] |
| Date range | [PLACEHOLDER] |
| Log format | [PLACEHOLDER — JSON / CSV / Plain text / Syslog] |
| Evidence reference | [EVID-YYYY-MM-DD-NNN — log sample] |

---

## Event Types Observed

Record which event types are present in the log sample:

| Event Category | Event Types Found | Coverage Assessment |
|---------------|------------------|---------------------|
| Authentication | [PLACEHOLDER — e.g., login_success, login_failure, logout] | [Complete / Partial / Missing] |
| Authorization | [PLACEHOLDER — e.g., access_denied] | [Complete / Partial / Missing] |
| Data access | [PLACEHOLDER — e.g., record_viewed, export_initiated] | [Complete / Partial / Missing] |
| Admin actions | [PLACEHOLDER — e.g., user_created, role_changed] | [Complete / Partial / Missing] |
| System events | [PLACEHOLDER — e.g., app_error, service_restart] | [Complete / Partial / Missing] |
| Input anomalies | [PLACEHOLDER — e.g., validation_error] | [Complete / Partial / Missing] |

---

## Coverage Gaps Identified

Events that should be present based on application functionality but are absent from the log sample:

| Expected Event | Reason It Should Be Present | Gap Severity | Finding ID |
|---------------|----------------------------|-------------|------------|
| [PLACEHOLDER — e.g., MFA failure] | [e.g., Application uses TOTP MFA] | [High/Medium/Low] | [FIND-NNN or —] |
| [PLACEHOLDER — e.g., Password reset completion] | [e.g., Reset flow observed in application] | [Medium] | [FIND-NNN or —] |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [FIND-NNN or —] |

---

## Log Record Quality Assessment

Assess the quality of logged events:

| Field | Present in Records? | Notes |
|-------|-------------------|-------|
| User identifier (user ID or session ID) | [Always / Sometimes / Never / N/A] | [NOTES] |
| Timestamp | [Always / Sometimes / Never] | Timezone: [UTC / Local / Missing] |
| Source IP address | [Always / Sometimes / Never] | [NOTES] |
| Action / event type | [Always / Sometimes / Never] | [NOTES] |
| Outcome (success/failure) | [Always / Sometimes / Never] | [NOTES] |
| Affected resource ID | [Always / Sometimes / Never / N/A] | [NOTES] |
| Structured format (machine-parseable) | [Yes / No / Mixed] | Format: [JSON / Text] |

**Overall Log Quality:** [Good / Adequate / Poor]

---

## PII and Sensitive Data Check

Review the log sample for inadvertent sensitive data inclusion:

| Data Type | Found in Logs? | Example (redacted) | Severity | Finding ID |
|-----------|---------------|-------------------|----------|------------|
| Passwords (plaintext or hash) | [Yes / No] | [REDACTED if found] | [Critical if found] | [FIND-NNN or —] |
| Authentication tokens / session IDs | [Yes / No] | [REDACTED if found] | [High if found] | [FIND-NNN or —] |
| API keys or secrets | [Yes / No] | [REDACTED if found] | [Critical if found] | [FIND-NNN or —] |
| Credit card numbers | [Yes / No] | [REDACTED if found] | [Critical if found] | [FIND-NNN or —] |
| Full names / email addresses | [Yes / No] | [REDACTED if found] | [Medium — assess necessity] | [FIND-NNN or —] |
| Excessive PII beyond operational need | [Yes / No] | [REDACTED if found] | [Medium] | [FIND-NNN or —] |

**IMPORTANT:** If credentials, tokens, or keys are found in logs, follow `.claude/rules/safety-authorization-rules.md` — escalate immediately.

---

## Tamper and Integrity Evidence

| Check | Status | Notes |
|-------|--------|-------|
| Log records appear continuous (no obvious gaps) | [Yes / No — note suspicious gaps] | [NOTES] |
| Timestamps are sequential and consistent | [Yes / No] | [NOTES] |
| No evidence of log entries being deleted or overwritten | [Yes / No / Unknown] | [NOTES] |
| Log source system appears isolated from application | [Yes / No / Unknown] | [NOTES] |

---

## Alerting Configuration Notes

Based on the log sample, assess alerting effectiveness:

| Alert Scenario | Alerting Apparent? | Notes |
|---------------|-------------------|-------|
| Brute force / repeated login failures | [Yes / No / Unknown] | [NOTES] |
| Account lockout events | [Yes / No / Unknown] | [NOTES] |
| Anomalous access patterns | [Yes / No / Unknown] | [NOTES] |
| Off-hours admin activity | [Yes / No / Unknown] | [NOTES] |

---

## Suspicious Patterns Observed

Note any anomalous patterns observed in the log sample during the review period:

| Pattern | Description | Period Observed | Action Taken |
|---------|-------------|----------------|-------------|
| [PLACEHOLDER — e.g., High login failure rate] | [PLACEHOLDER] | [DATE RANGE] | [e.g., Flagged for investigation / No action — assessed as expected traffic] |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

---

## Summary of Findings from Log Review

| Finding ID | Title | Severity | Type |
|------------|-------|----------|------|
| [FIND-NNN or —] | [PLACEHOLDER] | [SEVERITY] | [Coverage gap / PII exposure / Integrity concern / Alert gap] |

---

## Overall Assessment

**Log Coverage:** [Comprehensive / Adequate / Insufficient]
**Log Quality:** [Good / Adequate / Poor]
**PII Controls:** [Clean / Issues found]
**Integrity Controls:** [Strong / Adequate / Weak / Unknown]
**Alerting:** [Configured / Partial / Not configured / Unknown]

**Key Recommendations:**
1. [PLACEHOLDER]
2. [PLACEHOLDER]
3. [PLACEHOLDER]

---

*Template: audit-log-review-template.md*
