"""Tests for the parsers module."""
import pytest
from src.parsers.cookie_parser import parse_set_cookie_header
from src.parsers.jwt_parser import decode_jwt, find_jwts_in_text


# ── Cookie parser tests ───────────────────────────────────────────────────────

def test_parse_cookie_with_all_attributes():
    header = "session=abc123; Path=/; Secure; HttpOnly; SameSite=Strict"
    cookie = parse_set_cookie_header(header)
    assert cookie is not None
    assert cookie.name == "session"
    assert cookie.secure is True
    assert cookie.httponly is True
    assert cookie.samesite == "Strict"


def test_parse_cookie_missing_flags():
    header = "token=xyz; Path=/"
    cookie = parse_set_cookie_header(header)
    assert cookie.secure is False
    assert cookie.httponly is False
    assert cookie.samesite is None


def test_session_cookie_detection():
    header = "JSESSIONID=abc123; Path=/"
    cookie = parse_set_cookie_header(header)
    assert cookie.is_session_cookie is True


def test_non_session_cookie():
    header = "theme=dark; Path=/"
    cookie = parse_set_cookie_header(header)
    assert cookie.is_session_cookie is False


def test_samesite_none_without_secure():
    header = "tracking=abc; SameSite=None"
    cookie = parse_set_cookie_header(header)
    assert cookie.samesite == "None"
    assert cookie.secure is False


# ── JWT parser tests ──────────────────────────────────────────────────────────

def test_decode_jwt_alg_none():
    # Build a JWT with alg:none
    import base64, json
    header = base64.urlsafe_b64encode(json.dumps({"alg": "none", "typ": "JWT"}).encode()).rstrip(b"=").decode()
    payload = base64.urlsafe_b64encode(json.dumps({"sub": "1234", "name": "test"}).encode()).rstrip(b"=").decode()
    token = f"{header}.{payload}."
    jwt = decode_jwt(token)
    assert jwt.alg_is_none is True
    assert jwt.algorithm == "none"


def test_decode_jwt_with_exp():
    import base64, json, time
    header = base64.urlsafe_b64encode(json.dumps({"alg": "RS256", "typ": "JWT"}).encode()).rstrip(b"=").decode()
    future_exp = int(time.time()) + 3600
    payload = base64.urlsafe_b64encode(json.dumps({"sub": "1234", "exp": future_exp}).encode()).rstrip(b"=").decode()
    token = f"{header}.{payload}.fakesignature"
    jwt = decode_jwt(token)
    assert jwt.is_expired is False
    assert jwt.days_until_expiry is not None and jwt.days_until_expiry >= 0


def test_find_jwts_in_text():
    import base64, json
    header = base64.urlsafe_b64encode(json.dumps({"alg": "RS256"}).encode()).rstrip(b"=").decode()
    payload = base64.urlsafe_b64encode(json.dumps({"sub": "1"}).encode()).rstrip(b"=").decode()
    token = f"{header}.{payload}.fakesig"
    text = f"Authorization: Bearer {token}"
    found = find_jwts_in_text(text)
    assert len(found) == 1
