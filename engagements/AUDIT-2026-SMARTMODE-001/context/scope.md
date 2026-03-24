# Scope

> Read when: starting a domain review, classifying OOS observations, or verifying what is permitted.

## In-Scope Assets
| URL / Domain | Env | Notes |
|---|---|---|
| https://staff.smartmode.ai/ | Production | Primary target — staff portal |

### In-Scope Features
- Public-facing pages accessible without authentication
- Login / authentication flow (passive observation only)
- HTTP response headers, cookies, TLS configuration
- Publicly observable JavaScript references and dependencies
- Any API endpoints observable through standard application use

## Out-of-Scope
| Item | Reason |
|------|--------|
| Any domain not under smartmode.ai | Not in engagement agreement |
| Third-party embedded services (CDN, analytics, identity providers) | Not owned by target |
| Internal admin interfaces not publicly reachable | Not accessible in passive review |
| Other Smart Mode AI environments (staging, dev) | Not authorized |

### Prohibited Techniques
- Social engineering
- Denial of service or performance degradation
- Active exploitation or payload injection
- Fuzzing or brute force of any kind
- Form submissions with test payloads on production
- Credential stuffing

## Testing Boundaries
| Boundary | Constraint |
|----------|-----------|
| Active testing env | None — production passive review only |
| Window | 2026-03-24 → 2026-03-24 |
| Report due | 2026-03-24 |
| Data creation | Not permitted |
| Credentials | None provided — unauthenticated review only |

## Test Accounts
| Role | Email | Notes |
|------|-------|-------|
| N/A | N/A | No test accounts provided — unauthenticated passive review only |

## Scope Change Log
| Date | Change | Authorized By | Reference |
|------|--------|---------------|-----------|
| 2026-03-24 | Initial scope defined | Wilton White, CTO | Meeting Approval 2026-03-24 |

---
*Updated: 2026-03-24*
