"""Negative and positive consumer-contract checks; no private data in public CI."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ade.registry_bridge import assess_snapshot

SHA = "a" * 40
BRIEF = {"description": "Accessible camping booking with cancellation and concurrency",
         "requirements": ["prevent overlapping inventory booking"]}
RECORDS = [
    {"id": "requirements", "name": "Requirements", "domain": "product",
     "description": "Define requirements", "keywords": ["requirements"],
     "depends_on": [], "evidence": "Accepted criteria",
     "source_status": "synthesized", "maturity": "L1"},
    {"id": "transactions", "name": "Transactions", "domain": "data",
     "description": "Prevent conflicts", "keywords": ["booking"],
     "depends_on": ["requirements"], "evidence": "Concurrent overlap negative test",
     "source_status": "synthesized", "maturity": "L1"},
]


class RegistryBridgeTests(unittest.TestCase):
    def plan(self, records=None, **overrides):
        kwargs = {"records": RECORDS if records is None else records,
                  "source_repo": "gergins/engineering-knowledge-registry",
                  "source_commit": SHA, "brief": BRIEF,
                  "kind": "integration", "risks": ["concurrency"]}
        kwargs.update(overrides)
        return assess_snapshot(**kwargs)

    def test_integration_and_dependency_closure(self):
        plan = self.plan()
        self.assertEqual([x["id"] for x in plan["capabilities"]],
                         ["requirements", "transactions"])
        self.assertEqual(plan["capabilities"][0]["reason"], "dependency")
        self.assertIn("test-competing-writers-and-restart", plan["method"]["controls"])
        self.assertFalse(plan["approval_granted"])
        self.assertFalse(plan["source"]["source_authenticated"])

    def test_deterministic(self):
        self.assertEqual(self.plan(), self.plan(records=list(reversed(RECORDS))))

    def test_missing_dependency_is_blocked(self):
        modified = json.loads(json.dumps(RECORDS))
        modified[1]["depends_on"] = ["missing"]
        with self.assertRaises(ValueError):
            self.plan(records=modified)

    def test_cycle_is_blocked(self):
        modified = json.loads(json.dumps(RECORDS))
        modified[0]["depends_on"] = ["transactions"]
        with self.assertRaises(ValueError):
            self.plan(records=modified)

    def test_duplicate_id_is_blocked(self):
        with self.assertRaises(ValueError):
            self.plan(records=RECORDS + [RECORDS[0]])

    def test_unverified_source_claim_is_blocked(self):
        modified = json.loads(json.dumps(RECORDS))
        modified[0]["source_status"] = "source-verified"
        with self.assertRaises(ValueError):
            self.plan(records=modified)

    def test_mismatched_origin_or_revision_is_blocked(self):
        for changes in ({"source_repo": "other/repo"},
                        {"source_commit": "main"},
                        {"source_commit": "not-a-sha"}):
            with self.assertRaises(ValueError):
                self.plan(**changes)

    def test_unknown_risk_fails_closed(self):
        with self.assertRaises(ValueError):
            self.plan(risks=["unrecognized-risk"])

    def test_invalid_brief_or_capability_fails_closed(self):
        with self.assertRaises(ValueError):
            self.plan(brief={"description": "", "requirements": []})
        with self.assertRaises(ValueError):
            self.plan(records=[{"id": "x"}])

    def test_cli_on_synthetic_snapshot(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            snapshot = directory / "snapshot.json"
            brief = directory / "brief.json"
            snapshot.write_text(json.dumps(RECORDS), encoding="utf-8")
            brief.write_text(json.dumps(BRIEF), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, "-m", "ade.registry_bridge", str(snapshot),
                 str(brief), "--source-commit", SHA,
                 "--kind", "integration", "--risk", "concurrency"],
                capture_output=True, text=True, check=True)
            result = json.loads(proc.stdout)
            self.assertEqual(result["status"], "advisory-only")
            self.assertEqual(len(result["capabilities"]), 2)


if __name__ == "__main__":
    unittest.main()
