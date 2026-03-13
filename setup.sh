#!/usr/bin/env bash
# =============================================================
# setup.sh — Bootstrap the Python environment for appsec-ai-platform
# Usage: bash setup.sh
# =============================================================

set -e

PYTHON=${PYTHON:-python3}
VENV_DIR=".venv"

echo "==> Checking Python version..."
$PYTHON --version

echo "==> Creating virtual environment in $VENV_DIR..."
$PYTHON -m venv "$VENV_DIR"

echo "==> Activating virtual environment..."
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "==> Upgrading pip..."
pip install --upgrade pip --quiet

echo "==> Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "==> Setup complete."
echo ""
echo "    To activate the environment in your shell:"
echo "    source $VENV_DIR/bin/activate"
echo ""
echo "    To run an audit:"
echo "    python scripts/run_audit.py audit headers-tls --url https://TARGET --auditor 'Your Name'"
echo ""
echo "    IMPORTANT: Populate .claude/context/audit-context.md with confirmed"
echo "    authorization before running any audit commands."
echo ""
