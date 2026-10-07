import os
import subprocess
import json

def generate_markdown_report(json_file, md_file, title):
    if not os.path.exists(json_file):
        return
    with open(json_file, "r") as f:
        data = json.load(f)
        
    with open(md_file, "w") as f:
        f.write(f"# {title}\n\n")
        f.write("```json\n")
        f.write(json.dumps(data, indent=4))
        f.write("\n```\n")

if __name__ == "__main__":
    scripts = [
        "src/models/benchmark_engine.py",
        "src/ensembles/model_council.py",
        "src/calibration/calibrator.py",
        "src/explainability/explainer.py",
        "src/benchmarking/ablation.py",
        "src/benchmarking/robustness.py"
    ]
    
    for script in scripts:
        print(f"Running {script}...")
        subprocess.run(["python3", script], check=True)
        
    print("Generating reports...")
    generate_markdown_report("reports/benchmarks/jds_benchmark.json", "reports/benchmarks/jds_benchmark.md", "JDS Benchmark Report")
    generate_markdown_report("reports/benchmarks/sds_benchmark.json", "reports/benchmarks/sds_benchmark.md", "SDS Benchmark Report")
    
    # Combine ablation
    ablation_jds = json.load(open("reports/benchmarks/ablation_jds.json")) if os.path.exists("reports/benchmarks/ablation_jds.json") else {}
    ablation_sds = json.load(open("reports/benchmarks/ablation_sds.json")) if os.path.exists("reports/benchmarks/ablation_sds.json") else {}
    with open("reports/benchmarks/ablation_report.md", "w") as f:
        f.write("# Ablation Report\n\n## JDS\n```json\n" + json.dumps(ablation_jds, indent=4) + "\n```\n")
        f.write("\n## SDS\n```json\n" + json.dumps(ablation_sds, indent=4) + "\n```\n")
        
    # Combine robustness
    rob_jds = json.load(open("reports/benchmarks/robustness_jds.json")) if os.path.exists("reports/benchmarks/robustness_jds.json") else {}
    rob_sds = json.load(open("reports/benchmarks/robustness_sds.json")) if os.path.exists("reports/benchmarks/robustness_sds.json") else {}
    with open("reports/benchmarks/robustness_report.md", "w") as f:
        f.write("# Robustness Report\n\n## JDS\n```json\n" + json.dumps(rob_jds, indent=4) + "\n```\n")
        f.write("\n## SDS\n```json\n" + json.dumps(rob_sds, indent=4) + "\n```\n")
        
    print("All tasks completed.")
