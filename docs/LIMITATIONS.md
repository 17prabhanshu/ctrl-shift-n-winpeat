# Methodological Limitations & Epistemic Boundaries

Scientific rigor requires explicit boundaries on what the empirical data can and cannot substantiate. The Workforce Intelligence Engine (WIE) documents the following seven structural and methodological limitations.

---

## 1. Small Sample Constraints ($n=139$ and $n=161$)
- **Context**: The internal outcome datasets—Junior Data Scientist Skills (`JDS`, $n=139$) and Senior Data Scientist Personality (`SDS`, $n=161$)—represent very small cohorts.
- **Risk**: Small-sample regimes are highly vulnerable to sampling variance, sparse sub-cell counts, and seed-lottery artifacts where arbitrary data partitions yield wildly divergent metric estimates.
- **Mitigation & Boundary**: We utilized Repeated Stratified 5-Fold Cross-Validation (20 repetitions = 100 evaluations per algorithm) and Firth Penalized Likelihood estimation to guarantee finite parameter bounds. However, statistical power remains limited for higher-order interaction effects. All reported metrics must be interpreted with their corresponding 95% confidence intervals rather than as single point estimates.

---

## 2. Absence of Row-Level Identifiers & Ecological Inference
- **Context**: The four datasets (`Analytics Jobs`, `DataScience Jobs`, `JDS`, `SDS`) do not share a common candidate or employer primary key.
- **Risk**: Forcing a row-level join across datasets based on superficial string matches (such as job title) commits the **Ecological Fallacy**—falsely attributing aggregate labor market characteristics to individual practitioners.
- **Mitigation & Boundary**: We established strict **Context-Isolated Evidence Lanes**. Datasets are analyzed independently, and cross-dataset synthesis is conducted strictly at the abstract construct level (comparing market demand volume across five standardized skill dimensions to the estimated log-odds in internal evaluations). This cross-dataset alignment is strictly exploratory; it does not constitute proof that individual market trends determine specific career progressions.

---

## 3. Observational Design & Absence of Causal Identification
- **Context**: All analyzed data are observational cross-sections. No randomized controlled trial (A/B test of training interventions) or natural experiment (instrumental variable or regression discontinuity) is present.
- **Risk**: Conflating statistical association with causal mechanisms (e.g., claiming that upskilling in storytelling *causes* a junior promotion).
- **Mitigation & Boundary**: The evidence governance layer strictly enforces an associative vocabulary. Coefficients represent conditional associations after adjusting for observable covariates (such as experience and role family). Unobserved confounders—such as unmeasured mentorship, firm-specific budget cycles, or elite educational pedigree—remain unmodeled.

---

## 4. Forensic Label Generation Risk in SDS Cohort
- **Context**: Machine learning benchmarks on the Senior Data Scientist (`SDS`) dataset yielded an anomalous ROC-AUC of **0.998** across gradient-boosted ensembles.
- **Forensic Discovery**: A depth-restricted decision tree audit revealed that a simple two-node threshold rule:
  $$\text{openness\_to\_experience} > 38.50 \quad \land \quad \text{conscientiousness} > 36.50$$
  achieves an ROC-AUC of **0.917** on out-of-fold cross-validation.
- **Boundary**: This near-perfect separability strongly suggests that the target variable (`success_classification_high_low`) was generated via deterministic synthetic business rules rather than observed natural workplace performance. We report this high AUC as a **data-generation artifact**, not as an algorithmic achievement or deployment-ready predictor.

---

## 5. Non-Independence in Repeated Cross-Validation
- **Context**: We benchmarked models using 20 repeats of 5-fold cross-validation.
- **Risk**: While repeated cross-validation reduces variance from a single lucky split, the resulting 100 test folds share overlapping training instances. They do not constitute 100 independent statistical experiments.
- **Boundary**: Calculating standard errors directly across overlapping folds can underestimate true parameter uncertainty. While useful for internal model comparison, the confidence intervals should not be treated as independent sample distributions.

---

## 6. Skill Taxonomy & Keyword Extraction Limits
- **Context**: The `Analytics Jobs` dataset contains 15,841 raw, unstandardized `key_skills` entries.
- **Risk**: Deterministic N-gram matching and alias dictionaries may produce false negatives for novel libraries or false positives for ambiguous short acronyms (e.g., `"r"` as a language versus a character in an address).
- **Boundary**: We mapped skills into five canonical dimensions and verified precision against a 50-skill gold standard (`src/nlp/nlp_benchmark.py`). However, the taxonomy captures the most frequent ~80% of data tooling and does not account for subtle semantic context that a deep linguistic parser might detect.

---

## 7. Ethical & Governance Boundaries: Prohibition of Automated Screening
- **Context**: Deploying predictive models in human capital and hiring workflows carries profound legal and ethical responsibilities under frameworks like the EU AI Act (High-Risk AI Systems).
- **Boundary & Prohibition**: 
  - **No Automated Rejection**: These models must **never** be used for autonomous candidate filtering, hiring exclusion, or personality-based gatekeeping.
  - **Decision Support Only**: If piloted in workforce planning, the system must utilize distribution-free **Conformal Prediction Sets** ($1 - \alpha = 0.90$), which allow the system to output prediction sets containing both classes (abstaining) whenever applicant profiles exhibit ambiguity, routing them to human interviewers.
