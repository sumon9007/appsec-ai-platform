# Command: /review-rbac

Focused review of role-based access control and authorization. Loads the rbac-audit skill and guides through role definitions, permission matrix verification, IDOR surface assessment, and privilege escalation path analysis.

## Trigger

Invoked when the user wants to perform a targeted review of authorization and access control. Can be run standalone or as part of `/audit-website` or `/audit-monthly`.

---

## Pre-Conditions

1. `.claude/context/audit-context.md` is populated and Authorization Status is **CONFIRMED**
2. `.claude/context/target-profile.md` defines known user roles
3. `.claude/context/scope.md` defines which endpoints and features are in scope
4. Test accounts representing at least two different roles are available

---

## Steps

### Step 1: Context Load

1. Read `.claude/context/audit-context.md` — confirm authorization
2. Read `.claude/context/target-profile.md` — note all defined roles and their descriptions
3. Read `.claude/context/scope.md` — note which resources and endpoints are in scope for testing
4. Read `.claude/rules/safety-authorization-rules.md` — confirm authorization level for active testing

### Step 2: Load Skill

Load: `.claude/skills/rbac-audit/SKILL.md`

Read:
- `.claude/skills/rbac-audit/templates/rbac-test-matrix.md`
- `.claude/skills/rbac-audit/templates/idor-review-template.md`

### Step 3: Role Definition Review

- List all roles defined in the application (`.claude/context/target-profile.md`)
- For each role, document what resources and functions it should be able to access
- Identify any roles with elevated or privileged permissions (admin, super-admin, manager)
- Note any service accounts or API roles
- Identify any roles that should have read-only or no-write access

### Step 4: Permission Matrix — Populate rbac-test-matrix.md

Using `rbac-test-matrix.md`, map:

**For each combination of Role × Resource:**
- What is the expected permission? (Read, Write, Delete, No Access)
- What is the observed permission? (Based on testing or documented behavior)
- Does the observed match the expected? (Pass / Fail)
- Notes on any discrepancies

Priority resources to test:
- User profile data (own vs. others)
- Administrative functions (user management, configuration)
- Financial or sensitive data records
- Bulk operations (export, delete, mass update)
- API endpoints for privileged operations

### Step 5: Horizontal Access Control Testing (IDOR)

Using `idor-review-template.md`, test for Insecure Direct Object References:

For each testable object type:
- Identify the endpoint and parameter used to reference the object (e.g., `/api/users/123`)
- Is the object ID guessable or sequential?
- Can User A access User B's object by substituting the object ID?
- Document: endpoint, parameter, test description, expected behavior, observed behavior

**IDOR test priority:**
1. User profile / account data
2. User-uploaded files or documents
3. Orders, transactions, or payment records
4. Messages or communications
5. Settings and configuration objects

**AUTHORIZATION REQUIRED:** IDOR testing involves making requests with modified object references. This requires explicit authorization in `.claude/context/audit-context.md`. In passive review mode, assess the attack surface only without performing active substitution.

### Step 6: Vertical Access Control Testing

- Can a standard user access admin-only endpoints?
- Can a read-only user perform write operations?
- Are authorization checks enforced server-side (not just hidden in the UI)?
- Test by attempting to access privileged endpoints with a lower-privilege test account

Document in `rbac-test-matrix.md` under the Admin role rows.

### Step 7: Privilege Escalation Path Analysis

- Are there any API parameters that specify a user's role or permissions?
- Can a user modify their own role through the user update endpoint?
- Are there any mass assignment risks (accepting role or permission fields in user update)?
- Can a standard user invite another user with elevated permissions?

### Step 8: Document Findings

For each access control failure:
- Record in the findings register using the auth-findings-template format
- Assign Finding ID
- Rate severity (IDOR with data access = High; privilege escalation to admin = Critical)
- Reference evidence items

---

## Outputs

| Output | Location | Template |
|--------|----------|---------|
| RBAC test matrix | `audit-runs/active/` | `rbac-test-matrix.md` |
| IDOR review records | `audit-runs/active/` | `idor-review-template.md` |
| Authorization findings | Findings register | `auth-findings-template.md` (RBAC section) |
| Evidence items | `evidence/raw/` | EVID- convention |

---

## Related Commands

- `/review-auth` — Authentication review (prerequisite or companion)
- `/audit-quarterly` — Quarterly audit includes full RBAC review
