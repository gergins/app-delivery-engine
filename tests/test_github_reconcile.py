import unittest
from ade.github_reconcile import reconcile_github_snapshot
from ade.continuity import recommend_next_work

HEAD = "a" * 40
OLDER = "b" * 40
PR = {"head_sha": HEAD, "state": "open", "draft": True,
      "url": "https://github.com/example/app/pull/1"}


def run(sha=HEAD, status="completed", conclusion="success", identifier=1,
        event="pull_request"):
    return {"head_sha": sha, "status": status, "conclusion": conclusion,
            "id": identifier, "event": event,
            "html_url": "https://github.com/example/app/actions/runs/" + str(identifier)}


class GitHubReconcileTests(unittest.TestCase):
    def test_exact_head_success_yields_advisory_not_approval(self):
        result = reconcile_github_snapshot(PR, [run()])
        self.assertEqual(result["ci_status"], "success")
        self.assertEqual(result["tested_sha"], HEAD)
        self.assertFalse(result["approvals"]["merge"])
        next_work = recommend_next_work(result, [{
            "id": "issue-1", "kind": "unfinished-slice",
            "description": "Finish approved slice", "dependency_ready": True,
            "evidence_ref": "https://github.com/example/app/issues/1"}])
        self.assertEqual(next_work["decision"], "RECOMMEND")
        self.assertEqual(next_work["authorization"], "advisory-only")

    def test_changed_head_stops(self):
        self.assertEqual(reconcile_github_snapshot(PR, [run()],
                         expected_head=OLDER)["reason"], "head-diverged")

    def test_stale_success_does_not_prove_current_head(self):
        result = reconcile_github_snapshot(PR, [run(OLDER)])
        self.assertEqual(result["reason"], "no-exact-head-run")
        self.assertEqual(result["stale_run_count"], 1)

    def test_missing_ci_stops(self):
        self.assertEqual(reconcile_github_snapshot(PR, [])["decision"], "STOP")

    def test_pending_run_not_promoted(self):
        result = reconcile_github_snapshot(PR, [run(status="in_progress")])
        self.assertEqual(result["ci_status"], "pending")
        self.assertEqual(recommend_next_work(result, [])["reason"], "ci-unverified")

    def test_mixed_exact_head_runs_are_not_false_green(self):
        result = reconcile_github_snapshot(PR, [
            run(identifier=1), run(identifier=2, conclusion="failure")])
        self.assertEqual(result["ci_status"], "failure")

    def test_non_pr_push_run_not_counted(self):
        self.assertEqual(reconcile_github_snapshot(PR, [
            run(event="push")])["reason"], "no-exact-head-run")

    def test_malformed_run_stops(self):
        invalid = run()
        invalid["id"] = "not-an-int"
        self.assertEqual(reconcile_github_snapshot(PR, [invalid])["reason"],
                         "unverifiable-workflow")

    def test_closed_pr_stops(self):
        self.assertEqual(reconcile_github_snapshot(
            dict(PR, state="closed"), [run()])["reason"], "unverified-pr-state")

    def test_invalid_sha_stops(self):
        self.assertEqual(reconcile_github_snapshot(
            dict(PR, head_sha="fake"), [run()])["decision"], "STOP")

    def test_non_object_input_refused(self):
        with self.assertRaises(ValueError):
            reconcile_github_snapshot(None, [run()])
        with self.assertRaises(ValueError):
            reconcile_github_snapshot(PR, [None])


if __name__ == "__main__":
    unittest.main()
