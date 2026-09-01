#!/usr/bin/env python3
"""Check append-only library records for basic integrity without network access."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "library" / "article-metadata.jsonl"
FULLTEXT_NOTES = ROOT / "library" / "fulltext-reading-notes.jsonl"


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

    if FULLTEXT_NOTES.exists():
        required = {
            "doi", "title", "journal", "full_text_url", "license", "review_type",
            "research_puzzle", "theoretical_mechanism", "data_and_sample",
            "variables_and_measurement", "identification_and_model",
            "diagnostics_and_robustness", "transferable_design_lesson", "limits",
        }
        note_dois, note_count = set(), 0
        for line_number, line in enumerate(FULLTEXT_NOTES.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            note = json.loads(line)
            missing = required - set(note)
            if missing:
                raise ValueError(f"full-text note line {line_number}: missing {sorted(missing)}")
            if note["doi"] in note_dois:
                raise ValueError(f"duplicate full-text note DOI: {note['doi']}")
            if "full_text" in note or "article_text" in note or "pdf" in note:
                raise ValueError("full-text notes must not store article text or PDFs")
            note_dois.add(note["doi"])
            note_count += 1
        print(f"Validated {note_count} structured full-text reading notes.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        raise SystemExit(1)
