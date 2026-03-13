"""Tests for stop condition detection."""
import pytest
from src.policies.stop_conditions import (
    StopConditionTriggered,
    check_all,
    check_for_sensitive_data,
    check_for_compromise_indicators,
)


def test_detect_private_key():
    content = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA..."
    result = check_for_sensitive_data(content, "test")
    assert result == "private_key"


def test_detect_aws_key():
    content = "AKIAIOSFODNN7EXAMPLE"
    result = check_for_sensitive_data(content, "test")
    assert result == "aws_access_key"


def test_no_sensitive_data():
    content = "HTTP/1.1 200 OK\nContent-Type: text/html\n<html><body>Hello</body></html>"
    result = check_for_sensitive_data(content, "test")
    assert result is None


def test_detect_compromise_indicator():
    content = "hacked by some_group"
    result = check_for_compromise_indicators(content, "test")
    assert result is not None


def test_check_all_raises_on_detection():
    content = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE..."
    with pytest.raises(StopConditionTriggered):
        check_all(content, "test-source", raise_on_detection=True)


def test_check_all_no_raise():
    content = "Normal response content with no sensitive data."
    triggered = check_all(content, "test-source", raise_on_detection=False)
    assert triggered == []
