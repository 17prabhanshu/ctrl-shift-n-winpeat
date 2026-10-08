"""
Ingestion module - load all datasets with proper encoding handling.
"""
import pandas as pd
from pathlib import Path
from src.utils.config import DATASETS, RAW_DIR

def load_data(dataset_key: str) -> pd.DataFrame:
    """Load a single dataset by key."""
    path = DATASETS[dataset_key]
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    
    if path.suffix == '.csv':
        # Try multiple encodings
        for encoding in ['utf-8', 'latin1', 'cp1252']:
            try:
                return pd.read_csv(path, encoding=encoding)
            except UnicodeDecodeError:
                continue
        raise UnicodeDecodeError(f"Could not read {path} with any encoding")
    elif path.suffix == '.xlsx':
        return pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported format: {path.suffix}")

def load_all() -> dict[str, pd.DataFrame]:
    """Load all four datasets."""
    return {k: load_data(k) for k in DATASETS.keys()}

def get_dataset_info() -> dict:
    """Get shape and column info for all datasets."""
    info = {}
    for key, path in DATASETS.items():
        if path.exists():
            df = load_data(key)
            info[key] = {
                'shape': list(df.shape),
                'columns': list(df.columns),
                'dtypes': {c: str(df[c].dtype) for c in df.columns},
                'missing': int(df.isnull().sum().sum()),
                'duplicates': int(df.duplicated().sum())
            }
    return info

if __name__ == "__main__":
    dfs = load_all()
    for k, df in dfs.items():
        print(f"{k}: {df.shape}")
