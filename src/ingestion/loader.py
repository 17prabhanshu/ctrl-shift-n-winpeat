import pandas as pd
from src.utils.config import DATASETS

def load_data(dataset_key):
    path = DATASETS[dataset_key]
    if path.endswith('.csv'):
        # trying different encodings just in case
        try:
            return pd.read_csv(path, encoding='utf-8')
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding='latin1')
    elif path.endswith('.xlsx'):
        return pd.read_excel(path)
    else:
        raise ValueError("Unsupported file format")

def load_all():
    return {k: load_data(k) for k in DATASETS.keys()}
