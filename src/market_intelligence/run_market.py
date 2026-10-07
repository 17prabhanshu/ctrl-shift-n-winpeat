import os
import sys

def run_all():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    scripts = [
        os.path.join(base_dir, 'market_intelligence', 'market_analysis.py'),
        os.path.join(base_dir, 'skill_intelligence', 'skill_engine.py'),
        os.path.join(base_dir, 'skill_intelligence', 'skill_graph.py'),
        os.path.join(base_dir, 'skill_intelligence', 'skill_signal_index.py'),
        os.path.join(base_dir, 'nlp', 'nlp_benchmark.py'),
        os.path.join(base_dir, 'agents', 'knowledge_graph.py')
    ]
    
    for script in scripts:
        print(f"Running {script}...")
        os.system(f"python3 {script}")

if __name__ == '__main__':
    run_all()
