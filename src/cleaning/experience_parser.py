import re
import pandas as pd
import numpy as np

def parse_experience(val):
    if pd.isna(val):
        return np.nan, np.nan, np.nan
    val = str(val).strip().lower()
    
    # "6-10 yrs" or "6-10"
    m_range = re.match(r'^(\d+)\s*-\s*(\d+)', val)
    if m_range:
        low = float(m_range.group(1))
        high = float(m_range.group(2))
        return low, high, (low+high)/2.0
    
    # "2"
    m_single = re.match(r'^(\d+)$', val)
    if m_single:
        val_float = float(m_single.group(1))
        return val_float, val_float, val_float
        
    return np.nan, np.nan, np.nan
