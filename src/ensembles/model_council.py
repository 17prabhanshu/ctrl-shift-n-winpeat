import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.benchmark_engine import load_and_prep_data

def evaluate_ensemble(X, y):
    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "RandomForest": RandomForestClassifier(random_state=42),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42),
        "LightGBM": LGBMClassifier(random_state=42, verbose=-1)
    }
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    base_preds = {}
    best_single_auc = 0
    best_single_name = ""
    
    for name, model in models.items():
        preds = cross_val_predict(model, X, y, cv=cv, method="predict_proba")[:, 1]
        base_preds[name] = preds
        
        auc = roc_auc_score(y, preds)
        if auc > best_single_auc:
            best_single_auc = auc
            best_single_name = name
            
    X_meta = pd.DataFrame(base_preds)
    
    meta_learner = LogisticRegression(random_state=42)
    meta_preds = cross_val_predict(meta_learner, X_meta, y, cv=cv, method="predict_proba")[:, 1]
    
    meta_auc = roc_auc_score(y, meta_preds)
    
    return {
        "best_single_model": best_single_name,
        "best_single_auc": best_single_auc,
        "ensemble_auc": meta_auc,
        "kept_ensemble": bool(meta_auc > best_single_auc)
    }

if __name__ == "__main__":
    X_jds, y_jds = load_and_prep_data("data/processed/jds_skills_clean.xlsx", "jds")
    jds_res = evaluate_ensemble(X_jds, y_jds)
    
    X_sds, y_sds = load_and_prep_data("data/processed/sds_personality_clean.xlsx", "sds")
    sds_res = evaluate_ensemble(X_sds, y_sds)
    
    res = {"jds": jds_res, "sds": sds_res}
    
    os.makedirs("reports/benchmarks", exist_ok=True)
    with open("reports/benchmarks/ensemble_results.json", "w") as f:
        json.dump(res, f, indent=4)
