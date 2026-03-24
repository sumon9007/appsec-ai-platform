"""
settings.py — Central configuration loaded from environment / .env file.

All magic strings and configurable constants live here.
Tools import from this module; nothing imports from .env directly.
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover - dependency-free fallback for fresh environments
    def load_dotenv(*_args, **_kwargs):
        return False

# Locate the project root by walking up from this file until .claude/ is found.
def _find_project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / ".claude").is_dir():
            return parent
    # Fallback: three levels up from src/config/settings.py → project root
    return Path(__file__).resolve().parents[2]


PROJECT_ROOT = _find_project_root()

# Load .env from project root (silently ignored if absent)
load_dotenv(PROJECT_ROOT / ".env")


def _optional_path(key: str):
    """Return Path if the env var is set and non-empty, else None."""
    val = os.getenv(key, "").strip()
    return Path(val) if val else None


# ── HTTP client ───────────────────────────────────────────────────────────────
REQUEST_TIMEOUT: int = int(os.getenv("AUDIT_REQUEST_TIMEOUT", "15"))
USER_AGENT: str = os.getenv("AUDIT_USER_AGENT", "appsec-audit-tool/1.0")
MAX_REDIRECTS: int = int(os.getenv("AUDIT_MAX_REDIRECTS", "5"))
SSL_VERIFY: bool = os.getenv("AUDIT_SSL_VERIFY", "true").lower() != "false"

# ── Identity ──────────────────────────────────────────────────────────────────
DEFAULT_AUDITOR: str = os.getenv("AUDIT_DEFAULT_AUDITOR", "unknown-auditor")

# ── Audit run defaults (tagged from .env / CLI fallback) ─────────────────────
_target_urls_raw: str = os.getenv("AUDIT_TARGET_URLS", "")
DEFAULT_TARGET_URLS: list = [u.strip() for u in _target_urls_raw.split(",") if u.strip()]

DEFAULT_REGISTER_PATH_ENV = _optional_path("AUDIT_REGISTER_PATH")
DEFAULT_MANIFEST_PATH = _optional_path("AUDIT_MANIFEST_PATH")
DEFAULT_SPEC_PATH = _optional_path("AUDIT_SPEC_PATH")
DEFAULT_SCAN_PATH = _optional_path("AUDIT_SCAN_PATH")
DEFAULT_MAX_CRAWL_PAGES: int = int(os.getenv("AUDIT_MAX_CRAWL_PAGES", "30"))

# ── Report defaults ───────────────────────────────────────────────────────────
DEFAULT_TARGET_NAME: str = os.getenv("AUDIT_TARGET_NAME", "")
DEFAULT_REPORT_VERSION: str = os.getenv("AUDIT_REPORT_VERSION", "DRAFT v0.1")

# ── OSV dependency API ────────────────────────────────────────────────────────
OSV_API_BASE_URL: str = os.getenv("OSV_API_BASE_URL", "https://api.osv.dev/v1")
OSV_BATCH_SIZE: int = 100         # packages per batch request
OSV_INTER_BATCH_DELAY: float = 0.5  # seconds between batches

# ── Engagement isolation ───────────────────────────────────────────────────────
# Set ACTIVE_ENGAGEMENT to the engagement folder name (e.g. AUDIT-2026-DR-001).
# When set, all data paths resolve inside engagements/<ACTIVE_ENGAGEMENT>/.
# When unset, falls back to the legacy single-engagement layout for compatibility.
ACTIVE_ENGAGEMENT: str = os.getenv("ACTIVE_ENGAGEMENT", "").strip()

# ── Workspace paths (always resolved from project root) ───────────────────────
if ACTIVE_ENGAGEMENT:
    _engagement_dir = PROJECT_ROOT / "engagements" / ACTIVE_ENGAGEMENT
    CONTEXT_DIR       = _engagement_dir / "context"
    EVIDENCE_RAW_DIR  = _engagement_dir / "evidence" / "raw"
    AUDIT_RUNS_ACTIVE_DIR = _engagement_dir / "audit-runs" / "active"
else:
    # Legacy fallback: single-engagement layout
    CONTEXT_DIR       = PROJECT_ROOT / ".claude" / "context"
    EVIDENCE_RAW_DIR  = PROJECT_ROOT / "evidence" / "raw"
    AUDIT_RUNS_ACTIVE_DIR = PROJECT_ROOT / "audit-runs" / "active"

FINDINGS_REGISTER_FILENAME = "findings-register.md"

# Default findings register path — env override takes precedence, then workspace default
DEFAULT_REGISTER_PATH = DEFAULT_REGISTER_PATH_ENV or (AUDIT_RUNS_ACTIVE_DIR / FINDINGS_REGISTER_FILENAME)

# ── Severity vocabulary (workspace-defined) ────────────────────────────────────
VALID_SEVERITIES = {"Critical", "High", "Medium", "Low", "Info"}
VALID_STATUSES = {"confirmed", "suspected", "review-gap", "mitigated", "accepted-risk"}
VALID_CONFIDENCES = {"high", "medium", "low"}
