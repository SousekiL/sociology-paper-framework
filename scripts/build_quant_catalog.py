#!/usr/bin/env python3
"""Build a searchable quantitative-sociology reference catalogue from maintained cards."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "quantitative-reference-catalog.json"

METHODS = [
 ("Descriptive statistics and weighted comparisons", "Sample composition, distributions, or group differences are central to the question", "Descriptive differences in the population/sample", "Sampling design, weights, and missingness are correctly reported", "Weighted/unweighted comparisons; confidence intervals; complex sampling design"),
 ("Multiple linear regression (OLS)", "Continuous outcome with a focus on conditional association", "Conditional mean difference/linear association", "Functional form and independence; unobserved confounding is not resolved", "Residual plots; nonlinear terms; robust/clustered standard errors; influential points"),
 ("Binary Logit/Probit", "Binary outcome requiring a conditional probability model", "Conditional probability differences", "Link function, rare events, and independent observations", "Report average marginal effects; event counts; predictive calibration; alternative links"),
 ("Ordered Logit/Probit", "Ordinal outcome with a clear ordering", "Differences in latent propensity/category probabilities", "Proportional-odds or parallel-lines assumption (if using ordered logit)", "Proportional-odds test; generalized ordered model; marginal effects"),
 ("Multinomial Logit", "Multicategory choice without a natural order", "Association with relative category choice", "IIA is reasonable in the specific choice context", "Alternative IIA diagnostics; predicted probabilities; reference-group sensitivity"),
 ("Count models (Poisson/negative binomial)", "Outcome is a count of occurrences or events", "Conditional incidence-rate ratio", "Mean–variance relationship and exposure-time handling", "Overdispersion; zero inflation; offset; negative-binomial alternative"),
 ("Two-part/zero-inflated models", "Zeros arise from separate nonparticipation and intensity processes", "Participation probability and conditional amount among positive values", "The distinction between the two processes has a theoretical basis", "Compare with hurdle/ordinary GLM; residuals for the positive-value part"),
 ("Quantile regression", "Focus on associations at different positions in the outcome distribution", "Conditional quantile differences", "Interpretation concerns quantiles rather than means", "Present multiple quantiles; bootstrap standard errors; support in sample tails"),
 ("Generalized additive models/splines", "Theory suggests nonlinearity but does not justify imposing a rigid functional form", "Smoothed conditional association", "Control of smoothness complexity and caution with extrapolation", "Effective degrees of freedom; cross-validation; linear-model comparison"),
 ("Multilevel models", "Individuals are nested in families, schools, communities, or regions", "Within-/between-group associations and variance decomposition", "Level specification, number of groups, and random-effects distribution", "ICC; random slopes; number of clusters; fixed-effects comparison"),
 ("Panel fixed effects", "Repeated observations of the same units with concern about time-invariant confounding", "Association in within-unit change", "Strict exogeneity and sufficient within-unit variation", "Unit/time FE; clustering; lagged outcomes; attrition checks"),
 ("Random effects/mixed models", "Need to estimate between-unit and within-unit variation simultaneously", "Conditional association and variance components", "Random effects are independent of explanatory variables (or Mundlak is explicitly used)", "Hausman/Mundlak comparison; random slopes; residual structure"),
 ("Difference-in-differences (2×2)", "Treatment and control groups with clearly defined pre/post periods", "Average treatment effect for the treated group", "Parallel trends, no differential concurrent shocks, and stable sample composition", "Event study; pre-trends; placebo time/group; clustering level"),
 ("Staggered-adoption DiD", "Different units receive treatment at different times", "Group–time ATT", "Use an estimator that avoids negative weights; parallel trends hold by cohort", "Sun-Abraham/Callaway-Sant'Anna; cohort plots; disclose weights"),
 ("Event study", "Need to show dynamic paths before and after an intervention", "Relative event-time effects", "Event-time definition, no anticipation, and comparable trends", "Coefficient plots with confidence intervals; window sensitivity; stacked design"),
 ("Regression discontinuity design (RDD)", "Treatment is determined by a continuous running variable crossing a clear threshold", "Local effect at the threshold", "Potential outcomes are continuous near the threshold; no precise manipulation", "Density test; covariate balance; bandwidth/order sensitivity; donut"),
 ("Instrumental variables (IV/2SLS)", "A strongly relevant and defensible exogenous instrument exists", "Local average treatment effect (LATE)", "Relevance, exclusion restriction, and monotonicity", "First-stage F/weak-instrument robust intervals; mechanism rebuttals; instrument balance"),
 ("Propensity-score weighting/matching", "Comparable groups can be constructed on observed covariates in observational data", "ATT/ATE under selection on observables", "Ignorability, overlap, and model specification", "Standardized differences; common support; trimming; doubly robust estimation"),
 ("Synthetic control", "Few treated units and a long pre-treatment period", "Effect for the treated unit relative to its synthetic counterfactual", "Comparable donor pool, credible pre-treatment fit, and no spillovers", "Pre-treatment RMSPE; placebo tests; donor/predictor sensitivity"),
 ("Survival/hazard models", "Interest lies in time to event with censoring", "Association with hazard rate/survival time", "Censoring mechanism and proportional hazards (if Cox)", "Kaplan–Meier; PH test; competing risks; time-varying coefficients"),
 ("Latent growth/trajectory models", "Interest lies in how individual outcomes change over time", "Average growth and heterogeneous trajectories", "Measurement timing and trajectory classes have substantive interpretations", "Sensitivity to number of classes; entropy; posterior classification uncertainty; alternative functions"),
 ("Structural equation modeling (SEM)", "Theory includes multiple paths or latent variables", "Prespecified path/latent-variable relationships", "Valid measurement model, sufficient identification, and theoretically grounded structure", "CFI/TLI/RMSEA/SRMR; alternative models; measurement invariance"),
 ("Causal mediation analysis", "The treatment–mediator–outcome sequence and mechanism evidence can be measured", "Natural direct/indirect effects (under strict assumptions)", "Sequential ignorability and no post-treatment mediator–outcome confounding", "Sensitivity analysis; temporal ordering; alternative mediator measures"),
 ("Multiple imputation (MICE)", "Missingness can be regarded as MAR conditional on observed information", "Reduced bias/efficiency loss due to missingness", "Imputation model includes analysis variables and predictors of missingness", "Missingness patterns; number of imputations; complete-case comparison; MNAR sensitivity"),
 ("Survey design analysis", "Complex sample surveys include stratification, clustering, or weights", "Population-level description/association", "Weights, PSUs, strata, and finite-population corrections are correctly specified", "Design effect; weighted distributions; sensitivity to weight trimming"),
 ("Spatial regression", "Geographic proximity may generate correlation or spillovers", "Association/effect adjusted for spatial dependence", "Spatial weight matrix and scale have substantive justification", "Moran's I; alternative matrices; residual spatial correlation; boundary sensitivity"),
 ("Network analysis", "The relational structure itself is an explanatory variable or outcome", "Network position/formation mechanisms", "Network boundaries, missing nodes, and dependence structure are handled", "Network description; permutation/ERGM diagnostics; alternative boundaries"),
 ("Text as data", "Large volumes of text can measure categories, frames, or sentiment", "Description/association between text features and social outcomes", "Corpus representativeness, preprocessing, and annotation validity", "Human-annotation agreement; dictionary/model robustness; temporal drift"),
 ("Repeated cross-sectional trends", "Samples from different years are comparable but do not include the same respondents", "Population-level trends and changes in associations", "Questionnaire, sampling, weights, and variable definitions are comparable", "Measurement equivalence; year interactions; standardize sample composition"),
]

CONSTRUCTS = [
 ("Socioeconomic status/class", ["Years of education/educational attainment", "Occupational status index or occupational category", "Household income/wealth percentile"], "Use theory to determine whether a unidimensional or multidimensional index is appropriate; income is often logged and equivalized by household size", "Do not mechanically add education, occupation, and income; report the sensitivity of each dimension and the index", ["class","inequality","education","work","income"]),
 ("Disposable personal income", ["Annual/monthly after-tax income", "Equivalized household income", "Income percentile or below-poverty-line status"], "Handle zero/negative values; specify currency, time unit, price deflation, and equivalence scale", "When right skew is severe, compare log, IHS, and quantile specifications; income missingness is usually nonrandom", ["income","poverty","inequality","family"]),
 ("Household wealth/debt", ["Net assets", "Financial assets", "Debt-to-income ratio"], "Assets minus debt; zero and negative values cannot be logged directly", "Top-coding can change inequality conclusions; report whether housing and business assets are included", ["wealth","debt","family","inequality","housing"]),
 ("Employment status", ["Employed/unemployed/out of the labor force", "Formal/informal", "Full-time/non-full-time"], "Specify working-age population, reference week/month, and unemployment definition; retain the original multicategory classification", "Do not combine students, retirees, and unemployed people into nonemployment; note selection into the labor market", ["employment","labor","unemployment","work"]),
 ("Job quality", ["Contract/social-insurance coverage", "Working hours and overtime", "Pay, stability, and control"], "Use a theory-driven dimensional index or estimate dimensions separately to avoid masking trade-offs", "For platform work, separately capture algorithmic control, order volatility, and multi-platform work", ["labor","platform","work","social insurance"]),
 ("Occupational status", ["ISCO/CASMIN/ESeC categories", "Occupational prestige/status score", "Managerial/professional positions"], "Retain occupational codes at a reproducible level and document the mapping version", "Occupational classifications have limited cross-year/country comparability; do not substitute subjective self-assessment for objective occupational position without explanation", ["occupation","class","mobility","work"]),
 ("Educational attainment", ["Highest qualification", "Years of schooling", "Completion of key educational stages"], "Prefer mappings based on the education system; for intergenerational/cross-regional comparisons, report both categories and years", "Educational expansion changes the relative status of the same qualification; consider birth cohorts", ["education","class","youth","mobility"]),
 ("Educational aspirations/investment", ["Parental expectations", "Tutoring expenditure/time", "School choice/further-study intentions"], "Distinguish child and parent reports; make clear that measurement precedes the outcome", "Aspirations are often jointly determined with prior achievement; avoid controlling for post-treatment investment at baseline", ["education","family","children","class"]),
 ("Self-rated health", ["Self-rated health 1–5", "Presence of chronic disease", "ADL/IADL limitations"], "Preserve the original scale direction; justify ordinal models or binary thresholds theoretically", "Self-rated health is affected by reference groups; check measurement comparability across groups", ["health","older adults","medical care"]),
 ("Mental health", ["CES-D/PHQ/GHQ total score", "Clinical threshold", "Frequency of individual emotions"], "Follow the scale manual for reverse coding, item-missing rules, and thresholds; report internal consistency", "Scales are not diagnoses; do not equate screening thresholds with clinical illness", ["mental health","depression","health","family"]),
 ("Life satisfaction/well-being", ["Overall satisfaction", "Positive/negative affect", "Sense of purpose/meaning"], "Prefer retaining ordinal scales; OLS may be reported as an interpretability comparison", "Response styles differ across cultures; avoid strong claims that ignore reverse causality", ["well-being","satisfaction","quality of life"]),
 ("Social trust", ["General trust item", "Institutional trust items", "Trust in specific groups"], "Distinguish generalized from institutional trust; report dimensional tests for multi-item scales", "Single items and scales are not interchangeable; describe missingness in politically sensitive items", ["trust","social capital","politics","community"]),
 ("Social participation", ["Association/volunteer activities", "Voting/consultation", "Online civic participation"], "Specify the frequency window and boundaries between formal and informal participation", "Opportunity structures generate zeros; use a two-part model when necessary", ["participation","volunteering","community","politics"]),
 ("Social capital", ["Network size/heterogeneity", "Reciprocal support", "Organizational embeddedness"], "Distinguish structural, relational, and cognitive dimensions; do not use the number of acquaintances alone to represent all social capital", "Network surveys are vulnerable to truncation and recall bias; document name-generator rules", ["social capital","network","trust","family"]),
 ("Gender attitudes", ["Agreement with gender roles", "Views on household/childcare division", "Views on workplace equality"], "Align item direction before building a scale; test measurement invariance across gender and generations", "Social-desirability bias may be substantial; treat attitudes cautiously as stable traits", ["gender","family","marriage","labor"]),
 ("Fertility intentions/behavior", ["Ideal/planned number of children", "Near-term fertility plans", "Actual births/birth spacing"], "Model intentions and behavior separately; event-history methods suit birth timing", "Intentions are affected by current partners, policy, and economic shocks; do not treat them as fixed preferences", ["fertility","marriage","family","women"]),
 ("Marriage and family structure", ["Marital status", "Cohabitation/age at first marriage", "Household size/intergenerational co-residence"], "Define legal, residential, and economic households clearly; document household-member identification rules", "Retain tracking rules for household splits/mergers across waves; avoid treating family structure as a purely voluntary outcome", ["marriage","family","generations","care"]),
 ("Care work", ["Caregiving hours", "Primary caregiver", "Care burden scale"], "Distinguish childcare, eldercare, and disability care; time diaries are preferable to rough recall items", "Zeros and intensity may reflect two processes; gender differences require controls for available time and need", ["care","family","older adults","gender"]),
 ("Migration/mobility", ["Migration status", "Migration distance/duration", "Whether registered and usual residence are separate"], "Distinguish interprovincial, intercity, rural–urban, and return migration; record the baseline time point", "Origin choice and survivor samples among migrants create selection bias; current residence is not a substitute for migration history", ["migration","migrants","household registration","urban"]),
 ("Household registration and institutional exclusion", ["Agricultural/non-agricultural registration", "Local/nonlocal registration", "Points-based/hukou eligibility"], "Record birth registration, current registration, and residence simultaneously; construct institutional-match variables", "Registration changes are selective; do not treat registration only as a static binary control", ["household registration","migration","urban","inequality"]),
 ("Social insurance", ["Pension/health/unemployment insurance enrollment", "Contribution continuity", "Benefit accessibility"], "Distinguish statutory coverage, actual contributions, and actual use; define enrollment consistently", "Self-reported enrollment may contain comprehension error; specify institutional pathways for platform/flexible workers", ["social insurance","labor","welfare","platform"]),
 ("Housing conditions", ["Ownership/renting", "Housing-cost burden", "Per-capita floor area/crowding"], "Burden is often defined as the expenditure-to-income ratio; handle zero income; distinguish household and individual ownership", "Housing prices and residential choice covary; regional comparisons should account for price levels and city tiers", ["housing","urban","family","inequality"]),
 ("Community/neighborhood conditions", ["Community facilities", "Subjective safety/cohesion", "Area poverty or service provision"], "Model individual perceptions and administrative-area indicators separately; specify spatial scale", "Area averages can produce ecological fallacies; document geographic linkage and privacy handling", ["community","urban","neighborhood","governance"]),
 ("Digital divide", ["Device/broadband access", "Digital skills", "Usage frequency/purpose"], "Distinguish access, capability, and use benefits; do not rely only on whether someone uses the internet", "Self-reported use bias and age confounding can be strong; platform-data coverage is not population coverage", ["digital","internet","platform","artificial intelligence"]),
 ("Platform work", ["Whether taking platform/crowdsourcing jobs", "Share of income from platforms", "Algorithmic control/evaluation pressure"], "Define platform type and reference period; record multi-platform and mixed online/offline work", "Nonprobability platform samples cannot be generalized; handle multiple sources of income and hours", ["platform","labor","algorithm","flexible employment"]),
 ("Public-service accessibility", ["Distance/time to nearest service", "Actual use", "Perceived affordability/quality"], "Separate supply, accessibility, use, and satisfaction; document geographic linkage", "Use is often driven by need severity; do not directly interpret higher use as better service", ["public services","medical care","education","governance"]),
 ("Subjective social mobility", ["Expectation of upward mobility", "Relative intergenerational position", "Social-status ladder"], "Distinguish objective and subjective mobility; report the reference group and time frame", "Optimism bias/adaptive preferences may be strong; present alongside, rather than substitute for, objective measures", ["mobility","class","inequality","expectations"]),
]

DATASETS = [
 ("CGSS", "Chinese General Social Survey", "Cross-sectional social attitudes and stratification at the individual/household/community levels", "Public application or project-specific rules", "https://cgss.ruc.edu.cn/", ["class","trust","attitudes","family","labor","social capital","network","participation"]),
 ("CFPS", "China Family Panel Studies", "Individual–household–community panel suited to family, education, health, and mobility", "Register and follow the data-use agreement", "https://opendata.pku.edu.cn/dataverse/CFPS", ["family","education","health","income","mobility","social capital","network"]),
 ("CLDS", "China Labor-force Dynamics Survey", "Workers, households, and communities, suited to employment, labor relations, and social insurance", "Apply under the provider's rules", "https://css.sysu.edu.cn/", ["labor","employment","social insurance","migration"]),
 ("CHARLS", "China Health and Retirement Longitudinal Study", "Longitudinal health, caregiving, and economic data on individuals and households aged 45 and older", "Register and follow the data-use agreement", "https://charls.charlsdata.com/", ["health","older adults","care","family"]),
 ("CHFS", "China Household Finance Survey", "Household assets, liabilities, income, insurance, and consumption", "Apply under the survey provider's data rules", "https://chfs.swufe.edu.cn/", ["wealth","income","finance","family"]),
 ("CHNS", "China Health and Nutrition Survey", "Long-term individual, household, and community health/nutrition and socioeconomic data", "Obtain under UNC data rules", "https://www.cpc.unc.edu/projects/china", ["health","family","community","income"]),
 ("CEPS", "China Education Panel Survey", "Longitudinal data on middle-school students, parents, teachers, and schools", "Register and follow the data-use agreement", "https://ceps.ruc.edu.cn/", ["education","children","family","school"]),
 ("CHIP", "China Household Income Project", "Microdata on income, poverty, distribution, and the labor market", "Obtain through research application/agreement", "https://cid.cass.cn/", ["income","poverty","inequality","labor"]),
 ("CSS", "Chinese Social Survey", "Social structure, public services, living conditions, and attitudes", "Follow data-release rules", "https://css.cssn.cn/", ["class","governance","public services","family","social capital","trust","participation"]),
 ("CMDS", "China Migrants Dynamic Survey", "Employment, family, health, and public services among migrants", "Often restricted or available through project channels", "https://www.nhc.gov.cn/", ["migration","household registration","health","public services"]),
 ("China Population Census", "National population census and sample surveys", "Aggregate/regional measures of population, education, migration, and housing", "Public tabulations; confirm separate access for micro samples", "https://www.stats.gov.cn/", ["population","migration","education","housing"]),
 ("National Bureau of Statistics database", "Annual national and regional statistics", "Prefecture-, city-, and county-level economic, demographic, employment, and public-service indicators", "Public tables; record download date and definitions", "https://data.stats.gov.cn/", ["regions","economy","employment","population"]),
 ("China City Statistical Yearbook", "Annual city-level statistics", "Urban economy, construction, public services, environment, and population", "Yearbook/database access depends on source", "https://www.stats.gov.cn/", ["urban","housing","public services","environment"]),
 ("China Labour Statistical Yearbook", "Annual labor-market statistics", "Regional measures of employment, wages, social insurance, and labor disputes", "Yearbook/database access depends on source", "https://www.stats.gov.cn/", ["labor","wages","social insurance","employment"]),
 ("Education statistics", "Ministry of Education statistics on educational development", "Administrative statistics on schools, teachers and students, funding, and progression", "Public tabulations; school-level microdata are usually restricted", "http://www.moe.gov.cn/", ["education","school","regions"]),
 ("China Judgments Online/government public information", "Public legal and government texts", "Observable traces of texts, cases, or policy implementation", "Public availability does not imply bulk-reuse rights; follow site rules", "https://wenshu.court.gov.cn/", ["law","governance","text","platform"]),
 ("Peking University Digital Financial Inclusion Index", "Regional digital-finance indicators", "Provincial, prefectural, and county-level digital-finance development and subdimensions", "Verify version, spatial matching, and usage license", "https://idf.pku.edu.cn/", ["digital","finance","urban","regions"]),
 ("China household panel/special-topic survey secondary data", "Special-topic data from academic institutions", "Supplementary microdata on specific groups and mechanisms", "Verify sampling, years, permissions, and field documentation for each dataset", "https://opendata.pku.edu.cn/", ["family","education","health","special topics"]),
 ("World Values Survey", "World Values Survey", "Cross-national comparisons of attitudes, values, and social trust", "Register, download, and use survey weights", "https://www.worldvaluessurvey.org/", ["values","trust","politics","comparative"]),
 ("ISSP", "International Social Survey Programme", "Cross-national, modular social attitudes and institutional evaluations", "Use according to archive rules", "https://issp.org/", ["attitudes","family","inequality","comparative"]),
]

CHECKS = [
 ("Research-question level", "First classify the study as descriptive, associational, mechanistic, or causal; do not make claims stronger than the design supports."),
 ("Unit of analysis", "Specify whether variables are at the individual, household, firm, community, or regional level; avoid cross-level interpretations."),
 ("Temporal ordering", "Mark measurement times for X, M, and Y; cross-sectional data cannot establish ordering."),
 ("Sample flow", "Report initial N, every exclusion rule, loss due to missingness, and final N."),
 ("Weights", "With survey data, consult the codebook to determine whether individual/household/longitudinal weights should be used."),
 ("Missingness", "Report missingness and handling separately for core variables; do not assume listwise deletion is unbiased."),
 ("Outliers", "Pre-specify trimming, winsorization, log/IHS transformations, and thresholds, then conduct sensitivity comparisons."),
 ("Reference groups", "Label reference groups for categorical variables; report combined predictions for interactions rather than reading coefficients alone."),
 ("Standard errors", "Choose clustered or complex-survey variance estimation according to the sampling, treatment-assignment, and repeated-observation levels."),
 ("Common support", "For matching, weighting, and causal models, check comparable support ranges for treatment and control groups."),
 ("Pre-trends", "For any DiD/event study, show pre-treatment coefficients, confidence intervals, and the specific window."),
 ("Placebos", "Use unaffected times, outcomes, or pseudo-treatment groups to test design specificity."),
 ("Multiple testing", "For multiple outcomes/groups, distinguish exploratory from confirmatory analyses and, when necessary, adjust or control the FDR."),
 ("Heterogeneity", "Subgroups must have theoretical justification; report interactions, group sample sizes, and common support."),
 ("Reproducibility", "Preserve raw-data versions, codebooks, cleaning scripts, analysis scripts, and random seeds."),
 ("Ethics and permissions", "Record data agreements, de-identification, minimization of sensitive variables, and access conditions for nonpublic materials."),
]


CARDS: list[dict] = []
CARD_SEQUENCE = 0


def card(group: str, label: str, facet: str, text: str, topics: list[str]) -> dict:
    global CARD_SEQUENCE
    CARD_SEQUENCE += 1
    return {"id": f"{group}:{CARD_SEQUENCE:03d}", "group": group, "label": label, "facet": facet, "text": text, "topics": topics}
for name, when, claim, assumptions, diagnostics in METHODS:
    CARDS.extend([
        card("method", name, "Applicable question", when, []),
        card("method", name, "Estimand and conclusion", claim, []),
        card("method", name, "Key assumptions", assumptions, []),
        card("method", name, "Minimum diagnostics", diagnostics, []),
    ])
for name, indicators, coding, caveat, topics in CONSTRUCTS:
    CARDS.extend([
        card("measurement", name, "Candidate indicators", ";".join(indicators), topics),
        card("measurement", name, "Primary coding rules", coding, topics),
        card("measurement", name, "Measurement warnings", caveat, topics),
        card("measurement", name, "Reporting requirements", "List original items/fields, values, reference groups, missing-value codes, transformations, and alternative codings.", topics),
    ])
for short, name, coverage, access, url, topics in DATASETS:
    CARDS.append(card("dataset", short, "Dataset", f"{name}: {coverage}. Access: {access}. Official entry point: {url}", topics))
for label, text in CHECKS:
    CARDS.append(card("quality_check", label, "Check", text, []))


def main() -> None:
    payload = {"version": "1.0", "purpose": "Searchable cards for quantitative sociology research design, variable measurement, data selection, and quality control.", "card_count": len(CARDS), "cards": CARDS}
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(CARDS)} cards to {OUT}")


if __name__ == "__main__":
    main()
