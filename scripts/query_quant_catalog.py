#!/usr/bin/env python3
"""Retrieve quantitative-research cards relevant to a sociology topic."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / "data" / "quantitative-reference-catalog.json"
SYNONYMS = {
    "劳动": ["就业", "工作", "平台", "灵活就业", "社保", "职业"],
    "平台": ["数字", "算法", "互联网", "灵活就业"],
    "不平等": ["阶层", "收入", "财富", "教育", "流动", "住房"],
    "教育": ["学校", "儿童", "青年", "学历"],
    "家庭": ["婚姻", "生育", "照护", "代际"],
    "社会关系": ["社会资本", "网络", "信任", "参与"],
    "人际关系": ["社会资本", "网络", "信任", "参与"],
    "健康": ["心理健康", "医疗", "老年", "照护"],
    "迁移": ["流动人口", "户籍", "城市"],
    "治理": ["政府", "政策", "公共服务", "社区"],
    "性别": ["女性", "婚姻", "生育", "照护"],
}
METHOD_BY_AIM = {
    "描述": ["描述统计与加权比较", "调查设计分析", "重复横截面趋势"],
    "关联": ["多元线性回归（OLS）", "二元 Logit/Probit", "有序 Logit/Probit", "多层模型", "面板固定效应"],
    "因果": ["双重差分（2×2）", "分期实施 DiD", "事件研究", "断点回归（RDD）", "工具变量（IV/2SLS）", "倾向得分加权/匹配", "合成控制"],
    "机制": ["因果中介分析", "结构方程模型（SEM）", "多层模型", "面板固定效应"],
}


def expand(topic: str) -> set[str]:
    terms = set(re.findall(r"[\u4e00-\u9fff]{2,}|[a-z][a-z-]{2,}", topic.lower()))
    for term, extras in SYNONYMS.items():
        if term in topic:
            terms.add(term)
            terms.update(extras)
    return terms


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--aim", choices=["auto", "描述", "关联", "因果", "机制"], default="auto")
    parser.add_argument("--limit", type=int, default=40)
    args = parser.parse_args()
    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    terms = expand(args.topic)
    aim = args.aim
    if aim == "auto":
        if any(x in args.topic.lower() for x in ("因果", "影响", "效应", "政策", "改革", "冲击")):
            aim = "因果"
        elif any(x in args.topic.lower() for x in ("机制", "中介", "路径")):
            aim = "机制"
        elif any(x in args.topic.lower() for x in ("趋势", "现状", "分布", "描述")):
            aim = "描述"
        else:
            aim = "关联"
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
        "note": "卡片用于设计与审查，不构成研究结论。因果方法仅在其假设可被实质辩护与诊断支持时采用。",
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
