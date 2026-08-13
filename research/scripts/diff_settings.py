#!/usr/bin/env python3
"""Diff a real settings.json against the documented config_keys list.

Loads the documented keys from the knowledge JSON (flat + dotted),
flattens a target settings file using the same dotted convention, and
reports every observed key that is not covered by the documented set.
A key is covered if it is documented directly OR any ancestor path is
documented as an object-type key (e.g. `statusLine` covers
`statusLine.command`).

Usage:
    python3 research/scripts/diff_settings.py [SETTINGS_PATH]
    python3 research/scripts/diff_settings.py --settings PATH --json PATH [--check]

Defaults: target = the live user settings
(~/.gemini/antigravity-cli/settings.json), documented keys from the
repo knowledge file.

Exit codes:
    0  every observed key is documented (or --check not given)
    1  undocumented keys found and --check was given
"""

import argparse
import json
import sys
from pathlib import Path

from knowledge import Knowledge
from paths import knowledge_json

JSON_DEFAULT = knowledge_json()
SETTINGS_DEFAULT = Path.home() / ".gemini" / "antigravity-cli" / "settings.json"


def flatten(obj: dict, prefix: str = "") -> dict:
    """Flatten nested dicts with the dotted convention; arrays stay leaves."""
    out: dict = {}
    for k, v in obj.items():
        path = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(flatten(v, path))
        else:
            out[path] = v
    return out


def load_documented_keys(json_path: Path) -> set[str]:
    return Knowledge(json_path).config_keys()


def is_covered(path: str, documented: set[str]) -> bool:
    if path in documented:
        return True
    parts = path.split(".")
    return any(".".join(parts[:i]) in documented for i in range(1, len(parts)))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("settings", nargs="?", default=str(SETTINGS_DEFAULT))
    ap.add_argument("--json", default=str(JSON_DEFAULT), help="knowledge JSON path")
    ap.add_argument(
        "--check",
        action="store_true",
        help="exit 1 when undocumented keys are found (CI gate)",
    )
    args = ap.parse_args()

    settings_path = Path(args.settings)
    if not settings_path.exists():
        print(f"FAIL  settings file not found: {settings_path}")
        return 1

    try:
        raw = json.loads(settings_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAIL  settings file is not valid JSON: {e}")
        return 1

    documented = load_documented_keys(Path(args.json))
    observed = flatten(raw)
    undocumented = {
        path: value
        for path, value in sorted(observed.items())
        if not is_covered(path, documented)
    }

    print(f"settings: {settings_path}")
    print(f"documented keys: {len(documented)} | observed keys: {len(observed)}")
    if undocumented:
        print(f"\n{len(undocumented)} undocumented key(s):")
        for path, value in undocumented.items():
            preview = json.dumps(value) if not isinstance(value, str) else value
            if len(preview) > 90:
                preview = preview[:87] + "..."
            print(f"  {path} = {preview}")
        if args.check:
            print("\nFAIL  undocumented keys present (see above)")
            return 1
    else:
        print("\nok    every observed key is documented")

    return 0


if __name__ == "__main__":
    sys.exit(main())
