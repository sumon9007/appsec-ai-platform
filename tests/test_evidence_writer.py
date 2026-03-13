"""Tests for the evidence writer."""
import pytest
from pathlib import Path
from unittest.mock import patch
from src.utils.evidence_writer import next_evid_label, write_evidence, _redact_sensitive


def test_redact_private_key():
    content = "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA..."
    redacted, was_redacted = _redact_sensitive(content)
    assert was_redacted is True
    assert "PRIVATE KEY" not in redacted
    assert "[REDACTED" in redacted


def test_redact_bearer_token():
    content = "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.longpayload"
    redacted, was_redacted = _redact_sensitive(content)
    assert was_redacted is True


def test_no_redaction_needed():
    content = "HTTP/1.1 200 OK\nContent-Type: text/html\n\nHello World"
    redacted, was_redacted = _redact_sensitive(content)
    assert was_redacted is False
    assert redacted == content


def test_evid_label_format(tmp_path):
    with patch("src.utils.evidence_writer.EVIDENCE_RAW_DIR", tmp_path):
        label = next_evid_label("2026-03-13")
        assert label == "EVID-2026-03-13-001"


def test_evid_label_increments(tmp_path):
    with patch("src.utils.evidence_writer.EVIDENCE_RAW_DIR", tmp_path):
        # Create a dummy evidence file for today
        (tmp_path / "EVID-2026-03-13-001-test.md").write_text("test")
        label = next_evid_label("2026-03-13")
        assert label == "EVID-2026-03-13-002"


def test_write_evidence_creates_file(tmp_path):
    with patch("src.utils.evidence_writer.EVIDENCE_RAW_DIR", tmp_path):
        label, file_path = write_evidence(
            description="Test evidence item",
            domain="Security Headers",
            evidence_type="HTTP Capture",
            content="HTTP/1.1 200 OK\nServer: nginx",
            collector="test-auditor",
            target="https://example.com",
            observations="Server header present.",
            today="2026-03-13",
        )
        assert label.startswith("EVID-2026-03-13")
        assert file_path.exists()
        content = file_path.read_text()
        assert label in content
        assert "test-auditor" in content
