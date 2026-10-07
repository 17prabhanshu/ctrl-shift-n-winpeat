import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, balanced_accuracy_score, roc_auc_score, average_precision_score, brier_score_loss
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, HistGradientBoostingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

def load_and_prep_data(path, dataset_type="jds"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.replace(" ", "")
    
    if dataset_type == "jds":
        target_col = "salary_hike_high_or_low"
        features = ["big_data_skills", "maths-stats_skills", "coding_skills", "ai_and_ml_skills", "dashboard_and_storytelling_skills"]
    else: # sds
        target_col = "success_classification_high_low"
        features = ["neuroticism", "extraversion", "openness_to_experience", "agreeableness", "conscientiousness"]
        
    X = df[features]
    y = df[target_col]
    return X, y

def calculate_ece(y_true, y_prob, n_bins=10):
    bins = np.linspace(0., 1., n_bins + 1)
    binids = np.digitize(y_prob, bins) - 1
    
    bin_sums = np.bincount(binids, weights=y_prob, minlength=len(bins))
    bin_true = np.bincount(binids, weights=y_true, minlength=len(bins))
    bin_total = np.bincount(binids, minlength=len(bins))
    
    nonzero = bin_total != 0
    prob_true = bin_true[nonzero] / bin_total[nonzero]
    prob_pred = bin_sums[nonzero] / bin_total[nonzero]
    
    ece = np.sum(np.abs(prob_true - prob_pred) * (bin_total[nonzero] / len(y_true)))
    return ece

def get_models():
    return {
        "MajorityBaseline": DummyClassifier(strategy="prior"),
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "RandomForest": RandomForestClassifier(random_state=42),
        "ExtraTrees": ExtraTreesClassifier(random_state=42),
        "HistGradientBoosting": HistGradientBoostingClassifier(random_state=42),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42),
        "LightGBM": LGBMClassifier(random_state=42, verbose=-1),
        "CatBoost": CatBoostClassifier(verbose=0, random_seed=42)
    }

def run_benchmark(X, y, output_path):
    models = get_models()
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=20, random_state=42)
    
    results = {}
    
    for name, model in models.items():
        metrics = {
            "accuracy": [], "precision": [], "recall": [], "f1": [],
            "balanced_accuracy": [], "roc_auc": [], "pr_auc": [], "brier_score": [], "ece": []
        }
        
        for train_idx, test_idx in cv.split(X, y):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            if hasattr(model, "predict_proba"):
                y_prob = model.predict_proba(X_test)[:, 1]
            else:
                y_prob = y_pred
                
            metrics["accuracy"].append(accuracy_score(y_test, y_pred))
            metrics["precision"].append(precision_score(y_test, y_pred, zero_division=0))
            metrics["recall"].append(recall_score(y_test, y_pred, zero_division=0))
            metrics["f1"].append(f1_score(y_test, y_pred, zero_division=0))
            metrics["balanced_accuracy"].append(balanced_accuracy_score(y_test, y_pred))
            
            if len(np.unique(y_test)) > 1:
                metrics["roc_auc"].append(roc_auc_score(y_test, y_prob))
            metrics["pr_auc"].append(average_precision_score(y_test, y_prob))
            metrics["brier_score"].append(brier_score_loss(y_test, y_prob))
            metrics["ece"].append(calculate_ece(y_test, y_prob))
            
        summary = {}
        for k, v in metrics.items():
            if len(v) > 0:
                mean_val = float(np.mean(v))
                std_val = float(np.std(v))
                ci = float(1.96 * std_val / np.sqrt(len(v)))
                summary[k] = {"mean": mean_val, "std": std_val, "95_ci": ci}
        results[name] = summary
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)
        
    return results

if __name__ == "__main__":
    X_jds, y_jds = load_and_prep_data("data/processed/jds_skills_clean.xlsx", "jds")
    run_benchmark(X_jds, y_jds, "reports/benchmarks/jds_benchmark.json")
    
    X_sds, y_sds = load_and_prep_data("data/processed/sds_personality_clean.xlsx", "sds")
    run_benchmark(X_sds, y_sds, "reports/benchmarks/sds_benchmark.json")
