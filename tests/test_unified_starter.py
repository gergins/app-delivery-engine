"""Unified first-run: a project brief plus an opt-in runnable local UI/API/SQLite demo."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from ade.bootstrap import plan_bootstrap, bootstrap

LOW={"schema_version":"1.0","slug":"my-work-items","title":"My Work Items",
     "problem":"Track a few saved items","users":["Local user"],
     "outcome":"Create and revisit saved items","domain":"offline-tasks"}
HIGH={**LOW,"slug":"vrs-demo","domain":"vrs"}


class UnifiedStarterTests(unittest.TestCase):
    def test_opt_in_only_and_scope_remains_unapproved(self):
        base=plan_bootstrap(LOW)
        self.assertNotIn("app/server.py",base)
        full=plan_bootstrap(LOW,working_profile="web-list")
        self.assertIn("app/server.py",full)
        self.assertIn("app/index.html",full)
        self.assertIn("tests/test_app.py",full)
        self.assertIn("tools/startup.py",full)
        self.assertEqual(json.loads(full["delivery/current-state.yaml"])["status"],"blocked")
        self.assertFalse(json.loads(full["delivery/approvals.json"])["merge"])
        self.assertEqual(json.loads(full["project.yaml"])["runtime_status"],"local-demo-only")
        self.assertEqual(full,plan_bootstrap(dict(LOW),working_profile="web-list"))

    def test_reject_high_risk_and_unknown_profiles(self):
        with self.assertRaises(ValueError):
            plan_bootstrap(HIGH,working_profile="web-list")
        with self.assertRaises(ValueError):
            plan_bootstrap({**LOW,"risks":["personal-data"]},working_profile="web-list")
        with self.assertRaises(ValueError):
            plan_bootstrap(LOW,working_profile="unknown")

    def test_generate_and_test_one_documented_runnable_project(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            brief=root/"brief.json"
            brief.write_text(json.dumps(LOW))
            output=root/"generated"
            base=Path(__file__).resolve().parents[1]
            plan=subprocess.run([
                sys.executable,"-m","ade.bootstrap_cli","plan",str(brief),
                "--working-web-list"],cwd=base,capture_output=True,text=True,timeout=15)
            self.assertEqual(plan.returncode,0,plan.stderr)
            self.assertFalse(output.exists())
            created=subprocess.run([
                sys.executable,"-m","ade.bootstrap_cli","create",str(brief),
                str(output),"--working-web-list"],cwd=base,
                capture_output=True,text=True,timeout=15)
            self.assertEqual(created.returncode,0,created.stderr)
            self.assertIn("app/server.py",json.loads(created.stdout)["generated"])
            self.assertIn("python -m app.server",(output/"README.md").read_text())
            preflight=subprocess.run([sys.executable,"tools/startup.py"],cwd=output,
                                    capture_output=True,text=True,timeout=15)
            self.assertEqual(preflight.returncode,2)
            self.assertEqual(json.loads(preflight.stdout)["decision"],"STOP")
            tested=subprocess.run([sys.executable,"-m","unittest","discover",
                                   "-s","tests","-v"],cwd=output,
                                  capture_output=True,text=True,timeout=20)
            self.assertEqual(tested.returncode,0,tested.stderr)

    def test_existing_target_refused_without_data_loss(self):
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/"existing"
            output.mkdir()
            marker=output/"keep-me.txt"
            marker.write_text("keep")
            with self.assertRaises(FileExistsError):
                bootstrap(LOW,output,working_profile="web-list")
            self.assertEqual(marker.read_text(),"keep")


if __name__=="__main__":
    unittest.main()
