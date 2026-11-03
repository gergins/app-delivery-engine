import unittest
from ade.continuity import recommend_next_work

HEAD = "a" * 40
BASE = {"remote_verified": True, "head_sha": HEAD, "tested_sha": HEAD,
        "ci_status": "success", "approvals": {"merge": False, "deploy": False}}

def candidate(identifier, kind, ready=True):
    return {"id": identifier, "kind": kind, "description": kind + " work",
            "dependency_ready": ready, "evidence_ref": "issue:#" + identifier}


class ContinuityTests(unittest.TestCase):
    def test_prioritizes_security_and_integrity_over_features(self):
        result = recommend_next_work(BASE, [
            candidate("2", "new-slice"), candidate("1", "data-integrity"),
            candidate("3", "security")])
        self.assertEqual(result["candidate_id"], "3")
        self.assertEqual(result["authorization"], "advisory-only")
        self.assertIn("deploy", result["protected_actions"])

    def test_skips_unready_dependencies(self):
        result = recommend_next_work(BASE, [
            candidate("1", "security", False), candidate("2", "unfinished-slice")])
        self.assertEqual(result["candidate_id"], "2")

    def test_unverified_remote_state_stops(self):
        state = dict(BASE, remote_verified=False)
        self.assertEqual(recommend_next_work(state, [])["reason"],
                         "remote-head-not-verified")

    def test_stale_successful_ci_stops(self):
        state = dict(BASE, tested_sha="b" * 40)
        self.assertEqual(recommend_next_work(state, [])["reason"],
                         "stale-ci-evidence")

    def test_missing_ci_stops(self):
        state = dict(BASE, ci_status="missing")
        self.assertEqual(recommend_next_work(state, [])["decision"], "STOP")

    def test_failing_ci_blocks_new_features(self):
        state = dict(BASE, ci_status="failure")
        self.assertEqual(recommend_next_work(state, [
            candidate("1", "new-slice")])["reason"],
                         "failing-ci-needs-diagnosis")

    def test_failing_ci_allows_repair_recommendation(self):
        state = dict(BASE, ci_status="failure")
        self.assertEqual(recommend_next_work(state, [
            candidate("1", "broken-ci")])["kind"], "broken-ci")

    def test_missing_approval_ledger_stops(self):
        state = dict(BASE)
        del state["approvals"]
        self.assertEqual(recommend_next_work(state, [])["reason"],
                         "missing-approval-ledger")

    def test_invalid_and_duplicate_candidates_refused(self):
        with self.assertRaises(ValueError):
            recommend_next_work(BASE, [candidate("1", "new-slice")] * 2)
        with self.assertRaises(ValueError):
            recommend_next_work(BASE, [candidate("1", "unknown")])

    def test_no_ready_work_stops(self):
        self.assertEqual(recommend_next_work(BASE, [
            candidate("1", "new-slice", False)])["reason"], "no-ready-candidate")

    def test_stable_tie_break(self):
        result = recommend_next_work(BASE, [
            candidate("b", "documentation"), candidate("a", "documentation")])
        self.assertEqual(result["candidate_id"], "a")


if __name__ == "__main__":
    unittest.main()
