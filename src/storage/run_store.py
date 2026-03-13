"""
run_store.py — JSON-backed persistence for audit run state.

Allows workflows to resume safely after interruption and provides
a machine-readable audit trail of each automated run.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from uuid import uuid4

from src.config.settings import AUDIT_RUNS_ACTIVE_DIR
from src.models.entities import AuditRun, AuditRunStatus, AuthorizationGrant, Target

logger = logging.getLogger(__name__)

_RUN_STATE_FILENAME = "run-state.json"


def _run_state_path() -> Path:
    AUDIT_RUNS_ACTIVE_DIR.mkdir(parents=True, exist_ok=True)
    return AUDIT_RUNS_ACTIVE_DIR / _RUN_STATE_FILENAME


def _serialize_run(run: AuditRun) -> dict:
    return {
        "run_id": run.run_id,
        "audit_id": run.audit_id,
        "auditor": run.auditor,
        "status": run.status.value,
        "started_at": run.started_at.isoformat() if run.started_at else None,
        "ended_at": run.ended_at.isoformat() if run.ended_at else None,
        "targets": [{"url": t.url, "name": t.name, "environment": t.environment.value} for t in run.targets],
        "authorization_status": run.authorization.status,
        "authorization_mode": run.authorization.mode.value,
        "tools_run": run.tools_run,
        "findings_written": run.findings_written,
        "evidence_written": run.evidence_written,
        "errors": run.errors,
        "session_path": run.session_path,
    }


def save_run(run: AuditRun) -> None:
    """Persist the current run state to disk."""
    path = _run_state_path()
    try:
        path.write_text(json.dumps(_serialize_run(run), indent=2), encoding="utf-8")
    except OSError as exc:
        logger.error("Could not save run state to %s: %s", path, exc)


def load_run() -> Optional[AuditRun]:
    """
    Load the most recent run state from disk.
    Returns None if no run state exists or it cannot be parsed.
    """
    path = _run_state_path()
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        targets = [
            Target(url=t["url"], name=t.get("name", ""), environment=t.get("environment", "Unknown"))
            for t in data.get("targets", [])
        ]
        authorization = AuthorizationGrant(
            status=data.get("authorization_status", "NOT CONFIRMED"),
            mode=data.get("authorization_mode", "Passive review only"),
        )
        run = AuditRun(
            run_id=data["run_id"],
            audit_id=data.get("audit_id", ""),
            auditor=data.get("auditor", ""),
            authorization=authorization,
            targets=targets,
            status=AuditRunStatus(data.get("status", "pending")),
            tools_run=data.get("tools_run", []),
            findings_written=data.get("findings_written", []),
            evidence_written=data.get("evidence_written", []),
            errors=data.get("errors", []),
            session_path=data.get("session_path", ""),
        )
        if data.get("started_at"):
            run.started_at = datetime.fromisoformat(data["started_at"])
        if data.get("ended_at"):
            run.ended_at = datetime.fromisoformat(data["ended_at"])
        return run
    except (KeyError, ValueError, json.JSONDecodeError) as exc:
        logger.warning("Could not deserialize run state from %s: %s", path, exc)
        return None


def new_run(audit_id: str, auditor: str, authorization: AuthorizationGrant, targets: list) -> AuditRun:
    """Create and immediately persist a new AuditRun."""
    run = AuditRun(
        run_id=f"RUN-{datetime.now(tz=timezone.utc).strftime('%Y%m%d-%H%M%S')}-{uuid4().hex[:6].upper()}",
        audit_id=audit_id,
        auditor=auditor,
        authorization=authorization,
        targets=targets,
        status=AuditRunStatus.RUNNING,
        started_at=datetime.now(tz=timezone.utc),
    )
    save_run(run)
    return run


def complete_run(run: AuditRun) -> None:
    """Mark the run complete and persist."""
    run.status = AuditRunStatus.COMPLETE
    run.ended_at = datetime.now(tz=timezone.utc)
    save_run(run)


def fail_run(run: AuditRun, reason: str) -> None:
    """Mark the run failed, record reason, and persist."""
    run.status = AuditRunStatus.FAILED
    run.ended_at = datetime.now(tz=timezone.utc)
    run.errors.append(f"[FATAL] {reason}")
    save_run(run)
