"""
JDS Interaction Test (H4) - storytelling × maths-stats interaction.

This is the key hypothesis: do technical and communication skills
show complementarity in junior salary hikes?
"""
import pandas as pd
import numpy as np
import json
import statsmodels.api as sm
import statsmodels.formula.api as smf
from pathlib import Path
from src.utils.config import PROCESSED_DIR, EVIDENCE_DIR, BENCHMARKS_DIR

def test_jds_interaction():
    """Test H4: storytelling × maths-stats interaction in JDS hike label."""
    print("=" * 60)
    print("H4: JUNIOR CAREER COMPLEMENTARITY (JDS)")
    print("=" * 60)
    
    # Load data
    df = pd.read_excel(PROCESSED_DIR / 'jds_skills_clean.xlsx')
    # Normalize column names
    df.columns = [c.replace(' ', '').replace('-', '').lower() for c in df.columns]
    
    # Use columns as-is (they're already normalized)
    col_map = {}
    for col in df.columns:
        if 'big_data' in col:
            col_map[col] = 'big_data'
        elif 'maths' in col:
            col_map[col] = 'maths_stats'
        elif col == 'coding_skills':
            col_map[col] = 'coding'
        elif 'ai' in col and 'ml' in col:
            col_map[col] = 'ai_ml'
        elif 'dashboard' in col or 'story' in col:
            col_map[col] = 'storytelling'
    
    df = df.rename(columns=col_map)
    features = ['big_data', 'maths_stats', 'coding', 'ai_ml', 'storytelling']
    target = 'salary_hike_high_or_low'
    
    X = df[features]
    y = df[target]
    
    print(f"\nDataset: {len(y)} samples")
    print(f"Class balance: {np.mean(y):.3f} ({np.sum(y)} high / {len(y) - np.sum(y)} low)")
    print(f"\nFeature correlations with target:")
    for feat in features:
        corr = np.corrcoef(df[feat], y)[0, 1]
        print(f"  {feat:20s}: {corr:.3f}")
    
    results = {
        'n': len(y),
        'class_balance': float(np.mean(y)),
        'models': {},
        'interaction_test': {},
        'power_analysis': {}
    }
    
    # 1. Baseline models
    print("\n[1/4] Logistic Regression (additive):")
    print("-" * 40)
    
    # Additive model
    X_additive = sm.add_constant(X)
    try:
        logit_add = sm.Logit(y, X_additive).fit(disp=0)
        
        results['models']['logistic_additive'] = {
            'auc': None,  # Would need CV
            'coefficients': {feat: float(logit_add.params[feat]) for feat in features},
            'pvalues': {feat: float(logit_add.pvalues[feat]) for feat in features},
            'summary': logit_add.summary().as_csv()
        }
        
        print(f"  Storytelling coef: {logit_add.params['storytelling']:.4f} (p={logit_add.pvalues['storytelling']:.4f})")
        print(f"  Maths/Stats coef: {logit_add.params['maths_stats']:.4f} (p={logit_add.pvalues['maths_stats']:.4f})")
    except Exception as e:
        print(f"  Error: {e}")
        results['models']['logistic_additive'] = {'error': str(e)}
    
    # 2. Interaction model (storytelling × maths_stats)
    print("\n[2/4] Logistic Regression (with interaction):")
    print("-" * 40)
    
    df['storytelling_x_maths'] = df['storytelling'] * df['maths_stats']
    
    X_interaction = df[['big_data', 'maths_stats', 'coding', 'ai_ml', 'storytelling', 'storytelling_x_maths']]
    X_interaction = sm.add_constant(X_interaction)
    
    try:
        logit_int = sm.Logit(y, X_interaction).fit(disp=0)
        
        interaction_coef = logit_int.params['storytelling_x_maths']
        interaction_p = logit_int.pvalues['storytelling_x_maths']
        
        results['models']['logistic_interaction'] = {
            'coefficients': {feat: float(logit_int.params[feat]) for feat in features + ['storytelling_x_maths']},
            'pvalues': {feat: float(logit_int.pvalues[feat]) for feat in features + ['storytelling_x_maths']},
            'interaction_coef': float(interaction_coef),
            'interaction_p': float(interaction_p)
        }
        
        print(f"  Interaction (storytelling × maths_stats): {interaction_coef:.4f} (p={interaction_p:.4f})")
        print(f"  Storytelling main: {logit_int.params['storytelling']:.4f} (p={logit_int.pvalues['storytelling']:.4f})")
        print(f"  Maths/Stats main: {logit_int.params['maths_stats']:.4f} (p={logit_int.pvalues['maths_stats']:.4f})")
        
    except Exception as e:
        print(f"  Error: {e}")
        results['models']['logistic_interaction'] = {'error': str(e)}
        interaction_coef, interaction_p = 0, 1
    
    # 3. Likelihood Ratio Test
    print("\n[3/4] Likelihood Ratio Test (additive vs interaction):")
    print("-" * 40)
    
    try:
        # LRT
        lrt_stat = 2 * (logit_int.llf - logit_add.llf)
        lrt_df = 1  # One additional parameter
        from scipy.stats import chi2
        lrt_p = 1 - chi2.cdf(lrt_stat, lrt_df)
        
        results['interaction_test'] = {
            'lrt_statistic': float(lrt_stat),
            'lrt_df': lrt_df,
            'lrt_p_value': float(lrt_p),
            'significant': bool(lrt_p < 0.05),
            'interpretation': 'Interaction improves model fit' if lrt_p < 0.05 else 'No significant improvement from interaction'
        }
        
        print(f"  LRT statistic: {lrt_stat:.4f}")
        print(f"  LRT p-value: {lrt_p:.4f}")
        print(f"  Significant: {lrt_p < 0.05}")
        
    except Exception as e:
        print(f"  Error: {e}")
        results['interaction_test'] = {'error': str(e)}
    
    # 4. Bootstrap confidence interval for interaction
    print("\n[4/4] Bootstrap CI for interaction coefficient (2000 reps):")
    print("-" * 40)
    
    n_bootstrap = 2000
    bootstrap_coefs = []
    
    np.random.seed(42)
    for i in range(n_bootstrap):
        idx = np.random.choice(len(y), size=len(y), replace=True)
        X_boot = X_interaction.iloc[idx]
        y_boot = y[idx]
        
        try:
            # Check if we have both classes
            if len(np.unique(y_boot)) < 2:
                continue
            
            model_boot = sm.Logit(y_boot, X_boot).fit(disp=0)
            bootstrap_coefs.append(model_boot.params['storytelling_x_maths'])
        except:
            continue
    
    if bootstrap_coefs:
        bootstrap_coefs = np.array(bootstrap_coefs)
        ci_lower = np.percentile(bootstrap_coefs, 2.5)
        ci_upper = np.percentile(bootstrap_coefs, 97.5)
        bootstrap_mean = np.mean(bootstrap_coefs)
        
        results['interaction_test']['bootstrap_ci'] = {
            'n_bootstrap': len(bootstrap_coefs),
            'mean': float(bootstrap_mean),
            'ci95_lower': float(ci_lower),
            'ci95_upper': float(ci_upper),
            'includes_zero': bool(ci_lower <= 0 <= ci_upper)
        }
        
        print(f"  Bootstrap mean: {bootstrap_mean:.4f}")
        print(f"  95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
        print(f"  Includes zero: {ci_lower <= 0 <= ci_upper}")
    
    # 5. Minimum Detectable Effect (power analysis)
    print("\n[Power Analysis] Minimum Detectable Effect:")
    print("-" * 40)
    
    # For n=139, alpha=0.05, power=0.80
    # Approximate MDE for interaction in logistic regression
    # Using rule of thumb: need ~10-20 events per parameter
    n_events = np.sum(y)
    n_params = 7  # 5 main + intercept + interaction
    
    mde_estimate = 0.5  # Approximate - would need simulation for precise
    results['power_analysis'] = {
        'n_events': int(n_events),
        'n_params': n_params,
        'rule_of_thumb_events_per_param': float(n_events / n_params),
        'mde_estimate': 'Large effects only detectable with n=139; interaction effects < 0.5 log-odds likely underpowered',
        'note': 'Proper power simulation requires 2000+ replicates of synthetic data generation'
    }
    
    print(f"  Events: {n_events}, Parameters: {n_params}")
    print(f"  Events/param: {n_events/n_params:.1f} (rule of thumb: 10-20 needed)")
    print(f"  MDE: Large effects only - interaction coef < 0.5 likely underpowered")
    
    # Register claim in evidence registry
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    registry_path = EVIDENCE_DIR / 'evidence_registry.json'
    
    registry = []
    if registry_path.exists():
        with open(registry_path) as f:
            registry = json.load(f)
    
    # Determine verdict
    ci_includes_zero = results['interaction_test'].get('bootstrap_ci', {}).get('includes_zero', True)
    lrt_significant = results['interaction_test'].get('significant', False)
    
    if lrt_significant and not ci_includes_zero:
        verdict = 'supported'
        statement = 'Storytelling × Maths/Stats interaction improves prediction of JDS salary hike'
    elif lrt_significant:
        verdict = 'partial'
        statement = 'Interaction model fits better but CI includes zero - suggestive but not conclusive'
    else:
        verdict = 'not_supported'
        statement = 'No evidence for storytelling × maths_stats interaction in JDS hike prediction'
    
    claim = {
        'claim_id': 'H4-Interaction-001',
        'statement': statement,
        'dataset': 'Job Description Success (JDS)',
        'evidence_tag': 'M',
        'method': 'Logistic regression with storytelling × maths_stats interaction; LRT; 2000-bootstrap CI',
        'metric': 'Interaction coefficient (log-odds); LRT p-value',
        'value': float(interaction_coef) if 'interaction_coef' in dir() else None,
        'ci95_lower': float(ci_lower) if 'ci_lower' in dir() else None,
        'ci95_upper': float(ci_upper) if 'ci_upper' in dir() else None,
        'n': len(y),
        'limitation': f'n={len(y)}; {"CI includes zero" if ci_includes_zero else "CI excludes zero"}; '
                     f'LRT p={lrt_p:.4f}; '
                     'association only; MDE large due to small sample',
        'status': 'accepted'
    }
    
    existing = next((i for i, r in enumerate(registry) if r.get('claim_id') == 'H4-Interaction-001'), None)
    if existing is not None:
        registry[existing] = claim
    else:
        registry.append(claim)
    
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)
    
    # Save detailed results
    with open(BENCHMARKS_DIR / 'jds_interaction.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"H4 VERDICT: {verdict.upper()}")
    print(f"{'='*60}")
    print(f"\nSaved: {BENCHMARKS_DIR / 'jds_interaction.json'}")
    
    return results

if __name__ == "__main__":
    test_jds_interaction()
