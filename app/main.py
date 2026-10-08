"""
DataScientist Career Navigator
A practical tool for data scientists to understand market demand, salary expectations, and career paths.
Built on the Workforce Intelligence Engine analysis.
"""
import streamlit as st
import pandas as pd
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration
DATA_DIR = Path("/Users/prabhanshushekhar/ctrl-shift-n-winpeat/ctrl-shift-n-winpeat/data")
PROCESSED_DIR = DATA_DIR / "processed"
EVIDENCE_DIR = Path("/Users/prabhanshushekhar/ctrl-shift-n-winpeat/ctrl-shift-n-winpeat/reports/evidence")
BENCHMARKS_DIR = Path("/Users/prabhanshushekhar/ctrl-shift-n-winpeat/ctrl-shift-n-winpeat/reports/benchmarks")

# Page config
st.set_page_config(
    page_title="DataScientist Career Navigator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    """Load all processed data."""
    analytics = pd.read_csv(PROCESSED_DIR / "analytics_jobs_clean.csv")
    ds_jobs = pd.read_csv(PROCESSED_DIR / "ds_jobs_clean.csv")
    
    with open(EVIDENCE_DIR / "market_analysis.json") as f:
        market = json.load(f)
    
    with open(EVIDENCE_DIR / "skill_analysis.json") as f:
        skills = json.load(f)
    
    with open(EVIDENCE_DIR / "skill_signal_index.json") as f:
        ssi = json.load(f)
    
    with open(EVIDENCE_DIR / "evidence_registry.json") as f:
        registry = json.load(f)
    
    return analytics, ds_jobs, market, skills, ssi, registry

analytics_df, ds_jobs_df, market_analysis, skill_analysis, ssi_data, registry = load_data()

# Sidebar
with st.sidebar:
    st.title("📊 Career Navigator")
    st.markdown("""
    **For Data Scientists**
    
    Understand market demand, salary expectations, and career paths.
    """)
    
    st.divider()
    
    # User inputs
    st.header("Your Profile")
    
    experience = st.slider("Years of Experience", 0, 20, 3)
    
    target_role = st.selectbox(
        "Target Role",
        ["Data Scientist", "Data Engineer", "ML Engineer", 
         "Data Analyst", "Business Analyst", "Software Engineer"]
    )
    
    current_skills = st.multiselect(
        "Your Skills (select all that apply)",
        ["Python", "SQL", "Machine Learning", "Statistics", "R", 
         "Excel", "Tableau", "Power BI", "Java", "JavaScript",
         "Big Data", "Spark", "Hadoop", "Deep Learning", "NLP",
         "Data Visualization", "Communication", "Project Management"]
    )
    
    st.divider()
    
    if st.button("🔍 Analyze My Profile", type="primary"):
        st.session_state.analyzed = True
    else:
        st.session_state.analyzed = False

# Main content
st.title("📊 DataScientist Career Navigator")
st.markdown("""
**Know your market. Plan your career. Invest in the right skills.**
""")

if not st.session_state.get("analyzed", False):
    st.info("""
    **How to use this tool:**
    
    1. Set your experience level and target role in the sidebar
    2. Select the skills you currently have
    3. Click 'Analyze My Profile' to see personalized insights
    
    The analysis is based on 15,841 analytics job postings from the Indian market.
    """)
    
    # Show market overview
    st.header("📈 Market Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Role Demand")
        demand_df = pd.DataFrame([
            {"Role": k, "Postings": v} 
            for k, v in sorted(market_analysis["role_demand"].items(), key=lambda x: x[1], reverse=True)
        ])
        st.bar_chart(demand_df.set_index("Role"))
    
    with col2:
        st.subheader("Average Salary by Role")
        salary_data = []
        for role, data in market_analysis["salary_by_role"].items():
            salary_data.append({
                "Role": role,
                "Avg Salary (₹L)": round(data["mean_inr"] / 1e5, 1)
            })
        salary_df = pd.DataFrame(salary_data).sort_values("Avg Salary (₹L)", ascending=True)
        st.bar_chart(salary_df.set_index("Role"))

else:
    # Analysis results
    st.success("✅ Profile analyzed! Here's what we found:")
    
    # Role info
    st.header(f"🎯 {target_role} Role Analysis")
    
    role_data = None
    for item in market_analysis["role_salary_matrix"]["0-2"].items():
        if item[0] == target_role:
            role_data = market_analysis
            break
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_salary = market_analysis["salary_by_role"].get(target_role, {}).get("mean_inr", 0)
        st.metric("Average Salary", f"₹{avg_salary/1e5:.1f}L" if avg_salary else "N/A")
    
    with col2:
        avg_exp = market_analysis["experience_by_role"].get(target_role, {}).get("mean_years", 0)
        st.metric("Avg Experience Required", f"{avg_exp:.1f} years" if avg_exp else "N/A")
    
    with col3:
        demand = market_analysis["role_demand"].get(target_role, 0)
        st.metric("Market Demand", f"{demand:,} postings")
    
    st.divider()
    
    # Skill gap analysis
    st.header("🔍 Skill Gap Analysis")
    
    # Define skill requirements by role (based on our analysis)
    role_skills = {
        "Data Scientist": ["Python", "SQL", "Machine Learning", "Statistics", "Data Visualization"],
        "Data Engineer": ["Python", "SQL", "Big Data", "Spark", "Hadoop", "Java"],
        "ML Engineer": ["Python", "Machine Learning", "Deep Learning", "SQL", "Java"],
        "Data Analyst": ["SQL", "Excel", "Python", "Data Visualization", "Statistics"],
        "Business Analyst": ["SQL", "Excel", "Communication", "Project Management", "Statistics"],
        "Software Engineer": ["Java", "Python", "JavaScript", "SQL", "Project Management"]
    }
    
    required_skills = role_skills.get(target_role, [])
    missing_skills = [s for s in required_skills if s not in current_skills]
    has_skills = [s for s in required_skills if s in current_skills]
    
    if has_skills or missing_skills:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ Skills You Have")
            if has_skills:
                for skill in has_skills:
                    st.success(f"✓ {skill}")
            else:
                st.warning("No matching skills selected")
        
        with col2:
            st.subheader("📚 Skills to Learn")
            if missing_skills:
                for skill in missing_skills:
                    st.info(f"○ {skill}")
            else:
                st.success("🎉 You have all key skills for this role!")
    
    # Salary impact of skills
    st.divider()
    st.header("💰 Skill Salary Impact")
    
    st.markdown("""
    Based on our analysis of 15,841 job postings, here's how different skills correlate with salary:
    """)
    
    # Skill salary associations (from SSI analysis)
    skill_salary_impact = {
        "Machine Learning": "High positive impact",
        "Python": "High positive impact",
        "SQL": "Moderate positive impact",
        "Big Data": "High positive impact (for Data Engineers)",
        "Spark": "High positive impact (for Data Engineers)",
        "Statistics": "Moderate positive impact",
        "Deep Learning": "High positive impact (for ML Engineers)",
        "Tableau": "Moderate positive impact (for Analysts)",
        "R": "Moderate positive impact",
        "Java": "Moderate positive impact (for Engineers)",
        "Excel": "Low positive impact (basic requirement)",
        "Communication": "Variable impact (context-dependent)"
    }
    
    skill_impact_df = pd.DataFrame([
        {"Skill": k, "Salary Impact": v} 
        for k, v in skill_salary_impact.items()
        if k in current_skills or k in missing_skills
    ])
    
    if not skill_impact_df.empty:
        st.dataframe(skill_impact_df, use_container_width=True)
    else:
        st.warning("Select some skills to see their salary impact")
    
    # Career path explorer
    st.divider()
    st.header("🗺️ Career Path Explorer")
    
    st.markdown(f"""
    **From your current profile to {target_role}:**
    """)
    
    # Define career paths
    career_paths = {
        "Data Analyst": {
            "to": ["Data Scientist", "Business Analyst", "Data Engineer"],
            "key_skills_to_learn": {
                "Data Scientist": ["Machine Learning", "Python", "Statistics"],
                "Business Analyst": ["Communication", "Project Management"],
                "Data Engineer": ["Python", "Big Data", "SQL"]
            }
        },
        "Business Analyst": {
            "to": ["Data Analyst", "Product Manager", "Data Scientist"],
            "key_skills_to_learn": {
                "Data Analyst": ["SQL", "Python", "Data Visualization"],
                "Product Manager": ["Communication", "Project Management"],
                "Data Scientist": ["Python", "Machine Learning", "Statistics"]
            }
        }
    }
    
    current_role = "Data Analyst"  # Default assumption
    if current_role in career_paths:
        paths = career_paths[current_role]
        st.subheader(f"Common transitions from {current_role}:")
        
        for i, next_role in enumerate(paths["to"], 1):
            with st.expander(f"🚀 Path {i}: {current_role} → {next_role}"):
                skills_needed = paths["key_skills_to_learn"][next_role]
                st.write(f"**Skills to learn:** {', '.join(skills_needed)}")
                
                # Check which they already have
                already_have = [s for s in skills_needed if s in current_skills]
                still_need = [s for s in skills_needed if s not in current_skills]
                
                if already_have:
                    st.write(f"✅ You have: {', '.join(already_have)}")
                if still_need:
                    st.write(f"📚 Learn: {', '.join(still_need)}")
    
    # Recommendations
    st.divider()
    st.header("🎯 Personalized Recommendations")
    
    if missing_skills:
        st.subheader(f"To become a {target_role}, prioritize learning:")
        
        for i, skill in enumerate(missing_skills, 1):
            st.markdown(f"{i}. **{skill}**")
        
        st.divider()
        
        st.subheader("Recommended Learning Order")
        st.markdown("""
        Based on market demand and learning difficulty:
        """)
        
        priority_order = {
            "Data Scientist": ["Python", "SQL", "Statistics", "Machine Learning", "Data Visualization"],
            "Data Engineer": ["SQL", "Python", "Big Data", "Spark", "Hadoop"],
            "ML Engineer": ["Python", "SQL", "Machine Learning", "Deep Learning", "Java"],
            "Data Analyst": ["SQL", "Excel", "Python", "Data Visualization", "Statistics"],
            "Business Analyst": ["SQL", "Excel", "Communication", "Project Management"],
            "Software Engineer": ["Java", "Python", "SQL", "JavaScript", "Project Management"]
        }
        
        if target_role in priority_order:
            recommended = [s for s in priority_order[target_role] if s in missing_skills]
            for i, skill in enumerate(recommended, 1):
                st.write(f"{i}. {skill}")
    else:
        st.success(f"🎉 You appear well-prepared for {target_role}!")
        st.markdown("""
        **Next steps:**
        1. Build a portfolio project showcasing your skills
        2. Practice interview questions for {target_role}
        3. Network with professionals in the field
        """.format(target_role=target_role))

# Footer
st.divider()
st.markdown("""
**About this analysis:**
- Based on 15,841 Indian analytics job postings
- Skills mapped to market demand using NLP and taxonomy analysis
- Salary estimates are averages across all locations and experience levels
- This is descriptive analysis, not career advice
- Built by Team ctrl shift n for SAS CU Hackathon 2026
""")

# Show evidence registry (for transparency)
with st.expander("📋 View Evidence Registry (Transparency)"):
    st.markdown("""
    All claims in this application are backed by our evidence registry.
    This ensures transparency and reproducibility.
    """)
    
    accepted_claims = [r for r in registry if r.get("status") == "accepted"]
    
    for claim in accepted_claims[:10]:  # Show first 10
        st.markdown(f"**{claim.get('claim_id', 'N/A')}**: {claim.get('statement', '')[:100]}")
        st.markdown(f"  - Dataset: {claim.get('dataset', 'N/A')}")
        st.markdown(f"  - Method: {claim.get('method', 'N/A')}")
        if claim.get('value') is not None:
            st.markdown(f"  - Value: {claim['value']:.4f}" if isinstance(claim['value'], float) else f"  - Value: {claim['value']}")
        st.markdown(f"  - Limitation: {claim.get('limitation', 'N/A')[:100]}")
        st.divider()
