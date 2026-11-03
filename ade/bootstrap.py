"""Offline application bootstrap and deterministic continuity gate.

The bootstrap does not create GitHub repositories, contact providers, run agents,
grant approval or deploy. JSON emitted into *.yaml is valid YAML 1.2, avoiding
a new parser dependency. Product-specific implementation remains unbuilt.
"""
import json
import re
from pathlib import Path
from .generator import generate as safe_generate, SLUG
from .method_selection import select_method

VERSION="1.0"
DOMAINS={
    "general": (),
    "vrs": ("identity","personal-data","external-provider","concurrency","public-exposure"),
    "offline-tasks": (),
}
GATES=("merge","deploy","production-credentials","paid-infrastructure","independent-security-review")

def _json(data):
    return json.dumps(data,indent=2,sort_keys=True,ensure_ascii=False)+"\n"

def _line(value, label, max_length=500):
    if type(value) is not str or not value.strip() or len(value)>max_length or any(ord(c)<32 for c in value):
        raise ValueError("Invalid "+label)
    return value.strip()

def validate_brief(brief):
    allowed={"schema_version","slug","title","problem","users","outcome","domain","risks"}
    if type(brief) is not dict or set(brief)-allowed or set(brief)!=allowed-{"risks"} and set(brief)!=allowed:
        raise ValueError("Invalid brief fields")
    if brief["schema_version"]!=VERSION or type(brief["slug"]) is not str or not SLUG.fullmatch(brief["slug"]) or len(brief["slug"])>50:
        raise ValueError("Invalid brief version or slug")
    for field in ("title","problem","outcome"):
        _line(brief[field],field)
    if type(brief["users"]) is not list or not 1<=len(brief["users"])<=8:
        raise ValueError("Users required")
    for item in brief["users"]:
        _line(item,"user",100)
    domain=brief["domain"]
    if type(domain) is not str or domain not in DOMAINS:
        raise ValueError("Unknown application domain: requires review")
    risks=brief.get("risks",[])
    if type(risks) is not list:
        raise ValueError("Invalid risks")
    selected=sorted(set(risks)|set(DOMAINS[domain]))
    select_method("new-slice",selected)  # unknown risk never downgraded
    return selected

STARTUP_SCRIPT = '''"""Generated offline continuity verifier, no GitHub connectivity."""
import argparse
import json
from pathlib import Path

REQUIRED=(
 "AGENTS.md","project.yaml","docs/product/requirements.md",
 "docs/architecture/overview.md","docs/decisions/0001-initial-constraints.md",
 "docs/quality/acceptance.md","docs/security/risk-register.md",
 "delivery/current-state.yaml","delivery/decision-log.json",
 "delivery/approvals.json","delivery/evidence.json",
 "docs/operations/release-readiness.md",".github/workflows/verify.yml"
)

def inspect(root):
    root=Path(root)
    if any(not (root/path).is_file() for path in REQUIRED):
        return {"decision":"STOP","reason":"missing-required-files",
                "missing":[path for path in REQUIRED if not (root/path).is_file()]}
    try:
        project=json.loads((root/"project.yaml").read_text(encoding="utf-8"))
        state=json.loads((root/"delivery/current-state.yaml").read_text(encoding="utf-8"))
        approvals=json.loads((root/"delivery/approvals.json").read_text(encoding="utf-8"))
        evidence=json.loads((root/"delivery/evidence.json").read_text(encoding="utf-8"))
    except (ValueError,OSError):
        return {"decision":"STOP","reason":"invalid-structured-state"}
    if project.get("schema_version")!="1.0" or state.get("schema_version")!="1.0" or project.get("slug")!=state.get("project_slug"):
        return {"decision":"STOP","reason":"schema-or-project-drift"}
    if type(approvals) is not dict or approvals.get("merge") is not False or approvals.get("deploy") is not False or approvals.get("production_credentials") is not False:
        return {"decision":"STOP","reason":"unverified-authority-state"}
    if state.get("status") not in ("blocked","ready","in_progress","complete") or not state.get("milestone") or not state.get("next_action"):
        return {"decision":"STOP","reason":"missing-milestone-continuity"}
    if state.get("status")=="complete" and (not evidence.get("tested_sha") or evidence.get("ci_conclusion")!="success" or not evidence.get("workflow_url")):
        return {"decision":"STOP","reason":"unsupported-completion"}
    return {"decision":"STOP" if state["status"]=="blocked" else "CONTINUE",
            "reason":"approval-or-requirements-gate" if state["status"]=="blocked" else "local-preflight-only",
            "stage":state.get("stage"),"milestone":state["milestone"],
            "next_action":state["next_action"],
            "requires_remote_github_verification":True,
            "approval_required_for":["merge","deploy","paid-infrastructure","production-credentials","independent-signoff"]}

if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Read-only offline agent startup preflight")
    parser.add_argument("--root",default=".")
    args=parser.parse_args()
    result=inspect(args.root)
    print(json.dumps(result,sort_keys=True))
    raise SystemExit(2 if result["decision"]=="STOP" else 0)
'''

def plan_bootstrap(brief):
    risks=validate_brief(brief)
    selection=select_method("new-slice",risks)
    slug=brief["slug"]
    project={"schema_version":VERSION,"slug":slug,"title":brief["title"],
             "domain":brief["domain"],"users":brief["users"],"problem":brief["problem"],
             "outcome":brief["outcome"],"risks":risks,"runtime_status":"not-built",
             "hosting":"not-selected","source_of_truth":"GitHub"}
    state={"schema_version":VERSION,"project_slug":slug,"stage":"requirements",
           "milestone":"M0-brief-and-scope","status":"blocked",
           "next_action":"Obtain explicit acceptance of requirements, risks and minimum vertical slice.",
           "blocked_by":["unapproved-product-scope"],"tested_sha":None,
           "last_verified_ci":None}
    ag='''# Application engineering operating contract

Read this file BEFORE editing. This project was generated by the App Delivery Engine.
**Do not assume generated scaffold = built or production-ready application.**

Startup protocol for ChatGPT Work, Codex, AI agents and humans:
1. Run `python tools/startup.py` from the repo root. A STOP exit is deliberate: do not implement beyond documented gates.
2. Read `project.yaml`, `delivery/current-state.yaml`, requirements, ADR, risk register and acceptance criteria.
3. Inspect actual GitHub branch/PR and exact HEAD/CI. Offline startup cannot verify remote CI. Never infer green checks from JSON alone.
4. Choose task kind/risks and appropriate method using the Engine method-selection contract. Preserve accepted scope and smallest vertical slice.
5. Test expected behavior plus security failures, concurrency, accessibility and recovery where applicable; record exact commit and CI evidence.
6. Update existing PR and `delivery/current-state.yaml` as a handoff. Do not create duplicate PRs or silently rewrite decisions.

Stop and ask for named human approval to merge, deploy, spend, use real secrets, change review policies, grant external access or claim independent security signoff.
Escalate conflicting product requirements, missing qualifications and high-risk external integrations.
Never let an agent approve its own output. GitHub source/CI and accepted product decisions override memories of past chats.

Method and senior leadership guidance (Engine, current reviewed ref):
- docs/SENIOR-ENGINEERING-CONTRACT-V1.md
- docs/METHOD-SELECTION-V1.md
- docs/APP-LIFECYCLE-BENCHMARK-V1.md
- docs/BENCHMARK-TO-OWNERSHIP-POLICY.md
Resolve these in the App Delivery Engine's actual approved GitHub revision; references are guidance, not a copied framework.

'''
    def mditems(items):
        return "".join("- "+i+"\n" for i in items)
    requirements=("# Product requirements — unapproved draft\n\n**Problem:** "+brief["problem"]+
      "\n\n**Intended users**\n"+mditems(brief["users"])+
      "\n**Desired outcome:** "+brief["outcome"]+
      "\n\n## Required before implementation\n- [ ] Verify problem and users with owner\n"+
      "- [ ] Accept measurable outcomes and non-goals\n- [ ] Define one user-visible runnable vertical slice\n"+
      "- [ ] Define functional and nonfunctional acceptance tests\n- [ ] Review safety, privacy, accessibility, legal/regulatory exposure\n"+
      "- [ ] Assign decision and escalation owners\n")
    risks_md="# Initial risk register — not approved\n\n"+mditems(
      ["**"+r+"** — identify owner, negative tests, incident/recovery controls and independent review where required" for r in risks] or
      ["No elevated risk flags supplied; verify this classification before implementation."])+
      "\nRisks may only be narrowed after explicit review; a green unit test is not authorization.\n"
    docs={
      "AGENTS.md":ag,
      "project.yaml":_json(project),
      "docs/product/requirements.md":requirements,
      "docs/architecture/overview.md":"# Architecture — decision pending\n\nSelect build/reuse/defer alternatives, component boundaries, identity, data, runtime and failure modes. No stack automatically chosen.\n",
      "docs/decisions/0001-initial-constraints.md":"# ADR 0001: constraints and ownership\n\nStatus: proposed\n\nSeparate application repo; source of truth GitHub; minimal vertical slice; provider independence; no merge/deploy/real credentials without user approval.\n",
      "docs/quality/acceptance.md":"# Acceptance criteria — draft\n\n- [ ] User journey described with verifiable behavior\n- [ ] Negative and accessibility cases selected by risks\n- [ ] Tests and evidence recorded against exact PR HEAD\n- [ ] Human scope acceptance documented\n",
      "docs/security/risk-register.md":risks_md,
      "docs/operations/release-readiness.md":"# Release readiness: NOT READY\n\nMust verify requirements, identity and privacy, accessibility, security review, SBOM/licensing, data migration, operations owner, backup/restore, monitoring, rollback and explicit deployment approval as applicable.\n",
      "delivery/current-state.yaml":_json(state),
      "delivery/decision-log.json":_json({"schema_version":VERSION,"decisions":[]}),
      "delivery/approvals.json":_json({"merge":False,"deploy":False,"production_credentials":False,"external_review":False}),
      "delivery/evidence.json":_json({"tested_sha":None,"ci_conclusion":None,"workflow_url":None,"reviewer":None}),
      "delivery/method-selection.json":_json(selection),
      "tools/startup.py":STARTUP_SCRIPT,
      "tests/test_startup.py":'''import unittest
from pathlib import Path
from tools.startup import inspect

class StartupTests(unittest.TestCase):
    def test_new_repository_stops_at_requirements_gate(self):
        result=inspect(Path(__file__).resolve().parents[1])
        self.assertEqual(result["decision"],"STOP")
        self.assertEqual(result["reason"],"approval-or-requirements-gate")

if __name__=="__main__":
    unittest.main()
''',
      "tests/__init__.py":"",
      "tools/__init__.py":"",
      ".github/workflows/verify.yml":'''name: Bootstrap continuity preflight
on:
  push:
  pull_request:
permissions:
  contents: read
jobs:
  preflight:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          persist-credentials: false
      - uses: actions/setup-python@6d4fd22b20465ccc0f7354476588e8df7c9ca0e0
        with:
          python-version: '3.11'
      - name: Unit verify allowed documented BLOCKED state
        run: python -m unittest discover -s tests -v
      - name: Assert startup appropriately stops before scope approval
        run: |
          set +e
          python tools/startup.py
          status=$?
          test "$status" -eq 2
''',
      "README.md":("# "+brief["title"]+"\n\n"+brief["outcome"]+
        "\n\n**Status: requirements-only starter. No application implementation, cloud hosting, accounts or product tests are included.**\n"+
        "\nStart: `python tools/startup.py`; expected STOP until product scope is approved.\n"+
        "Read AGENTS.md, project.yaml, delivery/current-state.yaml and docs.\n"),
      ".gitignore":"__pycache__/\n*.pyc\n.env\n.env.*\n!.env.example\n.venv/\n",
    }
    if brief["domain"]=="vrs":
        docs["docs/product/vrs-invariants.md"]=("# VRS design safety gates — proposed\n\n"+
          "Deaf caller, interpreter, operator, and third-party participants require explicit authorization and accessible controls.\n"+
          "Separate session lifecycle, queue fairness/assignment, presence, media routing and telephony boundaries.\n"+
          "Require scoped consent/privacy, audit redaction, reconnect, emergency handling, abuse protection and regional telecom/legal review.\n"+
          "No simulated signaling or browser-only call proves public carrier/PSTN service. Do not implement actual emergency routing without qualified legal/telecom review.\n")
    return docs

def bootstrap(brief,destination):
    files=plan_bootstrap(brief)
    destination=Path(destination)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError("Never overwrite an existing repository")
    if not destination.parent.is_dir():
        raise ValueError("Destination parent missing")
    destination.mkdir()
    try:
        for name,contents in files.items():
            path=destination/name
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(contents,encoding="utf-8")
    except BaseException:
        import shutil
        shutil.rmtree(destination)
        raise
    return tuple(sorted(files))
