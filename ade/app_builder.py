"""Minimal local idea -> plan -> approved template -> verified project workflow.

M8 is intentionally NOT an AI code generator. The sole supported template is a
low-risk, single-user offline list. All project writes are local, confined to
the configured workspace, and require explicit confirmation.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from .bootstrap import bootstrap, plan_bootstrap

SLUG = re.compile(r"[a-z][a-z0-9-]{2,49}\Z")
BLOCKED = re.compile(
    r"\b(payment|payments|checkout|bank|medical|patient|hospital|"
    r"vrs|interpreter|telephony|emergency|login|oauth|oidc|"
    r"identity|multi.?tenant|real.?time|booking|reservation|"
    r"public|production|credit.?card|password|health)\b", re.I)
EXPECTED = frozenset({"slug", "title", "idea", "template"})
TEMPLATE = "offline-list"


def plan_request(request):
    if type(request) is not dict or set(request) != EXPECTED:
        raise ValueError("A complete, explicit app request is required")
    if request["template"] != TEMPLATE:
        raise ValueError("Only the generic offline-list template is available")
    slug, title, idea = (request[k] for k in ("slug", "title", "idea"))
    if type(slug) is not str or not SLUG.fullmatch(slug):
        raise ValueError("Invalid project slug")
    if (type(title) is not str or not title.strip() or len(title) > 100
            or any(ord(ch) < 32 for ch in title)):
        raise ValueError("Invalid project title")
    if (type(idea) is not str or not 15 <= len(idea.strip()) <= 1000
            or any(ord(ch) < 32 for ch in idea)):
        raise ValueError("Describe a local single-user list (15–1000 characters)")
    # This flag only rules OUT recognizable high-risk cases. It does not
    # claim semantic classification, validate approval, or prove safety.
    if BLOCKED.search(title + " " + idea):
        raise ValueError("This scope needs product review; the local list template cannot implement it")
    brief = {
        "schema_version": "1.0",
        "slug": slug,
        "title": title.strip(),
        "problem": idea.strip(),
        "users": ["Local user"],
        "outcome": "Add, view and persist local list items across restarts",
        "domain": "offline-tasks",
    }
    files = plan_bootstrap(brief, working_profile="web-list")
    digest = hashlib.sha256(json.dumps(brief, sort_keys=True,
                                      separators=(",", ":")).encode()).hexdigest()
    return {
        "decision": "PLAN",
        "template": TEMPLATE,
        "brief": brief,
        "plan_hash": digest,
        "files": len(files),
        "sample_paths": ["app/server.py", "app/index.html",
                         "delivery/current-state.yaml", "tests/test_app.py"],
        "implemented_behavior": "Local single-user list with UI, API and SQLite persistence",
        "not_implemented": ["requested domain-specific features", "AI-written code",
                            "external APIs", "identity", "payments", "deployment"],
        "human_approval_for_production": True,
        "status": "proposal-only",
    }


def create_project(request, *, plan_hash, confirmed, workspace):
    plan = plan_request(request)
    if confirmed is not True or type(plan_hash) is not str or plan_hash != plan["plan_hash"]:
        raise ValueError("Explicit confirmation of the current plan is required")
    root = Path(workspace).expanduser().resolve()
    if root.exists() and (not root.is_dir() or root.is_symlink()):
        raise ValueError("Invalid workspace")
    root.mkdir(parents=True, exist_ok=True)
    dest = root / plan["brief"]["slug"]
    if dest.exists() or dest.is_symlink():
        raise FileExistsError("Project already exists and will never be overwritten")
    generated = bootstrap(plan["brief"], dest, working_profile="web-list")
    tested = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests",
         "-p", "test_app.py", "-v"], cwd=dest, capture_output=True,
        text=True, timeout=60, check=False)
    if tested.returncode != 0:
        # Preserve failure evidence and project for diagnosis, not false success.
        return {"decision": "STOP", "reason": "generated-app-tests-failed",
                "project_path": str(dest), "tests_passed": False,
                "approval_granted": False}
    return {
        "decision": "CREATED_LOCAL_DEMO",
        "project_path": str(dest),
        "generated_file_count": len(generated),
        "tests_passed": True,
        "start_command": "cd " + str(dest) + " ; python -m app.server",
        "preview_url": "http://127.0.0.1:8000/",
        "approval_granted": False,
        "remote_ci_verified": False,
        "scope": "generic single-user list; not implementation of arbitrary idea",
    }
