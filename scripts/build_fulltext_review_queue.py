#!/usr/bin/env python3
"""Select a small weekly queue of lawful open-access full texts for structured review."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "library"
RECORDS = LIBRARY / "article-metadata.jsonl"
NOTES = LIBRARY / "fulltext-reading-notes.jsonl"
QUEUE = LIBRARY / "fulltext-review-queue.json"
USER_AGENT = "sociology-paper-framework-library/1.0 (open-access review queue)"


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def openalex(doi: str) -> dict | None:
    url = "https://api.openalex.org/works/" + urllib.parse.quote("https://doi.org/" + doi, safe="")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except Exception:
        return None


def oa_location(work: dict) -> tuple[str | None, str | None, str | None]:
    if not work.get("open_access", {}).get("is_oa"):
        return None, None, None
    for location in [work.get("best_oa_location"), *(work.get("locations") or [])]:
        if not location:
            continue
        pdf = location.get("pdf_url")
        landing = location.get("landing_page_url")
        if pdf or landing:
            return pdf, landing, location.get("license")
    return None, None, None


def actual_pdf(url: str) -> bool:
    """Reject landing pages and access-gated URLs mislabeled as PDFs by an index."""
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return "application/pdf" in response.headers.get("Content-Type", "").lower()
    except Exception:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max", type=int, default=3, help="maximum papers to queue")
    parser.add_argument("--scan-limit", type=int, default=75, help="newest unreviewed DOI records to inspect")
    args = parser.parse_args()
    reviewed = {row.get("doi") for row in load_jsonl(NOTES) if row.get("doi")}
    candidates = [row for row in load_jsonl(RECORDS) if row.get("doi") and row.get("doi") not in reviewed]
    candidates.sort(key=lambda row: row.get("published") or "", reverse=True)
    papers = []
    for row in candidates[: args.scan_limit]:
        work = openalex(row["doi"])
        if not work:
            continue
        pdf, landing, license_name = oa_location(work)
        if not pdf or not license_name or not actual_pdf(pdf):  # Require an explicit OA license and retrievable PDF.
            continue
        papers.append({
            "doi": row["doi"], "title": row["title"], "journal": row["journal"], "published": row.get("published"),
            "metadata_url": row["url"], "full_text_url": pdf, "landing_page_url": landing,
            "license": license_name, "selected_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "status": "queued_open_access_full_text",
        })
        if len(papers) >= args.max:
            break
        time.sleep(0.1)
    QUEUE.write_text(json.dumps({"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(), "selection_rule": "unreviewed records with an explicit OpenAlex OA license and a retrievable PDF; no full text is committed", "papers": papers}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"queued": len(papers), "papers": papers}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
