import pandas as pd
from .salary_parser import parse_ds_salary, parse_analytics_salary
from .experience_parser import parse_experience
import json
import os
from src.utils.config import PROCESSED_DIR

ledger = []

def log_transformation(dataset, column, original, new, reason, affected):
    ledger.append({
        'dataset': dataset,
        'column': column,
        'original_sample': original,
        'new_sample': new,
        'reason': reason,
        'affected_rows': affected
    })

def clean_ds_jobs(df):
    df_clean = df.copy()
    if 'avg_salary' in df_clean.columns:
        parsed = df_clean['avg_salary'].apply(parse_ds_salary)
        log_transformation('ds_jobs', 'avg_salary', '7.8L', 780000, 'Parsed LPA format', len(df_clean))
        df_clean['avg_salary_parsed'] = parsed
    return df_clean

def clean_analytics_jobs(df):
    df_clean = df.copy()
    if 'salary' in df_clean.columns:
        parsed = df_clean['salary'].apply(parse_analytics_salary)
        df_clean['salary_min'] = [p[0] for p in parsed]
        df_clean['salary_max'] = [p[1] for p in parsed]
        log_transformation('analytics_jobs', 'salary', '6to10', '(600000, 1000000)', 'Parsed range to min/max', len(df_clean))
    
    if 'experience' in df_clean.columns:
        parsed_exp = df_clean['experience'].apply(parse_experience)
        df_clean['exp_min'] = [p[0] for p in parsed_exp]
        df_clean['exp_max'] = [p[1] for p in parsed_exp]
        df_clean['exp_mid'] = [p[2] for p in parsed_exp]
        log_transformation('analytics_jobs', 'experience', '6-10 yrs', '(6, 10, 8)', 'Parsed exp range', len(df_clean))
        
    return df_clean

def save_ledger():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    with open(os.path.join(PROCESSED_DIR, 'cleaning_ledger.json'), 'w') as f:
        json.dump(ledger, f, indent=4)
