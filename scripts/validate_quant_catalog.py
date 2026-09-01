#!/usr/bin/env python3
"""Validate catalogue completeness and the invariants relied on by the skill."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / "data" / "quantitative-reference-catalog.json"
REQUIRED = {"id", "group", "label", "facet", "text", "topics"}
MINIMUMS = {"method": 100, "measurement": 100, "dataset": 15, "quality_check": 15}


def main() -> int:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    cards = data.get("cards", [])
    if data.get("card_count") != len(cards):
        raise ValueError("card_count does not equal actual card count")
    if len(cards) < 250:
        raise ValueError("catalogue has fewer than 250 cards")
    ids = [row.get("id") for row in cards]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate card IDs")
    groups = Counter()
    for index, row in enumerate(cards, 1):
        absent = REQUIRED - set(row)
        if absent:
            raise ValueError(f"card {index} missing {sorted(absent)}")
        if not isinstance(row["topics"], list) or not row["text"].strip():
            raise ValueError(f"card {index} has invalid topics or empty text")
        groups[row["group"]] += 1
    for group, minimum in MINIMUMS.items():
        if groups[group] < minimum:
            raise ValueError(f"{group}: {groups[group]} < {minimum}")
    print(json.dumps({"cards": len(cards), "groups": groups}, ensure_ascii=False, default=dict))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        raise SystemExit(1)
