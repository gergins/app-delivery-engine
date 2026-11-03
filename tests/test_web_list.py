import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ade.generator import plan, generate, validate

SPEC = {"schema_version": "1.0", "slug": "my-picks", "title": 'My <Picks> & More',
        "outcome": "Add and revisit recommendations", "profile": "web-list"}

class WebListGeneratorTests(unittest.TestCase):
    def test_unknown_profile_rejected(self):
        with self.assertRaises(ValueError):
            validate({**SPEC, "profile": "unknown"})

    def test_profile_is_deterministic_and_html_is_escaped(self):
        a, b = plan(SPEC), plan(SPEC)
        self.assertEqual(a, b)
        self.assertIn("&lt;Picks&gt; &amp; More", a["app/index.html"])
        self.assertIn("tests/test_browser.py", a)
        self.assertNotIn("app/core.py", a)

    def test_legacy_spec_remains_compatible(self):
        old = {k: v for k, v in SPEC.items() if k != "profile"}
        self.assertIn("app/core.py", plan(old))
        self.assertEqual(json.loads(plan(old)["project-manifest.json"])["profile"], "cli")

    def test_generated_application_unit_and_http_tests(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "app"
            generate(SPEC, dest)
            self.assertEqual(json.loads((dest / "project-manifest.json").read_text())["status"], "local-web-benchmark")
            done = subprocess.run([sys.executable, "-m", "unittest", "discover",
                                   "-s", "tests", "-p", "test_app.py", "-v"],
                                   cwd=dest, capture_output=True, text=True, timeout=30)
            self.assertEqual(done.returncode, 0, done.stdout + done.stderr)

    def test_two_independent_applications_from_distinct_specs(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "first"
            b = Path(tmp) / "second"
            spec_a = {**SPEC, "slug": "alpha", "title": "Alpha Picks"}
            spec_b = {**SPEC, "slug": "beta", "title": "Beta Notes"}
            self.assertNotEqual(plan(spec_a)["app/index.html"], plan(spec_b)["app/index.html"])
            generate(spec_a, a)
            generate(spec_b, b)
            self.assertEqual(json.loads((a / "project-manifest.json").read_text())["slug"], "alpha")
            self.assertEqual(json.loads((b / "project-manifest.json").read_text())["slug"], "beta")
            self.assertIn("Alpha Picks", (a / "app/index.html").read_text())
            self.assertIn("Beta Notes", (b / "app/index.html").read_text())
            self.assertEqual((a / "app/server.py").read_bytes(), (b / "app/server.py").read_bytes())

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "app"
            generate(SPEC, dest)
            (dest / "app/index.html").write_text("user modification", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                generate(SPEC, dest)
            self.assertEqual((dest / "app/index.html").read_text(encoding="utf-8"), "user modification")

if __name__ == "__main__":
    unittest.main()
