# Audit Scope Rules

These rules govern the boundaries of testing activity. Claude Code must enforce these rules throughout every audit engagement.

---

## Rule 1: Scope Confirmation Before Starting

**Before beginning any audit activity, confirm that `.claude/context/scope.md` is populated with:**
- A clearly defined list of in-scope URLs, domains, and endpoints
- A clearly defined list of out-of-scope items
- An authorization status of CONFIRMED in `.claude/context/audit-context.md`

If either document is missing or incomplete, halt all audit activity and request that the user complete them before proceeding.

---

## Rule 2: Never Test Out-of-Scope Targets

**Under no circumstances may Claude Code initiate testing — passive or active — against targets not listed in the In-Scope section of `.claude/context/scope.md`.**

This includes:
- Subdomains not explicitly listed as in-scope
- Third-party services integrated with the application
- Other applications operated by the same organization but not listed in scope
- IP addresses outside the defined target range
- Internal network systems accessible from the application (SSRF vectors should be noted but not exploited)

---

## Rule 3: Out-of-Scope Issue Discovery

If an issue is discovered passively that relates to an out-of-scope target or system:

1. Note the observation with the label: `[OUT OF SCOPE — NOT TESTED]`
2. Do not investigate, probe, or test the out-of-scope element further
3. Record the observation in a separate section of the session notes under "Out-of-Scope Observations"
4. Inform the user that an out-of-scope issue was observed and recommend they separately engage appropriate parties

**Example:** If reviewing in-scope `app.example.com` and observing a reference to a third-party CDN with a potentially misconfigured endpoint, note it as `[OUT OF SCOPE — NOT TESTED: possible misconfiguration observed in CDN references — recommend separate review]` and stop.

---

## Rule 4: Scope Change Process

The scope may only be expanded during an engagement when:

1. The change is agreed in writing by the authorizing party (document reference required)
2. The change is recorded in `.claude/context/scope.md` under the Scope Change Log
3. Claude Code is explicitly told that the scope has changed and shown the updated document

Scope may never be expanded unilaterally by the auditor.

---

## Rule 5: Test Account Restrictions

When test accounts are provided:

- Only use test accounts explicitly provided for the engagement
- Do not use credentials of real users, even if discovered during the audit
- Do not create permanent test data that could affect real users
- Clean up or document any test data created during active testing

---

## Rule 6: Environment Restrictions

Unless explicitly stated otherwise in `.claude/context/scope.md`:

- Treat production environments as **passive review only** (no form submissions, no API calls with test payloads, no account creation)
- Active testing (form submissions, API calls, authentication tests) is only permitted on non-production environments (staging, QA)
- If both environments are in scope, document which activities were performed in each environment

---

## Rule 7: Scope Note Labeling

Use these standard labels when scope considerations affect finding documentation:

| Label | Usage |
|-------|-------|
| `[OUT OF SCOPE — NOT TESTED]` | Issue observed passively relating to an out-of-scope target |
| `[SCOPE LIMITED — PARTIAL ASSESSMENT]` | In-scope item that could only be partially assessed due to scope restrictions |
| `[ENVIRONMENT: STAGING]` | Finding observed on staging environment — may or may not apply to production |
| `[ENVIRONMENT: PRODUCTION]` | Finding observed on production |

---

## Violations

If a user instructs Claude Code to test beyond the defined scope, Claude Code must:

1. Decline the instruction
2. Explain that the target is outside the defined scope in `.claude/context/scope.md`
3. Offer to update the scope document if the user has authorization to expand scope
4. Document the request and refusal in the audit session record
