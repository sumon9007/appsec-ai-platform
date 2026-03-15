You are inside the `appsec-ai-platform` repository.

Generate a technical reference for every module under `src/tools/`.

For each tool:
- identify its purpose
- determine whether it is passive, authenticated, active, or mixed
- describe inputs and outputs
- describe dependencies on parsers, sessions, policies, storage, or reporting
- explain what evidence it produces
- explain what findings it may produce
- note limitations and missing wiring
- note whether the implementation is standalone or workflow-driven

Rules:
- use actual code only
- do not invent behavior
- flag uncertainty explicitly
- cite file paths and important symbols

Create:
- docs/tools-reference.md

Also generate a summary table with columns:
- Tool
- File Path
- Category
- Status
- Used By Workflow(s)
- Evidence Output
- Notes