"""Bootstrap CLI: offline-only, deterministic, no remote repository creation."""
import argparse
import json
from pathlib import Path
from .bootstrap import bootstrap,plan_bootstrap

def main(argv=None):
    parser=argparse.ArgumentParser(description="Offline application bootstrap")
    parser.add_argument("action",choices=("plan","create"))
    parser.add_argument("brief",type=Path)
    parser.add_argument("destination",type=Path,nargs="?")
    parser.add_argument("--working-web-list",action="store_true",help="Include opt-in local runnable demo; low-risk briefs only")
    args=parser.parse_args(argv)
    brief=json.loads(args.brief.read_text(encoding="utf-8"))
    if args.action=="plan":
        print(json.dumps({"files":sorted(plan_bootstrap(brief,working_profile="web-list" if args.working_web_list else None)),"mutates":False},indent=2))
    else:
        if args.destination is None:
            parser.error("create requires a destination")
        print(json.dumps({"generated":list(bootstrap(brief,args.destination,working_profile="web-list" if args.working_web_list else None)),
                          "mutates_only":str(args.destination)},indent=2))

if __name__=="__main__":
    main()
