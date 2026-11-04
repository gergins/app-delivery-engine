"""CLI for the offline generator."""
import argparse
import json
from pathlib import Path
from .generator import generate


def main():
    parser = argparse.ArgumentParser(description="Generate a minimal offline application")
    parser.add_argument("spec", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    generated = generate(spec, args.destination)
    print("Generated", len(generated), "files in", args.destination)


if __name__ == "__main__":
    main()
