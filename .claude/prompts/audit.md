# Audit Prompts

Reusable reasoning helpers for starting and executing audit sessions.

---

## Starting an Audit Session

**Objective:** Initialize a structured audit session for a new target.

**Steps:**

1. Read all four context files:
   - `.claude/context/audit-context.md` — confirm Authorization Status is CONFIRMED
   - `.claude/context/target-profile.md` — note tech stack, roles, integrations
   - `.claude/context/scope.md` — establish in-scope targets and exclusions
   - `.claude/context/assumptions.md` — note anything unconfirmed

2. Confirm scope and constraints. If authorization is not CONFIRMED, halt.

3. Create a session record using `.claude/templates/audit-session-template.md`. Save to `audit-runs/active/YYYY-MM-DD-session.md`.

4. Identify initial review focus areas based on what evidence is available:
   - headers and TLS (always passive-reviewable)
   - authentication entry points
   - session indicators (cookies, tokens in responses)
   - access control surface
   - input validation surface
   - logging indicators

5. Note what is unknown and cannot be assessed without further evidence.

**Output:** session record with audit overview, known evidence inventory, unknown areas, initial review plan.

**Python CLI:** `python scripts/run_audit.py session status` to verify authorization state.

---

## Full Website Audit Execution

**Objective:** Run a structured end-to-end security audit covering all in-scope domains.

**Steps:**

1. Complete the session start steps above.

2. Run the Python CLI for automated coverage:
   ```bash
   python scripts/run_audit.py audit full
   ```

3. For domains requiring manual review, use the relevant skills as reference guides:
   - `headers-tls-audit` — transport security
   - `auth-access-audit` — authentication
   - `rbac-audit` — access control
   - `session-jwt-audit` — session and JWT
   - `input-validation-audit` — injection surface
   - `security-misconfig-audit` — misconfiguration
   - `logging-monitoring-audit` — logging coverage (manual only)

4. For each domain, record:
   - confirmed findings (with EVID- references)
   - suspected findings (labeled with confidence)
   - review gaps (what could not be confirmed)

5. Update `audit-runs/active/findings-register.md` after each domain.

**Output:**
- Updated findings register
- Updated audit session record
- Evidence files in `evidence/raw/`

---

## Evidence Review Checklist

When reviewing collected evidence before writing findings:

- Does each EVID- item have a date, collector, and target?
- Is each item stored in `evidence/raw/`?
- Does any item contain credentials, PII, or payment data? → Handle per safety rules before proceeding.
- Is the evidence reproducible (could it be recreated with the same steps)?
- Does it directly support the finding it is linked to?

---

## Gap Analysis Prompt

When an audit domain cannot be fully assessed:

1. State clearly what was tested and what evidence was collected.
2. State what could not be tested and why (no access, passive-only mode, no test account).
3. Label the gap: `[REVIEW GAP — REQUIRES: <what is needed>]`
4. Include review gaps in the findings register as `review-gap` status items.
5. Include them in the report under a dedicated Review Gaps section.

Never treat a review gap as a confirmed vulnerability. Never treat it as confirmed safety.
