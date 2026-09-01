#!/usr/bin/env python3
"""Check append-only library records for basic integrity without network access."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "library" / "article-metadata.jsonl"


def key(row: dict) -> str:
    return row.get("doi") or f"{row.get('source_id')}|{row.get('published')}|{row.get('title')}"


def main() -> int:
    seen, journals = set(), Counter()
    for line_number, line in enumerate(RECORDS.read_text(encoding="utf-8").splitlines(), 1):
        row = json.loads(line)
        required = {"source_id", "journal", "title", "published", "url", "source"}
        missing = required - set(row)
        if missing:
            raise ValueError(f"line {line_number}: missing {sorted(missing)}")
        if "full_text" in row or "pdf" in row:
            raise ValueError(f"line {line_number}: record must not contain full-text fields")
        identifier = key(row)
        if identifier in seen:
            raise ValueError(f"line {line_number}: duplicate record {identifier}")
        seen.add(identifier)
        journals[row["journal"]] += 1
    if not seen:
        raise ValueError("library is empty")
    print(json.dumps({"records": len(seen), "journals": dict(journals)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        raise SystemExit(1)
