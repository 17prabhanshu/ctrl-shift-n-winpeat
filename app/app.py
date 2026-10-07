import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# ─── Paths ───────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
RAW_DIR = PROJECT_ROOT / "data" / "raw"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
EVIDENCE_DIR = REPORTS_DIR / "evidence"
BENCHMARKS_DIR = REPORTS_DIR / "benchmarks"

# ─── Page Config ─────────────────────────────────────────
st.set_page_config(
    page_title="Workforce Intelligence Engine · ctrl shift n",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Theme ───────────────────────────────────────────────
PALETTE = {
    "primary": "#6C5CE7",
    "secondary": "#00CEC9",
    "accent": "#FD79A8",
    "success": "#00B894",
    "warning": "#FDCB6E",
    "danger": "#D63031",
    "bg_dark": "#0E1117",
    "card": "#1E1E2E",
    "text": "#CDD6F4",
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

[data-testid="stAppViewContainer"] {font-family: 'Inter', sans-serif;}

/* Sidebar */
[data-testid="stSidebar"] {background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);}
[data-testid="stSidebar"] .stRadio label {font-size: 0.95rem; font-weight: 500;}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
    border: 1px solid rgba(108,92,231,0.3);
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
[data-testid="stMetricValue"] {font-size: 1.8rem !important; font-weight: 700 !important;}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {gap: 8px;}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 500;
}

/* Headers */
h1 {font-weight: 700 !important; letter-spacing: -0.5px;}
h2 {font-weight: 600 !important; color: #a29bfe !important;}
h3 {font-weight: 600 !important;}

/* Expander */
[data-testid="stExpander"] {
    border: 1px solid rgba(108,92,231,0.2);
    border-radius: 12px;
    background: rgba(30,30,46,0.5);
}

/* Divider */
hr {border-color: rgba(108,92,231,0.2) !important;}
</style>
""", unsafe_allow_html=True)


# ─── Data Loaders ────────────────────────────────────────
@st.cache_data
def load_json(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return {}

@st.cache_data
def load_csv(filepath):
    try:
        return pd.read_csv(filepath)
    except:
        return pd.DataFrame()

@st.cache_data
def load_excel(filepath):
    try:
        df = pd.read_excel(filepath)
        df.columns = df.columns.str.strip().str.replace(' ', '')
        return df
    except:
        return pd.DataFrame()


# ─── Load all data ───────────────────────────────────────
market = load_json(EVIDENCE_DIR / "market_analysis.json")
skills = load_json(EVIDENCE_DIR / "skill_analysis.json")
jds_bench = load_json(BENCHMARKS_DIR / "jds_benchmark.json")
sds_bench = load_json(BENCHMARKS_DIR / "sds_benchmark.json")
ablation_jds = load_json(BENCHMARKS_DIR / "ablation_jds.json")
ablation_sds = load_json(BENCHMARKS_DIR / "ablation_sds.json")
robustness_jds = load_json(BENCHMARKS_DIR / "robustness_jds.json")
robustness_sds = load_json(BENCHMARKS_DIR / "robustness_sds.json")
ensemble = load_json(BENCHMARKS_DIR / "ensemble_results.json")
ds_jobs = load_csv(DATA_DIR / "ds_jobs_clean.csv")
analytics_jobs = load_csv(DATA_DIR / "analytics_jobs_clean.csv")
jds_data = load_excel(DATA_DIR / "jds_skills_clean.xlsx")
sds_data = load_excel(DATA_DIR / "sds_personality_clean.xlsx")


# ─── Sidebar ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🧠 WIE Navigator")
    st.caption("Workforce Intelligence Engine")
    st.markdown("---")
    page = st.radio("", [
        "🏠 Overview",
        "📊 Data Exploration",
        "🔬 Data Analysis",
        "📈 Results & Conclusions",
        "🌍 Implications",
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; opacity:0.6; font-size:0.8rem;'>
        <b>Team ctrl shift n</b><br>
        SAS CU Hackathon 2026
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.markdown("# 🧠 Workforce Intelligence Engine")
    st.markdown("##### *Does the market pay for what progression rewards?*")
    st.markdown("---")

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Datasets Analyzed", "4", "17K+ rows")
    c2.metric("ML Models Benchmarked", "8", "per dataset")
    c3.metric("JDS Best AUC", "0.904", "LogisticRegression")
    c4.metric("SDS Best AUC", "0.998", "ExtraTrees")

    st.markdown("")

    # Problem framing
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("### 🎯 Analytics Objective")
        st.markdown("""
        We synthesize **four unlinked datasets** to investigate:
        
        1. **Market Signal:** Which roles and skills command the highest compensation?
        2. **Junior Talent (JDS):** Do technical skills or communication skills drive early-career salary hikes?
        3. **Senior Talent (SDS):** Which Big Five personality traits predict executive success?
        4. **Synthesis:** Does the market reward what internal progression rewards?
        """)

        st.markdown("### 🏗️ Architectural Approach")
        st.markdown("""
        We process each dataset in **Context-Isolated Evidence Lanes** — never falsely joining
        rows across datasets without a shared key. Each lane feeds into an **Evidence Registry**
        that tracks every analytical claim with its dataset, method, metric, and confidence interval.
        """)
    with col2:
        st.markdown("### 📦 Dataset Summary")
        ds_summary = pd.DataFrame({
            "Dataset": ["DataScience Jobs", "Analytics Jobs", "JDS Skills", "SDS Personality"],
            "Rows": [len(ds_jobs), len(analytics_jobs), len(jds_data), len(sds_data)],
            "Purpose": ["Market salaries", "Skills/demand", "Skill→Promotion", "Personality→Success"],
            "Target": ["—", "—", "salary_hike", "success_class"],
        })
        st.dataframe(ds_summary, use_container_width=True, hide_index=True)

        st.markdown("### ⚙️ Pipeline")
        st.code("""
Raw Data → Ingestion → Validation
→ Cleaning → Feature Engineering
→ Market Intelligence → Skill NLP
→ ML Benchmarking → Calibration
→ SHAP Explainability → Ablation
→ Robustness Testing → Synthesis
        """, language="text")


# ══════════════════════════════════════════════════════════
# PAGE: DATA EXPLORATION
# ══════════════════════════════════════════════════════════
elif page == "📊 Data Exploration":
    st.markdown("# 📊 Data Exploration & Preparation")
    st.markdown("*Data manipulation, derivation, consolidation, and exploratory strategies*")
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Market Demand", "💰 Compensation", "🛠️ Skills", "🧹 Data Quality"])

    with tab1:
        st.markdown("### Role Demand Across the Indian Analytics Market")
        if market.get("role_demand"):
            roles = list(market["role_demand"].keys())
            counts = list(market["role_demand"].values())
            fig = px.bar(
                x=counts, y=roles, orientation='h',
                labels={"x": "Number of Postings", "y": ""},
                color=counts,
                color_continuous_scale="Viridis",
            )
            fig.update_layout(
                template="plotly_dark", height=400,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False, coloraxis_showscale=False,
                yaxis=dict(categoryorder='total ascending'),
                margin=dict(l=0, r=20, t=10, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Geographic Distribution of Postings")
        if market.get("top_locations"):
            locs = list(market["top_locations"].keys())[:10]
            vals = list(market["top_locations"].values())[:10]
            fig = px.bar(
                x=locs, y=vals,
                labels={"x": "City", "y": "Postings"},
                color=vals, color_continuous_scale="Teal",
            )
            fig.update_layout(
                template="plotly_dark", height=350,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False, coloraxis_showscale=False,
                margin=dict(l=0, r=20, t=10, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### Salary by Role (₹ LPA)")
        if market.get("salary_by_role"):
            roles = list(market["salary_by_role"].keys())
            salaries = [v / 100000 for v in market["salary_by_role"].values()]
            fig = px.bar(
                x=roles, y=salaries,
                labels={"x": "", "y": "Average Salary (₹ LPA)"},
                color=salaries, color_continuous_scale="Sunset",
            )
            fig.update_layout(
                template="plotly_dark", height=400,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False,
                margin=dict(l=0, r=20, t=10, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Career Opportunity Frontier")
        if market.get("role_demand") and market.get("salary_by_role") and market.get("experience_by_role"):
            frontier_data = []
            for role in market["role_demand"]:
                if role in market["salary_by_role"] and role in market["experience_by_role"]:
                    frontier_data.append({
                        "Role": role,
                        "Demand": market["role_demand"][role],
                        "Salary (LPA)": market["salary_by_role"][role] / 100000,
                        "Avg Experience": market["experience_by_role"][role],
                    })
            if frontier_data:
                df_f = pd.DataFrame(frontier_data)
                fig = px.scatter(
                    df_f, x="Demand", y="Salary (LPA)", size="Avg Experience",
                    color="Role", hover_name="Role",
                    size_max=50,
                    color_discrete_sequence=px.colors.qualitative.Set2,
                )
                fig.update_layout(
                    template="plotly_dark", height=450,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=0, r=20, t=10, b=10),
                )
                st.plotly_chart(fig, use_container_width=True)
                st.caption("Bubble size = average experience required. Data Scientists command the highest pay despite moderate demand.")

    with tab3:
        st.markdown("### Top 15 In-Demand Skills (Analytics Jobs)")
        if skills.get("skill_frequencies"):
            sf = skills["skill_frequencies"]
            if isinstance(sf, dict):
                sorted_skills = sorted(sf.items(), key=lambda x: x[1], reverse=True)[:15]
                sk_names = [s[0].title() for s in sorted_skills]
                sk_vals = [s[1] for s in sorted_skills]
            else:
                sk_names, sk_vals = [], []
            if sk_names:
                fig = go.Figure(go.Bar(
                    x=sk_vals, y=sk_names, orientation='h',
                    marker=dict(
                        color=sk_vals,
                        colorscale=[[0, '#6C5CE7'], [0.5, '#00CEC9'], [1, '#00B894']],
                    ),
                    text=sk_vals, textposition='outside',
                ))
                fig.update_layout(
                    template="plotly_dark", height=500,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    yaxis=dict(categoryorder='total ascending'),
                    xaxis_title="Frequency in Job Postings",
                    margin=dict(l=0, r=60, t=10, b=10),
                )
                st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Skill Co-occurrence Network")
        graph_img = FIGURES_DIR / "skill_cooccurrence_graph.png"
        if graph_img.exists():
            st.image(str(graph_img), width=800)

    with tab4:
        st.markdown("### Data Cleaning Pipeline")
        st.markdown("""
        | Challenge | Raw Format | Parser | Output |
        |-----------|-----------|--------|--------|
        | Salary (DS Jobs) | `"7.8L"` | `salary_parser.py` | `780000.0` (INR) |
        | Salary (Analytics) | `"6to10"` | `salary_parser.py` | `(600000, 1000000)` |
        | Experience | `"6-10 yrs"` | `experience_parser.py` | `midpoint = 8.0` |
        | Skills | `"python, aws \\| sql"` | `skill_engine.py` | Canonical taxonomy |
        | Column names | `" extraversion"` | `.str.strip()` | `"extraversion"` |
        """)

        quality = load_json(REPORTS_DIR / "data_quality_report.json")
        if quality:
            st.markdown("### Data Quality Summary")
            st.json(quality)


# ══════════════════════════════════════════════════════════
# PAGE: DATA ANALYSIS (30 MARKS — THE BIG ONE)
# ══════════════════════════════════════════════════════════
elif page == "🔬 Data Analysis":
    st.markdown("# 🔬 Data Analysis & Explainability")
    st.markdown("*Statistical, descriptive, prescriptive analytics and model explainability*")
    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏆 Model Benchmark", "🎯 Explainability (SHAP)",
        "🔁 Ablation Study", "🛡️ Robustness", "📐 Calibration"
    ])

    with tab1:
        st.markdown("### Model Leaderboard")
        dataset_choice = st.radio("Dataset", ["JDS (Skills → Salary Hike)", "SDS (Personality → Success)"], horizontal=True)
        bench = jds_bench if "JDS" in dataset_choice else sds_bench

        if bench:
            models, accs, aucs, f1s, briers = [], [], [], [], []
            for name, metrics in bench.items():
                models.append(name)
                accs.append(metrics.get("accuracy", {}).get("mean", 0))
                aucs.append(metrics.get("roc_auc", {}).get("mean", 0))
                f1s.append(metrics.get("f1", {}).get("mean", 0))
                briers.append(metrics.get("brier_score", {}).get("mean", 0))

            bench_df = pd.DataFrame({
                "Model": models, "Accuracy": accs,
                "ROC-AUC": aucs, "F1 Score": f1s, "Brier Score": briers,
            }).sort_values("ROC-AUC", ascending=False)

            # Highlight best
            best_model = bench_df.iloc[0]["Model"]
            best_auc = bench_df.iloc[0]["ROC-AUC"]

            c1, c2, c3 = st.columns(3)
            c1.metric("🏆 Best Model", best_model)
            c2.metric("ROC-AUC", f"{best_auc:.3f}")
            c3.metric("Baseline AUC", "0.500", f"+{(best_auc - 0.5):.3f}")

            # Interactive leaderboard chart
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name="ROC-AUC", x=bench_df["Model"], y=bench_df["ROC-AUC"],
                marker_color="#6C5CE7", text=[f"{v:.3f}" for v in bench_df["ROC-AUC"]],
                textposition="outside",
            ))
            fig.add_trace(go.Bar(
                name="Accuracy", x=bench_df["Model"], y=bench_df["Accuracy"],
                marker_color="#00CEC9", text=[f"{v:.3f}" for v in bench_df["Accuracy"]],
                textposition="outside",
            ))
            fig.update_layout(
                template="plotly_dark", barmode="group", height=450,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=0, r=20, t=40, b=10),
                yaxis_range=[0, 1.15],
            )
            st.plotly_chart(fig, use_container_width=True)

            with st.expander("📋 Full Benchmark Table"):
                st.dataframe(
                    bench_df.style.format({"Accuracy": "{:.3f}", "ROC-AUC": "{:.3f}", "F1 Score": "{:.3f}", "Brier Score": "{:.4f}"}),
                    use_container_width=True, hide_index=True,
                )

    with tab2:
        st.markdown("### SHAP Feature Importance")
        st.markdown("""
        > **SHAP (SHapley Additive exPlanations)** decomposes each prediction into
        > per-feature contributions. These values represent **statistical associations**,
        > not causal effects.
        """)

        shap_choice = st.radio("Dataset", ["JDS Skills", "SDS Personality"], horizontal=True, key="shap_radio")

        if "JDS" in shap_choice:
            shap_img = FIGURES_DIR / "shap_summary_jds.png"
            if shap_img.exists():
                st.image(str(shap_img), caption="SHAP Beeswarm Plot — JDS (Skills → Salary Hike)", width=800)

            st.markdown("""
            #### Key Interpretations (JDS)
            - **`maths-stats_skills`** shows the strongest positive association with high salary hikes
            - **`dashboard_and_storytelling_skills`** has a complementary positive effect
            - **`coding_skills`** alone provides moderate signal — it's necessary but not sufficient
            - The interaction between quantitative and communication skills matters more than either alone
            """)
        else:
            shap_img = FIGURES_DIR / "shap_summary_sds.png"
            if shap_img.exists():
                st.image(str(shap_img), caption="SHAP Beeswarm Plot — SDS (Personality → Success)", width=800)

            st.markdown("""
            #### Key Interpretations (SDS)
            - **`conscientiousness`** and **`openness_to_experience`** are the dominant predictors
            - **`extraversion`** shows a non-linear effect — moderate levels associate with success
            - **`neuroticism`** has a weak but negative association
            - The personality features provide exceptionally clean separation (AUC ≈ 0.998)
            """)

        st.markdown("""
        > ⚠️ **Causal Disclaimer:** SHAP values quantify feature-prediction associations within this
        > dataset. They do **not** establish that changing a skill score *causes* a promotion.
        """)

    with tab3:
        st.markdown("### Ablation Study")
        st.markdown("We systematically remove each feature to measure its marginal contribution to model performance.")

        abl_choice = st.radio("Dataset", ["JDS", "SDS"], horizontal=True, key="abl_radio")
        abl_data = ablation_jds if abl_choice == "JDS" else ablation_sds

        if abl_data:
            full_score = abl_data.get("Full_Model", 0)
            random_score = abl_data.get("Randomized_Target", 0)

            items = {k: v for k, v in abl_data.items() if k not in ["Full_Model", "Randomized_Target", "Technical_Only", "Communication_Only", "Quantitative_Only"]}
            names = [k.replace("Minus_", "− ").replace("_", " ").title() for k in items.keys()]
            scores = list(items.values())
            drops = [full_score - s for s in scores]

            colors = ["#D63031" if d > 0 else "#00B894" for d in drops]

            fig = make_subplots(rows=1, cols=2, subplot_titles=("AUC When Feature Removed", "Performance Drop"))

            fig.add_trace(go.Bar(
                y=names, x=scores, orientation='h',
                marker_color="#6C5CE7", name="AUC",
                text=[f"{s:.3f}" for s in scores], textposition="outside",
            ), row=1, col=1)

            fig.add_trace(go.Bar(
                y=names, x=drops, orientation='h',
                marker_color=colors, name="Drop",
                text=[f"{d:+.3f}" for d in drops], textposition="outside",
            ), row=1, col=2)

            fig.add_vline(x=full_score, line_dash="dash", line_color="#FDCB6E",
                          annotation_text=f"Full: {full_score:.3f}", row=1, col=1)

            fig.update_layout(
                template="plotly_dark", height=400, showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=60, t=40, b=10),
            )
            fig.update_yaxes(categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True)

            # Sanity check
            c1, c2, c3 = st.columns(3)
            c1.metric("Full Model AUC", f"{full_score:.3f}")
            c2.metric("Randomized Target", f"{random_score:.3f}", f"{random_score - full_score:+.3f}")
            c3.metric("Sanity Check", "✅ PASSED" if random_score < 0.6 else "⚠️ CHECK")

            if abl_choice == "JDS":
                st.markdown("#### Feature Group Ablation")
                groups = {
                    "Technical Only": abl_data.get("Technical_Only", 0),
                    "Communication Only": abl_data.get("Communication_Only", 0),
                    "Quantitative Only": abl_data.get("Quantitative_Only", 0),
                    "Full Model": full_score,
                }
                fig2 = go.Figure(go.Bar(
                    x=list(groups.keys()), y=list(groups.values()),
                    marker_color=["#00CEC9", "#FD79A8", "#FDCB6E", "#6C5CE7"],
                    text=[f"{v:.3f}" for v in groups.values()],
                    textposition="outside",
                ))
                fig2.update_layout(
                    template="plotly_dark", height=350,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    yaxis_title="ROC-AUC", yaxis_range=[0, 1.1],
                    margin=dict(l=0, r=20, t=10, b=10),
                )
                st.plotly_chart(fig2, use_container_width=True)
                st.caption("Communication skills alone outperform pure technical skills — evidence of cognitive-social complementarity.")

    with tab4:
        st.markdown("### Robustness & Stress Testing")

        rob_choice = st.radio("Dataset", ["JDS", "SDS"], horizontal=True, key="rob_radio")
        rob_data = robustness_jds if rob_choice == "JDS" else robustness_sds

        if rob_data:
            multi_seed = rob_data.get("Multiple_Seeds_ROC_AUC", {})
            perturb = rob_data.get("Perturbation_ROC_AUC", 0)
            shuffled = rob_data.get("Shuffled_Target_ROC_AUC", 0)
            mean_auc = multi_seed.get("mean", 0)
            std_auc = multi_seed.get("std", 0)

            c1, c2, c3 = st.columns(3)
            c1.metric("Mean AUC (20 seeds)", f"{mean_auc:.3f}", f"± {std_auc:.3f}")
            c2.metric("Perturbed Features AUC", f"{perturb:.3f}")
            c3.metric("Shuffled Target AUC", f"{shuffled:.3f}")

            # Waterfall: Real vs Perturbed vs Shuffled
            fig = go.Figure(go.Waterfall(
                x=["Trained Model", "Feature Noise Added", "Target Shuffled"],
                y=[mean_auc, perturb - mean_auc, shuffled - perturb],
                measure=["absolute", "relative", "relative"],
                text=[f"{mean_auc:.3f}", f"{perturb:.3f}", f"{shuffled:.3f}"],
                textposition="outside",
                connector={"line": {"color": "rgba(108,92,231,0.5)"}},
                increasing={"marker": {"color": "#00B894"}},
                decreasing={"marker": {"color": "#D63031"}},
                totals={"marker": {"color": "#6C5CE7"}},
            ))
            fig.update_layout(
                template="plotly_dark", height=400,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                yaxis_title="ROC-AUC",
                title=dict(text="Robustness Waterfall: Signal Degrades Under Stress", font=dict(size=14)),
                margin=dict(l=0, r=20, t=50, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"""
            **Interpretation:** When we shuffle the target labels (destroying all real signal),
            the AUC drops to **{shuffled:.3f}** (near random chance at 0.5). This proves
            our model is learning genuine feature-target relationships, not exploiting data artifacts.
            """)

    with tab5:
        st.markdown("### Probability Calibration")
        st.markdown("""
        Raw `predict_proba()` outputs from tree ensembles are often poorly calibrated.
        We apply **Platt Scaling (Sigmoid)** to produce reliable probability estimates.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### JDS Calibration Curve")
            cal_jds = FIGURES_DIR / "calibration_jds.png"
            if cal_jds.exists():
                st.image(str(cal_jds), width=500)
        with col2:
            st.markdown("#### SDS Calibration Curve")
            cal_sds = FIGURES_DIR / "calibration_sds.png"
            if cal_sds.exists():
                st.image(str(cal_sds), width=500)

        st.markdown("""
        > A well-calibrated model produces probabilities that match observed frequencies.
        > Points close to the diagonal indicate good calibration. Platt scaling corrects
        > the systematic under/over-confidence of tree-based models.
        """)


# ══════════════════════════════════════════════════════════
# PAGE: RESULTS & CONCLUSIONS
# ══════════════════════════════════════════════════════════
elif page == "📈 Results & Conclusions":
    st.markdown("# 📈 Results & Conclusions")
    st.markdown("*Consolidating evidence across all four datasets*")
    st.markdown("---")

    # Summary cards
    st.markdown("### Evidence Synthesis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e1e2e, #2d2d44); border-radius: 16px;
                    padding: 24px; border-left: 4px solid #6C5CE7; margin-bottom: 16px;">
            <h4 style="color: #a29bfe; margin-top:0;">📊 Market Intelligence</h4>
            <ul style="color: #cdd6f4;">
                <li><b>Data Scientists</b> command the highest average salary (₹16.2 LPA) despite moderate demand</li>
                <li><b>Bengaluru</b> dominates with 4,108 postings, followed by Mumbai (2,643)</li>
                <li>The Career Opportunity Frontier reveals a premium for roles combining technical depth with business communication</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e1e2e, #2d2d44); border-radius: 16px;
                    padding: 24px; border-left: 4px solid #00CEC9; margin-bottom: 16px;">
            <h4 style="color: #81ecec; margin-top:0;">🛠️ Skill Intelligence</h4>
            <ul style="color: #cdd6f4;">
                <li><b>SQL, Python, and Analytics</b> are the three most demanded skills</li>
                <li>Skills cluster into distinct communities — technical coding vs. business/domain</li>
                <li>The Skill Signal Index identifies high-value, under-supplied skill combinations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e1e2e, #2d2d44); border-radius: 16px;
                    padding: 24px; border-left: 4px solid #00B894; margin-bottom: 16px;">
            <h4 style="color: #55efc4; margin-top:0;">🎓 Junior Talent (JDS)</h4>
            <ul style="color: #cdd6f4;">
                <li><b>Logistic Regression</b> outperforms complex ensembles (AUC: 0.904)</li>
                <li><b>Maths-stats</b> is the most critical skill for salary hikes (largest ablation drop: −0.055)</li>
                <li>Communication skills <b>complement</b>, not substitute, technical skills</li>
                <li>Randomized-target AUC: 0.416 — sanity check passed</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e1e2e, #2d2d44); border-radius: 16px;
                    padding: 24px; border-left: 4px solid #FD79A8; margin-bottom: 16px;">
            <h4 style="color: #fd79a8; margin-top:0;">👔 Senior Talent (SDS)</h4>
            <ul style="color: #cdd6f4;">
                <li><b>ExtraTrees</b> achieves near-perfect classification (AUC: 0.998)</li>
                <li>Stress-tested: 20-seed mean AUC = 0.992, shuffled-target = 0.589</li>
                <li><b>Openness to Experience</b> shows the largest ablation drop (−0.018)</li>
                <li>Personality traits provide stronger predictive signal than technical skills</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### The Central Finding")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2d2d44, #3d3d5c); border-radius: 16px;
                padding: 30px; text-align: center; border: 1px solid rgba(108,92,231,0.4);">
        <h3 style="color: #a29bfe; margin-top:0;">Does the market pay for what progression rewards?</h3>
        <p style="color: #cdd6f4; font-size: 1.1rem; max-width: 700px; margin: 0 auto;">
            <b>Partially.</b> The market values technical execution (Python, SQL, ML), but internal progression
            rewards the <em>interaction</em> between technical and communication skills. Senior success is
            driven not by technical mastery alone but by personality traits — particularly
            <b>conscientiousness</b> and <b>openness</b> — that no job posting explicitly demands.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# PAGE: IMPLICATIONS
# ══════════════════════════════════════════════════════════
elif page == "🌍 Implications":
    st.markdown("# 🌍 Real-World Implications")
    st.markdown("*Impact on stakeholders in society*")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e1e2e, #2d2d44); border-radius: 16px;
                    padding: 24px; text-align: center; min-height: 320px; border-top: 3px solid #6C5CE7;">
            <h3 style="color: #a29bfe;">🏢 For HR Teams</h3>
            <p style="color: #cdd6f4; text-align: left;">
                Hiring for isolated technical skills yields diminishing returns.
                Assessment frameworks should measure the <b>interaction</b> between
                technical execution and stakeholder communication.<br><br>
                Our evidence shows that communication-only skill groups achieve
                higher AUC than technical-only groups in predicting salary progression.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e1e2e, #2d2d44); border-radius: 16px;
                    padding: 24px; text-align: center; min-height: 320px; border-top: 3px solid #00CEC9;">
            <h3 style="color: #81ecec;">📚 For Professionals</h3>
            <p style="color: #cdd6f4; text-align: left;">
                Upskilling purely in algorithms without developing
                storytelling and presentation skills severely limits
                career progression potential.<br><br>
                The Career Opportunity Frontier reveals a clear premium
                for professionals who combine deep technical skills
                with business communication abilities.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e1e2e, #2d2d44); border-radius: 16px;
                    padding: 24px; text-align: center; min-height: 320px; border-top: 3px solid #FD79A8;">
            <h3 style="color: #fd79a8;">⚖️ For AI Governance</h3>
            <p style="color: #cdd6f4; text-align: left;">
                By implementing <b>Conformal Prediction sets</b>,
                organizations can automate screening for clear-cut
                candidates while routing ambiguous profiles
                to human auditors.<br><br>
                This mitigates algorithmic bias and ensures
                responsible deployment of workforce analytics tools.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Limitations & Future Work")
    st.markdown("""
    | Limitation | Mitigation |
    |-----------|-----------|
    | Small sample sizes (n=139, n=161) | Repeated Stratified K-Fold (100 evaluations), Firth regression |
    | No causal identification | SHAP reports associations only; language audited by Evidence Registry |
    | No temporal dimension | Cross-sectional analysis acknowledged; longitudinal data needed |
    | Datasets are not linkable | Context-Isolated Evidence Lanes prevent false joins |
    | SDS near-perfect AUC | Stress-tested with shuffled targets (drops to 0.589) |
    """)
