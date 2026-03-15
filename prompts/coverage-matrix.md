You are inside the `appsec-ai-platform` repository.

Your task is to verify the project’s coverage claims against the actual codebase.

Focus:
- current maturity summary
- executable coverage today
- OWASP WSTG mapping
- OWASP ASVS mapping
- roadmap phase completion

Instructions:
1. Locate and read the existing coverage matrix and roadmap docs.
2. Inspect the repository code to verify each claim.
3. For every coverage claim, classify it as:
   - Implemented
   - Partial
   - Missing
   - Documented but not verified
   - Doc/code mismatch
4. Use code paths as evidence for each conclusion.
5. Do not assume a capability exists unless the implementation is present.
6. Clearly distinguish:
   - code that exists
   - code that is partially wired
   - methodology/docs without executable implementation

Required deliverables:
- docs/coverage-matrix-verified.md
- docs/documentation-validation-summary.md
- docs/phase-completion-assessment.md

For each section include:
- claim
- verification status
- supporting code path(s)
- notes
- remediation recommendation if mismatched

Also provide a concise summary:
- what is truly implemented today
- what is overstated in docs
- what is missing but planned
- what should be built next