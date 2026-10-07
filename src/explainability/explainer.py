import os
import shap
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.benchmark_engine import load_and_prep_data
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression

def explain_model(X, y, name="jds"):
    # Train model
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X, y)
    
    # SHAP
    explainer = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(X)
    
    shap.summary_plot(shap_values, X, show=False)
    os.makedirs("reports/figures", exist_ok=True)
    plt.savefig(f"reports/figures/shap_summary_{name}.png", bbox_inches='tight')
    plt.close()
    
    # Permutation Importance
    perm_importance = permutation_importance(clf, X, y, n_repeats=10, random_state=42)
    
    # Linear coefficients for association
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X, y)

if __name__ == "__main__":
    X_jds, y_jds = load_and_prep_data("data/processed/jds_skills_clean.xlsx", "jds")
    explain_model(X_jds, y_jds, "jds")
    
    X_sds, y_sds = load_and_prep_data("data/processed/sds_personality_clean.xlsx", "sds")
    explain_model(X_sds, y_sds, "sds")
