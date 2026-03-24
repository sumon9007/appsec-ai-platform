# PRD Security Analysis Output

Use this template to record the output of a `prd-security-review` skill session. One document per PRD or feature reviewed.

**Important:** Content here is design-time observations, not audit findings. Do not create FIND-NNN records from this document.

---

## Review Metadata

```
PRD / Feature:      [Name or title of the feature or document reviewed]
PRD Version:        [Version or date of the document]
Review Date:        [YYYY-MM-DD]
Reviewer:           [Analyst name]
Engagement:         [Engagement ID from audit-context.md if applicable]
Status:             Design-time review — not a live audit
```

---

## Feature Inventory

| Feature ID | Feature Name | Data Handled | User Roles | New Endpoints? | File Handling? | Security Flags |
|-----------|-------------|--------------|------------|----------------|----------------|---------------|
| F-001 | | | | Yes/No | Yes/No | |
| F-002 | | | | Yes/No | Yes/No | |
| F-003 | | | | Yes/No | Yes/No | |

**Security flag key:**
- `AUTH` — touches authentication (login, registration, MFA, SSO)
- `AUTHZ` — touches authorization (roles, permissions, resource access)
- `DATA` — introduces new PII, financial, or health data
- `FILE` — file upload, download, or user-supplied content rendering
- `3P` — new third-party integration
- `PRIV` — privileged operations (admin, bulk, export)
- `PUB` — publicly accessible without authentication

---

## Data Flow Map

For each flagged feature, complete one block:

```
Feature:        F-[NNN] — [Feature name]
Trigger:        [User action or event]
Source:         [Where data originates]
Processing:     [Validation, encoding, transformation steps — note gaps]
Destination:    [Database, external API, file system, email]
Storage:        [Where persisted, if at all]
Retention:      [How long retained]
Security Notes: [Any undocumented validation, encoding, or authorization gaps observed in the spec]
```

---

## Trust Boundary Map

| Boundary ID | From (Lower Trust) | To (Higher Trust) | Data Crossing | Auth at Boundary Described? | Notes |
|-------------|-------------------|-------------------|---------------|---------------------------|-------|
| TB-001 | | | | Yes/No | |
| TB-002 | | | | Yes/No | |
| TB-003 | | | | Yes/No | |

---

## Threat Surface Observations

Design-time observations only — not findings. These inform future audit focus.

| Feature | Observation | Threat Scenario | Priority | Audit Domain |
|---------|------------|----------------|----------|-------------|
| F-001 | | | High/Med/Low | |
| F-002 | | | High/Med/Low | |

---

## Implicit Security Requirements

Security controls that should be present based on the features described, even if not stated in the PRD:

| Feature | Implicit Requirement | Why Required |
|---------|---------------------|-------------|
| F-001 | [e.g., "Password reset tokens must be single-use and expire within 1 hour"] | Password reset flow introduced |
| F-002 | | |

---

## Audit Domain Priority List

When this feature is deployed, invoke domain skills in this order:

| Priority | Audit Domain | Reason | Skill |
|----------|-------------|--------|-------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |

---

## Required Controls Checklist

Controls to verify once the feature is built and live. Pass this list to the release gate review.

| Feature | Required Control | Verification Method | Authorized Mode |
|---------|----------------|--------------------|----|
| F-001 | | | Passive / Active |
| F-002 | | | Passive / Active |

---

## Open Questions

Items that could not be determined from the PRD alone — require clarification before or during audit:

- [ ] [Question 1]
- [ ] [Question 2]

---

## Summary

```
Features reviewed:            [N total]
Flagged as security-relevant: [N]
Threat observations noted:    [N]
Implicit requirements found:  [N]
Audit domains to prioritize:  [list]
Open questions:               [N]

Recommended action: [e.g., "Clarify open questions before development. Prioritize auth and
                    input-validation audit once feature is live."]
```

---

*Template version: 1.0 | Outputs are design-time observations, not audit findings*
*Governed by `.claude/docs/prd-analysis.md` and `.claude/rules/reporting-rules.md` Rule 2*
