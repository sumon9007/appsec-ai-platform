# AppSec AI Platform Full Build Roadmap

This document defines the recommended implementation roadmap for evolving `appsec-ai-platform` from a structured audit workspace with limited passive automation into a fuller web application security assessment platform.

It is based on the current platform coverage documented in `docs/coverage-matrix.md`.

---

## Goal

Build a practical, evidence-based, agentic application security platform that can support:

- passive web security assessment
- authenticated web application review
- controlled active testing with authorization gates
- API security assessment
- broader AppSec engineering checks over time

---

## Guiding Principles

1. **Safety first**
   - Active testing must remain disabled by default.
   - Every intrusive technique must require explicit authorization.
   - Stop conditions must be enforceable in code.

2. **Evidence first**
   - Every finding must have supporting evidence.
   - Findings should be reproducible from stored artifacts.
   - Review gaps must be distinct from confirmed vulnerabilities.

3. **Structured before broad**
   - Build durable orchestration, storage, and policy layers before adding many checkers.
   - Avoid a collection of disconnected scripts.

4. **Authenticated realism**
   - Full web app assessment requires authenticated workflows, role-aware testing, and session handling.

5. **Incremental completeness**
   - Reach meaningful value quickly through passive and authenticated phases before tackling the full active-testing surface.

---

## Target End State

At maturity, the platform should support:

- target and scope definition
- authorization-aware workflow selection
- route and endpoint discovery
- passive security assessment
- authenticated multi-role testing
- controlled active testing
- API assessment
- evidence capture and finding normalization
- executive, technical, and remediation reporting
- optional engineering AppSec extensions such as secrets, SAST, IaC, and container scanning

---

## Delivery Phases

## Phase 1: Platform Core

### Objective

Create a reliable foundation for workflows, persistence, and policy enforcement.

### Scope

- Define typed core entities:
  - `Target`
  - `AuditRun`
  - `Evidence`
  - `Finding`
  - `ControlCheck`
  - `ReviewGap`
  - `TestAccount`
  - `AuthorizationGrant`
- Add run-state persistence so workflows can resume safely
- Normalize findings/evidence/report schemas in code
- Add workflow context loading and execution metadata
- Expand CLI into domain-based subcommands
- Add structured logging and machine-readable outputs

### Deliverables

- `src/models/`
- `src/storage/`
- `src/workflows/`
- `src/policies/`
- expanded `src/cli.py`
- baseline tests for workflow orchestration and storage

### Exit Criteria

- A workflow can start, persist state, resume, and produce evidence/finding output deterministically
- Authorization mode is enforced in code
- Findings and evidence use stable schemas

---

## Phase 2: Passive Coverage Expansion

### Objective

Move beyond headers/TLS into meaningful passive web assessment coverage.

### Scope

- Build a crawler and route inventory engine
- Add public-page and asset discovery
- Add cookie/session/JWT passive analysis
- Add client-side inventory:
  - third-party scripts
  - iframe/embed review
  - mixed content signals
  - CSP and browser policy quality
- Add passive misconfiguration review:
  - metadata leaks
  - framework disclosures
  - cache controls
  - robots/security.txt
- Add dependency/CVE workflow for manifests and lockfiles

### Deliverables

- `src/tools/crawler.py`
- `src/tools/session_jwt_audit.py`
- `src/tools/dependency_audit.py`
- `src/tools/misconfig_audit.py`
- passive route inventory evidence

### Exit Criteria

- Public targets can be crawled safely
- Discovered pages/assets can be cataloged
- Session cookies/JWTs can be parsed and assessed
- Dependency manifests can produce evidence-backed findings

---

## Phase 3: Authenticated Assessment

### Objective

Support real web app testing with approved credentials and multi-role review.

### Scope

- Add secure handling for user-provided test credentials
- Add session manager and authenticated request handling
- Support authenticated crawling and per-role page capture
- Implement authentication review workflow:
  - MFA presence
  - password reset review
  - login behavior
  - lockout/rate-limit behavior
  - logout/session invalidation review
- Implement RBAC and IDOR workflow:
  - role matrix
  - horizontal access checks
  - vertical access checks
  - object reference review

### Deliverables

- `src/auth/`
- `src/session/`
- `src/tools/auth_audit.py`
- `src/tools/rbac_audit.py`
- credential/session handling policies

### Exit Criteria

- The platform can authenticate with approved test accounts
- It can run role-aware workflows
- It can produce evidence-backed auth and RBAC findings

---

## Phase 4: Controlled Active Testing

### Objective

Introduce carefully governed active validation for the core vulnerability classes.

### Scope

- Build explicit authorization checks for active modules
- Add rate-limit protection and stop conditions
- Add safe request replay controls
- Implement controlled active workflows for:
  - reflected XSS validation
  - SQL injection heuristics
  - SSRF probes
  - file upload review
  - CSRF validation
  - path traversal checks
- Require active-test evidence tagging with authorization context

### Deliverables

- `src/policies/authorization.py`
- `src/policies/stop_conditions.py`
- `src/tools/input_validation_audit.py`
- `src/tools/active_probe_engine.py`

### Exit Criteria

- Active testing cannot run without explicit approved mode
- Requests are rate-limited and auditable
- Confirmed active findings contain exact supporting evidence

---

## Phase 5: API Security

### Objective

Support modern web application assessment for REST, GraphQL, and related APIs.

### Scope

- OpenAPI and Postman collection ingestion
- API route and schema inventory
- Auth token capture and replay support
- API-specific testing for:
  - object-level authorization
  - function-level authorization
  - mass assignment
  - excessive data exposure
  - weak token enforcement
  - schema mismatch and unsafe defaults

### Deliverables

- `src/parsers/openapi.py`
- `src/parsers/postman.py`
- `src/tools/api_audit.py`
- API evidence and reporting templates

### Exit Criteria

- API definitions can be ingested and mapped into workflows
- Authenticated API testing is supported with evidence-backed outputs

---

## Phase 6: Engineering AppSec Extensions

### Objective

Extend beyond runtime web testing into broader application security coverage.

### Scope

- dependency governance and SBOM support
- secrets scanning
- SAST integration
- IaC scanning
- container image scanning
- cloud posture checks
- remediation tracking and trend reporting

### Deliverables

- `src/tools/secrets_scan.py`
- `src/tools/sast_integration.py`
- `src/tools/iac_scan.py`
- `src/tools/container_scan.py`
- `src/tools/cloud_posture.py`
- remediation dashboard/reporting extensions

### Exit Criteria

- Engineering AppSec scans can be run as optional workflows
- Findings integrate into the same evidence/reporting model

---

## Recommended Build Order

To maximize useful progress while minimizing rework, build in this exact order:

1. Core models and run-state persistence
2. Crawler and route inventory
3. Session/cookie/JWT passive analysis
4. Dependency/CVE workflow
5. Authenticated session support
6. Authentication workflow
7. RBAC/IDOR workflow
8. API security workflow
9. Controlled input validation / active testing
10. Engineering AppSec extensions

---

## Suggested Repository Structure

```text
src/
├── auth/
├── cli.py
├── config/
├── models/
├── parsers/
├── policies/
├── reporting/
├── session/
├── storage/
├── tools/
├── utils/
└── workflows/
```

### Responsibilities

- `models/`: typed entities and schemas
- `storage/`: persistence for runs, evidence, findings, state
- `policies/`: authorization, scope, safety, stop conditions
- `parsers/`: cookies, JWT, OpenAPI, HTML, JS, manifests
- `tools/`: domain-specific assessment logic
- `workflows/`: orchestration and sequencing
- `reporting/`: executive/technical/remediation generation
- `auth/` and `session/`: credential/session lifecycle logic

---

## Milestones

| Milestone | Meaning |
|----------|---------|
| M1 | Passive platform complete |
| M2 | Authenticated assessment complete |
| M3 | Controlled active testing complete |
| M4 | API assessment complete |
| M5 | Engineering AppSec extensions complete |

---

## Success Criteria By Milestone

### M1: Passive Platform Complete

- public route discovery works
- passive headers/TLS/session/dependency review works
- findings and evidence are normalized
- draft reporting is consistent

### M2: Authenticated Assessment Complete

- approved test credentials can be used safely
- role-aware workflows are supported
- authentication and RBAC findings are evidence-based

### M3: Controlled Active Testing Complete

- active testing is gated by explicit authorization
- stop conditions are enforceable
- high-risk vulnerability validation can be performed safely

### M4: API Assessment Complete

- OpenAPI/Postman ingestion works
- API auth, access control, and schema checks are operational

### M5: Engineering AppSec Extensions Complete

- secrets, SAST, IaC, container, and cloud findings can be normalized into the same platform

---

## Backlog By Priority

### P0: Must Build First

- core data model
- run-state persistence
- workflow engine
- policy/authorization layer
- crawler
- session/cookie/JWT analyzer

### P1: High Value

- authenticated session support
- auth review workflow
- RBAC/IDOR workflow
- dependency/CVE workflow
- report generation refinement

### P2: Major Expansion

- API security workflow
- controlled active testing
- misconfiguration expansion

### P3: Broader Platform Scope

- secrets scanning
- SAST
- IaC
- container scanning
- cloud posture

---

## Estimated Timeline

| Stage | Estimate |
|------|----------|
| Useful passive+authenticated v1 | 6-10 weeks |
| Strong end-to-end web app assessment platform | 3-5 months |
| Broader AppSec platform with engineering security extensions | 6+ months |

These estimates assume focused implementation effort and iterative delivery.

---

## Product Definition Of Done

The platform should only be described as a **full web application security assessment platform** when:

- major WSTG domains are at least partially executable
- authentication, session, RBAC, input validation, and API testing are implemented
- authenticated testing is supported
- active testing is explicitly policy-gated
- all findings are evidence-backed
- workflows are resumable and auditable
- reports can be generated consistently from stored findings/evidence

---

## Immediate Next Step

The recommended next implementation step is:

**Build Phase 1 completely, then begin Phase 2 with crawler plus session/cookie/JWT support.**

That will create the foundation needed for every later authenticated and active workflow.
