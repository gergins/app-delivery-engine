"""Synthetic new-contributor journey, not an independent human usability study."""
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

SOURCE = Path(__file__).resolve().parents[1]


class FreshSessionTests(unittest.TestCase):
    def test_brief_to_local_app_restart_and_handoff_without_source_edits(self):
        with tempfile.TemporaryDirectory() as temp:
            scratch = Path(temp)
            brief = SOURCE / "examples/offline-list-brief.json"
            dest = scratch / "app"
            started = time.monotonic()
            invocations = 0

            def execute(*args, cwd=SOURCE, expected=0):
                nonlocal invocations
                invocations += 1
                p = subprocess.run([sys.executable, *args], cwd=cwd,
                                   capture_output=True, text=True, timeout=25)
                self.assertEqual(p.returncode, expected, p.stderr + p.stdout)
                return p

            planned = execute("-m", "ade.bootstrap_cli", "plan", str(brief), "--working-web-list")
            self.assertFalse(dest.exists())
            self.assertIn("app/server.py", json.loads(planned.stdout)["files"])
            execute("-m", "ade.bootstrap_cli", "create", str(brief),
                    str(dest), "--working-web-list")
            self.assertIn("*.sqlite3", (dest / ".gitignore").read_text())
            self.assertTrue((dest / "AGENTS.md").exists())
            before = {str(p.relative_to(dest)): p.read_bytes()
                      for p in dest.rglob("*") if p.is_file() and
                      p.suffix in (".py", ".html", ".js")}
            execute("-m", "unittest", "discover", "-s", "tests",
                    "-p", "test_app.py", "-v", cwd=dest)
            preflight = execute("tools/startup.py", cwd=dest, expected=2)
            result = json.loads(preflight.stdout)
            self.assertEqual(result["reason"], "approval-or-requirements-gate")
            self.assertTrue(result["requires_remote_github_verification"])

            def start_server():
                nonlocal invocations
                invocations += 1
                proc = subprocess.Popen([sys.executable, "-m", "app.server"],
                                        cwd=dest, stdout=subprocess.DEVNULL,
                                        stderr=subprocess.PIPE)
                for _ in range(70):
                    if proc.poll() is not None:
                        self.fail("Server exited early: " +
                                  proc.stderr.read().decode(errors="replace")[:200])
                    try:
                        with urlopen("http://127.0.0.1:8000/health", timeout=1) as response:
                            if json.load(response) == {"status": "ok"}:
                                return proc
                    except (URLError, OSError):
                        time.sleep(.1)
                proc.kill()
                proc.wait(timeout=5)
                self.fail("Server never started")

            def stop_server(proc):
                proc.terminate()
                try:
                    proc.wait(timeout=4)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=5)
                proc.stderr.close()

            process = start_server()
            try:
                payload = json.dumps({"title": "resume me"}).encode()
                with urlopen(Request("http://127.0.0.1:8000/api/items",
                                     data=payload,
                                     headers={"Content-Type": "application/json"}),
                             timeout=3) as response:
                    self.assertEqual(response.status, 201)
            finally:
                stop_server(process)
            process = start_server()
            try:
                with urlopen("http://127.0.0.1:8000/api/items", timeout=3) as response:
                    self.assertEqual(json.load(response)["items"][0]["title"], "resume me")
                resume = execute("tools/startup.py", cwd=dest, expected=2)
                self.assertEqual(json.loads(resume.stdout)["decision"], "STOP")
            finally:
                stop_server(process)

            after = {str(p.relative_to(dest)): p.read_bytes()
                     for p in dest.rglob("*") if p.is_file() and
                     p.suffix in (".py", ".html", ".js")}
            self.assertEqual(before, after, "Required changes to generated source")
            print(json.dumps({
                "benchmark": "unified-starter-synthetic-fresh-session",
                "scope": "automated-cli-http-restart-no-independent-user",
                "cli_invocations_including_server_starts": invocations,
                "server_starts": 2, "manual_source_edits": 0,
                "network_dependencies": 0, "persisted_after_restart": True,
                "scope_gate_remains_blocked": True,
                "elapsed_seconds": round(time.monotonic() - started, 3)
            }, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
