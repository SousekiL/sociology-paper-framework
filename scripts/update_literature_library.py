#!/usr/bin/env python3
"""Append public journal metadata to the research library without replacing history."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "library"
SOURCES_FILE = LIBRARY / "sources.json"
RECORDS_FILE = LIBRARY / "article-metadata.jsonl"
STATE_FILE = LIBRARY / "state.json"
MANUAL_QUEUE = LIBRARY / "manual-review-queue.md"
WINDOW_DAYS = 183
EMPTY_LIMIT = 4
USER_AGENT = "sociology-paper-framework-library/1.0 (metadata only; mailto:maintainer@example.invalid)"


def clean(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]*>", " ", value))).strip()


def published_date(item: dict) -> str | None:
    for key in ("published-online", "published-print", "published", "issued", "created"):
        bits = item.get(key, {}).get("date-parts", [[]])
        if bits and bits[0]:
            year, *rest = bits[0]
            month = rest[0] if len(rest) >= 1 else 1
            day = rest[1] if len(rest) >= 2 else 1
            return f"{year:04d}-{month:02d}-{day:02d}"
    return None


def authors(item: dict) -> list[str]:
    return [" ".join(x for x in (row.get("given"), row.get("family")) if x).strip() for row in item.get("author", []) if row.get("given") or row.get("family")]


def record_id(record: dict) -> str:
    return record.get("doi") or f"{record.get('source_id')}|{record.get('published')}|{record.get('title')}"


def existing_ids() -> set[str]:
    if not RECORDS_FILE.exists():
        return set()
    ids = set()
    for number, line in enumerate(RECORDS_FILE.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            ids.add(record_id(json.loads(line)))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL at {RECORDS_FILE}:{number}") from exc
    return ids


def fetch(source: dict, start: dt.date, end: dt.date) -> list[dict]:
    filt = f"from-pub-date:{start.isoformat()},until-pub-date:{end.isoformat()},type:journal-article"
    params = urllib.parse.urlencode({"filter": filt, "rows": 1000, "sort": "published", "order": "desc"})
    url = f"https://api.crossref.org/journals/{source['issn']}/works?{params}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=45) as response:
        payload = json.load(response)
    records = []
    for item in payload["message"]["items"]:
        title = clean(" ".join(item.get("title", [])))
        if not title:
            continue
        doi = item.get("DOI", "").lower() or None
        records.append({
            "source_id": source["id"], "journal": source["name"], "kind": source["kind"],
            "title": title, "authors": authors(item), "published": published_date(item),
            "doi": doi, "url": item.get("URL") or source["official_url"],
            "abstract": clean(item.get("abstract")) or None,
            "abstract_available": bool(clean(item.get("abstract"))), "record_type": item.get("type"),
            "retrieved_at": dt.datetime.now(dt.timezone.utc).isoformat(), "source": "Crossref public metadata",
        })
    return records


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"version": 1, "sources": {}, "runs": []}


def source_state(state: dict, source: dict, current_start: dt.date) -> dict:
    item = state["sources"].setdefault(source["id"], {})
    item.setdefault("next_backfill_end", (current_start - dt.timedelta(days=1)).isoformat())
    item.setdefault("empty_backfill_batches", 0)
    item.setdefault("backfill_complete", False)
    return item


def append(records: list[dict], seen: set[str]) -> int:
    added = [row for row in records if record_id(row) not in seen]
    if not added:
        return 0
    with RECORDS_FILE.open("a", encoding="utf-8") as handle:
        for row in added:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            seen.add(record_id(row))
    return len(added)


def write_manual_queue(sources: list[dict]) -> None:
    manual = [row for row in sources if not row.get("issn")]
    lines = ["# 中文期刊人工核验队列", "", "这些来源不稳定地提供开放结构化元数据，因此不会被脚本伪装成已自动抓取。每周可依据官网目录手动追加题名、作者、期次、公开摘要（如有）和官网链接到 `article-metadata.jsonl`。", ""]
    for row in manual:
        lines.append(f"- **{row['name']}**：{row['official_url']}")
    MANUAL_QUEUE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_window(source: dict, start: dt.date, end: dt.date, seen: set[str]) -> tuple[int, int]:
    records = fetch(source, start, end)
    return len(records), append(records, seen)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["current", "weekly", "history"], default="weekly")
    parser.add_argument("--batches", type=int, default=1, help="historical six-month windows per source in history mode")
    args = parser.parse_args()
    if args.batches < 1:
        parser.error("--batches must be positive")

    today = dt.date.today()
    current_start = today - dt.timedelta(days=WINDOW_DAYS)
    sources = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
    automated = [row for row in sources if row.get("issn")]
    seen, state = existing_ids(), load_state()
    summary = {"at": dt.datetime.now(dt.timezone.utc).isoformat(), "mode": args.mode, "current_window": [current_start.isoformat(), today.isoformat()], "sources": {}, "added": 0, "failures": []}

    for source in automated:
        status = source_state(state, source, current_start)
        source_summary = summary["sources"].setdefault(source["id"], {"current_added": 0, "history_added": 0})
        if args.mode in ("current", "weekly"):
            try:
                _, added = run_window(source, current_start, today, seen)
                source_summary["current_added"] = added
                summary["added"] += added
                status["last_current_scan"] = today.isoformat()
            except Exception as exc:
                summary["failures"].append({"source": source["id"], "stage": "current", "error": str(exc)})
        if args.mode in ("weekly", "history") and not status["backfill_complete"]:
            for _ in range(args.batches):
                end = dt.date.fromisoformat(status["next_backfill_end"])
                start = end - dt.timedelta(days=WINDOW_DAYS - 1)
                try:
                    found, added = run_window(source, start, end, seen)
                    source_summary["history_added"] += added
                    summary["added"] += added
                    status["next_backfill_end"] = (start - dt.timedelta(days=1)).isoformat()
                    status["empty_backfill_batches"] = status["empty_backfill_batches"] + 1 if found == 0 else 0
                    if status["empty_backfill_batches"] >= EMPTY_LIMIT:
                        status["backfill_complete"] = True
                        status["backfill_completion_reason"] = f"{EMPTY_LIMIT} consecutive empty Crossref windows"
                        break
                except Exception as exc:
                    summary["failures"].append({"source": source["id"], "stage": "history", "error": str(exc)})
                    break
        time.sleep(0.15)

    write_manual_queue(sources)
    state["runs"].append(summary)
    state["runs"] = state["runs"][-100:]
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
