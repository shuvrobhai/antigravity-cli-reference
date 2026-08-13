#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from paths import raw_doc, reference_doc, research_dir, scripts_dir

DOC_PATH = reference_doc()
RAW_PATH = raw_doc()


def main():
    ap = argparse.ArgumentParser(
        description="Sync working copy (raw/) to published copy (docs/)"
    )
    ap.add_argument(
        "--source", default=str(RAW_PATH), help="Path to working copy (raw/)"
    )
    ap.add_argument(
        "--to", default=str(DOC_PATH), help="Path to published copy (docs/)"
    )
    ap.add_argument(
        "--force", action="store_true", help="Overwrite even if published copy is newer"
    )
    args = ap.parse_args()

    src = Path(args.source)
    dest = Path(args.to)

    if not src.exists():
        print(f"Error: Source file {src} does not exist", file=sys.stderr)
        sys.exit(1)

    # Scripts never write outside research/.
    if not dest.resolve().is_relative_to(research_dir().resolve()):
        print(
            f"Error: destination {dest} is outside research/; scripts only write inside research/",
            file=sys.stderr,
        )
        sys.exit(1)

    # Check if dest is newer
    if dest.exists() and not args.force:
        src_mtime = src.stat().st_mtime
        dest_mtime = dest.stat().st_mtime
        if dest_mtime > src_mtime:
            print(
                f"Error: Published copy ({dest}) is newer than working copy ({src}).",
                file=sys.stderr,
            )
            print("Use --force to override and overwrite.", file=sys.stderr)
            sys.exit(1)

    # Copy file
    try:
        shutil.copy2(src, dest)
        print(f"Synced: {src} -> {dest}")
    except Exception as e:
        print(f"Error copying file: {e}", file=sys.stderr)
        sys.exit(1)

    # Run check_consistency.py
    print("Running consistency check...")
    checker = scripts_dir() / "check_consistency.py"
    res = subprocess.run(
        [sys.executable, str(checker), "--doc", str(dest)],
        capture_output=True,
        text=True,
        check=False,
    )
    print(res.stdout)
    if res.stderr:
        print(res.stderr, file=sys.stderr)

    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
