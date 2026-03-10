# Evidence Quality Rules

These rules govern how evidence must be collected, labeled, stored, and referenced. All findings must comply with these rules.

---

## Rule 1: No Finding Without Evidence

**Every finding recorded in this workspace must reference at least one piece of evidence.**

A finding that lacks an evidence reference is not a finding — it is an observation or a hypothesis. Such items must be clearly labeled `[UNCONFIRMED — REQUIRES EVIDENCE]` and must not be included in formal reports or the findings register until evidence is obtained.

If evidence cannot be obtained (e.g., the auditor cannot access the relevant system), the observation may be recorded as an `[UNKNOWN]` item with an explanation of why it could not be confirmed.

---

## Rule 2: Evidence Labeling Convention

All evidence items must be labeled using the standard format:

```
EVID-YYYY-MM-DD-NNN
```

Where:
- `YYYY-MM-DD` is the date the evidence was collected
- `NNN` is a three-digit sequential number, resetting each day (001, 002, 003...)

This label must appear:
- In the evidence file name: `EVID-YYYY-MM-DD-NNN-[brief-description].md`
- In the evidence file header
- In every finding that references this evidence item

**Non-compliant labels (do not use):**
- `screenshot-1`, `img_001`, `test-result`, unnamed screenshots, etc.

---

## Rule 3: Evidence Storage Locations

Evidence must be stored in the appropriate stage folder:

| Stage | Location | When to Store |
|-------|----------|---------------|
| Raw | `evidence/raw/` | Immediately upon collection, before review |
| Reviewed | `evidence/reviewed/` | After confirming evidence is valid and relevant to a finding |
| Summarized | `evidence/summarized/` | After sanitizing of PII, credentials, and sensitive system details — for inclusion in reports |

**Never move evidence to `evidence/summarized/` until:**
- It has been reviewed for sensitive data (credentials, PII, private keys)
- Sensitive data has been redacted or noted for exclusion from reports

---

## Rule 4: Evidence Must Be Reproducible

Evidence must demonstrate a reproducible condition. A one-time, transient observation that cannot be reproduced does not constitute evidence for a formal finding unless:
- The transience itself is part of the finding (e.g., race condition, intermittent exposure)
- The observation is documented in sufficient detail to establish that it occurred

For reproducibility, document:
- The exact steps to reproduce the condition
- The environment (URL, endpoint, parameters, authentication state)
- The expected vs. observed result

---

## Rule 5: Evidence Must Be Authentic

Evidence must not be:
- Altered or modified after collection
- Fabricated or constructed from assumptions
- Misleadingly cropped to omit context that would change interpretation
- Presented as more recent or from a different target than it is

If evidence needs to be annotated or highlighted, do so in a way that makes clear what is original content and what is annotation (e.g., annotations in red boxes on screenshots).

---

## Rule 6: Evidence Must Be Dated and Attributed

Every evidence item must clearly show:
- **Date collected:** The date the evidence was captured
- **Collector:** Who collected it (auditor name)
- **Target:** What system or URL it relates to

Evidence without a date may not be used to support a finding.

---

## Rule 7: Sensitive Data in Evidence

If evidence contains sensitive data, follow this protocol:

| Data Type | Action |
|-----------|--------|
| Passwords or plaintext credentials | Stop — escalate per `.claude/rules/safety-authorization-rules.md`. Do not store in evidence files without explicit guidance. Redact before referencing in reports. |
| Authentication tokens, API keys | Redact before promoting to `evidence/summarized/`. Truncate tokens (show first/last 4 characters, mask middle). |
| PII (names, emails, phone, addresses, health data) | Redact before promoting to `evidence/summarized/`. Use placeholder: `[PII REDACTED]`. |
| Payment card data | Do not store. Redact immediately and escalate. |
| Private encryption keys | Do not store. Escalate immediately. |

---

## Rule 8: Evidence References in Findings

When referencing evidence in a finding, use the format:

```
**Evidence:** EVID-2026-03-11-001 (Missing HSTS header — HTTP response capture)
```

Multiple evidence items:

```
**Evidence:**
- EVID-2026-03-11-001 (Missing HSTS header — HTTP response capture of main page)
- EVID-2026-03-11-002 (HSTS also absent on authenticated response — curl output)
```

Never reference evidence by informal name only (e.g., "see the screenshot"). Always use the EVID- label.

---

## Rule 9: Evidence Register Maintenance

A running evidence register must be maintained for each engagement. Record all collected evidence items in it, even if they do not yet have an associated finding.

See `.claude/docs/evidence-standard.md` for the evidence register format.

---

## Rule 10: Chain of Custody

For engagements with compliance or legal implications, document the chain of custody for each evidence item:
- Date and time of collection
- Who collected it
- How it was stored
- Any access or handling after initial collection

This is optional for routine audits but required for audits that may be used in legal proceedings or compliance reporting.
