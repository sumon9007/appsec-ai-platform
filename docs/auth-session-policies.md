# Auth, Session, and Policies

## Credential Handling

`src/auth/credential_store.py` loads credentials from environment variables.

Conventions:

- `AUDIT_USERNAME_<ROLE>`
- `AUDIT_PASSWORD_<ROLE>`
- `AUDIT_MFA_<ROLE>`

Credentials are intended to:

- remain in memory
- stay out of source control
- stay out of evidence files and logs

## Session Management

`src/session/session_manager.py` provides:

- form login
- bearer-token session setup
- basic-auth session setup

It captures limited metadata such as:

- role
- username
- cookie names and attributes
- truncated tokens

## Authorization Modes

Defined modes:

- `Passive review only`
- `Passive + Active Testing on Staging`
- `Full active testing authorized`

Policy functions:

- `load_authorization()`
- `require_confirmed()`
- `require_active_testing()`

## Stop Conditions

`src/policies/stop_conditions.py` detects:

- private keys
- payment card patterns
- SSNs
- AWS access keys
- plaintext password patterns
- compromise indicators such as defacement or web-shell markers

## Safety Constraints

- Workflows require confirmed authorization before running.
- Active testing requires an explicit stronger authorization mode.
- Evidence writer redacts several sensitive patterns before storage.

Doc/code mismatch:
- Stop conditions are well defined in policy code, but not consistently called from each tool path.

Needs verification:
- There is no single global middleware-like enforcement layer ensuring every response or file payload passes through stop-condition checks.
