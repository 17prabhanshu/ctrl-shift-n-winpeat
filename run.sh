#!/bin/bash
set -euo pipefail

# Workforce Intelligence Engine — Master Pipeline
# Runs the entire analytical DAG from raw data to final evidence.
# Any failure stops the pipeline immediately (set -e).

echo "============================================"
echo " Workforce Intelligence Engine — Full Run"
echo "============================================"

# --- Environment ---
echo "[1/7] Installing dependencies..."
pip3 install -r requirements.txt --break-system-packages -q

# --- Data Cleaning & Profiling ---
echo "[2/7] Profiling and auditing data cleaning..."
python3 scripts/profile_cleaning.py

# --- Leakage Audit ---
echo "[3/7] Running executable leakage audit..."
python3 scripts/leakage_audit.py

# --- Intelligence Engine (Market + Skill Analysis) ---
echo "[4/7] Running Skill Signal Index..."
python3 src/skill_intelligence/skill_signal_index.py

# --- ML Forensics ---
echo "[5/7] Running SDS forensic analysis..."
python3 src/benchmarking/sds_forensic.py

# --- Cross-Dataset Synthesis ---
echo "[6/7] Running Demand-Reward Alignment..."
python3 src/benchmarking/demand_reward_alignment.py
python3 src/models/interaction_test.py

# --- Evidence Registry ---
echo "[7/7] Building evidence registry..."
python3 scripts/generate_final_evidence.py

echo ""
echo "============================================"
echo " Pipeline complete."
echo " Outputs:"
echo "   data/processed/cleaning_ledger.json"
echo "   docs/LEAKAGE_AUDIT.md"
echo "   reports/evidence/evidence_registry.json"
echo "   reports/evidence/skill_signal_index.json"
echo "============================================"
