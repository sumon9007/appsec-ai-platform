# Command: /audit-website

Full security audit of a website or web application, covering all audit domains in sequence.

## Trigger

Invoked when the user wants a comprehensive security audit of a website or web application. This command orchestrates the full audit workflow from context loading through report generation.

---

## Pre-Conditions

Before execution, Claude Code must verify:

1. `.claude/context/audit-context.md` is populated and Authorization Status is **CONFIRMED**
2. `.claude/context/target-profile.md` is populated with target details
3. `.claude/context/scope.md` defines in-scope and out-of-scope targets
4. `.claude/context/assumptions.md` is reviewed and current

If any of the above are missing or incomplete, halt and prompt the user to complete them.

---

## Steps

### Step 1: Context Load

1. Read `.claude/context/audit-context.md` — confirm authorization status
2. Read `.claude/context/target-profile.md` — note tech stack, roles, integrations
3. Read `.claude/context/scope.md` — establish testing boundaries
4. Read `.claude/context/assumptions.md` — note any assumptions that will affect methodology
5. Read all files in `.claude/rules/` — internalize scope, evidence, severity, and safety rules
6. Create an audit session record using `.claude/templates/audit-session-template.md`
7. Save session record to `audit-runs/active/YYYY-MM-DD-full-website-session.md`

### Step 2: Load All Audit Skills

Load each skill's SKILL.md in sequence before beginning domain reviews:

1. `.claude/skills/auth-access-audit/SKILL.md`
2. `.claude/skills/rbac-audit/SKILL.md`
3. `.claude/skills/session-jwt-audit/SKILL.md`
4. `.claude/skills/input-validation-audit/SKILL.md`
5. `.claude/skills/headers-tls-audit/SKILL.md`
6. `.claude/skills/dependency-audit/SKILL.md`
7. `.claude/skills/logging-monitoring-audit/SKILL.md`
8. `.claude/skills/security-misconfig-audit/SKILL.md`

### Step 3: Domain Audits (Perform in Sequence)

For each domain below, follow the methodology defined in the skill, use the templates provided, and document all findings with evidence references.

#### 3.1 Security Headers & TLS (Quick Win — Start Here)

Skill: `.claude/skills/headers-tls-audit/`
Templates: `headers-checklist.md`, `tls-review-template.md`

- Check all HTTP response headers against the headers checklist
- Check TLS version, cipher suites, and certificate validity
- Note any missing or misconfigured headers
- Document findings immediately — do not batch until end

#### 3.2 Authentication & Access Control

Skill: `.claude/skills/auth-access-audit/`
Templates: `auth-checklist.md`, `auth-findings-template.md`

- Review login mechanism, error messages, rate limiting
- Review MFA availability and enforcement
- Review password reset flow
- Review OAuth/SSO configuration if applicable
- Review session initiation behavior

#### 3.3 Session Management & JWT

Skill: `.claude/skills/session-jwt-audit/`
Templates: `jwt-review-template.md`, `session-control-checklist.md`

- Inspect session tokens or JWTs
- Check cookie flags on session cookies
- Review token expiry and rotation policy
- Test logout behavior

#### 3.4 Authorization / RBAC

Skill: `.claude/skills/rbac-audit/`
Templates: `rbac-test-matrix.md`, `idor-review-template.md`

- Map role permissions against the defined role matrix
- Test horizontal access control (access other users' resources)
- Test vertical access control (access higher-privilege functions)
- Document IDOR surface

#### 3.5 Input Validation & Injection

Skill: `.claude/skills/input-validation-audit/`
Templates: `validation-review-template.md`, `injection-test-notes.md`

- Review input handling for key endpoints
- Note indicators of server-side validation (or lack thereof)
- Document injection test observations within authorized scope
- Review file upload handling if applicable

#### 3.6 Security Misconfiguration

Skill: `.claude/skills/security-misconfig-audit/`
Templates: `misconfig-review-template.md`, `hardening-checklist.md`

- Check for debug mode, verbose errors
- Check for exposed sensitive files
- Check for default credentials
- Review CORS configuration
- Complete hardening checklist

#### 3.7 Dependency & Supply Chain

Skill: `.claude/skills/dependency-audit/`
Templates: `dependency-findings-template.md`, `vulnerable-component-review.md`

- Review dependency manifests provided or observed
- Check for known CVEs
- Note abandoned or unmaintained packages
- Document high-severity vulnerable components in detail

#### 3.8 Logging & Monitoring

Skill: `.claude/skills/logging-monitoring-audit/`
Templates: `logging-checklist.md`, `audit-log-review-template.md`

- Review logging configuration and coverage
- Check for PII or credentials in logs
- Review log retention and integrity controls
- Note alerting configuration

### Step 4: Findings Collection and Register

1. Compile all findings from all domains into the findings register
2. Use `.claude/templates/findings-register-template.md` as the master register
3. Assign Finding IDs sequentially (`FIND-001`, `FIND-002`, ...)
4. Apply severity ratings per `.claude/rules/severity-rating-rules.md`
5. Confirm every finding has at least one EVID- reference
6. Note any `[UNKNOWN]` or `[ASSUMED]` items that influenced findings

### Step 5: Report Outline

1. Load `.claude/skills/report-writer/SKILL.md`
2. Draft the executive summary using `.claude/skills/report-writer/templates/executive-summary-template.md`
3. Draft the technical report using `.claude/skills/report-writer/templates/technical-report-template.md`
4. Save draft reports to `reports/draft/YYYY-MM-DD-website-[executive|technical]-report.md`
5. Optionally generate remediation plan using `/generate-remediation-plan`

### Step 6: Session Close

1. Update the audit session record with summary of activities, findings count, and next steps
2. Move session file from `audit-runs/active/` to `audit-runs/completed/`
3. Save a copy of the findings register to `audits/` with the appropriate date

---

## Outputs

| Output | Location | Template |
|--------|----------|---------|
| Audit session record | `audit-runs/completed/` | `audit-session-template.md` |
| Findings register | Root or `audits/` | `findings-register-template.md` |
| Executive summary (draft) | `reports/draft/` | `executive-summary-template.md` |
| Technical report (draft) | `reports/draft/` | `technical-report-template.md` |

---

## Safety Notes

**AUTHORIZATION REQUIRED:** Confirm authorization in `.claude/context/audit-context.md` before beginning. Default mode is passive review. Active testing (form submission, API calls with test payloads) is only permitted if explicitly authorized.

**SCOPE NOTE:** Do not test targets not listed in `.claude/context/scope.md`. If an out-of-scope issue is observed passively, note it as `[OUT OF SCOPE — NOT TESTED]`.
