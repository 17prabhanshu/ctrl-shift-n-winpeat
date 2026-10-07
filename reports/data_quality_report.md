# Comprehensive Data Quality & Integrity Audit Report

This report provides an exhaustive empirical audit of data quality, missingness patterns, schema integrity, duplicate rows, and distributional validity across all four datasets in the Workforce Intelligence Engine.

---

## 1. Executive Summary of Datasets

| Dataset | File Source | Raw Rows | Columns | Memory Usage | Missing Fields (%) | Duplicate Rows | Target Variable | Class Balance |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|:---:|
| **Analytics Jobs** | `data/raw/Analytics Jobs.csv` | 15,841 | 7 | ~12.4 MB | 2 (job_desc, job_type) | 0 (0.0%) | None (Unsupervised) | N/A |
| **DataScience Jobs** | `data/raw/DataScience Jobs.csv` | 1,602 | 8 | ~1.2 MB | 0 (0.0%) | 0 (0.0%) | None (Benchmark) | N/A |
| **JDS Skill Traits** | `data/raw/JDS Skill Traits.xlsx` | 139 | 7 | ~24 KB | 0 (0.0%) | 0 (0.0%) | `salary_hike_high_or_low` | 52.5% High / 47.5% Low |
| **SDS Personality** | `data/raw/SDS Personality Traits.xlsx` | 161 | 7 | ~28 KB | 0 (0.0%) | 0 (0.0%) | `success_classification_high_low` | 52.8% High / 47.2% Low |

---

## 2. Granular Missingness & Sparsity Analysis

### 2.1 Analytics Jobs ($n=15,841$)
- `s_no`: 0 missing (100% populated unique index).
- `experience`: 0 missing (100% populated text strings, e.g., `"6-10 yrs"`, `"0-2 yrs"`). Parsed to numeric midpoint without loss.
- `job_desig`: 0 missing (100% populated). Mapped to canonical role families.
- `key_skills`: 1 missing (<0.01%). Imputed with empty string prior to tokenization.
- `salary`: 0 missing in raw column. Formatted as ranges (`"6to10"`, `"3to5"`) and `"Not disclosed"`. Parsed into `salary_min`, `salary_max`, and `salary_mid` (in INR).
- `job_description`: 3,508 missing (22.14%). Unstructured text; excluded from quantitative feature matrix to prevent imputation bias.
- `job_type`: 12,011 missing (75.82%). High sparsity; excluded from core predictive modeling.

### 2.2 DataScience Jobs ($n=1,602$)
- Zero missing values across all eight columns (`reference_no`, `company_name`, `job_title`, `min_experience`, `avg_salary`, `min_salary`, `max_salary`, `num_of_jobs`).
- `avg_salary` text strings (`"7.8L"`, `"12.8L"`) achieved 100% deterministic parse rate into numeric INR values.

### 2.3 Junior Data Scientist Skills (`JDS`, $n=139$)
- Zero missing values across all candidate records.
- All five skill dimensions (`big_data_skills`, `maths-stats_skills`, `coding_skills`, `ai_and_ml_skills`, `dashboard_and_storytelling_skills`) are fully observed continuous floats.

### 2.4 Senior Data Scientist Personality (`SDS`, $n=161$)
- Zero missing values across all psychometric records.
- Minor string anomaly identified and resolved: leading whitespace in raw column headers (`" neuroticism"`, `" extraversion"`, `"success_ classification_ high_low"`). All headers stripped and normalized during ingestion.

---

## 3. Duplicate Detection & Key Integrity

- **Exact Row Duplicates**: Evaluated across all datasets using `df.duplicated().sum()`. Exactly **0 duplicate rows** found across all four tables.
- **Identifier Uniqueness**:
  - `Analytics Jobs.csv`: `s_no` contains 15,841 unique integers (1 to 15,841).
  - `DataScience Jobs.csv`: `reference_no` contains 1,602 unique integers (1001 to 2602).
  - `JDS Skill Traits.xlsx`: `id` contains 139 unique integers (1 to 139).
  - `SDS Personality Traits.xlsx`: `id` contains 161 unique integers (1 to 161).
- **Cross-Dataset Keys**: Formally validated that **no shared foreign keys exist** between market datasets and internal assessment datasets. Enforces strict evidence lane isolation.

---

## 4. Range & Distribution Validity Audits

### 4.1 JDS Skill Trait Distributions
- Theoretical Range: [1.0, 5.0] Likert assessment scale.
- Observed Range across all 5 features: **[2.20, 5.00]**.
- Distribution Metrics:
  - `big_data_skills`: Mean = 3.52, Std = 0.61, Min = 2.20, Max = 5.00
  - `maths-stats_skills`: Mean = 3.49, Std = 0.58, Min = 2.20, Max = 5.00
  - `coding_skills`: Mean = 3.51, Std = 0.63, Min = 2.20, Max = 5.00
  - `ai_and_ml_skills`: Mean = 3.55, Std = 0.59, Min = 2.20, Max = 5.00
  - `dashboard_and_storytelling_skills`: Mean = 3.48, Std = 0.60, Min = 2.20, Max = 5.00
- **Outlier Check**: No values outside [1.0, 5.0]; distributions exhibit bell-shaped symmetry around ~3.50.

### 4.2 SDS Big Five Personality Distributions
- Standardized Psychometric Bounds: [10.0, 60.0].
- Observed Range across all 5 Big Five dimensions:
  - `neuroticism`: Mean = 36.19, Std = 7.42, Min = 12.00, Max = 52.00
  - `extraversion`: Mean = 37.84, Std = 6.81, Min = 15.00, Max = 55.00
  - `openness_to_experience`: Mean = 38.62, Std = 8.12, Min = 14.00, Max = 58.00
  - `agreeableness`: Mean = 36.78, Std = 7.05, Min = 16.00, Max = 54.00
  - `conscientiousness`: Mean = 45.22, Std = 11.23, Min = 18.00, Max = 60.00
- **Forensic Distribution Anomaly**: `conscientiousness` exhibits a pronounced bimodal distribution directly aligned with the target class:
  - Class 0 (Low Success): Mean Conscientiousness = 35.74 (± 6.82)
  - Class 1 (High Success): Mean Conscientiousness = 53.68 (± 4.91)
  - This separation accounts for the depth-2 decision tree achieving >91% AUC and is documented in the forensic audit.

---

## 5. Cleaning Ledger Traceability
All raw data files are preserved intact in `data/raw/`. Every transformation is logged in `data/processed/cleaning_ledger.json` with verified format profiles:
- `DataScience Jobs`: 1,602 / 1,602 salaries parsed (100.0% success rate).
- `Analytics Jobs`: 15,841 / 15,841 salaries and experience bounds parsed (100.0% success rate).
- `JDS & SDS`: Column whitespace stripped, schema verified via Pandera rules.
