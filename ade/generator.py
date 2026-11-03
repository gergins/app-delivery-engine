"""Deterministic, standard-library-only, offline application generator.

No shell execution, network calls, GitHub writes, credentials, or deployments.
"""
import json
import re
import shutil
from pathlib import Path

VERSION = "1.0"
SLUG = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")


def validate(spec):
    if not isinstance(spec, dict) or not {"schema_version", "slug", "title", "outcome"} <= set(spec) or set(spec) - {"schema_version", "slug", "title", "outcome", "profile"}:
        raise ValueError("Specification must contain exactly schema_version, slug, title, outcome")
    if spec["schema_version"] != VERSION:
        raise ValueError("Unsupported specification version")
    if not isinstance(spec["slug"], str) or len(spec["slug"]) > 50 or not SLUG.fullmatch(spec["slug"]):
        raise ValueError("Invalid project slug")
    for key in ("title", "outcome"):
        value = spec[key]
        if not isinstance(value, str) or not value.strip() or len(value) > 200 or any(ord(c) < 32 for c in value):
            raise ValueError("Invalid " + key)
    if spec.get("profile", "cli") not in ("cli", "web-list"):\n        raise ValueError("Unsupported application profile")\n    return spec\n\n\ndef plan(spec):
    """Return an inspectable file plan without writing anything."""
    spec = validate(spec)
    manifest = {"schema_version": VERSION, "slug": spec["slug"], "profile": spec.get("profile", "cli"), "status": "scaffold-only",
                "deployment": "not-configured"}
    if spec.get("profile", "cli") == "web-list":\n        from .web_list import files as web_list_files\n        result = web_list_files(spec)\n        result["project-manifest.json"] = json.dumps({**manifest, "status": "local-web-benchmark"}, indent=2, sort_keys=True) + "\\n"\n        return result\n    core = '''"""Minimal application core. Replace with product behavior."""\n\ndef transform(value):\n    if not isinstance(value, str) or not value.strip():\n        raise ValueError("A non-empty string is required")\n    return value.strip()\n'''
    test = '''import unittest\nfrom app.core import transform\n\nclass CoreTests(unittest.TestCase):\n    def test_valid(self):\n        self.assertEqual(transform(" hello "), "hello")\n\n    def test_invalid(self):\n        with self.assertRaises(ValueError):\n            transform("")\n'''
    return {
        "README.md": "# " + spec["title"] + "\n\n" + spec["outcome"] +
          "\n\nGenerated offline scaffold only. Not production-ready or deployed.\n"
          "\nRun: `python -m unittest discover -s tests -v`\n",
        "app/__init__.py": "",
        "app/core.py": core,
        "tests/__init__.py": "",
        "tests/test_core.py": test,
        "project-manifest.json": json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        ".gitignore": "__pycache__/\n.pytest_cache/\n.env\n",
    }


def generate(spec, destination):
    """Create new files only. Existing targets are never overwritten."""
    files = plan(spec)
    destination = Path(destination)
    if destination.is_symlink() or destination.exists():
        raise FileExistsError("Destination already exists")
    if not destination.parent.is_dir():
        raise ValueError("Destination parent must exist")
    destination.mkdir(exist_ok=False)
    try:
        for relative, content in files.items():
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
    except BaseException:
        shutil.rmtree(destination)
        raise
    return tuple(sorted(files))
