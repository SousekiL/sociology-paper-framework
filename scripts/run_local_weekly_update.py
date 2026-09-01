#!/usr/bin/env python3
"""Run the private, machine-local weekly literature refresh without Git operations."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEYCHAIN_SERVICES = {
    "LLM_API_KEY": "sociology-paper-framework-llm-api-key",
    "LLM_BASE_URL": "sociology-paper-framework-llm-base-url",
    "LLM_MODEL": "sociology-paper-framework-llm-model",
}


def run(*args: str) -> None:
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def load_local_configuration() -> None:
    """Use explicit environment values first, then the current macOS user's Keychain."""
    if sys.platform != "darwin":
        return
    for variable, service in KEYCHAIN_SERVICES.items():
        if os.environ.get(variable) or (variable == "LLM_API_KEY" and os.environ.get("OPENAI_API_KEY")):
            continue
        result = subprocess.run(
            ["/usr/bin/security", "find-generic-password", "-s", service, "-w"],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            os.environ[variable] = result.stdout.strip()


def main() -> int:
    load_local_configuration()
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
