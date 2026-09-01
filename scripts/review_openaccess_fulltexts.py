#!/usr/bin/env python3
"""Read queued OA PDFs and append model-generated research-design notes (no full text stored)."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "library"
QUEUE = LIBRARY / "fulltext-review-queue.json"
NOTES = LIBRARY / "fulltext-reading-notes.jsonl"
MAX_BYTES = 20 * 1024 * 1024
CHUNK_CHARS = 45_000

CHUNK_PROMPT = """You are reading one consecutive chunk of a lawful open-access research article. Return strict JSON only.
Extract concise, Chinese, non-quoted evidence relevant to: research puzzle, theory/mechanism, data/sample,
variables/measurement, identification/model, diagnostics/robustness, transferable design lesson, and limits.
Use null for unavailable details. Do not infer from the title or abstract; report only this chunk's content.
ARTICLE CHUNK:\n"""

SYNTHESIS_PROMPT = """The following JSON evidence cards were made by reading every consecutive chunk of one lawful
open-access research article. Synthesize them into strict JSON only, with Chinese fields: research_puzzle,
theoretical_mechanism, data_and_sample, variables_and_measurement, identification_and_model,
diagnostics_and_robustness, transferable_design_lesson, limits. Be concrete, do not quote at length, and use null
where the full article does not support a field. Do not invent details. EVIDENCE CARDS:\n"""


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "sociology-paper-framework full-text reviewer"})
    with urllib.request.urlopen(request, timeout=90) as response:
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("PDF exceeds review size limit")
    return data


def extract_pdf(data: bytes) -> str:
    with tempfile.TemporaryDirectory() as directory:
        pdf = Path(directory) / "article.pdf"
        text = Path(directory) / "article.txt"
        pdf.write_bytes(data)
        subprocess.run(["pdftotext", "-layout", str(pdf), str(text)], check=True, timeout=90, capture_output=True)
        return text.read_text(encoding="utf-8", errors="replace")


def ask_model(api_key: str, prompt: str, content: str) -> dict:
    request_body = json.dumps({"model": os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"), "temperature": 0, "response_format": {"type": "json_object"}, "messages": [{"role": "user", "content": prompt + content}]}).encode()
    request = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=request_body, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=180) as response:
        payload = json.load(response)
    return json.loads(payload["choices"][0]["message"]["content"])


def chunks(text: str) -> list[str]:
    """Split at paragraph boundaries so every extracted character is reviewed."""
    pieces, start = [], 0
    while start < len(text):
        end = min(start + CHUNK_CHARS, len(text))
        if end < len(text):
            boundary = text.rfind("\n\n", start, end)
            if boundary > start:
                end = boundary + 2
        pieces.append(text[start:end])
        start = end
    return pieces


def review_full_article(api_key: str, article_text: str) -> dict:
    evidence = [ask_model(api_key, CHUNK_PROMPT, chunk) for chunk in chunks(article_text)]
    return ask_model(api_key, SYNTHESIS_PROMPT, json.dumps(evidence, ensure_ascii=False))


def main() -> int:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise SystemExit("OPENAI_API_KEY is required for automated full-text learning; no review was attempted.")
    queued = json.loads(QUEUE.read_text(encoding="utf-8")).get("papers", [])
    reviewed = {json.loads(line).get("doi") for line in NOTES.read_text(encoding="utf-8").splitlines() if line.strip()} if NOTES.exists() else set()
    written = 0
    with NOTES.open("a", encoding="utf-8") as handle:
        for paper in queued:
            if paper["doi"] in reviewed:
                continue
            article_text = extract_pdf(download(paper["full_text_url"]))
            if len(article_text.strip()) < 5_000:
                raise ValueError(f"Extracted text is too short for full-text review: {paper['doi']}")
            note = review_full_article(key, article_text)
            note.update({"doi": paper["doi"], "title": paper["title"], "journal": paper["journal"], "full_text_url": paper["full_text_url"], "license": paper.get("license"), "reviewed_at": datetime.now(timezone.utc).isoformat(), "review_type": "open-access full-text model reading"})
            handle.write(json.dumps(note, ensure_ascii=False, sort_keys=True) + "\n")
            written += 1
    print(json.dumps({"reviewed": written}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
