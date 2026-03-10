# Audit Scope

Defines the exact boundaries of the audit. Claude Code will enforce these boundaries throughout the engagement.

**SCOPE NOTE:** This document must be completed and reviewed before any audit activity begins. Claude Code will refuse to test targets not listed in the In-Scope section.

---

## In-Scope Targets

### URLs and Domains

| URL / Domain | Environment | Notes |
|--------------|-------------|-------|
| [PLACEHOLDER — e.g., https://app.example.com] | [e.g., Production] | [e.g., Primary application] |
| [PLACEHOLDER — e.g., https://api.example.com] | [e.g., Production] | [e.g., REST API] |
| [PLACEHOLDER — e.g., https://staging.example.com] | [e.g., Staging] | [e.g., Active testing permitted] |

### In-Scope Endpoints

| Endpoint | Method(s) | Notes |
|----------|-----------|-------|
| [PLACEHOLDER — e.g., /api/v1/*] | [e.g., GET, POST, PUT, DELETE] | [e.g., Full API surface] |
| [PLACEHOLDER — e.g., /auth/*] | [e.g., GET, POST] | [e.g., Authentication flows] |
| [PLACEHOLDER — e.g., /admin/*] | [e.g., GET, POST] | [e.g., Admin panel] |

### In-Scope Features

- [PLACEHOLDER — e.g., User registration and login]
- [PLACEHOLDER — e.g., Password reset flow]
- [PLACEHOLDER — e.g., User profile management]
- [PLACEHOLDER — e.g., File upload functionality]
- [PLACEHOLDER — e.g., Admin dashboard]
- [PLACEHOLDER — e.g., API key management]

---

## Out-of-Scope Items

**SCOPE NOTE:** The following are explicitly excluded from testing. If issues are discovered passively related to out-of-scope items, they will be noted as `[OUT OF SCOPE — NOT TESTED]` without further investigation.

### Out-of-Scope URLs and Domains

| URL / Domain | Reason for Exclusion |
|--------------|---------------------|
| [PLACEHOLDER — e.g., https://thirdparty.example.com] | [e.g., Not owned by client] |
| [PLACEHOLDER — e.g., https://legacy.example.com] | [e.g., Scheduled for decommission, separate engagement] |

### Out-of-Scope Features

- [PLACEHOLDER — e.g., Third-party payment processor UI (Stripe-hosted pages)]
- [PLACEHOLDER — e.g., CDN infrastructure]
- [PLACEHOLDER — e.g., Corporate network and internal systems]
- [PLACEHOLDER — e.g., Mobile applications (separate engagement)]

### Out-of-Scope Testing Techniques

- [PLACEHOLDER — e.g., Social engineering]
- [PLACEHOLDER — e.g., Physical security testing]
- [PLACEHOLDER — e.g., Denial of service testing]
- [PLACEHOLDER — e.g., Active exploitation on production (passive review only)]

---

## Testing Boundaries

| Boundary | Constraint |
|----------|-----------|
| Active Testing Environment | [PLACEHOLDER — e.g., Staging only / Production read-only] |
| Testing Window | [PLACEHOLDER — e.g., Weekdays 09:00–17:00 UTC] |
| Rate Limit Awareness | [PLACEHOLDER — e.g., Do not trigger rate limits on production] |
| Data Creation | [PLACEHOLDER — e.g., Use test accounts only; delete test data after] |
| Credential Usage | [PLACEHOLDER — e.g., Use only provided test credentials] |

---

## Test Accounts Provided

| Account Role | Username / Email | Notes |
|--------------|-----------------|-------|
| [PLACEHOLDER — e.g., Admin] | [PLACEHOLDER] | [e.g., Full admin privileges] |
| [PLACEHOLDER — e.g., Standard User] | [PLACEHOLDER] | [e.g., Typical user account] |
| [PLACEHOLDER — e.g., Read-Only] | [PLACEHOLDER] | [e.g., Read-only role] |

> Credentials are stored separately and must not be recorded in this document.

---

## Time Constraints

| Constraint | Detail |
|------------|--------|
| Audit Start Date | [PLACEHOLDER] |
| Audit End Date | [PLACEHOLDER] |
| Report Due Date | [PLACEHOLDER] |
| Total Allocated Time | [PLACEHOLDER — e.g., 40 hours] |

---

## Scope Change Process

Any changes to scope during the engagement must be:

1. Agreed in writing with the authorizing party
2. Documented here with date and reference
3. Confirmed before extending testing to newly in-scope targets

### Scope Change Log

| Date | Change Description | Authorized By | Reference |
|------|-------------------|---------------|-----------|
| [DATE] | [CHANGE] | [AUTHORIZER] | [REFERENCE] |

---

*Last updated: [PLACEHOLDER — Date]*
