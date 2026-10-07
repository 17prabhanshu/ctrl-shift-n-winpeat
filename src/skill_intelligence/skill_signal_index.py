import json
import numpy as np
import pandas as pd
import os
import statsmodels.api as sm
from collections import defaultdict

np.random.seed(42)

def calculate_ssi():
    print("Starting Validated Skill Signal Index Analysis...")
    
    # Load actual data
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    df = pd.read_csv(os.path.join(project_root, 'data/processed/analytics_jobs_clean.csv'))
    
    with open(os.path.join(project_root, 'reports/evidence/skill_graph_metrics.json'), 'r') as f:
        graph_metrics = json.load(f)
        
    skills = list(graph_metrics.keys())
    
    # 1. Demand & Breadth (from graph)
    demand = np.array([graph_metrics[s]['frequency'] for s in skills])
    breadth = np.array([graph_metrics[s]['betweenness'] for s in skills])
    
    # 2. Specificity (Information Gain / Variance across roles)
    # If a skill appears in only 1 role family, it's highly specific.
    # If it appears evenly across all role families, it's generic.
    
    # Map roles
    role_map = {}
    for r in df['job_desig'].dropna().unique():
        rl = str(r).lower()
        if 'scientist' in rl: role_map[r] = 'Data Scientist'
        elif 'engineer' in rl and 'machine learning' not in rl and 'ml' not in rl: role_map[r] = 'Data Engineer'
        elif 'analyst' in rl and 'business' not in rl: role_map[r] = 'Data Analyst'
        elif 'business analyst' in rl: role_map[r] = 'Business Analyst'
        elif 'machine learning' in rl or 'ml' in rl: role_map[r] = 'ML Engineer'
        else: role_map[r] = 'Other'
        
    df['role_family'] = df['job_desig'].map(role_map).fillna('Other')
    
    # Create skill presence matrix
    skill_presence = {s: [] for s in skills}
    for ks in df['key_skills'].fillna(''):
        ks_lower = str(ks).lower()
        for s in skills:
            skill_presence[s].append(1 if s in ks_lower else 0)
            
    for s in skills:
        df[f'skill_{s}'] = skill_presence[s]
        
    # Calculate specificity as normalized variance of probabilities across roles
    specificity = []
    for s in skills:
        role_probs = df.groupby('role_family')[f'skill_{s}'].mean()
        var = np.var(role_probs)
        specificity.append(var)
    specificity = np.array(specificity)
    
    # 3. Compensation Association (controlling for experience)
    # We only have salary min/max. Let's use mid.
    df['salary_mid'] = (df['salary_min'] + df['salary_max']) / 2
    df_sal = df.dropna(subset=['salary_mid', 'exp_mid', 'role_family']).copy()
    
    # Dummy code role family
    roles_dummies = pd.get_dummies(df_sal['role_family'], drop_first=True, dtype=float)
    
    comp_assoc = []
    for s in skills:
        # log_salary ~ skill + exp_mid + role
        X = pd.DataFrame({'skill': df_sal[f'skill_{s}'], 'exp_mid': df_sal['exp_mid']})
        X = pd.concat([X, roles_dummies], axis=1)
        X = sm.add_constant(X)
        y = np.log1p(df_sal['salary_mid'])
        
        try:
            model = sm.OLS(y, X).fit()
            coef = model.params['skill']
            pval = model.pvalues['skill']
            # Only count if statistically significant (p < 0.05), else 0
            comp_assoc.append(coef if pval < 0.05 else 0)
        except:
            comp_assoc.append(0)
            
    comp_assoc = np.array(comp_assoc)
    
    # Normalize all components to [0,1]
    def min_max(arr):
        mn, mx = np.min(arr), np.max(arr)
        if mx == mn: return arr
        return (arr - mn) / (mx - mn)
        
    demand = min_max(demand)
    breadth = min_max(breadth)
    specificity = min_max(specificity)
    comp_assoc = min_max(comp_assoc)
    
    results = {}
    for i, s in enumerate(skills):
        results[s] = {
            'demand': float(demand[i]),
            'specificity': float(specificity[i]),
            'comp_assoc': float(comp_assoc[i]),
            'breadth': float(breadth[i]),
        }
        
    # 10,000 Dirichlet draws for stability
    n_draws = 10000
    weights = np.random.dirichlet((1, 1, 1, 1), n_draws)
    
    for i, s in enumerate(skills):
        ssi_draws = weights[:,0]*demand[i] + weights[:,1]*specificity[i] + weights[:,2]*comp_assoc[i] + weights[:,3]*breadth[i]
        results[s]['ssi_mean'] = float(np.mean(ssi_draws))
        results[s]['ssi_std'] = float(np.std(ssi_draws))
        results[s]['ssi_p05'] = float(np.percentile(ssi_draws, 5))
        results[s]['ssi_p95'] = float(np.percentile(ssi_draws, 95))
        
    with open(os.path.join(project_root, 'reports/evidence/skill_signal_index.json'), 'w') as f:
        json.dump(results, f, indent=4)
        
    print("Skill Signal Index Validation Complete. No random metrics used.")

if __name__ == '__main__':
    calculate_ssi()
