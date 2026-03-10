# Logging and Monitoring Controls Checklist

**Auditor:** [PLACEHOLDER]
**Date:** [PLACEHOLDER]
**Target:** [PLACEHOLDER]
**Log Access Available:** [Yes / No / Partial]

---

## Legend

| Status | Meaning |
|--------|---------|
| LOGGED | Event is logged with appropriate detail |
| PARTIAL | Event is logged but missing key fields or not all cases covered |
| NOT LOGGED | Event is not logged — finding required |
| UNKNOWN | Could not determine — document as [UNKNOWN] |
| N/A | Not applicable to this application |

---

## 1. Authentication Events

| # | Event | Status | Required Fields Present? | Notes | Finding ID |
|---|-------|--------|--------------------------|-------|------------|
| 1.1 | Successful login | [STATUS] | User ID, IP, Timestamp, User-Agent | [NOTES] | [FIND-NNN or —] |
| 1.2 | Failed login | [STATUS] | IP, Timestamp, Failure reason category (not credential) | [NOTES] | [FIND-NNN or —] |
| 1.3 | Logout | [STATUS] | User ID, Session ID, Timestamp | [NOTES] | [FIND-NNN or —] |
| 1.4 | Password change | [STATUS] | User ID, Timestamp, IP | [NOTES] | [FIND-NNN or —] |
| 1.5 | Password reset request | [STATUS] | User ID or email, Timestamp, IP | [NOTES] | [FIND-NNN or —] |
| 1.6 | Password reset completion | [STATUS] | User ID, Timestamp | [NOTES] | [FIND-NNN or —] |
| 1.7 | MFA enrollment | [STATUS] | User ID, Timestamp, MFA type | [NOTES] | [FIND-NNN or —] |
| 1.8 | MFA removal | [STATUS] | User ID, Timestamp, who initiated | [NOTES] | [FIND-NNN or —] |
| 1.9 | MFA failure | [STATUS] | User ID, Timestamp, IP | [NOTES] | [FIND-NNN or —] |
| 1.10 | Account lockout | [STATUS] | User ID, Timestamp, trigger (failed count) | [NOTES] | [FIND-NNN or —] |
| 1.11 | Account unlock | [STATUS] | User ID, Timestamp, who unlocked | [NOTES] | [FIND-NNN or —] |

---

## 2. Authorization and Access Events

| # | Event | Status | Required Fields Present? | Notes | Finding ID |
|---|-------|--------|--------------------------|-------|------------|
| 2.1 | Access denied (401/403) | [STATUS] | User ID, Endpoint, Timestamp, IP | [NOTES] | [FIND-NNN or —] |
| 2.2 | Authorization failure on API endpoint | [STATUS] | User ID, Endpoint, Method, Timestamp | [NOTES] | [FIND-NNN or —] |
| 2.3 | Admin panel access | [STATUS] | Admin User ID, Action, Timestamp | [NOTES] | [FIND-NNN or —] |
| 2.4 | User role change | [STATUS] | Target User ID, Old Role, New Role, Acting User ID, Timestamp | [NOTES] | [FIND-NNN or —] |
| 2.5 | Privilege escalation attempt | [STATUS] | User ID, Attempted action, Timestamp | [NOTES] | [FIND-NNN or —] |

---

## 3. Data Events

| # | Event | Status | Required Fields Present? | Notes | Finding ID |
|---|-------|--------|--------------------------|-------|------------|
| 3.1 | Bulk data export or download | [STATUS] | User ID, Data scope, Timestamp, IP | [NOTES] | [FIND-NNN or —] |
| 3.2 | Sensitive record access (e.g., PII, financial) | [STATUS] | User ID, Resource ID, Timestamp | [NOTES] | [FIND-NNN or —] |
| 3.3 | Data modification of critical records | [STATUS] | User ID, Resource ID, Old/New values (or change indication), Timestamp | [NOTES] | [FIND-NNN or —] |
| 3.4 | Account creation | [STATUS] | New User ID, Created by (admin or self-registration), Timestamp | [NOTES] | [FIND-NNN or —] |
| 3.5 | Account deletion | [STATUS] | Deleted User ID, Acting User ID, Timestamp | [NOTES] | [FIND-NNN or —] |
| 3.6 | File upload | [STATUS] | User ID, File name/type, Timestamp | [NOTES] | [FIND-NNN or —] |

---

## 4. System and Application Events

| # | Event | Status | Required Fields Present? | Notes | Finding ID |
|---|-------|--------|--------------------------|-------|------------|
| 4.1 | Application errors / unhandled exceptions | [STATUS] | Error type, Stack trace (internal only, not exposed to user), Timestamp | [NOTES] | [FIND-NNN or —] |
| 4.2 | Configuration changes | [STATUS] | What changed, Who changed it, Timestamp | [NOTES] | [FIND-NNN or —] |
| 4.3 | Service startup and shutdown | [STATUS] | Service name, Timestamp | [NOTES] | [FIND-NNN or —] |
| 4.4 | Integration / third-party API failures | [STATUS] | Service, Error, Timestamp | [NOTES] | [FIND-NNN or —] |
| 4.5 | Input validation failures / anomalous input | [STATUS] | Input type, Endpoint, Timestamp, IP | [NOTES] | [FIND-NNN or —] |

---

## 5. Log Storage and Integrity

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 5.1 | Logs stored in a system separate from the application | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 5.2 | Logs are append-only or write-once (tamper-resistant) | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 5.3 | Log access is restricted to authorized personnel only | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 5.4 | Log access and modification is itself logged | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 5.5 | Hot log retention: ≥ 90 days | [STATUS] | Current retention: [VALUE] | [FIND-NNN or —] |
| 5.6 | Archive log retention: meets compliance requirements | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 5.7 | Logs are backed up / replicated | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 6. PII and Sensitive Data in Logs

| # | Control | Status | Notes | Finding ID |
|---|---------|--------|-------|------------|
| 6.1 | Passwords or password hashes are NOT logged | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 6.2 | Authentication tokens / session IDs are NOT logged in plain | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 6.3 | API keys / secrets are NOT logged | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 6.4 | Full credit card numbers are NOT logged | [STATUS] | [NOTES] | [FIND-NNN or —] |
| 6.5 | Excessive PII not logged beyond operational necessity | [STATUS] | [NOTES] | [FIND-NNN or —] |

---

## 7. Alerting Configuration

| # | Alert | Configured? | Threshold | Delivery | Last Tested | Finding ID |
|---|-------|-------------|-----------|----------|-------------|------------|
| 7.1 | High-frequency login failures (brute force) | [Yes / No / Unknown] | [e.g., 10 failures/5 min] | [Email/SIEM/PagerDuty] | [DATE or Unknown] | [FIND-NNN or —] |
| 7.2 | Account lockout spike | [Yes / No / Unknown] | [THRESHOLD] | [DELIVERY] | [DATE] | [FIND-NNN or —] |
| 7.3 | Anomalous data export volume | [Yes / No / Unknown] | [THRESHOLD] | [DELIVERY] | [DATE] | [FIND-NNN or —] |
| 7.4 | Repeated authorization failures from a single user | [Yes / No / Unknown] | [THRESHOLD] | [DELIVERY] | [DATE] | [FIND-NNN or —] |
| 7.5 | Application error rate spike | [Yes / No / Unknown] | [THRESHOLD] | [DELIVERY] | [DATE] | [FIND-NNN or —] |

---

## Checklist Summary

| Section | Controls | LOGGED/PASS | NOT LOGGED/FAIL | PARTIAL | UNKNOWN |
|---------|----------|-------------|----------------|---------|---------|
| 1. Authentication Events | 11 | — | — | — | — |
| 2. Authorization Events | 5 | — | — | — | — |
| 3. Data Events | 6 | — | — | — | — |
| 4. System Events | 5 | — | — | — | — |
| 5. Log Storage & Integrity | 7 | — | — | — | — |
| 6. PII Controls | 5 | — | — | — | — |
| 7. Alerting | 5 | — | — | — | — |
| **Total** | **44** | — | — | — | — |

---

*Template: logging-checklist.md*
