# Severity Rating Rules

Defines the criteria for rating the severity of security findings. All findings must be rated using these definitions. No other severity labels are permitted.

---

## Severity Levels

### Critical

**Definition:** Immediate exploitation risk. Data breach, full system compromise, remote code execution, or equivalent catastrophic impact is possible without requiring special conditions or user interaction.

**Characteristics:**
- Exploitation is straightforward (no special privileges required, no user interaction needed)
- Impact is catastrophic (data breach of sensitive data, full account compromise, remote code execution)
- No mitigating controls significantly reduce the risk
- Actively exploited in the wild (CISA KEV) — automatically Critical regardless of CVSS

**Examples:**
- SQL injection allowing unauthenticated access to the entire database
- Authentication bypass allowing any user to access any account
- Remote code execution via a known vulnerability in a public-facing component
- Hardcoded administrative credentials in a publicly accessible admin panel
- JWT accepting `alg: none` — token forgery trivially possible

**Response Required:** Immediate — notify stakeholders, consider disabling affected feature, patch within 24 hours.

**CVSS Guidance:** CVSS v3 ≥ 9.0 is typically Critical. A CVSS 9.0+ score is automatically rated Critical unless significant environmental factors substantially reduce risk (document the override reason).

---

### High

**Definition:** Significant security control failure. Exploitation is likely with limited effort. Impact is substantial — significant data exposure, account takeover, or privilege escalation is achievable.

**Characteristics:**
- Exploitation requires limited conditions (authenticated user, specific configuration) but is still straightforward
- Impact affects confidentiality, integrity, or availability in a meaningful way
- May require some user interaction or a specific state but is practically exploitable

**Examples:**
- IDOR allowing authenticated users to access other users' data
- Missing MFA on admin accounts accessible from the internet
- Stored XSS in a user-facing feature without CSP mitigation
- Known CVE (CVSS 7.0–8.9) in a directly used, publicly exposed dependency
- Session tokens not invalidated on logout
- Vertical privilege escalation (standard user accessing admin functions)

**Response Required:** Fix within 7 days. Escalate to development manager. May block release gate.

**CVSS Guidance:** CVSS v3 7.0–8.9 is typically High.

---

### Medium

**Definition:** Meaningful security weakness. Exploitation requires specific conditions, additional steps, or user interaction. Impact is moderate — partial data exposure, limited account risk, or requires chaining with other vulnerabilities.

**Characteristics:**
- Exploitation is possible but requires specific preconditions or user interaction
- Impact is limited in scope or requires additional conditions to be significant
- Often a control gap that increases risk rather than a direct exploitable vulnerability

**Examples:**
- Reflected XSS requiring significant user interaction (e.g., must click a crafted link)
- Missing Content-Security-Policy (increases impact of XSS but not directly exploitable)
- TLS 1.1 or 1.0 supported (deprecated protocol, requires network position)
- Missing rate limiting on a non-authentication endpoint
- Weak password policy not meeting NIST recommendations
- Verbose error messages exposing framework version
- Known CVE (CVSS 4.0–6.9) in a dependency

**Response Required:** Fix within 30 days. Track in findings register.

**CVSS Guidance:** CVSS v3 4.0–6.9 is typically Medium.

---

### Low

**Definition:** Minor issue with limited direct impact. May contribute to a multi-step attack chain or represents a best-practice deviation with low standalone risk.

**Characteristics:**
- Standalone exploitability is minimal
- Impact is limited or highly conditional
- May enable or facilitate other attacks if chained

**Examples:**
- Missing Referrer-Policy (low risk for this specific application)
- Missing Permissions-Policy
- Information disclosure of non-sensitive technology details (e.g., `X-Powered-By: Express`)
- Session timeout set to longer than recommended but not critically long
- Cookie missing `SameSite` attribute (browser default behavior applies)
- Abandoned package with no known CVE
- Known CVE (CVSS < 4.0) in a dependency

**Response Required:** Fix within 90 days. Include in next security improvement cycle.

**CVSS Guidance:** CVSS v3 0.1–3.9 is typically Low.

---

### Info

**Definition:** Observation of interest with no direct security risk. May indicate an area worth monitoring, a control gap of no immediate consequence, or a security improvement opportunity.

**Characteristics:**
- No exploitable vulnerability identified
- Risk is theoretical or negligible
- Represents a hardening opportunity or operational note

**Examples:**
- Security headers present but could be strengthened
- HSTS not on preload list (but HSTS is present)
- API documentation accessible without authentication but containing no sensitive information
- Use of a library that is approaching end-of-life but currently maintained and without CVEs
- Observation that logging is adequate but structured logging would improve SIEM integration

**Response Required:** Review at next audit cycle. No immediate action required.

---

## Severity Override Rules

### Automatic Escalation

Escalate severity one level above CVSS guidance when:
- The vulnerability has a known public exploit (PoC or weaponized)
- The vulnerability is listed in the CISA Known Exploited Vulnerabilities (KEV) catalog
- The application handles particularly sensitive data (financial, health, government classified)
- The finding represents a regression (previously fixed and now reintroduced)

### Automatic Downgrade

Downgrade severity one level below CVSS guidance when:
- A compensating control effectively mitigates the risk (WAF rule, network isolation, feature disable)
- The vulnerable code path is demonstrably not reachable in this application
- Exploitation requires physical access and this is not a relevant threat model

**Always document the reason for any override in the finding's notes.**

---

## CVSS Guidance Summary

| CVSS v3 Score | Default Severity | Override Possible? |
|---------------|-----------------|-------------------|
| 9.0 – 10.0 | Critical | Yes, with documented justification |
| 7.0 – 8.9 | High | Yes, with documented justification |
| 4.0 – 6.9 | Medium | Yes, with documented justification |
| 0.1 – 3.9 | Low | Yes, with documented justification |
| 0.0 | Info | — |

CVSS scores are a guide, not a mandate. The auditor's judgment, informed by the application context, threat model, and exploitability, takes precedence over CVSS score alone.
