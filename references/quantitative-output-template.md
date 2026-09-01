# Quantitative Sociology Paper-Framework Output Template

This is the default deliverable structure for one skill invocation. If information is insufficient, write “to verify” and give the minimum viable choice; do not fabricate survey items, sample sizes, policy shocks, or results.

## 0. Working title and research boundary

- Working title:
- Population / place / period:
- Unit of analysis and comparison group:
- Sociological significance and external-validity boundary:

## 1. Puzzle, question, and hypotheses

- Empirical puzzle:
- Main research question:
- H1 (primary association or effect):
- H2 (mechanism/mediation, only if temporal order and measurement support it):
- H3 (heterogeneity/moderation):
- Rival explanations and exclusion strategy:

## 2. Theoretical mechanism and causal diagram

Write `X → M → Y` on one line. List pre-treatment common causes, possible post-treatment variables, potential colliders, and unmeasured alternative mechanisms. Without credible identification, call this a theoretical process map rather than a causal DAG.

## 3. Estimand and claim strength

- Target: description / conditional association / mechanism evidence / causal effect (choose one and explain).
- Estimand: e.g., population-weighted mean difference, conditional mean difference, ATT, or event-time effect.
- Permitted conclusion:
- Conclusion not supported:

## 4. Data and sample construction

| Item | Decision | Codebook/metadata to verify |
| --- | --- | --- |
| Primary dataset |  | Waves, access permission, sampling population |
| Backup dataset |  | Presence of core variables |
| Inclusion/exclusion |  | Age, status, region, repeat observations |
| Merge |  | Keys, levels, years, duplicate rules |
| Weights/design |  | Person/household/longitudinal weights, PSU, strata |
| Expected sample |  | N and missing-data loss at each step |

## 5. Variable dictionary and measurement

| Role | Construct | Raw item/field (to verify) | Primary coding | Missingness/transformation | Alternative coding and risk |
| --- | --- | --- | --- | --- | --- |
| Y |  |  |  |  |  |
| X |  |  |  |  |  |
| M |  |  |  |  |  |
| Z |  |  |  |  |  |
| Pre-treatment control |  |  |  |  |  |

Include only common causes measured before treatment as controls. For every scale, state item count, reverse-coded items, aggregation rule, reliability, and cross-group comparability.

## 6. Primary model, identification, and diagnostics

- Primary model/estimating equation:
- Why it matches Y's distribution, nesting, and estimand:
- Identification assumptions:
- Standard errors, clustering, and weights:
- Minimum diagnostics:
- Fallback if diagnostics fail (for example, downgrade a causal to an associational design):

## 7. Robustness, heterogeneity, and transparency

1. Alternative Y/X measures:
2. Sensitivity to sample, window, and weights:
3. Placebo or assumption diagnostics appropriate to the design:
4. Theory-motivated heterogeneity:
5. Missingness and selection bias:
6. Code, versions, data permission, and ethics:

## 8. Writeable conclusion

Write only a conditional conclusion template: if preregistered models, diagnostics, and robustness checks support the design, state what pattern can be reported, what mechanism account it supports, and which populations or settings it cannot generalize to. Never write hypotheses as established findings.
