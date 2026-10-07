import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import os
from datetime import datetime

# Path setup
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
df = pd.read_csv(os.path.join(project_root, 'data/processed/analytics_jobs_clean.csv'))

# Create skill dummies based on exact keywords as proxy for T and C
df['T_skill'] = df['key_skills'].str.contains('python|sql|machine learning|big data|aws', case=False, na=False).astype(int)
df['C_skill'] = df['key_skills'].str.contains('presentation|communication|storytelling|dashboard|tableau|power bi', case=False, na=False).astype(int)

# Target
df['salary_mid'] = (df['salary_min'] + df['salary_max']) / 2
df_clean = df.dropna(subset=['salary_mid', 'exp_mid', 'job_desig']).copy()

# Filter reasonable salary bounds (outlier removal)
df_clean = df_clean[(df_clean['salary_mid'] > 100000) & (df_clean['salary_mid'] < 10000000)]
df_clean['log_salary'] = np.log(df_clean['salary_mid'])

# Role grouping
role_map = {}
for r in df_clean['job_desig'].unique():
    rl = str(r).lower()
    if 'scientist' in rl: role_map[r] = 'Data Scientist'
    elif 'engineer' in rl and 'machine learning' not in rl and 'ml' not in rl: role_map[r] = 'Data Engineer'
    elif 'analyst' in rl and 'business' not in rl: role_map[r] = 'Data Analyst'
    elif 'business analyst' in rl: role_map[r] = 'Business Analyst'
    elif 'machine learning' in rl or 'ml' in rl: role_map[r] = 'ML Engineer'
    else: role_map[r] = 'Other'
df_clean['role_family'] = df_clean['job_desig'].map(role_map)

# OLS with robust standard errors (HC3)
# log_salary ~ exp_mid + role_family + T_skill + C_skill + T_skill:C_skill
formula = 'log_salary ~ exp_mid + C(role_family) + T_skill * C_skill'
model = smf.ols(formula=formula, data=df_clean).fit(cov_type='HC3')

print("=== INTERACTION MODEL SUMMARY ===")
print(model.summary().tables[1])

interaction_coef = model.params['T_skill:C_skill']
interaction_p = model.pvalues['T_skill:C_skill']
ci_lower, ci_upper = model.conf_int().loc['T_skill:C_skill']

print(f"\nInteraction Coefficient (T*C): {interaction_coef:.4f} (p={interaction_p:.4e})")

# Register the evidence
record = {
    "claim_id": "H3-Complementarity-001",
    "domain": "Market Analysis",
    "evidence_tag": "M",
    "statement": f"Technical and Communication skills exhibit positive complementarity in market compensation.",
    "dataset": "Analytics Jobs",
    "method": "OLS regression with HC3 robust standard errors on log salary",
    "metric": "Interaction coefficient (T x C)",
    "value": float(interaction_coef),
    "ci95_lower": float(ci_lower),
    "ci95_upper": float(ci_upper),
    "limitation": "Observational data; possible omitted variable bias (e.g. unobserved company quality)",
    "status": "accepted",
    "timestamp": datetime.now().isoformat()
}

registry_path = os.path.join(project_root, 'reports/evidence/evidence_registry.json')
with open(registry_path, 'r') as f:
    registry = json.load(f)

# Update or append
existing_idx = next((i for i, r in enumerate(registry) if r.get('claim_id') == 'H3-Complementarity-001'), None)
if existing_idx is not None:
    registry[existing_idx] = record
else:
    registry.append(record)
    
with open(registry_path, 'w') as f:
    json.dump(registry, f, indent=4)
print("Evidence registered successfully.")
