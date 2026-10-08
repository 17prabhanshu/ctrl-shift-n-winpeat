# WORKFORCE INTELLIGENCE ENGINE - FINAL APPROACH NOTE

**Does the market pay for what progression rewards?**  
A boundary-preserving audit of demand, skills and career success in data-science work

**Team ctrl shift n | SAS CU Hackathon 2026 | Round 2 Approach Note**

---

## Executive Summary

### The Problem
The organizers supply four unlinked files and no prediction target: 1,602 and 15,841 job-posting rows, 139 junior-professional skill records labelled with a high or low salary hike, and 161 senior-professional Big Five records labelled with a high or low success class.

Our first task was to decide what question these files can answer defensibly. We ask whether what the market pays for, what early-career progression rewards, and what separates observed senior success point in the same direction, without joining rows that share no identifier.

### One Hypothesis, Tested Three Times
From the labour-economics literature we take a single organising hypothesis: **technical skill and communication or social skill are complements**. Deming and Kahn report a cognitive-social complementarity in pay and firm performance using job postings. We test that pattern independently in postings (advertised salary), in JDS (hike label) and in SDS (trait interactions with the success label).

**Agreement across independent files is stronger evidence than any one model score. Disagreement is equally reportable.**

### System
Four context-isolated evidence lanes (Market, Skill, Junior, Senior) write to a persistent Evidence Registry. An auditor rejects any claim that lacks dataset, method, metric, interval and limitation, and flags causal wording. The lanes meet at one construct only: the five skill dimensions that JDS already measures, onto which we map posting skills with a curated taxonomy scored against a hand-labelled gold set.

The design borrows the context isolation and shared knowledge hub of FIRMHIVE's Tree of Agents, but every node is a deterministic analysis worker and no language model sits on the path that produces a number.

### Validation
Models are scored with nested, repeated, stratified cross-validation (20 repeats of 5 outer folds), with no oversampling, shuffled-target null distributions, calibration and conformal coverage reported with intervals, and an ablation for every component.

### Key Findings

| Hypothesis | Verdict | Key Result |
|------------|---------|------------|
| **H1**: Role families differ in salary | ✅ **SUPPORTED** | ε² = 0.35 (large); Data Scientists ₹16.2L vs Software Engineers ₹10.9L |
| **H2**: Skills are role-specific | ✅ **SUPPORTED** | 79,880 skill mentions mapped; distinct role-skill patterns |
| **H3**: Technical×Communication complementarity in salary | ⚠️ **NOT SIGNIFICANT** | Interaction coef = 0.084, 95% CI [-0.014, 0.181]; CI includes zero |
| **H4**: Same complementarity in JDS hike | ⚠️ **NOT SUPPORTED** | LRT p = 0.093; Bootstrap CI [-6.12, 0.21] includes zero |
| **H5**: SDS trait-success is non-additive | ❌ **INVALIDATED** | Depth-2 tree AUC = 0.917; labels are near-deterministic function of inputs |

**Not claimed**: causation, individual-level prediction, time trends, or any person-level link across files.

---

## 1. Problem Definition and Analytics Objective

### 1.1 The Brief and What It Leaves Open
The brief names three themes (data-science jobs, skills, personality) and invites data management, visualisation, pattern identification, statistical analysis and data mining. It warns that the data may contain public and self-reported entries, masked values, misspellings, mistyped entries and outliers, and that personality traits are normalised. It also states that everything depends on the problem identified.

We therefore treated problem formulation as a technical deliverable and scored four candidate formulations against what the files can support.

### 1.2 Selected Problem
Let M be posting-level market evidence (salary, experience, role, company, location), K the skill content of postings, J = {(x_i, y_i)} the junior records with five skill scores x_i on a 1 to 5 scale and hike label y_i, and S = {(z_j, t_j)} the senior records with five normalised traits z_j and success label t_j.

No identifier links M, K, J and S. The analytics objective is to estimate, with uncertainty and without a row-level join:
1. The role-conditional structure of demand and salary in M and K
2. The association between each skill dimension and y in J
3. The functional form (additive, quadratic or interactive) of the association between traits and t in S
4. Whether a technical-by-communication complementarity appears in all three

**Headline question**: Where the market pays a premium for technical skill, does it pay more when that skill is paired with communication skill, and do the junior and senior files show the same pattern?

### 1.3 Objectives
- **O1. Audit**: Produce reproducible clean tables for all four files, with a ledger recording the original state, transformation, reason and affected rows for every change.
- **O2. Normalise skills**: Map free-text posting skills to a curated taxonomy of ~300 canonical skills and five JDS-aligned dimensions.
- **O3. Market structure**: Test H1 to H3 on the posting files with effect sizes and false-discovery control.
- **O4. Talent structure**: Estimate JDS and SDS associations under nested repeated cross-validation, comparing additive and non-additive models.
- **O5. Governance**: Register every headline claim with provenance, and publish the interpretation rule for each outcome pattern before the final run.

### 1.4 Hypotheses

| ID | Statement | Data | Test | Falsified if |
|----|-----------|------|------|--------------|
| H1 | Role families differ in demand and salary profiles | DataScience Jobs | Kruskal-Wallis on log salary by role family, ε², Dunn with Holm; mixed model with company random intercept | Role effect interval includes 0 after the company term |
| H2 | Skill requirements are role-specific, not uniform | Analytics Jobs | Log-odds ratio with informative Dirichlet prior per skill and role; 1,000 role-label permutations; FDR q < 0.05 | Count of specific skills is within the permutation null |
| H3 | Technical-by-communication complementarity in advertised salary | Analytics Jobs | log salary ~ role + experience + T + C + T×C, robust SE; quantile regression at 0.25, 0.5, 0.75 | Interaction interval includes 0 and sign is unstable across quantiles |
| H4 | The same complementarity in the junior hike label | JDS | Logistic, storytelling × maths-statistics versus additive, likelihood-ratio test; bootstrap; power simulation | LRT p ≥ 0.05 with interval including 0 (report minimum detectable effect) |
| H5 | Trait-success association in SDS is non-additive | SDS | Additive logistic versus quadratic and pairwise logistic, EBM, depth-3 tree; nested repeated CV; corrected resampled t-test | No non-additive model beats additive with a ΔAUC interval excluding 0 |

### 1.5 Scope and Non-Goals
The study is observational. We do not estimate causal effects, produce individual-level predictions or recommendations, infer time trends (the posting files do not provide the temporal granularity for them), or link rows across files.

---

## 2. Analytical Approach

### 2.1 Evidence Classes and the No-False-Join Rule
Every table and figure carries one of three tags:
- **Observed (O)**: computed from the supplied rows
- **External (E)**: taxonomy or prior knowledge, never allowed to alter observed rows
- **Model-derived (M)**: an estimate, prediction or explanation

Because no person or posting identifier spans the files, the datasets meet only at shared constructs (role family, skill dimension, seniority), never at rows. An alignment claim may state that a dimension has demand share a in postings and association b with the JDS label; it may not state that the skill causes promotion.

### 2.2 Architecture
The pipeline has four evidence lanes running in isolation:
- **M1 Market**: DataScience Jobs, Analytics Jobs → H1 estimates, Career Opportunity Frontier
- **M2 Skill**: Analytics Jobs text + taxonomy → Canonical skills, role specificity, graph, Signal Index, H2 and H3
- **M3 Junior**: JDS only → H4, benchmark, calibration, explanations
- **M4 Senior**: SDS only → H5, forensics, benchmark, explanations

Each lane reads only its own cleaned tables and writes only to the registry. The lanes never share intermediate objects, which is how leakage between files is prevented by construction.

### 2.3 The Construct Bridge
JDS records five skill dimensions: big data, mathematics and statistics, coding, AI and machine learning, and dashboard and storytelling. We map every canonical skill extracted from postings onto the same five, plus an explicit unmapped bucket.

This is the only quantity that crosses lanes, and it is the place the framework is most exposed. Two controls apply:
1. The mapping is scored against a hand-labelled gold set
2. Every ambiguous skill (SQL is the standard case) is reassigned at random in 1,000 draws to show how much any alignment estimate depends on the assignment

### 2.4 Validation Protocol
All supervised results use nested, repeated, stratified cross-validation:
- Preprocessing, tuning and calibration sit inside the training folds
- The sealed outer fold is touched only at prediction time
- 20 repeats of 5-fold rather than leave-one-out for model selection
- No oversampling (class prevalence ~52.5% vs 47.5%)
- Shuffled-target null distributions to check for leakage

### 2.5 Evidence Registry and Auditor
Every headline number is a registry record with: claim_id, statement, dataset, evidence_tag, method, metric, value, 95% interval, n, limitation, code_ref, status.

The auditor enforces six rules:
- **A1**: All fields present
- **A2**: Every numeric claim carries an interval or an exact n
- **A3**: Language lint rejects causal verbs and individual-outcome phrasing
- **A4**: Claim cites one lane's dataset unless it is typed alignment
- **A5**: Code reference resolves and a rerun reproduces the value
- **A6**: Evidence tag is present

---

## 3. Data Exploration and Preparation

### 3.1 Inventory

| File | Shape | Unit | Fields | Outcome |
|------|-------|------|--------|---------|
| DataScience Jobs.csv | 1,602 × 8 | Posting by company | reference_no, company_name, job_title, min_experience, avg_salary, min_salary, max_salary, num_of_jobs | None |
| Analytics Jobs.csv | 15,841 × 8 | Posting | s_no, experience, job_description, job_desig, job_type, key_skills, location, salary | None |
| JDS Skill Traits.xlsx | 139 × 7 | Junior professional | id; 5 skill scores (1-5); salary_hike_high_or_low | High (1) or Low (0) |
| SDS Personality Traits.xlsx | 161 × 7 | Senior professional | id; 5 trait scores (normalised); success_classification_high_low | High or Low |

### 3.2 Cleaning Summary

The cleaning pipeline processes all four files with full ledger tracking:

**DataScience Jobs:**
- Salary strings parsed from "7.8L" format → numeric INR (1,602 rows)
- Experience parsed to numeric (1,602 rows)
- Role categorization applied (7 role families)

**Analytics Jobs:**
- Salary ranges parsed from "6to10" format → min/max INR (15,841 rows)
- 75.8% job_type missing, 22.1% job_description missing (recorded, not imputed)
- 79,880 skill mentions tokenized and mapped
- Experience ranges parsed (15,841 rows)
- Role categorization applied (7 role families)

**JDS Skills:**
- 5 skill scores verified in 1-5 range
- Class balance: 52.5% high hike (73/139)

**SDS Personality:**
- 5 trait scores checked for normalization
- Class balance: 52.8% high success (85/161)
- **Forensic flag**: Traits show large differences by class (Cohen's d = 1.1-1.8)

### 3.3 Skill Taxonomy Mapping

We mapped 79,880 skill mentions to 10,336 canonical skills across 5 dimensions:

| Dimension | Count | Percentage |
|-----------|-------|------------|
| Coding | 12,116 | 15.2% |
| Big Data | 2,230 | 2.8% |
| Maths/Statistics | 2,030 | 2.5% |
| AI/ML | 1,931 | 2.4% |
| Dashboard/Storytelling | 1,859 | 2.3% |
| Unmapped (non-technical) | 59,714 | 74.8% |

**Key skills by dimension:**
- Coding: SQL (1,978), Java (1,154), Python (987)
- Big Data: Spark, Hadoop, Hive
- Maths/Stats: SAS (636), Statistics, R
- AI/ML: Machine Learning (770), Deep Learning, NLP
- Dashboard: Excel (693), Tableau, Power BI

### 3.4 Leakage Audit
All 8 leakage tests PASSED:
- LK1: No ID columns used as features
- LK2: No duplicate rows straddling folds
- LK3: Preprocessing inside training folds only
- LK4: No target-derived features
- LK5: Calibration data separate from scored folds
- LK6: Taxonomy built without outcome labels
- LK7: Shuffled-target AUC centred on 0.5
- LK8: Stacking on out-of-fold predictions only

---

## 4. Data Analysis

### 4.1 Market Structure (H1) ✅ SUPPORTED

**Kruskal-Wallis Test on Log Salary by Role Family:**
- H-statistic: 630.5
- p-value: < 0.001
- ε² (effect size): 0.35 (large)

**Post-hoc Pairwise Comparisons (Dunn's test with Bonferroni):**
All comparisons between technical roles (Data Scientist, Data Engineer, ML Engineer) and non-technical roles (Business Analyst, Other) are significant. Data Scientists earn ₹16.2L median vs Software Engineers ₹10.9L (Δ = +5.3L, p < 0.001).

**Company Variance:**
- Company variance share: 31.2% (material)
- Role differences survive company clustering

**Career Opportunity Frontier:**
- Data Scientists: High salary (₹16.2L), moderate demand (470 postings)
- Data Engineers: High salary (₹15.2L), moderate demand (408 postings)
- Software Engineers: Lower salary (₹10.9L), high demand (1,208 postings)

### 4.2 Skill Structure (H2) ✅ SUPPORTED

Skills show strong role-specificity:
- Data Scientists: Machine Learning, Python, R, Data Science
- Data Engineers: Hadoop, Spark, Big Data, Hive
- ML Engineers: Machine Learning, SAS, R, Python
- Data Analysts: Data Analysis, SQL, Excel
- Business Analysts: Business Analysis, SQL, Finance

**Skill Signal Index (SSI):**
Top skills by multi-component score (demand × specificity × compensation × breadth, 10,000 Dirichlet draws):
1. SQL - High demand, broad across roles
2. Python - High demand, strong in DS/ML roles
3. Java - High demand, strong in engineering roles
4. Machine Learning - Niche but high compensation association

### 4.3 Complementarity in Postings (H3) ⚠️ NOT SIGNIFICANT

**Interaction Model:** log_salary ~ experience + role + has_technical × has_communication

| Parameter | Coefficient | p-value | 95% CI |
|-----------|-------------|---------|--------|
| Technical (T) | 0.276 | < 0.001 | [0.221, 0.331] |
| Communication (C) | -0.074 | 0.005 | [-0.126, -0.022] |
| **T × C Interaction** | **0.084** | **0.092** | **[-0.014, 0.181]** |

**Interpretation:**
- Technical skills have strong positive main effect (p < 0.001)
- Communication skills have unexpected negative main effect (p = 0.005)
- **Interaction is NOT significant** (p = 0.092, CI includes zero)
- Quantile regression shows consistent non-significance across Q0.25, Q0.5, Q0.75

**Conclusion for H3:** We cannot claim significant technical-communication complementarity in advertised salary. The CI includes zero, and the sign is not stable.

### 4.4 Junior Lane (H4) ⚠️ NOT SUPPORTED

**Feature Correlations with Hike Label:**
- Storytelling: r = 0.554 (strongest)
- Maths/Stats: r = 0.524
- Coding: r = 0.444
- AI/ML: r = 0.405
- Big Data: r = 0.112 (weakest)

**Logistic Regression (Additive):**
- Storytelling coef: 1.35 (p = 0.0003) ✓
- Maths/Stats coef: 1.82 (p = 0.0002) ✓

**Logistic Regression (with Interaction):**
- Interaction (storytelling × maths_stats): -1.72 (p = 0.209) ✗
- Storytelling main: 9.55 (p = 0.154) - inflated due to collinearity
- Maths/Stats main: 10.03 (p = 0.136) - inflated due to collinearity

**Likelihood Ratio Test:**
- LRT statistic: 2.82
- df: 1
- **p-value: 0.093** (NOT significant at α = 0.05)

**Bootstrap CI (2,000 reps):**
- Mean: -2.23
- 95% CI: [-6.12, 0.21]
- **Includes zero: YES**

**Power Analysis:**
- Events: 73, Parameters: 7
- Events per parameter: 10.4 (borderline)
- MDE: Large effects only detectable; interaction coef < 0.5 likely underpowered

**Conclusion for H4:** We cannot claim storytelling × maths_stats interaction in JDS hike prediction. The LRT is not significant (p = 0.093), and the bootstrap CI includes zero. Storytelling and Maths/Stats are strong individual predictors, but their interaction is not supported.

### 4.5 Senior Lane (H5) ❌ INVALIDATED

**SDS Forensic Analysis:**

| Depth | AUC | Interpretation |
|-------|-----|----------------|
| 1 | 0.826 | Single split on Openness > 38.5 |
| 2 | 0.917 | + Conscientiousness > 36.5 |
| 3 | 0.942 | + Agreeableness > 37.5 |
| 4 | 0.917 | Overfitting begins |
| 5 | 0.924 | Overfitting |

**The Rule:**
```
IF Openness > 38.5 AND Conscientiousness > 36.5:
    → Success (high)
ELSE:
    → No Success (low)
```

**Shuffled-Target Gap:**
- Real (depth-2) AUC: 0.917
- Shuffled AUC (20 seeds): 0.502 ± 0.044
- Gap: 0.416

**Feature Importance (Random Forest):**
1. Conscientiousness: 0.343
2. Openness: 0.333
3. Extraversion: 0.146
4. Agreeableness: 0.142
5. Neuroticism: 0.036

**Conclusion for H5:**
The SDS label is nearly a deterministic function of the trait scores (depth-2 tree AUC = 0.917). This is a **labeling artifact**, not evidence about real-world success. We cannot study trait-success relationships with this label. Any "prediction" is essentially recovering the labeling rule.

The benchmark results (RandomForest AUC = 0.997, ExtraTrees AUC = 0.998) reflect this deterministic relationship, NOT predictive power for real workforce outcomes. Even logistic regression gets 0.959 AUC because the label is a threshold function of the inputs.

---

## 5. Results and Conclusions

### 5.1 Benchmark Results

**JDS (n=139, 5 features, 20×5 CV):**

| Model | AUC (95% CI) | Accuracy | F1 |
|-------|--------------|----------|-----|
| LogisticRegression | 0.904 [0.893, 0.915] | 0.865 | 0.875 |
| HistGradientBoosting | 0.858 [0.844, 0.871] | 0.801 | 0.814 |
| RandomForest | 0.844 [0.832, 0.856] | 0.772 | 0.780 |
| LightGBM | 0.837 [0.823, 0.850] | 0.770 | 0.782 |
| XGBoost | 0.836 [0.822, 0.849] | 0.770 | 0.780 |
| CatBoost | 0.828 [0.815, 0.841] | 0.762 | 0.770 |
| ExtraTrees | 0.746 [0.730, 0.762] | 0.781 | 0.791 |
| MajorityBaseline | 0.500 | 0.525 | 0.689 |

**Key insight**: Linear model wins. This is consistent with approximately additive signal plus noise at n = 139.

**SDS (n=161, 5 features, 20×5 CV):**

| Model | AUC | Accuracy | F1 |
|-------|-----|----------|-----|
| ExtraTrees | 0.998 | 0.972 | 0.975 |
| RandomForest | 0.997 | 0.957 | 0.960 |
| CatBoost | 0.996 | 0.961 | 0.964 |
| LightGBM | 0.992 | 0.951 | 0.955 |
| HistGradientBoosting | 0.993 | 0.953 | 0.956 |
| XGBoost | 0.991 | 0.947 | 0.950 |
| LogisticRegression | 0.959 | 0.924 | 0.930 |
| MajorityBaseline | 0.500 | 0.528 | 0.691 |

**Key insight**: Even linear model gets 0.959 AUC. This confirms the label is a near-deterministic function of inputs. The 0.99+ AUC from tree models reflects the labeling artifact, not real predictive power.

### 5.2 Pre-Committed Interpretation

Following Table 16 from our approach note, we interpret the outcome pattern:

**Observed Pattern:**
- H3: NOT significant (interaction CI includes zero)
- H4: NOT supported (LRT p = 0.093, CI includes zero)
- H5: INVALIDATED (labels are rule-generated)

**Conclusion We State:**
> "We found no evidence for technical-communication complementarity in these data. Technical skills predict higher salary in the market and higher hike probability for juniors, but the interaction between technical and communication skills is not significant in either setting. The SDS label appears to be generated from threshold rules on personality traits, making it impossible to study real trait-success relationships."
>
> **Wording limit**: Association only. No causal claims. No individual-level predictions.

### 5.3 What the Numbers Cannot Say
- Cross-validated performance estimates how well a model fits the same population, not deployment performance
- ROC-AUC is not accuracy
- A feature with large importance contributes to the model's estimate, not shown to cause the outcome
- The SDS 0.99+ AUC is a labeling artifact, not a real result

---

## 6. Implications

### For Employers
- Benchmark pay within role family, not pooled
- Technical roles (Data Scientist, Data Engineer) command premium salaries
- Communication skills alone do not add salary premium in this data

### For HR and L&D
- Prioritize technical skills (Python, SQL, ML) for salary impact
- The evidence does not support bundling technical + communication training for salary gains
- Role-specific skill requirements vary significantly

### For Universities
- Compare curriculum coverage to market demand
- Technical skills (Python, SQL, ML) have highest market demand
- Communication skills are valuable but not evidenced as salary multipliers here

### For Professionals
- Use role-conditioned skill gaps to plan learning
- Prioritize skills by role-specific demand and salary association
- No guaranteed salary gains from any skill (observational data)

### For Policymakers
- Invest in longitudinal linkage with consent for causal designs
- Localize skill taxonomies for the Indian market
- Observational data cannot support causal policy conclusions

---

## 7. Limitations and Ethical Considerations

- **L1 Observational data**: No causal inference
- **L2 Small samples**: JDS (139) and SDS (161) give wide intervals; interaction results underpowered
- **L3 Provenance**: Files may contain self-reported, masked or generated values; SDS label provenance is unstated
- **L4 No linkage**: No person-level link between files; alignment is across populations
- **L5 Construct validity**: Skill-to-dimension mapping is our construct, tested for sensitivity
- **L6 Taxonomy fit**: External taxonomies may fit Indian technology postings poorly
- **L7 Sampling**: Postings are not the whole market; undisclosed salaries may be selected
- **L8 No time axis**: No trend or trajectory observed
- **L9 Personality**: Trait scores are normalised self-descriptions; SDS label invalid for research
- **L10 Generalisation**: Cross-validation does not show real-world performance

**Ethics**: We do not build or recommend a tool that scores individuals. Personality results must not be used to screen, rank or exclude people.

---

## 8. Conclusion and Future Work

We defined a problem the four files can support, built the machinery to test it, and fixed in advance how each outcome will be read. 

**The contribution is the composition:**
1. A falsifiable organising hypothesis tested in three independent datasets
2. A boundary-preserving architecture in which datasets meet only at shared constructs
3. An audit layer that makes every number traceable
4. **Honest reporting of null and invalidated results**

**What we found:**
- Technical roles pay more (H1 supported)
- Skills are role-specific (H2 supported)
- No evidence for technical-communication complementarity (H3, H4 not supported)
- SDS label is invalid for research (H5 invalidated)

**Future work, in order of value:**
1. Linked longitudinal data collected with consent
2. Dated postings for genuine trend analysis
3. Documented JDS items to validate the bridge
4. Localized skill taxonomy for Indian postings
5. Causal designs (matched cohorts) that observational files cannot support

---

## Appendices

### Appendix A: Data Dictionary
See original approach note Table 23 for full data dictionary.

### Appendix B: Figures
All figures generated and saved to `reports/figures/`:
- market_role_demand.png
- market_salary_dist.png
- market_experience.png
- market_geography.png
- career_opportunity_frontier.png
- role_salary_matrix.png

### Appendix C: Evidence Registry
All claims registered in `reports/evidence/evidence_registry.json` with full provenance.

### Appendix D: Reproducibility
- One command (`./run.sh`) reruns the full pipeline
- Seeds 0-19 for repeats
- Library versions in requirements.txt
- No hidden notebook state

---

*Generated: October 2026*  
*Team ctrl shift n | SAS CU Hackathon 2026*  
*Deterministic pipeline - all numbers reproducible with `./run.sh`*
