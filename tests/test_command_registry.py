"""Advertised Engine commands must be truthful, narrow, and non-privileged."""
import json
import unittest
from pathlib import Path

from ade.bootstrap import plan_bootstrap
from ade.method_selection import select_method
from ade.generator import plan


ROOT=Path(__file__).resolve().parents[1]


class CommandRegistryTests(unittest.TestCase):
    def test_registry_only_lists_real_narrow_operations(self):
        registry=json.loads((ROOT/"registry/commands.json").read_text())
        self.assertEqual(registry["schema_version"],"1.0")
        ids=[item["id"] for item in registry["commands"]]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(set(ids),{
            "repo.bootstrap.plan","repo.bootstrap.create",
            "repo.scaffold.generate","repo.continuity.start","method.select",
            "continuity.next-work.recommend","continuity.github.reconcile",
            "continuity.github.inspect", "control-center.readonly",
            "repo.demo.run", "intelligence.registry.plan"})
        for command in registry["commands"]:
            self.assertIn(command["effect"],{
                "read-only","local-create-only","pure-function",
                "localhost-read-only","local-create-and-run"})
            self.assertNotIn("deploy",command["id"])
            self.assertNotIn("shell",command["id"])
            self.assertTrue(command["guarantee"])
            self.assertNotIn(command["status"],("automatic-release","independent-review"))

    def test_new_entrypoints_are_real_and_bounded(self):
        from ade.control_center import catalog, Handler
        from ade.demo import run_demo
        from ade.registry_bridge import assess_snapshot
        self.assertTrue(callable(run_demo))
        self.assertTrue(callable(assess_snapshot))
        self.assertTrue(hasattr(Handler, "do_GET"))
        self.assertIn("control-center.readonly",
                      {x["id"] for x in catalog()["commands"]})

    def test_existing_entrypoints_match_claimed_modes(self):
        self.assertIn("AGENTS.md",plan_bootstrap({
            "schema_version":"1.0","slug":"verify-commands","title":"Verify",
            "problem":"A small application","users":["Reader"],
            "outcome":"A valid starter","domain":"offline-tasks"}))
        self.assertIn("README.md",plan({
            "schema_version":"1.0","slug":"verify-commands",
            "title":"Verify","outcome":"A minimal demo"}))
        selected=select_method("new-slice",[])
        self.assertIn("no-automatic-merge",selected["stop_gates"])


if __name__=="__main__":
    unittest.main()
