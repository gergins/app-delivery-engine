"""Evidence-based pipeline learning must never silently self-promote."""
import unittest
from ade.learning_loop import recommend_learning


def observation(identifier, repository, mechanism="browser-setup", verified=True,
                outcome="success"):
    return {
        "id": identifier, "repository": repository,
        "commit_sha": "a" * 40,
        "evidence_url": "https://github.com/example/repo/actions/runs/123",
        "category": "efficiency", "mechanism": mechanism,
        "finding": "Browser setup dominates elapsed CI time",
        "verified": verified, "outcome": outcome,
    }


class LearningLoopTests(unittest.TestCase):
    def test_single_application_does_not_promote(self):
        output = recommend_learning([
            observation("a", "example/camping"),
            observation("b", "example/camping")])
        p = output["proposals"][0]
        self.assertEqual(p["decision"], "defer")
        self.assertEqual(p["repositories"], ["example/camping"])
        self.assertFalse(p["may_modify_pipeline"])

    def test_distinct_apps_propose_trial_not_automatic_change(self):
        output = recommend_learning([
            observation("b", "example/community"),
            observation("a", "example/camping")])
        p = output["proposals"][0]
        self.assertEqual(p["decision"], "propose")
        self.assertFalse(p["may_modify_pipeline"])
        self.assertFalse(p["may_reduce_required_tests"])
        self.assertEqual(p["evidence_ids"], ["a", "b"])

    def test_unverified_or_unknown_cannot_influence_learning(self):
        output = recommend_learning([
            observation("a", "example/camping"),
            observation("b", "example/community", verified=False),
            observation("c", "example/other", outcome="unknown")])
        self.assertEqual(output["proposals"][0]["decision"], "defer")
        self.assertEqual(output["unverified_observations_ignored"], 2)

    def test_mechanisms_are_not_falsely_combined(self):
        output = recommend_learning([
            observation("a", "example/camping", "keycloak-setup"),
            observation("b", "example/community", "browser-setup")])
        self.assertEqual(len(output["proposals"]), 2)
        self.assertTrue(all(p["decision"] == "defer" for p in output["proposals"]))

    def test_invalid_inputs_fail_closed(self):
        for bad in (
            "not-list",
            [observation("a", "example/camping")] * 2,
            [{**observation("a", "example/camping"), "commit_sha": "stale"}],
            [{**observation("a", "example/camping"), "category": "unknown"}],
            [{**observation("a", "example/camping"), "verified": "yes"}],
            [{**observation("a", "example/camping"), "evidence_url": "http://other"}],
        ):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    recommend_learning(bad)


if __name__ == "__main__":
    unittest.main()
