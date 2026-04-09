"""CLI entry point for env-guard."""

import sys
import argparse
from pathlib import Path

from env_guard.scanner import scan
from env_guard import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="env-guard",
        description="Scan directories for .env files not covered by .gitignore.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root directory to scan (default: current directory)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if any exposed .env files are found",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"env-guard {__version__}",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"[ERROR] Path does not exist: {root}", file=sys.stderr)
        sys.exit(2)

    print(f"\n🔍 Scanning: {root}\n")
    safe, exposed = scan(str(root))

    if not safe and not exposed:
        print("  No .env files found.")
        return

    if safe:
        print(f"✅ Protected ({len(safe)}):")
        for f in safe:
            print(f"   {f}")

    if exposed:
        print(f"\n⚠️  EXPOSED ({len(exposed)}) — not in any .gitignore:")
        for f in exposed:
            print(f"   {f}")
        print("\n  Add these to your .gitignore to prevent accidental commits.\n")
        if args.strict:
            sys.exit(1)
    else:
        print("\n  All .env files are covered. You're good to go. 🎉\n")


if __name__ == "__main__":
    main()
