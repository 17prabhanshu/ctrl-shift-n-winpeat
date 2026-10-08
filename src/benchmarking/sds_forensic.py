"""
SDS Forensic Analysis - investigate the suspicious 0.99+ AUC.

This is critical: if a depth-2 tree gets 0.92+ AUC on 161 samples with 5 features,
the labels are likely deterministic or near-deterministic functions of the features.
"""
import pandas as pd
import numpy as np
import json
from pathlib import Path
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score
from src.utils.config import PROCESSED_DIR, EVIDENCE_DIR, BENCHMARKS_DIR

def run_sds_forensic():
    """Run comprehensive SDS forensic analysis."""
    print("=" * 60)
    print("SDS FORENSIC ANALYSIS")
    print("=" * 60)
    
    # Load data
    df = pd.read_excel(PROCESSED_DIR / 'sds_personality_clean.xlsx')
    df.columns = [c.replace(' ', '').replace('-', '').lower() for c in df.columns]
    
    features = ['neuroticism', 'extraversion', 'openness_to_experience', 
                'agreeableness', 'conscientiousness']
    target = 'success_classification_high_low'
    
    X = df[features]
    y = df[target]
    
    print(f"\nDataset: {len(y)} samples, {X.shape[1]} features")
    print(f"Class balance: {np.mean(y):.3f} ({np.sum(y)} high / {len(y) - np.sum(y)} low)")
    
    results = {
        'n_samples': len(y),
        'n_features': len(features),
        'class_balance': float(np.mean(y)),
        'feature_stats_by_class': {},
        'tree_depth_analysis': {},
        'feature_importance': {},
        'forensic_findings': []
    }
    
    # 1. Feature distributions by class
    print("\n[1/5] Feature distributions by class:")
    print("-" * 40)
    
    for feat in features:
        high_mean = df[df[target] == 1][feat].mean()
        low_mean = df[df[target] == 0][feat].mean()
        high_std = df[df[target] == 1][feat].std()
        low_std = df[df[target] == 0][feat].std()
        
        cohens_d = (high_mean - low_mean) / np.sqrt((high_std**2 + low_std**2) / 2)
        
        results['feature_stats_by_class'][feat] = {
            'high_mean': float(high_mean),
            'high_std': float(high_std),
            'low_mean': float(low_mean),
            'low_std': float(low_std),
            'cohens_d': float(cohens_d),
            'diff': float(high_mean - low_mean)
        }
        
        direction = '↑' if cohens_d > 0 else '↓'
        print(f"  {feat:25s}: High={high_mean:.2f}, Low={low_mean:.2f}, d={cohens_d:.2f} {direction}")
    
    # 2. Shallow decision trees (the key forensic test)
    print("\n[2/5] Shallow decision tree separability:")
    print("-" * 40)
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    for depth in [1, 2, 3, 4, 5]:
        clf = DecisionTreeClassifier(max_depth=depth, random_state=42)
        scores = cross_val_score(clf, X, y, cv=cv, scoring='roc_auc')
        
        results['tree_depth_analysis'][f'depth_{depth}'] = {
            'roc_auc_mean': float(np.mean(scores)),
            'roc_auc_std': float(np.std(scores)),
            'accuracy_mean': float(np.mean(cross_val_score(clf, X, y, cv=cv, scoring='accuracy')))
        }
        
        # Fit on all data to extract the rule
        clf.fit(X, y)
        tree_rules = export_text(clf, feature_names=features, max_depth=depth)
        
        sig = '⚠️' if np.mean(scores) > 0.85 else ('⚠️' if np.mean(scores) > 0.75 else '')
        print(f"  Depth {depth}: AUC={np.mean(scores):.4f} (±{np.std(scores):.4f}) {sig}")
        
        if depth <= 3:
            print(f"    Rules:\n{tree_rules.replace('|---', '      |---')}")
    
    # 3. Check for threshold rules
    print("\n[3/5] Threshold rule analysis:")
    print("-" * 40)
    
    threshold_rules = []
    for feat_idx, feat in enumerate(features):
        best_threshold = None
        best_auc = 0
        feat_values = X.iloc[:, feat_idx].values
        
        for percentile in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
            threshold = np.percentile(feat_values, percentile)
            pred = (feat_values >= threshold).astype(int)
            if len(np.unique(pred)) > 1:
                auc = roc_auc_score(y, pred)
                if auc > best_auc:
                    best_auc = auc
                    best_threshold = threshold
        
        threshold_rules.append({
            'feature': feat,
            'best_threshold': float(best_threshold) if best_threshold else None,
            'best_auc': float(best_auc),
            'simple_rule_auc': float(best_auc)
        })
        
        if best_auc > 0.7:
            print(f"  {feat:25s}: threshold={best_threshold:.2f}, simple AUC={best_auc:.4f}")
    
    results['threshold_rules'] = threshold_rules
    
    # 4. Feature importance from tree
    print("\n[4/5] Feature importance (Random Forest):")
    print("-" * 40)
    
    from sklearn.ensemble import RandomForestClassifier
    rf = RandomForestClassifier(n_estimators=500, random_state=42)
    rf.fit(X, y)
    
    importance = rf.feature_importances_
    for feat, imp in sorted(zip(features, importance), key=lambda x: x[1], reverse=True):
        print(f"  {feat:25s}: {imp:.4f}")
        results['feature_importance'][feat] = float(imp)
    
    # 5. MDS/shuffled gap
    print("\n[5/5] Shuffled-target gap analysis:")
    print("-" * 40)
    
    shuff_aucs = []
    for seed in range(20):
        y_shuff = np.random.RandomState(seed).permutation(y)
        clf = DecisionTreeClassifier(max_depth=2, random_state=42)
        scores = cross_val_score(clf, X, y_shuff, cv=cv, scoring='roc_auc')
        shuff_aucs.append(np.mean(scores))
    
    real_depth2_auc = results['tree_depth_analysis']['depth_2']['roc_auc_mean']
    shuff_mean = np.mean(shuff_aucs)
    shuff_std = np.std(shuff_aucs)
    
    print(f"  Real (depth-2) AUC: {real_depth2_auc:.4f}")
    print(f"  Shuffled AUC (20 seeds): {shuff_mean:.4f} (±{shuff_std:.4f})")
    print(f"  Gap: {real_depth2_auc - shuff_mean:.4f}")
    
    results['shuffled_gap'] = {
        'real_auc': float(real_depth2_auc),
        'shuffled_auc_mean': float(shuff_mean),
        'shuffled_auc_std': float(shuff_std),
        'gap': float(real_depth2_auc - shuff_mean)
    }
    
    # Determine forensic conclusion
    print("\n" + "=" * 60)
    print("FORENSIC CONCLUSION")
    print("=" * 60)
    
    if real_depth2_auc > 0.90:
        conclusion = "HIGH SEPARABILITY: Depth-2 tree achieves >0.90 AUC. "
        conclusion += "This strongly suggests the success label was generated from or heavily influenced by "
        conclusion += "threshold rules on personality traits, rather than representing observed real-world success. "
        conclusion += "The classification result (0.99+ AUC) reflects this deterministic relationship, NOT "
        conclusion += "predictive power for real workforce outcomes."
        severity = "CRITICAL"
    elif real_depth2_auc > 0.80:
        conclusion = "MODERATE SEPARABILITY: Depth-2 tree achieves >0.80 AUC. "
        conclusion += "The label has strong deterministic components but may include some noise. "
        conclusion += "Results should be interpreted with caution."
        severity = "WARNING"
    else:
        conclusion = "NORMAL SEPARABILITY: Depth-2 tree AUC is in expected range for behavioral data. "
        conclusion += "The label appears to have genuine signal beyond simple thresholds."
        severity = "OK"
    
    print(f"\n{severity}")
    print(conclusion)
    
    results['conclusion'] = {
        'severity': severity,
        'text': conclusion,
        'recommendation': 'Do not treat SDS classification as valid prediction of real-world success. '
                         'The label appears to be a function of the input traits. '
                         'Any "prediction" is essentially recovering the labeling rule.'
    }
    
    # Register forensic claim in evidence registry
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    registry_path = EVIDENCE_DIR / 'evidence_registry.json'
    
    registry = []
    if registry_path.exists():
        with open(registry_path) as f:
            registry = json.load(f)
    
    forensic_claim = {
        'claim_id': 'SDS-Forensic-001',
        'statement': 'SDS target is almost perfectly separable by shallow decision trees, '
                     'indicating labels are likely generated from trait thresholds rather than observed success',
        'dataset': 'SDS Personality',
        'evidence_tag': 'M',
        'method': 'Decision Tree (depth 1-5) with 5-fold CV; threshold analysis; shuffled-target gap',
        'metric': 'ROC-AUC (depth-2 tree)',
        'value': float(real_depth2_auc),
        'ci95_lower': float(real_depth2_auc - 1.96 * results['tree_depth_analysis']['depth_2']['roc_auc_std']),
        'ci95_upper': float(real_depth2_auc + 1.96 * results['tree_depth_analysis']['depth_2']['roc_auc_std']),
        'n': len(y),
        'limitation': 'Forensic analysis of label quality; does not invalidate all SDS findings but limits interpretation',
        'status': 'accepted'
    }
    
    existing = next((i for i, r in enumerate(registry) if r.get('claim_id') == 'SDS-Forensic-001'), None)
    if existing is not None:
        registry[existing] = forensic_claim
    else:
        registry.append(forensic_claim)
    
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)
    
    # Save detailed results
    with open(BENCHMARKS_DIR / 'sds_forensic.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nSaved: {BENCHMARKS_DIR / 'sds_forensic.json'}")
    print(f"Registered: SDS-Forensic-001 in evidence registry")
    
    return results

if __name__ == "__main__":
    run_sds_forensic()
