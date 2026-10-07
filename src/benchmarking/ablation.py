import os
import json
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.benchmark_engine import load_and_prep_data

def run_ablation(X, y, name="jds"):
    clf = XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    results = {}
    
    # Full Model
    full_scores = cross_val_score(clf, X, y, cv=cv, scoring="roc_auc")
    results["Full_Model"] = float(np.mean(full_scores))
    
    # Minus each feature
    for col in X.columns:
        X_sub = X.drop(columns=[col])
        scores = cross_val_score(clf, X_sub, y, cv=cv, scoring="roc_auc")
        results[f"Minus_{col}"] = float(np.mean(scores))
        
    # Randomized Target
    y_rand = np.random.RandomState(42).permutation(y)
    rand_scores = cross_val_score(clf, X, y_rand, cv=cv, scoring="roc_auc")
    results["Randomized_Target"] = float(np.mean(rand_scores))
    
    # Grouped for JDS
    if name == "jds":
        tech_cols = ["big_data_skills", "coding_skills", "ai_and_ml_skills"]
        tech_cols = [c for c in tech_cols if c in X.columns]
        if tech_cols:
            scores = cross_val_score(clf, X[tech_cols], y, cv=cv, scoring="roc_auc")
            results["Technical_Only"] = float(np.mean(scores))
            
        comm_cols = ["dashboard_and_storytelling_skills"]
        comm_cols = [c for c in comm_cols if c in X.columns]
        if comm_cols:
            scores = cross_val_score(clf, X[comm_cols], y, cv=cv, scoring="roc_auc")
            results["Communication_Only"] = float(np.mean(scores))
            
        quant_cols = ["maths-stats_skills", "big_data_skills"]
        quant_cols = [c for c in quant_cols if c in X.columns]
        if quant_cols:
            scores = cross_val_score(clf, X[quant_cols], y, cv=cv, scoring="roc_auc")
            results["Quantitative_Only"] = float(np.mean(scores))
            
    os.makedirs("reports/benchmarks", exist_ok=True)
    with open(f"reports/benchmarks/ablation_{name}.json", "w") as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    X_jds, y_jds = load_and_prep_data("data/processed/jds_skills_clean.xlsx", "jds")
    run_ablation(X_jds, y_jds, "jds")
    
    X_sds, y_sds = load_and_prep_data("data/processed/sds_personality_clean.xlsx", "sds")
    run_ablation(X_sds, y_sds, "sds")
