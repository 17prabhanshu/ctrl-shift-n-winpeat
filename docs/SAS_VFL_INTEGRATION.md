# SAS Viya for Learners (VFL) Integration Architecture

The **Workforce Intelligence Engine (WIE)** is explicitly designed with a hybrid open-source/enterprise architecture. While the core data engineering, deterministic parsing, and forensic analytics were developed locally using Python, the output layer is heavily optimized for seamless ingestion into **SAS Viya for Learners (VFL)**.

By cleanly separating the Data Engineering layer from the Presentation/AutoML layer, this repository achieves **SAS VFL Readiness**.

## 1. SAS Visual Analytics (VA) for the Presentation Layer
Instead of relying on fragile open-source dashboarding frameworks (e.g., Streamlit or Dash), WIE outputs highly structured, clean tabular data directly into the `data/processed/` directory.

*   **Actionable Integration:** The `analytics_jobs_clean.csv` and `jds_skills_clean.xlsx` files can be directly uploaded into SAS Cloud Analytic Services (CAS) memory.
*   **VFL Use Case:** Once in CAS, students and HR executives can use **SAS Visual Analytics (VA)** to build interactive, drag-and-drop dashboards. The Lorenz curves, Missingness maps, and PCA clusters generated in our Python EDA phase can be natively recreated and interactively explored using SAS VA's advanced visualization suite.

## 2. SAS Studio & Model Studio (AutoML Extension)
Our Python pipeline establishes a rigorous baseline using `scikit-learn` and `xgboost` with 20x Repeated Stratified 5-Fold Cross-Validation.

*   **Actionable Integration:** The clean, null-handled, and categorically encoded datasets provide the perfect foundation for **SAS Model Studio**.
*   **VFL Use Case:** Users can import our processed datasets into a SAS Model Studio pipeline to run SAS's proprietary Gradient Boosting and Forest nodes. This allows for a direct algorithmic comparison between the open-source baseline and SAS's highly optimized enterprise modeling algorithms.

## 3. SAS SWAT (Scripting Wrapper for Analytics Transfer)
For teams looking to scale this engine to process millions of job postings, local Python execution becomes a bottleneck.

*   **Actionable Integration:** The Python scripts in our `src/` directory are functionally modular. They can be wrapped using the **SAS SWAT** library.
*   **VFL Use Case:** By importing `swat`, the WIE pipeline can connect to a SAS Viya CAS server. The `pandas` data manipulations (like the N-gram tokenization of 15,000+ skills) can be pushed down to the CAS server for distributed, in-memory execution, optimizing computational efficiency.

---
*This hybrid architecture ensures the Workforce Intelligence Engine leverages the rapid prototyping of open-source Python while utilizing the enterprise-grade visualization and distributed computing power of SAS Viya for Learners.*
