---
name: socpaper
description: Design, assess methods, frame theory, or map literature for a sociology topic through one keyword-routed skill.
---

# Socpaper

Use one command with a leading mode keyword. If the first word after `/socpaper` case-insensitively matches a keyword below, remove it from the topic before working. Otherwise retain all text as the topic and default to `paper`.

| Keyword | Task |
| --- | --- |
| `paper` | Full, journal-oriented quantitative paper framework |
| `method` | Methods, identification, and diagnostics only |
| `theory` | Theoretical background, mechanisms, and propositions only |
| `review` | Research streams, debates, and feasible gaps only |

Respond in Chinese unless asked otherwise. Use general social-science reasoning first. Local method cards and a private `library/` may refine an answer when present; never assume they exist, or invent a citation or full-text reading.

## paper

Run `scripts/query_quant_catalog.py --topic "<topic>"`, then read [references/quantitative-research-standard.md](references/quantitative-research-standard.md) and [references/quantitative-output-template.md](references/quantitative-output-template.md). Deliver a complete quantitative design: puzzle, research question, theory and rival explanation, falsifiable hypotheses, claim level/estimand, variable dictionary, feasible data and sample plan, primary model and assumptions, diagnostics and robustness, conditional conclusion, ethics and reproducibility.

Do not call observational regression causal without a plausible source of quasi-exogenous variation. Treat Chinese institutions as mechanisms or scope conditions, not decorative context.

## method

Infer whether the target is descriptive, associational, mechanistic, predictive, or causal. Compare 2–4 viable approaches by estimand, minimum data/design requirements, assumptions, diagnostics, and main failure mode. Recommend one and state the smallest next step needed for credibility. Read the quantitative research standard before proposing causal identification.

## theory

Start with the sociological puzzle: what varies, for whom, relative to what comparison, and why it is non-obvious. Set out 2–4 genuinely competing lenses, each with a mechanism, observable implication, scope condition, and disconfirming pattern. End with an integrative argument and 2–3 testable propositions. Distinguish constructs from empirical proxies.

## review

Map 3–5 research streams, their central questions, typical evidence, disagreements, and unresolved tensions. If the private local library exists, use verified records as optional reading leads; otherwise provide Chinese and English search strings plus journals or data sources to inspect. Do not invent authors, titles, DOIs, or results. End with a feasible gap and the evidence needed to substantiate it.

For field-specific checks and China-oriented data routing, read [references/framework-checklist.md](references/framework-checklist.md). Do not reproduce copyrighted articles or bypass access controls.
