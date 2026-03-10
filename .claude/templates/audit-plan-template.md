# Audit Plan

A pre-engagement planning document. Complete before beginning any audit to align objectives, scope, resources, and deliverables.

---

## Plan Header

| Field | Value |
|-------|-------|
| **Audit Name** | [PLACEHOLDER] |
| **Audit ID** | [PLACEHOLDER — e.g., AUDIT-2026-001] |
| **Plan Version** | [PLACEHOLDER — e.g., v1.0] |
| **Plan Date** | [PLACEHOLDER — YYYY-MM-DD] |
| **Audit Type** | [PLACEHOLDER — e.g., Quarterly / Pre-Release / Annual] |
| **Planned Start Date** | [PLACEHOLDER] |
| **Planned End Date** | [PLACEHOLDER] |
| **Report Due Date** | [PLACEHOLDER] |

---

## Target

| Field | Value |
|-------|-------|
| **Application Name** | [PLACEHOLDER] |
| **Target URL(s)** | [PLACEHOLDER] |
| **Environment** | [PLACEHOLDER — Production / Staging / QA] |
| **Application Owner** | [PLACEHOLDER] |
| **Criticality** | [PLACEHOLDER — Critical / High / Medium / Low] |

---

## Objectives

[PLACEHOLDER — List the specific objectives of this audit. What questions should the audit answer? What risks are being assessed?]

1. [PLACEHOLDER — e.g., Assess the security of the new file upload feature introduced in v2.4.0]
2. [PLACEHOLDER — e.g., Verify remediation of findings from the Q4 2025 audit]
3. [PLACEHOLDER — e.g., Conduct quarterly assessment of all security domains]

---

## Team

| Role | Name | Responsibilities |
|------|------|-----------------|
| Lead Auditor | [PLACEHOLDER] | Overall audit management, report authorship |
| Security Reviewer | [PLACEHOLDER] | Domain-specific testing and analysis |
| Technical Contact (Client) | [PLACEHOLDER] | Provide test accounts, manifests, log access |
| Authorization Contact | [PLACEHOLDER] | Sign-off and scope confirmation |

---

## Scope

**In-Scope:**

| Item | Type | Notes |
|------|------|-------|
| [PLACEHOLDER — e.g., https://app.example.com] | Primary application | [NOTES] |
| [PLACEHOLDER — e.g., https://api.example.com] | REST API | [NOTES] |
| [PLACEHOLDER] | [PLACEHOLDER] | [NOTES] |

**Out-of-Scope:**

| Item | Reason |
|------|--------|
| [PLACEHOLDER] | [PLACEHOLDER] |

**Testing Approach:** [PLACEHOLDER — e.g., Passive review only / Active testing on staging]

---

## Audit Domains to Cover

| Domain | Coverage Level | Priority | Skill |
|--------|---------------|---------|-------|
| Authentication & Access Control | [Full / Spot-check / Skip] | [High/Medium/Low] | auth-access-audit |
| Authorization / RBAC | [Full / Spot-check / Skip] | [High/Medium/Low] | rbac-audit |
| Session Management & JWT | [Full / Spot-check / Skip] | [High/Medium/Low] | session-jwt-audit |
| Input Validation & Injection | [Full / Spot-check / Skip] | [High/Medium/Low] | input-validation-audit |
| Security Headers & Transport | [Full / Spot-check / Skip] | [High/Medium/Low] | headers-tls-audit |
| Dependency / Supply Chain | [Full / Spot-check / Skip] | [High/Medium/Low] | dependency-audit |
| Logging & Monitoring | [Full / Spot-check / Skip] | [High/Medium/Low] | logging-monitoring-audit |
| Security Misconfiguration | [Full / Spot-check / Skip] | [High/Medium/Low] | security-misconfig-audit |

---

## Schedule

| Day | Activity | Responsible |
|-----|----------|------------|
| Day 1 | Context review, scope confirmation, session setup | [PLACEHOLDER] |
| Day 2 | Security headers, TLS, misconfiguration review | [PLACEHOLDER] |
| Day 3 | Authentication, session management review | [PLACEHOLDER] |
| Day 4 | RBAC and authorization review | [PLACEHOLDER] |
| Day 5 | Input validation, dependency review | [PLACEHOLDER] |
| Day 6 | Logging review, findings compilation | [PLACEHOLDER] |
| Day 7 | Draft report preparation | [PLACEHOLDER] |
| Day 8 | Report review and finalization | [PLACEHOLDER] |

---

## Tools to Use

| Tool | Purpose | Notes |
|------|---------|-------|
| [PLACEHOLDER — e.g., Browser DevTools] | [e.g., Header and session inspection] | [NOTES] |
| [PLACEHOLDER — e.g., SSL Labs] | [e.g., TLS assessment] | [NOTES] |
| [PLACEHOLDER — e.g., npm audit / OSV] | [e.g., Dependency CVE scanning] | [NOTES] |
| [PLACEHOLDER] | [PLACEHOLDER] | [NOTES] |

---

## Required Inputs from Client

| Item | Owner | Due Date | Received? |
|------|-------|----------|---------|
| Test account credentials (all roles) | [PLACEHOLDER] | [DATE] | [Yes/No/Pending] |
| Dependency manifests | [PLACEHOLDER] | [DATE] | [Yes/No/Pending] |
| API documentation | [PLACEHOLDER] | [DATE] | [Yes/No/Pending] |
| Log sample (past 30 days) | [PLACEHOLDER] | [DATE] | [Yes/No/Pending] |
| Signed authorization document | [PLACEHOLDER] | [DATE] | [Yes/No/Pending] |

---

## Deliverables

| Deliverable | Format | Due Date | Recipient |
|-------------|--------|----------|-----------|
| Executive Summary | Markdown report | [DATE] | [PLACEHOLDER] |
| Technical Report | Markdown report | [DATE] | [PLACEHOLDER] |
| Remediation Plan | Markdown document | [DATE] | [PLACEHOLDER] |
| Findings Register (updated) | Markdown register | [DATE] | [PLACEHOLDER] |

---

## Sign-Off

This audit plan is approved by:

| Role | Name | Signature / Reference | Date |
|------|------|----------------------|------|
| Audit Lead | [PLACEHOLDER] | [PLACEHOLDER] | [DATE] |
| Authorizing Party | [PLACEHOLDER] | [PLACEHOLDER] | [DATE] |

---

*Template: audit-plan-template.md*
