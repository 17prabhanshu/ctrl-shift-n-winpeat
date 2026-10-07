# Model Cards: Workforce Intelligence Engine

This document provides formal model documentation adhering to the Model Cards for Model Reporting framework (Mitchell et al., 2019) for the predictive models trained in the Workforce Intelligence Engine.

---

## 1. Junior Data Scientist (JDS) Progression Model

### 1.1 Model Details
- **Developer**: Team ctrl shift n (SAS CU Hackathon 2026).
- **Model Type**: Regularized Logistic Regression (Primary interpretable benchmark) & Random Forest Classifier.
- **Task**: Predict internal salary hike classification (`salary_hike_high_or_low`: 1 = High, 0 = Low).
- **Features (5 continuous traits)**: `big_data_skills`, `maths-stats_skills`, `coding_skills`, `ai_and_ml_skills`, `dashboard_and_storytelling_skills` (Scored in range [2.2, 5.0]).
- **Sample Size**: $n = 139$ evaluated junior practitioners.

### 1.2 Performance Metrics
Evaluated using Repeated Stratified 5-Fold Cross-Validation (20 repeats = 100 evaluations):

| Model Architecture | Accuracy (Mean ± SD) | ROC-AUC (Mean ± SD) | F1-Score (Mean ± SD) | Brier Score | ECE (Calibrated) |
|:---|:---|:---|:---|:---|:---|
| **Majority Baseline** | 0.525 ± 0.012 | 0.500 ± 0.000 | 0.000 ± 0.000 | 0.249 | 0.475 |
| **Logistic Regression (L2)** | **0.865 ± 0.052** | **0.904 ± 0.048** | **0.875 ± 0.046** | **0.102** | **0.038** |
| **Random Forest** | 0.820 ± 0.061 | 0.830 ± 0.055 | 0.828 ± 0.058 | 0.124 | 0.062 |
| **XGBoost** | 0.812 ± 0.065 | 0.841 ± 0.058 | 0.819 ± 0.060 | 0.131 | 0.071 |

### 1.3 Explainability & Feature Attribution
- **TreeSHAP & Logistic Coefficients**:
  - The highest positive associations with a salary hike are `maths-stats_skills` (Log-odds: +1.821) and `dashboard_and_storytelling_skills` (Log-odds: +1.355).
  - `coding_skills` exhibited the lowest relative incremental association (+0.609), indicating that baseline coding proficiency is a prerequisite rather than a differentiator for premium internal progression.
- **Interaction Testing**: Interaction between quantitative rigor and executive communication (`maths_stats * storytelling`) is positive (+0.087, $p = 0.148$).

---

## 2. Senior Data Scientist (SDS) Personality Model

### 2.1 Model Details
- **Developer**: Team ctrl shift n (SAS CU Hackathon 2026).
- **Model Type**: ExtraTrees Classifier & Random Forest Classifier.
- **Task**: Predict career success classification (`success_classification_high_low`: 1 = High, 0 = Low).
- **Features (5 Big Five Traits)**: `neuroticism`, `extraversion`, `openness_to_experience`, `agreeableness`, `conscientiousness` (Continuous scores).
- **Sample Size**: $n = 161$ senior practitioners.

### 2.2 Performance Metrics & Forensic Findings

| Model Architecture | Accuracy (Mean ± SD) | ROC-AUC (Mean ± SD) | F1-Score (Mean ± SD) | Notes / Status |
|:---|:---|:---|:---|:---|
| **Majority Baseline** | 0.528 ± 0.010 | 0.500 ± 0.000 | 0.000 ± 0.000 | Random guessing baseline |
| **ExtraTrees Classifier** | **0.972 ± 0.025** | **0.998 ± 0.006** | **0.975 ± 0.022** | Near-perfect separation |
| **Random Forest** | 0.957 ± 0.029 | 0.992 ± 0.008 | 0.961 ± 0.026 | Benchmark runner-up |
| **Depth-2 Decision Tree** | 0.913 ± 0.038 | 0.917 ± 0.045 | 0.918 ± 0.034 | 2 threshold rules extract >91% AUC |
| **Shuffled-Target Sanity Test** | 0.512 ± 0.048 | 0.589 ± 0.054 | 0.518 ± 0.046 | Null check drops to chance level |

### 2.3 Forensic Audit Statement
> **Crucial Scientific Caveat**: The exceptionally high ROC-AUC (0.998) on the SDS dataset is **not** presented as a production success metric. A post-hoc forensic audit revealed that a depth-2 decision tree on just two features (`openness > 38.5` and `conscientiousness > 36.5`) captures 0.917 of the area under the curve. This indicates that the target outcome was likely synthesized through hardcoded rules rather than observed natural behavior. The shuffled-target test drops to 0.589, confirming the pipeline does not leak labels, but the dataset itself reflects synthetic label construction.

---

## 3. Intended Use & Deployment Guardrails

### 3.1 Intended Domain
- **Workforce Planning Analytics**: Understanding empirical patterns and relative returns on skill combinations across roles.
- **Curriculum & Upskilling Guidance**: Providing data-informed advice on complementary skill development (e.g., advising data analysts to pair SQL with storytelling).

### 3.2 Prohibited Uses
- **Autonomous Candidate Screening**: The models must **never** be used to screen, rank, or reject job applicants.
- **Psychometric Gatekeeping**: Personality scores (SDS) must never be used for compensation or employment decisions.

### 3.3 Uncertainty Quantification via Conformal Prediction
For high-ambiguity decision regimes, the system implements **inductive conformal prediction** at a significance level of $\alpha = 0.10$ (90% marginal coverage). Whenever an individual candidate's feature profile is ambiguous, the conformal predictor outputs a set containing both labels:
$$\Gamma_{0.90}(x) = \{0, 1\}$$
This forces the automated engine to **abstain** and route the case directly to human talent leaders.
