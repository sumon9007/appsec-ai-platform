# Reporting Rules

These rules govern all reporting outputs produced by this workspace. Claude Code must comply with these rules when generating any report, summary, or finding document.

---

## Rule 1: Use Defined Severity Vocabulary Only

All findings must use exactly one of the following severity labels:

- **Critical**
- **High**
- **Medium**
- **Low**
- **Info**

**Prohibited labels (do not use):**
- Severe, Severe High, Informational, Notice, Warning, Important, Very High, Extreme, etc.

If any existing finding in the register uses a non-standard label, flag it for correction before generating a report.

---

## Rule 2: No Speculative Findings

**Every finding in a formal report must be based on observed evidence.**

Observations that cannot be confirmed with evidence must be labeled:
- `[UNKNOWN]` — if the condition could not be determined
- `[ASSUMED]` — if an assumption is being made that affects the finding
- `[UNCONFIRMED — REQUIRES EVIDENCE]` — if suspicion exists but evidence is not yet collected

Speculative statements such as "it is likely that..." or "this application probably..." are not acceptable in formal finding descriptions without an evidence basis.

---

## Rule 3: All Findings Must Have a Recommendation

**Every finding in a report must include at least one specific, actionable recommendation.**

Vague recommendations are not acceptable. Compare:

| Not Acceptable | Acceptable |
|---------------|-----------|
| "Fix the XSS vulnerability" | "Apply HTML encoding to all user-controlled values before rendering in HTML responses. Use the application framework's built-in output encoding functions rather than building custom sanitization." |
| "Update the dependency" | "Update lodash from version 4.17.15 to version 4.17.21 or later to remediate CVE-2021-23337." |
| "Improve authentication" | "Implement account lockout after 5 consecutive failed login attempts, with a 15-minute lockout period. Ensure the lockout response does not reveal whether the account exists." |

---

## Rule 4: Executive Summary Must Be Non-Technical

The executive summary is written for non-technical leadership. It must not contain:

- Raw HTTP request or response data
- Code snippets or stack traces
- CVE numbers (write "known vulnerable component" instead)
- Specific header names or values (write "missing transport security protection" instead)
- Technical tool output
- IP addresses or internal hostnames
- Database or framework-specific terminology

Verify the executive summary against these prohibited items before finalizing.

---

## Rule 5: Report Filename Convention

All reports must follow this naming convention:

```
YYYY-MM-DD-[type]-report.md
```

Examples:
- `2026-03-11-weekly-report.md`
- `2026-03-15-quarterly-technical-report.md`
- `2026-03-15-quarterly-executive-summary.md`
- `2026-03-20-v2.4.0-release-gate.md`

Files not following this convention will not be recognized as formal audit outputs.

---

## Rule 6: Report Version Labeling

All reports must include a version label:

- Draft reports: `DRAFT v0.x` (e.g., DRAFT v0.1, DRAFT v0.2)
- Final reports: `Final v1.0`

Reports without a version label are considered informal working documents.

---

## Rule 7: Evidence Reference in Technical Reports

Every finding in the technical report must include:
- At least one EVID-YYYY-MM-DD-NNN reference
- A brief description of what the evidence demonstrates

Findings without evidence references may not appear in the technical report.

---

## Rule 8: Findings Register as Ground Truth

The findings register is the single source of truth for all findings in an engagement.

- A finding closed in a report must also be closed in the findings register
- A finding severity changed in a report must be updated in the register
- The findings register must be updated at the end of every audit session
- Do not create findings in reports that are not also in the findings register

---

## Rule 9: No Duplicate Finding IDs

Each finding ID (FIND-NNN) must be unique within an engagement. Do not:
- Reuse a finding ID after a finding is closed
- Assign the same ID to two different findings
- Skip or skip-number finding IDs (they should be sequential)

---

## Rule 10: Overall Posture Statement Required

Every formal report (technical or executive) must include an overall security posture statement. This is a single sentence summarizing the current security state of the application.

Examples:
- "The application maintains a strong security baseline with no Critical findings and consistent remediation of High severity issues."
- "The application has significant access control weaknesses that require immediate attention before further production operation."
- "Security posture has improved since the prior quarter, with all High findings from Q4 remediated, though new Medium findings in the dependency domain require attention."
