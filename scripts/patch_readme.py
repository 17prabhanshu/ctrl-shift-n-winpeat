import re

with open('README.md', 'r') as f:
    text = f.read()

# Remove Streamlit badge
text = re.sub(r'\[\!\[Streamlit\]\(https://img\.shields\.io/badge/UI-Streamlit-FF4B4B\.svg\)\]\(https://streamlit\.io/\)\n', '', text)

# Remove Streamlit from mermaid diagram
text = re.sub(r'ST\[Streamlit App\]', '', text)
text = re.sub(r'ER --> ST', '', text)

# Update Running the Application section
run_section = """### 🚀 Running the Analytical Pipeline
The entire pipeline runs deterministically from raw data to the final evidence registry, completely regenerating the research findings and figures.

```bash
# 1. Clone the repository
git clone https://github.com/17prabhanshu/ctrl-shift-n-winpeat.git
cd ctrl-shift-n-winpeat

# 2. Run the automated master pipeline
./run.sh
```

**Final Artifacts:**
- **`app_final_note.docx`**: The comprehensive, 25-page, research-grade approach note with embedded statistical plots and verified metrics.
- **`docs/APPROACH_NOTE.md`**: Markdown equivalent of the final approach note.
- **`reports/evidence/evidence_registry.json`**: The source of truth for all analytical claims.
"""

text = re.sub(r'### 🚀 Running the Application.*', run_section, text, flags=re.DOTALL)

with open('README.md', 'w') as f:
    f.write(text)

