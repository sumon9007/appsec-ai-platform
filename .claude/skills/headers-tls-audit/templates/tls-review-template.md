# TLS Configuration Review Template

Documents the TLS/SSL configuration assessment for the target application.

**Auditor:** [PLACEHOLDER]
**Date:** [PLACEHOLDER]
**Target Domain:** [PLACEHOLDER]
**Review Method:** [PLACEHOLDER — e.g., SSL Labs scan, manual curl, browser DevTools]

---

## TLS Protocol Support

| Protocol | Supported? | Assessment |
|----------|-----------|------------|
| TLS 1.3 | [Yes / No / Unknown] | [Recommended — best] |
| TLS 1.2 | [Yes / No / Unknown] | [Required minimum] |
| TLS 1.1 | [Yes / No / Unknown] | [Should be DISABLED — Medium finding] |
| TLS 1.0 | [Yes / No / Unknown] | [Should be DISABLED — Medium/High finding] |
| SSL 3.0 | [Yes / No / Unknown] | [Must be DISABLED — Critical finding] |
| SSL 2.0 | [Yes / No / Unknown] | [Must be DISABLED — Critical finding] |

**Protocol Assessment:** [PASS / FAIL — if TLS 1.1 or earlier is supported]
**Finding ID (if any):** [FIND-NNN or —]

---

## Cipher Suite Assessment

### Preferred / Recommended Ciphers

| Cipher Suite | Supported? | Notes |
|-------------|-----------|-------|
| TLS_AES_256_GCM_SHA384 (TLS 1.3) | [Yes / No / Unknown] | TLS 1.3 preferred |
| TLS_CHACHA20_POLY1305_SHA256 (TLS 1.3) | [Yes / No / Unknown] | TLS 1.3 preferred |
| ECDHE-RSA-AES256-GCM-SHA384 | [Yes / No / Unknown] | TLS 1.2 preferred |
| ECDHE-RSA-AES128-GCM-SHA256 | [Yes / No / Unknown] | TLS 1.2 preferred |

### Weak / Prohibited Ciphers (Should Be Disabled)

| Cipher | Supported? | Severity if Enabled |
|--------|-----------|---------------------|
| RC4 (any) | [Yes / No / Unknown] | High |
| DES | [Yes / No / Unknown] | High |
| 3DES | [Yes / No / Unknown] | Medium |
| NULL cipher (no encryption) | [Yes / No / Unknown] | Critical |
| EXPORT cipher suites | [Yes / No / Unknown] | High |
| ANON cipher suites (no authentication) | [Yes / No / Unknown] | Critical |
| MD5 HMAC | [Yes / No / Unknown] | High |

**Forward Secrecy:** [Supported / Not supported] — ECDHE or DHE key exchange in use?
**Cipher Assessment:** [PASS / FAIL]
**Finding ID (if any):** [FIND-NNN or —]

---

## Certificate Details

| Field | Value | Assessment |
|-------|-------|------------|
| **Domain** | [PLACEHOLDER] | |
| **Subject / Common Name (CN)** | [PLACEHOLDER] | Matches target domain? [Yes / No] |
| **Subject Alternative Names (SAN)** | [PLACEHOLDER — list all SANs] | Appropriate? [Yes / No] |
| **Issuer** | [PLACEHOLDER — e.g., Let's Encrypt R3, DigiCert] | Trusted CA? [Yes / No] |
| **Certificate Type** | [PLACEHOLDER — DV / OV / EV] | |
| **Valid From** | [YYYY-MM-DD] | |
| **Valid Until** | [YYYY-MM-DD] | |
| **Days Until Expiry** | [N days] | See threshold assessment below |
| **Signature Algorithm** | [PLACEHOLDER — e.g., SHA256withRSA] | SHA-256+ required |
| **Public Key Algorithm** | [PLACEHOLDER — e.g., RSA 2048, ECDSA P-256] | |
| **Key Length** | [PLACEHOLDER — e.g., 2048 bits] | RSA 2048+ or ECDSA 256+ |
| **Certificate Transparency (CT)** | [Logged / Not logged / Unknown] | |

### Certificate Expiry Assessment

| Days Until Expiry | Severity | Action Required |
|-------------------|----------|-----------------|
| Expired | Critical | Renew immediately — site is broken or producing errors |
| 0–7 days | Critical | Renew within 24 hours |
| 8–30 days | High | Schedule renewal urgently this week |
| 31–90 days | Medium | Plan renewal — do not let it lapse |
| > 90 days | OK | No action required |

**Days Until Expiry:** [N]
**Certificate Assessment:** [PASS / FAIL]
**Finding ID (if any):** [FIND-NNN or —]

---

## Certificate Chain

| Check | Status | Notes |
|-------|--------|-------|
| Full certificate chain served (intermediates included) | [Yes / No / Unknown] | |
| Root certificate from a trusted public CA | [Yes / No] | |
| No self-signed certificate in production | [Yes / No] | |
| Chain is ordered correctly | [Yes / No / Unknown] | |

**Chain Assessment:** [PASS / FAIL]

---

## HSTS Preload Status

| Check | Status |
|-------|--------|
| Domain on HSTS preload list | [Yes / No / Pending] |
| HSTS header qualifies for preload | [Yes / No — see headers-checklist.md] |

**Preload URL:** https://hstspreload.org/?domain=[TARGET DOMAIN]

---

## Mixed Content Check

| Check | Status | Notes |
|-------|--------|-------|
| No HTTP resources loaded on HTTPS pages | [PASS / FAIL / UNKNOWN] | [Note any HTTP resources found] |
| No mixed content warnings in browser console | [PASS / FAIL / UNKNOWN] | |
| Upgrade-Insecure-Requests header in use | [Yes / No] | |

**Finding ID (if any):** [FIND-NNN or —]

---

## TLS Assessment — SSL Labs Grade (if available)

| Field | Value |
|-------|-------|
| SSL Labs Grade | [PLACEHOLDER — e.g., A+ / A / B / C / F] |
| Scan Date | [PLACEHOLDER] |
| Scan URL | [PLACEHOLDER] |
| Key findings from SSL Labs | [PLACEHOLDER] |

Evidence: [EVID-YYYY-MM-DD-NNN — SSL Labs screenshot/export]

---

## TLS Review Summary

| Area | Assessment | Finding ID |
|------|-----------|------------|
| Protocol versions | [PASS / FAIL] | [FIND-NNN or —] |
| Cipher suites | [PASS / FAIL] | [FIND-NNN or —] |
| Certificate validity | [PASS / FAIL] | [FIND-NNN or —] |
| Certificate chain | [PASS / FAIL] | [FIND-NNN or —] |
| HSTS preload | [PASS / NOT PRELOADED] | [FIND-NNN or —] |
| Mixed content | [PASS / FAIL] | [FIND-NNN or —] |

---

*Template: tls-review-template.md*
