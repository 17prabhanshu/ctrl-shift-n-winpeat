import re

with open('README.md', 'r') as f:
    text = f.read()

eda_link = """## 📊 Advanced Exploratory Data Analysis
To ensure full transparency and interpretability of our features, we have exported all findings from our Advanced EDA research notebooks directly into GitHub. 

👉 **[View the Advanced EDA Documentation & Visuals](docs/ADVANCED_EDA.md)**

Includes:
- Multivariate PCA Projections
- JDS & SDS Correlation Matrices
- Feature Separability Distributions (KDE)
- Missingness Audits

---

## 🔬 Data Analysis & Explainable AI"""

text = re.sub(r'## 🔬 Data Analysis & Explainable AI', eda_link, text)

with open('README.md', 'w') as f:
    f.write(text)

