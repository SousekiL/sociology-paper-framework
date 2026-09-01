#!/usr/bin/env python3
"""Retrieve quantitative-research cards relevant to a sociology topic."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / "data" / "quantitative-reference-catalog.json"
SYNONYMS = {
    "labor": ["employment", "work", "platform", "flexible employment", "social security", "occupation"],
    "platform": ["digital", "algorithm", "internet", "flexible employment"],
    "inequality": ["class", "income", "wealth", "education", "mobility", "housing"],
    "education": ["school", "children", "youth", "educational attainment"],
    "family": ["marriage", "fertility", "caregiving", "intergenerational"],
    "social relations": ["social capital", "network", "trust", "participation"],
    "interpersonal relations": ["social capital", "network", "trust", "participation"],
    "health": ["mental health", "healthcare", "older adults", "caregiving"],
    "migration": ["migrants", "household registration", "urban areas"],
    "governance": ["government", "policy", "public services", "community"],
    "gender": ["women", "marriage", "fertility", "caregiving"],
}
CHINESE_INPUT_TERMS = {
    "\u52b3\u52a8": ["labor", "employment", "work", "platform", "flexible employment", "social insurance", "occupation"],
    "\u5e73\u53f0": ["platform", "digital", "algorithm", "internet", "flexible employment"],
    "\u4e0d\u5e73\u7b49": ["inequality", "class", "income", "wealth", "education", "mobility", "housing"],
    "\u6559\u80b2": ["education", "school", "children", "youth", "educational attainment"],
    "\u5bb6\u5ead": ["family", "marriage", "fertility", "caregiving", "intergenerational"],
    "\u793e\u4f1a\u5173\u7cfb": ["social relations", "social capital", "network", "trust", "participation"],
    "\u4eba\u9645\u5173\u7cfb": ["interpersonal relations", "social capital", "network", "trust", "participation"],
    "\u5065\u5eb7": ["health", "mental health", "healthcare", "older adults", "caregiving"],
    "\u8fc1\u79fb": ["migration", "migrants", "household registration", "urban areas"],
    "\u6cbb\u7406": ["governance", "government", "policy", "public services", "community"],
    "\u6027\u522b": ["gender", "women", "marriage", "fertility", "caregiving"],
}
METHOD_BY_AIM = {
    "description": ["Descriptive statistics and weighted comparisons", "Survey design analysis", "Repeated cross-sectional trends"],
    "association": ["Multiple linear regression (OLS)", "Binary Logit/Probit", "Ordered Logit/Probit", "Multilevel models", "Panel fixed effects"],
    "causal": ["Difference-in-differences (2×2)", "Staggered-adoption DiD", "Event study", "Regression discontinuity (RDD)", "Instrumental variables (IV/2SLS)", "Propensity-score weighting/matching", "Synthetic control"],
    "mechanism": ["Causal mediation analysis", "Structural equation modeling (SEM)", "Multilevel model", "Panel fixed effects"],
}


def expand(topic: str) -> set[str]:
    terms = set(re.findall(r"[\u4e00-\u9fff]{2,}|[a-z][a-z-]{2,}", topic.lower()))
    for term, extras in SYNONYMS.items():
        if term in topic:
            terms.add(term)
            terms.update(extras)
    for term, extras in CHINESE_INPUT_TERMS.items():
        if term in topic:
            terms.update(extras)
    return terms


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--aim", choices=["auto", "description", "association", "causal", "mechanism"], default="auto")
    parser.add_argument("--limit", type=int, default=40)
    args = parser.parse_args()
    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    terms = expand(args.topic)
    aim = args.aim
    if aim == "auto":
        if any(x in args.topic.lower() for x in ("causal", "impact", "effect", "policy", "reform", "shock", "\u56e0\u679c", "\u5f71\u54cd", "\u6548\u5e94", "\u653f\u7b56", "\u6539\u9769", "\u51b2\u51fb")):
            aim = "causal"
        elif any(x in args.topic.lower() for x in ("mechanism", "mediation", "pathway", "\u673a\u5236", "\u4e2d\u4ecb", "\u8def\u5f84")):
            aim = "mechanism"
        elif any(x in args.topic.lower() for x in ("trend", "current status", "distribution", "description", "\u8d8b\u52bf", "\u73b0\u72b6", "\u5206\u5e03", "\u63cf\u8ff0")):
            aim = "description"
        else:
            aim = "association"
    relevant = []
    for row in payload["cards"]:
        topics = set(row.get("topics") or [])
        hits = terms.intersection(topics)
        if hits:
            relevant.append((len(hits), row))
    relevant.sort(key=lambda x: (x[0], x[1]["group"], x[1]["label"]), reverse=True)
    selected = [row for _, row in relevant[: args.limit]]
    labels = set(METHOD_BY_AIM[aim])
    method_cards = [row for row in payload["cards"] if row["group"] == "method" and row["label"] in labels]
    quality_cards = [row for row in payload["cards"] if row["group"] == "quality_check"]
    print(json.dumps({
        "topic": args.topic, "inferred_aim": aim, "query_terms": sorted(terms),
        "recommended_method_cards": method_cards,
        "relevant_measurement_and_dataset_cards": selected,
        "universal_quality_checks": quality_cards,
        "note": "Cards are for design and review and do not constitute research conclusions. Use causal methods only when their assumptions can be substantively justified and supported by diagnostics.",
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
