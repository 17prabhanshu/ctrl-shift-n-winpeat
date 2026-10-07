import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# Config options
SEED = 42

DATASETS = {
    'ds_jobs': os.path.join(RAW_DIR, 'DataScience Jobs.csv'),
    'analytics_jobs': os.path.join(RAW_DIR, 'Analytics Jobs.csv'),
    'jds_skills': os.path.join(RAW_DIR, 'JDS Skill Traits.xlsx'),
    'sds_personality': os.path.join(RAW_DIR, 'SDS Personality Traits.xlsx')
}
