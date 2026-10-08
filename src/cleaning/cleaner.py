"""
Data cleaning module with full ledger tracking.
Every transformation is recorded for reproducibility.
"""
import json
import pandas as pd
import numpy as np
from pathlib import Path
from .salary_parser import clean_salary_column, parse_ds_salary, parse_analytics_salary
from .experience_parser import clean_experience_column, parse_experience
from src.utils.config import (
    PROCESSED_DIR, DATASETS, categorize_role, 
    SKILL_TAXONOMY, NON_TECHNICAL_SKILLS
)

# Cleaning ledger - records every transformation
cleaning_ledger = []

def log_transformation(dataset: str, action: str, details: dict):
    """Record a cleaning transformation."""
    cleaning_ledger.append({
        'dataset': dataset,
        'action': action,
        'timestamp': pd.Timestamp.now().isoformat(),
        'details': details
    })

def clean_column_names(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    """Normalize column names to snake_case, preserving originals."""
    df = df.copy()
    original_cols = list(df.columns)
    
    def to_snake(name):
        # Replace spaces and special chars with underscores
        name = str(name).strip()
        name = name.replace(' ', '_').replace('-', '_').replace('.', '_')
        # Remove special characters but keep alphanumeric and underscore
        name = ''.join(c if c.isalnum() or c == '_' else '' for c in name)
        # Lowercase
        name = name.lower()
        return name
    
    df.columns = [to_snake(c) for c in df.columns]
    
    log_transformation(dataset_name, 'column_rename', {
        'original': original_cols,
        'normalized': list(df.columns),
        'mapping': dict(zip(original_cols, df.columns))
    })
    
    return df

def audit_schema(df: pd.DataFrame, dataset_name: str) -> dict:
    """Audit the schema and return quality metrics."""
    return {
        'dataset': dataset_name,
        'shape': list(df.shape),
        'columns': list(df.columns),
        'dtypes': {c: str(df[c].dtype) for c in df.columns},
        'missing_counts': df.isnull().sum().to_dict(),
        'missing_rates': (df.isnull().sum() / len(df)).to_dict(),
        'duplicate_rows': int(df.duplicated().sum()),
        'unique_counts': {c: df[c].nunique() for c in df.columns if df[c].dtype == 'object'}
    }

def clean_ds_jobs(df: pd.DataFrame) -> pd.DataFrame:
    """Clean DataScience Jobs dataset."""
    df = df.copy()
    dataset = 'ds_jobs'
    
    # 1. Normalize column names
    df = clean_column_names(df, dataset)
    
    # 2. Parse salary (format: "7.8L" = 7.8 LPA)
    df['avg_salary_inr'] = df['avg_salary'].apply(parse_ds_salary)
    df['salary_disclosed'] = df['avg_salary_inr'].notna()
    
    log_transformation(dataset, 'salary_parse', {
        'column': 'avg_salary',
        'format': 'LPA with L suffix (e.g., 7.8L = 780,000 INR)',
        'parsed_column': 'avg_salary_inr',
        'disclosed_rate': float(df['salary_disclosed'].mean()),
        'rows_processed': len(df)
    })
    
    # 3. Parse experience
    if 'min_experience' in df.columns:
        df['exp_numeric'] = pd.to_numeric(df['min_experience'], errors='coerce')
        # Flag implausible values
        df['exp_valid'] = df['exp_numeric'].notna() & (df['exp_numeric'] <= 40)
        log_transformation(dataset, 'experience_parse', {
            'column': 'min_experience',
            'valid_rate': float(df['exp_valid'].mean())
        })
    
    # 4. Normalize job titles
    df['job_title_normalized'] = df['job_title'].str.lower().str.strip()
    
    # 5. Categorize roles
    df['role_family'] = df['job_title'].apply(categorize_role)
    
    # 6. Log company info
    company_counts = df['company_name'].value_counts()
    log_transformation(dataset, 'company_audit', {
        'unique_companies': int(df['company_name'].nunique()),
        'total_rows': len(df),
        'repeated_reference_nos': int(df['reference_no'].duplicated().sum()) if 'reference_no' in df.columns else 0
    })
    
    return df

def clean_analytics_jobs(df: pd.DataFrame) -> pd.DataFrame:
    """Clean Analytics Jobs dataset."""
    df = df.copy()
    dataset = 'analytics_jobs'
    
    # 1. Normalize column names
    df = clean_column_names(df, dataset)
    
    # 2. Parse salary range
    salary_parsed = df['salary'].apply(parse_analytics_salary)
    df['salary_min_inr'] = [s[0] for s in salary_parsed]
    df['salary_max_inr'] = [s[1] for s in salary_parsed]
    df['salary_disclosed'] = df['salary_min_inr'].notna()
    
    # Calculate midpoint where both exist
    mask = df['salary_min_inr'].notna() & df['salary_max_inr'].notna()
    df['salary_mid_inr'] = np.nan
    df.loc[mask, 'salary_mid_inr'] = (df.loc[mask, 'salary_min_inr'] + df.loc[mask, 'salary_max_inr']) / 2
    
    # Salary range ratio (for disclosure analysis)
    df['salary_range_ratio'] = np.nan
    valid_range = mask & (df['salary_mid_inr'] > 0)
    df.loc[valid_range, 'salary_range_ratio'] = (
        (df.loc[valid_range, 'salary_max_inr'] - df.loc[valid_range, 'salary_min_inr']) / 
        df.loc[valid_range, 'salary_mid_inr']
    )
    
    log_transformation(dataset, 'salary_parse', {
        'column': 'salary',
        'format': 'Range format "XtoY" or "X-Y" in LPA',
        'disclosed_rate': float(df['salary_disclosed'].mean()),
        'median_range_ratio': float(df.loc[valid_range, 'salary_range_ratio'].median()) if valid_range.sum() > 0 else None
    })
    
    # 3. Parse experience range
    df = clean_experience_column(df, 'experience')
    
    log_transformation(dataset, 'experience_parse', {
        'column': 'experience',
        'valid_rate': float(df['experience_valid'].mean()) if 'experience_valid' in df.columns else None
    })
    
    # 4. Categorize roles
    df['role_family'] = df['job_desig'].apply(categorize_role)
    
    # 5. Parse location
    if 'location' in df.columns:
        df['location_primary'] = df['location'].str.split(',').str[0].str.strip()
    
    # 6. Process key_skills (initial tokenization - full processing in skill module)
    df['skills_list'] = df['key_skills'].apply(
        lambda x: [s.strip() for s in str(x).lower().split(',') if s.strip()] 
        if pd.notna(x) else []
    )
    df['n_skills'] = df['skills_list'].apply(len)
    
    log_transformation(dataset, 'skills_initial', {
        'total_skill_mentions': int(df['n_skills'].sum()),
        'avg_skills_per_posting': float(df['n_skills'].mean()),
        'postings_with_skills': int((df['n_skills'] > 0).sum())
    })
    
    return df

def clean_jds_skills(df: pd.DataFrame) -> pd.DataFrame:
    """Clean JDS Skills dataset."""
    df = df.copy()
    dataset = 'jds_skills'
    
    # Normalize column names
    df = clean_column_names(df, dataset)
    
    # Verify scores are in 1-5 range
    skill_cols = [c for c in df.columns if 'skills' in c or 'skill' in c]
    for col in skill_cols:
        df[f'{col}_valid'] = df[col].between(1, 5)
    
    # Check for duplicates
    if 'id' in df.columns:
        n_dupes = df['id'].duplicated().sum()
        if n_dupes > 0:
            log_transformation(dataset, 'duplicate_check', {
                'duplicate_ids': int(n_dupes),
                'action': 'investigate'
            })
    
    log_transformation(dataset, 'schema_audit', {
        'n_records': len(df),
        'n_features': len(skill_cols),
        'score_range_valid': bool(df[skill_cols].apply(lambda x: x.between(1, 5)).all().all()) if skill_cols else None
    })
    
    return df

def clean_sds_personality(df: pd.DataFrame) -> pd.DataFrame:
    """Clean SDS Personality dataset."""
    df = df.copy()
    dataset = 'sds_personality'
    
    # Normalize column names
    df = clean_column_names(df, dataset)
    
    # Trait columns (Big Five)
    trait_cols = ['neuroticism', 'extraversion', 'openness_to_experience', 
                  'agreeableness', 'conscientiousness']
    
    # Check normalization (should be standardized)
    for col in trait_cols:
        if col in df.columns:
            mean = df[col].mean()
            std = df[col].std()
            log_transformation(dataset, 'normality_check', {
                'trait': col,
                'mean': round(float(mean), 3),
                'std': round(float(std), 3),
                'min': round(float(df[col].min()), 3),
                'max': round(float(df[col].max()), 3)
            })
    
    # Check for duplicates
    if 'id' in df.columns:
        n_dupes = df['id'].duplicated().sum()
        if n_dupes > 0:
            log_transformation(dataset, 'duplicate_check', {
                'duplicate_ids': int(n_dupes)
            })
    
    log_transformation(dataset, 'schema_audit', {
        'n_records': len(df),
        'n_traits': len(trait_cols),
        'target_column': 'success_classification_high_low' if 'success_classification_high_low' in df.columns else None,
        'class_balance': df['success_classification_high_low'].value_counts(normalize=True).to_dict() 
            if 'success_classification_high_low' in df.columns else None
    })
    
    return df

def save_cleaned_data(dfs: dict, ledger: list):
    """Save cleaned datasets and ledger."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    for name, df in dfs.items():
        out_path = PROCESSED_DIR / f"{name}_clean.csv"
        df.to_csv(out_path, index=False)
        print(f"Saved: {out_path}")
    
    # Save ledger
    ledger_path = PROCESSED_DIR / "cleaning_ledger.json"
    with open(ledger_path, 'w') as f:
        json.dump(ledger, f, indent=2)
    print(f"Saved ledger: {ledger_path}")

def run_full_cleaning():
    """Run the complete cleaning pipeline."""
    from src.ingestion.loader import load_all
    
    print("=" * 60)
    print("DATA CLEANING PIPELINE")
    print("=" * 60)
    
    # Load raw data
    print("\n[1/5] Loading raw datasets...")
    raw_dfs = load_all()
    for name, df in raw_dfs.items():
        print(f"  {name}: {df.shape}")
    
    # Clean each dataset
    print("\n[2/5] Auditing schemas...")
    for name, df in raw_dfs.items():
        audit = audit_schema(df, name)
        print(f"  {name}: {audit['shape']} rows, {audit['missing_counts']}")
    
    print("\n[3/5] Cleaning datasets...")
    clean_dfs = {
        'ds_jobs': clean_ds_jobs(raw_dfs['ds_jobs']),
        'analytics_jobs': clean_analytics_jobs(raw_dfs['analytics_jobs']),
        'jds_skills': clean_jds_skills(raw_dfs['jds_skills']),
        'sds_personality': clean_sds_personality(raw_dfs['sds_personality'])
    }
    
    print("\n[4/5] Saving cleaned data...")
    save_cleaned_data(clean_dfs, cleaning_ledger)
    
    print("\n[5/5] Cleaning summary...")
    print(f"  Total transformations logged: {len(cleaning_ledger)}")
    for entry in cleaning_ledger:
        print(f"  - [{entry['dataset']}] {entry['action']}")
    
    return clean_dfs

if __name__ == "__main__":
    run_full_cleaning()
