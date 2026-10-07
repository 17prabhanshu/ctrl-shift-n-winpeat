# Workforce Intelligence Engine: Methodological Foundations & Research References

## Executive Summary & Theoretical Framework

The **Workforce Intelligence Engine** investigates a fundamental labor-market question: *Does the market pay for what progression rewards?* 

The empirical foundation comprises four unlinked datasets provided without an explicit prediction target:
1. `Analytics Jobs.csv` (15,841 postings with salaries, titles, and raw comma-delimited skill lists)
2. `DataScience Jobs.csv` (1,602 postings with LPA salaries and company/role attributes)
3. `JDS Skill Traits.xlsx` (139 junior-professional records scored across five technical and communication competencies, labelled with a high/low salary hike outcome)
4. `SDS Personality Traits.xlsx` (161 senior-professional Big Five personality records labelled with a high/low career success classification)

Rather than forcing illegitimate row-level joins across datasets that share no individual-level identifier—which would introduce catastrophic ecological fallacies and leakage—the engine employs four **context-isolated evidence lanes** (Market Intelligence, Skill Intelligence, Junior Professional / JDS, and Senior Professional / SDS) governed by a persistent Evidence Registry.

To ensure empirical validity, all analytical choices are grounded in established labor economics, natural language processing, glassbox machine learning, and distribution-free uncertainty quantification. This document formalizes the ten foundational methodological references underpinning the project, detailing what each method provides, how it is implemented in our engine (or the precise empirical rationale for why an alternative was chosen), and its verified academic citation.

---

## 1. ESCO (European Skills, Competences, Qualifications and Occupations)

### What It Is
The **European Skills, Competences, Qualifications and Occupations (ESCO)** taxonomy is the European Commission's multilingual classification system (Directorate-General for Employment, Social Affairs and Inclusion). ESCO operates as a semantic web ontology structured on the Simple Knowledge Organization System (SKOS) standard, defining and categorizing approximately 3,008 occupations and 13,890 skill and competence concepts. Occupations are strictly mapped to the international standard classification of occupations (ISCO-08) across a four-level hierarchy.

ESCO organizes skills into a structured pillar distinguishing between *knowledge* (theoretical concepts, disciplines, tools) and *skills/competences* (practical abilities, work activities, transversal soft skills). Crucially, ESCO connects occupations to skills through explicit, bipartite relational links categorized as either "essential" (indispensable for the role) or "optional" (frequently demanded or context-dependent). Each concept includes unique persistent Uniform Resource Identifiers (URIs), canonical preferred labels, alternative synonyms, and multi-lingual translations.

### How We Use It in Our Project (or Why We Chose Not To)
In our architecture, ESCO was evaluated as an external ontological normalization layer to map unstructured, messy `key_skills` strings from `Analytics Jobs.csv` and job titles into standardized canonical skills and ISCO occupation codes. 

However, we **chose not to depend on a live or full offline ESCO ontology in the core deterministic pipeline**, for two methodological reasons documented in our Approach Note (Section 2.5 and Appendix F):
1. **Regional and Domain Coverage Mismatch:** ESCO is calibrated on the European labor market and public employment services (EURES). Our job-posting corpus reflects the Indian information technology and analytics market. An audit of technical tool names in Indian tech postings revealed severe out-of-vocabulary rates in ESCO for specialized modern data-stack libraries and local abbreviations (e.g., specific ETL tools, cloud data warehouse variants, SAS base macros). Reporting ESCO's coverage deficit is itself an empirical finding rather than a normalization solution.
2. **Deterministic, Offline Reproducibility:** Querying the live ESCO API or parsing the multi-gigabyte RDF/SKOS database creates heavyweight external dependencies incompatible with our sandboxed, offline competition requirements.

Instead, we designed a curated, 5-dimension canonical taxonomy (`big_data`, `maths_statistics`, `coding`, `ai_ml`, `dashboard_storytelling`) mapped directly to the five constructs measured in the JDS junior cohort. This mapping is evaluated against a 50-skill manually annotated gold standard (`src/nlp/nlp_benchmark.py`). ESCO remains our theoretical reference point for hierarchical skill-to-occupation structures.

### Citation
- **European Commission.** (2022). *ESCO: European Skills, Competences, Qualifications and Occupations* (Version 1.1/1.2). Directorate-General for Employment, Social Affairs and Inclusion. Brussels: Publications Office of the European Union.  
  URL: [https://esco.ec.europa.eu/](https://esco.ec.europa.eu/)

---

## 2. O*NET (Occupational Information Network)

### What It Is
The **Occupational Information Network (O\*NET)** is the primary occupational database and taxonomy for the United States economy, developed by the National Center for O\*NET Development under the sponsorship of the U.S. Department of Labor / Employment and Training Administration (USDOL/ETA). O\*NET provides an empirical framework structured around the **O\*NET Content Model**, which dissects occupations along six major conceptual domains:
- *Worker Characteristics:* Enduring human attributes, including cognitive/psychomotor abilities, occupational interests, work values, and work styles (personality traits).
- *Worker Requirements:* Developed capacities, including basic skills, cross-functional skills, and formal knowledge domains.
- *Experience Requirements:* Practical training, work experience, and credentialing.
- *Occupational Requirements:* Generalized Work Activities (GWAs), detailed work activities, and physical/organizational context.
- *Workforce Characteristics:* Labor market data, employment projections, and wage information.
- *Occupation-Specific Information:* Granular tasks and technology tools.

Occupations are aligned with the federal Standard Occupational Classification (SOC) system. Unlike purely taxonomic ontologies, O\*NET collects continuous survey data from incumbent workers and occupational analysts, publishing quantitative ratings of **Importance**, **Level**, and **Frequency** on standardized 1–5 and 1–7 Likert scales for every skill, ability, and work style across more than 900 occupations.

### How We Use It in Our Project (or Why We Chose Not To)
O\*NET provides the theoretical blueprint for our multidimensional assessment of workforce performance. Specifically, the SDS dataset measures senior professional performance using the Five-Factor Model of personality (Neuroticism, Extraversion, Openness, Agreeableness, Conscientiousness), which directly parallels O\*NET’s "Work Styles" domain. Meanwhile, the JDS dataset captures applied technical capabilities that mirror O\*NET’s "Worker Requirements."

However, we **strictly reject row-level merging or imputation of external O\*NET numeric ratings into our raw data files**. Joining O\*NET scores to our job postings or junior/senior cohorts based on loose job-title matching would violate our strict *Leakage Audit Rule* (Table 11: *DO NOT join datasets that share no individual-level identifier*). Because our datasets stem from distinct regional and corporate contexts with unlinked subjects, attaching US national average scores would induce false-precision ecological bias. We use O\*NET exclusively as an independent theoretical validation benchmark to cross-reference whether the skill dimensions and personality traits that emerge as important in our models match empirical patterns documented in the wider industrial-organizational psychology literature.

### Citation
- **Peterson, N. G., Mumford, M. D., Borman, W. C., Jeanneret, P. R., Fleishman, E. A., Levin, K. Y., Campany, M. A., & Dye, C. F.** (2001). Understanding work using the Occupational Information Network (O\*NET): Implications for practice and research. *Personnel Psychology*, 54(2), 451–492.  
  DOI: [10.1111/j.1744-6570.2001.tb00097.x](https://doi.org/10.1111/j.1744-6570.2001.tb00097.x)
- **National Center for O\*NET Development.** (2024). *The O\*NET Database*. U.S. Department of Labor, Employment and Training Administration.  
  URL: [https://www.onetcenter.org/database.html](https://www.onetcenter.org/database.html)

---

## 3. CareerBERT

### What It Is
**CareerBERT** is a domain-adapted natural language processing model and representation architecture developed by Julian Rosenberger, Lukas Wolfrum, Sven Weinzierl, Mathias Kraus, and Patrick Zschech (published in *Expert Systems with Applications*, 2025). The model addresses the vocabulary gap and semantic divergence between candidate resumes, informal job advertisements, and standardized occupational taxonomies.

Built upon a Sentence-BERT (SBERT) transformer architecture, CareerBERT maps job vacancy descriptions and unstructured CV texts into a shared high-dimensional embedding space alongside ESCO/EURES occupational definitions. By fine-tuning transformer weights using contrastive metric learning on millions of occupational descriptions and resume pairs, CareerBERT optimizes cosine similarity such that equivalent career pathways cluster together regardless of lexical variations, spelling differences, or regional phrasing.

### How We Use It in Our Project (or Why We Chose Not To)
In our NLP pipeline benchmarking (`src/nlp/nlp_benchmark.py`), we evaluated candidate methods across a four-tiered hierarchy of representational complexity:
- Level 1: Deterministic dictionary and exact regex keyword matching.
- Level 2: TF-IDF vectorization with cosine similarity scoring.
- Level 3: Character and sub-word n-gram overlap matching.
- Level 4: Dense deep transformer embeddings (such as CareerBERT or Sentence-BERT).

We **chose not to incorporate CareerBERT into the production execution pipeline**. First, CareerBERT introduces heavyweight PyTorch/HuggingFace model checkpoints (>400 MB) requiring substantial GPU resources or high CPU latency, making it unsuitable for deterministic, offline, low-overhead pipeline execution within competition time limits. Second, our empirical benchmark against a 50-skill human-annotated gold standard demonstrated that a curated deterministic n-gram and regex matcher achieved sufficient precision (>80%) for mapping Indian analytics job skills onto our five target dimensions, with zero hallucination risk, instantaneous throughput, and complete rule audibility. CareerBERT is retained in our research documentation as the gold-standard dense-embedding candidate for future web-scale production deployments.

### Citation
- **Rosenberger, J., Wolfrum, L., Weinzierl, S., Kraus, M., & Zschech, P.** (2025). CareerBERT: Matching resumes to ESCO jobs in a shared embedding space for generic job recommendations. *Expert Systems with Applications*, 275, Article 127043.  
  DOI: [10.1016/j.eswa.2024.127043](https://doi.org/10.1016/j.eswa.2024.127043)  
  Preprint: *arXiv:2407.13511* [cs.CL].  
  Repository: [https://github.com/julianrosenberger/careerbert](https://github.com/julianrosenberger/careerbert)

---

## 4. ESCO Skill Extractor (ESCOX)

### What It Is
The **ESCO Skill Extractor** (introduced academically as **ESCOX**) is an open-source, AI-driven entity extraction and classification framework developed by researchers at the DataLab, School of Informatics, Aristotle University of Thessaloniki (AUTH) (Dimitrios Christos Kavargyris, Konstantinos Petrakis, Eleanna Papaioannou, Konstantinos Georgiou, Nikolaos Mittas, and Lefteris Angelis) as part of the European Union’s Horizon Europe SKILLAB research project.

ESCOX automatically extracts skills, competences, and occupational titles from unstructured documents (job descriptions, syllabi, CVs) and maps them to canonical ESCO URIs and ISCO-08 occupational codes. The architecture combines Large Language Models (LLMs) for boundary detection and contextual entity extraction with dense sentence embeddings (using models like `all-MiniLM-L6-v2`) to perform semantic vector search against pre-indexed ESCO vectors. The package provides both an open Python library (`pip install esco-skill-extractor`) and a no-code visual interface for labor-market researchers.

### How We Use It in Our Project (or Why We Chose Not To)
We evaluated the ESCO Skill Extractor as an automated pipeline component for parsing the free-text `job_description` and `key_skills` fields in `Analytics Jobs.csv`. 

We **chose not to deploy it in our automated processing loop** for two explicit operational reasons:
1. **Network Egress and Hardware Constraints:** ESCOX relies on downloading transformer checkpoints and accessing pre-built vector indices. In our target offline evaluation environment, dependencies requiring unpinned network downloads or external inference calls are disabled.
2. **Domain-Specific Noise in Indian IT Job Postings:** In `Analytics Jobs.csv`, the `key_skills` column contains idiosyncratic concatenation patterns (e.g., `"java, sql, python, big data | spark, hadoop - hyderabad"`). Automated European LLM/embedding extractors struggle with location bleed, combined acronyms, and non-standard syntax, often producing false-positive mappings to obscure agricultural or industrial ESCO concepts.

Consequently, we built a custom, deterministic, rule-based normalizer (`src/skill_intelligence/skill_engine.py`) featuring explicit punctuation scrubbing, custom delimiter splitting, alias lookups, and conservative thresholding, guaranteeing full auditability in our Cleaning Ledger (`cleaning_ledger.json`).

### Citation
- **Kavargyris, D. C., Petrakis, K., Papaioannou, E., Georgiou, K., Mittas, N., & Angelis, L.** (2025). ESCOX: A tool for skill and occupation extraction using LLMs from unstructured text. *Software Impacts*, 23, Article 100725.  
  DOI: [10.1016/j.simpa.2024.100725](https://doi.org/10.1016/j.simpa.2024.100725)  
  Repository: [https://github.com/KonstantinosPetrakis/esco-skill-extractor](https://github.com/KonstantinosPetrakis/esco-skill-extractor) (DataLab-AUTH).

---

## 5. SHAP (SHapley Additive exPlanations)

### What It Is
**SHAP (SHapley Additive exPlanations)** is a foundational framework for explaining the output of complex predictive machine learning models, introduced by Scott M. Lundberg and Su-In Lee (NeurIPS 2017). Grounded in cooperative game theory (Shapley, 1953), SHAP reframes feature attribution as a game where feature values act as players cooperating to generate the prediction (the payout).

SHAP is the unique attribution method that simultaneously satisfies four desirable mathematical axioms:
1. *Local Accuracy (Efficiency):* The sum of feature attributions equals the difference between the model's prediction and the base expected outcome: $f(x) = \phi_0 + \sum_{i=1}^M \phi_i(x)$.
2. *Missingness:* If a feature is absent from a coalition, its attribution is zero ($\phi_i(x) = 0$ when $x'_i = 0$).
3. *Consistency (Monotonicity):* If a model changes such that the marginal contribution of a feature increases or stays the same regardless of other features, that feature's attribution cannot decrease.
4. *Additivity:* For an ensemble of models, the overall attribution is the sum of the individual models' attributions.

The development of **TreeSHAP** (Lundberg et al., *Nature Machine Intelligence*, 2020) enabled the exact calculation of Shapley values for tree-based ensemble models (XGBoost, LightGBM, CatBoost, Random Forest) in polynomial time $O(TLD^2)$ rather than exponential time $O(TL2^M)$, where $T$ is the number of trees, $L$ is the number of leaves, and $D$ is tree depth.

### How We Use It in Our Project (or Why We Chose Not To)
We **actively use SHAP** in our explainability module (`src/explainability/explainer.py`). For our benchmark gradient boosted trees (e.g., XGBoost models fit on JDS junior skills and SDS senior personality traits), we compute exact TreeSHAP values and generate global summary bee-swarm plots (`reports/figures/shap_summary_jds.png` and `reports/figures/shap_summary_sds.png`).

However, we establish strict **auditing guardrails** around SHAP interpretation (Approach Note Section 4.7):
- *Triangulation Requirement:* No feature is declared important based on SHAP alone. We enforce a four-way triangulation protocol requiring that (1) SHAP values, (2) sealed-fold permutation importance, (3) EBM shape functions, and (4) Firth linear regression coefficients agree in sign and approximate relative rank.
- *Auditor Rule A3 (Non-Causal Language):* SHAP attributions are strictly documented as *additive statistical contributions to the model’s estimate of the observed class within this sample*, never as the causal effect of changing an applicant's personality or skill score.

### Citation
- **Lundberg, S. M., & Lee, S.-I.** (2017). A unified approach to interpreting model predictions. In *Advances in Neural Information Processing Systems (NeurIPS 2017)*, 30, 4765–4774.
- **Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin, J. M., Nair, B., Katz, R., Himmelfarb, J., Bansal, N., & Lee, S.-I.** (2020). From local explanations to global understanding with explainable AI for trees. *Nature Machine Intelligence*, 2(1), 56–67.  
  DOI: [10.1038/s42256-019-0138-9](https://doi.org/10.1038/s42256-019-0138-9)

---

## 6. scikit-learn Probability Calibration (Platt Scaling vs. Isotonic Regression)

### What It Is
Probability calibration in machine learning addresses the discrepancy between a classifier's raw discriminant score and the true empirical probability of the target class: a model is calibrated if among samples assigned predicted probability $\hat{p}$, the true proportion of positive instances is approximately $\hat{p}$ ($P(Y=1 \mid \hat{P}=p) \approx p$). Standard classification models—especially Support Vector Machines, Naive Bayes, and Gradient Boosted Decision Trees—frequently produce poorly calibrated probabilities due to margin maximization, feature independence assumptions, or log-loss minimization that drives scores toward 0 and 1.

The `sklearn.calibration` module implements two post-processing calibration algorithms via `CalibratedClassifierCV`:
1. **Platt Scaling (Sigmoid Method; Platt, 1999):** Fits a univariate two-parameter logistic regression model mapping raw decision scores $f(x)$ to posterior probabilities:
   $$P(Y=1 \mid f) = \frac{1}{1 + \exp(A \cdot f + B)}$$
   Parameters $A$ and $B$ are estimated via maximum likelihood on a holdout calibration set. Because it estimates only two parameters, Platt scaling is smooth, well-regularized, and resistant to overfitting on small validation samples.
2. **Isotonic Regression (Zadrozny & Elkan, 2001, 2002):** Fits a non-parametric, piece-wise constant monotonic increasing function using the Pool Adjacent Violators Algorithm (PAVA). While it can correct arbitrary non-linear distortions without assuming a sigmoid shape, it is completely unconstrained between step intervals and requires substantial calibration sample sizes ($n > 1,000$) to avoid severe step-wise overfitting.

Model calibration quality is evaluated quantitatively via the Brier score loss and the Expected Calibration Error (ECE), visualized using reliability diagrams (`CalibrationDisplay`).

### How We Use It in Our Project (or Why We Chose Not To)
In our benchmarking and calibration engine (`src/calibration/calibrator.py` and `src/models/benchmark_engine.py`), we track Brier score and ECE across all models.

We make a deliberate methodological choice regarding calibration algorithms:
- **We USE Platt Scaling (`method='sigmoid'`):** We fit Platt scaling exclusively within inner cross-validation folds to calibrate tree and ensemble predictions. Reliability diagrams are generated with bootstrap confidence bands across 5 bins (`reports/figures/calibration_jds.png` and `reports/figures/calibration_sds.png`).
- **We EXPLICITLY DROP Isotonic Regression:** As formalized in Section 4.6 of our Approach Note: *"Probabilities are compared uncalibrated and Platt-calibrated; isotonic regression is not used because it overfits at these sample sizes."* With total cohort sizes of $n=139$ (JDS) and $n=161$ (SDS), an outer test or inner validation fold contains only 20 to 35 observations. Fitting a non-parametric PAVA step function on 30 points results in extreme discretization artifacts and sample memorization.

### Citation
- **Platt, J. C.** (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. In A. J. Smola, P. J. Bartlett, B. Schölkopf, & D. Schuurmans (Eds.), *Advances in Large Margin Classifiers* (pp. 61–74). MIT Press.
- **Zadrozny, B., & Elkan, C.** (2001). Obtaining calibrated probability estimates from decision trees and naive Bayesian classifiers. In *Proceedings of the Eighteenth International Conference on Machine Learning (ICML '01)* (pp. 609–616). Morgan Kaufmann.
- **Zadrozny, B., & Elkan, C.** (2002). Transforming classifier scores into accurate multiclass probability estimates. In *Proceedings of the Eighth ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '02)* (pp. 694–699).  
  DOI: [10.1145/775047.775151](https://doi.org/10.1145/775047.775151)
- **Pedregosa, F., et al.** (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.

---

## 7. Deming & Kahn — Cognitive-Social Skill Complementarity in Job Postings

### What It Is
The foundational economics research by **David Deming (Harvard University)** and **Lisa B. Kahn (University of Rochester)**—published in the *Journal of Labor Economics* (2018) and circulated as NBER Working Paper No. 23328 (2017)—provides the core empirical demonstration of skill requirements and wage determination across professional labor markets.

Using large-scale vacancy data from Burning Glass Technologies, Deming and Kahn decomposed job advertisement requirements into ten general skill clusters, specifically focusing on cognitive skills (analytical reasoning, mathematics, statistics, computer software) and social skills (collaboration, communication, client relations). Their principal finding is the existence of **cognitive-social skill complementarity**:
1. Within narrowly defined occupations, firms exhibit massive heterogeneity in the specific combinations of skills demanded.
2. Cognitive skills and social skills are not merely independent additive inputs; their positive interaction is strongly associated with higher advertised compensation and superior firm-level performance. That is, the wage return to cognitive skills is significantly amplified when paired with high communication demands, and vice-versa.

### How We Use It in Our Project (or Why We Chose Not To)
Deming and Kahn’s complementarity thesis serves as the **single organizing hypothesis** across the entire Workforce Intelligence Engine (Approach Note Executive Summary and Section 1). 

Rather than chasing spurious prediction scores on disconnected files, we formulate a unified hypothesis tested independently across three evidence lanes:
1. **Market Lane:** We evaluate whether job postings requiring technical/cognitive capabilities (`coding`, `maths_statistics`, `ai_ml`) paired with `dashboard_storytelling` demand a super-additive wage premium in advertised LPA salaries.
2. **Junior Professional Lane (JDS):** We explicitly test Hypothesis H4: that `dashboard_and_storytelling_skills` and `maths-stats_skills` act as complements in predicting junior salary hikes, estimated via an interaction logistic regression model compared against an additive baseline using likelihood-ratio tests and 2,000 bootstrap iterations.
3. **Senior Professional Lane (SDS):** We test whether social/interpersonal traits (Extraversion, Agreeableness) interact with Conscientiousness in separating executive success classifications.

By grounding our project in Deming and Kahn, agreement across our unjoined datasets provides robust triangulation of economic labor principles without risking false row linkage.

### Citation
- **Deming, D., & Kahn, L. B.** (2018). Skill requirements across firms and labor markets: Evidence from job postings for professionals. *Journal of Labor Economics*, 36(S1), S337–S369.  
  DOI: [10.1086/694106](https://doi.org/10.1086/694106)  
  (Preprint: National Bureau of Economic Research Working Paper No. 23328, 2017. DOI: [10.3386/w23328](https://doi.org/10.3386/w23328)).

---

## 8. Firth Logistic Regression — Bias Reduction for Small Samples

### What It Is
**Firth Logistic Regression** is a penalized maximum likelihood estimation procedure developed by David Firth in *Biometrika* (1993). In standard maximum likelihood estimation (MLE) of generalized linear models, parameter estimates are consistent asymptotically but suffer from first-order small-sample bias of order $O(n^{-1})$.

More critically, standard logistic regression breaks down completely when data exhibit **complete separation** or **quasi-complete separation**—a common occurrence in small samples where a predictor or combination of predictors highly predicts the binary outcome. In separated data, standard MLE fails to converge: parameter estimates diverge toward $\pm \infty$, the log-likelihood plateaus, and Wald tests produce invalid, artificially inflated standard errors.

Firth solved this fundamental defect by penalizing the log-likelihood function using the Jeffreys invariant prior:
$$L^*(\beta) = L(\beta) \cdot |I(\beta)|^{1/2}$$
where $|I(\beta)|$ is the determinant of the Fisher information matrix. By modifying the score estimating function, Firth's penalized likelihood removes the leading $O(n^{-1})$ bias term from the parameter estimates. Mathematically, it guarantees finite, bounded parameter estimates and well-behaved profile-penalized likelihood confidence intervals, even in the presence of complete separation (Heinze & Schemper, 2002).

### How We Use It in Our Project (or Why We Chose Not To)
We **actively use Firth Logistic Regression** as our primary statistical estimator for evaluating interaction effects in small-sample cohorts (Approach Note Appendix C & Section 4.3).

With $n=139$ in JDS and $n=161$ in SDS, evaluating multi-term models (e.g., five main skill effects plus interaction terms like `maths-stats × storytelling`) quickly leads to sparse cells and near-complete separation. Standard unregularized logistic regression yields unstable odds-ratio estimates and misleads hypothesis tests. By implementing Firth’s penalized logit:
- We obtain bias-reduced log-odds estimates with finite confidence bounds.
- We perform penalized likelihood-ratio tests (LRT) to rigorously evaluate whether the interaction term significantly improves fit over the additive model.
- We report minimum detectable effect sizes (MDE) at 80% power, ensuring that non-significant findings are honestly reported as sample-size power limitations rather than definitive absence of an effect.

### Citation
- **Firth, D.** (1993). Bias reduction of maximum likelihood estimates. *Biometrika*, 80(1), 27–38.  
  DOI: [10.1093/biomet/80.1.27](https://doi.org/10.1093/biomet/80.1.27)
- **Heinze, G., & Schemper, M.** (2002). A solution to the problem of separation in logistic regression. *Statistics in Medicine*, 21(16), 2409–2419.  
  DOI: [10.1002/sim.1047](https://doi.org/10.1002/sim.1047)

---

## 9. Explainable Boosting Machine (EBM) from InterpretML

### What It Is
The **Explainable Boosting Machine (EBM)** is an interpretable "glassbox" machine learning model developed by Harsha Nori, Rich Caruana, Samuel Jenkins, Paul Koch, and Yin Lou at Microsoft Research, distributed within the open-source **InterpretML** library (Nori et al., 2019). EBM modernizes Generalized Additive Models with Pairwise Interactions ($GA^2M$; Lou et al., 2012, 2013), taking the mathematical form:
$$g(E[y]) = \beta_0 + \sum_{i=1}^M f_i(x_i) + \sum_{i \neq j} f_{ij}(x_i, x_j)$$
where $g(\cdot)$ is the link function (logit for binary classification), $f_i$ are univariate non-linear shape functions, and $f_{ij}$ are bivariate interaction surfaces.

EBM resolves the historic trade-off between predictive accuracy and interpretability. Unlike standard tree ensembles (Random Forest, XGBoost) that build deep multivariate trees that tangle feature dependencies, EBM trains shallow trees in a round-robin cyclic fashion on one feature at a time using a very low learning rate. Because each tree split is confined to a single feature, the cumulative learned component $f_i(x_i)$ can be extracted as an exact lookup table. Significant pairwise interactions ($f_{ij}$) are selectively identified via the FAST interaction search algorithm. The model matches the predictive performance of state-of-the-art gradient boosting while remaining completely transparent: practitioners can visualize the exact 1D shape curves and 2D heatmaps without relying on post-hoc approximation algorithms.

### How We Use It in Our Project (or Why We Chose Not To)
We **actively use EBM** in our model benchmarking and explainability suites (Approach Note Section 2, Section 4.4, and Figure Slots F17/F18).

EBM serves three vital functions in our architecture:
1. **Curvilinear Trait Auditing in SDS:** In behavioral economics and organizational psychology, high conscientiousness or extraversion often exhibits curvilinear or plateauing relationships with job performance (Carter et al., 2014; Le et al., 2011). Because linear models force monotonic effects, we use EBM univariate shape curves ($f_i$) with bagged confidence intervals to inspect whether senior success plateaus or declines at extreme trait levels.
2. **Transparent Validation of Interaction Hypotheses:** EBM’s explicit interaction surfaces ($f_{ij}$) allow us to directly visualize the `maths-stats × storytelling` interaction (JDS) and `conscientiousness × openness` interaction (SDS) as 2D probability heatmaps, with the data's convex hull overlaid to prevent reading extrapolation artifacts.
3. **Forensic Triangulation:** EBM provides an independent glassbox benchmark against which our XGBoost, Random Forest, and Firth logistic regression models are validated.

### Citation
- **Nori, H., Jenkins, S., Koch, P., & Caruana, R.** (2019). InterpretML: A unified framework for machine learning interpretability. *arXiv preprint arXiv:1909.09223* [cs.LG].
- **Lou, Y., Caruana, R., & Gehrke, J.** (2012). Intelligible models for classification and regression. In *Proceedings of the 18th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '12)* (pp. 150–158).  
  DOI: [10.1145/2339530.2339556](https://doi.org/10.1145/2339530.2339556)
- **Lou, Y., Caruana, R., Gehrke, J., & Hooker, G.** (2013). Accurate intelligible models with pairwise interactions. In *Proceedings of the 19th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '13)* (pp. 623–631).  
  DOI: [10.1145/2487575.2487579](https://doi.org/10.1145/2487575.2487579)

---

## 10. Conformal Prediction

### What It Is
**Conformal Prediction** is a distribution-free, model-agnostic statistical framework for predictive uncertainty quantification, pioneered by Vladimir Vovk, Alex Gammerman, and Glenn Shafer (*Algorithmic Learning in a Random World*, 2005) and recently unified for practical machine learning by Anastasios N. Angelopoulos and Stephen Bates (2021, 2023).

Unlike conventional machine learning approaches that output point predictions or heuristic probability scores, conformal prediction converts point predictors into **prediction sets** (in classification) or **prediction intervals** (in regression) with rigorous, finite-sample statistical guarantees. Under the sole assumption that data points are exchangeable (satisfied whenever observations are independent and identically distributed), split conformal prediction guarantees that the true label $Y_{n+1}$ falls within the predicted set $C(X_{n+1})$ with user-defined coverage probability $1 - \alpha$:
$$P\left(Y_{n+1} \in C(X_{n+1})\right) \ge 1 - \alpha$$
The method functions by computing non-conformity scores (e.g., $s_i = 1 - \hat{f}(x_i)_{y_i}$) on a held-out calibration dataset, calculating the empirical $(1 - \alpha)(1 + 1/n_{cal})$-th quantile $\hat{q}$, and constructing prediction sets containing all candidate classes whose non-conformity score does not exceed $\hat{q}$.

### How We Use It in Our Project (or Why We Chose Not To)
We **actively use Split-Conformal Prediction** as our primary per-candidate uncertainty quantification mechanism (Approach Note Section 4.6 and Figure Slot F16).

In human resources and career mobility decisions, forcing a rigid binary classification ({High} vs. {Low}) is irresponsible when predictions carry high uncertainty. We calibrate conformal prediction sets at error level $\alpha = 0.10$ (guaranteeing 90% marginal coverage):
- When a candidate's conformal prediction set is a singleton (`{High}` or `{Low}`), the model is confident in the directional outcome.
- When a candidate’s prediction set is empty ($\emptyset$), the candidate’s profile is anomalous relative to the training distribution.
- When the prediction set contains both outcomes (`{High, Low}`), the model formally **abstains**, signaling high epistemic ambiguity and indicating that the profile should be routed to human review rather than subjected to automated algorithmic screening.

Given our small cohort sizes ($n=139$ and $n=161$), we report empirical coverage across repeated cross-validation folds alongside set-size distribution histograms, transparently displaying the sampling variance of the coverage guarantee.

### Citation
- **Angelopoulos, A. N., & Bates, S.** (2023). A gentle introduction to conformal prediction and distribution-free uncertainty quantification. *Foundations and Trends in Machine Learning*, 16(4), 494–591.  
  DOI: [10.1561/2200000101](https://doi.org/10.1561/2200000101)  
  (Preprint: *arXiv:2107.07511* [cs.LG], 2021).
- **Vovk, V., Gammerman, A., & Shafer, G.** (2005). *Algorithmic Learning in a Random World*. New York: Springer.  
  DOI: [10.1007/b106715](https://doi.org/10.1007/b106715)

---

## 11. Methodological Decision Matrix & Summary

The following table summarizes the operational status and role of each investigated reference across the Workforce Intelligence Engine codebase:

| Ref # | Construct / Framework | Methodological Domain | Status in Project | Implementation Rationale / Decision Justification |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **ESCO** | Skill Ontology | **Reference Only** (Dropped from runtime) | Regional vocab mismatch for Indian IT postings; heavy runtime overhead. Used as reference for skill-occupation hierarchy. |
| **2** | **O\*NET** | Occupational Model | **Reference Only** (No row-level join) | Conceptual blueprint for skill/personality domains. Row-level joins rejected to prevent leakage and ecological fallacy. |
| **3** | **CareerBERT** | Deep Job NLP | **Benchmarked / Dropped** | Heavy transformer weights incompatible with offline requirements. Replaced by fast, deterministic n-gram matching. |
| **4** | **ESCO Skill Extractor** | Automated NLP Tool | **Evaluated / Dropped** | External network dependencies and vocabulary mismatch. Replaced by audited regex normalizer and Cleaning Ledger. |
| **5** | **SHAP (TreeSHAP)** | ML Explainability | **Adopted** (`src/explainability`) | Local and global attribution for XGBoost. Must triangulate with permutation importance, EBM shapes, and Firth coefficients. |
| **6** | **scikit-learn Calibration** | Probability Calibration | **Adopted (Platt) / Dropped (Isotonic)** | Platt scaling adopted for regularized calibration. Isotonic regression explicitly dropped due to severe overfitting at $n \approx 150$. |
| **7** | **Deming & Kahn** | Labor Economics | **Core Organizing Hypothesis** | Theoretical foundation: cognitive-social skill complementarity tested independently across Market, Junior, and Senior lanes. |
| **8** | **Firth Logistic Reg.** | Small-Sample Statistics | **Adopted** (`src/models`) | Eliminates small-sample bias and solves quasi-complete separation in JDS/SDS interaction hypothesis testing. |
| **9** | **EBM (InterpretML)** | Glassbox Generalized Additive Models | **Adopted** (`src/models`) | Detects non-linear trait plateaus in SDS and provides transparent 2D interaction surfaces for Deming-Kahn hypotheses. |
| **10** | **Conformal Prediction** | Uncertainty Quantification | **Adopted** (`src/calibration`) | Generates 90% guaranteed prediction sets ($\alpha=0.10$), allowing automated abstention on ambiguous HR profiles. |
