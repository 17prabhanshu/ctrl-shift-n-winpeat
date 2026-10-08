"""
Central configuration for the Workforce Intelligence Engine.
All paths, seeds, and hyperparameters are defined here.
"""
import os
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = Path("/Users/prabhanshushekhar/ctrl-shift-n-winpeat/ctrl-shift-n-winpeat/data")
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = Path("/Users/prabhanshushekhar/ctrl-shift-n-winpeat/ctrl-shift-n-winpeat/reports")
EVIDENCE_DIR = REPORTS_DIR / "evidence"
BENCHMARKS_DIR = REPORTS_DIR / "benchmarks"
FIGURES_DIR = REPORTS_DIR / "figures"

# Dataset paths
DATASETS = {
    "ds_jobs": RAW_DIR / "DataScience Jobs.csv",
    "analytics_jobs": RAW_DIR / "Analytics Jobs.csv",
    "jds_skills": RAW_DIR / "JDS Skill Traits.xlsx",
    "sds_personality": RAW_DIR / "SDS Personality Traits.xlsx",
}

# Random seeds for reproducibility
SEEDS = list(range(20))  # 0-19 for repeated CV
DEFAULT_SEED = 42

# Cross-validation configuration
CV_SPLITS = 5
CV_REPEATS = 20

# Hypothesis test configurations
ALPHA = 0.05
CONFORMAL_ALPHA = 0.10  # 90% prediction sets

# Role categorization (canonical, used everywhere)
def categorize_role(title: str) -> str:
    """Canonical role categorization - single source of truth."""
    title_lower = str(title).lower().strip()
    
    if "data scientist" in title_lower or "data science" in title_lower:
        return "Data Scientist"
    if "machine learning" in title_lower or title_lower.startswith("ml") or " ml " in title_lower:
        return "ML Engineer"
    if "data engineer" in title_lower or "big data" in title_lower or "etl" in title_lower:
        return "Data Engineer"
    if "business analyst" in title_lower or title_lower == "ba":
        return "Business Analyst"
    if "data analyst" in title_lower or "reporting analyst" in title_lower:
        return "Data Analyst"
    if "software engineer" in title_lower or "software developer" in title_lower or "developer" in title_lower:
        return "Software Engineer"
    return "Other"

# Skill taxonomy - canonical mapping to 5 JDS dimensions
# Based on Table 10 in the approach note
SKILL_TAXONOMY = {
    "big_data": {
        "keywords": [
            "hadoop", "spark", "hive", "kafka", "data warehousing", "big data",
            "hdfs", "pig", "mapreduce", "hbase", "nosql", "mongodb", "cassandra",
            "data lake", "snowflake", "redshift", "bigdata"
        ],
        "description": "Big data technologies and distributed data platforms"
    },
    "maths_statistics": {
        "keywords": [
            "statistics", "regression", "probability", "forecasting", "hypothesis testing",
            "statistical modeling", "statistical analysis", "mathematical", "quantitative",
            "optimization", "linear algebra", "calculus", "bayesian"
        ],
        "description": "Mathematical and statistical analysis"
    },
    "coding": {
        "keywords": [
            "python", "java", "scala", "c++", "c#", "r programming", "r ", "sql",
            "javascript", "typescript", "go", "golang", "rust", "julia",
            "csharp", "dotnet", ".net", "php", "perl", "ruby", "swift", "kotlin"
        ],
        "description": "Programming languages (SQL included here; sensitivity run reassigns to big_data)"
    },
    "ai_ml": {
        "keywords": [
            "machine learning", "deep learning", "nlp", "natural language processing",
            "computer vision", "tensorflow", "pytorch", "keras", "neural network",
            "neural networks", "reinforcement learning", "supervised learning",
            "unsupervised learning", "transfer learning", "bert", "gpt", "llm",
            "data mining", "predictive modeling", "predictive analytics",
            "algorithm", "algorithms", "classification", "clustering"
        ],
        "description": "AI and machine learning techniques and frameworks"
    },
    "dashboard_storytelling": {
        "keywords": [
            "tableau", "power bi", "powerbi", "data visualization", "visualization",
            "visualisation", "reporting", "presentation", "storytelling",
            "dashboard", "business intelligence", "bi ", "excel", "spreadsheet",
            "powerpoint", "communicat", "stakeholder", "data storytelling"
        ],
        "description": "Data visualization, reporting, and communication"
    }
}

# Skills that should NOT be mapped to any technical dimension
# These are explicitly non-technical or business skills
NON_TECHNICAL_SKILLS = {
    "project management", "product management", "program management",
    "agile", "scrum", "kanban", "sprints",
    "sales", "marketing", "digital marketing", "seo", "sem", "ppc",
    "finance", "financial analysis", "financial modeling", "financial planning", "budgeting", "accounting",
    "hr", "human resources", "recruitment", "hiring", "talent",
    "consulting", "business analysis", "business analyst", "business development", "strategy",
    "operations", "supply chain", "logistics",
    "customer service", "client management", "client interfacing",
    "communication skills", "team management", "leadership", "management",
    "outsource", "outsourcing", "bpo",
    "banking", "insurance", "risk management", "credit risk",
    "technical support", "it support",
    "market research",
    "auditing", "compliance",
    "social media", "content", "creative",
    "english", "verbal", "written communication",
    "presentation",  # Already in dashboard_storytelling but be explicit
}

# Skills that ARE technical but often misclassified
# These should be mapped, not blocked
TECHNICAL_BUT_OFTEN_MISSED = {
    'sas', 'spss', 'stata',  # Statistical software - maths_statistics
    'r', 'r programming', 'r studio', 'rstudio',  # R language - coding
    'matlab', 'octave',  # Math software - maths_statistics
    'tableau', 'power bi', 'powerbi',  # Visualization - dashboard_storytelling
    'qlik', 'looker', 'looker studio', 'gibbon',  # BI tools - dashboard_storytelling
    'mongodb', 'cassandra', 'couchdb', 'redis', 'dynamodb', 'neo4j',  # NoSQL - big_data
    'snowflake', 'redshift', 'bigquery', 'databricks',  # Cloud data - big_data
    'docker', 'kubernetes', 'k8s', 'jenkins', 'ci/cd', 'devops',  # DevOps - coding
    'angular', 'react', 'vue', 'node', 'express', 'next.js', 'nuxt',  # Web frameworks - coding
    'html', 'html5', 'css', 'css3', 'sass', 'scss', 'less',  # Web tech - coding
    'jquery', 'ajax', 'json', 'xml', 'rest', 'soap', 'graphql', 'api',  # Web/API - coding
    'linux', 'unix', 'shell', 'bash', 'powershell', 'scripting',  # Systems - coding
    'git', 'github', 'gitlab', 'bitbucket', 'version control',  # VCS - coding
    'android', 'ios', 'mobile', 'flutter', 'react native', 'swift', 'kotlin',  # Mobile - coding
    'aws', 'azure', 'gcp', 'google cloud', 'cloud', 'terraform', 'ansible',  # Cloud - coding
    'excel',  # Spreadsheets can be dashboard - but ambiguous
}

# Firth logistic regression configuration
FIRTH_MAX_ITER = 1000

# Conformal prediction configuration
CONFORMAL_N_CALIBRATION = 50  # size of calibration set

# Hyperparameter search spaces (inner loop)
HYPERPARAM_SPACES = {
    "logistic": {"C": [1e-3, 1e-2, 1e-1, 1, 1e1, 1e2, 1e3]},
    "random_forest": {
        "n_estimators": [500],
        "max_depth": [2, 3, 4, None],
        "min_samples_leaf": [1, 2, 4, 8],
        "max_features": ["sqrt", "log2", 0.5, 1.0]
    },
    "extra_trees": {
        "n_estimators": [500],
        "max_depth": [2, 3, 4, None],
        "min_samples_leaf": [1, 2, 4, 8],
        "max_features": ["sqrt", "log2", 0.5, 1.0]
    },
    "hist_gradient_boosting": {
        "learning_rate": [0.03, 0.1],
        "max_depth": [2, 3],
        "max_iter": [100, 300],
        "l2_regularization": [0, 1, 10]
    },
    "xgboost": {
        "max_depth": [2, 3, 4],
        "learning_rate": [0.03, 0.1],
        "n_estimators": [100, 300],
        "subsample": [0.8, 1.0]
    },
    "lightgbm": {
        "num_leaves": [4, 8, 16],
        "min_child_samples": [5, 10, 20],
        "learning_rate": [0.03, 0.1],
        "n_estimators": [100, 300],
        "reg_lambda": [0, 1, 10]
    },
    "catboost": {
        "depth": [2, 3, 4],
        "learning_rate": [0.03, 0.1],
        "iterations": [100, 300],
        "l2_leaf_reg": [1, 3, 5]
    }
}

# Ensure directories exist
for d in [PROCESSED_DIR, REPORTS_DIR, EVIDENCE_DIR, BENCHMARKS_DIR, FIGURES_DIR]:
    d.mkdir(parents=True, exist_ok=True)
