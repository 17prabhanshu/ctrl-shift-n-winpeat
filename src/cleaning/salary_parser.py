"""
Salary and experience parsers with explicit format profiling.

Every parser returns (parsed_value, format_code) so the cleaning ledger
can count exactly how many rows matched each pattern and how many failed.
"""
import re
import pandas as pd
import numpy as np


# --- DS Jobs salary parser ---

def parse_ds_salary(val):
    """Parse DataScience Jobs avg_salary column.

    Known formats (from format profiling):
      '7.8L'   -> 780000.0   (format: NL)
      '12.8L'  -> 1280000.0  (format: NNL)
      '15L'    -> 1500000.0  (format: NL)
      NaN      -> NaN        (format: missing)

    Returns: (parsed_float, format_code)
    """
    if pd.isna(val):
        return np.nan, "missing"
    val = str(val).strip()

    # Pattern 1: "7.8L" or "12.8L" (Lakhs)
    m = re.match(r'^([\d\.]+)\s*[Ll]$', val)
    if m:
        try:
            return float(m.group(1)) * 100000, "lakhs"
        except ValueError:
            return np.nan, "parse_error"

    # Pattern 2: plain number (already numeric)
    m = re.match(r'^[\d\.]+$', val)
    if m:
        try:
            return float(val), "numeric"
        except ValueError:
            return np.nan, "parse_error"

    # Pattern 3: range like "6-10" or "6 - 10"
    m = re.match(r'^([\d\.]+)\s*[-–]\s*([\d\.]+)$', val)
    if m:
        try:
            lo, hi = float(m.group(1)), float(m.group(2))
            return (lo + hi) / 2 * 100000, "range_lakhs"
        except ValueError:
            return np.nan, "parse_error"

    return np.nan, f"unmatched:{val[:30]}"


def parse_analytics_salary(val):
    """Parse Analytics Jobs salary column.

    Known formats:
      '6to10'         -> (600000, 1000000)  (format: range)
      'Not disclosed' -> (NaN, NaN)         (format: not_disclosed)
      NaN             -> (NaN, NaN)         (format: missing)
      '3to6'          -> (300000, 600000)   (format: range)

    Returns: (min_salary, max_salary, format_code)
    """
    if pd.isna(val):
        return np.nan, np.nan, "missing"
    val = str(val).strip().lower()

    if 'not disclosed' in val or val == '':
        return np.nan, np.nan, "not_disclosed"

    # Pattern 1: "6to10"
    m = re.match(r'^(\d+)\s*to\s*(\d+)$', val)
    if m:
        return float(m.group(1)) * 100000, float(m.group(2)) * 100000, "range_lpa"

    # Pattern 2: "6-10" or "6 - 10"
    m = re.match(r'^(\d+)\s*[-–]\s*(\d+)$', val)
    if m:
        return float(m.group(1)) * 100000, float(m.group(2)) * 100000, "range_dash"

    # Pattern 3: plain number
    m = re.match(r'^[\d\.]+$', val)
    if m:
        v = float(val) * 100000
        return v, v, "single_lpa"

    return np.nan, np.nan, f"unmatched:{val[:30]}"


def profile_formats(series, parser_fn, name="column"):
    """Profile all unique formats in a series and print a summary table.

    Returns dict of {format_code: count}.
    """
    format_counts = {}
    for val in series:
        result = parser_fn(val)
        fmt = result[-1]  # last element is format_code
        format_counts[fmt] = format_counts.get(fmt, 0) + 1

    total = sum(format_counts.values())
    parsed = total - format_counts.get("missing", 0) - sum(
        v for k, v in format_counts.items() if k.startswith("unmatched")
    )

    print(f"\n--- Format Profile: {name} (n={total}) ---")
    print(f"{'Format':<25} {'Count':>6} {'Pct':>7}")
    print("-" * 40)
    for fmt, count in sorted(format_counts.items(), key=lambda x: -x[1]):
        print(f"{fmt:<25} {count:>6} {count/total*100:>6.1f}%")
    print(f"{'TOTAL PARSED':<25} {parsed:>6} {parsed/total*100:>6.1f}%")

    return format_counts
