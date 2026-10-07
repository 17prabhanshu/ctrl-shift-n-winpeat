# Pipeline Automation & Verification Utilities (`scripts/`)

This directory contains standalone execution and audit scripts that verify data integrity, run automated checks, and generate analytical artifacts for the Workforce Intelligence Engine.

---

## Utility Overview

| Script Name | Purpose | Key Inputs | Outputs / Artifacts | Execution Stage |
|:---|:---|:---|:---|:---|
| `profile_cleaning.py` | Audits string salary and experience parsing formats; logs verified transformation counts. | `data/raw/*.csv`, `data/raw/*.xlsx` | `data/processed/cleaning_ledger.json` | Data Engineering (Stage 2) |
| `leakage_audit.py` | Dynamically audits 6 isolation rules to verify zero shared keys and zero target leakage. | Processed datasets in `data/processed/` | `docs/LEAKAGE_AUDIT.md` | Verification (Stage 3) |
| `generate_final_evidence.py` | Reads computed benchmark JSONs, enforces limitations, and populates the evidence registry without defaults. | `reports/benchmarks/*.json` | `reports/evidence/evidence_registry.json`, `reports/evidence/evidence_audit_report.md` | Governance (Stage 7) |
| `generate_eda_figures.py` | Generates publication-ready static figures (PCA, KDE, Lorenz curve, correlation matrices). | Cleaned processed data | `reports/figures/eda/*.png` | Exploratory Analysis |
| `generate_interactive_graph.py` | Builds the interactive Vis.js force-directed skill co-occurrence network graph. | `reports/evidence/skill_graph_metrics.json` | `docs/interactive_graph.html` | Presentation Layer |

---

## Execution Instructions

All scripts can be executed individually from the project root:

```bash
# 1. Profile data formats and generate cleaning ledger
python3 scripts/profile_cleaning.py

# 2. Run automated 6-point leakage audit
python3 scripts/leakage_audit.py

# 3. Generate final evidence registry
python3 scripts/generate_final_evidence.py

# 4. Generate EDA research plots
python3 scripts/generate_eda_figures.py

# 5. Build interactive network graph
python3 scripts/generate_interactive_graph.py
```

Or execute all stages automatically via the unified runner:
```bash
./run.sh
```
