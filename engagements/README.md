# Engagements

This directory holds all per-engagement audit data. Each sub-folder is a self-contained engagement unit — fully isolated from all other engagements in this workspace.

---

## Structure

```
engagements/
  _template/                   ← Blank template. Copy this to start a new engagement.
  AUDIT-YYYY-CLIENT-NNN/       ← One folder per engagement.
    context/                   ← Engagement context: target, scope, authorization, assumptions
    audit-runs/
      active/                  ← Current session files and findings register
      completed/               ← Archived session files once closed
    evidence/
      raw/                     ← Evidence collected but not yet reviewed (EVID-YYYY-MM-DD-NNN files)
      reviewed/                ← Evidence confirmed as valid and linked to findings
      summarized/              ← Evidence sanitized of PII/credentials — for report inclusion
    reports/
      draft/                   ← Draft Markdown report files
      final/                   ← Final versioned reports
    audits/
      weekly/ monthly/ quarterly/ release/ annual/
```

---

## Active Engagement

The active engagement is identified in `.claude/context/active.md` and via the `ACTIVE_ENGAGEMENT` environment variable in `.env`.

To confirm which engagement the Python CLI is targeting:

```bash
python scripts/run_audit.py session status
```

---

## Creating a New Engagement

1. Copy the template folder:
   ```bash
   cp -r engagements/_template/ engagements/AUDIT-YYYY-CLIENT-NNN/
   ```

2. Populate all four context files:
   - `context/audit-context.md` — engagement ID, target, authorization
   - `context/target-profile.md` — application profile and tech stack
   - `context/scope.md` — in-scope / out-of-scope targets and techniques
   - `context/assumptions.md` — assumptions and known unknowns

3. Set the active engagement in `.env`:
   ```bash
   ACTIVE_ENGAGEMENT=AUDIT-YYYY-CLIENT-NNN
   ```

4. Update `.claude/context/active.md` to point to the new engagement.

5. Confirm authorization status is `CONFIRMED` in `context/audit-context.md` before running any audit commands.

---

## Data Isolation and Confidentiality

Each engagement directory contains data specific to a single client and engagement. Do not mix data across engagement directories. When an engagement is complete, archive or remove its directory according to your data retention policy.

---

## Engagements in this Workspace

| Engagement ID | Target | Status | Started |
|--------------|--------|--------|---------|
| AUDIT-2026-DR-001 | diversifiedrobotic.com | Active | 2026-03-13 |
| AUDIT-2026-DEMO-001 | TechStartup SaaS Platform (https://app.techstartup.io) | Active — Authorization PENDING | 2026-03-24 |
