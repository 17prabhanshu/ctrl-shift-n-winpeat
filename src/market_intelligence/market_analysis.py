import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import re

def categorize_role(title):
    title = str(title).lower()
    if 'data scientist' in title or 'data science' in title:
        return 'Data Scientist'
    elif 'data engineer' in title or 'big data' in title or 'etl' in title:
        return 'Data Engineer'
    elif 'machine learning' in title or 'ml' in title or 'ai' in title:
        return 'ML Engineer'
    elif 'business analyst' in title or 'ba' in title:
        return 'Business Analyst'
    elif 'data analyst' in title or 'reporting' in title:
        return 'Data Analyst'
    elif 'software' in title or 'developer' in title:
        return 'Software Engineer'
    else:
        return 'Other'

def analyze_market():
    print("Starting Market Analysis...")
    ds_jobs = pd.read_csv('../../data/processed/ds_jobs_clean.csv')
    analytics_jobs = pd.read_csv('../../data/processed/analytics_jobs_clean.csv')
    
    # Process analytics jobs for role family
    analytics_jobs['role_family'] = analytics_jobs['job_desig'].apply(categorize_role)
    ds_jobs['role_family'] = ds_jobs['job_title'].apply(categorize_role)
    
    # 1. Role demand analysis
    role_demand = analytics_jobs['role_family'].value_counts().to_dict()
    
    plt.figure(figsize=(10,6))
    sns.countplot(data=analytics_jobs, y='role_family', order=analytics_jobs['role_family'].value_counts().index)
    plt.title('Role Demand Analysis')
    plt.tight_layout()
    plt.savefig('../../reports/figures/market_role_demand.png')
    plt.close()

    # 2. Compensation analysis (from ds_jobs where avg_salary_parsed is available or analytics_jobs where salary_min/max available)
    # Using analytics jobs since it has salary_min and salary_max
    analytics_jobs['avg_salary_lpa'] = (analytics_jobs['salary_min'] + analytics_jobs['salary_max']) / 2
    salary_by_role = analytics_jobs.groupby('role_family')['avg_salary_lpa'].mean().to_dict()
    
    plt.figure(figsize=(10,6))
    sns.boxplot(data=analytics_jobs, x='avg_salary_lpa', y='role_family')
    plt.title('Salary Distribution by Role (LPA)')
    plt.tight_layout()
    plt.savefig('../../reports/figures/market_salary_dist.png')
    plt.close()
    
    # 3. Experience analysis
    analytics_jobs['avg_exp'] = (analytics_jobs['exp_min'] + analytics_jobs['exp_max']) / 2
    exp_by_role = analytics_jobs.groupby('role_family')['avg_exp'].mean().to_dict()
    
    plt.figure(figsize=(10,6))
    sns.boxplot(data=analytics_jobs, x='avg_exp', y='role_family')
    plt.title('Experience Distribution by Role (Years)')
    plt.tight_layout()
    plt.savefig('../../reports/figures/market_experience.png')
    plt.close()

    # 4. Geographic analysis
    locations = analytics_jobs['location'].dropna().str.split(',').explode().str.strip()
    top_locations = locations.value_counts().head(10)
    
    plt.figure(figsize=(10,6))
    sns.barplot(x=top_locations.values, y=top_locations.index)
    plt.title('Top Job Locations')
    plt.tight_layout()
    plt.savefig('../../reports/figures/market_geography.png')
    plt.close()
    
    # 5. Career Opportunity Frontier
    # Bubble plot: x=demand (count), y=salary, size=experience, color=role_family
    cof_data = analytics_jobs.groupby('role_family').agg({
        's_no': 'count',
        'avg_salary_lpa': 'mean',
        'avg_exp': 'mean'
    }).reset_index()
    cof_data.rename(columns={'s_no': 'demand'}, inplace=True)
    
    plt.figure(figsize=(10,8))
    sns.scatterplot(data=cof_data, x='demand', y='avg_salary_lpa', 
                    size='avg_exp', hue='role_family', sizes=(100, 1000), alpha=0.7)
    plt.title('Career Opportunity Frontier')
    plt.xlabel('Demand (Number of Jobs)')
    plt.ylabel('Average Salary (LPA)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('../../reports/figures/career_opportunity_frontier.png')
    plt.close()

    # Role-salary matrix (heatmap of role vs experience bucket for salary)
    analytics_jobs['exp_bucket'] = pd.cut(analytics_jobs['avg_exp'], bins=[0,2,5,8,12,20], labels=['0-2', '3-5', '6-8', '9-12', '12+'])
    role_salary_matrix = analytics_jobs.pivot_table(values='avg_salary_lpa', index='role_family', columns='exp_bucket', aggfunc='mean')
    
    results = {
        'role_demand': role_demand,
        'salary_by_role': salary_by_role,
        'experience_by_role': exp_by_role,
        'top_locations': top_locations.to_dict(),
        'role_salary_matrix': role_salary_matrix.fillna(0).to_dict()
    }
    
    with open('../../reports/evidence/market_analysis.json', 'w') as f:
        json.dump(results, f, indent=4)
    print("Market Analysis Complete.")

if __name__ == '__main__':
    analyze_market()
