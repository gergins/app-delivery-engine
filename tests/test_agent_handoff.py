"""Provider-neutral agent work-order boundaries; no remote mutations."""
import unittest
from ade.agent_handoff import prepare_work_order

HEAD = "a" * 40
SNAP = {"decision": "RECONCILED", "repo": "example/camping",
        "pr_number": 2, "head_sha": HEAD, "ci_status": "success"}
ARGS = {"repository": "example/camping", "pr_number": 2,
        "task": "Improve customer pending hold controls.",
        "acceptance": ["Prevent duplicate active holds", "Keep previous UI path working"],
        "kind": "bugfix", "risks": ["concurrency"]}


class WorkOrderTests(unittest.TestCase):
    def test_reviewable_readonly_work_order(self):
        result = prepare_work_order(**ARGS, snapshot=SNAP)
        self.assertEqual(result["decision"], "PREPARED_NOT_DISPATCHED")
        self.assertEqual(result["expected_head_sha"], HEAD)
        self.assertEqual(result["method"]["kind"], "bugfix")
        self.assertIn("test-competing-writers-and-restart", result["method"]["controls"])
        self.assertTrue(all(value is False for value in result["authority"].values()))

    def test_source_mismatch_and_bad_requests_refused(self):
        for changed in ({"repository": "../escape"},
                        {"task": "short"}, {"acceptance": []},
                        {"risks": ["unsafe-unrecognized"]}):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                prepare_work_order(**{**ARGS, **changed}, snapshot=SNAP)
        with self.assertRaises(ValueError):
            prepare_work_order(**ARGS, snapshot={**SNAP, "repo": "other/repo"})

    def test_unverified_pr_cannot_dispatch(self):
        result = prepare_work_order(**ARGS, snapshot={**SNAP, "decision": "STOP"})
        self.assertEqual(result["decision"], "STOP")
        self.assertFalse(result["approval_granted"])

    def test_failed_ci_does_not_become_green(self):
        result = prepare_work_order(**ARGS, snapshot={**SNAP, "ci_status": "failure"})
        self.assertEqual(result["ci_status_at_admission"], "failure")
        self.assertFalse(result["authority"]["dispatch"])


if __name__ == "__main__":
    unittest.main()
