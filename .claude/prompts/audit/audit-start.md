# Audit Start Prompt

## Objective
Initialize a new website security audit session.

## Inputs
Target website URL
Audit scope
Constraints
Available evidence

## Instructions

1. Read the context files:

.claude/context/audit-context.md  
.claude/context/target-profile.md  
.claude/context/scope.md  
.claude/context/assumptions.md  

2. Confirm the audit scope and constraints.

3. Create or update the working audit session.

4. Identify the initial review areas:

- headers and TLS
- authentication entry points
- session indicators
- access control indicators
- input validation indicators
- logging indicators

5. Create a working audit note under:

audits/active/

## Output

Produce:

- audit overview
- known evidence
- unknown areas
- review plan