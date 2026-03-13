"""
session_manager.py — Authenticated session orchestration for multi-role audit workflows.

Manages login, session maintenance, and logout for approved test accounts.
Credentials are loaded from CredentialStore (env vars only — never hardcoded).

This module only performs authenticated requests when:
1. Authorization is CONFIRMED in audit-context.md
2. A valid TestCredential is available

All authenticated activity is logged for audit trail purposes.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

import requests

from src.auth.credential_store import TestCredential
from src.config.settings import REQUEST_TIMEOUT, SSL_VERIFY, USER_AGENT
from src.policies.authorization import AuthorizationGrant, require_confirmed

logger = logging.getLogger(__name__)


@dataclass
class AuthenticatedSession:
    """
    An active authenticated session with associated metadata.
    """
    role: str
    username: str
    base_url: str
    session: requests.Session
    cookies_captured: List[Dict[str, Any]] = field(default_factory=list)
    tokens_captured: List[str] = field(default_factory=list)  # truncated for safety
    login_url: str = ""
    auth_method: str = ""   # form, bearer, basic, cookie

    def get(self, path: str, **kwargs) -> Optional[requests.Response]:
        """Make an authenticated GET request."""
        url = urljoin(self.base_url, path)
        try:
            return self.session.get(url, timeout=REQUEST_TIMEOUT, verify=SSL_VERIFY, **kwargs)
        except Exception as exc:
            logger.error("Authenticated GET failed for %s: %s", url, exc)
            return None

    def close(self) -> None:
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class SessionManager:
    """
    Orchestrates authenticated sessions for audit workflows.

    Supports:
    - Form-based login (POST username/password)
    - Bearer token (set from env var or credential store)
    - Basic auth
    """

    def __init__(self, grant: AuthorizationGrant) -> None:
        require_confirmed(grant)
        self._grant = grant

    def login_form(
        self,
        base_url: str,
        login_path: str,
        credential: TestCredential,
        username_field: str = "username",
        password_field: str = "password",
        extra_fields: Optional[Dict[str, str]] = None,
    ) -> Optional[AuthenticatedSession]:
        """
        Authenticate via a standard HTML form submission.

        Returns an AuthenticatedSession on success, None on failure.
        Does NOT raise — failed login is recorded as a review gap.
        """
        login_url = urljoin(base_url, login_path)
        session = requests.Session()
        session.headers["User-Agent"] = USER_AGENT

        payload = {
            username_field: credential.username,
            password_field: credential.password,
        }
        if extra_fields:
            payload.update(extra_fields)

        try:
            # First GET the login page to capture any CSRF tokens
            pre_response = session.get(login_url, timeout=REQUEST_TIMEOUT, verify=SSL_VERIFY)
            csrf = self._extract_csrf(pre_response.text)
            if csrf:
                payload["csrf_token"] = csrf
                payload["_token"] = csrf  # Laravel convention
                payload["csrfmiddlewaretoken"] = csrf  # Django convention

            response = session.post(login_url, data=payload, timeout=REQUEST_TIMEOUT, verify=SSL_VERIFY)

            # Heuristic: login succeeded if we got redirected away from the login path
            # or got a 200 without an obvious login form in the body
            if response.status_code in (200, 302, 303):
                # Check we're not still on the login page
                if login_path in response.url and "error" in response.text.lower():
                    logger.warning(
                        "Form login appears to have failed for %s at %s — still on login page.",
                        credential.username,
                        login_url,
                    )
                    session.close()
                    return None

                auth_session = AuthenticatedSession(
                    role=credential.role,
                    username=credential.username,
                    base_url=base_url,
                    session=session,
                    login_url=login_url,
                    auth_method="form",
                )
                # Capture cookie names (not values) for evidence
                for cookie in session.cookies:
                    auth_session.cookies_captured.append({
                        "name": cookie.name,
                        "secure": cookie.secure,
                        "domain": cookie.domain,
                    })
                # Check for bearer token in response
                auth_header = response.headers.get("Authorization", "")
                if auth_header.startswith("Bearer "):
                    auth_session.tokens_captured.append(auth_header[:30] + "...[TRUNCATED]")

                logger.info(
                    "Authenticated session established: role=%s, url=%s",
                    credential.role,
                    base_url,
                )
                return auth_session

        except requests.exceptions.RequestException as exc:
            logger.error("Form login request failed for %s: %s", login_url, exc)

        return None

    def login_bearer(
        self,
        base_url: str,
        token: str,
        role: str = "api-user",
    ) -> AuthenticatedSession:
        """Create an authenticated session using a pre-supplied Bearer token."""
        session = requests.Session()
        session.headers["User-Agent"] = USER_AGENT
        session.headers["Authorization"] = f"Bearer {token}"
        return AuthenticatedSession(
            role=role,
            username="token-based",
            base_url=base_url,
            session=session,
            auth_method="bearer",
            tokens_captured=[token[:20] + "...[TRUNCATED]"],
        )

    def login_basic(
        self,
        base_url: str,
        credential: TestCredential,
    ) -> AuthenticatedSession:
        """Create an authenticated session using HTTP Basic Auth."""
        session = requests.Session()
        session.headers["User-Agent"] = USER_AGENT
        session.auth = (credential.username, credential.password)
        return AuthenticatedSession(
            role=credential.role,
            username=credential.username,
            base_url=base_url,
            session=session,
            auth_method="basic",
        )

    @staticmethod
    def _extract_csrf(html: str) -> Optional[str]:
        """Extract a CSRF token from an HTML form."""
        import re
        patterns = [
            re.compile(r'name=["\']csrf[_-]token["\'][^>]+value=["\']([^"\']+)["\']', re.IGNORECASE),
            re.compile(r'name=["\']_token["\'][^>]+value=["\']([^"\']+)["\']', re.IGNORECASE),
            re.compile(r'name=["\']csrfmiddlewaretoken["\'][^>]+value=["\']([^"\']+)["\']', re.IGNORECASE),
        ]
        for pattern in patterns:
            match = pattern.search(html)
            if match:
                return match.group(1)
        return None
