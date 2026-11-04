"""M1 bounded evidence-reuse benchmark using actual disposable generated apps.

Real generated artifacts are tested in temporary directories. Deliberate
mutations must be detected by existing application tests. This does NOT
measure CI cost savings or validate the authenticity of a past GitHub run.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ade.generator import generate
from ade.method_selection import assess_evidence_reuse

ROOT = Path(__file__).resolve().parents[1]
CLI_SPEC = {"schema_version": "1.0", "slug": "mutation-cli",
            "title": "Mutation CLI", "outcome": "Validate text"}
WEB_SPEC = {"schema_version": "1.0", "slug": "mutation-web",
            "title": "Mutation Web", "outcome": "Save items", "profile": "web-list"}


def prior(behavior, scope):
    # A fixture record, NOT a real authenticated verification attestation.
    return {"behavior": behavior, "result": "passed", "commit_sha": "a" * 40,
            "environment": "linux-python3.11", "dependencies": {"runtime": "3.11"},
            "scope": list(scope), "evidence_url": "https://github.com/example/repo/actions/runs/1"}


def decide(behavior, scope, changed, risks=()):
    return assess_evidence_reuse(
        behavior=behavior, changed_scopes=changed,
        current_dependencies={"runtime": "3.11"},
        environment="linux-python3.11",
        evidence=prior(behavior, scope), risks=risks)


def run_generated(root, pattern):
    return subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests",
         "-p", pattern, "-v"], cwd=root, text=True, capture_output=True,
        timeout=25)


class AdaptiveEvidenceBenchmark(unittest.TestCase):
    def test_low_risk_document_only_reuse_without_waiving_ci(self):
        # The application behavior was not modified. Reusing prior evidence
        # for the unchanged scope is advisory, not an approval or new CI pass.
        decision = decide("cli-transform", ["cli-transform", "core"], ["docs"])
        self.assertEqual(decision["decision"], "reuse-prior-evidence")
        self.assertTrue(decision["current_ci_required"])
        self.assertTrue(decision["approval_gates_unchanged"])

    def test_medium_risk_generated_core_mutation_is_caught(self):
        self.assertEqual(
            decide("cli-transform", ["cli-transform", "core"], ["core"])["decision"],
            "expanded-verification")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "cli"
            generate(CLI_SPEC, root)
            self.assertEqual(run_generated(root, "test_core.py").returncode, 0)
            module = root / "app" / "core.py"
            src = module.read_text(encoding="utf-8")
            self.assertIn("return value.strip()", src)
            module.write_text(src.replace("return value.strip()", "return value"),
                              encoding="utf-8")
            failed = run_generated(root, "test_core.py")
            self.assertNotEqual(failed.returncode, 0,
                                "Mutation escaped existing transform regression tests")
            self.assertIn("FAIL", failed.stderr)

    def test_high_risk_validation_mutation_is_caught_by_http_tests(self):
        decision = decide("web-input", ["web-input", "database"], ["web-input"],
                          risks=["concurrency"])
        self.assertEqual(decision["decision"], "expanded-verification")
        self.assertTrue(decision["current_ci_required"])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "web"
            generate(WEB_SPEC, root)
            self.assertEqual(run_generated(root, "test_app.py").returncode, 0)
            module = root / "app" / "server.py"
            src = module.read_text(encoding="utf-8")
            needle = 'if (type(title) is not str or not title.strip() or len(title.strip()) > 100'
            self.assertIn(needle, src)
            # Mutation: remove the validation gate without touching other code.
            mutated = src.replace(needle, 'if (False and type(title) is not str or False and not title.strip() or False and len(title.strip()) > 100')
            # Make the entire original multiline guard inert, not just the first line.
            mutated = mutated.replace('or any(ord(c) < 32 for c in title)):', 'or False and any(ord(c) < 32 for c in title)):')
            module.write_text(mutated, encoding="utf-8")
            failed = run_generated(root, "test_app.py")
            self.assertNotEqual(failed.returncode, 0,
                                "Mutation escaped existing invalid-input regression tests")
            self.assertIn("FAIL", failed.stderr)

    def test_transitive_dependency_and_stale_evidence_require_verification(self):
        original = prior("cli-transform", ["cli-transform"])
        drift = assess_evidence_reuse(
            behavior="cli-transform", changed_scopes=["docs"],
            current_dependencies={"runtime": "3.12"},
            environment="linux-python3.11", evidence=original)
        self.assertEqual(drift["decision"], "expanded-verification")
        incomplete = dict(original)
        incomplete.pop("commit_sha")
        decision = assess_evidence_reuse(
            behavior="cli-transform", changed_scopes=["docs"],
            current_dependencies={"runtime": "3.11"},
            environment="linux-python3.11", evidence=incomplete)
        self.assertNotEqual(decision["decision"], "reuse-prior-evidence")


if __name__ == "__main__":
    unittest.main()
