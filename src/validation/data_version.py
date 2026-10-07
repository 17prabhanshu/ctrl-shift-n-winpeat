import hashlib
import os
import json
from src.utils.config import DATASETS, REPORTS_DIR

def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def version_datasets(dfs):
    versions = {}
    for key, path in DATASETS.items():
        if os.path.exists(path):
            df = dfs[key]
            versions[key] = {
                'file_hash': get_file_hash(path),
                'row_count': len(df),
                'col_count': len(df.columns),
                'schema': {col: str(dtype) for col, dtype in df.dtypes.items()}
            }
    
    with open(os.path.join(REPORTS_DIR, 'dataset_versions.json'), 'w') as f:
        json.dump(versions, f, indent=4)
    return versions
