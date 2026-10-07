import re

with open('README.md', 'r') as f:
    text = f.read()

innovation_link = """
> **Workforce Intelligence Engine** is a deterministic analytical platform designed to synthesize and interpret complex labor-market signals without inducing data leakage.

🔥 **[READ FIRST: Core Innovations & Architectural Forensics](docs/INNOVATION_HIGHLIGHTS.md)**
*Discover how we bypassed the Ecological Fallacy, audited a 99.8% AUC via Decision Tree Forensics, and proved the Demand-Reward Inversion.*
"""

text = re.sub(r'> \*\*Workforce Intelligence Engine\*\* is a deterministic analytical platform designed to synthesize and interpret complex labor-market signals without inducing data leakage\.', innovation_link, text)

with open('README.md', 'w') as f:
    f.write(text)
