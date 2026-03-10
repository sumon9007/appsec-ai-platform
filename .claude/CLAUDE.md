# Claude Code — Security Audit Workspace Instructions

These instructions govern how Claude Code operates within this security audit workspace. Follow them strictly and completely.

---

## Mandatory Pre-Audit Steps

Before executing any audit command or producing any findings, Claude Code MUST:

1. **Read all files in `.claude/context/`** — audit-context.md, target-profile.md, scope.md, assumptions.md
2. **Confirm authorization** — verify that `.claude/context/audit-context.md` contains an explicit authorization confirmation. If missing, stop and request it.
3. **Read all files in `.claude/rules/`** — especially `safety-authorization-rules.md` and `audit-scope-rules.md`
4. **Identify the relevant skill(s)** for the audit command being run
5. **Load the relevant skill's SKILL.md** and its templates before producing any output

---

## Command Invocation

Commands are invoked as slash commands, e.g.:

- `/audit-website` → reads `.claude/commands/audit-website.md`
- `/review-auth` → reads `.claude/commands/review-auth.md`
- `/generate-report` → reads `.claude/commands/generate-report.md`

For each command:
- Load the command definition from `.claude/commands/[command-name].md`
- Follow the Steps section in order
- Load all skills listed in the command before beginning
- Use the templates referenced in the command for all outputs

---

## Findings Standards

- All findings MUST be evidence-based — no finding without a referenced evidence item
- Evidence items MUST use the `EVID-YYYY-MM-DD-NNN` labeling convention (see `.claude/docs/evidence-standard.md`)
- Every finding MUST include: Finding ID, Title, Severity, Domain, Description, Evidence reference, Impact, Recommendation, Status
- Severity MUST use only the defined vocabulary: **Critical / High / Medium / Low / Info**
- Severity ratings MUST follow `.claude/rules/severity-rating-rules.md`
- Speculative findings are not permitted — findings must be based on observed evidence

---

## Handling Unknowns and Assumptions

- Any information that cannot be confirmed MUST be labeled `[UNKNOWN]`
- Any assumption being made MUST be labeled `[ASSUMED]` and documented in `.claude/context/assumptions.md`
- Do not treat assumed information as confirmed fact in findings

---

## Scope Enforcement

- **Never test or probe targets outside the scope defined in `.claude/context/scope.md`**
- If an out-of-scope issue is discovered during passive review, flag it as `[OUT OF SCOPE — NOT TESTED]` and do not investigate further
- Confirm scope is populated before beginning any audit step
- See `.claude/rules/audit-scope-rules.md` for full rules

---

## Safety and Authorization

- **Passive review only by default.** Active exploitation requires explicit written authorization documented in `.claude/context/audit-context.md`
- Stop and escalate if unexpected sensitive data (PII, credentials, private keys) is encountered unexpectedly
- Document authorization status at the start of every audit session using `.claude/templates/audit-session-template.md`
- See `.claude/rules/safety-authorization-rules.md` for full rules

---

## Template Usage

Always use templates when producing output documents:

| Output Type | Template |
|-------------|---------|
| Audit plan | `.claude/templates/audit-plan-template.md` |
| Audit session record | `.claude/templates/audit-session-template.md` |
| Findings register | `.claude/templates/findings-register-template.md` |
| Weekly summary | `.claude/templates/weekly-summary-template.md` |
| Monthly summary | `.claude/templates/monthly-summary-template.md` |
| Quarterly summary | `.claude/templates/quarterly-summary-template.md` |
| Release gate | `.claude/templates/release-gate-template.md` |
| Annual review | `.claude/templates/annual-review-template.md` |
| Executive summary | `.claude/skills/report-writer/templates/executive-summary-template.md` |
| Technical report | `.claude/skills/report-writer/templates/technical-report-template.md` |
| Remediation plan | `.claude/skills/report-writer/templates/remediation-plan-template.md` |

---

## Skill Loading

Each audit domain has a corresponding skill. Load the relevant skill before auditing that domain:

| Domain | Skill Path |
|--------|-----------|
| Authentication & Access | `.claude/skills/auth-access-audit/SKILL.md` |
| RBAC & Authorization | `.claude/skills/rbac-audit/SKILL.md` |
| Dependencies | `.claude/skills/dependency-audit/SKILL.md` |
| Security Headers & TLS | `.claude/skills/headers-tls-audit/SKILL.md` |
| Logging & Monitoring | `.claude/skills/logging-monitoring-audit/SKILL.md` |
| Input Validation | `.claude/skills/input-validation-audit/SKILL.md` |
| Session & JWT | `.claude/skills/session-jwt-audit/SKILL.md` |
| Security Misconfiguration | `.claude/skills/security-misconfig-audit/SKILL.md` |
| Report Generation | `.claude/skills/report-writer/SKILL.md` |

---

## Output File Naming

- Reports: `reports/[draft|final]/YYYY-MM-DD-[type]-report.md`
- Audit summaries: `audits/[weekly|monthly|quarterly|release|annual]/YYYY-MM-DD-[type].md`
- Audit session records: `audit-runs/[active|completed]/YYYY-MM-DD-[domain]-session.md`
- Evidence: `evidence/raw/EVID-YYYY-MM-DD-NNN-[description].md`

---

## Prohibited Actions

- Do not produce findings without evidence references
- Do not test outside defined scope
- Do not perform active exploitation without documented authorization
- Do not use non-standard severity labels
- Do not skip template usage for output documents
- Do not begin any audit without reading .claude/context/ and .claude/rules/ first
