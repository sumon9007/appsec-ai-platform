# Claude Code Security Audit Agent Architecture

## Purpose

This document defines the architecture of this repository as a Claude Code-native Security Audit Agent workspace.

The architecture is designed to support:
- target-specific website and web application audits
- reusable command-based audit execution
- evidence-based analysis
- standardized findings and reporting
- safe, non-destructive review workflows
- long-term audit reuse and continuous improvement

This workspace is Markdown-first and environment-agnostic.

---

## Architecture Goal

The goal is to make this repository operate like a structured audit agent rather than a loose collection of notes.

The system should:
1. accept target-specific context
2. execute structured review workflows
3. apply governance rules
4. use specialist skills
5. update working audit state
6. generate normalized findings
7. produce draft and final reports
8. support remediation planning

---

## High-Level Architecture

```text
Analyst
  │
  ▼
Context Layer
  │
  ▼
Command Layer
  │
  ▼
Rules + Skills + Prompts + Templates
  │
  ▼
Working Audit State
  │
  ▼
Findings Register + Acceptance Criteria View
  │
  ▼
Draft Report + Remediation Plan
  │
  ▼
Final Audit Output