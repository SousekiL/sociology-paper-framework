# Open-Access Full-Text Review Protocol

Review one explicitly open-access, downloadable PDF each week. The output is a structured research-design card, not a copy of the article, a long abstract, or training material.

The extracted text of every article must be read in coverage-preserving chunks and synthesized from the resulting evidence cards; never review only the introduction, abstract, or first pages. Each final card records the research puzzle, theoretical mechanism, data and sample, variables and measurement, identification and model, diagnostics and robustness, transferable design lesson, limitations, DOI, and open full-text link. Use `null` when the full text does not support a field; never infer it from an abstract.

Do not automatically review paywalled articles, robots-restricted content, PDFs without explicit open access, or articles without an effective license signal. A user with lawful access may provide a full text. The public repository never commits PDFs, extracted article text, or private reading cards.

The reviewer uses an OpenAI Chat Completions-compatible API. It reads `LLM_API_KEY` (or `OPENAI_API_KEY`) locally; `LLM_BASE_URL` sets a compatible URL ending in `/v1`, and `LLM_MODEL` selects the model. Store all credentials only in a local secure credential store or private environment configuration, never in a repository or chat.
