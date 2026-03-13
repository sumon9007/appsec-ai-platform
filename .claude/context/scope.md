# Audit Scope

Defines the exact boundaries of the audit. Claude Code will enforce these boundaries throughout the engagement.

**SCOPE NOTE:** This document must be completed and reviewed before any audit activity begins. Claude Code will refuse to test targets not listed in the In-Scope section.

---

## In-Scope Targets

### URLs and Domains

| URL / Domain | Environment | Notes |
|--------------|-------------|-------|
| https://diversifiedrobotic.com/ | Production | Primary public website; passive review only |

### In-Scope Endpoints

| Endpoint | Method(s) | Notes |
|----------|-----------|-------|
| / | GET | Homepage passive response review |
| /blog | GET | Public content review if observed passively |
| /evolve | GET | Public content review if observed passively |

### In-Scope Features

- Public website responses and transport configuration
- Security headers and TLS posture
- Publicly accessible pages linked from the main site

---

## Out-of-Scope Items

**SCOPE NOTE:** The following are explicitly excluded from testing. If issues are discovered passively related to out-of-scope items, they will be noted as `[OUT OF SCOPE — NOT TESTED]` without further investigation.

### Out-of-Scope URLs and Domains

| URL / Domain | Reason for Exclusion |
|--------------|---------------------|
| Third-party embedded services | Not owned by target unless explicitly authorized |

### Out-of-Scope Features

- Third-party chat/coprocessor services embedded by iframe
- Corporate network, internal systems, and non-public applications
- Source code review and authenticated-only functionality

### Out-of-Scope Testing Techniques

- Social engineering
- Physical security testing
- Denial of service testing
- Active exploitation, fuzzing, brute force, or intrusive scanning

---

## Testing Boundaries

| Boundary | Constraint |
|----------|-----------|
| Active Testing Environment | None authorized |
| Testing Window | Current session on 2026-03-13 |
| Rate Limit Awareness | Passive requests only; avoid high-volume access |
| Data Creation | No data creation permitted |
| Credential Usage | No credentials used in this review |

---

## Test Accounts Provided

| Account Role | Username / Email | Notes |
|--------------|-----------------|-------|
| None provided | N/A | Passive public-site review only |

> Credentials are stored separately and must not be recorded in this document.

---

## Time Constraints

| Constraint | Detail |
|------------|--------|
| Audit Start Date | 2026-03-13 |
| Audit End Date | 2026-03-13 |
| Report Due Date | 2026-03-13 |
| Total Allocated Time | Short focused review |

---

## Scope Change Process

Any changes to scope during the engagement must be:

1. Agreed in writing with the authorizing party
2. Documented here with date and reference
3. Confirmed before extending testing to newly in-scope targets

### Scope Change Log

| Date | Change Description | Authorized By | Reference |
|------|-------------------|---------------|-----------|
| 2026-03-13 | Initial passive-review scope recorded for diversifiedrobotic.com | Requester | User authorization statement in current session |

---

*Last updated: 2026-03-13*
