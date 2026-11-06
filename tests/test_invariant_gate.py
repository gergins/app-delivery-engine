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
