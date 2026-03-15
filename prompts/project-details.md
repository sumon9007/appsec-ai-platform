I have a Python project workspace named `appsec-ai-platform`. I want you to generate complete, professional documentation for the project by analyzing the actual repository code and aligning it with the existing product/coverage documentation already present in the workspace.

Your task is to inspect the full codebase and produce a documentation set that explains:
1. what is already implemented,
2. how the system works technically,
3. how the code maps to the intended platform roadmap,
4. what is still missing,
5. and how close the platform is to a complete web application security assessment platform.

Important rules:
- Use the actual repository as the source of truth.
- Do not invent features that are not present in code.
- If existing docs claim something is implemented, verify it in code before repeating it as fact.
- If docs and code differ, explicitly call that out.
- Preserve a lawful, authorized, defensive framing for all security testing language.
- Mark uncertainty clearly with:
  - `Assumption:`
  - `Needs verification:`
  - `Doc/code mismatch:`

Repository context:
This workspace includes existing documentation that describes:
- an AppSec AI Platform Coverage Matrix
- OWASP WSTG mapping
- OWASP ASVS mapping
- current maturity summary
- executable coverage
- gap analysis
- a full build roadmap and phased delivery plan

You must use those existing docs as inputs, but validate their claims against the codebase before finalizing documentation.

Primary documentation goals:
- Create complete technical documentation for the current implementation
- Reconcile documentation claims with real code
- Produce an accurate “current state vs target state” view
- Explain architecture, modules, workflows, policies, evidence handling, reporting, and roadmap alignment
- Make the docs useful for engineers, reviewers, and future maintainers

Required analysis process:
1. Recursively scan the full repository.
2. Identify:
   - Python packages/modules
   - CLI entry points
   - workflows
   - tools
   - parsers
   - models
   - storage layer
   - reporting layer
   - policy modules
   - auth/session modules
   - tests
   - existing docs
   - configuration/dependency files
3. Read important files first:
   - root `README*`
   - `pyproject.toml`, `requirements*.txt`, `setup.py`, `poetry.lock`, etc.
   - `src/cli.py`
   - `scripts/run_audit.py`
   - files under `src/workflows/`
   - files under `src/tools/`
   - files under `src/policies/`
   - files under `src/models/`
   - files under `src/storage/`
   - files under `src/reporting/`
   - files under `src/auth/`
   - files under `src/session/`
   - files under `src/parsers/`
   - relevant tests
   - existing coverage/roadmap docs
4. Reconstruct the platform end-to-end:
   - how a run starts
   - how scope/authorization is loaded
   - how workflows execute
   - how evidence is written
   - how findings are normalized
   - how reports are generated
   - how stop conditions are enforced
5. Compare current code to the existing coverage matrix and roadmap.
6. Generate or update documentation accordingly.

What I want documented:
- Project overview
- Platform purpose and scope
- Current maturity and implementation status
- Architecture and execution flow
- Repository structure
- CLI and entrypoints
- Workflow engine and orchestration
- Tool-by-tool documentation
- Parser-by-parser documentation
- Models and data schemas
- Persistence/run-state handling
- Authorization and stop-condition policies
- Authentication/session handling
- Evidence and findings lifecycle
- Reporting outputs
- Configuration and environment expectations
- Installation/setup
- Usage examples
- Testing approach
- Current coverage against OWASP WSTG and ASVS
- Current gaps
- Roadmap alignment
- Technical debt / recommended next engineering priorities

Required output files:
Create a `/docs` folder with at least these files:

- `/docs/README.md`
  - docs index
  - quick navigation
  - concise current-state summary

- `/docs/project-overview.md`
  - what the platform is
  - intended users
  - scope and non-goals
  - lawful/authorized use framing

- `/docs/current-state.md`
  - what is implemented today
  - verified implementation summary
  - code-backed maturity summary

- `/docs/architecture.md`
  - system architecture
  - major components
  - execution flow
  - data flow
  - trust/safety boundaries
  - how evidence, findings, and reports move through the system

- `/docs/project-structure.md`
  - important repository tree
  - explanations of major directories and files

- `/docs/setup-and-installation.md`
  - prerequisites
  - install steps
  - environment setup
  - dependency installation
  - how to run locally

- `/docs/configuration.md`
  - config files
  - environment variables
  - secrets handling expectations
  - authorization/scope context handling

- `/docs/cli-and-workflows.md`
  - CLI usage
  - entry points
  - workflow descriptions
  - how passive/full audit execution works

- `/docs/tools-reference.md`
  - each tool in `src/tools/`
  - purpose
  - inputs
  - outputs
  - evidence produced
  - notable limitations
  - whether passive/authenticated/active

- `/docs/parsers-reference.md`
  - each parser in `src/parsers/`
  - what it extracts
  - where it is used

- `/docs/models-and-storage.md`
  - typed entities
  - run-state persistence
  - evidence/finding schemas
  - storage responsibilities

- `/docs/auth-session-policies.md`
  - credential handling
  - session management
  - authorization modes
  - stop conditions
  - safety constraints

- `/docs/reporting.md`
  - findings register
  - evidence store
  - report generation flow
  - output artifact descriptions

- `/docs/coverage-matrix-verified.md`
  - verified WSTG mapping
  - verified ASVS mapping
  - clearly separate:
    - Implemented in code
    - Partial
    - Documented but unverified
    - Missing

- `/docs/gap-analysis.md`
  - what is missing
  - what is partially wired
  - engineering AppSec extension gaps
  - active testing gaps
  - business logic / identity / client-side gaps

- `/docs/roadmap-alignment.md`
  - compare current codebase to the phase roadmap
  - identify which phases are complete, partial, or not started
  - recommend next implementation order based on the real codebase

- `/docs/troubleshooting.md`
  - common failure modes
  - debugging notes
  - incomplete/misaligned areas
  - operational caveats

- `/docs/developer-notes.md`
  - technical debt
  - refactor opportunities
  - missing abstractions
  - code/doc mismatches
  - recommended next engineering steps

Also create or update the root `README.md` so it is concise, polished, and consistent with the generated docs.

Special comparison requirement:
You must explicitly compare:
- existing documentation claims
vs
- actual code implementation

Produce a section called:
`Documentation Validation Summary`

This section must include:
- Verified claims
- Partially verified claims
- Unverified claims
- Incorrect or outdated claims
- Missing documentation for code that exists

Specific analysis instructions:
- Trace the main execution path from CLI to workflow to tools to evidence/reporting.
- Identify all likely main entry points.
- Identify which tools are passive, authenticated, or active.
- Identify where authorization gates are enforced.
- Identify where intrusive actions are prevented or conditioned.
- Identify where evidence is written and how findings are serialized.
- Identify whether workflows are resumable and how state is persisted.
- Identify whether OWASP mapping claims are explicitly supported by code behavior.
- Distinguish implementation from aspiration.

Documentation style requirements:
- Write in clean technical Markdown.
- Prefer concise explanations grounded in code.
- Use tables where they improve clarity.
- Use code blocks for commands/examples.
- Do not dump large source files.
- Summarize classes/functions/modules instead of copying them.
- When possible, cite file paths and relevant symbols.
- Keep claims evidence-based.

Before generating final docs, first produce a discovery summary with:
1. detected project type
2. main entry points
3. core architecture components
4. dependency files found
5. workflows found
6. major tools found
7. policy/safety modules found
8. reporting/storage modules found
9. existing docs found
10. proposed documentation plan

Then generate the documentation files.

Final deliverables:
1. Discovery summary
2. Documentation validation summary
3. List of generated/updated files
4. Full `/docs` content
5. Updated root `README.md`
6. Final section: assumptions, gaps, and recommended next documentation improvements