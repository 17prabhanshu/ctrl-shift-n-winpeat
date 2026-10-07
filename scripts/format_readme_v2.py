import re

with open('README.md', 'r') as f:
    content = f.read()

# Fix the duplication issue
pattern = r"</details>\n1\. \*\*Glassbox Explainability.*?too high\."
content = re.sub(pattern, "</details>", content, flags=re.DOTALL)

# Let's add blockquotes to the key findings to make them look slicker
content = content.replace("1. **Market Evidence:** We established a clear Career Opportunity Frontier. Technical cognitive skills (Coding, AI/ML) require communication (Dashboard/Storytelling) to achieve premium compensation tiers.", "> **Market Evidence:** We established a clear Career Opportunity Frontier. Technical cognitive skills (Coding, AI/ML) require communication (Dashboard/Storytelling) to achieve premium compensation tiers.")

content = content.replace("2. **JDS Findings:** The `dashboard_and_storytelling_skills` interact positively with `maths-stats_skills`, providing a measurable lift in junior salary hikes. The Full ML Model achieved a stable accuracy of **0.865**.", "> **JDS Findings:** The `dashboard_and_storytelling_skills` interact positively with `maths-stats_skills`, providing a measurable lift in junior salary hikes. The Full ML Model achieved a stable accuracy of **0.865**.")

content = content.replace("3. **SDS Findings:** Conscientiousness exhibits plateauing, non-additive effects with Extraversion in Senior Data Scientist success classifications. Our model achieved a robust **0.992** ROC-AUC (which safely drops to 0.589 under a shuffled-target test, definitively proving no data leakage).", "> **SDS Findings:** Conscientiousness exhibits plateauing, non-additive effects with Extraversion in Senior Data Scientist success classifications. Our model achieved a robust **0.992** ROC-AUC (which safely drops to 0.589 under a shuffled-target test, definitively proving no data leakage).")

# Clean up HR implications
content = content.replace("- **For HR Professionals:**", "💡 **For HR Professionals:**")
content = content.replace("- **For Analytics Professionals:**", "📊 **For Analytics Professionals:**")
content = content.replace("- **For Algorithmic Governance:**", "⚖️ **For Algorithmic Governance:**")

with open('README.md', 'w') as f:
    f.write(content)
