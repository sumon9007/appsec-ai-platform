# Skill: Dependency and Supply Chain Audit

## Purpose

Assess the application's third-party dependencies for known security vulnerabilities (CVEs), abandonment risk, supply chain concerns, and license risk. Produce a prioritized list of remediation actions.

---

## Inputs Required

| Input | Source | Required? |
|-------|--------|-----------|
| Dependency manifests | Provided by client or observable | Strongly recommended |
| Lock files | Provided by client | Recommended |
| Tech stack and language ecosystem | `.claude/context/target-profile.md` | Required |
| Authorization confirmation | `.claude/context/audit-context.md` | Required |

**Acceptable manifest formats:**
- npm: `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- Python: `requirements.txt`, `Pipfile`, `Pipfile.lock`, `pyproject.toml`, `poetry.lock`
- Ruby: `Gemfile`, `Gemfile.lock`
- Java/Kotlin: `pom.xml`, `build.gradle`, `build.gradle.kts`
- Go: `go.mod`, `go.sum`
- PHP: `composer.json`, `composer.lock`
- .NET: `*.csproj`, `packages.config`, `packages.lock.json`

If manifests are not available: note as `[UNKNOWN]` and assess based on observable technology indicators only.

---

## Method

### Phase 1: Inventory

1. Parse all provided dependency manifests
2. Separate direct dependencies from transitive dependencies
3. Record: package name, installed version, declared version constraint (e.g., `^2.1.0` vs `2.1.0`)
4. Note whether lock files are present (pin to exact versions — security best practice)
5. Count total direct and transitive dependencies

### Phase 2: CVE Scan

6. For each dependency, check against vulnerability databases:
   - **NVD** (nvd.nist.gov) — primary CVE database
   - **OSV** (osv.dev) — open source vulnerability database covering npm, PyPI, Go, RubyGems, Maven
   - **GitHub Security Advisories** (github.com/advisories) — package-specific advisories
   - **Snyk** (snyk.io/vuln) — curated vulnerability data
   - Package-ecosystem-specific advisories:
     - npm audit advisories
     - PyPI advisory database
     - RubyGems advisories

7. For each CVE identified:
   - Record in `dependency-findings-template.md`
   - Note: CVE ID, CVSS v3 score, severity rating, affected version range, fix version
   - Determine if the application's installed version is in the affected range
   - Determine if a fix version is available

### Phase 3: Exploitability Assessment

8. For each Critical or High CVE:
   - Is the vulnerable code path reachable from this application? (Are the affected functions/features used?)
   - Is the attack vector network-accessible? (Remote code execution vs. local only)
   - Does the application's environment reduce exploitability? (e.g., WAF, network isolation)
   - Complete `vulnerable-component-review.md` for each Critical/High finding

### Phase 4: Abandonment and Maintenance Assessment

9. For each direct dependency:
   - Last release date (flag if > 24 months)
   - Number of open security issues in the repository
   - Active maintainer(s) present?
   - Known successor/fork/alternative?
   - Downloads per week (npm, PyPI) as a proxy for ecosystem health

### Phase 5: Supply Chain Risk Assessment

10. Are all packages sourced from the official registry for the ecosystem?
11. Are any packages pinned to mutable references (git branches, `latest` tags)?
12. Are there any recently renamed packages or namespace changes (potential dependency confusion)?
13. Do any packages have unusual installation hooks (postinstall scripts, setup.py actions)?
14. Is a Software Bill of Materials (SBOM) produced in the build pipeline?
15. Are package signatures verified during installation?

### Phase 6: License Review (Advisory)

16. For each dependency (especially in commercial products):
    - What is the declared license?
    - Are there any copyleft licenses (GPL, AGPL, SSPL)?
    - Are there commercial license restrictions?
    - Document any incompatible licenses as advisory findings

---

## Outputs

| Output | Template | Description |
|--------|---------|-------------|
| Dependency findings table | `dependency-findings-template.md` | CVE findings per dependency |
| Vulnerable component reviews | `vulnerable-component-review.md` | Deep review for Critical/High CVEs |
| Findings in register | Standard finding format | Formal finding records |
| Evidence items | EVID- convention | Tool outputs, advisory screenshots |

---

## Templates Used

- `.claude/skills/dependency-audit/templates/dependency-findings-template.md`
- `.claude/skills/dependency-audit/templates/vulnerable-component-review.md`

---

## References

- [OWASP A06:2021 — Vulnerable and Outdated Components](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)
- [OWASP Dependency Check](https://owasp.org/www-project-dependency-check/)
- [CWE-1104 — Use of Unmaintained Third-Party Components](https://cwe.mitre.org/data/definitions/1104.html)
- [NIST SP 800-161 — Supply Chain Risk Management](https://csrc.nist.gov/publications/detail/sp/800-161/rev-1/final)
