# Roadmap Alignment

## Summary

The current codebase aligns well with the early roadmap phases, but later phases are only partially started.

## Phase-by-Phase Status

| Phase | Status | Notes |
|------|--------|------|
| Phase 1: Platform Core | Mostly complete | Models, storage, CLI, workflows, and policies exist |
| Phase 2: Passive Coverage Expansion | Mostly complete | Crawl, cookies, JWTs, misconfig, dependency review are present |
| Phase 3: Authenticated Assessment | Partial | Credential and session modules exist, but broad end-to-end authenticated workflow coverage is limited |
| Phase 4: Controlled Active Testing | Partial | Authorization policy exists; active probe execution remains limited |
| Phase 5: API Security | Partial | OpenAPI/Postman parsing and passive API analysis exist |
| Phase 6: Engineering AppSec Extensions | Started only in secrets scanning | No SAST, IaC, container, or cloud modules yet |

## Notable Roadmap Mismatches

Doc/code mismatch:
- The roadmap implies Phase 3 exit criteria around real role-aware authenticated workflows. The current implementation has support modules, but not a clearly complete end-to-end authenticated test engine.

Doc/code mismatch:
- The roadmap for Phase 4 anticipates an `active_probe_engine.py`, but no such module exists.

Doc/code mismatch:
- The roadmap for API security anticipates richer authenticated API testing than the current passive/spec-focused implementation provides.

## Recommended Next Implementation Order

1. Wire authenticated sessions into real workflow paths for auth, RBAC, session, and API review.
2. Add a small, explicit active probe engine that can be authorization-gated and audited.
3. Centralize stop-condition enforcement so it cannot be skipped accidentally.
4. Improve run-state tracking to capture evidence IDs and support resume semantics.
5. Add logging/monitoring automation.
6. Extend into engineering AppSec areas such as SAST and IaC.
