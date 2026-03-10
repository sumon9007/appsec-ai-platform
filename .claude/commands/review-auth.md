# Command: /review-auth

Focused review of authentication and access control. Loads the auth-access-audit skill and guides through a complete authentication mechanism review.

## Trigger

Invoked when the user wants to perform a targeted review of authentication controls. Can be run standalone or as part of a broader audit workflow.

---

## Pre-Conditions

1. `.claude/context/audit-context.md` is populated and Authorization Status is **CONFIRMED**
2. `.claude/context/scope.md` defines which auth endpoints and flows are in scope

---

## Steps

### Step 1: Context Load

1. Read `.claude/context/audit-context.md` — confirm authorization
2. Read `.claude/context/scope.md` — note which auth flows are in scope
3. Read `.claude/context/target-profile.md` — note auth mechanism, identity provider, MFA status
4. Read `.claude/rules/safety-authorization-rules.md` — confirm passive review mode unless active testing authorized

### Step 2: Load Skill

Load: `.claude/skills/auth-access-audit/SKILL.md`

Read:
- `.claude/skills/auth-access-audit/templates/auth-checklist.md`
- `.claude/skills/auth-access-audit/templates/auth-findings-template.md`

### Step 3: Authentication Mechanism Review

Using `auth-checklist.md`, work through each control:

#### Login Mechanism
- What authentication method is in use? (Username/password, SSO, OAuth, SAML)
- Is HTTPS enforced on the login form and endpoint?
- Are error messages differential (do they reveal whether username vs. password is wrong)?
- Is there evidence of rate limiting on the login endpoint?
- Is brute force protection in place (lockout, CAPTCHA, progressive delay)?

#### Password Policy
- What is the minimum password length?
- Is there complexity enforcement?
- Is there breach-checking against known leaked password lists (e.g., HaveIBeenPwned)?
- Are there restrictions on password reuse?
- What is the password expiry policy?

#### Multi-Factor Authentication (MFA)
- Is MFA available to users?
- Is MFA enforced for privileged or admin accounts?
- What MFA methods are supported? (TOTP, SMS, push, hardware key)
- Can MFA be bypassed or disabled by the user without re-authentication?

#### Account Lockout
- After how many failed attempts is an account locked?
- What is the lockout duration?
- Can locked accounts be unlocked without additional verification?
- Is there logging of lockout events?

#### Password Reset Flow
- How is identity verified during reset? (Email link, SMS code, security questions)
- Are reset tokens single-use?
- Do reset tokens expire, and within what timeframe?
- Are prior sessions invalidated after a password reset?
- Does the reset flow reveal whether an email address is registered (enumeration)?

#### OAuth / SSO Configuration (if applicable)
- Is the OAuth `state` parameter in use to prevent CSRF?
- Is the redirect URI validated against a strict allowlist?
- Is the identity provider's token validated properly?
- Are OAuth tokens stored securely (not in localStorage without additional controls)?

#### Credential Storage Indicators
- Are there any observable indicators of how credentials are stored? (e.g., password hash in API response, timing differences suggesting bcrypt)
- Is any credential or token observable in URL parameters?

### Step 4: Document Findings

For each issue identified, complete `auth-findings-template.md`:

- Assign a Finding ID
- Rate severity per `.claude/rules/severity-rating-rules.md`
- Reference evidence items (EVID- convention)
- Include a specific recommendation

### Step 5: Session Initiation Review

- After authentication, is the session token or JWT newly generated? (No session fixation)
- Is the session token transmitted securely?
- Note session token characteristics for the session-jwt-audit review

---

## Outputs

| Output | Location | Template |
|--------|----------|---------|
| Authentication findings | `audit-runs/active/` or findings register | `auth-findings-template.md` |
| Auth checklist record | `audit-runs/active/` | `auth-checklist.md` |
| Evidence items | `evidence/raw/` | EVID- convention |

---

## Related Commands

- `/review-rbac` — Follow up with RBAC review after auth review
- `/review-auth` combines naturally with `/audit-website` step 3.2
