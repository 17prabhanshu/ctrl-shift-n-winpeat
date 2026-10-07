import os
import json
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import StratifiedKFold, cross_val_score
from datetime import datetime

print("Starting SDS Forensic Analysis...")

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
df = pd.read_excel(os.path.join(project_root, 'data/processed/sds_personality_clean.xlsx'))
df.columns = df.columns.str.replace(" ", "")

features = ["neuroticism", "extraversion", "openness_to_experience", "agreeableness", "conscientiousness"]
target = "success_classification_high_low"

X = df[features]
y = df[target]

# 1. Feature distributions by class
print("\n=== Feature Distributions by Class ===")
print(df.groupby(target)[features].mean())

# 2. Shallow Decision Trees (Depth 1, 2, 3)
print("\n=== Shallow Decision Trees (Forensic Leakage Test) ===")
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for depth in [1, 2, 3]:
    clf = DecisionTreeClassifier(max_depth=depth, random_state=42)
    scores = cross_val_score(clf, X, y, cv=cv, scoring='roc_auc')
    print(f"Depth {depth} ROC-AUC: {np.mean(scores):.4f} (± {np.std(scores):.4f})")
    
    # Fit on all to extract the rule
    clf.fit(X, y)
    rules = export_text(clf, feature_names=features)
    print(f"Rules (Depth {depth}):\n{rules}")

# Register evidence for Depth-2 separability
record = {
    "claim_id": "SDS-Forensic-001",
    "domain": "Senior Evidence",
    "evidence_tag": "M",
    "statement": "SDS target is almost perfectly separable by a depth-2 decision tree on Conscientiousness and Openness, suggesting labels are strongly deterministic derived from these traits.",
    "dataset": "SDS Personality",
    "method": "Decision Tree (max_depth=2) with 5-fold CV",
    "metric": "ROC-AUC",
    "value": float(np.mean(cross_val_score(DecisionTreeClassifier(max_depth=2, random_state=42), X, y, cv=cv, scoring='roc_auc'))),
    "limitation": "The target classification was likely generated synthetically or rules-based from personality scores rather than observed real-world performance.",
    "status": "accepted",
    "timestamp": datetime.now().isoformat()
}

registry_path = os.path.join(project_root, 'reports/evidence/evidence_registry.json')
with open(registry_path, 'r') as f:
    registry = json.load(f)

existing_idx = next((i for i, r in enumerate(registry) if r.get('claim_id') == 'SDS-Forensic-001'), None)
if existing_idx is not None:
    registry[existing_idx] = record
else:
    registry.append(record)
    
with open(registry_path, 'w') as f:
    json.dump(registry, f, indent=4)

print("\nSDS Forensic Evidence Registered.")
