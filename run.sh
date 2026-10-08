#!/bin/bash
# run.sh - Master analytical pipeline runner
# Team ctrl shift n | SAS CU Hackathon 2026

set -e

echo "============================================================"
echo "WORKFORCE INTELLIGENCE ENGINE - FULL PIPELINE"
echo "============================================================"

# Step 1: Install dependencies (if needed)
echo ""
echo "[1/7] Checking dependencies..."
pip3 install -r requirements.txt --quiet --break-system-packages 2>/dev/null || true

# Step 2: Clean data
echo ""
echo "[2/7] Running data cleaning pipeline..."
python3 -m src.cleaning.cleaner

# Step 3: Process skills
echo ""
echo "[3/7] Running skill intelligence engine..."
python3 -m src.skill_intelligence.skill_engine

# Step 4: Market analysis
echo ""
echo "[4/7] Running market analysis..."
python3 -m src.market_intelligence.market_analysis
python3 -m src.market_intelligence.market_statistics

# Step 5: Benchmarks (takes longer)
echo ""
echo "[5/7] Running benchmarks (this may take a few minutes)..."
python3 -m src.models.benchmark_engine

# Step 6: Forensic analyses
echo ""
echo "[6/7] Running forensic analyses..."
python3 -m src.benchmarking.sds_forensic
python3 -m src.models.interaction_test

# Step 7: Skill signal index
echo ""
echo "[7/7] Computing skill signal index..."
python3 -m src.skill_intelligence.skill_signal_index

echo ""
echo "============================================================"
echo "PIPELINE COMPLETE!"
echo "============================================================"
echo ""
echo "Evidence Registry: reports/evidence/evidence_registry.json"
echo "Market Analysis: reports/evidence/market_analysis.json"
echo "Skill Analysis: reports/evidence/skill_analysis.json"
echo "JDS Benchmark: reports/benchmarks/jds_benchmark.json"
echo "SDS Benchmark: reports/benchmarks/sds_benchmark.json"
echo "SDS Forensic: reports/benchmarks/sds_forensic.json"
echo "JDS Interaction: reports/benchmarks/jds_interaction.json"
echo ""
echo "To run the Career Navigator app:"
echo "  cd app && streamlit run main.py"
echo ""
echo "To view figures: open reports/figures/"
