# Evidence Standard

Defines how evidence must be collected, labeled, stored, and referenced within this audit workspace.

---

## Core Principle

**No finding may be recorded without at least one referenced evidence item.** Evidence is the foundation of credible, defensible security findings. Unsupported observations must be labeled `[UNKNOWN]` or held as `[ASSUMED]` until evidence is obtained.

---

## Evidence Types

| Type | Description | Examples |
|------|-------------|---------|
| Screenshot | Visual capture of a browser, tool, or terminal output | Browser showing missing security header, error message exposing stack trace |
| HTTP Request/Response | Raw or captured HTTP traffic showing the request and response | Burp Suite capture, curl output, browser DevTools network tab |
| Tool Output | Output from a scanning or analysis tool | npm audit output, SSL Labs report, OWASP ZAP scan result |
| Manual Observation Note | Structured written account of an observed behavior | Documented step-by-step reproduction of a finding |
| Configuration Extract | A specific configuration value or setting observed | Nginx config snippet, cookie attribute inspection |
| Log Extract | A sample of log data relevant to a finding | Absence of expected log entry, presence of PII in log |
| Code Reference | Reference to a specific code pattern where source is available | Identified unsanitized SQL query location |

---

## Evidence Labeling Convention

All evidence items must be labeled using the following format:

```
EVID-YYYY-MM-DD-NNN
```

Where:
- `YYYY-MM-DD` is the date the evidence was collected
- `NNN` is a sequential three-digit number, resetting each day

**Examples:**
- `EVID-2026-03-11-001` — First evidence item collected on March 11, 2026
- `EVID-2026-03-11-002` — Second evidence item collected the same day
- `EVID-2026-03-15-001` — First item collected on March 15, 2026

Labels must be consistent — use the same label in the evidence file, in the finding record that references it, and in the evidence register.

---

## Evidence Storage Locations

| Stage | Location | Description |
|-------|----------|-------------|
| Raw | `evidence/raw/` | Unprocessed evidence as captured. May contain sensitive data — handle appropriately. |
| Reviewed | `evidence/reviewed/` | Evidence that has been verified, annotated, and confirmed as relevant to a finding. |
| Summarized | `evidence/summarized/` | Sanitized or summarized evidence suitable for inclusion in reports. Remove credentials, PII, and system-sensitive details before promoting to this stage. |

### File Naming

Evidence files should be named:

```
EVID-YYYY-MM-DD-NNN-[brief-description].md
```

Example: `EVID-2026-03-11-001-missing-hsts-header.md`

---

## Evidence File Format

Each evidence file should include:

```
# Evidence: EVID-YYYY-MM-DD-NNN

**Label:** EVID-YYYY-MM-DD-NNN
**Date Collected:** YYYY-MM-DD
**Collector:** [Auditor name]
**Type:** [Screenshot / HTTP Capture / Tool Output / Manual Observation / Configuration Extract / Log Extract / Code Reference]
**Domain:** [Audit domain this evidence relates to]
**Related Finding:** [Finding ID, or PENDING if not yet assigned]

---

## Description

[Plain language description of what this evidence shows and why it is relevant.]

---

## Evidence Content

[Paste the evidence content here: HTTP request/response, tool output, configuration value, etc.]

[For screenshots: describe what the screenshot shows in detail, as the image may not be visible in all contexts.]

---

## Observations

[What does this evidence demonstrate? What security implication does it have?]

---

## Chain of Custody Notes

[If relevant: Note any handling steps taken to preserve integrity of the evidence.]
```

---

## Evidence Quality Requirements

Evidence must meet these standards to be referenced in a finding:

| Requirement | Detail |
|-------------|--------|
| Reproducible | The evidence must demonstrate a reproducible condition, not a one-time anomaly (unless the anomaly itself is the finding) |
| Dated | The evidence must have a clear collection date |
| Attributed | The evidence must identify the auditor who collected it |
| Specific | The evidence must relate to a specific endpoint, configuration, or behavior |
| Authentic | Evidence must not be altered, fabricated, or misleadingly cropped |

---

## Sensitive Data in Evidence

**IMPORTANT:** Evidence frequently contains sensitive data. Handle appropriately:

- Do not store production credentials in evidence files
- Redact or mask PII before promoting evidence to `evidence/summarized/`
- Do not include evidence files containing sensitive data in reports shared externally without redaction review
- If evidence unexpectedly contains passwords, tokens, or private keys: stop, document the discovery, and escalate per `.claude/rules/safety-authorization-rules.md`

---

## Evidence Register

Maintain a running log of all collected evidence for the engagement:

| Evidence ID | Date | Type | Domain | Finding ID | Storage Location | Notes |
|-------------|------|------|--------|------------|-----------------|-------|
| EVID-YYYY-MM-DD-001 | [DATE] | [TYPE] | [DOMAIN] | [FINDING-ID] | [PATH] | [NOTES] |
| EVID-YYYY-MM-DD-002 | [DATE] | [TYPE] | [DOMAIN] | [FINDING-ID] | [PATH] | [NOTES] |

---

## Referencing Evidence in Findings

When recording a finding, reference evidence using the label:

```
**Evidence:** EVID-2026-03-11-001 (Missing HSTS header — HTTP response capture)
```

Multiple evidence items may be referenced per finding:

```
**Evidence:**
- EVID-2026-03-11-001 (Missing HSTS header — HTTP response capture)
- EVID-2026-03-11-002 (HSTS absent on redirect from HTTP — curl output)
```
