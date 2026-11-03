"""Fresh-checkout, no-edit first-run benchmark of the existing working app.

This is automated onboarding evidence, not a human usability study. Browser
behavior is separately verified by the existing Chromium CI.
"""
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request,urlopen

from ade.generator import generate

SPEC={"schema_version":"1.0","slug":"first-run-list","title":"First Run List",
      "outcome":"Add an item and see it after server restart","profile":"web-list"}


class FirstRunBenchmarkTests(unittest.TestCase):
    def test_new_app_generate_run_save_restart_no_source_edits(self):
        with tempfile.TemporaryDirectory() as root:
            directory=Path(root)/"working-app"
            started=time.monotonic()
            generated=generate(SPEC,directory)
            self.assertTrue((directory/"app/server.py").is_file())
            self.assertTrue((directory/"app/index.html").is_file())
            before={str(path.relative_to(directory)):path.read_bytes()
                    for path in directory.rglob("*") if path.is_file() and
                    path.suffix in (".py",".js",".html")}
            base="http://127.0.0.1:8000"
            def request(method="GET",route="/health",payload=None):
                body=None if payload is None else json.dumps(payload).encode("utf-8")
                req=Request(base+route,data=body,method=method,
                    headers={"Content-Type":"application/json"} if body is not None else {})
                with urlopen(req,timeout=2) as reply:
                    return reply.status,json.load(reply) if route!="/" else reply.read()
            def start():
                proc=subprocess.Popen(
                    [sys.executable,"-m","app.server"],cwd=directory,
                    stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
                for _ in range(60):
                    if proc.poll() is not None:
                        raise AssertionError("Generated server exited before ready: "+
                                             proc.stderr.read().decode("utf-8")[:350])
                    try:
                        status,result=request()
                        if status==200 and result=={"status":"ok"}:
                            return proc
                    except (OSError,URLError):
                        time.sleep(.1)
                proc.terminate()
                proc.wait(timeout=3)
                raise AssertionError("Generated server did not become healthy")
            def stop(proc):
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=3)
                proc.stderr.close()
            p=start()
            try:
                status,created=request("POST","/api/items",{"title":"Useful saved item"})
                self.assertEqual(status,201)
                self.assertEqual(created["title"],"Useful saved item")
                self.assertEqual(request(route="/api/items")[1]["items"][0]["title"],
                                 "Useful saved item")
            finally:
                stop(p)
            p=start()
            try:
                self.assertEqual(request(route="/api/items")[1]["items"][0]["title"],
                                 "Useful saved item")
            finally:
                stop(p)
            after={str(path.relative_to(directory)):path.read_bytes()
                   for path in directory.rglob("*") if path.is_file() and
                   path.suffix in (".py",".js",".html")}
            self.assertEqual(before,after,"Working app required manual source changes")
            elapsed=time.monotonic()-started
            print(json.dumps({"benchmark":"first-run-working-web-list",
                              "source_edits":0,"generated_files":len(generated),
                              "server_starts":2,"persisted_after_restart":True,
                              "elapsed_seconds":round(elapsed,3),
                              "scope":"synthetic-CI-not-human-usability"},sort_keys=True))


if __name__=="__main__":
    unittest.main()
