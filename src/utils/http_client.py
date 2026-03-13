"""
http_client.py — Thin passive HTTP client for audit evidence collection.

Principles:
- GET only (passive review — no payload injection)
- Captures full redirect chain
- Hard timeouts enforced
- SSL errors surfaced clearly with remediation guidance
- One instance shared across all tools in a session
"""

import logging
from typing import Optional
from urllib.parse import urlparse

import requests
from requests import Response, Session

from src.config.settings import MAX_REDIRECTS, REQUEST_TIMEOUT, SSL_VERIFY, USER_AGENT

logger = logging.getLogger(__name__)


class HttpClient:
    """Passive HTTP client for audit evidence collection."""

    def __init__(
        self,
        timeout: int = REQUEST_TIMEOUT,
        user_agent: str = USER_AGENT,
        max_redirects: int = MAX_REDIRECTS,
        ssl_verify: bool = SSL_VERIFY,
    ) -> None:
        self._timeout = timeout
        self._ssl_verify = ssl_verify
        self._max_redirects = max_redirects
        self._session = Session()
        self._session.headers.update({"User-Agent": user_agent})
        self._session.max_redirects = max_redirects

        if not ssl_verify:
            logger.warning(
                "SSL verification is DISABLED. "
                "Only use this against non-production environments with self-signed certificates."
            )
            # Suppress the urllib3 InsecureRequestWarning when verify=False
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get(
        self,
        url: str,
        allow_redirects: bool = True,
        capture_chain: bool = True,
        **kwargs,
    ) -> Optional[Response]:
        """
        Perform a GET request and return the Response.

        If capture_chain is True, response.history will include all
        intermediate redirect responses (standard requests behaviour).

        Returns None on connection error — caller must handle the None case.
        """
        try:
            response = self._session.get(
                url,
                timeout=self._timeout,
                verify=self._ssl_verify,
                allow_redirects=allow_redirects,
                **kwargs,
            )
            self._warn_on_http_downgrade(response)
            return response

        except requests.exceptions.SSLError as exc:
            parsed = urlparse(url)
            logger.error(
                "SSL certificate validation failed for %s: %s\n"
                "Remediation: If this is a staging environment with a self-signed certificate, "
                "set AUDIT_SSL_VERIFY=false in your .env file. "
                "NEVER disable SSL verification against production targets.",
                parsed.netloc,
                exc,
            )
            return None

        except requests.exceptions.ConnectionError as exc:
            logger.error(
                "Connection failed for %s: %s\n"
                "Remediation: Verify the target URL in .claude/context/scope.md is reachable "
                "from this machine and that no firewall or proxy is blocking the connection.",
                url,
                exc,
            )
            return None

        except requests.exceptions.Timeout:
            logger.error(
                "Request to %s timed out after %ds.\n"
                "Remediation: Increase AUDIT_REQUEST_TIMEOUT in .env or check network latency.",
                url,
                self._timeout,
            )
            return None

        except requests.exceptions.TooManyRedirects:
            logger.error(
                "Too many redirects for %s (limit: %d).\n"
                "Remediation: Increase AUDIT_MAX_REDIRECTS in .env or investigate the redirect loop.",
                url,
                self._max_redirects,
            )
            return None

        except requests.exceptions.RequestException as exc:
            logger.error("Unexpected request error for %s: %s", url, exc)
            return None

    def _warn_on_http_downgrade(self, response: Response) -> None:
        """Warn if any redirect in the chain downgrades from HTTPS to HTTP."""
        for r in response.history:
            location = r.headers.get("Location", "")
            if r.url.startswith("https://") and location.startswith("http://"):
                logger.warning(
                    "HTTPS→HTTP redirect detected: %s → %s — "
                    "this may indicate a misconfigured HSTS policy or mixed-content issue.",
                    r.url,
                    location,
                )

    def close(self) -> None:
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
