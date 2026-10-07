import re
import pandas as pd
import numpy as np

def parse_ds_salary(val):
    if pd.isna(val):
        return np.nan
    val = str(val).strip().upper()
    m = re.match(r'^([\d\.]+)\s*L$', val)
    if m:
        try:
            return float(m.group(1)) * 100000
        except:
            return np.nan
    return np.nan

def parse_analytics_salary(val):
    if pd.isna(val):
        return np.nan, np.nan
    val = str(val).strip().lower()
    if 'not disclosed' in val or not val:
        return np.nan, np.nan
    m = re.match(r'^(\d+)to(\d+)$', val)
    if m:
        return float(m.group(1)) * 100000, float(m.group(2)) * 100000
    return np.nan, np.nan
