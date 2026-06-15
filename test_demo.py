"""
Minimal demo file for testing code_navigation_Python.py.
Resolving "get_bug_info()" inside main() should find the definition below.
"""
import json


def get_bug_info():
    """Return bug information as a dict."""
    return {"bug": "info", "version": "1.0"}


def main():
    """Pretty-print the bug information as JSON."""
    print(json.dumps(get_bug_info(), sort_keys=True, indent=2))
