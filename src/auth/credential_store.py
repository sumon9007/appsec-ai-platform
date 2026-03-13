"""
credential_store.py — Secure handling of test account credentials.

Credentials are NEVER stored in code or evidence files.
They are loaded from environment variables only and used in-memory.

Usage pattern:
    creds = CredentialStore.load("AUDIT_USERNAME_ADMIN", "AUDIT_PASSWORD_ADMIN", role="admin")
    session = SessionManager(http_client, creds)
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class TestCredential:
    """
    In-memory credential for an audit test account.
    Never written to disk, logs, or evidence files.
    """
    username: str
    password: str           # held in memory only — never stored
    role: str
    mfa_secret_env: str = ""   # env var containing TOTP secret if MFA is used


class CredentialStore:
    """
    Loads test credentials from environment variables.

    Convention:
        AUDIT_USERNAME_<ROLE>    — e.g., AUDIT_USERNAME_ADMIN
        AUDIT_PASSWORD_<ROLE>    — e.g., AUDIT_PASSWORD_ADMIN
        AUDIT_MFA_<ROLE>         — e.g., AUDIT_MFA_ADMIN (optional TOTP secret)
    """

    @staticmethod
    def load(
        username_env: str,
        password_env: str,
        role: str = "unknown",
        mfa_env: str = "",
    ) -> Optional[TestCredential]:
        """
        Load a test credential from environment variables.
        Returns None and logs a remediation message if variables are not set.
        """
        username = os.getenv(username_env, "")
        password = os.getenv(password_env, "")

        if not username or not password:
            missing = []
            if not username:
                missing.append(username_env)
            if not password:
                missing.append(password_env)
            logger.warning(
                "Test credentials not found for role '%s'. Missing env vars: %s. "
                "Remediation: Add the missing environment variables to your .env file. "
                "NEVER commit credentials to the repository.",
                role,
                ", ".join(missing),
            )
            return None

        return TestCredential(
            username=username,
            password=password,
            role=role,
            mfa_secret_env=mfa_env,
        )

    @staticmethod
    def load_for_role(role: str) -> Optional[TestCredential]:
        """
        Convenience method. Loads credentials using standard env var naming convention.
        Role 'admin' → AUDIT_USERNAME_ADMIN / AUDIT_PASSWORD_ADMIN
        """
        role_upper = role.upper()
        return CredentialStore.load(
            username_env=f"AUDIT_USERNAME_{role_upper}",
            password_env=f"AUDIT_PASSWORD_{role_upper}",
            role=role,
            mfa_env=f"AUDIT_MFA_{role_upper}",
        )

    @staticmethod
    def list_available_roles() -> list[str]:
        """Detect which roles have credentials configured via env vars."""
        roles = []
        for key in os.environ:
            if key.startswith("AUDIT_USERNAME_"):
                role = key[len("AUDIT_USERNAME_"):].lower()
                roles.append(role)
        return roles
