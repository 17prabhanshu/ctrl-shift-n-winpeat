"""
Experience parser - handles multiple experience string formats.
Formats: "6-10 yrs", "6to10", "2", "0-2", etc.
"""
import re
import numpy as np
import pandas as pd

def parse_experience(val) -> tuple:
    """
    Parse experience requirement string.
    Returns (min_years, max_years, midpoint_years) or (nan, nan, nan) if unparseable.
    """
    if pd.isna(val) or str(val).strip() == '':
        return np.nan, np.nan, np.nan
    
    val = str(val).strip().lower()
    
    # Remove "yrs", "years", "y" suffix
    val = re.sub(r'\s*(?:yrs?|years?)\s*$', '', val)
    
    # Range: "6-10" or "6 to 10" or "6-10 yrs"
    m_range = re.match(r'^([\d\.]+)\s*(?:to|\-)\s*([\d\.]+)$', val)
    if m_range:
        try:
            low = float(m_range.group(1))
            high = float(m_range.group(2))
            # Ensure low <= high (swap if reversed)
            if low > high:
                low, high = high, low
            # Flag implausible values (>40 years experience)
            if low > 40 or high > 40:
                return np.nan, np.nan, np.nan
            midpoint = (low + high) / 2
            return low, high, midpoint
        except ValueError:
            return np.nan, np.nan, np.nan
    
    # Single value: "2" or "5"
    m_single = re.match(r'^([\d\.]+)$', val)
    if m_single:
        try:
            val_float = float(m_single.group(1))
            if val_float > 40:  # Flag implausible
                return np.nan, np.nan, np.nan
            return val_float, val_float, val_float
        except ValueError:
            return np.nan, np.nan, np.nan
    
    # "fresher", "0", "entry level"
    if val in ['fresher', 'fresh', 'entry', '0', '0.0']:
        return 0, 0, 0
    
    return np.nan, np.nan, np.nan

def clean_experience_column(df: pd.DataFrame, col: str = 'experience') -> pd.DataFrame:
    """Clean experience column, adding min, max, midpoint and width columns."""
    df = df.copy()
    
    parsed = df[col].apply(parse_experience)
    df[f'{col}_min'] = [p[0] for p in parsed]
    df[f'{col}_max'] = [p[1] for p in parsed]
    df[f'{col}_mid'] = [p[2] for p in parsed]
    df[f'{col}_width'] = df[f'{col}_max'] - df[f'{col}_min']
    
    # Flag implausible or missing
    df[f'{col}_valid'] = df[f'{col}_mid'].notna()
    
    return df

if __name__ == "__main__":
    assert parse_experience("6-10 yrs") == (6, 10, 8)
    assert parse_experience("3 to 8") == (3, 8, 5.5)
    assert parse_experience("2") == (2, 2, 2)
    assert parse_experience("fresher") == (0, 0, 0)
    assert parse_experience("invalid") == (np.nan, np.nan, np.nan)
    assert parse_experience(np.nan) == (np.nan, np.nan, np.nan)
    
    # Test reversed range swap
    assert parse_experience("10-5 yrs") == (5, 10, 7.5)
    
    print("All experience parser tests passed!")
