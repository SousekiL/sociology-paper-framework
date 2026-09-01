# Sociology Quantitative Research Framework Skill

[中文](README.md) · [English](README.en.md)

Turn a sociology topic into a feasible, journal-oriented **quantitative research design**. Chinese is the default output language; English is available on request.

## What you get

- A research question, theoretical mechanism, falsifiable hypotheses, and rival explanations.
- A clear distinction between descriptive, associational, mechanism, and causal claims.
- A variable dictionary with coding, missing-data rules, reference groups, and alternative measures.
- China-focused data options, including CGSS, CFPS, CLDS, CHARLS, CHFS, CEPS, CHIP, and official statistics.
- A primary model, identification assumptions, diagnostics, robustness checks, and heterogeneity tests.
- A design that can become a paper outline—not invented empirical findings.

## Use

### 1. Install

Open the [Socpaper repository](https://github.com/SousekiL/sociology-paper-framework) and install the skill, or download the [ZIP package](https://github.com/SousekiL/sociology-paper-framework/archive/refs/heads/main.zip).

It can be used in tools that support custom Skills, Agents, or prompt packages. Import or copy the **entire folder**, then start a new chat. The UI and folder location differ by tool; no API key is needed to generate a research framework.

Common options include Codex, Claude Code, Hermes Agent, and the following widely used China-focused platforms:

- [WorkBuddy](https://www.workbuddy.cn/work/) for custom Skills;
- [Coze](https://docs.coze.cn/): create an agent, put this skill's instructions in its persona/response logic, and add a workflow if needed;
- [Dify](https://docs.dify.ai/): create a Chatbot or Agent, put `SKILL.md` in the system prompt, and optionally attach a knowledge base;
- [FastGPT](https://doc.fastgpt.cn/): create a Chat Agent or workflow and place the core instructions in system configuration.

Platforms do not necessarily import the same Skill-folder format. If direct import is unavailable, retain the full folder as reference and copy `SKILL.md` into the platform's system-prompt or agent-instructions field.

### 2. Use one command

Remember just one command: `/socpaper`. Put a mode keyword after it, then your topic. Without a keyword, it defaults to `paper`.

```text
/socpaper paper How do social relationships affect platform workers' mobility?
/socpaper method social relationships and occupational mobility
/socpaper theory social relationships in digital platforms
/socpaper review social capital and youth employment in China
```

| Keyword | Purpose | Best input |
| --- | --- | --- |
| `paper` | Full quantitative paper framework | Topic or research question |
| `method` | Method selection, identification, and diagnostics | Question or keywords |
| `theory` | Theory, mechanisms, and propositions | Topic or phenomenon |
| `review` | Prior research, debates, and gaps | Field or keywords |

All four modes primarily use the model's own social-science and methodological reasoning. A private local library is used only when it is genuinely available as supplementary evidence; uncertain memory is never presented as a verified citation.

You can also specify the intended design directly:

```text
/socpaper paper In English, design a causal study of hukou status and occupational mobility, prioritizing accessible Chinese panel data.
```

The skill includes method, measurement, data, and quality-control standards. Always verify final items, fields, sample rules, and permissions against the selected data documentation.

## Privacy

This public repository contains no personal literature library, article texts, reading notes, API keys, or data created by updates. A private local library may enrich a user’s own results, but it is never distributed through installation, forks, or downloads.

## Scope

This project supports research design. It does not replace data cleaning, codebook verification, ethics review, data-use agreements, or empirical analysis.
