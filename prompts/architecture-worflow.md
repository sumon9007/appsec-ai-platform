You are working in the `appsec-ai-platform` repository.

Your goal is to reverse-engineer the platform architecture and execution flow from the actual code.

Analyze:
- CLI entrypoints
- workflow orchestration
- tool execution
- parser usage
- policy enforcement
- evidence/finding lifecycle
- report generation
- storage/run-state handling
- auth/session interactions

Instructions:
1. Trace the main execution path from entrypoint to final output.
2. Identify all major components and their responsibilities.
3. Describe how data flows between modules.
4. Identify boundaries for:
   - authorization
   - safety/stop conditions
   - evidence creation
   - finding normalization
   - persistence
5. Identify passive vs authenticated vs active pathways.
6. Note assumptions and incomplete wiring.

Create:
- docs/architecture.md
- docs/execution-flow.md
- docs/component-responsibilities.md

Include:
- module interaction summaries
- simplified flow diagrams in Markdown
- key symbols/functions/classes by file path
- implementation caveats
- doc/code mismatches related to architecture