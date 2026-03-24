# Documentation Index

This documentation set describes the current, code-verified state of `appsec-ai-platform`.

---

## Current-State Summary

- The platform is a structured audit workspace with a runnable Python CLI and a Claude governance layer.
- Passive assessment, evidence capture, findings normalization, and draft report generation are fully implemented.
- Auth/session abstractions and authorization enforcement exist in code but are not end-to-end wired into all workflows.
- Active testing execution is gated by authorization policy but not yet orchestrated.
- See [current-state.md](current-state.md) for a code-verified implementation summary.

---

## Quick Navigation

### Getting Started
- [Setup and installation](setup-and-installation.md)
- [Configuration reference](configuration.md)
- [Audit tool requirements — step-by-step](audit-tool-requirements.md)

### Architecture and Structure
- [Project overview](project-overview.md)
- [Repository layout](project-structure.md)
- [Architecture](architecture.md)
- [Models and storage](models-and-storage.md)
- [Auth, session, and policies](auth-session-policies.md)
- [Parsers reference](parsers-reference.md)

### Running Audits
- [CLI and workflows](cli-and-workflows.md)
- [Tools reference](tools-reference.md)
- [Reporting](reporting.md)

### Current State and Planning
- [Verified implementation summary](current-state.md)
- [Verified coverage matrix](coverage-matrix-verified.md)
- [Gap analysis](gap-analysis.md)
- [Roadmap alignment](roadmap-alignment.md)
- [Full platform roadmap](full-platform-roadmap.md)

### Reference
- [Troubleshooting](troubleshooting.md)
- [Developer notes](developer-notes.md)
