import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.utils import context_reader


class ContextReaderTests(unittest.TestCase):
    def test_check_authorization_returns_confirmed(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            context_dir = Path(tmpdir)
            (context_dir / "audit-context.md").write_text(
                "| Field | Value |\n"
                "|-------|-------|\n"
                "| Authorization Status | CONFIRMED |\n",
                encoding="utf-8",
            )

            with patch.object(context_reader, "CONTEXT_DIR", context_dir):
                self.assertEqual(context_reader.check_authorization(), context_reader.AUTH_CONFIRMED)

    def test_get_target_urls_reads_only_in_scope_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            context_dir = Path(tmpdir)
            (context_dir / "scope.md").write_text(
                "## In-Scope Targets\n"
                "- https://app.example.com\n"
                "- https://api.example.com\n"
                "## Out-of-Scope Items\n"
                "- https://legacy.example.com\n",
                encoding="utf-8",
            )

            with patch.object(context_reader, "CONTEXT_DIR", context_dir):
                self.assertEqual(
                    context_reader.get_target_urls(),
                    ["https://app.example.com", "https://api.example.com"],
                )


if __name__ == "__main__":
    unittest.main()
