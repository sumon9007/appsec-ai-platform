# Safety and Authorization Rules

These rules exist to ensure all audit activity is authorized, conducted safely, and handled appropriately when sensitive data is encountered. These are the highest-priority rules in this workspace — they override all other considerations.

---

## Rule 1: No Testing Without Confirmed Authorization

**No audit activity of any kind may begin until:**

1. `.claude/context/audit-context.md` is populated with:
   - An explicit Authorization Status of **CONFIRMED**
   - The name and title of the authorizing party
   - The date of authorization
   - A reference to the authorization document (email, ticket, signed scope agreement)

2. The scope defined in `.claude/context/scope.md` is agreed upon and matches the authorization

If Authorization Status is anything other than CONFIRMED, Claude Code must halt and display:

> **AUTHORIZATION REQUIRED:** Audit activity cannot begin until authorization is confirmed in `.claude/context/audit-context.md`. Please confirm written authorization from an authorized party before proceeding.

---

## Rule 2: Passive Review Only by Default

**The default mode of all audit activity is passive review.**

Passive review includes:
- Observing HTTP responses to normal application requests
- Analyzing response headers, cookies, and tokens from authenticated sessions
- Reviewing dependency manifests provided or observable
- Reviewing log samples provided by the client
- Reviewing configuration documentation provided by the client
- Making standard requests to the application as an authenticated user (using provided test accounts)

Passive review does not include:
- Submitting payloads designed to trigger injection vulnerabilities
- Attempting to access another user's data by modifying object references
- Brute-forcing credentials
- Fuzzing inputs
- Exploiting any discovered vulnerability to demonstrate impact

---

## Rule 3: Active Testing Requires Explicit Authorization

**Active security testing requires explicit, specific written authorization documented in `.claude/context/audit-context.md`.**

Active testing includes:
- Submitting injection test payloads (SQL, XSS, command injection, etc.)
- Testing IDOR by substituting other users' object IDs
- Testing authentication bypass by modifying requests
- Brute-force or fuzzing of any kind
- Exploiting any vulnerability to demonstrate impact
- Scanning tools (automated vulnerability scanners, DAST tools)

The authorization must specify:
- What type of active testing is permitted
- Which environment (staging, QA — production active testing requires exceptional authorization)
- Any specific restrictions (e.g., "active testing permitted but no exploit chains that would destroy data")

If active testing authorization is absent or ambiguous: **default to passive review only** and note the limitation in the audit session record.

---

## Rule 4: Mandatory Stop Conditions

Claude Code must immediately stop all audit activity and alert the user if any of the following are encountered:

### Unexpected Sensitive Data

If unexpected sensitive data is discovered that was not anticipated in the scope:
- Passwords or password hashes in plaintext
- Payment card numbers (PCI data)
- Health or medical records (PHI/HIPAA relevant data)
- Government identification numbers (SSN, passport numbers)
- Private encryption keys or certificates
- API keys, access tokens, or secrets belonging to third parties
- Evidence of prior unauthorized access or active breach

**Response:** Stop immediately. Document what was encountered (without storing the sensitive data itself). Alert the user. Seek guidance from the authorizing party before continuing.

### Evidence of Active Compromise

If evidence suggests the application is currently under active attack or has been compromised:
- Unexpected admin accounts created
- Files modified with unexpected timestamps
- Malware indicators in application responses
- Unexpected outbound connections observed

**Response:** Stop all testing. Alert the client immediately. Do not clean up or modify anything. Preserve evidence.

### Accidental Out-of-Scope Access

If audit activity accidentally accesses a system outside the defined scope:
- Stop the activity immediately
- Document what was accessed, when, and how
- Alert the user and the authorizing party
- Do not use any information obtained through the out-of-scope access

---

## Rule 5: Session Authorization Record

At the start of every audit session, record authorization status:

In `.claude/templates/audit-session-template.md`, complete the Authorization section:
- Authorization Status: [CONFIRMED]
- Authorizing Party: [NAME / TITLE]
- Authorization Reference: [REFERENCE]
- Testing Mode: [Passive Only / Passive + Active Testing on [ENVIRONMENT]]

This must be completed before any audit activity begins in that session.

---

## Rule 6: No Evidence Storage of Sensitive Secrets

If credentials, private keys, or other secrets are discovered as evidence:
- Do not store the full credential/key in evidence files
- Record the existence and location of the finding without storing the secret itself
- In reports, reference as "credentials observed in [location]" without reproducing them
- Notify the client immediately so they can rotate the exposed credential/key

---

## Rule 7: Data Handling Obligations

Audit findings, evidence, and reports may contain sensitive information about the client's systems and users. Handle accordingly:

- Do not share audit materials outside the authorized engagement parties
- Do not retain client-specific evidence beyond the agreed engagement period
- Follow any data handling agreements (DPA, NDA) established with the client
- When the engagement concludes, follow agreed procedures for evidence retention or destruction

---

## Rule 8: Communication in Ambiguous Situations

When encountering a situation not clearly covered by these rules or where safety/authorization is ambiguous:

1. Stop the activity in question
2. Document the situation in the audit session record
3. Present the situation to the user clearly
4. Wait for explicit guidance before continuing
5. Do not make assumptions about authorization — when in doubt, the answer is "stop and ask"
