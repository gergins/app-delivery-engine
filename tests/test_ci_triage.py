"""The CI triage aid never guesses a root cause or skips required tests."""
import unittest
from ade.ci_triage import classify_first_failure

GOOD = [
    {"name": "camping", "conclusion": "success", "runner_name": "runner-1",
     "steps": ["checkout", "tests"]},
    {"name": "postgres", "conclusion": "success", "runner_name": "runner-2",
     "steps": ["checkout", "database"]},
]
BAD = [
    {"name": "camping", "conclusion": "failure", "runner_name": "", "steps": []},
    {"name": "postgres", "conclusion": "failure", "runner_name": "", "steps": []},
]


class TriageTests(unittest.TestCase):
    def test_first_failure_before_workflow_change(self):
        result = classify_first_failure(
            previous_jobs=GOOD, failed_jobs=BAD, workflow_changed=False)
        self.assertEqual(result["phase"], "pre-step-unknown")
        self.assertFalse(result["first_failure_workflow_changed"])
        self.assertEqual(result["next_owner_role"], "repository-actions-operator")
        self.assertEqual(result["next_evidence"], "pre-step-job-error-banner-or-check-annotation")
        self.assertFalse(result["root_cause_confirmed"])
        self.assertFalse(result["may_change_ci"])
        self.assertFalse(result["may_skip_required_tests"])

    def test_same_symptom_after_workflow_change_not_root_cause(self):
        result = classify_first_failure(
            previous_jobs=GOOD, failed_jobs=BAD, workflow_changed=True)
        self.assertEqual(result["phase"], "pre-step-unknown")
        self.assertFalse(result["root_cause_confirmed"])

    def test_actual_failing_step_routes_to_maintainer(self):
        jobs = [{"name": "camping", "conclusion": "failure",
                 "runner_name": "runner-3", "steps": ["checkout", "unit-failed"]}]
        result = classify_first_failure(
            previous_jobs=GOOD, failed_jobs=jobs, workflow_changed=False)
        self.assertEqual(result["phase"], "step-execution-failure")
        self.assertEqual(result["next_evidence"], "first-failing-step-name-and-log")

    def test_no_baseline_does_not_guess(self):
        result = classify_first_failure(
            previous_jobs=[], failed_jobs=BAD, workflow_changed=False)
        self.assertEqual(result["phase"], "insufficient-evidence")

    def test_malformed_jobs_fail_closed(self):
        for jobs in (None, "unknown", [GOOD[0], GOOD[0]],
                     [{**GOOD[0], "runner_name": None}],
                     [{**GOOD[0], "extra": "value"}]):
            with self.subTest(jobs=jobs):
                with self.assertRaises(ValueError):
                    classify_first_failure(
                        previous_jobs=GOOD, failed_jobs=jobs,
                        workflow_changed=False)
        with self.assertRaises(ValueError):
            classify_first_failure(
                previous_jobs=GOOD, failed_jobs=BAD,
                workflow_changed="unknown")


if __name__ == "__main__":
    unittest.main()
