import re

with open('README.md', 'r') as f:
    text = f.read()

# Add SAS Viya Badge
badge = "[![SAS Viya](https://img.shields.io/badge/SAS-Viya_for_Learners-0075D8.svg)](https://www.sas.com/en_us/software/viya.html)\n"
text = re.sub(r'\[\!\[License: MIT\]', badge + r'[![License: MIT]', text)

# Add SAS VFL Section right after Architecture
sas_section = """
### ☁️ SAS Viya for Learners (VFL) Readiness
This project utilizes a hybrid architecture. The rigorous data engineering, deterministic parsing, and forensic analyses operate in open-source Python, acting as the perfect ETL pipeline for **SAS Viya for Learners**. 

Instead of forcing a localized UI, our `data/processed/` outputs are strictly formatted for direct upload into **SAS Cloud Analytic Services (CAS)**. This allows the final presentation and advanced AutoML to be executed natively within **SAS Visual Analytics** and **SAS Model Studio**. 

👉 **[View the SAS VFL Integration Architecture Guide](docs/SAS_VFL_INTEGRATION.md)**

---
"""
text = text.replace('## 🧹 Data Engineering Strategy', sas_section + '\n## 🧹 Data Engineering Strategy')

with open('README.md', 'w') as f:
    f.write(text)
