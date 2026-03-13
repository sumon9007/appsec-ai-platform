# Gap Analysis

## What Is Missing

- SAST integration
- IaC scanning
- container image scanning
- cloud posture checks
- business-logic testing workflows
- identity-management testing
- robust client-side security review
- stored cryptography review

## What Is Partially Wired

- Authenticated session support exists, but the main workflows do not yet use it to deliver broad role-aware testing.
- RBAC and input-validation tooling exist, but much of the behavior still produces guidance and review gaps rather than complete active validation.
- Stop conditions are implemented as policy functions, not a consistently enforced pipeline-wide safeguard.
- Run-state persistence exists, but true pause/resume workflow control is limited.

## Engineering AppSec Extension Gaps

- No SBOM workflow
- No code scanning integrations
- No infrastructure scanning
- No CI-oriented security policy checks beyond docs and templates

## Active Testing Gaps

- No general active probe engine
- No rate-limited replay orchestration exposed to users
- No full exploit confirmation pipeline with evidence capture

## Identity and Business-Logic Gaps

- No account lifecycle review automation
- No username enumeration workflow
- No stateful abuse-case or privilege-chain modeling
- No explicit workflow engine for checkout/payment/approval-type business flows

## Practical Impact

The current platform is useful for structured passive assessments and reporting, but it should not yet be described as a complete web application security assessment platform without qualification.
