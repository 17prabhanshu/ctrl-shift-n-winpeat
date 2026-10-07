
def validate_schemas(dfs):
    # Minimal validation
    required = {
        'ds_jobs': ['company_name', 'job_title', 'avg_salary'],
        'analytics_jobs': ['experience', 'job_desig', 'salary']
    }
    for k, req_cols in required.items():
        if k in dfs:
            for c in req_cols:
                if c not in dfs[k].columns:
                    raise ValueError(f"Missing required column {c} in {k}")
    return True
