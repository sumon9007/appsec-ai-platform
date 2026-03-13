# Setup and Installation

## Prerequisites

- Python 3.10+ recommended
- Network access if you want dependency CVE lookups or live HTTP/TLS checks
- A writable local workspace

## Install Steps

```bash
cd /home/suruz/claude-workspace/01-PROJECTS/appsec-ai-platform
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Dependencies

The project currently uses:

- `requests`
- `python-dotenv`
- `rich`
- `click`
- `packaging`
- `beautifulsoup4`
- `pyyaml`
- `tomli` on older Python versions

## Environment Setup

Populate `.env` as needed:

- default auditor
- default target URLs
- findings register path
- manifest path
- API spec path
- secrets scan path
- report labels

## Context Setup

Before running workflows, review:

- `.claude/context/audit-context.md`
- `.claude/context/scope.md`
- `.claude/context/target-profile.md`
- `.claude/context/assumptions.md`

## Run Locally

```bash
python3 scripts/run_audit.py session status
python3 scripts/run_audit.py audit full --dry-run
python3 scripts/run_audit.py report technical
```

## Testing

The repository includes unit tests under `tests/`.

Needs verification:
- In this environment, `pytest` was not installed, so the suite could not be executed without additional setup.
