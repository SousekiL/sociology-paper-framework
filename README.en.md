# Sociology Quantitative Research Framework Skill

[中文](README.md) · [English](README.en.md)

This Codex skill turns a sociology topic into a reviewable, reproducible, journal-oriented **quantitative research design**. It does not store or copy original articles. Its core is a maintained library of method, measurement, data-selection, identification, and diagnostic standards.

## What it produces

- A precise research question, theoretical mechanism, falsifiable hypotheses, and rival explanations.
- A conclusion level matched to the design: description, association, mechanism evidence, or causal effect.
- A variable dictionary with constructs, codebook fields to verify, coding, missingness, reference groups, and alternatives.
- China-focused data options, including CGSS, CFPS, CLDS, CHARLS, CHFS, CEPS, CHIP, and official statistics.
- A primary model, assumptions, diagnostics, robustness checks, heterogeneity analysis, reproducibility, and ethics requirements.
- Conditional conclusions rather than invented findings.

## Built-in standards

`data/quantitative-reference-catalog.json` contains 260 searchable cards: 116 method/diagnostic cards, 108 measurement/coding cards, 20 dataset cards, and 16 quality-control cards.

## Literature library

`library/` contains lawful public **metadata and available abstracts**, never full papers. Its update process is append-only and DOI-deduplicated: new scans enrich the archive and never overwrite accumulated records. Each week it may select up to three explicitly licensed open-access PDFs, cover the complete extracted text in chunks, and store only structured design notes—not PDFs or extracted article text. Automated reading accepts an OpenAI Chat Completions-compatible API: configure `LLM_API_KEY` as a repository secret and optionally `LLM_BASE_URL` and `LLM_MODEL` as repository variables; official OpenAI remains the default.

The weekly workflow scans recent work and advances one six-month historical window per source. It covers Chinese sociology-related English journals, ASR, *Social Problems*, *The British Journal of Sociology*, and selected economics/statistics journals for methodological breadth. The Chinese journals *Sociological Studies* and *Society* remain in a manual verification queue because their metadata is not reliably exposed through open APIs.

## Install and run

Place the directory in Codex’s skills directory, then invoke:

```text
$sociology-paper-framework
Topic: How do social relationships affect occupational mobility among platform workers?
```

See the Chinese README for commands and operational details.
