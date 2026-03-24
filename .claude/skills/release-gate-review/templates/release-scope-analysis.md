# Release Scope Analysis

Use this template at the start of a release gate review (Phase 2 of `release-gate-review` skill) to map the security risk of each change in the release.

---

## Release Metadata

```
Release Version:    [e.g., v2.4.0]
Release Date:       [YYYY-MM-DD]
Changelog Source:   [Link or reference to changelog / PR list / release notes]
Gate Session:       [SESSION-YYYY-MM-DD-NNN]
Reviewer:           [Auditor name]
```

---

## Change Inventory

Document every meaningful change in this release. Add rows as needed.

| # | Change Description | Type | Security Risk Level | Domains Affected |
|---|-------------------|------|--------------------|--------------------|
| 1 | [e.g., "Add OTP-based 2FA to login flow"] | New feature | High | Authentication, Session Management |
| 2 | [e.g., "Update lodash from 4.17.15 to 4.17.21"] | Dependency update | Medium | Dependencies |
| 3 | [e.g., "Fix typo in user dashboard label"] | Bug fix | None | — |
| 4 | | | | |
| 5 | | | | |

**Security Risk Levels:**
- **High** — directly touches auth, authz, session, input handling, or introduces new external attack surface
- **Medium** — dependency updates, infrastructure changes, or moderate-complexity features
- **Low** — refactoring, UI changes, or performance improvements with no security-relevant behavior change
- **None** — cosmetic, content, or documentation changes

---

## Domain Skill Selection

Based on the change inventory, check which domain skills are required for this gate review:

| Domain Skill | Required? | Reason |
|---|---|---|
| `headers-tls-audit` | Always yes | Verify no regression in header config |
| `auth-access-audit` | Always yes | Verify no regression in auth controls |
| `session-jwt-audit` | ☐ Yes / ☐ No | [Reason if yes] |
| `rbac-audit` | ☐ Yes / ☐ No | [Reason if yes] |
| `input-validation-audit` | ☐ Yes / ☐ No | [Reason if yes] |
| `dependency-audit` | ☐ Yes / ☐ No | [Reason if yes] |
| `security-misconfig-audit` | ☐ Yes / ☐ No | [Reason if yes] |
| `logging-monitoring-audit` | ☐ Yes / ☐ No | [Reason if yes] |

---

## New Attack Surface Introduced

List any new entry points, endpoints, or integrations added in this release:

| Surface | Type | Authentication Required? | Authorization Checked? | Input Validated? |
|---------|------|--------------------------|------------------------|-----------------|
| [e.g., /api/v2/export] | New API endpoint | Yes / No / Unknown | Yes / No / Unknown | Yes / No / Unknown |
| | | | | |

---

## New Dependencies Introduced

| Package | Version | CVE Status | Notes |
|---------|---------|-----------|-------|
| [package name] | [version] | No known CVEs / [CVE-YYYY-NNNNN] | [any notes] |
| | | | |

---

## Prior Findings Blocker Assessment

| Finding ID | Title | Severity | Status | Blocker? |
|-----------|-------|----------|--------|---------|
| FIND-NNN | [Title] | Critical/High | Open / Risk Accepted (expires YYYY-MM-DD) | Yes / No |
| | | | | |

**Automatic blocker conditions:**
- Any open Critical finding with no accepted risk → **Fail**
- Any Must-Fix item from this review unresolved → **Fail**

---

## Preliminary Gate Assessment

```
Changes reviewed:       [N total | N high-risk | N medium-risk | N low-risk | N none]
Domain skills required: [list]
New attack surface:     [None | Yes — [brief description]]
Prior finding blockers: [None | Yes — [FIND-NNN list]]

Preliminary gate status: LIKELY PASS / LIKELY CONDITIONAL PASS / LIKELY FAIL
Reason:                  [Brief explanation]
```

*Complete the formal gate decision in `.claude/templates/release-gate-template.md` after full review.*
