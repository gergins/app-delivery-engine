import json
import tempfile
import unittest
from pathlib import Path
from ade.generator import plan, generate, validate

SPEC = {"schema_version": "1.0", "slug": "demo-app",
        "title": "Demo App", "outcome": "Demonstrate a small working slice"}


class GeneratorTests(unittest.TestCase):
    def test_deterministic_plan(self):
        self.assertEqual(plan(dict(SPEC)), plan(dict(SPEC)))
        self.assertIn("app/core.py", plan(SPEC))

    def test_schema_rejects_extras(self):
        with self.assertRaises(ValueError):
            validate({**SPEC, "secret": "not accepted"})

    def test_slug_rejects_traversal(self):
        with self.assertRaises(ValueError):
            validate({**SPEC, "slug": "../bad"})

    def test_rejects_control_characters(self):
        with self.assertRaises(ValueError):
            validate({**SPEC, "title": "bad\nname"})

    def test_rejects_wrong_version(self):
        with self.assertRaises(ValueError):
            validate({**SPEC, "schema_version": "2"})

    def test_no_overwrite_and_generated_manifest(self):
        with tempfile.TemporaryDirectory() as root:
            destination = Path(root) / "demo"
            created = generate(SPEC, destination)
            self.assertIn("project-manifest.json", created)
            manifest = json.loads((destination / "project-manifest.json").read_text())
            self.assertEqual(manifest["status"], "scaffold-only")
            (destination / "app/core.py").write_text("user edit", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                generate(SPEC, destination)
            self.assertEqual((destination / "app/core.py").read_text(), "user edit")

    def test_failed_parent_no_artifacts(self):
        with tempfile.TemporaryDirectory() as root:
            destination = Path(root) / "missing" / "app"
            with self.assertRaises(ValueError):
                generate(SPEC, destination)
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
