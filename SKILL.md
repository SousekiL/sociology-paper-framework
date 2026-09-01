---
name: sociology-paper-framework
description: Generate a feasible sociology-journal quantitative research framework for a user topic, grounded in methods, measurement, data, and quality standards.
---

# Sociology Paper Framework

Turn a topic into a rigorous, primarily **quantitative** sociology research design. This is a research-design system—not an archive of copyrighted articles, nor a promise to store or reproduce original papers.

## Start with the quantitative reference system

1. Run `scripts/query_quant_catalog.py --topic "<topic>"`. It retrieves maintained cards for research designs, variable measurement, Chinese/ comparative datasets, coding cautions, and diagnostic checks. Use the `--aim` option only when the user clearly specifies description, association, mechanism, or causal effect.
2. Read [references/quantitative-research-standard.md](references/quantitative-research-standard.md) before proposing an identification strategy. It is the required output and measurement standard.
3. Build the sociological puzzle directly from the topic, mechanism, scope condition, and comparison group. Do not force a theory or a causal claim merely because a method card exists.
4. A private local `library/` directory may be present on the current device. Use it only when it exists and the user requests literature leads, a journal scan, or methodological trends. Never assume it is installed, distributed, or available to other users.
5. If private full-text reading notes are present, use them as stronger design evidence than metadata alone. Follow [references/full-text-review-protocol.md](references/full-text-review-protocol.md); never claim to have read a paper when no local note or lawful user-provided full text exists.

## Deliverable

Respond in Chinese unless asked otherwise. Use [references/quantitative-output-template.md](references/quantitative-output-template.md) as the default structure, and give a publication-oriented quantitative design with the twelve required items in the standard. In particular, include:

- one precise research question and two to three falsifiable hypotheses, each linked to an observable mechanism and a competing explanation;
- an estimand and a claim level (description, association, mechanism, or causal effect); do not call an observational regression causal by default;
- a variable dictionary table: role (Y/X/M/Z/control), construct, raw question/field to verify in the codebook, coding, reference group or unit, missing-value rule, expected direction, and alternative coding;
- a sample-construction and data plan: unit, population, years/waves, inclusion/exclusion, weights, merge keys, likely final N, permissions, and why the proposed data actually covers the question;
- one primary estimation strategy, its assumptions, minimum diagnostics, robust standard error/cluster rule, and at least three theory-motivated robustness or heterogeneity tests;
- a conditional conclusion: what the design could support, what it cannot establish, and the external-validity boundary;
- a compact data-management and ethics note.

Choose the simplest design that matches the estimand. Offer a causal design only when a plausible source of quasi-exogenous variation is specified; otherwise provide a strong association design and state what additional data or event would be needed for causality. Qualitative work is an optional secondary design only if the user asks for it.

Do **not** include original-paper links by default or claim to have stored original articles. If literature support is requested, select a small number of verifiable library records, cite their DOI/publisher URL, and label them as reading leads—not as evidence for an unperformed analysis.

## China-specific quality bar

Treat institutional arrangements (hukou, local fiscal capacity, platform governance, family strategy, regional hierarchy, etc.) as potential mechanisms or scope conditions, not decorative context. Explain why the proposed case can inform a broader Chinese sociological question, and what it cannot generalize to.

For a detailed field checklist and data routing, read [references/framework-checklist.md](references/framework-checklist.md). Do not reproduce copyrighted full articles or bypass access controls; use abstracts, metadata, and user-provided lawful full text for deeper reading.
