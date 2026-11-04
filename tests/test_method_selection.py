"""Fail-closed selection and composition of delivery practices."""
import unittest
from ade.method_selection import select_method, KINDS, RISKS

class MethodTests(unittest.TestCase):
    def test_known_kinds_are_stable_and_unique(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                one=select_method(kind,["identity","concurrency"])
                two=select_method(kind,["concurrency","identity","identity"])
                self.assertEqual(one,two)
                self.assertEqual(len(one["controls"]),len(set(one["controls"])))
                self.assertIn("verify-exact-head-ci-and-logs",one["controls"])
                self.assertIn("no-automatic-merge",one["stop_gates"])

    def test_schema_change_requires_recovery_and_migration(self):
        plan=select_method("schema-change",["migration"])
        self.assertIn("versioned-additive-migration",plan["controls"])
        self.assertIn("test-upgrade-rollback-restore",plan["controls"])

    def test_auth_provider_must_prove_live_not_mock(self):
        plan=select_method("integration",["identity","external-provider"])
        self.assertIn("deny-unverified-identity",plan["controls"])
        self.assertIn("require-real-idp-proof-for-live-identity-claims",plan["controls"])
        self.assertIn("document-provider-credentials-owner",plan["controls"])
        self.assertIn("no-production-credentials-or-spending",plan["stop_gates"])

    def test_release_exposure_needs_independent_review(self):
        plan=select_method("release-preparation",["public-exposure","personal-data"])
        self.assertIn("threat-model-and-independent-security-review",plan["controls"])
        self.assertIn("privacy-retention-access-and-redaction-review",plan["controls"])
        self.assertIn("require-deployment-authorization",plan["controls"])

    def test_unknown_inputs_fail_closed(self):
        for kind,risks in [("other",()),("new-slice",["not-known"]),
                           ("new-slice","identity"),("new-slice",[3]),
                           ("new-slice",None),("new-slice",[""])]:
            with self.subTest(kind=kind,risks=risks):
                with self.assertRaises(ValueError):
                    select_method(kind,risks)

    def test_all_declared_risk_flags_have_controls(self):
        for risk in RISKS:
            self.assertGreater(len(select_method("bugfix",[risk])["controls"]),
                               len(select_method("bugfix")["controls"]))

if __name__=="__main__":
    unittest.main()

from ade.method_selection import assess_evidence_reuse


class EvidenceReuseTests(unittest.TestCase):
    def setUp(self):
        self.evidence = {
            "behavior": "list-items", "result": "passed",
            "commit_sha": "a" * 40, "environment": "linux-python3.11",
            "dependencies": {"sqlite": "3.45"}, "scope": ["list-items", "database"],
            "evidence_url": "https://github.com/example/repo/actions/runs/1",
        }
        self.params = dict(behavior="list-items", changed_scopes=["docs"],
                           current_dependencies={"sqlite": "3.45"},
                           environment="linux-python3.11", evidence=self.evidence)

    def test_reuses_only_covered_unchanged_evidence(self):
        result = assess_evidence_reuse(**self.params)
        self.assertEqual(result["decision"], "reuse-prior-evidence")
        self.assertTrue(result["current_ci_required"])
        self.assertTrue(result["approval_gates_unchanged"])

    def test_changed_transitive_scope_invalidates_reuse(self):
        self.params["changed_scopes"] = ["database"]
        self.assertEqual(assess_evidence_reuse(**self.params)["decision"],
                         "expanded-verification")

    def test_dependency_drift_invalidates_reuse(self):
        self.params["current_dependencies"] = {"sqlite": "3.46"}
        self.assertEqual(assess_evidence_reuse(**self.params)["reason"], "dependency-drift")

    def test_environment_drift_and_missing_provenance(self):
        self.params["environment"] = "windows-python3.11"
        self.assertEqual(assess_evidence_reuse(**self.params)["decision"],
                         "targeted-verification")
        self.params["environment"] = "linux-python3.11"
        self.params["evidence"] = {}
        self.assertNotEqual(assess_evidence_reuse(**self.params)["decision"],
                            "reuse-prior-evidence")

    def test_uncovered_behavior_or_failed_evidence(self):
        self.params["behavior"] = "cancel-booking"
        self.assertEqual(assess_evidence_reuse(**self.params)["reason"], "behavior-not-covered")
        self.params["behavior"] = "list-items"
        self.evidence["result"] = "failed"
        self.assertEqual(assess_evidence_reuse(**self.params)["reason"], "no-passing-evidence")

    def test_high_risk_requires_fresh_verification(self):
        for risk in ("identity", "payment", "personal-data", "migration",
                     "concurrency", "public-exposure"):
            with self.subTest(risk=risk):
                self.assertEqual(
                    assess_evidence_reuse(**self.params, risks=[risk])["reason"],
                    "high-consequence-risk")

    def test_malformed_inputs_fail_closed(self):
        for changes in (None, "docs", ["docs", 4]):
            with self.assertRaises(ValueError):
                assess_evidence_reuse(**{**self.params, "changed_scopes": changes})
        with self.assertRaises(ValueError):
            assess_evidence_reuse(**self.params, risks=["unknown-risk"])
