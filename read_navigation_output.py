#!/usr/bin/env python3
"""
Read JSON output from code_navigation_Python.py and print a short summary.
Usage:
  python code_navigation_Python.py ... | python read_navigation_output.py
  # or
  python read_navigation_output.py < output.json
"""
import json
import sys


def main():
    data = json.load(sys.stdin)

    ok = data.get("ok", False)
    error = data.get("error")

    print("Result:", "OK" if ok else "FAILED")
    if error:
        print("Error:", error)
        return

    # Where was the snippet found?
    chosen = data.get("matches", {}).get("chosen")
    if chosen:
        ref = chosen.get("ref", {})
        print("\nUsage found:")
        print(f"  File:   {ref.get('path', '?')}")
        print(f"  Line:   {ref.get('line1', '?')}, column {ref.get('col1', '?')}")
        print(f"  Line:   {chosen.get('line_text', '').strip()}")

    # Where does it resolve to?
    defs = data.get("definitions") or []
    if not defs:
        print("\nNo definitions in output.")
        return

    outer = defs[0]
    outer_ok = outer.get("outer_ok", False)
    outer_err = outer.get("outer_error")
    outer_def = outer.get("outer_definition")

    if outer_err:
        print("\nResolution error:", outer_err)
        return

    if not outer_def:
        print("\nNo definition details.")
        return

    path = outer_def.get("path", "?")
    rng = outer_def.get("range", {})
    start = rng.get("start", {})
    line1 = start.get("line0", 0) + 1
    col1 = start.get("col0", 0) + 1
    source = outer_def.get("full_def_source", "").strip()

    print("\nResolved definition:")
    print(f"  File:   {path}")
    print(f"  Line:   {line1}, column {col1}")
    if source:
        print("\n  Source:")
        for line in source.splitlines():
            print("    ", line)


if __name__ == "__main__":
    main()
