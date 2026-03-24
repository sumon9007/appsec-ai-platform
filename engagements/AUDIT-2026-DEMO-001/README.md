# AUDIT-2026-DEMO-001 — TechStartup SaaS Platform

**URL:** https://app.techstartup.io  |  **Env:** Staging  |  **Mode:** active-staging  |  **Type:** release-gate
**Status:** Authorization PENDING  |  **Auditor:** Security Analyst  |  **Created:** 2026-03-24

---

## File Index & Load Order

> **Token-efficient load order:** `engagement-summary.md` → `MEMORY.md` → `audit-context.md` → [others as needed]

| File | Purpose | Load When |
|------|---------|-----------|
| `context/engagement-summary.md` | Status, findings snapshot, next steps | **Always — load first** |
| `memory/MEMORY.md` | Decisions, questions, session notes | **Always** |
| `context/audit-context.md` | Auth gate, engagement metadata | **Always** |
| `context/scope.md` | In/out-of-scope assets, permitted activities | Starting a domain review |
| `context/target-profile.md` | Tech stack, auth model, integrations | Tech context needed |
| `context/assumptions.md` | Working assumptions, unknowns, blockers | Labeling findings |
| `audit-runs/active/findings-register.md` | All findings for this engagement | Reviewing / adding findings |
| `evidence/raw/` | Collected evidence | Classifying evidence |
| `reports/` | Draft and final reports | Report generation |

---
*Updated: 2026-03-24*
