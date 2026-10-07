import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

sns.set_theme(style="whitegrid", context="paper")

project_root = os.path.dirname(os.path.abspath(__file__))
fig_dir = os.path.join(project_root, 'reports', 'figures', 'eda')
os.makedirs(fig_dir, exist_ok=True)

df_jds = pd.read_excel(os.path.join(project_root, 'data/processed/jds_skills_clean.xlsx'))
df_jds.columns = df_jds.columns.str.replace(" ", "")

df_sds = pd.read_excel(os.path.join(project_root, 'data/processed/sds_personality_clean.xlsx'))
df_sds.columns = df_sds.columns.str.replace(" ", "")

df_analytics = pd.read_csv(os.path.join(project_root, 'data/processed/analytics_jobs_clean.csv'))

jds_features = ["big_data_skills", "maths-stats_skills", "coding_skills", "ai_and_ml_skills", "dashboard_and_storytelling_skills"]
sds_features = ["neuroticism", "extraversion", "openness_to_experience", "agreeableness", "conscientiousness"]

# 1. JDS Correlation Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(df_jds[jds_features].corr(), annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
plt.title("JDS Skill Correlation Matrix")
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'jds_corr.png'), dpi=150)
plt.close()

# 2. SDS Correlation Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(df_sds[sds_features].corr(), annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
plt.title("SDS Personality Correlation Matrix")
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'sds_corr.png'), dpi=150)
plt.close()

# 3. PCA Projection for JDS
X_jds = df_jds[jds_features]
scaler = StandardScaler()
X_jds_scaled = scaler.fit_transform(X_jds)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_jds_scaled)

plt.figure(figsize=(8, 6))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df_jds["salary_hike_high_or_low"], cmap='coolwarm', edgecolors='k', alpha=0.8)
plt.title(f"PCA 2D Projection of Junior Skills (High vs Low Hike)\nPC1: {pca.explained_variance_ratio_[0]:.1%} | PC2: {pca.explained_variance_ratio_[1]:.1%}")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.colorbar(scatter, ticks=[0, 1], label='Salary Hike Outcome')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'jds_pca.png'), dpi=150)
plt.close()

# 4. Feature Separability (KDE plots) - JDS
plt.figure(figsize=(15, 10))
for i, feature in enumerate(jds_features, 1):
    plt.subplot(3, 2, i)
    sns.kdeplot(data=df_jds, x=feature, hue="salary_hike_high_or_low", fill=True, common_norm=False, palette=['#e74c3c', '#2ecc71'])
    plt.title(f"Distribution: {feature.replace('_', ' ').title()}")
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'jds_separability.png'), dpi=150)
plt.close()

# 5. Feature Separability (KDE plots) - SDS
plt.figure(figsize=(15, 10))
for i, feature in enumerate(sds_features, 1):
    plt.subplot(3, 2, i)
    sns.kdeplot(data=df_sds, x=feature, hue="success_classification_high_low", fill=True, common_norm=False, palette=['#e74c3c', '#2ecc71'])
    plt.title(f"Distribution: {feature.replace('_', ' ').title()}")
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'sds_separability.png'), dpi=150)
plt.close()

# 6. Missingness Map
plt.figure(figsize=(10, 6))
missing_ratio = (df_analytics.isnull().sum() / len(df_analytics))[df_analytics.isnull().sum() > 0].sort_values()
sns.barplot(x=missing_ratio.values, y=missing_ratio.index, palette='Reds_d')
plt.title("Missingness Map (Analytics Jobs)")
plt.xlabel("Ratio of Missing Values")
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'missingness_map.png'), dpi=150)
plt.close()

print("Generated EDA static figures.")
