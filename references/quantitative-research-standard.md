# Quantitative Sociology Deliverable Standard

The task is not to restate papers. It is to turn a topic into a reviewable, reproducible research design with a conclusion strength matched to its evidence. Run `scripts/query_quant_catalog.py --topic "..."` first, then use the following sequence.

## Twelve required elements

1. **Population and boundary:** who, where, when, and at what unit of analysis; name the comparison group.
2. **Research question:** one answerable primary question and no more than three subquestions; distinguish description, association, mechanism, and causation.
3. **Theoretical mechanism and falsifiable hypotheses:** state how “X → M → Y changes under Z,” including competing mechanisms.
4. **Estimand:** for example, a population mean difference, conditional association, policy ATT, or mediation path; never equate a regression coefficient with a causal effect by default.
5. **Data feasibility:** dataset name, observation level, wave/year, access, measurement of core variables, and coverage of the target population.
6. **Variable dictionary:** outcome, exposure, mediator/moderator, confounding controls, and clustering level. For each, give construct, raw item or field, coding, missing-data rule, expected direction, and alternative coding.
7. **Sample construction:** inclusion/exclusion, weights, merge rules, repeat observations, sample loss, and final N.
8. **Model and identification:** formula/estimating equation, fixed effects or comparison baseline, identification assumptions, and why those assumptions may or may not hold here.
9. **Diagnostics:** at minimum model specification, clustering/weights, missingness, collinearity, and outliers; add design-specific checks such as parallel trends, manipulation, or weak-instrument diagnostics for causal designs.
10. **Robustness and heterogeneity:** prestate alternative measures, sample windows, placebos, model forms, and subgroups; do not search endlessly for significance.
11. **Possible conclusions:** conditionally state what the evidence can and cannot support, plus the external-validity boundary.
12. **Transparency and ethics:** data permission, de-identification, preregistration/codebook, version control, and non-public material.

## Hard constraints on variable roles

- Controls must be common causes measured before treatment or the main exposure. Do not control for mediators, colliders, or post-treatment variables.
- Mediation analysis needs a defensible temporal order; a smaller coefficient after adding a mediator is not mechanism proof.
- For moderation, report interactions and predicted values/marginal effects, not only an interaction coefficient's sign.
- For scales, state items, reverse coding, aggregation, reliability when applicable, and cross-group comparability. Do not remove theoretically essential items merely to raise alpha.
- For categorical variables, state the reference group. For continuous variables, state units, transformations, centering/standardization, and trimming rules. Preserve reproducible recoding rules.

## Preferred analysis gradient

Start with descriptive statistics and sample selection, estimate the primary model next, and consider stronger identification only afterward. Do not claim causality merely to appear advanced when the topic lacks a credible exogenous shock, threshold, or instrument. A strong associational design, mechanism boundary, and measurement quality come first.
