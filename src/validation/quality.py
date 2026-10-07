import pandas as pd
import json
import os
from src.utils.config import REPORTS_DIR

def run_quality_checks(dfs):
    report = {}
    
    for name, df in dfs.items():
        report[name] = {
            'missing_values': df.isnull().sum().to_dict(),
            'duplicate_rows': int(df.duplicated().sum()),
        }
    
    with open(os.path.join(REPORTS_DIR, 'data_quality_report.json'), 'w') as f:
        json.dump(report, f, indent=4)
        
    with open(os.path.join(REPORTS_DIR, 'data_quality_report.md'), 'w') as f:
        f.write("# Data Quality Report\n\n")
        for k, v in report.items():
            f.write(f"## {k}\n")
            f.write(f"- Duplicates: {v['duplicate_rows']}\n")
            f.write("- Missing Values:\n")
            for col, mv in v['missing_values'].items():
                if mv > 0:
                    f.write(f"  - {col}: {mv}\n")
    return report
