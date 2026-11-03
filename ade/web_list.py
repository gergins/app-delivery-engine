"""Minimal reusable local web-list application profile.

Produces a real UI → JSON API → SQLite vertical slice.
No third-party runtime dependency, credentials or deployment.
"""
from .generator import validate


def files(spec):
    validate(spec)
    title = spec["title"]
    html = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>APP_TITLE</title>
<style>body{font:1rem/1.5 system-ui;max-width:650px;margin:35px auto;padding:0 16px}
input,button{font:inherit;padding:9px}input:focus-visible,button:focus-visible{outline:3px solid orange}
li{padding:5px;overflow-wrap:anywhere}</style></head><body><main>
<h1>APP_TITLE</h1><form id="form"><label for="item">New item</label>
<input id="item" required maxlength="100"><button>Add</button></form>
<p id="status" role="status" aria-live="polite"></p>
<h2>Items</h2><ul id="items"></ul></main>
<script src="/app.js" defer></script></body></html>
""".replace("APP_TITLE", _escape_html(title))
    script = """const list=document.getElementById('items'),status=document.getElementById('status');
async function refresh(){
  try{
    const response=await fetch('/api/items');
    if(!response.ok)throw Error('load');
    const data=await response.json();
    list.replaceChildren();
    for(const item of data.items){
      const li=document.createElement('li');li.textContent=item.title;list.append(li);
    }
  }catch(_){status.textContent='Failed to load items';}
}
document.getElementById('form').addEventListener('submit',async event=>{
  event.preventDefault();
  const input=document.getElementById('item');
  try{
    const response=await fetch('/api/items',{method:'POST',
      headers:{'Content-Type':'application/json'},body:JSON.stringify({title:input.value})});
    if(!response.ok)throw Error('save');
    input.value='';status.textContent='Item saved';await refresh();input.focus();
  }catch(_){status.textContent='Failed to save item';}
});
refresh();
"""
    server = '''"""Loopback-only demo server with SQLite persistence."""
import json
import os
import sqlite3
from contextlib import closing
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).parent

def connect(db_path):
    db = sqlite3.connect(db_path, timeout=5)
    db.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, title TEXT NOT NULL)")
    db.commit()
    return db

def list_items(db_path):
    with closing(connect(db_path)) as db:
        return [{"id": row[0], "title": row[1]} for row in
                db.execute("SELECT id, title FROM items ORDER BY id DESC LIMIT 100")]

def add_item(db_path, title):
    if (type(title) is not str or not title.strip() or len(title.strip()) > 100
            or any(ord(c) < 32 for c in title)):
        raise ValueError("Invalid title")
    with closing(connect(db_path)) as db:
        cursor = db.execute("INSERT INTO items(title) VALUES (?)", (title.strip(),))
        db.commit()
        return {"id": cursor.lastrowid, "title": title.strip()}

def handler_factory(db_path):
    class Handler(BaseHTTPRequestHandler):
        def send_body(self, status, payload, mime):
            self.send_response(status)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy",
                             "default-src 'none'; script-src 'self'; connect-src 'self'; style-src 'unsafe-inline'")
            self.end_headers()
            self.wfile.write(payload)

        def json_reply(self, status, obj):
            self.send_body(status, json.dumps(obj).encode("utf-8"), "application/json")

        def do_GET(self):
            route = urlsplit(self.path).path
            if route == "/":
                return self.send_body(200, (ROOT / "index.html").read_bytes(), "text/html; charset=utf-8")
            if route == "/app.js":
                return self.send_body(200, (ROOT / "app.js").read_bytes(), "application/javascript")
            if route == "/health":
                return self.json_reply(200, {"status": "ok"})
            if route == "/api/items":
                return self.json_reply(200, {"items": list_items(db_path)})
            return self.json_reply(404, {"error": "not_found"})

        def do_POST(self):
            if urlsplit(self.path).path != "/api/items":
                return self.json_reply(404, {"error": "not_found"})
            if self.headers.get("Content-Type", "").split(";")[0].strip().lower() != "application/json":
                return self.json_reply(415, {"error": "invalid_content_type"})
            length = self.headers.get("Content-Length", "")
            if not length.isdecimal() or not 0 < int(length) <= 2048:
                return self.json_reply(413, {"error": "invalid_length"})
            try:
                payload = json.loads(self.rfile.read(int(length)))
                if not isinstance(payload, dict) or set(payload) != {"title"}:
                    raise ValueError("Invalid payload")
                result = add_item(db_path, payload["title"])
            except (ValueError, UnicodeDecodeError, RecursionError):
                return self.json_reply(400, {"error": "invalid_input"})
            return self.json_reply(201, result)

        def log_message(self, fmt, *args):
            pass

    return Handler

def make_server(db_path, host="127.0.0.1", port=0):
    if host != "127.0.0.1":
        raise ValueError("Local-only demo")
    return ThreadingHTTPServer((host, port), handler_factory(db_path))

if __name__ == "__main__":
    server = make_server(os.environ.get("APP_DB", str(ROOT / "local.sqlite3")), port=8000)
    print("Local demo: http://127.0.0.1:8000", flush=True)
    server.serve_forever()
'''
    tests = '''import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from app.server import make_server, add_item, list_items

class AppTests(unittest.TestCase):
    def test_persistence_validation_and_http(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "data.sqlite3"
            self.assertEqual(list_items(db), [])
            with self.assertRaises(ValueError):
                add_item(db, "")
            server = make_server(db)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                base = "http://127.0.0.1:" + str(server.server_port)
                req = Request(base + "/api/items", data=json.dumps({"title": "hello"}).encode(),
                              headers={"Content-Type": "application/json"})
                with urlopen(req, timeout=3) as res:
                    self.assertEqual(res.status, 201)
                with urlopen(base + "/api/items", timeout=3) as res:
                    self.assertEqual(json.load(res)["items"][0]["title"], "hello")
                with urlopen(base, timeout=3) as res:
                    self.assertIn(b"<form", res.read())
                with urlopen(base + "/app.js", timeout=3) as res:
                    self.assertIn(b"fetch(", res.read())
                bad = Request(base + "/api/items", data=json.dumps({"title": []}).encode(),
                              headers={"Content-Type": "application/json"})
                with self.assertRaises(HTTPError) as exc:
                    urlopen(bad, timeout=3)
                self.assertEqual(exc.exception.code, 400)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)
            self.assertEqual(list_items(db)[0]["title"], "hello")

    def test_local_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                make_server(str(Path(tmp) / "data.db"), host="0.0.0.0")

if __name__ == "__main__":
    unittest.main()
'''
    browser = '''import tempfile
import threading
import unittest
from pathlib import Path
from app.server import make_server

class BrowserTests(unittest.TestCase):
    def test_browser_to_api_to_sqlite_and_reload(self):
        from playwright.sync_api import sync_playwright
        with tempfile.TemporaryDirectory() as tmp:
            server = make_server(str(Path(tmp) / "data.sqlite3"))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    try:
                        page = browser.new_page()
                        page.goto("http://127.0.0.1:" + str(server.server_port))
                        page.get_by_label("New item").fill("verified item")
                        page.get_by_role("button", name="Add").click()
                        page.get_by_text("Item saved").wait_for()
                        self.assertEqual(page.locator("#items li").first.inner_text(), "verified item")
                        page.reload()
                        self.assertEqual(page.locator("#items li").first.inner_text(), "verified item")
                    finally:
                        browser.close()
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)
'''
    return {
        "app/__init__.py": "",
        "app/server.py": server,
        "app/index.html": html,
        "app/app.js": script,
        "tests/test_app.py": tests,
        "tests/test_browser.py": browser,
        "README.md": "# " + title + "\n\nLocal-only web-list benchmark; no authentication or public deployment.\n"
                     "Run: `python -m app.server` then open http://127.0.0.1:8000.\n"
                     "Tests: `python -m unittest discover -s tests -p test_app.py -v`.\n",
        ".gitignore": "__pycache__/\n*.pyc\n*.sqlite3\n.env\n",
    }


def _escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")
