import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
EVIDENCE_DIR = REPORTS_DIR / "evidence"
BENCHMARKS_DIR = REPORTS_DIR / "benchmarks"

st.set_page_config(
    page_title="Workforce Intelligence Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .reportview-container .main .block-container{
        max-width: 1200px;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("Workforce Intelligence Engine")
st.markdown("*Does the market pay for what progression rewards?*")
st.markdown("---")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "1. Market Radar",
    "2. Skill Intelligence",
    "3. Career Progression (JDS)",
    "4. Senior Success (SDS)",
    "5. Model Lab"
])

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

if page == "1. Market Radar":
    st.header("Market Radar")
    st.markdown("Analyzing demand, salary, and experience across roles.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Role Demand")
        demand_img = FIGURES_DIR / "market_role_demand.png"
        if demand_img.exists():
            st.image(str(demand_img), use_container_width=True)
            
        st.subheader("Salary Distribution")
        salary_img = FIGURES_DIR / "market_salary_dist.png"
        if salary_img.exists():
            st.image(str(salary_img), use_container_width=True)
            
    with col2:
        st.subheader("Career Opportunity Frontier")
        frontier_img = FIGURES_DIR / "career_opportunity_frontier.png"
        if frontier_img.exists():
            st.image(str(frontier_img), use_container_width=True)
            
        st.subheader("Experience vs Salary")
        exp_img = FIGURES_DIR / "market_experience.png"
        if exp_img.exists():
            st.image(str(exp_img), use_container_width=True)

elif page == "2. Skill Intelligence":
    st.header("Skill Intelligence")
    st.markdown("Analyzing skill demand and co-occurrence.")
    
    st.subheader("Skill Co-occurrence Graph")
    graph_img = FIGURES_DIR / "skill_cooccurrence_graph.png"
    if graph_img.exists():
        st.image(str(graph_img), use_container_width=True)
        
    st.subheader("Knowledge Graph")
    kg_img = FIGURES_DIR / "knowledge_graph.png"
    if kg_img.exists():
        st.image(str(kg_img), use_container_width=True)

elif page == "3. Career Progression (JDS)":
    st.header("Career Progression: Junior Data Scientists")
    st.markdown("Predicting early-career salary hikes based on technical and communication skills.")
    
    st.subheader("Feature Importance & SHAP")
    shap_jds = FIGURES_DIR / "shap_summary_jds.png"
    if shap_jds.exists():
        st.image(str(shap_jds), use_container_width=True)
    else:
        st.info("SHAP analysis is currently running...")

elif page == "4. Senior Success (SDS)":
    st.header("Senior Success: Senior Data Scientists")
    st.markdown("Analyzing personality traits and their association with executive success.")
    
    st.subheader("Feature Importance & SHAP")
    shap_sds = FIGURES_DIR / "shap_summary_sds.png"
    if shap_sds.exists():
        st.image(str(shap_sds), use_container_width=True)
    else:
        st.info("SHAP analysis is currently running...")

elif page == "5. Model Lab":
    st.header("Model Lab & Governance")
    st.markdown("Rigorous validation, calibration, and benchmarking of all models.")
    
    st.subheader("Probability Calibration")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**JDS Calibration**")
        cal_jds = FIGURES_DIR / "calibration_jds.png"
        if cal_jds.exists():
            st.image(str(cal_jds), use_container_width=True)
    with col2:
        st.markdown("**SDS Calibration**")
        cal_sds = FIGURES_DIR / "calibration_sds.png"
        if cal_sds.exists():
            st.image(str(cal_sds), use_container_width=True)
            
    st.subheader("Robustness & Ablation")
    st.info("Robustness and ablation results loading...")
    
st.sidebar.markdown("---")
st.sidebar.markdown("**Team ctrl shift n**")
st.sidebar.markdown("SAS CU Hackathon 2026")
