"""
cookie_parser.py — Parse Set-Cookie response headers into structured attributes.

Used by cookie_audit.py and session_jwt_audit.py.
Does not access the network — operates on header strings only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ParsedCookie:
    """Structured representation of a single Set-Cookie value."""
    name: str
    value: str                        # raw value (may be truncated for evidence)
    secure: bool = False
    httponly: bool = False
    samesite: Optional[str] = None    # "Strict" / "Lax" / "None" / None (absent)
    path: str = "/"
    domain: Optional[str] = None
    expires: Optional[str] = None     # raw expires string
    max_age: Optional[int] = None     # seconds
    raw: str = ""                     # original Set-Cookie header value

    @property
    def is_session_cookie(self) -> bool:
        """Heuristic: likely a session cookie if name matches common patterns."""
        session_names = {
            "session", "sessionid", "sess", "auth", "token", "sid",
            "jsessionid", "phpsessid", "connect.sid", "asp.net_sessionid",
            "rails.session", "_session", "user_session", "authtoken",
        }
        return self.name.lower() in session_names or self.name.lower().startswith("sess")

    @property
    def is_persistent(self) -> bool:
        """True if the cookie has an expiry or max-age (not session-scoped)."""
        return bool(self.expires or self.max_age is not None)


def parse_set_cookie_header(header_value: str) -> Optional[ParsedCookie]:
    """
    Parse a single Set-Cookie header value into a ParsedCookie.
    Returns None if the header is malformed.
    """
    if not header_value:
        return None

    parts = [p.strip() for p in header_value.split(";")]
    if not parts:
        return None

    # First part is name=value
    first = parts[0]
    if "=" in first:
        name, _, value = first.partition("=")
    else:
        name = first
        value = ""

    name = name.strip()
    value = value.strip()
    if not name:
        return None

    cookie = ParsedCookie(name=name, value=value[:64], raw=header_value)  # truncate value for safety

    for attr in parts[1:]:
        lower = attr.lower()
        if lower == "secure":
            cookie.secure = True
        elif lower == "httponly":
            cookie.httponly = True
        elif lower.startswith("samesite="):
            cookie.samesite = attr.split("=", 1)[1].strip().capitalize()
        elif lower.startswith("path="):
            cookie.path = attr.split("=", 1)[1].strip()
        elif lower.startswith("domain="):
            cookie.domain = attr.split("=", 1)[1].strip()
        elif lower.startswith("expires="):
            cookie.expires = attr.split("=", 1)[1].strip()
        elif lower.startswith("max-age="):
            try:
                cookie.max_age = int(attr.split("=", 1)[1].strip())
            except ValueError:
                pass

    return cookie


def parse_all_set_cookie_headers(headers: dict) -> List[ParsedCookie]:
    """
    Extract and parse all Set-Cookie headers from a response headers dict.
    requests combines multiple Set-Cookie values into one comma-separated string,
    but the response.cookies jar is more reliable. This parser handles both.
    """
    cookies = []
    # requests may give us a single string with all Set-Cookie values
    raw = headers.get("set-cookie", "")
    if raw:
        # Attempt naive split — works for most cases
        for part in raw.split(", "):
            if "=" in part and not part.strip().lower().startswith(
                ("expires=", "path=", "domain=", "samesite=", "secure", "httponly", "max-age=")
            ):
                parsed = parse_set_cookie_header(part)
                if parsed:
                    cookies.append(parsed)
    return cookies
