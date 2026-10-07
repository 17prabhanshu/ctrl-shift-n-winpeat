import os
import json
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.benchmark_engine import load_and_prep_data

def run_robustness(X, y, name="jds"):
    results = {}
    
    # 20 seeds
    seed_scores = []
    for s in range(20):
        clf = XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=s)
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=s)
        scores = cross_val_score(clf, X, y, cv=cv, scoring="roc_auc")
        seed_scores.append(np.mean(scores))
        
    results["Multiple_Seeds_ROC_AUC"] = {
        "mean": float(np.mean(seed_scores)),
        "std": float(np.std(seed_scores))
    }
    
    # Feature perturbation
    X_noisy = X + np.random.normal(0, 0.1, X.shape)
    clf = XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    noisy_scores = cross_val_score(clf, X_noisy, y, cv=cv, scoring="roc_auc")
    results["Perturbation_ROC_AUC"] = float(np.mean(noisy_scores))
    
    # Shuffled target
    y_shuff = np.random.RandomState(42).permutation(y)
    shuff_scores = cross_val_score(clf, X, y_shuff, cv=cv, scoring="roc_auc")
    results["Shuffled_Target_ROC_AUC"] = float(np.mean(shuff_scores))
    
    os.makedirs("reports/benchmarks", exist_ok=True)
    with open(f"reports/benchmarks/robustness_{name}.json", "w") as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    X_jds, y_jds = load_and_prep_data("data/processed/jds_skills_clean.xlsx", "jds")
    run_robustness(X_jds, y_jds, "jds")
    
    X_sds, y_sds = load_and_prep_data("data/processed/sds_personality_clean.xlsx", "sds")
    run_robustness(X_sds, y_sds, "sds")
