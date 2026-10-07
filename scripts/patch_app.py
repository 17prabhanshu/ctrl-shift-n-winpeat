import re
import os

app_path = '/Users/prabhanshushekhar/Desktop/ctrlshiftn/app/app.py'
with open(app_path, 'r') as f:
    app_code = f.read()

# 1. Add advanced_eda.json loading
load_block = """
analytics_jobs = load_csv(DATA_DIR / "analytics_jobs_clean.csv")
jds_data = load_excel(DATA_DIR / "jds_skills_clean.xlsx")
sds_data = load_excel(DATA_DIR / "sds_personality_clean.xlsx")
advanced_eda = load_json(EVIDENCE_DIR / "advanced_eda.json")
"""
app_code = app_code.replace("""
analytics_jobs = load_csv(DATA_DIR / "analytics_jobs_clean.csv")
jds_data = load_excel(DATA_DIR / "jds_skills_clean.xlsx")
sds_data = load_excel(DATA_DIR / "sds_personality_clean.xlsx")
""", load_block)

# 2. Add Advanced EDA tabs
eda_page_header = """
elif page == "📊 Data Exploration":
    st.markdown("# 📊 Advanced Exploratory Data Analysis (EDA)")
    st.markdown("*Data manipulation, derivation, consolidation, and multivariate exploratory strategies*")
    st.markdown("---")

    tab1, tab2, tab3, tab_pca, tab_dist, tab4 = st.tabs([
        "🏢 Market Demand", "💰 Compensation", "🛠️ Skills", 
        "🧠 PCA & Correlations", "📈 Feature Separability", "🧹 Data Quality"
    ])
"""
app_code = re.sub(
    r'elif page == "📊 Data Exploration":.*?tab1, tab2, tab3, tab4 = st.tabs\(\["🏢 Market Demand", "💰 Compensation", "🛠️ Skills", "🧹 Data Quality"\]\)',
    eda_page_header,
    app_code,
    flags=re.DOTALL
)

# 3. Add content for PCA and Distributions tabs
new_tabs_content = """
    with tab_pca:
        st.markdown("### 🧠 Multivariate Feature Analysis")
        st.markdown("Understanding the structural relationships between features before modeling.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### JDS Skill Correlation Matrix")
            if advanced_eda and 'jds_corr' in advanced_eda:
                import plotly.figure_factory as ff
                z = advanced_eda['jds_corr']['values']
                x = [c.replace('_skills','').replace('_',' ') for c in advanced_eda['jds_corr']['columns']]
                fig = ff.create_annotated_heatmap(z, x=x, y=x, colorscale='Viridis', showscale=True)
                fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig, use_container_width=True)
                
        with c2:
            st.markdown("#### PCA (2D Projection) of JDS Skills")
            if advanced_eda and 'jds_pca' in advanced_eda:
                pca = advanced_eda['jds_pca']
                df_pca = pd.DataFrame({'PC1': pca['pc1'], 'PC2': pca['pc2'], 'Target': pca['target']})
                df_pca['Outcome'] = df_pca['Target'].map({0: 'Low Hike', 1: 'High Hike'})
                fig = px.scatter(df_pca, x='PC1', y='PC2', color='Outcome', 
                               color_discrete_sequence=["#D63031", "#00B894"],
                               title=f"Explained Variance: {pca['variance_explained'][0]*100:.1f}% (PC1), {pca['variance_explained'][1]*100:.1f}% (PC2)")
                fig.update_layout(template="plotly_dark", height=400)
                st.plotly_chart(fig, use_container_width=True)

    with tab_dist:
        st.markdown("### 📈 Feature Separability by Outcome")
        st.markdown("Kernel Density approximations to evaluate how individual traits separate success.")
        
        dataset_choice = st.radio("Dataset for Distribution", ["Senior Personality (SDS)", "Junior Skills (JDS)"], horizontal=True)
        
        if "SDS" in dataset_choice and advanced_eda and 'sds_dists' in advanced_eda:
            features = list(advanced_eda['sds_dists'].keys())
            cols = st.columns(2)
            for i, f in enumerate(features):
                d = advanced_eda['sds_dists'][f]
                fig = go.Figure()
                # Use bar to approximate hist
                fig.add_trace(go.Bar(x=d['bins0'][:-1], y=d['hist0'], name='Low Success', marker_color='#D63031', opacity=0.7))
                fig.add_trace(go.Bar(x=d['bins1'][:-1], y=d['hist1'], name='High Success', marker_color='#00B894', opacity=0.7))
                fig.update_layout(template="plotly_dark", title=f.replace('_',' ').title(), barmode='overlay', height=300, margin=dict(l=0, r=0, t=30, b=0))
                cols[i % 2].plotly_chart(fig, use_container_width=True)
                
        elif "JDS" in dataset_choice and advanced_eda and 'jds_dists' in advanced_eda:
            features = list(advanced_eda['jds_dists'].keys())
            cols = st.columns(2)
            for i, f in enumerate(features):
                d = advanced_eda['jds_dists'][f]
                fig = go.Figure()
                fig.add_trace(go.Bar(x=d['bins0'][:-1], y=d['hist0'], name='Low Hike', marker_color='#D63031', opacity=0.7))
                fig.add_trace(go.Bar(x=d['bins1'][:-1], y=d['hist1'], name='High Hike', marker_color='#00B894', opacity=0.7))
                fig.update_layout(template="plotly_dark", title=f.replace('_skills','').replace('_',' ').title(), barmode='overlay', height=300, margin=dict(l=0, r=0, t=30, b=0))
                cols[i % 2].plotly_chart(fig, use_container_width=True)

"""

# Insert new tabs content right before 'with tab4:'
app_code = app_code.replace("    with tab4:", new_tabs_content + "\n    with tab4:")

# Update Tab 4 missingness
missingness_block = """
        if advanced_eda and 'missingness' in advanced_eda:
            st.markdown("### Missingness Map (Analytics Jobs)")
            missing = advanced_eda['missingness']
            if missing:
                df_miss = pd.DataFrame({'Column': list(missing.keys()), 'Missing Ratio': list(missing.values())})
                fig = px.bar(df_miss, x='Missing Ratio', y='Column', orientation='h', color='Missing Ratio', color_continuous_scale='Reds')
                fig.update_layout(template="plotly_dark", height=300, margin=dict(l=0, r=0, t=10, b=10))
                st.plotly_chart(fig, use_container_width=True)
"""
app_code = app_code.replace("        quality = load_json(REPORTS_DIR / \"data_quality_report.json\")", missingness_block + "\n        quality = load_json(REPORTS_DIR / \"data_quality_report.json\")")

with open(app_path, 'w') as f:
    f.write(app_code)

print("App patched successfully with advanced EDA visualizations.")
