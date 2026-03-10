# Command: /review-dependencies

Focused review of third-party dependencies for known CVEs, abandoned packages, license risks, and supply chain concerns.

## Trigger

Invoked when the user wants to perform a targeted dependency and supply chain security review. Can be run standalone or as part of any cadence audit.

---

## Pre-Conditions

1. `.claude/context/audit-context.md` is populated and Authorization Status is **CONFIRMED**
2. Dependency manifests are available (package.json, requirements.txt, Gemfile, go.mod, pom.xml, or equivalent)
3. `.claude/context/target-profile.md` identifies the tech stack and language ecosystem

---

## Steps

### Step 1: Context Load

1. Read `.claude/context/audit-context.md` — confirm authorization
2. Read `.claude/context/target-profile.md` — note language ecosystem, package manager, and known frameworks
3. Read `.claude/context/assumptions.md` — note any dependency-related unknowns

### Step 2: Load Skill

Load: `.claude/skills/dependency-audit/SKILL.md`

Read:
- `.claude/skills/dependency-audit/templates/dependency-findings-template.md`
- `.claude/skills/dependency-audit/templates/vulnerable-component-review.md`

### Step 3: Dependency Inventory

If dependency manifests are provided:
- Parse the direct dependency list
- Note the language ecosystem(s): npm, pip, gem, Maven, Gradle, Composer, Go modules, NuGet
- Note the total count of direct dependencies
- Note the package manager and whether lock files are present (package-lock.json, Pipfile.lock, etc.)
- Note whether lock files are committed (good practice for reproducible builds)

If dependency manifests are not provided:
- Document as `[UNKNOWN]` in `.claude/context/assumptions.md`
- Proceed with review of what is observable from the application's technology indicators

### Step 4: CVE Review

For each direct dependency (and key transitive dependencies):

1. Check against known CVE databases and advisory feeds:
   - GitHub Security Advisories
   - NVD (National Vulnerability Database)
   - OSV (Open Source Vulnerabilities — osv.dev)
   - Snyk vulnerability database
   - Package-specific advisories (npm advisories, PyPI advisories)

2. For each CVE identified:
   - Record in `dependency-findings-template.md`
   - Note: package name, installed version, CVE ID, CVSS score, fix version, exploitability

3. Prioritize by CVSS score and exploitability:
   - CVSS ≥ 9.0 or CISA KEV listed: Critical — immediate action required
   - CVSS 7.0–8.9: High — fix within 7 days
   - CVSS 4.0–6.9: Medium — fix within 30 days
   - CVSS < 4.0: Low — fix within 90 days

### Step 5: Abandoned Package Review

For each dependency:
- When was the last release? (> 24 months without a release = at-risk)
- Does the package have active maintainers?
- Are there open security issues with no response from maintainers?
- Is there a successor package or fork?

Document abandoned packages in `dependency-findings-template.md` — severity typically Low unless they contain unpatched vulnerabilities.

### Step 6: Supply Chain Concerns

- Are any packages pinned to mutable references (e.g., `latest`, a branch name, a git SHA)?
- Are all packages sourced from the official registry for that ecosystem?
- Are there any recently deprecated packages (name changes, takeovers)?
- Are there any packages with unusual installation scripts or post-install hooks?
- Is there a Software Bill of Materials (SBOM) for this application?

Document any supply chain concerns found.

### Step 7: License Risk Review

For commercial applications, check for copyleft licenses in dependencies:
- GPL v2/v3 in a commercial product (may require source disclosure)
- AGPL in a SaaS product (AGPL has network use provisions)
- SSPL in a commercial product
- Commercial license restrictions

Note: License review is advisory unless a clearly incompatible license is present.

### Step 8: Deep Review of High-Severity Findings

For any dependency with a CVSS ≥ 7.0 CVE:
- Complete `vulnerable-component-review.md` for each affected package
- Assess: Is the vulnerable code path reachable in this application?
- Assess: Is there a viable attack path given the application's architecture?
- Document exploitability notes and recommended remediation

### Step 9: Document Findings and Recommendations

1. Complete findings register with all CVE findings
2. Provide a prioritized list of packages to update
3. Note any packages where no fix is available (document mitigating controls)

---

## Outputs

| Output | Location | Template |
|--------|----------|---------|
| Dependency findings table | `audit-runs/active/` | `dependency-findings-template.md` |
| Vulnerable component reviews | `audit-runs/active/` | `vulnerable-component-review.md` |
| Findings in register | Current findings register | Standard finding format |
| Evidence items | `evidence/raw/` | EVID- convention |
