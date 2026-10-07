import pandas as pd
import json
import re

TAXONOMY = {
    'big_data': ['hadoop', 'spark', 'hive', 'kafka', 'data warehousing', 'big data'],
    'maths_statistics': ['statistics', 'regression', 'probability', 'forecasting'],
    'coding': ['python', 'java', 'scala', 'c++', 'r', 'sql'],
    'ai_ml': ['machine learning', 'deep learning', 'nlp', 'tensorflow', 'pytorch'],
    'dashboard_storytelling': ['tableau', 'power bi', 'data visualization', 'reporting']
}

def clean_skill(skill):
    return re.sub(r'[^a-z0-9\s]', '', str(skill).lower().strip()).strip()

def map_taxonomy(skill):
    for dim, keywords in TAXONOMY.items():
        if any(k in skill for k in keywords):
            return dim
    return 'unmapped'

def process_skills():
    print("Starting Skill Engine...")
    analytics_jobs = pd.read_csv('../../data/processed/analytics_jobs_clean.csv')
    
    # Categorize roles to match market analysis
    def categorize_role(title):
        title = str(title).lower()
        if 'data scientist' in title or 'data science' in title: return 'Data Scientist'
        if 'data engineer' in title or 'big data' in title or 'etl' in title: return 'Data Engineer'
        if 'machine learning' in title or 'ml' in title or 'ai' in title: return 'ML Engineer'
        if 'business analyst' in title or 'ba' in title: return 'Business Analyst'
        if 'data analyst' in title or 'reporting' in title: return 'Data Analyst'
        if 'software' in title or 'developer' in title: return 'Software Engineer'
        return 'Other'
    
    analytics_jobs['role_family'] = analytics_jobs['job_desig'].apply(categorize_role)
    
    skill_records = []
    skill_freq = {}
    role_skill_freq = {}
    
    for idx, row in analytics_jobs.iterrows():
        skills_str = str(row['key_skills'])
        if pd.isna(skills_str) or skills_str == 'nan':
            continue
            
        raw_skills = re.split(r'[,|]', skills_str)
        role = row['role_family']
        
        if role not in role_skill_freq:
            role_skill_freq[role] = {}
            
        for rs in raw_skills:
            if not rs.strip(): continue
            cleaned = clean_skill(rs)
            if not cleaned: continue
            
            canonical = cleaned  # Simple identity mapping for canonical in this iteration
            dim = map_taxonomy(canonical)
            
            skill_records.append({
                'original_skill': rs.strip(),
                'normalized_skill': cleaned,
                'canonical_skill': canonical,
                'dimension': dim,
                'confidence': 1.0 if dim != 'unmapped' else 0.5
            })
            
            skill_freq[canonical] = skill_freq.get(canonical, 0) + 1
            role_skill_freq[role][canonical] = role_skill_freq[role].get(canonical, 0) + 1
            
    # Remove duplicates from skill_records for output mapping
    unique_skills = {d['canonical_skill']: d for d in skill_records}.values()
    
    results = {
        'skill_frequencies': dict(sorted(skill_freq.items(), key=lambda item: item[1], reverse=True)[:100]),
        'role_skill_associations': {r: dict(sorted(s.items(), key=lambda i: i[1], reverse=True)[:20]) for r, s in role_skill_freq.items()},
        'mapped_skills': list(unique_skills)[:100]  # sample of 100
    }
    
    with open('../../reports/evidence/skill_analysis.json', 'w') as f:
        json.dump(results, f, indent=4)
        
    print("Skill Engine Complete.")

if __name__ == '__main__':
    process_skills()
