"""Offline, synthetic consumer-contract tests for OWAC bridge."""
import copy
import unittest

from ade.owac_method import recommend_owac

RECORD = {
    "id": "method-outcome-to-working-app-v1",
    "kind": "methods",
    "version": "1.0.0",
    "status": "proposed",
    "provenance": {
        "canonical_contract_url": "https://github.com/gergins/app-delivery-engine/blob/docs/owac-v1-20261108/docs/operating/OUTCOME_TO_WORKING_APP_CONTRACT.md"
    },
    "authority": {"no_automatic_merge": True, "no_automatic_deploy": True,
                  "no_unapproved_spend": True}
}
SHA = "a" * 40


class OWACAdvisoryHandoffTests(unittest.TestCase):
    def assess(self, record=None, **updates):
        data = dict(method_record=copy.deepcopy(RECORD) if record is None else record,
                    selected_method_id="method-outcome-to-working-app-v1",
                    source_repo="gergins/engineering-knowledge-registry",
                    source_commit=SHA, kind="new-slice", risks=("concurrency",))
        data.update(updates)
        return recommend_owac(**data)

    def test_recommendation_composes_existing_ade_controls(self):
        out = self.assess()
        self.assertEqual(out["method"]["id"], RECORD["id"])
        self.assertIn("test-competing-writers-and-restart", out["delivery_controls"]["controls"])
        self.assertIn("no-automatic-merge", out["delivery_controls"]["stop_gates"])
        self.assertFalse(out["approval_granted"])
        self.assertFalse(out["execution_authorized"])
        self.assertFalse(out["registry_source"]["authenticated_by_this_function"])

    def test_reproducible(self):
        self.assertEqual(self.assess(), self.assess())

    def test_foreign_or_unpinned_source_rejected(self):
        for extra in ({"source_repo": "another/registry"}, {"source_commit": "main"},
                      {"source_commit": "bad"}, {"source_commit": "A" * 40}):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                self.assess(**extra)

    def test_method_identity_rejected(self):
        with self.assertRaises(ValueError):
            self.assess(selected_method_id="some-other-method")
        changed = copy.deepcopy(RECORD)
        changed["id"] = "different"
        with self.assertRaises(ValueError):
            self.assess(record=changed)

    def test_bad_version_and_maturity_rejected(self):
        for key, value in (("version", "2.0.0"), ("status", "verified")):
            changed = copy.deepcopy(RECORD)
            changed[key] = value
            with self.assertRaises(ValueError):
                self.assess(record=changed)

    def test_missing_or_foreign_provenance_rejected(self):
        for p in ({}, {"canonical_contract_url": "https://example.org/method"}):
            changed = copy.deepcopy(RECORD)
            changed["provenance"] = p
            with self.assertRaises(ValueError):
                self.assess(record=changed)

    def test_authority_cannot_be_downgraded(self):
        for key in RECORD["authority"]:
            changed = copy.deepcopy(RECORD)
            changed["authority"][key] = False
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.assess(record=changed)

    def test_unknown_ade_risk_stays_fail_closed(self):
        with self.assertRaises(ValueError):
            self.assess(risks=("unknown-risk",))

    def test_missing_record_rejected(self):
        with self.assertRaises(ValueError):
            self.assess(record={})


if __name__ == "__main__":
    unittest.main()
