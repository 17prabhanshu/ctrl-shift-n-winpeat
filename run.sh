#!/bin/bash
# run.sh - Master analytical pipeline runner
echo "Installing dependencies..."
pip3 install -r requirements.txt --break-system-packages

echo "Running full analytical pipeline..."
python3 src/skill_intelligence/skill_signal_index.py
python3 src/benchmarking/sds_forensic.py
python3 src/benchmarking/demand_reward_alignment.py
python3 src/models/interaction_test.py

echo "Generating final research documents..."
python3 generate_research_paper.py
python3 generate_md.py

echo "Pipeline execution complete! Check docs/APPROACH_NOTE.md and app_final_note.docx for the final outputs."
