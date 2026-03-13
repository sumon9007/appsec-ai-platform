import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.workflows.passive_web_audit import run_passive_web_audit


class PassiveWebAuditTests(unittest.TestCase):
    def test_workflow_requires_confirmed_authorization(self) -> None:
        with patch("src.workflows.passive_web_audit.check_authorization", return_value="NOT_CONFIRMED"):
            with self.assertRaises(RuntimeError):
                run_passive_web_audit(urls=["https://app.example.com"])

    def test_workflow_writes_findings_for_tool_results(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            register_path = Path(tmpdir) / "findings-register.md"
            session_path = Path(tmpdir) / "session.md"

            headers_results = [
                {
                    "check": "Content-Security-Policy (CSP)",
                    "assessment": "MISSING",
                    "severity": "Medium",
                    "confidence": "high",
                    "detail": "No Content-Security-Policy header found.",
                    "recommendation": "Add a restrictive CSP.",
                    "url": "https://app.example.com",
                    "evid_label": "EVID-2026-03-13-001",
                    "domain": "Security Headers",
                }
            ]
            tls_results = [
                {
                    "check": "TLS — Cipher Suite Enumeration",
                    "assessment": "REVIEW_GAP",
                    "severity": "Info",
                    "confidence": "low",
                    "detail": "Only the negotiated cipher is known.",
                    "recommendation": "Run authorized active TLS scanning.",
                    "url": "https://app.example.com",
                    "evid_label": "EVID-2026-03-13-002",
                    "domain": "TLS / Certificate",
                }
            ]

            with patch("src.workflows.passive_web_audit.check_authorization", return_value="CONFIRMED"), patch(
                "src.workflows.passive_web_audit.get_target_urls",
                return_value=["https://app.example.com"],
            ), patch(
                "src.workflows.passive_web_audit.get_audit_id",
                return_value="AUDIT-2026-001",
            ), patch(
                "src.workflows.passive_web_audit.get_auditor_name",
                return_value="Tester",
            ), patch(
                "src.workflows.passive_web_audit.get_testing_mode",
                return_value="Passive review only",
            ), patch(
                "src.workflows.passive_web_audit.HeadersAudit.run",
                return_value=headers_results,
            ), patch(
                "src.workflows.passive_web_audit.TLSAudit.run",
                return_value=tls_results,
            ), patch(
                "src.workflows.passive_web_audit._write_session_record",
                return_value=session_path,
            ):
                summary = run_passive_web_audit(register_path=register_path)

            self.assertEqual(len(summary.findings_written), 2)
            self.assertEqual(summary.session_path, session_path)

            content = register_path.read_text(encoding="utf-8")
            self.assertIn("Content-Security-Policy (CSP) on https://app.example.com", content)
            self.assertIn("TLS — Cipher Suite Enumeration on https://app.example.com", content)
            self.assertIn("review-gap", content)


if __name__ == "__main__":
    unittest.main()
