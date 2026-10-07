"""
Profile and audit all data cleaning transformations.

This script runs the salary and experience parsers against the actual data,
counts real parse rates, logs them to the cleaning ledger, and generates
a verifiable audit report.
"""
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.cleaning.salary_parser import parse_ds_salary, parse_analytics_salary, profile_formats
from src.cleaning.cleaning_ledger import CleaningLedger

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    ledger = CleaningLedger()

    # --- DS Jobs ---
    ds_path = os.path.join(PROJECT_ROOT, "data", "processed", "ds_jobs_clean.csv")
    if os.path.exists(ds_path):
        ds = pd.read_csv(ds_path)

        # Profile avg_salary
        if "avg_salary" in ds.columns:
            fmt_counts = profile_formats(ds["avg_salary"], parse_ds_salary, "DS avg_salary")
            parsed = sum(v for k, v in fmt_counts.items()
                         if k not in ("missing",) and not k.startswith("unmatched"))
            unmatched = sum(v for k, v in fmt_counts.items() if k.startswith("unmatched"))
            ledger.log(
                dataset="DataScience Jobs",
                column="avg_salary",
                transformation="parse_lakhs_to_float",
                reason="Salary stored as text like '7.8L'; converted to INR float",
                total_rows=len(ds),
                affected_rows=parsed,
                unmatched_rows=unmatched,
                format_profile=fmt_counts,
            )
    else:
        print(f"WARNING: {ds_path} not found")

    # --- Analytics Jobs ---
    aj_path = os.path.join(PROJECT_ROOT, "data", "processed", "analytics_jobs_clean.csv")
    if os.path.exists(aj_path):
        aj = pd.read_csv(aj_path)

        if "salary" in aj.columns:
            fmt_counts = profile_formats(aj["salary"], parse_analytics_salary, "Analytics salary")
            parsed = sum(v for k, v in fmt_counts.items()
                         if k not in ("missing", "not_disclosed") and not k.startswith("unmatched"))
            unmatched = sum(v for k, v in fmt_counts.items() if k.startswith("unmatched"))
            not_disclosed = fmt_counts.get("not_disclosed", 0)
            ledger.log(
                dataset="Analytics Jobs",
                column="salary",
                transformation="parse_range_to_min_max",
                reason="Salary stored as text like '6to10'; converted to INR min/max",
                total_rows=len(aj),
                affected_rows=parsed,
                unmatched_rows=unmatched + not_disclosed,
                format_profile=fmt_counts,
            )
    else:
        print(f"WARNING: {aj_path} not found")

    # --- JDS ---
    jds_path = os.path.join(PROJECT_ROOT, "data", "processed", "jds_skills_clean.xlsx")
    if os.path.exists(jds_path):
        jds = pd.read_excel(jds_path)
        jds.columns = jds.columns.str.strip()
        missing = int(jds.isnull().sum().sum())
        ledger.log(
            dataset="JDS Skill Traits",
            column="all_columns",
            transformation="column_name_strip",
            reason="Column names had leading/trailing whitespace",
            total_rows=len(jds),
            affected_rows=len(jds),
            unmatched_rows=0,
        )

    # --- SDS ---
    sds_path = os.path.join(PROJECT_ROOT, "data", "processed", "sds_personality_clean.xlsx")
    if os.path.exists(sds_path):
        sds = pd.read_excel(sds_path)
        sds.columns = sds.columns.str.strip()
        ledger.log(
            dataset="SDS Personality Traits",
            column="all_columns",
            transformation="column_name_strip",
            reason="Column names had leading/trailing whitespace and spaces",
            total_rows=len(sds),
            affected_rows=len(sds),
            unmatched_rows=0,
        )

    ledger.summary()
    print(f"\nCleaning ledger saved to: {ledger.path}")


if __name__ == "__main__":
    main()
