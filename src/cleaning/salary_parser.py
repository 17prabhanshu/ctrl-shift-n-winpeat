"""
Salary parser - handles multiple salary string formats from Indian job postings.
Formats: "7.8L" (lakh per annum), "6to10" (range), "₹50,000", etc.
"""
import re
import numpy as np
import pandas as pd

def parse_ds_salary(val) -> float:
    """
    Parse DataScience Jobs salary format: "7.8L" = 7.8 lakh per annum.
    Returns salary in INR (absolute value).
    """
    if pd.isna(val) or val == '' or val is None:
        return np.nan
    
    val = str(val).strip().upper()
    
    # "7.8L" or "7.8 L" - lakh per annum
    m = re.match(r'^[\₹]?\s*([\d\.]+)\s*L\s*$', val)
    if m:
        try:
            lakhs = float(m.group(1))
            return lakhs * 100_000  # Convert to absolute INR
        except ValueError:
            return np.nan
    
    # Try numeric directly (already in absolute form)
    try:
        return float(val)
    except ValueError:
        return np.nan

def parse_analytics_salary(val) -> tuple:
    """
    Parse Analytics Jobs salary format: "6to10" = range 6-10 LPA.
    Returns (min_salary, max_salary) in INR absolute.
    Unknown/disclosed values return (nan, nan) with indicator.
    """
    if pd.isna(val) or str(val).strip() == '':
        return np.nan, np.nan
    
    val = str(val).strip().lower()
    
    # "not disclosed", "undisclosed", "not mentioned"
    if 'not disclosed' in val or 'undisclosed' in val or 'not mention' in val:
        return np.nan, np.nan
    
    # "6to10" or "6 to 10" - range in LPA
    m = re.match(r'^([\d\.]+)\s*(?:to|\-)\s*([\d\.]+)\s*$', val)
    if m:
        try:
            min_lpa = float(m.group(1))
            max_lpa = float(m.group(2))
            return min_lpa * 100_000, max_lpa * 100_000
        except ValueError:
            return np.nan, np.nan
    
    # Single value "8" (assumes LPA)
    try:
        val_float = float(val)
        return val_float * 100_000, val_float * 100_000
    except ValueError:
        return np.nan, np.nan

def parse_salary_with_indicator(val, parser_func) -> tuple:
    """
    Parse salary and return (value, disclosed_bool).
    disclosed_bool = True if salary was actually disclosed.
    """
    parsed = parser_func(val)
    disclosed = not pd.isna(parsed) and parsed != ''
    return parsed, disclosed

def clean_salary_column(df: pd.DataFrame, col: str, parser_func, 
                        min_val: float = 100_000, max_val: float = 50_000_000) -> pd.DataFrame:
    """
    Clean a salary column in-place, adding parsed and disclosed columns.
    Outliers outside [min_val, max_val] are flagged as missing.
    """
    df = df.copy()
    
    parsed_col = f"{col}_parsed"
    disclosed_col = f"{col}_disclosed"
    
    parsed_values = []
    disclosed_values = []
    
    for val in df[col]:
        parsed, disclosed = parse_salary_with_indicator(val, parser_func)
        # Flag outliers
        if not pd.isna(parsed) and (parsed < min_val or parsed > max_val):
            parsed = np.nan
            disclosed = False
        parsed_values.append(parsed)
        disclosed_values.append(disclosed)
    
    df[parsed_col] = parsed_values
    df[disclosed_col] = disclosed_values
    
    return df

if __name__ == "__main__":
    # Test cases
    assert parse_ds_salary("7.8L") == 780_000
    assert parse_ds_salary("12.8L") == 1_280_000
    assert np.isnan(parse_ds_salary("invalid"))
    assert np.isnan(parse_ds_salary("not disclosed"))
    
    assert parse_analytics_salary("6to10") == (600_000, 1_000_000)
    assert parse_analytics_salary("10 to 20") == (1_000_000, 2_000_000)
    assert np.isnan(parse_analytics_salary("Not disclosed")[0])
    
    print("All salary parser tests passed!")
