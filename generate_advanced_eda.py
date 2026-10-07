import pandas as pd
import numpy as np
import json
import os
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

np.random.seed(42)

# Paths
project_root = os.path.dirname(os.path.abspath(__file__))
jds_path = os.path.join(project_root, 'data/processed/jds_skills_clean.xlsx')
sds_path = os.path.join(project_root, 'data/processed/sds_personality_clean.xlsx')
analytics_path = os.path.join(project_root, 'data/processed/analytics_jobs_clean.csv')

# Load data
df_jds = pd.read_excel(jds_path)
df_jds.columns = df_jds.columns.str.replace(" ", "")

df_sds = pd.read_excel(sds_path)
df_sds.columns = df_sds.columns.str.replace(" ", "")

df_analytics = pd.read_csv(analytics_path)

eda_results = {}

# 1. JDS Correlation Matrix
jds_features = ["big_data_skills", "maths-stats_skills", "coding_skills", "ai_and_ml_skills", "dashboard_and_storytelling_skills"]
jds_corr = df_jds[jds_features].corr().round(3)
eda_results['jds_corr'] = {
    'columns': jds_corr.columns.tolist(),
    'values': jds_corr.values.tolist()
}

# 2. SDS Correlation Matrix
sds_features = ["neuroticism", "extraversion", "openness_to_experience", "agreeableness", "conscientiousness"]
sds_corr = df_sds[sds_features].corr().round(3)
eda_results['sds_corr'] = {
    'columns': sds_corr.columns.tolist(),
    'values': sds_corr.values.tolist()
}

# 3. PCA for JDS
X_jds = df_jds[jds_features]
scaler = StandardScaler()
X_jds_scaled = scaler.fit_transform(X_jds)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_jds_scaled)

pca_data = {
    'pc1': X_pca[:, 0].tolist(),
    'pc2': X_pca[:, 1].tolist(),
    'target': df_jds["salary_hike_high_or_low"].tolist(),
    'variance_explained': pca.explained_variance_ratio_.tolist()
}
eda_results['jds_pca'] = pca_data

# 4. Feature distributions by target (KDE approximations for plotly)
def get_hist_data(df, feature, target_col):
    h0, bins0 = np.histogram(df[df[target_col]==0][feature].dropna(), bins=10, density=True)
    h1, bins1 = np.histogram(df[df[target_col]==1][feature].dropna(), bins=10, density=True)
    return {
        'bins0': bins0.tolist(), 'hist0': h0.tolist(),
        'bins1': bins1.tolist(), 'hist1': h1.tolist()
    }

eda_results['jds_dists'] = {}
for f in jds_features:
    eda_results['jds_dists'][f] = get_hist_data(df_jds, f, "salary_hike_high_or_low")

eda_results['sds_dists'] = {}
for f in sds_features:
    eda_results['sds_dists'][f] = get_hist_data(df_sds, f, "success_classification_high_low")

# 5. Missingness (Analytics Jobs)
missing_counts = df_analytics.isnull().sum().to_dict()
total_rows = len(df_analytics)
eda_results['missingness'] = {k: float(v/total_rows) for k, v in missing_counts.items() if v > 0}

with open(os.path.join(project_root, 'reports/evidence/advanced_eda.json'), 'w') as f:
    json.dump(eda_results, f)

print("Advanced EDA metrics calculated and saved.")
