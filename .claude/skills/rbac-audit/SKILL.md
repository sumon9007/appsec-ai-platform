> **Reference Guide** — This skill documents the methodology. For automated execution, run:
> `python scripts/run_audit.py audit full --tools rbac`
> Use this skill to interpret tool output, conduct manual review steps, or guide authorized active testing.

# Skill: RBAC and Authorization Audit

## Purpose

Assess the role-based access control implementation and authorization enforcement across the application to identify broken access control vulnerabilities, including horizontal privilege escalation (IDOR), vertical privilege escalation, missing server-side checks, and role permission drift.

---

## Inputs Required

| Input | Source | Required? |
|-------|--------|-----------|
| Target application URL(s) | `.claude/context/scope.md` | Required |
| User role definitions | `.claude/context/target-profile.md` | Required |
| Test accounts (minimum 2 different roles) | Provided by client | Required for active testing |
| List of in-scope endpoints/resources | `.claude/context/scope.md` | Required |
| Authorization confirmation | `.claude/context/audit-context.md` | Required |

---

## Method

### Phase 1: Role Mapping

1. List all roles defined in the application (from `.claude/context/target-profile.md`)
2. For each role, determine the expected permissions:
   - Which resources can it read?
   - Which resources can it write or modify?
   - Which resources can it delete?
   - Which functions or admin operations can it access?
3. Identify the role hierarchy (which roles are supersets of others)
4. Identify any special-purpose roles (service accounts, read-only, support agents)

### Phase 2: Permission Matrix Population

Using `rbac-test-matrix.md`:

5. For each Role × Resource combination, record:
   - Expected permission (from design documentation or client-stated intent)
   - Observed permission (from testing)
   - Pass/Fail comparison
   - Evidence reference

Priority resource types:
- User account data (own vs. others)
- Administrative configuration
- Financial or transaction records
- User-generated content or files
- Bulk operations (export, bulk delete, mass updates)
- System management functions

### Phase 3: Horizontal Access Control Testing (IDOR)

6. For each object-based resource type:
   - Identify the parameter used to reference the object (ID, UUID, slug)
   - Is the ID sequential, predictable, or guessable?
   - Using Account A's session, attempt to access Account B's resource by substituting the object identifier
   - Document in `idor-review-template.md`

7. Test IDOR on:
   - GET requests (reading another user's data)
   - PUT/PATCH requests (modifying another user's data)
   - DELETE requests (deleting another user's data)
   - File access (downloading another user's uploads)

**AUTHORIZATION REQUIRED:** Active IDOR testing requires explicit authorization. In passive mode, assess the attack surface and note ID predictability only.

### Phase 4: Vertical Access Control Testing

8. Using a lower-privilege account, attempt to access:
   - Admin UI pages
   - Admin API endpoints
   - Functions visible only to higher-privilege roles in the UI

9. Verify that server-side authorization is enforced:
   - Is access denied via UI hiding only, or is it also enforced server-side?
   - Can the user call an admin API endpoint directly if they know the URL?

### Phase 5: Privilege Escalation Path Analysis

10. Are there user-controlled parameters that affect the user's own role or permissions?
    - Can a user set their own role via a POST/PUT parameter?
    - Is there a mass assignment vulnerability on user objects?
11. Can a user invite another user with a higher role than their own?
12. Can a user create objects that gain them elevated access?

---

## Outputs

| Output | Template | Description |
|--------|---------|-------------|
| RBAC test matrix | `rbac-test-matrix.md` | Role × Resource permission mapping |
| IDOR review records | `idor-review-template.md` | Per-resource IDOR test cases |
| Authorization findings | `auth-findings-template.md` | Finding records for all failures |
| Evidence items | EVID- convention | Request/response captures |

---

## Templates Used

- `.claude/skills/rbac-audit/templates/rbac-test-matrix.md`
- `.claude/skills/rbac-audit/templates/idor-review-template.md`

---

## References

- [OWASP A01:2021 — Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [OWASP Testing Guide — Authorization Testing](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/05-Authorization_Testing/)
- [OWASP API Security — BOLA (API1:2023)](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)
- [CWE-285 — Improper Authorization](https://cwe.mitre.org/data/definitions/285.html)
- [CWE-639 — Authorization Bypass Through User-Controlled Key](https://cwe.mitre.org/data/definitions/639.html)
