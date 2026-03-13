"""
entities.py — Core typed data model for the appsec-ai-platform.

All workflow components exchange these dataclasses rather than raw dicts,
providing stable schemas for storage, reporting, and serialization.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


# ── Enumerations (workspace vocabulary) ──────────────────────────────────────

class Severity(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class FindingStatus(str, Enum):
    CONFIRMED = "confirmed"
    SUSPECTED = "suspected"
    REVIEW_GAP = "review-gap"
    MITIGATED = "mitigated"
    ACCEPTED_RISK = "accepted-risk"
    CLOSED = "closed"


class AuthorizationMode(str, Enum):
    PASSIVE = "Passive review only"
    ACTIVE_STAGING = "Passive + Active Testing on Staging"
    ACTIVE_FULL = "Full active testing authorized"


class Environment(str, Enum):
    PRODUCTION = "Production"
    STAGING = "Staging"
    QA = "QA"
    DEVELOPMENT = "Development"
    UNKNOWN = "Unknown"


class AuditRunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"
    ABORTED = "aborted"


# ── Core Entities ─────────────────────────────────────────────────────────────

@dataclass
class Target:
    """A scoped audit target."""
    url: str
    name: str = ""
    environment: Environment = Environment.UNKNOWN
    notes: str = ""


@dataclass
class AuthorizationGrant:
    """Records the authorization basis for an audit engagement."""
    status: str                   # CONFIRMED / PENDING / NOT CONFIRMED
    authorized_by: str = ""
    authorization_date: str = ""
    authorization_reference: str = ""
    mode: AuthorizationMode = AuthorizationMode.PASSIVE

    @property
    def is_confirmed(self) -> bool:
        return self.status.upper() == "CONFIRMED"

    @property
    def allows_active_testing(self) -> bool:
        return self.is_confirmed and self.mode != AuthorizationMode.PASSIVE


@dataclass
class TestAccount:
    """
    Reference to a provided test account. No passwords stored here.
    Credentials must be supplied via environment variables or .env.
    """
    username: str
    role: str
    environment: Environment = Environment.STAGING
    credential_env_var: str = ""   # e.g., "AUDIT_PASSWORD_ADMIN"
    notes: str = ""


@dataclass
class Evidence:
    """Metadata record for a collected evidence item."""
    label: str                    # EVID-YYYY-MM-DD-NNN
    date_collected: str
    collector: str
    evidence_type: str
    domain: str
    target: str
    file_path: str
    related_finding: str = "PENDING"
    description: str = ""


@dataclass
class Finding:
    """A normalized security finding."""
    find_id: str                   # FIND-NNN
    title: str
    domain: str
    severity: Severity
    confidence: Confidence
    target: str
    evidence_labels: List[str]
    observation: str
    risk: str
    recommendation: str
    acceptance_criteria: str
    status: FindingStatus
    review_type: str               # passive / active / document review / configuration review
    opened: str
    closed: str = "open"
    closure_evidence: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class ControlCheck:
    """The result of a single security control check from a tool."""
    check: str
    domain: str
    assessment: str               # PASS / FAIL / MISSING / WEAK / VULNERABLE / REVIEW_GAP
    severity: Optional[Severity]
    confidence: Confidence
    target: str
    detail: str
    recommendation: Optional[str]
    evidence_label: Optional[str] = None
    error: Optional[str] = None


@dataclass
class ReviewGap:
    """A domain area that could not be assessed with available evidence."""
    domain: str
    description: str
    reason: str
    requires: str = ""            # e.g., "authenticated test account", "authorized active testing"


@dataclass
class AuditRun:
    """
    State record for a single audit execution.
    Written to audit-runs/active/run-state.json for resumability.
    """
    run_id: str
    audit_id: str
    auditor: str
    authorization: AuthorizationGrant
    targets: List[Target]
    status: AuditRunStatus = AuditRunStatus.PENDING
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    tools_run: List[str] = field(default_factory=list)
    findings_written: List[str] = field(default_factory=list)   # list of FIND-NNN IDs
    evidence_written: List[str] = field(default_factory=list)   # list of EVID- labels
    errors: List[str] = field(default_factory=list)
    session_path: str = ""
