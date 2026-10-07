import re

with open('README.md', 'r') as f:
    content = f.read()

# 1. Remove the marks
content = re.sub(r' \(\d+ Marks\)', '', content)

# 2. Refine the AI-like structure to look like a top-tier open source project
# I'll replace the section titles and add styling.

content = content.replace("## 1. Problem Definition & Analytics Objective", "## 🎯 Analytics Objective")
content = content.replace("## 2. Approach Description", "## 🏗️ Architecture & Approach")
content = content.replace("## 3. Data Exploration & Preparation", "## 🧹 Data Engineering Strategy")
content = content.replace("## 4. Data Analysis & Explainability", "## 🔬 Data Analysis & Explainable AI")
content = content.replace("## 5. Results and Conclusions", "## 📈 Results & Key Findings")
content = content.replace("## 6. Implications", "## 🌍 Real-World Implications")

content = content.replace("### Advanced Analytical Implementations", "<details>\n<summary><b>View Advanced Analytical Implementations (TreeSHAP, Firth, Conformal)</b></summary>\n<br>\n\n1. **Glassbox Explainability (TreeSHAP):** We use exact Shapley Additive exPlanations to interpret tree ensembles. We strictly bound our analysis to *statistical associations*, avoiding unfounded causal claims. \n2. **Firth Penalized Logistic Regression:** To detect interactions (e.g., `maths_stats * storytelling`) in small samples ($n=139$), standard MLE fails due to quasi-complete separation. We implemented Firth's penalized likelihood to guarantee finite confidence intervals.\n3. **Conformal Prediction:** For prescriptive HR deployment, forced binary classifications are irresponsible. We utilize distribution-free **Conformal Prediction**, generating 90% confidence prediction sets that allow the model to *abstain* when applicant ambiguity is too high.\n</details>")

content = content.replace("#### Code Snippet: Robustness & Calibration", "<details>\n<summary><b>View Pipeline Code Snippet</b></summary>\n")

# Need to cap the details block for the code snippet
content = content.replace("```python\n# Demonstrating rigorous evaluation avoiding \"perfect score\" leakage\nfrom sklearn.calibration import CalibratedClassifierCV\nfrom sklearn.model_selection import RepeatedStratifiedKFold\nfrom xgboost import XGBClassifier\n\n# Base model with calibrated probabilities\nbase_xgb = XGBClassifier(eval_metric='logloss', random_state=42)\ncalibrated_xgb = CalibratedClassifierCV(base_xgb, method='sigmoid', cv=5)\n\n# Rigorous evaluation\ncv = RepeatedStratifiedKFold(n_splits=5, n_repeats=20, random_state=42)\n# Null hypothesis check: verify score drops to ~0.5 when target is shuffled\n```\n", "```python\n# Demonstrating rigorous evaluation avoiding \"perfect score\" leakage\nfrom sklearn.calibration import CalibratedClassifierCV\nfrom sklearn.model_selection import RepeatedStratifiedKFold\nfrom xgboost import XGBClassifier\n\n# Base model with calibrated probabilities\nbase_xgb = XGBClassifier(eval_metric='logloss', random_state=42)\ncalibrated_xgb = CalibratedClassifierCV(base_xgb, method='sigmoid', cv=5)\n\n# Rigorous evaluation\ncv = RepeatedStratifiedKFold(n_splits=5, n_repeats=20, random_state=42)\n# Null hypothesis check: verify score drops to ~0.5 when target is shuffled\n```\n</details>\n")

content = content.replace("This repository houses the complete **Workforce Intelligence Engine**. To assist the jury in evaluation, this documentation is structured directly according to the **Round 2 Evaluation Criteria**.", "> **Workforce Intelligence Engine** is a deterministic analytical platform designed to synthesize and interpret complex labor-market signals without inducing data leakage.")

with open('README.md', 'w') as f:
    f.write(content)
