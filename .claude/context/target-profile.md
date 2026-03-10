# Target Profile

Describes the application under audit. Populate before beginning. Update as new information is discovered during the engagement.

---

## Application Identity

| Field | Value |
|-------|-------|
| Application Name | [PLACEHOLDER] |
| Application Version / Release | [PLACEHOLDER] |
| Application Owner | [PLACEHOLDER — Team or individual responsible] |
| Business Purpose | [PLACEHOLDER — Brief description of what the application does] |
| Criticality | [PLACEHOLDER — Critical / High / Medium / Low] |
| Data Classification | [PLACEHOLDER — e.g., Public / Internal / Confidential / Restricted / PII / PCI / PHI] |

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend Framework | [PLACEHOLDER — e.g., React 18, Vue 3, Angular 17] |
| Backend Framework | [PLACEHOLDER — e.g., Node.js/Express, Django, Laravel, Rails] |
| Language(s) | [PLACEHOLDER — e.g., TypeScript, Python 3.11, PHP 8.2] |
| Database(s) | [PLACEHOLDER — e.g., PostgreSQL 15, MySQL 8, MongoDB 7] |
| Cache / Queue | [PLACEHOLDER — e.g., Redis, RabbitMQ, SQS] |
| Search | [PLACEHOLDER — e.g., Elasticsearch, Algolia] |
| File Storage | [PLACEHOLDER — e.g., AWS S3, Azure Blob, local filesystem] |
| API Style | [PLACEHOLDER — e.g., REST, GraphQL, gRPC, SOAP] |

---

## Hosting Environment

| Field | Value |
|-------|-------|
| Cloud Provider | [PLACEHOLDER — e.g., AWS, GCP, Azure, Self-hosted] |
| Deployment Model | [PLACEHOLDER — e.g., Containers (EKS/ECS), VMs, Serverless, PaaS] |
| CDN / WAF | [PLACEHOLDER — e.g., Cloudflare, AWS CloudFront, Akamai, None] |
| Load Balancer | [PLACEHOLDER — e.g., AWS ALB, nginx, HAProxy] |
| Region(s) | [PLACEHOLDER — e.g., us-east-1, eu-west-1] |
| Environment Type | [PLACEHOLDER — Production / Staging / QA] |

---

## Authentication

| Field | Value |
|-------|-------|
| Primary Auth Mechanism | [PLACEHOLDER — e.g., Username/Password, SSO, OAuth 2.0, SAML] |
| Identity Provider | [PLACEHOLDER — e.g., Auth0, Okta, AWS Cognito, Custom] |
| MFA Support | [PLACEHOLDER — Yes / No / Optional / Unknown] |
| MFA Methods | [PLACEHOLDER — e.g., TOTP, SMS, Push, Hardware Key] |
| Session Management | [PLACEHOLDER — e.g., JWT, Server-side sessions, Cookie-based] |
| Password Policy | [PLACEHOLDER — Min length, complexity, expiry, breach check] |

---

## User Roles

| Role Name | Description | Approximate User Count |
|-----------|-------------|----------------------|
| [PLACEHOLDER — e.g., Admin] | [PLACEHOLDER — Role description] | [PLACEHOLDER] |
| [PLACEHOLDER — e.g., Manager] | [PLACEHOLDER] | [PLACEHOLDER] |
| [PLACEHOLDER — e.g., Standard User] | [PLACEHOLDER] | [PLACEHOLDER] |
| [PLACEHOLDER — e.g., Read-Only] | [PLACEHOLDER] | [PLACEHOLDER] |
| [PLACEHOLDER — e.g., API Service] | [PLACEHOLDER] | [PLACEHOLDER] |

---

## Known Integrations and Third Parties

| Integration | Type | Data Shared | Trust Level |
|-------------|------|-------------|-------------|
| [PLACEHOLDER — e.g., Stripe] | [e.g., Payment processor] | [e.g., Payment details] | [e.g., High] |
| [PLACEHOLDER — e.g., SendGrid] | [e.g., Email delivery] | [e.g., Email addresses] | [e.g., Medium] |
| [PLACEHOLDER — e.g., Google Analytics] | [e.g., Analytics] | [e.g., Usage data, IP] | [e.g., Low] |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

---

## API Surface

| Field | Value |
|-------|-------|
| Public API | [PLACEHOLDER — Yes / No] |
| API Authentication | [PLACEHOLDER — e.g., API Key, OAuth 2.0, JWT, None] |
| API Documentation | [PLACEHOLDER — Public / Internal / None] |
| Key API Endpoints Known | [PLACEHOLDER — List or reference] |

---

## Security Controls Known

| Control | Status |
|---------|--------|
| WAF / DDoS Protection | [PLACEHOLDER — Present / Absent / Unknown] |
| Rate Limiting | [PLACEHOLDER — Present / Absent / Unknown] |
| SIEM / Centralized Logging | [PLACEHOLDER — Present / Absent / Unknown] |
| Vulnerability Scanning | [PLACEHOLDER — Present / Absent / Unknown] |
| Penetration Testing History | [PLACEHOLDER — Last tested: DATE / Never / Unknown] |
| Bug Bounty Program | [PLACEHOLDER — Yes / No / Unknown] |

---

## Notes and Observations

[PLACEHOLDER — Record any additional observations about the target that are relevant to the audit.]

---

*Last updated: [PLACEHOLDER — Date]*
