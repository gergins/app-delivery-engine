"""M8 bounded app-builder real create+smoke test and negative cases."""
import json
import tempfile
import unittest
from pathlib import Path
from ade.app_builder import plan_request, create_project

GOOD = {"slug": "family-items", "title": "Family Items",
        "idea": "Keep a simple personal list of household items on my laptop.",
        "template": "offline-list"}


class AppBuilderTests(unittest.TestCase):
    def test_plan_is_deterministic_and_read_only(self):
        self.assertEqual(plan_request(GOOD), plan_request(dict(GOOD)))
        self.assertEqual(plan_request(GOOD)["decision"], "PLAN")
        self.assertIn("not_implemented", plan_request(GOOD))

    def test_real_app_is_created_and_smoke_tested(self):
        with tempfile.TemporaryDirectory() as temp:
            plan = plan_request(GOOD)
            result = create_project(GOOD, plan_hash=plan["plan_hash"],
                                    confirmed=True, workspace=temp)
            self.assertEqual(result["decision"], "CREATED_LOCAL_DEMO", result)
            self.assertTrue(result["tests_passed"])
            self.assertFalse(result["approval_granted"])
            dest = Path(temp) / GOOD["slug"]
            self.assertTrue((dest / "app" / "server.py").is_file())
            self.assertTrue((dest / "delivery" / "current-state.yaml").is_file())
            with self.assertRaises(FileExistsError):
                create_project(GOOD, plan_hash=plan["plan_hash"],
                               confirmed=True, workspace=temp)

    def test_confirmation_and_plan_drift_are_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            plan = plan_request(GOOD)
            with self.assertRaises(ValueError):
                create_project(GOOD, plan_hash=plan["plan_hash"],
                               confirmed=False, workspace=temp)
            with self.assertRaises(ValueError):
                create_project({**GOOD, "idea": GOOD["idea"] + " Updated."},
                               plan_hash=plan["plan_hash"], confirmed=True,
                               workspace=temp)
            self.assertEqual(list(Path(temp).iterdir()), [])

    def test_not_an_arbitrary_application_generator(self):
        for idea in ("Build a real-time video interpreter platform for patients.",
                     "Make an online payment checkout booking system."):
            with self.assertRaises(ValueError):
                plan_request({**GOOD, "idea": idea})
        with self.assertRaises(ValueError):
            plan_request({**GOOD, "template": "any-app"})
        with self.assertRaises(ValueError):
            plan_request({**GOOD, "slug": "../escape"})
        with self.assertRaises(ValueError):
            plan_request({**GOOD, "extra": "unknown"})

    def test_does_not_approve_application_scope(self):
        with tempfile.TemporaryDirectory() as temp:
            plan = plan_request(GOOD)
            create_project(GOOD, plan_hash=plan["plan_hash"], confirmed=True,
                           workspace=temp)
            dest = Path(temp) / GOOD["slug"]
            approvals = json.loads((dest / "delivery" / "approvals.json").read_text())
            self.assertFalse(approvals["merge"])
            self.assertFalse(approvals["deploy"])


if __name__ == "__main__":
    unittest.main()
