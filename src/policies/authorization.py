"""
authorization.py — Policy enforcement layer for audit authorization.

Wraps context_reader checks with typed returns and runtime enforcement.
This is the single point of truth for "can this action proceed?"
"""

from __future__ import annotations

import logging
from typing import List

from src.models.entities import AuthorizationGrant, AuthorizationMode
from src.utils.context_reader import (
    AUTH_CONFIRMED,
    check_authorization,
    get_target_urls,
    get_testing_mode,
)

logger = logging.getLogger(__name__)


class AuthorizationError(RuntimeError):
    """Raised when an action is attempted without confirmed authorization."""


def load_authorization() -> AuthorizationGrant:
    """
    Read the current authorization state from audit-context.md.
    Returns a typed AuthorizationGrant regardless of status.
    """
    from src.utils.context_reader import _extract_table_value, _read_file, CONTEXT_DIR

    status = check_authorization()
    testing_mode_str = get_testing_mode()

    # Map the free-text authorization scope to a typed mode
    mode = AuthorizationMode.PASSIVE
    lower = testing_mode_str.lower()
    if "active" in lower and "staging" in lower:
        mode = AuthorizationMode.ACTIVE_STAGING
    elif "full active" in lower or ("active" in lower and "production" in lower):
        mode = AuthorizationMode.ACTIVE_FULL

    # Read extra fields for the grant record
    content = _read_file(CONTEXT_DIR / "audit-context.md") or ""
    authorized_by = _extract_table_value(content, "Authorized By") or ""
    authorization_date = _extract_table_value(content, "Authorization Date") or ""
    authorization_reference = _extract_table_value(content, "Authorization Reference") or ""

    return AuthorizationGrant(
        status=status,
        authorized_by=authorized_by,
        authorization_date=authorization_date,
        authorization_reference=authorization_reference,
        mode=mode,
    )


def require_confirmed(grant: AuthorizationGrant) -> None:
    """
    Raise AuthorizationError if the grant is not CONFIRMED.
    Call this at the start of every workflow.
    """
    if not grant.is_confirmed:
        raise AuthorizationError(
            "AUTHORIZATION REQUIRED: Audit activity cannot begin until Authorization Status "
            "is CONFIRMED in .claude/context/audit-context.md. "
            "Per safety-authorization-rules.md Rule 1, no audit activity may proceed without "
            "written confirmed authorization."
        )


def require_active_testing(grant: AuthorizationGrant, feature: str = "") -> None:
    """
    Raise AuthorizationError if active testing is not authorized.
    Use before running any payload-injecting, brute-force, or fuzzing activity.
    """
    require_confirmed(grant)
    if not grant.allows_active_testing:
        feature_label = f" ({feature})" if feature else ""
        raise AuthorizationError(
            f"ACTIVE TESTING NOT AUTHORIZED{feature_label}: "
            "The current scope of authorization is passive review only. "
            "Active testing requires explicit written authorization documented in "
            ".claude/context/audit-context.md with Scope of Authorization specifying "
            "active testing permission and the target environment. "
            "Per safety-authorization-rules.md Rule 3."
        )


def in_scope_urls(grant: AuthorizationGrant) -> List[str]:
    """Return the list of in-scope URLs, enforcing that authorization is confirmed first."""
    require_confirmed(grant)
    return get_target_urls()
