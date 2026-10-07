import json
import os

project_root = os.path.dirname(os.path.abspath(__file__))

def print_scores(path, name):
    print(f"=== {name} Scores ===")
    with open(os.path.join(project_root, path)) as f:
        bench = json.load(f)
    for model, metrics in bench.items():
        if model in ["LogisticRegression", "RandomForest", "ExtraTrees", "XGBoost"]:
            acc = metrics.get('accuracy', {}).get('mean', 0)
            auc = metrics.get('roc_auc', {}).get('mean', 0)
            f1 = metrics.get('f1', {}).get('mean', 0)
            print(f"  {model}: AUC = {auc:.3f} | Accuracy = {acc:.3f} | F1 = {f1:.3f}")

print_scores('reports/benchmarks/jds_benchmark.json', "JDS (Junior Data Scientist)")
print_scores('reports/benchmarks/sds_benchmark.json', "SDS (Senior Data Scientist)")
