"""Synthetic, entirely offline OWAC selector-to-ADE CLI acceptance tests."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ade.owac_handoff_cli import compose_selection

SHA = "a" * 40
URL = ("https://github.com/gergins/app-delivery-engine/blob/"
       "docs/owac-v1-20261108/docs/operating/OUTCOME_TO_WORKING_APP_CONTRACT.md")
METHOD = {
    "id": "method-outcome-to-working-app-v1", "kind": "methods",
    "version": "1.0.0", "status": "proposed",
    "authority": {"no_automatic_merge": True, "no_automatic_deploy": True,
                  "no_unapproved_spend": True},
    "provenance": {"canonical_contract_url": URL},
}
MATCH = {
    "selection_engine": "deterministic-phrase-matching-v1",
    "methods": [{"id": METHOD["id"], "version": "1.0.0", "status": "proposed",
                 "does_not_authorize_execution": True, "matched_phrases": ["build an app"],
                 "source_url": URL}],
    "unmatched": False,
}


class OWACSelectionHandoffTests(unittest.TestCase):
    def compose(self, selection=None, record=None, **kwargs):
        data = {"selection": copy.deepcopy(MATCH) if selection is None else selection,
                "record": copy.deepcopy(METHOD) if record is None else record,
                "source_commit": SHA, "kind": "new-slice",
                "risks": ["concurrency"]}
        data.update(kwargs)
        return compose_selection(**data)

    def test_expected_match_composes_ade_controls(self):
        result = self.compose()
        self.assertFalse(result["execution_authorized"])
        self.assertFalse(result["approval_granted"])
        self.assertFalse(result["registry_source"]["authenticated_by_this_function"])
        self.assertIn("test-competing-writers-and-restart",
                      result["delivery_controls"]["controls"])
        self.assertIn("no-automatic-merge", result["delivery_controls"]["stop_gates"])

    def test_no_match_refused(self):
        selection = copy.deepcopy(MATCH)
        selection["methods"] = []
        selection["unmatched"] = True
        with self.assertRaises(ValueError):
            self.compose(selection=selection)

    def test_duplicate_match_refused(self):
        selection = copy.deepcopy(MATCH)
        selection["methods"].append(dict(selection["methods"][0]))
        with self.assertRaises(ValueError):
            self.compose(selection=selection)

    def test_wrong_selected_source_refused(self):
        selection = copy.deepcopy(MATCH)
        selection["methods"][0]["source_url"] = "https://example.com/"
        with self.assertRaises(ValueError):
            self.compose(selection=selection)

    def test_unauthorized_selection_refused(self):
        selection = copy.deepcopy(MATCH)
        selection["methods"][0]["does_not_authorize_execution"] = False
        with self.assertRaises(ValueError):
            self.compose(selection=selection)

    def test_missing_match_evidence_refused(self):
        selection = copy.deepcopy(MATCH)
        selection["methods"][0]["matched_phrases"] = []
        with self.assertRaises(ValueError):
            self.compose(selection=selection)

    def test_missing_or_unknown_risk_refused(self):
        with self.assertRaises(ValueError):
            self.compose(risks=["invented-risk"])

    def test_wrong_source_revision_refused(self):
        with self.assertRaises(ValueError):
            self.compose(source_commit="main")

    def test_deterministic(self):
        self.assertEqual(self.compose(), self.compose())

    def test_cli_produces_advisory_json(self):
        with tempfile.TemporaryDirectory() as temp:
            sel, method = Path(temp) / "selection.json", Path(temp) / "method.json"
            sel.write_text(json.dumps(MATCH), encoding="utf-8")
            method.write_text(json.dumps(METHOD), encoding="utf-8")
            run = subprocess.run(
                [sys.executable, "-m", "ade.owac_handoff_cli",
                 "--selection", str(sel), "--method-record", str(method),
                 "--source-commit", SHA, "--kind", "new-slice",
                 "--risk", "concurrency"], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertFalse(json.loads(run.stdout)["approval_granted"])

    def test_cli_rejects_unmatched(self):
        with tempfile.TemporaryDirectory() as temp:
            sel, method = Path(temp) / "selection.json", Path(temp) / "method.json"
            bad = copy.deepcopy(MATCH)
            bad["methods"] = []
            bad["unmatched"] = True
            sel.write_text(json.dumps(bad), encoding="utf-8")
            method.write_text(json.dumps(METHOD), encoding="utf-8")
            run = subprocess.run(
                [sys.executable, "-m", "ade.owac_handoff_cli",
                 "--selection", str(sel), "--method-record", str(method),
                 "--source-commit", SHA, "--kind", "new-slice"],
                capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertIn("ERROR:", run.stderr)

if __name__ == "__main__":
    unittest.main()
