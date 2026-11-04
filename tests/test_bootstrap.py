"""Bootstrap and cross-agent continuity benchmark: offline, deterministic, fail-closed."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from ade.bootstrap import bootstrap,plan_bootstrap,validate_brief

SAMPLE={"schema_version":"1.0","slug":"vrs-benchmark",
        "title":"VRS Benchmark","problem":"Accessible relay calling needs safe design",
        "users":["Deaf caller","Interpreter","Supervisor"],
        "outcome":"Validate the minimal three party workflow",
        "domain":"vrs"}


class BootstrapTests(unittest.TestCase):
    def test_same_brief_reproducible_and_has_mandatory_files(self):
        first=plan_bootstrap(SAMPLE)
        second=plan_bootstrap(dict(SAMPLE))
        self.assertEqual(first,second)
        for p in ("AGENTS.md","project.yaml","docs/product/requirements.md",
                  "docs/architecture/overview.md","docs/decisions/0001-initial-constraints.md",
                  "docs/quality/acceptance.md","docs/security/risk-register.md",
                  "delivery/current-state.yaml","delivery/evidence.json","delivery/approvals.json",
                  "delivery/method-selection.json","tools/startup.py","tests/test_startup.py",
                  ".github/workflows/verify.yml","docs/product/vrs-invariants.md"):
            self.assertIn(p,first)
        self.assertIn("telecom",first["docs/product/vrs-invariants.md"])
        self.assertIn("no-automatic-deployment-or-public-hosting",
                      first["delivery/method-selection.json"])
        self.assertEqual(json.loads(first["delivery/current-state.yaml"])["status"],"blocked")

    def test_generated_repository_stops_before_approval_and_tests_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/"vrs"
            bootstrap(SAMPLE,root)
            result=subprocess.run([sys.executable,"tools/startup.py"],cwd=root,
                                  text=True,capture_output=True,timeout=12)
            self.assertEqual(result.returncode,2,result.stderr)
            payload=json.loads(result.stdout)
            self.assertEqual(payload["decision"],"STOP")
            self.assertEqual(payload["reason"],"approval-or-requirements-gate")
            self.assertTrue(payload["requires_remote_github_verification"])
            tests=subprocess.run([sys.executable,"-m","unittest","discover","-s","tests","-v"],
                                 cwd=root,text=True,capture_output=True,timeout=12)
            self.assertEqual(tests.returncode,0,tests.stderr)

    def test_missing_file_and_mismatched_project_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/"vrs"
            bootstrap(SAMPLE,root)
            sys.path.insert(0,str(root))
            try:
                from tools.startup import inspect
                (root/"docs/quality/acceptance.md").unlink()
                self.assertEqual(inspect(root)["reason"],"missing-required-files")
                (root/"docs/quality/acceptance.md").write_text("draft\n")
                state=json.loads((root/"delivery/current-state.yaml").read_text())
                state["project_slug"]="unrelated-app"
                (root/"delivery/current-state.yaml").write_text(json.dumps(state))
                self.assertEqual(inspect(root)["reason"],"schema-or-project-drift")
            finally:
                sys.path.pop(0)
                sys.modules.pop("tools.startup",None)
                sys.modules.pop("tools",None)

    def test_malformed_authority_and_fake_completion_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/"vrs"
            bootstrap(SAMPLE,root)
            # Execute the generated verifier in a separate process, like Codex.
            approvals=root/"delivery/approvals.json"
            approvals.write_text(json.dumps({"merge":True,"deploy":False,
                                              "production_credentials":False}))
            result=subprocess.run([sys.executable,"tools/startup.py"],cwd=root,
                                  capture_output=True,text=True)
            self.assertEqual(json.loads(result.stdout)["reason"],"unverified-authority-state")
            approvals.write_text(json.dumps({"merge":False,"deploy":False,
                                              "production_credentials":False}))
            state=root/"delivery/current-state.yaml"
            obj=json.loads(state.read_text())
            obj["status"]="complete"
            state.write_text(json.dumps(obj))
            result=subprocess.run([sys.executable,"tools/startup.py"],cwd=root,
                                  capture_output=True,text=True)
            self.assertEqual(json.loads(result.stdout)["reason"],"unsupported-completion")

    def test_unknown_risk_domain_extra_and_traversal_denied(self):
        variants=[
          {**SAMPLE,"domain":"surveillance"},
          {**SAMPLE,"risks":["unrecognized-risk"]},
          {**SAMPLE,"slug":"../../escape"},
          {**SAMPLE,"title":"line\nbreak"},
          {**SAMPLE,"admin_token":"not-allowed"},
        ]
        for b in variants:
            with self.subTest(b=b):
                with self.assertRaises(ValueError):
                    validate_brief(b)

    def test_existing_target_never_modified(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)/"app"
            folder.mkdir()
            marker=folder/"keep.txt"
            marker.write_text("retain")
            with self.assertRaises(FileExistsError):
                bootstrap(SAMPLE,folder)
            self.assertEqual(marker.read_text(),"retain")

    def test_general_offline_app_not_forced_to_use_vrs_tech(self):
        src={**SAMPLE,"domain":"offline-tasks","slug":"task-benchmark"}
        files=plan_bootstrap(src)
        self.assertNotIn("docs/product/vrs-invariants.md",files)
        self.assertNotIn("require-real-idp-proof-for-live-identity-claims",
                         files["delivery/method-selection.json"])

    def test_cli_plan_no_side_effect_and_create_without_approval(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            file=root/"brief.json"
            file.write_text(json.dumps(SAMPLE))
            destination=root/"project"
            planned=subprocess.run([sys.executable,"-m","ade.bootstrap_cli","plan",str(file)],
                                   cwd=Path(__file__).resolve().parents[1],
                                   capture_output=True,text=True,timeout=12)
            self.assertEqual(planned.returncode,0,planned.stderr)
            self.assertFalse(destination.exists())
            created=subprocess.run([sys.executable,"-m","ade.bootstrap_cli","create",
                                    str(file),str(destination)],
                                   cwd=Path(__file__).resolve().parents[1],
                                   capture_output=True,text=True,timeout=12)
            self.assertEqual(created.returncode,0,created.stderr)
            self.assertTrue((destination/"AGENTS.md").is_file())


if __name__=="__main__":
    unittest.main()
