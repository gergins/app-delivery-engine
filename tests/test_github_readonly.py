import unittest
from ade.github_readonly import inspect_pull_request, main

SHA = "a" * 40
BASE = "https://api.github.com/repos/example/app"

def pr(head=SHA):
    return {"head": {"sha": head}, "state": "open", "draft": True,
            "html_url": "https://github.com/example/app/pull/5"}

def run(head=SHA, status="completed", conclusion="success"):
    return {"head_sha": head, "event": "pull_request", "id": 1,
            "status": status, "conclusion": conclusion,
            "html_url": "https://github.com/example/app/actions/runs/1"}


class ReadonlyGitHubTests(unittest.TestCase):
    def test_two_exact_read_requests_and_reconciliation(self):
        seen = []
        def fetch(url):
            seen.append(url)
            return pr() if "/pulls/5" in url else {
                "total_count": 1, "workflow_runs": [run()]}
        result = inspect_pull_request("example/app", 5, fetch=fetch)
        self.assertEqual(result["decision"], "RECONCILED")
        self.assertEqual(result["tested_sha"], SHA)
        self.assertEqual(len(seen), 2)
        self.assertTrue(all(x.startswith(BASE) for x in seen))
        self.assertIn("head_sha=", seen[1])
        self.assertFalse(result["approvals"]["deploy"])

    def test_network_error_is_not_synthetic_success(self):
        def offline(_):
            raise OSError("offline")
        with self.assertRaises(OSError):
            inspect_pull_request("example/app", 5, fetch=offline)

    def test_failing_ci_is_not_production_ready(self):
        def fetch(url):
            return pr() if "/pulls/" in url else {
                "total_count": 1, "workflow_runs": [
                    run(conclusion="failure")]}
        self.assertEqual(inspect_pull_request("example/app", 5, fetch=fetch)[
            "ci_status"], "failure")

    def test_missing_ci_refused(self):
        def fetch(url):
            return pr() if "/pulls/" in url else {
                "total_count": 0, "workflow_runs": []}
        self.assertEqual(inspect_pull_request("example/app", 5, fetch=fetch)[
            "reason"], "no-exact-head-run")

    def test_truncated_ci_page_stops(self):
        def fetch(url):
            return pr() if "/pulls/" in url else {
                "total_count": 101, "workflow_runs": [run()]}
        self.assertEqual(inspect_pull_request("example/app", 5, fetch=fetch)[
            "reason"], "ci-results-incomplete")

    def test_invalid_response_refused(self):
        self.assertEqual(inspect_pull_request("example/app", 5, fetch=lambda _: {})[
            "decision"], "STOP")

    def test_bad_repository_and_pr_rejected_before_network(self):
        for owner in ["../bad", "example/app/extra", "https://evil.example/a"]:
            with self.assertRaises(ValueError):
                inspect_pull_request(owner, 5, fetch=lambda _: None)
        with self.assertRaises(ValueError):
            inspect_pull_request("example/app", True, fetch=lambda _: None)

    def test_cli_bad_arguments_safe(self):
        with self.assertRaises(SystemExit):
            main(["../wrong", "1"])


if __name__ == "__main__":
    unittest.main()
