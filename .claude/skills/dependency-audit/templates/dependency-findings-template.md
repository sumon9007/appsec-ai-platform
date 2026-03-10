# Dependency Findings Template

Documents vulnerable dependencies identified during the dependency and supply chain audit.

**Auditor:** [PLACEHOLDER]
**Date:** [PLACEHOLDER]
**Target:** [PLACEHOLDER]
**Manifest(s) Reviewed:** [PLACEHOLDER — e.g., package.json, requirements.txt]

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Total direct dependencies reviewed | [N] |
| Total with known CVEs | [N] |
| Critical severity CVEs | [N] |
| High severity CVEs | [N] |
| Medium severity CVEs | [N] |
| Low severity CVEs | [N] |
| Abandoned packages (no release > 24 months) | [N] |
| Packages with no fix available | [N] |

---

## CVE Findings Table

| # | Package Name | Installed Version | CVE ID | CVSS Score | Severity | Fix Version | Fix Available? | Exploitability Notes |
|---|-------------|-------------------|--------|------------|----------|-------------|----------------|---------------------|
| 1 | [PLACEHOLDER — e.g., lodash] | [e.g., 4.17.15] | [e.g., CVE-2021-23337] | [e.g., 7.2] | High | [e.g., 4.17.21] | Yes | [e.g., Requires unsanitized input to chain function] |
| 2 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [Yes/No/Partial] | [PLACEHOLDER] |
| 3 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [Yes/No/Partial] | [PLACEHOLDER] |
| 4 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [Yes/No/Partial] | [PLACEHOLDER] |
| 5 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [Yes/No/Partial] | [PLACEHOLDER] |

---

## Critical CVE Details

For each Critical (CVSS ≥ 9.0) finding, complete the full detail:

### CVE Detail: [CVE-XXXX-XXXXX]

| Field | Value |
|-------|-------|
| **Package** | [PLACEHOLDER] |
| **Installed Version** | [PLACEHOLDER] |
| **CVE ID** | [PLACEHOLDER] |
| **CVSS v3 Score** | [PLACEHOLDER] |
| **CVSS v3 Vector** | [PLACEHOLDER — e.g., AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H] |
| **CWE** | [PLACEHOLDER — e.g., CWE-79: XSS] |
| **Vulnerability Type** | [PLACEHOLDER — e.g., Remote Code Execution / XSS / SQL Injection / Denial of Service] |
| **Affected Versions** | [PLACEHOLDER — e.g., < 4.17.21] |
| **Fix Version** | [PLACEHOLDER] |
| **Published Date** | [PLACEHOLDER] |
| **CISA KEV Listed** | [Yes / No] |

**Description:**
[PLACEHOLDER — Brief description of the vulnerability from the advisory.]

**Exploitability in this Application:**
[PLACEHOLDER — Is the affected code path used? Is the attack surface reachable? Any mitigating controls in the environment?]

**Recommendation:**
[PLACEHOLDER — e.g., "Update lodash to version 4.17.21 or later. Review any usage of the `merge`, `mergeWith`, `defaultsDeep`, and `zipObjectDeep` functions for untrusted input."]

**Evidence:**
- [EVID-YYYY-MM-DD-NNN — dependency manifest showing installed version]

**Finding ID:** [FIND-NNN]

---

## High CVE Details

### CVE Detail: [CVE-XXXX-XXXXX]

| Field | Value |
|-------|-------|
| **Package** | [PLACEHOLDER] |
| **Installed Version** | [PLACEHOLDER] |
| **CVE ID** | [PLACEHOLDER] |
| **CVSS v3 Score** | [PLACEHOLDER] |
| **Vulnerability Type** | [PLACEHOLDER] |
| **Affected Versions** | [PLACEHOLDER] |
| **Fix Version** | [PLACEHOLDER] |
| **Published Date** | [PLACEHOLDER] |

**Description:**
[PLACEHOLDER]

**Exploitability in this Application:**
[PLACEHOLDER]

**Recommendation:**
[PLACEHOLDER]

**Evidence:**
- [EVID-YYYY-MM-DD-NNN]

**Finding ID:** [FIND-NNN]

---

## Abandoned Packages

| Package | Last Release | Notes | Recommended Action |
|---------|-------------|-------|-------------------|
| [PLACEHOLDER] | [YYYY-MM-DD] | [e.g., No maintainer active, 23 open security issues] | [e.g., Replace with [alternative package]] |
| [PLACEHOLDER] | [YYYY-MM-DD] | [PLACEHOLDER] | [PLACEHOLDER] |

---

## Supply Chain Notes

[PLACEHOLDER — Document any supply chain concerns identified:]

- Packages pinned to mutable references: [PLACEHOLDER or None found]
- Non-standard registry packages: [PLACEHOLDER or None found]
- Packages with unusual install scripts: [PLACEHOLDER or None found]
- SBOM availability: [PLACEHOLDER — Yes / No / In progress]

---

## Prioritized Update Recommendations

| Priority | Package | Current Version | Recommended Version | Reason |
|----------|---------|-----------------|---------------------|--------|
| 1 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [Critical CVE: CVE-XXXX] |
| 2 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [High CVE: CVE-XXXX] |
| 3 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [Abandoned package] |

---

*Template: dependency-findings-template.md*
