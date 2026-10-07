# Evidence Registry Report

Generated: 2026-10-07T23:49:37.648341
Total claims: 8
Accepted: 8
Rejected: 0
Pending: 0

## Claims by Dataset

### Analytics Jobs

| Claim ID | Statement | Method | Metric | Value | CI 95% | Status |
|----------|-----------|--------|--------|-------|--------|--------|
| H3-Complementarity-001 | Technical and Communication skills exhibit positive compleme... | OLS regression with HC3 robust standard errors on log salary | Interaction coefficient (T x C) | 0.0873 | [-0.031, 0.206] | accepted |
| SSI-001 | Skill 'machine learning' has the highest skill signal index.... | Skill Signal Index | ssi_mean | 0.6381 | — | accepted |

### Analytics Jobs + JDS Skills

| Claim ID | Statement | Method | Metric | Value | CI 95% | Status |
|----------|-----------|--------|--------|-------|--------|--------|
| Alignment-001 | Demand-Reward Alignment calculated across 5 dimensions witho... | Dimension-level alignment of Market Share vs JDS Log-Odds | Correlation | -0.7673 | — | accepted |

### JDS Skill Traits

| Claim ID | Statement | Method | Metric | Value | CI 95% | Status |
|----------|-----------|--------|--------|-------|--------|--------|
| JDS-ACC-001 | JDS Full Model Logistic Regression accuracy... | Logistic Regression | accuracy | 0.8650 | — | accepted |
| JDS-AUC-001 | JDS Random Forest AUC... | Random Forest | roc_auc | 0.8438 | — | accepted |

### SDS Personality

| Claim ID | Statement | Method | Metric | Value | CI 95% | Status |
|----------|-----------|--------|--------|-------|--------|--------|
| SDS-Forensic-001 | SDS target is almost perfectly separable by a depth-2 decisi... | Decision Tree (max_depth=2) with 5-fold CV | ROC-AUC | 0.9173 | — | accepted |

### SDS Personality Traits

| Claim ID | Statement | Method | Metric | Value | CI 95% | Status |
|----------|-----------|--------|--------|-------|--------|--------|
| SDS-ACC-001 | SDS Full Model Random Forest accuracy... | Random Forest | accuracy | 0.9575 | — | accepted |
| SDS-AUC-001 | SDS Multiple Seeds ROC-AUC mean... | Random Forest | roc_auc | 0.9967 | — | accepted |
