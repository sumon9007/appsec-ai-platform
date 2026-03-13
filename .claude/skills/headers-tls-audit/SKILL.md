> **Reference Guide** — This skill documents the methodology. For automated execution, run:
> `python scripts/run_audit.py audit headers   # and: audit tls`
> Use this skill to interpret tool output, conduct manual review steps, or guide authorized active testing.

# Skill: HTTP Security Headers and TLS Audit

## Purpose

Assess the HTTP response headers and TLS/SSL configuration of a web application to ensure browser-level security protections are in place and transport layer security meets current best practices.

---

## Inputs Required

| Input | Source | Required? |
|-------|--------|-----------|
| Target URL(s) | `.claude/context/scope.md` | Required |
| Authorization confirmation | `.claude/context/audit-context.md` | Required |
| CDN/WAF presence | `.claude/context/target-profile.md` | Important context |

---

## Method

### Phase 1: HTTP Response Header Collection

1. Make HTTP requests to the following to collect response headers:
   - Main application URL (authenticated and unauthenticated response)
   - Login page
   - A representative authenticated page or API endpoint
   - Static asset URL (if applicable — headers may differ)

2. Tools to use (in passive mode):
   - Browser DevTools → Network tab → select a request → Response Headers
   - `curl -I https://target.com` (prints response headers only)
   - `curl -si https://target.com | head -50`

3. Record headers for analysis in `headers-checklist.md`

### Phase 2: Security Header Assessment

Work through `headers-checklist.md` for each of the following:

**Content-Security-Policy (CSP)**
- Presence and enforcement mode
- `default-src` directive — is it restrictive?
- `script-src` — does it allow `unsafe-inline` or `unsafe-eval`? (Weakens XSS protection)
- `frame-ancestors` — is clickjacking protection in place via CSP?
- `report-uri` or `report-to` — is violation reporting configured?
- Assess overall CSP strength: Strong / Adequate / Weak / Missing

**Strict-Transport-Security (HSTS)**
- Is HSTS present?
- `max-age` value — recommended minimum: 15768000 (6 months)
- `includeSubDomains` — protects all subdomains
- `preload` — eligible for browser preload list?
- Is HSTS returned on the initial HTTP→HTTPS redirect?

**X-Content-Type-Options**
- Must be `nosniff` — binary: present/absent

**X-Frame-Options or CSP frame-ancestors**
- `X-Frame-Options: DENY` or `SAMEORIGIN`
- Or CSP `frame-ancestors 'none'` / `frame-ancestors 'self'`
- Both covering the same thing — either is acceptable

**Referrer-Policy**
- Recommended: `strict-origin-when-cross-origin` or stricter
- `unsafe-url` or absent: sensitive URL parameters may leak to third parties

**Permissions-Policy**
- Restricts access to sensitive browser APIs (camera, microphone, geolocation, payment, USB)
- Assess appropriateness for application type

**Cache-Control on Sensitive Responses**
- Authenticated pages: should include `no-store` or `Cache-Control: no-cache, no-store, must-revalidate`
- Are login pages, profile pages, or sensitive API responses cacheable?

**CORS Headers**
- `Access-Control-Allow-Origin` — is it `*` or restricted?
- `Access-Control-Allow-Credentials: true` with `*` = Critical finding
- Is the allowed origin list appropriate?

**Information-Exposing Headers (should be absent)**
- `X-Powered-By` — reveals technology stack
- `Server` (verbose) — reveals server version
- `X-AspNet-Version` / `X-AspNetMvc-Version`

### Phase 3: TLS Configuration Assessment

Using `tls-review-template.md`:

4. TLS Protocol Versions:
   - Supported protocols: TLS 1.3, TLS 1.2, TLS 1.1, TLS 1.0, SSLv3
   - Recommended: TLS 1.3 enabled, TLS 1.2 enabled, TLS 1.1/1.0/SSL disabled
   - TLS 1.0/1.1 enabled = Medium finding (may be High in regulated environments)

5. Cipher Suites:
   - Are weak ciphers enabled? (RC4, DES, 3DES, NULL, EXPORT)
   - Are forward secrecy ciphers preferred? (ECDHE-based)
   - Are AEAD ciphers in use? (AES-GCM, ChaCha20-Poly1305)

6. Certificate Assessment:
   - Issuer: is it a trusted public CA?
   - Common Name / Subject Alternative Names: does it match the target domain?
   - Validity period: start date and end date
   - Days to expiry: calculate and flag per severity thresholds
   - Signature algorithm: SHA-256 minimum (MD5/SHA-1 = Critical)
   - Certificate chain: are intermediates served?

7. HSTS Preload:
   - Is the domain listed at hstspreload.org?
   - If not, does the HSTS header qualify for preload?

8. Mixed Content:
   - Does the HTTPS application reference any HTTP resources?
   - Are there mixed content warnings in the browser console?

### Phase 4: Evidence Collection

9. Capture HTTP response headers as evidence (EVID- labeled)
10. Capture TLS configuration (SSL Labs report, or equivalent tool output) as evidence
11. Record certificate details as evidence

---

## Outputs

| Output | Template | Description |
|--------|---------|-------------|
| Headers checklist | `headers-checklist.md` | Per-header assessment |
| TLS review | `tls-review-template.md` | TLS configuration assessment |
| Findings | Standard finding format | One per missing/misconfigured header or TLS issue |
| Evidence items | EVID- convention | HTTP captures, tool outputs |

---

## Templates Used

- `.claude/skills/headers-tls-audit/templates/headers-checklist.md`
- `.claude/skills/headers-tls-audit/templates/tls-review-template.md`

---

## Useful Tools

- **SSL Labs** (ssllabs.com/ssltest) — comprehensive TLS analysis and grading
- **SecurityHeaders.com** — header analysis and grading
- **HSTS Preload** (hstspreload.org) — check HSTS preload status
- **curl** — direct header inspection from CLI
- **Browser DevTools** — request/response inspection

---

## References

- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- [OWASP TLS Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [MDN HTTP Headers Reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)
