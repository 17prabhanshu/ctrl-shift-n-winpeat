import os
import json
import numpy as np
import pandas as pd
from datetime import datetime
import statsmodels.formula.api as smf

print("Starting Demand-Reward Alignment Analysis...")

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 1. Get Market Demand Share for dimensions (from Analytics Jobs)
try:
    with open(os.path.join(project_root, 'reports/evidence/skill_analysis.json'), 'r') as f:
        skill_analysis = json.load(f)
except:
    print("Could not load skill analysis, skipping.")
    exit()

canonical_skills = skill_analysis.get('mapped_skills', [])
dim_counts = {'big_data': 0, 'maths_statistics': 0, 'coding': 0, 'ai_ml': 0, 'dashboard_storytelling': 0}
total_skills = 0

df_analytics = pd.read_csv(os.path.join(project_root, 'data/processed/analytics_jobs_clean.csv'))
for ks in df_analytics['key_skills'].dropna():
    ks_lower = str(ks).lower()
    for s in canonical_skills:
        if s['canonical_skill'] in ks_lower and s['dimension'] in dim_counts:
            dim_counts[s['dimension']] += 1
            total_skills += 1

demand_shares = {k: (v / total_skills) if total_skills > 0 else 0 for k, v in dim_counts.items()}

# 2. Get JDS Outcome Association (from JDS dataset)
df_jds = pd.read_excel(os.path.join(project_root, 'data/processed/jds_skills_clean.xlsx'))
df_jds.columns = df_jds.columns.str.replace(" ", "")

# Logistic regression: salary_hike ~ all 5 dimensions
model = smf.logit(
    'salary_hike_high_or_low ~ big_data_skills + Q("maths-stats_skills") + coding_skills + ai_and_ml_skills + dashboard_and_storytelling_skills',
    data=df_jds
).fit(disp=0)

jds_associations = {
    'big_data': model.params['big_data_skills'],
    'maths_statistics': model.params['Q("maths-stats_skills")'],
    'coding': model.params['coding_skills'],
    'ai_ml': model.params['ai_and_ml_skills'],
    'dashboard_storytelling': model.params['dashboard_and_storytelling_skills']
}

print("\n=== Demand vs Reward Alignment ===")
for dim in dim_counts.keys():
    print(f"Dimension: {dim}")
    print(f"  Market Demand Share: {demand_shares[dim]:.3f}")
    print(f"  JDS Log-Odds (Reward): {jds_associations[dim]:.3f}")

# Register evidence
record = {
    "claim_id": "Alignment-001",
    "domain": "Cross-Dataset Synthesis",
    "evidence_type": "M",
    "statement": "Demand-Reward Alignment calculated across 5 dimensions without joining rows.",
    "dataset": "Analytics Jobs + JDS Skills",
    "method": "Dimension-level alignment of Market Share vs JDS Log-Odds",
    "metric": "Correlation",
    "value": float(np.corrcoef(list(demand_shares.values()), list(jds_associations.values()))[0, 1]),
    "limitation": "Cross-dataset alignment relies on taxonomy consistency; not a causal link.",
    "status": "accepted",
    "timestamp": datetime.now().isoformat()
}

registry_path = os.path.join(project_root, 'reports/evidence/evidence_registry.json')
with open(registry_path, 'r') as f:
    registry = json.load(f)

existing_idx = next((i for i, r in enumerate(registry) if r.get('claim_id') == 'Alignment-001'), None)
if existing_idx is not None:
    registry[existing_idx] = record
else:
    registry.append(record)
    
with open(registry_path, 'w') as f:
    json.dump(registry, f, indent=4)

print("\nAlignment Evidence Registered.")
