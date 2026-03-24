# Skill: PRD and Feature Security Review

## Purpose

Review new features, product requirements documents (PRDs), architectural change proposals, and user stories for security impact before development begins or before a release gate. Identifies new attack surface, trust boundary crossings, abuse cases, required security controls, and which audit domains to prioritize once the feature is live.

Use this skill:
- When a new feature is being designed or specified
- When a significant architecture change is being planned
- When a new third-party integration is being introduced
- Before an engineering team begins implementation of a security-sensitive feature
- As an input to release gate planning when a PRD is available

**Important:** Outputs of this skill are design-time observations — not audit findings. No live evidence is collected. Do not create FIND-NNN records from PRD review. Once a feature is built and live, switch to the relevant domain skill for evidence-based audit.

---

## Inputs Required

| Input | Source | Required? |
|-------|--------|-----------|
| PRD, feature spec, or design document | Provided by user | Required |
| PRD analysis framework | `.claude/docs/prd-analysis.md` | Required |
| Audit domains reference | `.claude/docs/audit-domains.md` | Required |
| Current target profile | `.claude/context/target-profile.md` | Recommended |
| Current scope | `.claude/context/scope.md` | Recommended |

---

## Method

### Phase 1: Feature Inventory

1. Read the provided PRD or feature specification in full
2. Apply `.claude/docs/prd-analysis.md` — Step 1 (Feature Inventory)
3. Build the feature inventory table:

| Feature ID | Feature Name | Data Handled | User Roles | New Endpoints? | File Handling? |
|-----------|-------------|--------------|------------|----------------|----------------|
| F-001 | ... | ... | ... | Yes/No | Yes/No |

4. Apply security flags to each feature:
   - **Auth-touching:** login, registration, password reset, MFA, SSO changes
   - **Authz-touching:** new resources, role changes, permission changes
   - **Data-handling:** new PII, financial data, health data, or external data sources
   - **File-handling:** upload, download, rendering of user-supplied files
   - **Third-party integration:** new external service connections
   - **Privileged operations:** admin functions, bulk operations, data export
   - **Public-facing:** accessible without authentication

### Phase 2: Data Flow Mapping

5. Apply `.claude/docs/prd-analysis.md` — Step 2 (Data Flows)
6. For each flagged feature, map the flow:
   - Trigger → Source → Processing → Destination → Storage → Retention
7. Note any flows that lack documented validation, encoding, encryption, or authorization

### Phase 3: Trust Boundary Analysis

8. Apply `.claude/docs/prd-analysis.md` — Step 3 (Trust Boundaries)
9. Identify boundary crossings — where trust level changes:
   - Public internet → Application server
   - Standard user → Admin function
   - Application server → Database
   - Application server → Third-party API
10. For each crossing: is authentication or authorization explicitly described in the PRD?
11. Flag any crossing with no documented control as a boundary gap

### Phase 4: Threat Surface Observations

12. Apply `.claude/docs/prd-analysis.md` — Step 4 (Threat Surface Notes)
13. For each flagged feature, document potential threat scenarios:

| Feature | Observation | Threat Scenario | Priority | Audit Domain |
|---------|------------|----------------|----------|-------------|
| F-001 | File upload with no described MIME validation | Malicious file upload, stored XSS | High | Input Validation |

14. Identify implicit security requirements — controls that should be present but are not stated in the PRD:
    - File upload → "Files must be scanned for malware before storage; MIME type must be validated server-side"
    - Password reset → "Tokens must be single-use and expire within 1 hour"
    - New admin function → "All admin actions must be logged with user identity and timestamp"
    - New data export → "Export must be scoped to the requesting user's permissions"
    - New third-party integration → "Secrets and API keys must be stored in a vault, not in code or env files"

### Phase 5: Audit Domain Prioritization

15. Apply `.claude/docs/prd-analysis.md` — Step 5 (Audit Prioritization)
16. Produce a prioritized domain list for when the feature is live:

| Priority | Audit Domain | Reason | Skill to Invoke |
|----------|-------------|--------|----------------|
| 1 | Authentication | Feature modifies login flow | `auth-access-audit` |
| 2 | Input Validation | File upload introduced | `input-validation-audit` |
| ... | | | |

Domain-to-skill mapping:
- Authentication → `auth-access-audit`
- Authorization / IDOR → `rbac-audit`
- Session management / JWT → `session-jwt-audit`
- Input handling / injection → `input-validation-audit`
- Security headers / CORS / TLS → `headers-tls-audit`
- Dependencies / third-party packages → `dependency-audit`
- Misconfiguration / cloud config → `security-misconfig-audit`
- Logging / monitoring → `logging-monitoring-audit`

### Phase 6: Required Controls Checklist

17. For each flagged feature, list controls that must be verified once built:

| Feature | Required Control | How to Verify | Priority |
|---------|----------------|--------------|----------|
| F-001 | Rate limiting on OTP endpoint | Passive: observe rate limit response after N requests | High |
| F-002 | Server-side MIME validation on upload | Active (authorized): submit non-matching MIME type | High |

These become acceptance criteria verification items for the next release gate review.

---

## Outputs

| Output | Template | Description |
|--------|---------|-------------|
| PRD security analysis | `templates/prd-security-output.md` | Feature inventory, data flows, trust boundaries, threat observations |
| Implicit requirements | Within analysis | Security controls the spec should explicitly require |
| Audit domain priority list | Within analysis | Which skills to invoke once the feature is deployed |
| Required controls checklist | Within analysis | Verification items for the next release gate |

---

## Templates Used

- `.claude/skills/prd-security-review/templates/prd-security-output.md` — structured output template
- `.claude/docs/prd-analysis.md` — core analysis framework

---

## Important Constraints

- Do NOT create FIND-NNN records from a PRD review — no live evidence exists
- Label all outputs as design-time observations: "control may be required" not "control is absent"
- If the feature is already deployed, switch to the relevant domain skill and conduct a live review
- Threat scenarios are inputs to future audits, not current findings

---

## Rules Applied

- `.claude/rules/reporting-rules.md` — Rule 2 (no speculative findings — outputs here are design-time observations)
- `.claude/rules/evidence-quality-rules.md` — Rule 1 (no finding without evidence — this skill does not produce findings)
- `.claude/rules/safety-authorization-rules.md` — applies when outputs are acted upon in live testing

---

## Related Skills and Commands

- `release-gate-review` — use this skill's outputs as input when the release is ready for gate review
- `evidence-and-findings-ops` — use after the feature is deployed and live evidence is collected
- All domain audit skills — prioritized by Phase 5 of this skill; invoked post-deployment
- `.claude/docs/prd-analysis.md` — the core methodology framework this skill wraps and structures
