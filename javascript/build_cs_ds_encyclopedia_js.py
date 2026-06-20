#!/usr/bin/env python3
"""
Build script for the JavaScript CS & DS Encyclopedia.

This script exists for consistency with the Python, Java, and C++ reference
directories. The JavaScript encyclopedia is maintained as a single file
(JAVASCRIPT_CS_DS_ENCYCLOPEDIA.js) rather than assembled from chunks,
since JavaScript doesn't require compilation.

Usage:
    python build_cs_ds_encyclopedia_js.py

    This simply validates that the encyclopedia file exists and runs it
    with Node.js to verify correctness.
"""
import subprocess
import sys
import os

ENCYCLOPEDIA_FILE = os.path.join(os.path.dirname(__file__),
                                  "JAVASCRIPT_CS_DS_ENCYCLOPEDIA.js")


def main():
    print("=" * 70)
    print("  JAVASCRIPT CS & DS ENCYCLOPEDIA — BUILD & VERIFY")
    print("=" * 70)

    # Check file exists
    if not os.path.exists(ENCYCLOPEDIA_FILE):
        print(f"ERROR: {ENCYCLOPEDIA_FILE} not found!")
        sys.exit(1)

    # Get file stats
    size = os.path.getsize(ENCYCLOPEDIA_FILE)
    with open(ENCYCLOPEDIA_FILE, "r", encoding="utf-8") as f:
        lines = sum(1 for _ in f)

    print(f"  File: {os.path.basename(ENCYCLOPEDIA_FILE)}")
    print(f"  Size: {size:,} bytes")
    print(f"  Lines: {lines:,}")
    print()

    # Run with Node.js
    print("  Running with Node.js...")
    print("-" * 70)
    try:
        result = subprocess.run(
            ["node", ENCYCLOPEDIA_FILE],
            capture_output=True,
            text=True,
            timeout=60,
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        if result.returncode != 0:
            print(f"\nERROR: Node.js exited with code {result.returncode}")
            sys.exit(1)
        else:
            print("\n✅ Encyclopedia ran successfully!")
    except FileNotFoundError:
        print("ERROR: Node.js not found. Install Node.js (v18+) to run.")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("ERROR: Execution timed out (60s limit)")
        sys.exit(1)


if __name__ == "__main__":
    main()
