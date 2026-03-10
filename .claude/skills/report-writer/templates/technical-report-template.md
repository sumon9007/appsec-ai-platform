# Security Audit — Technical Report

**CLASSIFICATION:** [PLACEHOLDER — e.g., Confidential / Internal / Client Restricted]
**Report ID:** [PLACEHOLDER — e.g., AUDIT-2026-001-TECH]
**Version:** [PLACEHOLDER — e.g., DRAFT v0.1 / Final v1.0]
**Report Date:** [PLACEHOLDER — YYYY-MM-DD]

---

## Cover Information

| Field | Value |
|-------|-------|
| **Application** | [PLACEHOLDER] |
| **Target Environment** | [PLACEHOLDER — e.g., Production / Staging] |
| **Target URL(s)** | [PLACEHOLDER] |
| **Audit Period** | [PLACEHOLDER] |
| **Audit Type** | [PLACEHOLDER — e.g., Quarterly / Pre-Release / Annual] |
| **Auditor(s)** | [PLACEHOLDER] |
| **Report Prepared For** | [PLACEHOLDER] |
| **Authorization Reference** | [PLACEHOLDER] |

---

## Table of Contents

1. [Engagement Overview](#1-engagement-overview)
2. [Methodology](#2-methodology)
3. [Findings Summary](#3-findings-summary)
4. [Finding Details](#4-finding-details)
5. [Appendices](#5-appendices)

---

## 1. Engagement Overview

### 1.1 Scope

**In-Scope Targets:**
[PLACEHOLDER — List all in-scope URLs, endpoints, and features as defined in .claude/context/scope.md]

**Out-of-Scope:**
[PLACEHOLDER — List explicitly excluded targets and features]

### 1.2 Objectives

[PLACEHOLDER — Describe the objectives of this audit. E.g., "Assess the security posture of the Acme application ahead of the v2.4.0 production release, with focus on new features introduced in this release and remediation of findings from the Q4 2025 audit."]

### 1.3 Authorization

This engagement was authorized by [PLACEHOLDER — Name and title] on [PLACEHOLDER — Date].
Authorization Reference: [PLACEHOLDER — Email reference, document ID, or ticket number]
Testing approach: [PLACEHOLDER — Passive review / Passive + active testing on staging]

---

## 2. Methodology

### 2.1 Audit Domains Covered

| Domain | Coverage Level | Skill Used |
|--------|---------------|-----------|
| Authentication & Access Control | [Full / Spot-check / Not covered] | auth-access-audit |
| Authorization / RBAC | [Full / Spot-check / Not covered] | rbac-audit |
| Session Management & JWT | [Full / Spot-check / Not covered] | session-jwt-audit |
| Input Validation & Injection | [Full / Spot-check / Not covered] | input-validation-audit |
| Security Headers & Transport | [Full / Spot-check / Not covered] | headers-tls-audit |
| Dependency / Supply Chain | [Full / Spot-check / Not covered] | dependency-audit |
| Logging & Monitoring | [Full / Spot-check / Not covered] | logging-monitoring-audit |
| Security Misconfiguration | [Full / Spot-check / Not covered] | security-misconfig-audit |

### 2.2 Testing Approach

[PLACEHOLDER — Describe the testing approach:]
- Testing was conducted as [PLACEHOLDER — passive review / authenticated active testing]
- Test accounts: [PLACEHOLDER — roles tested]
- Observations were based on: [PLACEHOLDER — HTTP response analysis, configuration review, dependency manifest analysis, log review, etc.]

### 2.3 Tools and Resources Used

| Tool / Resource | Purpose |
|----------------|---------|
| [PLACEHOLDER — e.g., Browser DevTools] | [e.g., HTTP response header inspection] |
| [PLACEHOLDER — e.g., SSL Labs] | [e.g., TLS configuration assessment] |
| [PLACEHOLDER — e.g., npm audit / OSV] | [e.g., Dependency CVE scanning] |
| [PLACEHOLDER — e.g., SecurityHeaders.com] | [e.g., Header grading] |
| [PLACEHOLDER] | [PLACEHOLDER] |

### 2.4 Limitations

[PLACEHOLDER — Note any limitations that affected the assessment, e.g.:]
- [e.g., Log access was not available; logging assessment is based on client-provided information]
- [e.g., Full source code was not reviewed; findings are based on observable application behavior]
- [e.g., Assessment was limited to the staging environment]

---

## 3. Findings Summary

### 3.1 Severity Distribution

| Severity | Count | Open | Closed / Accepted |
|----------|-------|------|-------------------|
| Critical | [N] | [N] | [N] |
| High | [N] | [N] | [N] |
| Medium | [N] | [N] | [N] |
| Low | [N] | [N] | [N] |
| Info | [N] | [N] | [N] |
| **Total** | **[N]** | **[N]** | **[N]** |

### 3.2 Findings Table

| Finding ID | Title | Severity | Domain | Status | Date Found |
|------------|-------|----------|--------|--------|------------|
| FIND-001 | [PLACEHOLDER] | [SEVERITY] | [DOMAIN] | Open | [DATE] |
| FIND-002 | [PLACEHOLDER] | [SEVERITY] | [DOMAIN] | Open | [DATE] |
| FIND-003 | [PLACEHOLDER] | [SEVERITY] | [DOMAIN] | In Progress | [DATE] |
| FIND-004 | [PLACEHOLDER] | [SEVERITY] | [DOMAIN] | Closed | [DATE] |
| FIND-005 | [PLACEHOLDER] | [SEVERITY] | [DOMAIN] | Open | [DATE] |

---

## 4. Finding Details

*Complete one section per finding.*

---

### FIND-001: [PLACEHOLDER — Finding Title]

| Field | Value |
|-------|-------|
| **Finding ID** | FIND-001 |
| **Title** | [PLACEHOLDER] |
| **Severity** | [Critical / High / Medium / Low / Info] |
| **Domain** | [PLACEHOLDER] |
| **Status** | [Open / In Progress / Closed] |
| **Date Identified** | [YYYY-MM-DD] |
| **CWE** | [PLACEHOLDER — e.g., CWE-79] |

**Description:**

[PLACEHOLDER — Technical description of the vulnerability. Be precise and factual. Describe what was observed, where, and what the security issue is. Do not speculate beyond the evidence.]

**Evidence:**

| Evidence ID | Description |
|-------------|-------------|
| [EVID-YYYY-MM-DD-NNN] | [PLACEHOLDER — What this evidence demonstrates] |
| [EVID-YYYY-MM-DD-NNN] | [PLACEHOLDER] |

**Reproduction Steps:**

1. [PLACEHOLDER]
2. [PLACEHOLDER]
3. [PLACEHOLDER]
4. Observed result: [PLACEHOLDER]

**Impact:**

[PLACEHOLDER — Specific, technical impact assessment. What can an attacker achieve? What data or functionality is at risk?]

**Recommendation:**

[PLACEHOLDER — Specific, actionable remediation guidance with implementation detail.]

**References:**
- [CWE-NNN: CWE Title]
- [OWASP reference]

---

### FIND-002: [PLACEHOLDER — Finding Title]

| Field | Value |
|-------|-------|
| **Finding ID** | FIND-002 |
| **Title** | [PLACEHOLDER] |
| **Severity** | [SEVERITY] |
| **Domain** | [PLACEHOLDER] |
| **Status** | [PLACEHOLDER] |
| **Date Identified** | [YYYY-MM-DD] |

**Description:**
[PLACEHOLDER]

**Evidence:**
- [EVID-YYYY-MM-DD-NNN — description]

**Impact:**
[PLACEHOLDER]

**Recommendation:**
[PLACEHOLDER]

**References:**
- [PLACEHOLDER]

---

*[Add additional FIND-NNN sections as required — one per finding]*

---

## 5. Appendices

### Appendix A: Scope Confirmation

[PLACEHOLDER — Reproduce or reference the scope definition from .claude/context/scope.md]

### Appendix B: Methodology Notes

[PLACEHOLDER — Additional methodology detail not covered in the main body]

### Appendix C: Tool Output Excerpts

[PLACEHOLDER — Relevant tool output, SSL Labs summary, dependency scan summary, etc.]

### Appendix D: Evidence Index

| Evidence ID | Type | Domain | Finding ID | Location |
|-------------|------|--------|------------|---------|
| [EVID-YYYY-MM-DD-NNN] | [Type] | [Domain] | [FIND-NNN] | `evidence/reviewed/[filename]` |

---

*Report prepared by: [PLACEHOLDER] | Version: [PLACEHOLDER] | Date: [PLACEHOLDER]*
*Companion documents: Executive Summary, Remediation Plan*
