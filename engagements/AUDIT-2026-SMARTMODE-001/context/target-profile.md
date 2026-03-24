# Target Profile

> Read when: tech stack, auth model, integrations, or data sensitivity matter for a finding.

## Application
| Field | Value |
|-------|-------|
| Name | Smart Mode |
| Purpose | Staff portal — internal workforce or operations platform |
| Criticality | UNKNOWN |
| Data Class | UNKNOWN — assumed internal/confidential given staff portal nature |
| Owner | Smart Mode AI |
| Version | UNKNOWN |

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | UNKNOWN |
| Backend | Node.js (confirmed by client) |
| Language | JavaScript / Node.js |
| Database | UNKNOWN |
| Cache / Queue | UNKNOWN |
| API Style | UNKNOWN |

## Hosting
| Field | Value |
|-------|-------|
| Cloud / Provider | UNKNOWN |
| CDN / WAF | UNKNOWN |
| Deployment | UNKNOWN |
| Environment | Production |

## Auth Model
| Field | Value |
|-------|-------|
| Mechanism | UNKNOWN — login flow observable passively |
| IdP | UNKNOWN |
| MFA | UNKNOWN |
| Sessions | UNKNOWN |
| Password Policy | UNKNOWN |

## User Roles
| Role | Description |
|------|-------------|
| Staff | Internal users accessing the staff portal |
| [Others TBD] | Additional roles unknown until authenticated review |

## Integrations & Third Parties
| System | Type | Data Shared | Trust |
|--------|------|-------------|-------|
| [TBD] | [TBD] | [TBD] | [TBD] |

## API Surface
| Field | Value |
|-------|-------|
| Public API | UNKNOWN |
| Auth | UNKNOWN |
| Docs | UNKNOWN |

## Observations
- Staff portal implies internal-facing sensitive data — assume Confidential classification until confirmed
- Node.js backend confirmed by client — look for Node.js-specific headers (X-Powered-By: Express, etc.)

---
*Updated: 2026-03-24*
