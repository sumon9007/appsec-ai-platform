# PRD Security Analysis Guide

A structured guide for analyzing a Product Requirements Document (PRD), feature specification, or design document to identify security implications before audit or development review.

---

## Purpose

When provided with a PRD, feature spec, or user story document, use this guide to systematically surface:

- The features that introduce new attack surface
- Data flows that cross trust boundaries
- Implicit security requirements that may be unstated
- Threat scenarios worth noting before audit begins

---

## Step 1: Feature Inventory

Read the PRD and build a feature inventory. For each feature:

| Feature ID | Feature Name | Description | Data Handled | User Roles Involved | New Endpoints? | Files / Media? |
|-----------|-------------|-------------|--------------|---------------------|----------------|----------------|
| F-001 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [Yes/No] | [Yes/No] |
| F-002 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [Yes/No] | [Yes/No] |
| F-003 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [Yes/No] | [Yes/No] |

### Feature Security Flags

As you populate the inventory, flag features that exhibit these characteristics:

- **Authentication-touching:** Changes to login, registration, password reset, MFA, SSO
- **Authorization-touching:** New resources, new roles, permission changes
- **Data-handling:** Introduces new PII, sensitive data categories, or external data sources
- **File handling:** Upload, download, rendering of user-supplied files
- **Third-party integration:** New external service connections
- **Privileged operations:** Admin functions, bulk operations, data export
- **Public-facing:** Features accessible without authentication

---

## Step 2: Data Flows

Map how data moves through the system for each flagged feature.

### Data Flow Template

```
Feature: [PLACEHOLDER — Feature name]
Trigger: [PLACEHOLDER — What user action or event initiates the flow]
Source: [PLACEHOLDER — Where the data originates, e.g., User input, Third-party API, Database]
Destination: [PLACEHOLDER — Where the data goes, e.g., Database, External API, File system, Email]
Data Types: [PLACEHOLDER — What types of data are involved]
Transformations: [PLACEHOLDER — What processing occurs in transit, e.g., Validation, Encoding, Encryption]
Storage: [PLACEHOLDER — Where data is persisted, if at all]
Retention: [PLACEHOLDER — How long data is retained]
```

### Data Flow Notes

[PLACEHOLDER — Record any observations about data flows that raise security questions, e.g., "User-supplied data appears to flow directly into an SQL query without an obvious ORM layer mentioned."]

---

## Step 3: Trust Boundaries

Identify where data or control crosses a trust boundary — points where the risk profile changes.

### Trust Boundary Map

| Boundary ID | From (Lower Trust) | To (Higher Trust) | Data Crossing | Authentication at Boundary | Notes |
|-------------|-------------------|-------------------|---------------|---------------------------|-------|
| TB-001 | [e.g., Public Internet] | [e.g., Application Server] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| TB-002 | [e.g., Application Server] | [e.g., Database] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| TB-003 | [e.g., Application Server] | [e.g., Third-party API] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| TB-004 | [e.g., Standard User] | [e.g., Admin Function] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

### Trust Boundary Observations

[PLACEHOLDER — Note any trust boundary crossings that lack documented authentication, authorization checks, or validation steps.]

---

## Step 4: Threat Surface Notes

Based on the feature inventory, data flows, and trust boundaries, note potential threat scenarios.

**Note:** These are not findings — they are observations to inform audit focus. Do not label these as findings without evidence.

### Threat Surface Observations

| Feature | Observation | Threat Scenario | Audit Domain to Cover | Priority |
|---------|------------|----------------|----------------------|---------|
| [PLACEHOLDER] | [PLACEHOLDER — e.g., "File upload with no documented MIME type validation"] | [PLACEHOLDER — e.g., Malicious file upload, stored XSS"] | [e.g., Input Validation] | [High/Medium/Low] |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

### Implicit Security Requirements

Requirements that should be present based on the features described, even if not explicitly stated in the PRD:

- [PLACEHOLDER — e.g., "Password reset tokens must be single-use and time-limited"]
- [PLACEHOLDER — e.g., "File uploads must be scanned for malware before storage"]
- [PLACEHOLDER — e.g., "Admin actions must be logged with user identity and timestamp"]
- [PLACEHOLDER — e.g., "Exported data must be scoped to the requesting user's permissions"]

---

## Step 5: Audit Prioritization

Based on the PRD analysis, record which audit domains deserve the most focus for this engagement:

| Priority | Audit Domain | Reason |
|----------|-------------|--------|
| 1 | [PLACEHOLDER] | [PLACEHOLDER] |
| 2 | [PLACEHOLDER] | [PLACEHOLDER] |
| 3 | [PLACEHOLDER] | [PLACEHOLDER] |
| 4 | [PLACEHOLDER] | [PLACEHOLDER] |
| 5 | [PLACEHOLDER] | [PLACEHOLDER] |

---

## PRD Analysis Notes

[PLACEHOLDER — Free-form notes from reviewing the PRD. Record anything that doesn't fit the structured sections above.]

---

*Last updated: [PLACEHOLDER — Date]*
*PRD Version Reviewed: [PLACEHOLDER]*
*Analyst: [PLACEHOLDER]*
