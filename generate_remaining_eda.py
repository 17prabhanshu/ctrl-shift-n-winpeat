import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import mutual_info_classif

sns.set_theme(style="whitegrid", context="paper")

project_root = os.path.dirname(os.path.abspath(__file__))
fig_dir = os.path.join(project_root, 'reports', 'figures', 'eda')
os.makedirs(fig_dir, exist_ok=True)

df_jds = pd.read_excel(os.path.join(project_root, 'data/processed/jds_skills_clean.xlsx'))
df_jds.columns = df_jds.columns.str.replace(" ", "")
df_sds = pd.read_excel(os.path.join(project_root, 'data/processed/sds_personality_clean.xlsx'))
df_sds.columns = df_sds.columns.str.replace(" ", "")

# Load skill frequencies for Lorenz curve
import json
try:
    with open(os.path.join(project_root, 'reports/evidence/skill_analysis.json'), 'r') as f:
        skills_data = json.load(f)
        skill_freq = skills_data.get('skill_frequencies', {})
except:
    skill_freq = {}

# 1. Lorenz Curve (Cumulative Skill Concentration)
if skill_freq:
    freqs = sorted(list(skill_freq.values()), reverse=True)
    cum_freq = np.cumsum(freqs) / np.sum(freqs)
    
    plt.figure(figsize=(8, 6))
    plt.plot(np.arange(1, len(cum_freq)+1) / len(cum_freq), cum_freq, marker='', color='b', linewidth=2, label='Observed Concentration')
    plt.plot([0, 1], [0, 1], color='k', linestyle='--', label='Perfect Equality')
    plt.fill_between(np.arange(1, len(cum_freq)+1) / len(cum_freq), cum_freq, np.arange(1, len(cum_freq)+1) / len(cum_freq), alpha=0.2, color='blue')
    plt.title("Skill Demand Concentration (Lorenz Curve)")
    plt.xlabel("Cumulative Proportion of Unique Skills")
    plt.ylabel("Cumulative Proportion of Total Demand")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'skill_lorenz_curve.png'), dpi=150)
    plt.close()

# 2. Mutual Information Scores (JDS)
jds_features = ["big_data_skills", "maths-stats_skills", "coding_skills", "ai_and_ml_skills", "dashboard_and_storytelling_skills"]
X = df_jds[jds_features].fillna(0)
y = df_jds["salary_hike_high_or_low"]

mi_scores = mutual_info_classif(X, y, random_state=42)
mi_series = pd.Series(mi_scores, index=[f.replace('_skills', '').replace('_', ' ').title() for f in jds_features]).sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=mi_series.values, y=mi_series.index, palette="viridis")
plt.title("Mutual Information Scores (Information Gain) - JDS")
plt.xlabel("Mutual Information")
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'jds_mutual_information.png'), dpi=150)
plt.close()

# 3. Class Balance
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.countplot(data=df_jds, x="salary_hike_high_or_low", palette=["#e74c3c", "#2ecc71"])
plt.title("JDS Target Class Balance")
plt.xticks([0, 1], ['Low Hike', 'High Hike'])

plt.subplot(1, 2, 2)
sns.countplot(data=df_sds, x="success_classification_high_low", palette=["#e74c3c", "#2ecc71"])
plt.title("SDS Target Class Balance")
plt.xticks([0, 1], ['Low Success', 'High Success'])

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'target_class_balance.png'), dpi=150)
plt.close()

print("Remaining EDA elements generated.")
