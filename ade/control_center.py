"""ADE local read-only engineering control center (stdlib, localhost only).

Displays actual registered commands and allows an explicit read-only GitHub PR
inspection through ADE's existing connector. Never persists tokens or grants
execution approvals. No background jobs, shell dispatch, or cloud deployment.
"""
import argparse
import json
import re
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from .github_readonly import inspect_pull_request
from .app_builder import plan_request, create_project

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "registry" / "commands.json"
WORKSPACE = Path.home() / "ADE-Projects"
MAX_BODY = 6000

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ADE Engineering Control Center</title>
<style>
:root{font-family:system-ui,-apple-system,Segoe UI,sans-serif;color-scheme:light;background:#f3f5f9;color:#15243c}
*{box-sizing:border-box}body{margin:0}header{background:#142440;color:white;padding:22px max(5vw,18px)}
header p{color:#c8d7ef;margin:5px 0}main{max-width:1100px;margin:auto;padding:24px 18px}
h1{font-size:1.55rem;margin:0}h2{font-size:1.15rem;margin:0 0 14px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:18px}
section{background:white;border:1px solid #d9e0ea;border-radius:14px;padding:20px;margin-bottom:18px}
label{display:block;font-weight:600;margin:10px 0 5px}input{width:100%;padding:11px;border:1px solid #8797ae;border-radius:7px;font:inherit}
button{margin-top:14px;background:#2157c8;color:white;border:0;border-radius:7px;padding:11px 18px;font:inherit;cursor:pointer}
button:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid #df8d11;outline-offset:3px}
small,.subtle{color:#52627a}.item{border-top:1px solid #e6eaf0;padding:11px 0}
code{overflow-wrap:anywhere}pre{overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere;background:#f5f7fa;padding:12px;border-radius:8px}
.status{font-weight:700} .warning{color:#9a4509}.ok{color:#166347}
#result{min-height:60px}footer{padding:12px 0;color:#52627a}
</style></head><body>
<header><h1>ADE · Engineering Control Center</h1>
<p>Read-only local dashboard · GitHub evidence · methods · capabilities</p></header>
<main>
<section><h2>System boundaries</h2><p>This is the real ADE control interface, not the generated items-list app.
It is a read-only first milestone: no automatic coding, merging, deployment or approval.</p>
<p><strong>Private Registry:</strong> the separate registry bridge accepts a locally supplied pinned snapshot.
This dashboard does not expose or automatically fetch its contents.</p></section>
<div class="grid">
<section><h2>Inspect project PR and CI</h2><p class="subtle">Live GitHub read, only when you select Inspect. For private repositories, configure a read-only GITHUB_TOKEN in your trusted local environment.</p>
<form id="inspectForm"><label for="repo">GitHub repository (owner/name)</label>
<input id="repo" required maxlength="100" value="gergins/app-delivery-engine" autocomplete="off">
<label for="pr">Pull request number</label><input id="pr" required type="number" min="1" max="1000000" value="6">
<button type="submit">Inspect latest evidence</button></form>
<div id="result" role="status" aria-live="polite"><p class="subtle">No PR inspected yet. Remote verification is not claimed.</p></div></section>
<section><h2>Available ADE commands</h2><p class="subtle">Only real registered operations. Execute commands manually from a trusted terminal.</p>
<div id="commands" aria-live="polite">Loading command catalog...</div></section>
</div>
<section><h2>App Builder — first working workflow</h2>
<p class="subtle">Describe a low-risk single-user list app. ADE will show a plan before creating
a project in your local ADE-Projects workspace. This is a reusable template, not general AI coding.</p>
<form id="builderForm">
<div class="grid"><div><label for="appTitle">App name</label><input id="appTitle" maxlength="100" required value="Family Items"></div>
<div><label for="appSlug">Project folder name</label><input id="appSlug" maxlength="50" pattern="[a-z][a-z0-9-]{2,49}" required value="family-items"></div></div>
<label for="appIdea">What do you want it to do?</label>
<textarea id="appIdea" rows="3" maxlength="1000" required style="width:100%;padding:12px;font:inherit;border:1px solid #8797ae;border-radius:7px">Keep a simple personal list of household items on my laptop.</textarea>
<input type="hidden" id="appTemplate" value="offline-list">
<button type="submit">1. Review engineering plan</button></form>
<div id="builderResult" role="status" aria-live="polite"><p class="subtle">No project planned. Nothing will be created until you confirm.</p></div>
<div id="builderConfirm" hidden><label><input type="checkbox" id="approveCreate" style="width:auto">
I reviewed the plan and approve creating only this local demonstration.</label>
<button id="createApp" type="button">2. Create and test project</button></div></section>
<section><h2>Engineering status</h2><div class="grid">
<div><strong>Delivery and method selection</strong><p>Runnable local starter, tests, advisory method controls and continuity helpers.</p></div>
<div><strong>Registry intelligence</strong><p>Read-only snapshot bridge; private-source authentication and cross-repository verification remain separate.</p></div>
<div><strong>Human authority</strong><p>PR evidence is not merge approval. Release, paid infrastructure, external reviewers and deployment stay blocked without authorization.</p></div>
</div></section>
<footer>Local-only server at 127.0.0.1 · No telemetry or persisted project data in dashboard</footer>
</main>
<script>
"use strict";
const result=document.getElementById("result"),commands=document.getElementById("commands");
function el(tag, text, cls){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n}
function clear(node){while(node.firstChild)node.removeChild(node.firstChild)}
async function loadCommands(){
 try{
  const response=await fetch("/api/commands",{cache:"no-store"});
  if(!response.ok)throw new Error("Catalog unavailable");
  const data=await response.json();clear(commands);
  for(const cmd of data.commands){
   const item=el("div",undefined,"item");
   item.append(el("strong",cmd.id),el("div",cmd.effect+" · "+cmd.status,"subtle"));
   item.append(el("code",cmd.entrypoint));commands.append(item);
  }
 }catch(e){commands.textContent="Command catalog unavailable. Inspect local ADE installation."}
}
document.getElementById("inspectForm").addEventListener("submit",async(event)=>{
 event.preventDefault();clear(result);result.append(el("p","Inspecting remote state..."));
 const repo=document.getElementById("repo").value.trim();
 const pr=document.getElementById("pr").value;
 try{
  const response=await fetch("/api/inspect?"+new URLSearchParams({repo,pr}),{cache:"no-store"});
  const data=await response.json();clear(result);
  const decision=String(data.decision||"STOP");
  result.append(el("p","Decision: "+decision,"status "+(decision==="RECONCILED"?"ok":"warning")));
  if(data.reason)result.append(el("p","Reason: "+data.reason));
  if(data.head_sha)result.append(el("p","PR HEAD: "+data.head_sha));
  if(data.ci_status)result.append(el("p","Exact-HEAD CI: "+data.ci_status));
  if(data.approvals)result.append(el("p","Merge/deploy approvals: not granted by ADE","warning"));
  if(Array.isArray(data.workflow_urls))for(const url of data.workflow_urls){
   if(typeof url==="string"&&url.startsWith("https://github.com/")){
    const a=el("a","GitHub Actions evidence");a.href=url;a.target="_blank";a.rel="noopener noreferrer";result.append(a);
   }
  }
  if(!response.ok)result.append(el("p","Inspection blocked or incomplete.","warning"));
 }catch(e){clear(result);result.append(el("p","Inspection failed. No verified status.","warning"))}
});

let proposed=null;
const builderForm=document.getElementById("builderForm"),builderResult=document.getElementById("builderResult"),
      confirmation=document.getElementById("builderConfirm");
function currentRequest(){return {slug:document.getElementById("appSlug").value.trim(),
 title:document.getElementById("appTitle").value.trim(),idea:document.getElementById("appIdea").value.trim(),template:"offline-list"}}
async function builderCall(route,payload){
 const response=await fetch(route,{method:"POST",headers:{"Content-Type":"application/json"},
  body:JSON.stringify(payload),cache:"no-store"});
 const data=await response.json();
 if(!response.ok)throw new Error(data.reason||"Operation blocked");
 return data;
}
builderForm.addEventListener("submit",async(e)=>{
 e.preventDefault();proposed=null;confirmation.hidden=true;clear(builderResult);
 builderResult.append(el("p","Reviewing plan..."));
 try{
  const request=currentRequest();
  const data=await builderCall("/api/app-builder/plan",request);
  proposed={request,hash:data.plan_hash};clear(builderResult);
  builderResult.append(el("h3","Proposed local application"));
  builderResult.append(el("p",data.implemented_behavior));
  builderResult.append(el("p","Planned files: "+data.files));
  builderResult.append(el("p","NOT included: "+data.not_implemented.join(", "),"warning"));
  builderResult.append(el("p","Project scope and production release remain unapproved.","warning"));
  document.getElementById("approveCreate").checked=false;confirmation.hidden=false;
 }catch(err){clear(builderResult);builderResult.append(el("p","STOP: "+err.message,"warning"))}
});
for(const id of ["appSlug","appTitle","appIdea"]){
 document.getElementById(id).addEventListener("input",()=>{proposed=null;confirmation.hidden=true;
 clear(builderResult);builderResult.append(el("p","Inputs changed. Review a new plan before creating.","warning"))})
}
document.getElementById("createApp").addEventListener("click",async()=>{
 if(!proposed||!document.getElementById("approveCreate").checked){
  builderResult.append(el("p","Review the plan and check the confirmation first.","warning"));return
 }
 confirmation.hidden=true;
 builderResult.append(el("p","Creating and testing local project..."));
 try{
  const data=await builderCall("/api/app-builder/create",
    {request:proposed.request,plan_hash:proposed.hash,confirmed:true});
  clear(builderResult);builderResult.append(el("h3","Local project created and tested","ok"));
  builderResult.append(el("p","Directory: "+data.project_path));
  builderResult.append(el("p","Local API smoke tests passed: "+String(data.tests_passed)));
  builderResult.append(el("p","Open PowerShell and run:"));
  builderResult.append(el("pre",data.start_command));
  builderResult.append(el("p","Then open "+data.preview_url+" in the browser. Production approval is still required.","subtle"));
  proposed=null;
 }catch(err){clear(builderResult);builderResult.append(el("p","STOP: "+err.message,"warning"))}
});

loadCommands();
</script></body></html>"""


def catalog():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if (type(data) is not dict or data.get("schema_version") != "1.0"
            or type(data.get("commands")) is not list):
        raise ValueError("Command registry unavailable")
    return {"schema_version": "1.0", "commands": data["commands"]}


class Handler(BaseHTTPRequestHandler):
    def respond(self, status, content_type, body):
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy",
                         "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; base-uri 'none'; form-action 'self'")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(encoded)

    def respond_json(self, status, obj):
        self.respond(status, "application/json; charset=utf-8",
                     json.dumps(obj, sort_keys=True))

    def do_GET(self):
        url = urlsplit(self.path)
        if url.path in ("/", "/index.html") and not url.query:
            return self.respond(200, "text/html; charset=utf-8", PAGE)
        if url.path == "/favicon.ico" and not url.query:
            # Browsers request this automatically; it is not a failed ADE operation.
            self.send_response(204)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if url.path == "/api/commands" and not url.query:
            try:
                return self.respond_json(200, catalog())
            except (OSError, ValueError):
                return self.respond_json(503, {"decision": "STOP",
                                               "reason": "command-catalog-unavailable"})
        if url.path == "/api/inspect":
            try:
                args = parse_qs(url.query, strict_parsing=True)
                if set(args) != {"repo", "pr"} or any(len(value) != 1 for value in args.values()):
                    raise ValueError("Invalid query")
                number = int(args["pr"][0])
                if str(number) != args["pr"][0]:
                    raise ValueError("Invalid PR number")
                result = inspect_pull_request(args["repo"][0], number)
                status = 200 if result.get("decision") == "RECONCILED" else 409
                return self.respond_json(status, result)
            except (ValueError, OSError, urllib.error.URLError, json.JSONDecodeError):
                return self.respond_json(400, {"decision": "STOP",
                                               "reason": "invalid-input-or-remote-retrieval"})
        if url.path.startswith("/api/"):
            return self.respond_json(404, {"decision": "STOP", "reason": "unknown-api-route",
                                           "available_routes": ["/api/commands", "/api/inspect"]})
        return self.respond(
            404, "text/html; charset=utf-8",
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<title>ADE — Page not found</title></head><body>'
            '<main><h1>ADE page not found</h1>'
            '<p>This address is not a Control Center page. '
            'Open <a href="/">ADE Control Center home</a>.</p></main></body></html>')

    def do_POST(self):
        route = urlsplit(self.path)
        if route.path not in ("/api/app-builder/plan", "/api/app-builder/create") or route.query:
            return self.respond_json(405, {"decision": "STOP", "reason": "unsupported-write-route"})
        # Browser-initiated local writes require same-origin and loopback Host;
        # another website cannot submit a cross-site create request.
        host = self.headers.get("Host", "")
        origin = self.headers.get("Origin", "")
        if (not re.fullmatch(r"(?:localhost|127\.0\.0\.1):[0-9]{2,5}", host)
                or origin not in ("http://" + host,)):
            return self.respond_json(403, {"decision": "STOP", "reason": "origin-not-allowed"})
        if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
            return self.respond_json(415, {"decision": "STOP", "reason": "json-required"})
        try:
            size = int(self.headers.get("Content-Length", "-1"))
            if not 0 < size <= MAX_BODY:
                raise ValueError("Invalid size")
            request = json.loads(self.rfile.read(size))
            if route.path.endswith("/plan"):
                response = plan_request(request)
            else:
                if type(request) is not dict or set(request) != {"request", "plan_hash", "confirmed"}:
                    raise ValueError("Expected confirmed project plan")
                response = create_project(
                    request["request"], plan_hash=request["plan_hash"],
                    confirmed=request["confirmed"], workspace=WORKSPACE)
            status = 200 if response.get("decision") != "STOP" else 409
            return self.respond_json(status, response)
        except (ValueError, FileExistsError, OSError, TimeoutError):
            return self.respond_json(409, {"decision": "STOP", "reason": "invalid-or-conflicting-project-plan"})
        except (json.JSONDecodeError, TypeError):
            return self.respond_json(400, {"decision": "STOP", "reason": "malformed-request"})
        except Exception:
            # No secrets or server-local filesystem traces on the wire.
            return self.respond_json(500, {"decision": "STOP", "reason": "builder-internal-error"})

    def log_message(self, fmt, *args):
        # Avoid writing repository query details, token or request parameters.
        pass


def main(argv=None):
    parser = argparse.ArgumentParser(description="ADE read-only local control center")
    parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args(argv)
    if not 1024 <= args.port <= 65535:
        parser.error("Port must be between 1024 and 65535")
    with ThreadingHTTPServer(("127.0.0.1", args.port), Handler) as server:
        print("ADE Control Center: http://127.0.0.1:" + str(args.port), flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
