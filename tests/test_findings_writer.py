import tempfile
import unittest
from pathlib import Path

from src.utils.findings_writer import append_finding


class FindingsWriterTests(unittest.TestCase):
    def test_append_finding_updates_summary_and_detail_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            register_path = Path(tmpdir) / "findings-register.md"

            finding_id = append_finding(
                finding={
                    "title": "Missing CSP on https://app.example.com",
                    "domain": "Security Headers",
                    "severity": "Medium",
                    "confidence": "high",
                    "target": "https://app.example.com",
                    "evidence_labels": ["EVID-2026-03-13-001"],
                    "observation": "No Content-Security-Policy header found.",
                    "risk": "Browser-enforced XSS protections are reduced.",
                    "recommendation": "Add a restrictive CSP.",
                    "acceptance_criteria": "Headers-Advisory-1 — Missing Content-Security-Policy",
                    "status": "confirmed",
                    "review_type": "passive",
                },
                register_path=register_path,
            )

            self.assertEqual(finding_id, "FIND-001")

            content = register_path.read_text(encoding="utf-8")
            self.assertIn("| FIND-001 | Missing CSP on https://app.example.com |", content)
            self.assertIn("### FIND-001", content)
            self.assertIn("**Severity:** Medium", content)


if __name__ == "__main__":
    unittest.main()
