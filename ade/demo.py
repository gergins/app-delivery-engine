"""One-command local ADE demonstration; never merges, deploys or uses secrets.

Generate a low-risk runnable UI/API/SQLite application with its delivery handoff,
verify the generated API tests, and optionally serve it on localhost.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from .bootstrap import bootstrap

EXAMPLE = Path(__file__).resolve().parent.parent / "examples" / "offline-list-brief.json"


def run_demo(destination, *, serve=False, brief_path=EXAMPLE):
    destination = Path(destination).resolve()
    if destination.exists() or destination.is_symlink():
        raise FileExistsError("Target already exists; refusing to overwrite: " + str(destination))
    brief = json.loads(Path(brief_path).read_text(encoding="utf-8"))
    generated = bootstrap(brief, destination, working_profile="web-list")
    verified = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests",
         "-p", "test_app.py", "-v"], cwd=destination, capture_output=True,
        text=True, timeout=90, check=False)
    if verified.returncode:
        raise RuntimeError("Generated app smoke test failed (exit " +
                           str(verified.returncode) + "): " + verified.stderr[-2000:])
    result = {
        "result": "local-demo-verified",
        "generated_directory": str(destination),
        "generated_file_count": len(generated),
        "local_tests": "passed",
        "run_command": "python -m app.server",
        "url": "http://127.0.0.1:8000",
        "product_scope": "unapproved",
        "remote_ci_verified": False,
        "merge_or_deploy_approved": False,
    }
    print(json.dumps(result, indent=2), flush=True)
    if serve:
        print("Starting local demonstration. Stop with Ctrl+C.", flush=True)
        return subprocess.call([sys.executable, "-m", "app.server"], cwd=destination)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Execute and verify a local ADE starter application")
    parser.add_argument("destination", type=Path, help="New nonexistent directory for the demo")
    parser.add_argument("--serve", action="store_true", help="Run local HTTP server after tests")
    args = parser.parse_args(argv)
    try:
        return run_demo(args.destination, serve=args.serve)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        parser.exit(2, "STOP: " + str(exc) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
