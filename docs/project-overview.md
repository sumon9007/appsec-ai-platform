# Project Overview

## What This Platform Is

`appsec-ai-platform` is an audit workspace for authorized web application security reviews. It combines:

- A Python CLI and workflow engine for repeatable audit execution
- A Markdown-first governance layer for scope, authorization, evidence standards, and reporting
- A repository structure for evidence, findings, session records, and reports

The implementation is designed for defensive use in approved assessments. The codebase is not a general exploit framework and does not present itself as one.

## Intended Users

- Security engineers running internal or client-authorized reviews
- Reviewers and maintainers who need evidence-backed findings
- Engineers extending the platform toward broader AppSec coverage

## Scope

Current code supports:

- Passive HTTP and TLS inspection
- Passive crawling and HTML inventory
- Cookie and JWT observation
- Passive authentication and API spec review
- File-based dependency and secrets scanning
- Findings register and report generation
- Authorization enforcement and safety stop-condition checks

## Non-Goals

The repository does not currently provide a complete end-to-end web application testing platform. In particular, it does not yet implement:

- Broad active exploitation workflows
- Business-logic abuse modeling
- SAST, IaC, container, or cloud posture integrations
- Full authenticated multi-role orchestration in the shipped workflows

## Lawful Use

Use this platform only for lawful, authorized, defensive security work.

- Authorization must be documented before audit activity begins.
- Passive review is the default mode.
- Intrusive actions require explicit authorization.
- Sensitive data handling and stop conditions are part of the operating model.
