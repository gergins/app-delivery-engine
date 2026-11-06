import unittest
from ade.invariant_gate import assess_invariant_records

class TestInvariantGate(unittest.TestCase):
    def setUp(self):
        self.d = {"id":"D1","classification":"semantic",
                  "proposed_at":"2026-11-06T10:00:00+01:00",
                  "first_dependent_change_at":"2026-11-06T12:00:00+01:00",
                  "status":"approved","owner":"owner",
                  "approved_at":"2026-11-06T11:00:00+01:00",
                  "approval_reference":"approval-1"}
        self.f0 = {"id":"F0","entry":"request","artifact":"stored-item",
                   "evidence_revision":"a"*40,"checks_passed":True,
                   "negative_checks_passed":True,"running_spine_verified":True,
                   "stubs_disclosed":True,"decision_refs":["D1"]}

    def check(self, rungs=None, ask="semantic"):
        return assess_invariant_records(decisions=[self.d],
                                        rungs=[self.f0] if rungs is None else rungs,
                                        ask=ask)

    def test_valid_advisory_only(self):
        result = self.check()
        self.assertFalse(result["approval_granted"])
        self.assertTrue(result["independent_evidence_required"])

    def test_late_ledger_fails_even_if_delegated(self):
        self.d["proposed_at"] = "2026-11-06T13:00:00+01:00"
        with self.assertRaises(ValueError):
            self.check(ask="delegated")

    def test_unapproved_semantic_fails(self):
        self.d["status"] = "proposed"
        with self.assertRaises(ValueError):
            self.check()

    def test_late_approval_fails(self):
        self.d["approved_at"] = "2026-11-06T13:00:00+01:00"
        with self.assertRaises(ValueError):
            self.check()

    def test_f0_must_be_real(self):
        with self.assertRaises(ValueError):
            self.check([dict(self.f0, running_spine_verified=False)])

    def test_f1_must_cover_previous_checks_at_same_revision(self):
        f1 = {"id":"F1","entry":"request","artifact":"stored-result",
              "evidence_revision":"a"*40,"checks_passed":True,
              "negative_checks_passed":True,"decision_refs":["D1"],
              "predecessor_ids":["F0"]}
        self.assertEqual(self.check([self.f0,f1])["rungs_checked"],2)
        with self.assertRaises(ValueError):
            self.check([self.f0,dict(f1,predecessor_ids=[])])

if __name__ == "__main__":
    unittest.main()


from ade.invariant_gate import assess_invariant_evidence


class TestExactHeadInvariantEvidence(unittest.TestCase):
    SHA = "a" * 40

    def setUp(self):
        self.decision = {
            "id": "D1", "classification": "semantic",
            "proposed_at": "2026-11-06T10:00:00+01:00",
            "first_dependent_change_at": "2026-11-06T12:00:00+01:00",
            "status": "approved", "owner": "owner",
            "approved_at": "2026-11-06T11:00:00+01:00",
            "approval_reference": "review-1",
        }
        self.rung = {
            "id": "F0", "entry": "http", "artifact": "sqlite-record",
            "evidence_revision": self.SHA, "checks_passed": True,
            "negative_checks_passed": True, "running_spine_verified": True,
            "stubs_disclosed": True, "decision_refs": ["D1"],
            "evidence_refs": ["https://github.com/example/app/actions/runs/1"],
        }
        self.snapshot = {
            "decision": "RECONCILED", "remote_verified": True,
            "authority": "no-authorization-derived",
            "head_sha": self.SHA, "tested_sha": self.SHA,
            "ci_status": "success",
            "workflow_urls": ["https://github.com/example/app/actions/runs/1"],
        }

    def evaluate(self):
        return assess_invariant_evidence(
            decisions=[self.decision], rungs=[self.rung],
            github_snapshot=self.snapshot)

    def test_matching_exact_head_is_advisory_only(self):
        result = self.evaluate()
        self.assertEqual(result["exact_head_sha"], self.SHA)
        self.assertFalse(result["approval_granted"])
        self.assertEqual(result["authority"], "no-authorization-derived")

    def test_ci_must_be_successful_and_exact_head(self):
        for field, value in (
            ("tested_sha", "b" * 40), ("tested_sha", None),
            ("ci_status", "pending"), ("ci_status", "failure"),
            ("decision", "STOP"), ("remote_verified", False),
            ("authority", "approved"), ("head_sha", "not-a-sha"),
            ("workflow_urls", []),
        ):
            with self.subTest(field=field, value=value):
                good = self.snapshot[field]
                self.snapshot[field] = value
                try:
                    with self.assertRaises(ValueError):
                        self.evaluate()
                finally:
                    self.snapshot[field] = good

    def test_rung_revision_and_reference_cannot_be_missing(self):
        for field, value in (
            ("evidence_revision", "b" * 40),
            ("evidence_refs", []), ("evidence_refs", ["uninspectable"]),
        ):
            with self.subTest(field=field, value=value):
                good = self.rung[field]
                self.rung[field] = value
                try:
                    with self.assertRaises(ValueError):
                        self.evaluate()
                finally:
                    self.rung[field] = good

    def test_missing_snapshot_rejected(self):
        with self.assertRaises(ValueError):
            assess_invariant_evidence(decisions=[self.decision],
                                      rungs=[self.rung], github_snapshot=None)


from ade.invariant_gate import assess_rung_job_steps


class TestRungStepEvidence(unittest.TestCase):
    def setUp(self):
        self.sha = "a" * 40
        self.assessment = {
            "decision": "records-consistent", "ci_status": "success",
            "approval_granted": False, "exact_head_sha": self.sha,
            "rungs_checked": 1,
        }
        self.rung = {
            "id": "F0", "evidence_revision": self.sha,
            "evidence_steps": {"positive": "Verify application",
                               "negative": "Verify failure scenarios"},
        }
        self.jobs = [{
            "id": 44, "run_id": 10, "status": "completed",
            "conclusion": "success",
            "steps": [
                {"name": "Verify application", "status": "completed",
                 "conclusion": "success"},
                {"name": "Verify failure scenarios", "status": "completed",
                 "conclusion": "success"},
            ],
        }]

    def check(self):
        return assess_rung_job_steps(
            invariant_assessment=self.assessment, rungs=[self.rung],
            workflow_run_id=10, jobs=self.jobs)

    def test_matching_steps_do_not_grant_approval(self):
        result = self.check()
        self.assertEqual(result["decision"], "step-names-matched")
        self.assertFalse(result["approval_granted"])
        self.assertEqual(result["matched_rungs"]["F0"]["negative"],
                         "Verify failure scenarios")

    def test_failed_pending_and_missing_steps_rejected(self):
        for status, conclusion in (
            ("completed", "failure"), ("in_progress", None)
        ):
            with self.subTest(status=status, conclusion=conclusion):
                original = self.jobs[0]["steps"][1].copy()
                self.jobs[0]["steps"][1].update(
                    status=status, conclusion=conclusion)
                try:
                    with self.assertRaises(ValueError):
                        self.check()
                finally:
                    self.jobs[0]["steps"][1] = original
        self.rung["evidence_steps"]["negative"] = "Unknown step"
        with self.assertRaises(ValueError):
            self.check()

    def test_job_must_belong_to_same_run(self):
        self.jobs[0]["run_id"] = 999
        with self.assertRaises(ValueError):
            self.check()

    def test_missing_negative_step_and_duplicate_names_rejected(self):
        self.rung["evidence_steps"] = {"positive": "Verify application"}
        with self.assertRaises(ValueError):
            self.check()
        self.rung["evidence_steps"]["negative"] = "Verify application"
        with self.assertRaises(ValueError):
            self.check()

    def test_stale_rung_or_unverified_ci_rejected(self):
        self.rung["evidence_revision"] = "b" * 40
        with self.assertRaises(ValueError):
            self.check()
        self.rung["evidence_revision"] = self.sha
        self.assessment["ci_status"] = "pending"
        with self.assertRaises(ValueError):
            self.check()
