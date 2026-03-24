# Audit Tool Requirements — Step-by-Step Guide

What each audit tool needs to produce output, how to run it, and what it produces.

---

## Prerequisites for Every Tool

These steps must be completed before running any tool. Nothing works without them.

### Step 1 — Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 2 — Create and activate an engagement

```bash
cp -r engagements/_template engagements/AUDIT-YYYY-CLIENT-NNN
```

Edit `.env`:

```
ACTIVE_ENGAGEMENT=AUDIT-YYYY-CLIENT-NNN
AUDIT_DEFAULT_AUDITOR=Your Name
```

### Step 3 — Confirm authorization

Open `engagements/<ENGAGEMENT_ID>/context/audit-context.md` and set:

```
Authorization Status: CONFIRMED
Authorizing Party: [name and title]
Authorization Date: [YYYY-MM-DD]
Authorization Reference: [email / ticket / signed scope]
Testing Mode: Passive Only
```

The platform refuses to run if `Authorization Status` is anything other than `CONFIRMED`.

### Step 4 — Define scope

Open `engagements/<ENGAGEMENT_ID>/context/scope.md` and list the in-scope URLs. Every tool resolves its targets from this file (or from `--url` on the CLI).

### Step 5 — Verify the setup

```bash
python scripts/run_audit.py session status
```

Expected output: audit ID, auditor name, authorization status `CONFIRMED`, list of in-scope URLs. Fix any gaps before running tools.

---

## Tool-by-Tool Requirements

---

### `headers`

**What it checks:** Presence and correctness of HTTP security response headers:
`Strict-Transport-Security`, `Content-Security-Policy`, `X-Frame-Options`,
`X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, `Cache-Control`.

**What it needs:**
- In-scope target URL (from scope.md or `--url`)
- Network access to the target (outbound HTTP/HTTPS)
- No auth required — passive, unauthenticated requests only

**How to run:**

```bash
python scripts/run_audit.py audit headers
# or target a specific URL:
python scripts/run_audit.py audit headers --url https://target.example.com
```

**What it produces:**
- One finding per missing or misconfigured header
- Findings written to `engagements/<ID>/audit-runs/active/findings-register.md`
- Evidence labels (`EVID-YYYY-MM-DD-NNN`) embedded in each finding

---

### `tls`

**What it checks:** TLS protocol version support, certificate validity, cipher suite strength,
HSTS preload status, certificate expiry.

**What it needs:**
- Target URL (HTTPS endpoint — HTTP targets produce a review gap, not a TLS result)
- Network access to the target on port 443
- No auth required

**How to run:**

```bash
python scripts/run_audit.py audit tls
# or:
python scripts/run_audit.py audit tls --url https://target.example.com
```

**What it produces:**
- Findings for deprecated TLS versions (TLS 1.0/1.1), weak ciphers, expired/self-signed certs, missing HSTS
- Review gaps where active TLS probing would be required (cipher enumeration requires active tooling)

---

### `cookies`

**What it checks:** `Set-Cookie` response headers for security attributes:
`Secure`, `HttpOnly`, `SameSite`, `Path`, `Domain` scope.

**What it needs:**
- Target URL
- Network access
- The tool makes a standard GET request and inspects cookies in the response. It does not require authentication to capture cookies set on the login page or public pages, but will miss cookies only set after login.

**How to run:**

```bash
python scripts/run_audit.py audit cookies --url https://target.example.com
# or via full audit:
python scripts/run_audit.py audit full --tools cookies
```

**What it produces:**
- Finding per missing attribute (e.g. `Secure` flag absent, `SameSite` not set)
- Review gap noted for cookies only observable in authenticated sessions

---

### `session`

**What it checks:** Session token handling — JWT structure and algorithm, token length/entropy,
session-related response headers, evidence of insecure token transmission.

**What it needs:**
- Target URL
- Network access
- For JWT analysis: a JWT must be observable in response headers or body from the unauthenticated endpoint. If JWTs are only issued after login, the tool will produce review gaps for those checks and passive findings for anything observable without auth.
- To supply a known JWT for analysis: pass it as `--token <jwt>` if supported, or embed in the session context.

**How to run:**

```bash
python scripts/run_audit.py audit session --url https://target.example.com
# or via full audit:
python scripts/run_audit.py audit full --tools session
```

**What it produces:**
- Findings for weak JWT algorithms (`alg: none`, `HS256` on public endpoints), long session timeouts, missing token rotation signals
- Review gaps for checks that require an authenticated session token

---

### `misconfig`

**What it checks:** Security misconfiguration indicators — directory listing, debug/stack
traces in responses, admin interfaces accessible without auth, default credentials hints,
CORS misconfiguration, error page information disclosure.

**What it needs:**
- Target URL
- Network access
- Passive only — makes standard requests to known probe paths (e.g. `/admin`, `/.env`, `/api/debug`)

**How to run:**

```bash
python scripts/run_audit.py audit misconfig --url https://target.example.com
# or via full audit:
python scripts/run_audit.py audit full --tools misconfig
```

**What it produces:**
- Confirmed findings where misconfig indicators are directly observable in responses
- Review gaps for checks that would require authenticated access or active probing

---

### `auth`

**What it checks:** Authentication control observations — login page presence, brute-force
protection signals, MFA indicators, account lockout behavior, credential exposure in responses.

**What it needs:**
- Target URL
- Network access
- Passive only by default — observes login form structure, response headers, and error message behavior without submitting credentials
- Active auth testing (lockout testing, credential stuffing checks) requires `Testing Mode: Active` in `audit-context.md` and is not currently executed automatically

**How to run:**

```bash
python scripts/run_audit.py audit full --tools auth --url https://target.example.com
```

> **Note:** There is no standalone `audit auth` command. Use `audit full --tools auth`.

**What it produces:**
- Passive findings for observable auth weaknesses (verbose error messages, no CAPTCHA signal, missing security headers on auth pages)
- Review gaps for controls that require authenticated interaction or active testing

---

### `rbac`

**What it checks:** Authorization and access control — enumerable object IDs in URLs,
role-boundary indicators, mass assignment patterns, admin function exposure.

**What it needs:**
- Target URL
- Network access
- Crawl data is beneficial: `crawl` should be run first (or included in the same `--tools` list) so the RBAC tool receives a list of discovered pages/endpoints to analyze
- Authenticated session (optional but needed for full role-aware analysis) — without it, the tool produces passive observations and review gaps

**How to run:**

```bash
# Recommended: run with crawl to feed page inventory
python scripts/run_audit.py audit full --tools crawl,rbac --url https://target.example.com
```

> **Note:** There is no standalone `audit rbac` command. Use `audit full --tools rbac`.

**What it produces:**
- Findings for observable IDOR patterns (sequential IDs in URLs, predictable object references)
- Review gaps for privilege escalation checks that require multi-role authenticated testing

---

### `input`

**What it checks:** Input validation surfaces — forms, query parameters, and API inputs
observable from crawled pages. Identifies potential injection vectors.

**What it needs:**
- Target URL
- Network access
- **Requires crawl data** — `input` tool receives `page_inventories` from the crawler. Without a prior crawl, it has no input surfaces to analyze and will produce only review gaps.
- Run `crawl` in the same session or before this tool

**How to run:**

```bash
# Must include crawl to get page inventory
python scripts/run_audit.py audit full --tools crawl,input --url https://target.example.com
```

> **Note:** There is no standalone `audit input` command. Use `audit full --tools input`.
> Active injection testing (SQL injection payloads, XSS probes) requires `Testing Mode: Active` authorization and is not executed in passive mode.

**What it produces:**
- Findings for observable input surfaces lacking client-side or server-side validation signals
- Review gaps for injection testing that requires active payload submission

---

### `crawl`

**What it checks:** Discovers pages, links, forms, and JavaScript references by following
links from the seed URL up to `AUDIT_MAX_CRAWL_PAGES` pages.

**What it needs:**
- Target URL
- Network access
- Optionally: `AUDIT_MAX_CRAWL_PAGES` in `.env` (default: 30)
- Passive only — follows only observable links, does not brute-force paths

**How to run:**

```bash
# Run alone or as part of full audit
python scripts/run_audit.py audit full --tools crawl --url https://target.example.com
# Or include with other tools (recommended — crawl feeds rbac and input):
python scripts/run_audit.py audit full --tools crawl,headers,cookies,rbac,input
```

**What it produces:**
- Internal page inventory used by `rbac` and `input` tools
- Crawl errors logged to the session record
- No direct findings — it is a data-gathering step that enriches downstream tools

---

### `dependencies`

**What it checks:** Known CVEs in declared project dependencies by querying the
[OSV.dev](https://api.osv.dev) vulnerability database.

**What it needs:**
- A **local dependency manifest file** — one of:
  - `requirements.txt` (Python)
  - `package.json` or `package-lock.json` (Node.js)
  - `Gemfile.lock` (Ruby)
  - `pom.xml` (Java/Maven)
  - `go.sum` (Go)
- Outbound internet access to `https://api.osv.dev`
- The target URL is not needed — this is a file-based, not network-based, tool

**How to set up:**

Option A — set in `.env`:
```
AUDIT_MANIFEST_PATH=/path/to/requirements.txt
```

Option B — pass on CLI:
```bash
python scripts/run_audit.py audit dependencies --manifest requirements.txt
```

**How to run:**

```bash
python scripts/run_audit.py audit dependencies --manifest requirements.txt
# or via full audit:
python scripts/run_audit.py audit full --manifest requirements.txt
# (dependencies is auto-added when --manifest is supplied)
```

**What it produces:**
- One finding per package with a known CVE, including CVSS score, severity, and fix version
- Info findings for packages that are outdated but have no known CVEs
- Review gaps for packages the OSV API cannot identify

---

### `api`

**What it checks:** API security controls observable from an OpenAPI or Postman spec —
unauthenticated endpoints, overly permissive CORS, missing rate limiting signals,
sensitive data in spec-defined responses, undocumented endpoints discovered during crawl.

**What it needs:**
- A **local API spec file** — one of:
  - `openapi.yaml` or `openapi.json` (OpenAPI 3.x)
  - `swagger.yaml` or `swagger.json` (Swagger 2.x)
  - Postman collection JSON
- Target URL (for live endpoint validation)
- Network access

**How to set up:**

Option A — set in `.env`:
```
AUDIT_SPEC_PATH=/path/to/openapi.yaml
```

Option B — pass on CLI:
```bash
python scripts/run_audit.py audit api --spec openapi.yaml --url https://api.example.com
```

**How to run:**

```bash
python scripts/run_audit.py audit api --spec openapi.yaml
# or via full audit:
python scripts/run_audit.py audit full --spec openapi.yaml
# (api is auto-added when --spec is supplied)
```

**What it produces:**
- Findings for unauthenticated endpoints, missing auth headers in spec, CORS issues
- Review gaps where live API testing requires authenticated requests or active probing
- If no spec is provided, only review gaps are produced

---

### `secrets`

**What it checks:** Hardcoded secrets in local source files — API keys, tokens, passwords,
private keys, connection strings, and other credential patterns.

**What it needs:**
- A **local directory or file path** to scan — typically the application source code
- No network access required — fully local/static analysis
- The target URL is not needed

**How to set up:**

Option A — set in `.env`:
```
AUDIT_SCAN_PATH=/path/to/source/code
```

Option B — pass on CLI:
```bash
python scripts/run_audit.py audit secrets --scan src/
```

**How to run:**

```bash
python scripts/run_audit.py audit secrets --scan src/
# or via full audit:
python scripts/run_audit.py audit full --scan src/
# (secrets is auto-added when --scan is supplied)
```

**What it produces:**
- Findings for detected secret patterns with file path and line reference
- Severity is raised to Critical/High for private keys and auth tokens
- Review gaps for obfuscated or encoded secrets that pattern matching cannot detect

> **Important:** If a real secret is found, do not store it in evidence files.
> Follow the stop condition in `.claude/rules/safety-authorization-rules.md`:
> document the location, redact the value, notify the authorizing party, and rotate immediately.

---

## Quick Reference — What Each Tool Needs

| Tool | Target URL | Network | Manifest | Spec File | Scan Path | Crawl Data |
|------|-----------|---------|----------|-----------|-----------|------------|
| `headers` | Required | Required | — | — | — | — |
| `tls` | Required (HTTPS) | Required | — | — | — | — |
| `cookies` | Required | Required | — | — | — | — |
| `session` | Required | Required | — | — | — | — |
| `misconfig` | Required | Required | — | — | — | — |
| `auth` | Required | Required | — | — | — | — |
| `rbac` | Required | Required | — | — | — | Beneficial |
| `input` | Required | Required | — | — | — | **Required** |
| `crawl` | Required | Required | — | — | — | N/A |
| `dependencies` | — | Required | **Required** | — | — | — |
| `api` | Required | Required | — | **Required** | — | — |
| `secrets` | — | — | — | — | **Required** | — |

---

## Running All Tools Together

### Full passive audit (URL-based tools only)

```bash
python scripts/run_audit.py audit full \
  --url https://target.example.com \
  --auditor "Your Name"
```

Runs: `headers`, `tls`, `cookies`, `session`, `misconfig`, `auth`, `rbac`, `input`, `crawl`

### Full audit including file-based tools

```bash
python scripts/run_audit.py audit full \
  --url https://target.example.com \
  --manifest requirements.txt \
  --spec openapi.yaml \
  --scan src/ \
  --auditor "Your Name"
```

Runs all 12 tools.

### Dry run (no findings written — useful for testing setup)

```bash
python scripts/run_audit.py audit full --dry-run --url https://target.example.com
```

---

## After the Audit — Generate Reports

Once findings are in the register:

```bash
# Technical report (for engineers)
python scripts/run_audit.py report technical

# Executive summary (for management)
python scripts/run_audit.py report executive

# Prioritized remediation plan
python scripts/run_audit.py report remediation
```

Reports are written to `engagements/<ENGAGEMENT_ID>/reports/draft/`.
