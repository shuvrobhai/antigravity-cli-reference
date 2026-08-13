#!/usr/bin/env python3
"""Dump the live agy CLI's tool list as sorted JSON."""

import json
import sys

from probe import live_tools


def main():
    try:
        tools = live_tools()
    except Exception as e:
        print(f"Error executing agy: {e}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(sorted(tools), indent=2))


if __name__ == "__main__":
    main()
