"""Actual one-command creation, smoke tests and fail-closed target handling."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ExecutableDemoTests(unittest.TestCase):
    def test_end_to_end_cli_creates_and_verifies_app(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "starter"
            proc = subprocess.run(
                [sys.executable, "-m", "ade.demo", str(destination)],
                cwd=ROOT, capture_output=True, text=True, timeout=45)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads(proc.stdout)
            self.assertEqual(result["result"], "local-demo-verified")
            self.assertEqual(result["local_tests"], "passed")
            self.assertFalse(result["remote_ci_verified"])
            self.assertFalse(result["merge_or_deploy_approved"])
            self.assertEqual(result["product_scope"], "unapproved")
            self.assertTrue((destination / "app" / "server.py").is_file())
            self.assertTrue((destination / "delivery" / "approvals.json").is_file())
            approvals = json.loads((destination / "delivery" / "approvals.json").read_text())
            self.assertFalse(approvals["merge"])
            self.assertFalse(approvals["deploy"])

    def test_existing_target_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "existing"
            destination.mkdir()
            marker = destination / "evidence.txt"
            marker.write_text("preserve")
            proc = subprocess.run(
                [sys.executable, "-m", "ade.demo", str(destination)],
                cwd=ROOT, capture_output=True, text=True, timeout=15)
            self.assertEqual(proc.returncode, 2)
            self.assertIn("STOP", proc.stderr)
            self.assertEqual(marker.read_text(), "preserve")

    def test_missing_parent_stops_without_creating(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "missing" / "app"
            proc = subprocess.run(
                [sys.executable, "-m", "ade.demo", str(destination)],
                cwd=ROOT, capture_output=True, text=True, timeout=15)
            self.assertEqual(proc.returncode, 2)
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
