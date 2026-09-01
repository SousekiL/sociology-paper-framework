#!/usr/bin/env python3
"""Run the private, machine-local weekly literature refresh without Git operations."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> None:
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def main() -> int:
    run("scripts/update_literature_library.py", "--mode", "weekly")
    run("scripts/build_fulltext_review_queue.py", "--max", "1")
    if os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY"):
        run("scripts/review_openaccess_fulltexts.py")
    else:
        print("No local LLM_API_KEY: refreshed metadata and queue only.")
    run("scripts/validate_literature_library.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
