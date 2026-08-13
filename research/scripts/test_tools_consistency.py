#!/usr/bin/env python3
import sys

from knowledge import Knowledge
from probe import live_tools


def main():
    # Load documented tools
    try:
        documented_tools = Knowledge().tools()
    except Exception as e:
        print(f"Error loading knowledge JSON: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(documented_tools)} documented tools.")

    # Probe live CLI
    try:
        live = live_tools()
    except Exception as e:
        print(f"Error probing agy CLI: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(live)} live tools from probe.")

    # Check that documented tools match live tools
    extra_documented = documented_tools - live
    extra_live = live - documented_tools

    success = True
    if extra_documented:
        print(
            f"FAIL: Documented tools not found in live CLI: {extra_documented}",
            file=sys.stderr,
        )
        success = False
    if extra_live:
        print(f"FAIL: Live tools not documented in JSON: {extra_live}", file=sys.stderr)
        success = False

    if success:
        print("PASS: Documented tools match live CLI tools exactly.")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
