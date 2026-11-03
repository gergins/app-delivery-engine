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
