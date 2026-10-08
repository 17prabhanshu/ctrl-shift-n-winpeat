"""
Market Intelligence Module - salary, demand, and role analysis.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path
from src.utils.config import (
    PROCESSED_DIR, REPORTS_DIR, EVIDENCE_DIR, FIGURES_DIR,
    categorize_role
)

def analyze_market():
    """Run complete market analysis."""
    print("=" * 60)
    print("MARKET INTELLIGENCE ANALYSIS")
    print("=" * 60)
    
    # Load cleaned data
    ds_jobs = pd.read_csv(PROCESSED_DIR / 'ds_jobs_clean.csv')
    analytics_jobs = pd.read_csv(PROCESSED_DIR / 'analytics_jobs_clean.csv')
    
    print(f"\nLoaded: DS Jobs {ds_jobs.shape}, Analytics Jobs {analytics_jobs.shape}")
    
    # Categorize roles
    ds_jobs['role_family'] = ds_jobs['job_title'].apply(categorize_role)
    analytics_jobs['role_family'] = analytics_jobs['job_desig'].apply(categorize_role)
    
    results = {}
    
    # 1. Role demand analysis (Analytics Jobs)
    print("\n[1/6] Role demand analysis...")
    role_demand = analytics_jobs['role_family'].value_counts().to_dict()
    results['role_demand'] = role_demand
    
    fig, ax = plt.subplots(figsize=(10, 6))
    demand_df = pd.DataFrame([
        {'role': k, 'count': v} for k, v in role_demand.items()
    ]).sort_values('count', ascending=True)
    sns.barplot(data=demand_df, x='count', y='role', ax=ax, palette='viridis')
    ax.set_title('Role Demand (Number of Postings)', fontsize=14)
    ax.set_xlabel('Number of Postings')
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / 'market_role_demand.png', dpi=150)
    plt.close()
    print(f"  Saved: {FIGURES_DIR / 'market_role_demand.png'}")
    
    # 2. Salary by role (Analytics Jobs - where we have salary ranges)
    print("\n[2/6] Salary distribution by role...")
    analytics_jobs['salary_mid'] = (
        (analytics_jobs['salary_min_inr'] + analytics_jobs['salary_max_inr']) / 2
    )
    salary_by_role = analytics_jobs.groupby('role_family')['salary_mid'].agg(['mean', 'median', 'std', 'count']).to_dict('index')
    
    results['salary_by_role'] = {
        role: {
            'mean_inr': float(data['mean']),
            'median_inr': float(data['median']),
            'std_inr': float(data['std']) if pd.notna(data['std']) else None,
            'n': int(data['count'])
        }
        for role, data in salary_by_role.items()
    }
    
    fig, ax = plt.subplots(figsize=(10, 6))
    salary_df = analytics_jobs.dropna(subset=['salary_mid'])
    sns.boxplot(data=salary_df, x='salary_mid', y='role_family', ax=ax, palette='viridis')
    ax.set_title('Salary Distribution by Role (INR)', fontsize=14)
    ax.set_xlabel('Salary Midpoint (INR)')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/1e6:.1f}M'))
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / 'market_salary_dist.png', dpi=150)
    plt.close()
    print(f"  Saved: {FIGURES_DIR / 'market_salary_dist.png'}")
    
    # 3. Experience by role
    print("\n[3/6] Experience distribution by role...")
    exp_by_role = analytics_jobs.groupby('role_family')['experience_mid'].agg(['mean', 'median', 'std']).to_dict('index')
    
    results['experience_by_role'] = {
        role: {
            'mean_years': float(data['mean']),
            'median_years': float(data['median']),
            'std_years': float(data['std']) if pd.notna(data['std']) else None
        }
        for role, data in exp_by_role.items()
    }
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=analytics_jobs, x='experience_mid', y='role_family', ax=ax, palette='viridis')
    ax.set_title('Experience Distribution by Role (Years)', fontsize=14)
    ax.set_xlabel('Experience Midpoint (Years)')
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / 'market_experience.png', dpi=150)
    plt.close()
    print(f"  Saved: {FIGURES_DIR / 'market_experience.png'}")
    
    # 4. Geographic analysis
    print("\n[4/6] Geographic distribution...")
    locations = analytics_jobs['location'].dropna().str.split(',').explode().str.strip()
    top_locations = locations.value_counts().head(10).to_dict()
    results['top_locations'] = top_locations
    
    fig, ax = plt.subplots(figsize=(10, 6))
    loc_df = pd.DataFrame([
        {'location': k, 'count': v} for k, v in top_locations.items()
    ]).sort_values('count', ascending=True)
    sns.barplot(data=loc_df, x='count', y='location', ax=ax, palette='viridis')
    ax.set_title('Top 10 Job Locations', fontsize=14)
    ax.set_xlabel('Number of Postings')
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / 'market_geography.png', dpi=150)
    plt.close()
    print(f"  Saved: {FIGURES_DIR / 'market_geography.png'}")
    
    # 5. Career Opportunity Frontier
    print("\n[5/6] Career Opportunity Frontier...")
    cof_data = analytics_jobs.groupby('role_family').agg({
        's_no': 'count',
        'salary_mid': 'mean',
        'experience_mid': 'mean'
    }).reset_index()
    cof_data.columns = ['role_family', 'demand', 'avg_salary', 'avg_experience']
    cof_data = cof_data[cof_data['demand'] >= 10]  # Filter small roles
    
    results['career_frontier'] = cof_data.to_dict('records')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    scatter = sns.scatterplot(
        data=cof_data, x='demand', y='avg_salary', 
        size='avg_experience', hue='role_family',
        sizes=(100, 1000), alpha=0.7, palette='viridis', ax=ax
    )
    ax.set_title('Career Opportunity Frontier', fontsize=14)
    ax.set_xlabel('Demand (Number of Openings)')
    ax.set_ylabel('Average Salary (INR)')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/1e6:.1f}M'))
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / 'career_opportunity_frontier.png', dpi=150)
    plt.close()
    print(f"  Saved: {FIGURES_DIR / 'career_opportunity_frontier.png'}")
    
    # 6. Role-Salary matrix (heatmap)
    print("\n[6/6] Role-Experience-Salary matrix...")
    analytics_jobs['exp_bucket'] = pd.cut(
        analytics_jobs['experience_mid'], 
        bins=[0, 2, 5, 8, 12, 20, 50],
        labels=['0-2', '3-5', '6-8', '9-12', '12-20', '20+']
    )
    role_salary_matrix = analytics_jobs.pivot_table(
        values='salary_mid', 
        index='role_family', 
        columns='exp_bucket', 
        aggfunc='mean'
    )
    
    results['role_salary_matrix'] = role_salary_matrix.to_dict()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(
        role_salary_matrix / 1e6,  # Convert to millions
        annot=True, fmt='.1f', cmap='YlGnBu',
        ax=ax, cbar_kws={'label': 'Average Salary (₹M)'}
    )
    ax.set_title('Average Salary by Role and Experience', fontsize=14)
    ax.set_xlabel('Experience Bucket (Years)')
    ax.set_ylabel('Role Family')
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / 'role_salary_matrix.png', dpi=150)
    plt.close()
    print(f"  Saved: {FIGURES_DIR / 'role_salary_matrix.png'}")
    
    # Save results
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    with open(EVIDENCE_DIR / 'market_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {EVIDENCE_DIR / 'market_analysis.json'}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("MARKET SUMMARY")
    print("=" * 60)
    print("\nRole Demand:")
    for role, count in sorted(role_demand.items(), key=lambda x: x[1], reverse=True):
        print(f"  {role:20s}: {count:5d} postings")
    
    print("\nAverage Salary by Role:")
    for role in sorted(salary_by_role.keys()):
        data = salary_by_role[role]
        print(f"  {role:20s}: ₹{data['mean']/1e6:5.2f}M (n={data['count']})")
    
    return results

if __name__ == "__main__":
    analyze_market()
