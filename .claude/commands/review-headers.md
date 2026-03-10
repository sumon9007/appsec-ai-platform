# Command: /review-headers

Focused review of HTTP security headers, TLS configuration, and certificate validity. Loads the headers-tls-audit skill and produces a complete headers and transport security assessment.

## Trigger

Invoked when the user wants to review HTTP security headers and TLS configuration. Can be run standalone, as part of `/audit-weekly`, or as part of any broader audit.

---

## Pre-Conditions

1. `.claude/context/audit-context.md` is populated and Authorization Status is **CONFIRMED**
2. Target URL(s) are defined in `.claude/context/scope.md`

---

## Steps

### Step 1: Context Load

1. Read `.claude/context/audit-context.md` — confirm authorization
2. Read `.claude/context/scope.md` — note in-scope URLs to test
3. Read `.claude/context/target-profile.md` — note CDN or WAF presence (may affect observed headers)

### Step 2: Load Skill

Load: `.claude/skills/headers-tls-audit/SKILL.md`

Read:
- `.claude/skills/headers-tls-audit/templates/headers-checklist.md`
- `.claude/skills/headers-tls-audit/templates/tls-review-template.md`

### Step 3: HTTP Security Headers Review

Using `headers-checklist.md`, assess each security header:

#### Content-Security-Policy (CSP)
- Is CSP present?
- Does the policy use `default-src 'self'` or equivalent restrictive base?
- Does the policy avoid `unsafe-inline` and `unsafe-eval` in script-src?
- Is there a `report-uri` or `report-to` directive for violation reporting?
- Is the policy in enforcement mode (`Content-Security-Policy`) or report-only mode (`Content-Security-Policy-Report-Only`)?
- Assessment: Strong / Adequate / Weak / Missing

#### Strict-Transport-Security (HSTS)
- Is HSTS present?
- What is the `max-age` value? (Recommended: ≥ 15768000 / 6 months)
- Are `includeSubDomains` and `preload` directives present?
- Assessment: Strong / Adequate / Weak / Missing

#### X-Content-Type-Options
- Is the header present with value `nosniff`?

#### X-Frame-Options / CSP frame-ancestors
- Is X-Frame-Options present with `DENY` or `SAMEORIGIN`?
- Alternatively, is CSP `frame-ancestors` directive in use?
- Assessment: Protected / Vulnerable to Clickjacking

#### Referrer-Policy
- Is Referrer-Policy present?
- What is the value? (Recommended: `strict-origin-when-cross-origin` or stricter)
- Could the current policy leak sensitive URL parameters to third parties?

#### Permissions-Policy (Feature-Policy)
- Is Permissions-Policy present?
- Does it restrict access to sensitive browser features (camera, microphone, geolocation) appropriately?

#### Cache-Control
- For authenticated or sensitive responses: is caching disabled? (`no-store`, `no-cache`)
- Are there responses that should not be cached but are?

#### CORS (Cross-Origin Resource Sharing)
- What is the `Access-Control-Allow-Origin` value?
- Is `Access-Control-Allow-Credentials: true` combined with a wildcard or overly broad origin? (Critical if so)
- Is the origin allowlist restrictive?

#### Additional Headers to Check
- `X-Powered-By` — Should be absent (reveals server technology)
- `Server` — Should be absent or generic (reveals server version)
- `X-AspNet-Version` / `X-AspNetMvc-Version` — Should be absent

### Step 4: TLS Review

Using `tls-review-template.md`:

#### Protocol Version
- What TLS versions are supported? (TLS 1.3 recommended; TLS 1.2 acceptable; TLS 1.0/1.1 should be disabled)
- Is SSLv3 disabled?

#### Cipher Suites
- Are weak cipher suites disabled? (RC4, DES, 3DES, NULL, EXPORT ciphers)
- Are forward-secrecy cipher suites preferred? (ECDHE key exchange)
- Are insecure renegotiation configurations present?

#### Certificate
- Who issued the certificate? (Trusted CA?)
- What is the certificate validity period start and end date?
- How many days until expiry?
  - < 7 days: Critical — immediate renewal required
  - 8–30 days: High — schedule renewal urgently
  - 31–90 days: Medium — plan renewal
  - > 90 days: OK
- Is the certificate for the correct domain? (No mismatched CN or SAN)
- Is the full certificate chain provided? (Intermediate certificates included)

#### HSTS Preload
- Is the domain on the HSTS preload list?
- Is the preload directive present in the HSTS header?

#### Mixed Content
- Does the application load any HTTP resources from an HTTPS page?
- Are there mixed content warnings observable?

### Step 5: Document Findings

For each missing or misconfigured header or TLS issue:
- Record in findings register
- Assign Finding ID
- Rate severity per `.claude/rules/severity-rating-rules.md`
- Reference evidence items (HTTP response captures, EVID- labeled)

---

## Outputs

| Output | Location | Template |
|--------|----------|---------|
| Headers checklist | `audit-runs/active/` | `headers-checklist.md` |
| TLS review | `audit-runs/active/` | `tls-review-template.md` |
| Findings | Findings register | Standard finding format |
| Evidence items | `evidence/raw/` | EVID- convention |

---

## Tools Commonly Used for This Review

- Browser DevTools (Network tab) — inspect headers and certificate
- `curl -I https://target.com` — request headers inspection
- SSL Labs (ssllabs.com/ssltest) — comprehensive TLS grading
- SecurityHeaders.com — header assessment
- HSTS Preload (hstspreload.org) — preload status check
