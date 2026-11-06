"""Read-only ADE dashboard HTTP contract, no network, no credentials."""
import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from unittest.mock import patch

from ade import control_center


class ControlCenterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), control_center.Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = "http://127.0.0.1:" + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def read(self, path, method="GET"):
        req = urllib.request.Request(self.url + path, method=method)
        try:
            with urllib.request.urlopen(req, timeout=4) as r:
                return r.status, r.read().decode(), dict(r.headers)
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read().decode(), dict(exc.headers)

    def test_local_dashboard_is_actual_ade_interface(self):
        status, body, headers = self.read("/")
        self.assertEqual(status, 200)
        self.assertIn("ADE · Engineering Control Center", body)
        self.assertIn('id="inspectForm"', body)
        self.assertIn("default-src 'none'", headers["Content-Security-Policy"])
        self.assertIn("text/html", headers["Content-Type"])

    def test_live_registered_commands_from_existing_catalog(self):
        status, body, _ = self.read("/api/commands")
        self.assertEqual(status, 200)
        data = json.loads(body)
        ids = [item["id"] for item in data["commands"]]
        self.assertIn("method.select", ids)
        self.assertIn("repo.bootstrap.create", ids)

    def test_pr_remote_inspection_is_explicit_and_read_only(self):
        snapshot = {"decision": "RECONCILED", "head_sha": "a" * 40,
                    "ci_status": "success",
                    "approvals": {"merge": False, "deploy": False}}
        with patch.object(control_center, "inspect_pull_request",
                          return_value=snapshot) as call:
            status, body, _ = self.read("/api/inspect?repo=gergins%2Fapp-delivery-engine&pr=6")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body), snapshot)
        call.assert_called_once_with("gergins/app-delivery-engine", 6)

    def test_remote_failure_fails_closed(self):
        with patch.object(control_center, "inspect_pull_request",
                          side_effect=urllib.error.URLError("fake offline")):
            status, body, _ = self.read("/api/inspect?repo=gergins%2Fapp-delivery-engine&pr=6")
        self.assertEqual(status, 400)
        self.assertEqual(json.loads(body)["decision"], "STOP")

    def test_invalid_number_and_extra_parameters(self):
        for path in ("/api/inspect?repo=a%2Fb&pr=abc",
                     "/api/inspect?repo=a%2Fb&pr=1&admin=true",
                     "/api/inspect?repo=a%2Fb&pr=0"):
            status, body, _ = self.read(path)
            self.assertEqual(status, 400)
            self.assertEqual(json.loads(body)["decision"], "STOP")

    def test_browser_favicon_and_index_alias(self):
        status, _, _ = self.read("/favicon.ico")
        self.assertEqual(status, 204)
        status, body, _ = self.read("/index.html")
        self.assertEqual(status, 200)
        self.assertIn("ADE · Engineering Control Center", body)

    def post_builder(self, route, payload, *, origin=True):
        headers = {"Content-Type": "application/json"}
        if origin:
            headers["Origin"] = self.url
        req = urllib.request.Request(
            self.url + route, data=json.dumps(payload).encode(),
            headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as err:
            return err.code, json.loads(err.read())

    def test_builder_workflow_from_browser_is_real(self):
        from ade.app_builder import TEMPLATE
        from pathlib import Path
        import tempfile
        request = {"slug": "desk-items", "title": "Desk Items",
                   "idea": "Store a private list of my desk items on this computer.",
                   "template": TEMPLATE}
        with tempfile.TemporaryDirectory() as root:
            with patch.object(control_center, "WORKSPACE", Path(root)):
                status, plan = self.post_builder("/api/app-builder/plan", request)
                self.assertEqual(status, 200)
                self.assertEqual(plan["decision"], "PLAN")
                self.assertFalse((Path(root) / "desk-items").exists())
                status, created = self.post_builder("/api/app-builder/create", {
                    "request": request, "plan_hash": plan["plan_hash"], "confirmed": True})
                self.assertEqual(status, 200, created)
                self.assertTrue(created["tests_passed"])
                self.assertFalse(created["approval_granted"])
                self.assertTrue((Path(root) / "desk-items" / "app" / "server.py").exists())
                status, rejected = self.post_builder("/api/app-builder/create", {
                    "request": request, "plan_hash": plan["plan_hash"], "confirmed": True})
                self.assertEqual(status, 409)
                self.assertEqual(rejected["decision"], "STOP")

    def test_builder_requires_same_origin_and_explicit_current_confirmation(self):
        request = {"slug": "desk-items", "title": "Desk Items",
                   "idea": "Store a private list of my desk items on this computer.",
                   "template": "offline-list"}
        status, rejected = self.post_builder("/api/app-builder/plan", request, origin=False)
        self.assertEqual(status, 403)
        self.assertEqual(rejected["reason"], "origin-not-allowed")
        status, rejected = self.post_builder("/api/app-builder/create", {
            "request": request, "plan_hash": "invalid", "confirmed": False})
        self.assertEqual(status, 409)
        self.assertEqual(rejected["decision"], "STOP")

    def test_posts_and_unknown_routes_are_blocked(self):
        status, _, _ = self.read("/api/inspect", method="POST")
        self.assertEqual(status, 405)
        status, body, headers = self.read("/not-found")
        self.assertEqual(status, 404)
        self.assertIn("ADE Control Center home", body)
        self.assertIn("text/html", headers["Content-Type"])
        status, body, _ = self.read("/api/unknown")
        self.assertEqual(status, 404)
        self.assertEqual(json.loads(body)["reason"], "unknown-api-route")


if __name__ == "__main__":
    unittest.main()
