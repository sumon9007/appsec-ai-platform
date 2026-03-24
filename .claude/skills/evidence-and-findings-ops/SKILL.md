# Skill: Evidence and Findings Operations

## Purpose

Standardize evidence collection, labeling, storage, promotion, and referencing. Standardize finding creation, update, closure, and review-gap handling. Guide correct usage of the findings register and evidence store.

Use this skill when:
- You have observed something and need to decide if it is a finding, observation, or review gap
- You need to create or update a finding record
- You need to label and store new evidence
- You need to promote evidence through stages (raw → reviewed → summarized)
- You need to close a finding with evidence of fix
- You are unsure whether something meets the evidence quality standard

---

## Inputs Required

| Input | Source | Required? |
|-------|--------|-----------|
| Evidence quality rules | `.claude/rules/evidence-quality-rules.md` | Required |
| Evidence standard | `.claude/docs/evidence-standard.md` | Required |
| Reporting rules | `.claude/rules/reporting-rules.md` | Required (Rules 2, 7, 8, 9) |
| Remediation standard | `.claude/docs/remediation-standard.md` | Required for finding closure |
| Current findings register | `audits/[engagement-id]/findings-register.md` | Required |
| Python evidence writer | `src/utils/evidence_writer.py` | Python layer reference |
| Python findings writer | `src/utils/findings_writer.py` | Python layer reference |

---

## Method

### Phase 1: Classify the Observation

Before creating a finding, classify what you have observed:

| Classification | Definition | Finding Status | Action |
|---------------|------------|---------------|--------|
| Confirmed finding | Control failure with direct evidence | `confirmed` | Create finding with EVID- reference |
| Suspected finding | Reasonable inference from evidence, not proven | `suspected` | Create finding; label confidence clearly |
| Review gap | Condition cannot be confirmed or denied — insufficient access or evidence | `review-gap` | Record as GAP-NNN, not FIND-NNN |
| Out-of-scope observation | Relates to a target not listed in scope | Separate section | Label `[OUT OF SCOPE — NOT TESTED]` |
| Info observation | Worth noting, no direct security risk | `confirmed` / Info severity | Create finding with Info severity |

Do not create a `confirmed` finding without direct evidence. Never present guesses as confirmed findings.

### Phase 2: Evidence Labeling and Storage

**Label format:** `EVID-YYYY-MM-DD-NNN`
- `YYYY-MM-DD` = date of collection
- `NNN` = sequential number for that day (001, 002, 003...)

**File name format:** `EVID-YYYY-MM-DD-NNN-[brief-description].md`

**Header required in every evidence file:**
```
Evidence ID:    EVID-YYYY-MM-DD-NNN
Date Collected: YYYY-MM-DD
Collector:      [Auditor name]
Target:         [URL or component]
Description:    [What this evidence demonstrates]
```

**Storage stages — move through in order:**

| Stage | Location | When to Store |
|-------|----------|---------------|
| Raw | `evidence/raw/` | Immediately upon collection — no changes, no review |
| Reviewed | `evidence/reviewed/` | After confirming evidence is valid and relevant to a finding |
| Summarized | `evidence/summarized/` | After redacting sensitive data — safe for report inclusion |

**Never promote to `evidence/summarized/` without:**
1. Checking for credentials, PII, tokens, private keys, or payment data
2. Redacting sensitive values:
   - Tokens: show first/last 4 chars, mask middle → `eyJ...XXXX...dGVu`
   - PII: replace with `[PII REDACTED]`
   - Credentials: do not store — see `.claude/rules/safety-authorization-rules.md` Rule 6
   - Payment data: do not store — escalate immediately

**Python layer:** `src/utils/evidence_writer.py` handles EVID- labeling and raw storage automatically. Use it when running Python audit tools.

### Phase 3: Creating a Finding

Required fields for every finding (no exceptions):

```
Finding ID:       FIND-NNN (sequential; never reused; check register for next available)
Title:            [Short, descriptive title — no jargon]
Domain:           [Authentication | Authorization | Session Management | Input Validation |
                   Security Headers | Dependencies | Logging | Misconfiguration | API Security]
Severity:         [Critical | High | Medium | Low | Info]
Confidence:       [high | medium | low]
Status:           [confirmed | suspected | review-gap | mitigated | accepted-risk]
Target:           [URL or system component]
Evidence:         EVID-YYYY-MM-DD-NNN — [brief description of what the evidence shows]
Observation:      [What was observed — factual statements only, no speculation]
Risk:             [What an attacker could achieve if this is exploited]
Recommendation:   [Specific, actionable fix — see reporting rules Rule 3]
Date Identified:  YYYY-MM-DD
```

Before creating:
1. Verify severity is correct per `.claude/rules/severity-rating-rules.md`
2. Confirm evidence exists and is EVID-labeled
3. Check register for next available FIND-NNN (never reuse a closed finding's ID)
4. Confirm the finding uses standard severity vocabulary only (per `.claude/rules/reporting-rules.md` Rule 1)

**Python layer:** `src/utils/findings_writer.py` appends normalized findings to the register with validation.

### Phase 4: Updating a Finding

When a finding's status changes:
1. Update the Status field in the findings register
2. Add a status history note: `[YYYY-MM-DD] Status changed to [new status] — [reason]`
3. If adding evidence: add the new EVID- reference to the Evidence field
4. Do not delete prior status entries — preserve the history

### Phase 5: Closing a Finding

A finding may ONLY be moved to Closed status when all of the following are true:

1. Evidence of fix is provided:
   - Code fix: PR or commit reference
   - Config change: EVID-labeled capture of the new configuration
   - Dependency update: updated manifest file
   - Process change: written process description
2. You have reviewed the evidence and confirmed it directly addresses the finding
3. A verification re-test has been performed where possible — document as a new EVID- item
4. Both fix evidence and re-test evidence are referenced in the finding record

Finding IDs are **never** reused after closure. Reference closed findings by ID only.

### Phase 6: Recording a Review Gap

A review gap is not a finding — it is a documented limitation of the current assessment.

Record review gaps when:
- A control cannot be assessed due to lack of access (e.g., no log access, no test account)
- Evidence requires active testing that is not authorized in the current testing mode
- A system component is unknown (e.g., hosting provider not identified)
- An area is within scope but physically inaccessible during this session

Format:
```
Gap ID:               GAP-NNN
Domain:               [Affected domain]
Title:                [Brief description]
Why the Gap Exists:   [Access limitation | Authorization constraint | Unknown target detail]
Risk if Gap is Real:  [What would be discovered if a finding exists here]
Recommended Next Step: [What is needed to close this gap — test account, log access, active testing auth, etc.]
```

Record review gaps in:
- The current audit session record (`.claude/templates/audit-session-template.md`)
- The findings register under a "Review Gaps" section

---

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Labeled evidence files | `evidence/raw/EVID-YYYY-MM-DD-NNN-*.md` | Raw collected evidence |
| Promoted evidence | `evidence/reviewed/` and `evidence/summarized/` | After review and redaction |
| New finding records | `audits/[engagement-id]/findings-register.md` | Appended to findings register |
| Review gap records | Session record + findings register | Documented gaps for follow-up |

---

## Templates Used

- `.claude/docs/evidence-standard.md` — evidence format specification and register format
- `.claude/templates/findings-register-template.md` — findings register structure
- `.claude/templates/audit-session-template.md` — session record evidence inventory section
- `.claude/skills/evidence-and-findings-ops/templates/finding-record-template.md` — single finding record

---

## Rules Applied

- `.claude/rules/evidence-quality-rules.md` — all 10 rules
- `.claude/rules/reporting-rules.md` — Rules 1, 2, 3, 7, 8, 9
- `.claude/rules/remediation-rules.md` — Rule 5 (closure requires evidence), Rule 6 (regressions escalate)
- `.claude/rules/safety-authorization-rules.md` — Rule 6 (no secrets in evidence)

---

## Related Skills and Commands

- `/close-finding` — lifecycle command for closing a specific finding
- `report-writer` — reads the findings register as ground truth; register must be current before reporting
- `engagement-bootstrap` — creates the initial findings register for a new engagement
- `src/utils/evidence_writer.py` — Python: automated evidence labeling and raw storage
- `src/utils/findings_writer.py` — Python: automated finding registration with validation
