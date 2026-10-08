"""
Skill Market Signal Index (SSI) - multi-component skill ranking.

SSI(s) = Σ_k w_k · r_k(s) where w_k ~ Dirichlet(1,1,1,1)

Components:
1. Demand: frequency percentile
2. Specificity: role-specificity (variance across roles)
3. Compensation: salary association (controlled for role/experience)
4. Breadth: n_role_families percentile

Reports rank intervals from 10,000 Dirichlet draws.
"""
import pandas as pd
import numpy as np
import json
import statsmodels.api as sm
from pathlib import Path
from src.utils.config import (
    PROCESSED_DIR, EVIDENCE_DIR, 
    categorize_role, SKILL_TAXONOMY, NON_TECHNICAL_SKILLS
)

def calculate_ssi():
    """Calculate the Skill Market Signal Index."""
    print("=" * 60)
    print("SKILL MARKET SIGNAL INDEX")
    print("=" * 60)
    
    # Load data
    analytics_path = PROCESSED_DIR / 'analytics_jobs_clean.csv'
    analytics_df = pd.read_csv(analytics_path)
    
    skills_path = EVIDENCE_DIR / 'skill_analysis.json'
    with open(skills_path) as f:
        skill_analysis = json.load(f)
    
    # Get skills from skill_analysis (top skills)
    skills = [s['skill'] for s in skill_analysis['top_skills'][:80]]
    
    print(f"\nAnalyzing {len(skills)} top skills...")
    
    # Categorize roles
    analytics_df['role_family'] = analytics_df['job_desig'].apply(categorize_role)
    
    # Create skill presence matrix
    print("Building skill presence matrix...")
    skill_presence = {}
    for skill in skills:
        skill_lower = skill.lower()
        presence = analytics_df['key_skills'].fillna('').str.lower().str.contains(
            skill_lower, regex=False, na=False
        ).astype(int)
        skill_presence[skill] = presence
        analytics_df[f'skill_{skill}'] = presence
    
    # 1. Demand (frequency percentile)
    print("Computing demand component...")
    demand_freq = np.array([skill_presence[s].sum() for s in skills])
    demand_pct = np.argsort(np.argsort(demand_freq)) / len(skills)  # percentile rank
    
    # 2. Breadth (n_role_families percentile)
    print("Computing breadth component...")
    breadth = np.array([
        skill_df = analytics_df[skill_presence[s] == 1]
        n_roles = skill_df['role_family'].nunique() if len(skill_df) > 0 else 0
        n_roles
        for s in skills
    ])
    breadth_pct = np.argsort(np.argsort(breadth)) / len(skills)
    
    # 3. Specificity (variance across roles - high variance = specific)
    print("Computing specificity component...")
    specificity = []
    for s in skills:
        role_probs = analytics_df.groupby('role_family')[f'skill_{s}'].mean()
        if len(role_probs) > 1:
            var = role_probs.var()
        else:
            var = 0
        specificity.append(var)
    specificity = np.array(specificity)
    specificity_pct = np.argsort(np.argsort(specificity)) / len(skills)
    
    # 4. Compensation association (OLS with role/experience controls)
    print("Computing compensation association...")
    analytics_df['salary_mid'] = (
        (analytics_df['salary_min_inr'] + analytics_df['salary_max_inr']) / 2
    )
    df_sal = analytics_df.dropna(subset=['salary_mid', 'experience_mid', 'role_family']).copy()
    
    # Create role dummies
    role_dummies = pd.get_dummies(df_sal['role_family'], drop_first=True, dtype=float)
    
    comp_assoc = []
    for s in skills:
        X_cols = ['skill_{}'.format(s), 'experience_mid'] + list(role_dummies.columns)
        X = pd.concat([
            df_sal[[f'skill_{s}', 'experience_mid']], 
            role_dummies
        ], axis=1).dropna()
        y = np.log1p(df_sal.loc[X.index, 'salary_mid'])
        
        if len(X) < 50:  # Need minimum sample size
            comp_assoc.append(0)
            continue
            
        try:
            X_const = sm.add_constant(X)
            model = sm.OLS(y, X_const).fit()
            coef = model.params.get(f'skill_{s}', 0)
            pval = model.pvalues.get(f'skill_{s}', 1)
            # Only count significant associations
            comp_assoc.append(coef if pval < 0.05 else 0)
        except Exception as e:
            comp_assoc.append(0)
    
    comp_assoc = np.array(comp_assoc)
    comp_assoc_pct = np.argsort(np.argsort(np.abs(comp_assoc))) / len(skills)
    
    # Normalize all components to [0, 1]
    def minmax(arr):
        mn, mx = arr.min(), arr.max()
        if mx == mn:
            return np.zeros_like(arr)
        return (arr - mn) / (mx - mn)
    
    components = {
        'demand': minmax(demand_pct),
        'breadth': minmax(breadth_pct),
        'specificity': minmax(specificity_pct),
        'compensation': minmax(comp_assoc_pct)
    }
    
    # 10,000 Dirichlet draws for weight uncertainty
    print("Running 10,000 Dirichlet weight draws...")
    n_draws = 10000
    np.random.seed(42)
    weights = np.random.dirichlet([1, 1, 1, 1], n_draws)
    
    ssi_results = {}
    for i, skill in enumerate(skills):
        ssi_draws = (
            weights[:, 0] * components['demand'][i] +
            weights[:, 1] * components['specificity'][i] +
            weights[:, 2] * comp_assoc_pct[i] +
            weights[:, 3] * components['breadth'][i]
        )
        
        ssi_results[skill] = {
            'ssi_mean': float(np.mean(ssi_draws)),
            'ssi_std': float(np.std(ssi_draws)),
            'ssi_p05': float(np.percentile(ssi_draws, 5)),
            'ssi_p95': float(np.percentile(ssi_draws, 95)),
            'rank_mean': float(np.mean(np.argsort(np.argsort(-ssi_draws)) + 1)),
            'rank_p05': float(np.percentile(np.argsort(np.argsort(-ssi_draws)) + 1, 5)),
            'rank_p95': float(np.percentile(np.argsort(np.argsort(-ssi_draws)) + 1, 95)),
            'components': {
                'demand': float(components['demand'][i]),
                'specificity': float(components['specificity'][i]),
                'compensation': float(comp_assoc_pct[i]),
                'breadth': float(components['breadth'][i])
            },
            'dimension': next(
                (d['dimension'] for d in skill_analysis['top_skills'] 
                 if d['skill'] == skill), 'unknown'
            )
        }
    
    # Save results
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    with open(EVIDENCE_DIR / 'skill_signal_index.json', 'w') as f:
        json.dump(ssi_results, f, indent=2)
    
    print(f"\nSaved SSI results: {EVIDENCE_DIR / 'skill_signal_index.json'}")
    
    # Print top 20 skills
    print("\n" + "=" * 60)
    print("TOP 20 SKILLS BY SIGNAL INDEX")
    print("=" * 60)
    sorted_skills = sorted(ssi_results.items(), key=lambda x: x[1]['ssi_mean'], reverse=True)[:20]
    for i, (skill, data) in enumerate(sorted_skills, 1):
        dim = data['dimension']
        print(f"{i:2d}. {skill:25s} | SSI: {data['ssi_mean']:.3f} ± {data['ssi_std']:.3f} | "
              f"Rank: {data['rank_mean']:.0f} [{data['rank_p05']:.0f}-{data['rank_p95']:.0f}] | "
              f"Dim: {dim}")
    
    # Top skills by dimension
    print("\n" + "=" * 60)
    print("TOP SKILLS BY DIMENSION")
    print("=" * 60)
    for dim in ['big_data', 'maths_statistics', 'coding', 'ai_ml', 'dashboard_storytelling']:
        dim_skills = [(s, d) for s, d in ssi_results.items() if d['dimension'] == dim]
        dim_skills.sort(key=lambda x: x[1]['ssi_mean'], reverse=True)
        if dim_skills:
            print(f"\n{dim.upper()}:")
            for i, (skill, data) in enumerate(dim_skills[:5], 1):
                print(f"  {i}. {skill:25s} SSI: {data['ssi_mean']:.3f}")
    
    return ssi_results

if __name__ == "__main__":
    calculate_ssi()
