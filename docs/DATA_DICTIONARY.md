# Workforce Intelligence Engine: Comprehensive Data Dictionary

This document details the exact schema, data types, variable descriptions, ranges, and transformations for all four datasets analyzed in the Workforce Intelligence Engine (WIE).

---

## 1. Analytics Jobs (`data/raw/Analytics Jobs.csv`)
- **Source**: Indian job market portal postings for analytics and business intelligence roles.
- **Raw Dimensions**: 15,841 rows × 7 columns.
- **Target Variable**: None (Unsupervised market distribution dataset).

| Column Name | Data Type (Raw) | Cleaned / Parsed Type | Description | Observed Range / Format | Null Count (%) | Processing Notes |
|:---|:---|:---|:---|:---|:---|:---|
| `s_no` | Integer | Integer | Row identifier | 1 to 15,841 | 0 (0.0%) | Unique index; not used as a predictive feature. |
| `experience` | String | Float (`exp_mid`, `exp_min`, `exp_max`) | Required experience range | e.g., `"6-10 yrs"`, `"2"`, `"0-1 yrs"` | 0 (0.0%) | Parsed via regex into minimum, maximum, and midpoint numeric experience in years. |
| `job_description` | String | String | Free-text job description | Text strings | 0 (0.0%) | Explored for textual validation and industry context. |
| `job_desig` | String | Categorical (`role_family`) | Job designation / Title | e.g., `"Data Analyst"`, `"BI Consultant"` | 0 (0.0%) | Mapped to canonical role families (Data Analyst, Data Scientist, Data Engineer, ML Engineer, Business Analyst, Other). |
| `job_type` | String | Categorical | Contract or employment type | e.g., `"Full Time"`, `"Permanent"` | 0 (0.0%) | High cardinality; primarily full-time analytics roles. |
| `key_skills` | String | List of Strings / Canonical IDs | Delimited list of required candidate skills | Pipe (`\|`) or comma (`,`) separated | 0 (0.0%) | Parsed via deterministic N-gram tokenizer and alias dictionary to canonical taxonomy. |
| `salary` | String | Float (`salary_min`, `salary_max`, `salary_mid`) | Quoted salary range (Lakhs Per Annum) | e.g., `"6to10"`, `"3to5"`, `"Not disclosed"` | 0 (0.0% raw; ~100% disclosed in parsed range) | Parsed via format profiling to min, max, and midpoint annual compensation in INR (multiplied by 100,000). |

---

## 2. Data Science Jobs (`data/raw/DataScience Jobs.csv`)
- **Source**: Data science specific postings across Indian technology hubs.
- **Raw Dimensions**: 1,602 rows × 8 columns.
- **Target Variable**: None (Cross-sectional compensation benchmark).

| Column Name | Data Type (Raw) | Cleaned / Parsed Type | Description | Observed Range / Format | Null Count (%) | Processing Notes |
|:---|:---|:---|:---|:---|:---|:---|
| `reference_no` | Integer | Integer | Job posting reference ID | 1001 to 2602 | 0 (0.0%) | Checked for duplicates (1,602 unique rows). |
| `company_name` | String | String | Hiring organization | Anonymized / Named firms | 0 (0.0%) | Retained for enterprise distribution audits. |
| `job_title` | String | Categorical (`role_family`) | Specific role title | e.g., `"Senior Data Scientist"`, `"ML Specialist"` | 0 (0.0%) | Normalized and mapped to role families. |
| `min_experience` | Float / String | Float | Stated minimum experience required | 1 to 15 years | 0 (0.0%) | Converted directly to numeric years of experience. |
| `avg_salary` | String | Float (`avg_salary_parsed`) | Listed average compensation | e.g., `"7.8L"`, `"12.8L"`, `"15L"` | 0 (0.0%) | Parsed deterministically (100% matched format `NL` / `NNL` in Lakhs; multiplied by 100,000 for INR). |
| `min_salary` | Float | Float | Minimum salary bracket | Numeric (Lakhs) | 0 (0.0%) | Converted to standardized INR. |
| `max_salary` | Float | Float | Maximum salary bracket | Numeric (Lakhs) | 0 (0.0%) | Converted to standardized INR. |
| `num_of_jobs` | Integer | Integer | Number of open headcount positions | 1 to 50+ | 0 (0.0%) | Used to weight aggregate demand volume calculations. |

---

## 3. Junior Data Scientist (JDS) Skills Dataset (`data/raw/JDS Skill Traits.xlsx`)
- **Source**: Internal talent assessment evaluation of junior data science professionals.
- **Raw Dimensions**: 139 rows × 7 columns.
- **Target Variable**: `salary_hike_high_or_low` (Binary: 1 = High salary hike [n=73], 0 = Low salary hike [n=66]).

| Column Name | Cleaned Column | Type | Description | Scale / Valid Bounds | Missing (%) | Mean (Std) / Distribution |
|:---|:---|:---|:---|:---|:---|:---|
| `id` | `id` | Integer | Candidate evaluation ID | 1 to 139 | 0 (0.0%) | Primary key within JDS cohort only. |
| `big_data_skills` | `big_data_skills` | Float | Evaluated competency in distributed systems & data pipelines | Continuous [2.2, 5.0] | 0 (0.0%) | 3.52 (± 0.61) |
| `maths-stats_skills` | `maths_stats_skills` | Float | Evaluated quantitative, statistical, & probability rigor | Continuous [2.2, 5.0] | 0 (0.0%) | 3.49 (± 0.58) |
| `coding_skills` | `coding_skills` | Float | Software engineering, algorithmic coding, & clean code | Continuous [2.2, 5.0] | 0 (0.0%) | 3.51 (± 0.63) |
| `ai_and_ml_skills` | `ai_ml_skills` | Float | Machine learning algorithms, validation, & modelling | Continuous [2.2, 5.0] | 0 (0.0%) | 3.55 (± 0.59) |
| `dashboard_and_storytelling_skills` | `dashboard_storytelling_skills` | Float | Executive communication, storytelling, & dashboarding | Continuous [2.2, 5.0] | 0 (0.0%) | 3.48 (± 0.60) |
| `salary_hike_high_or_low` | `salary_hike_high_or_low` | Binary | Outcome label: 1 = High hike, 0 = Low hike | Categorical {0, 1} | 0 (0.0%) | Class balance: 52.5% (High) vs 47.5% (Low). |

---

## 4. Senior Data Scientist (SDS) Personality Dataset (`data/raw/SDS Personality Traits.xlsx`)
- **Source**: Internal psychometric evaluation of senior analytics leadership.
- **Raw Dimensions**: 161 rows × 7 columns.
- **Target Variable**: `success_classification_high_low` (Binary: 1 = High success [n=85], 0 = Low success [n=76]).

| Column Name (Raw) | Cleaned Column | Type | Description (Big Five Factor) | Scale / Valid Bounds | Missing (%) | Mean (Std) / Distribution |
|:---|:---|:---|:---|:---|:---|:---|
| `id` | `id` | Integer | Senior practitioner identifier | 1 to 161 | 0 (0.0%) | Primary key within SDS cohort only. |
| ` neuroticism` | `neuroticism` | Float | Emotional stability vs negative emotionality | Continuous [12.0, 52.0] | 0 (0.0%) | 36.19 (± 7.42); leading space stripped during cleaning. |
| ` extraversion` | `extraversion` | Float | Sociability, assertiveness, & stakeholder engagement | Continuous [15.0, 55.0] | 0 (0.0%) | 37.84 (± 6.81); leading space stripped during cleaning. |
| `openness_to_experience` | `openness_to_experience` | Float | Intellectual curiosity, novel idea adoption | Continuous [14.0, 58.0] | 0 (0.0%) | 38.62 (± 8.12) |
| `agreeableness` | `agreeableness` | Float | Interpersonal collaboration & trust | Continuous [16.0, 54.0] | 0 (0.0%) | 36.78 (± 7.05) |
| `conscientiousness` | `conscientiousness` | Float | Goal-directed persistence, rigor, & execution discipline | Continuous [18.0, 60.0] | 0 (0.0%) | 45.22 (± 11.23) |
| `success_ classification_ high_low` | `success_classification_high_low` | Binary | Outcome label: 1 = High success, 0 = Low success | Categorical {0, 1} | 0 (0.0%) | Class balance: 52.8% (High) vs 47.2% (Low). |

---

## 5. Cross-Dataset Harmonization: The Canonical 5-Dimension Skill Construct
To enable cross-dataset synthesis without committing row-level joins, the engine maps market-level textual skills to the five core competencies measured in JDS:

| Dimension Code | Dimension Name | Representative Raw Skill Keywords in Market Postings | Mapping Logic |
|:---|:---|:---|:---|
| `dim_bigdata` | Big Data & Data Infrastructure | `spark`, `hadoop`, `kafka`, `hive`, `pyspark`, `data warehouse`, `etl`, `aws` | Substring match & alias expansion |
| `dim_mathstats` | Mathematics & Statistics | `statistics`, `statistical modeling`, `probability`, `econometrics`, `r`, `hypothesis testing` | Exact keyword and n-gram overlap |
| `dim_coding` | Core Algorithmic Coding | `python`, `sql`, `java`, `c++`, `data structures`, `git`, `scala` | High-frequency token filtering |
| `dim_aiml` | Artificial Intelligence & Machine Learning | `machine learning`, `deep learning`, `nlp`, `computer vision`, `tensorflow`, `pytorch`, `scikit-learn` | Multi-token n-gram matcher |
| `dim_storytelling`| Dashboarding, Visualization & Storytelling | `tableau`, `power bi`, `data visualization`, `qlik`, `storytelling`, `executive presentation` | Domain visualization token set |
