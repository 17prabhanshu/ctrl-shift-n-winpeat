"""
Skill Intelligence Engine - proper taxonomy mapping to 5 JDS dimensions.

FIXED from original:
- ML → ai_ml (not coding)
- SQL → coding (with sensitivity reassignment option)
- Non-technical skills (project management, sales, finance, etc.) → unmapped
- Proper confidence scores based on match quality
"""
import pandas as pd
import numpy as np
import json
import re
from collections import defaultdict
from pathlib import Path
from src.utils.config import (
    PROCESSED_DIR, REPORTS_DIR, EVIDENCE_DIR,
    categorize_role, SKILL_TAXONOMY, NON_TECHNICAL_SKILLS
)

# Canonical skill aliases - maps variants to canonical form
SKILL_ALIASES = {
    # Programming languages
    'python': ['python', 'py', 'python3', 'python 3'],
    'java': ['java', 'core java', 'j2ee', 'java ee', 'java8', 'java 8', 'java11', 'java 11'],
    'javascript': ['javascript', 'js', 'ecmascript', 'es6', 'es2015', 'ecma'],
    'typescript': ['typescript', 'ts'],
    'c++': ['c++', 'cpp', 'c plus plus'],
    'c#': ['c#', 'csharp', 'c sharp'],
    'sql': ['sql', 'sql server', 'microsoft sql', 'tsql', 'plsql', 'mysql', 'postgresql', 'pgsql'],
    'r_lang': ['r programming', 'r studio', 'rstudio', 'r lang'],  # 'r' alone is too short, will match many things
    'scala': ['scala'],
    'go': ['go', 'golang'],
    'rust': ['rust'],
    'php': ['php'],
    'ruby': ['ruby', 'ruby on rails', 'ror'],
    'swift': ['swift'],
    'kotlin': ['kotlin'],
    
    # Big data
    'hadoop': ['hadoop', 'hdfs'],
    'spark': ['spark', 'apache spark'],
    'hive': ['hive'],
    'kafka': ['kafka'],
    'hbase': ['hbase'],
    'nosql': ['nosql', 'mongodb', 'cassandra', 'couchdb', 'redis', 'dynamodb'],
    'mapreduce': ['mapreduce', 'map reduce'],
    'pig': ['pig'],
    
    # AI/ML
    'machine learning': ['machine learning', 'ml', 'mlops'],
    'deep learning': ['deep learning', 'dl'],
    'nlp': ['nlp', 'natural language processing'],
    'computer vision': ['computer vision', 'cv'],
    'tensorflow': ['tensorflow', 'tf', 'tensor flow'],
    'pytorch': ['pytorch', 'torch'],
    'keras': ['keras'],
    'neural network': ['neural network', 'neural networks', 'nn'],
    
    # Visualization
    'tableau': ['tableau'],
    'power bi': ['power bi', 'powerbi', 'power bi desktop'],
    'excel': ['excel', 'microsoft excel', 'advanced excel'],
    
    # Cloud
    'aws': ['aws', 'amazon web services', 'amazon aws'],
    'azure': ['azure', 'microsoft azure'],
    'gcp': ['gcp', 'google cloud', 'google cloud platform'],
}

def get_canonical_skill(raw_skill: str) -> tuple:
    """
    Map a raw skill string to canonical form.
    Returns (canonical_skill, confidence, matched_aliases).
    """
    raw_lower = raw_skill.lower().strip()
    raw_clean = re.sub(r'[^a-z0-9\s]', '', raw_lower).strip()
    
    # Check aliases first
    for canonical, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            # Exact match or word-boundary match
            if raw_lower == alias or raw_clean == alias:
                return canonical, 1.0, alias
            # Handle short skills carefully
            if len(alias) >= 3 and (f' {alias} ' in f' {raw_lower} ' or raw_lower.startswith(alias + ' ') or raw_lower.endswith(' ' + alias)):
                return canonical, 0.9, alias
    
    # If contains a known skill as substring (only for longer aliases)
    for canonical, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            if len(alias) >= 4 and alias in raw_clean:
                return canonical, 0.8, alias
    
    # Return as-is with low confidence
    return raw_skill.strip(), 0.5, None

def map_to_dimension(canonical_skill: str) -> tuple:
    """
    Map a canonical skill to one of 5 JDS dimensions.
    Returns (dimension, reason).
    
    Dimensions:
    0: big_data
    1: maths_statistics
    2: coding
    3: ai_ml
    4: dashboard_storytelling
    5: unmapped (non-technical or unknown)
    """
    from src.utils.config import TECHNICAL_BUT_OFTEN_MISSED
    
    canonical_lower = canonical_skill.lower().strip()
    
    # First, check explicit non-technical skills
    for non_tech in NON_TECHNICAL_SKILLS:
        if non_tech in canonical_lower:
            return 'unmapped', f'non_technical: {non_tech}'
    
    # First check SKILL_TAXONOMY (more specific mappings)
    for dim_name, dim_config in SKILL_TAXONOMY.items():
        for keyword in dim_config['keywords']:
            if keyword in canonical_lower:
                return dim_name, f'taxonomy: {keyword}'
    
    # Then check explicit non-technical skills
    for non_tech in NON_TECHNICAL_SKILLS:
        if non_tech in canonical_lower:
            return 'unmapped', f'non_technical: {non_tech}'
    
    # Check if it's a known technical skill (exact or word-boundary match)
    for skill in sorted(TECHNICAL_BUT_OFTEN_MISSED, key=len, reverse=True):  # Longer first to avoid partial matches
        # Exact match or word boundary match
        if canonical_lower == skill or f' {skill} ' in f' {canonical_lower} ' or canonical_lower.startswith(skill + ' ') or canonical_lower.endswith(' ' + skill):
            # Determine dimension based on skill
            if skill in ['sas', 'spss', 'stata', 'matlab', 'octave']:
                return 'maths_statistics', f'statistical_software: {skill}'
            elif skill in ['r', 'r programming', 'r studio', 'rstudio']:
                return 'coding', f'programming_language: {skill}'
            elif skill in ['tableau', 'power bi', 'powerbi', 'qlik', 'looker', 'looker studio', 'excel']:
                return 'dashboard_storytelling', f'bi_tool: {skill}'
            elif skill in ['mongodb', 'cassandra', 'couchdb', 'redis', 'dynamodb', 'neo4j', 
                          'snowflake', 'redshift', 'bigquery', 'databricks', 'hadoop', 'spark', 'hive',
                          'kafka', 'hdfs', 'nosql', 'hbase']:
                return 'big_data', f'data_platform: {skill}'
            else:
                return 'coding', f'programming_tech: {skill}'
    
    # Map to dimensions based on SKILL_TAXONOMY keywords
    for dim_name, dim_config in SKILL_TAXONOMY.items():
        for keyword in dim_config['keywords']:
            if keyword in canonical_lower:
                # Handle special cases
                if dim_name == 'coding' and canonical_lower == 'sql':
                    return 'coding', 'sql_in_coding (sensitivity: reassign to big_data)'
                return dim_name, f'keyword_match: {keyword}'
    
    # Handle common programming languages and tech not in taxonomy
    if canonical_lower in ['java', 'javascript', 'typescript', 'python', 'scala', 'go', 'golang', 
                           'rust', 'php', 'ruby', 'swift', 'kotlin', 'c++', 'c#', 'csharp', 
                           'dotnet', '.net', 'c', 'perl', 'lua', 'haskell', 'clojure', 'elixir',
                           'html', 'html5', 'css', 'css3', 'shell', 'bash', 'powershell',
                           'docker', 'kubernetes', 'k8s', 'jenkins', 'ansible', 'terraform',
                           'angular', 'react', 'vue', 'node', 'express', 'next.js', 'nuxt',
                           'jquery', 'ajax', 'json', 'xml', 'rest', 'soap', 'graphql',
                           'linux', 'unix', 'git', 'github', 'gitlab', 'bitbucket',
                           'android', 'ios', 'flutter', 'react native',
                           'aws', 'azure', 'gcp', 'google cloud']:
        return 'coding', 'common_tech_language'
    
    return 'unmapped', 'no_keyword_match'

def process_all_skills(analytics_df: pd.DataFrame) -> pd.DataFrame:
    """
    Process all skill strings in the Analytics Jobs dataframe.
    Returns a skill mapping dataframe with full provenance.
    """
    records = []
    
    for idx, row in analytics_df.iterrows():
        skills_str = row.get('key_skills', '')
        if pd.isna(skills_str) or str(skills_str).strip() == '':
            continue
        
        role = categorize_role(row.get('job_desig', ''))
        skills = [s.strip() for s in str(skills_str).lower().split(',') if s.strip()]
        
        for skill in skills:
            canonical, confidence, matched = get_canonical_skill(skill)
            dimension, reason = map_to_dimension(canonical)
            
            records.append({
                'row_idx': idx,
                'original_skill': skill,
                'canonical_skill': canonical,
                'dimension': dimension,
                'confidence': confidence,
                'match_method': 'alias' if matched else ('substring' if confidence >= 0.8 else 'direct'),
                'match_detail': matched,
                'role_family': role,
                'job_desig': row.get('job_desig', '')
            })
    
    return pd.DataFrame(records)

def compute_skill_statistics(skill_df: pd.DataFrame) -> dict:
    """Compute skill frequency, role associations, and dimension statistics."""
    stats = {
        'total_mappings': len(skill_df),
        'unique_canonical_skills': skill_df['canonical_skill'].nunique(),
        'dimension_distribution': skill_df['dimension'].value_counts().to_dict(),
        'confidence_distribution': skill_df['confidence'].value_counts().to_dict(),
        'top_skills': [],
        'role_skill_associations': {},
        'dimension_role_matrix': {}
    }
    
    # Top skills by frequency
    skill_counts = skill_df['canonical_skill'].value_counts().head(100)
    stats['top_skills'] = [
        {'skill': s, 'frequency': int(c), 'dimension': 
         map_to_dimension(s)[0]} 
        for s, c in skill_counts.items()
    ]
    
    # Role-skill associations
    for role in skill_df['role_family'].unique():
        role_skills = skill_df[skill_df['role_family'] == role]['canonical_skill'].value_counts().head(20)
        stats['role_skill_associations'][role] = [
            {'skill': s, 'frequency': int(c)} 
            for s, c in role_skills.items()
        ]
    
    # Dimension by role matrix
    for dim in ['big_data', 'maths_statistics', 'coding', 'ai_ml', 'dashboard_storytelling', 'unmapped']:
        dim_data = skill_df[skill_df['dimension'] == dim]
        stats['dimension_role_matrix'][dim] = {}
        for role in dim_data['role_family'].unique():
            stats['dimension_role_matrix'][dim][role] = int(len(dim_data[dim_data['role_family'] == role]))
    
    return stats

def save_skill_analysis(skill_df: pd.DataFrame, stats: dict):
    """Save skill analysis results."""
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save full skill mapping
    skill_df.to_csv(EVIDENCE_DIR / 'skill_mapping.csv', index=False)
    
    # Save statistics (top 100 skills only for JSON)
    stats_serializable = {
        'total_mappings': stats['total_mappings'],
        'unique_canonical_skills': stats['unique_canonical_skills'],
        'dimension_distribution': stats['dimension_distribution'],
        'confidence_distribution': stats['confidence_distribution'],
        'top_skills': stats['top_skills'][:100],
        'role_skill_associations': stats['role_skill_associations'],
        'dimension_role_matrix': stats['dimension_role_matrix'],
        # SQL sensitivity note
        'sql_dimension_note': 'SQL mapped to coding dimension. Sensitivity analysis reassigns SQL to big_data dimension.'
    }
    
    with open(EVIDENCE_DIR / 'skill_analysis.json', 'w') as f:
        json.dump(stats_serializable, f, indent=2)
    
    print(f"Saved skill analysis: {EVIDENCE_DIR / 'skill_analysis.json'}")
    print(f"  Total skill mentions processed: {stats['total_mappings']}")
    print(f"  Unique canonical skills: {stats['unique_canonical_skills']}")
    print(f"  Dimension distribution: {stats['dimension_distribution']}")

def run_skill_engine():
    """Run the complete skill intelligence pipeline."""
    print("=" * 60)
    print("SKILL INTELLIGENCE ENGINE")
    print("=" * 60)
    
    # Load cleaned analytics jobs
    analytics_path = PROCESSED_DIR / 'analytics_jobs_clean.csv'
    if not analytics_path.exists():
        print(f"ERROR: Cleaned analytics jobs not found at {analytics_path}")
        print("Run the cleaning pipeline first.")
        return None
    
    df = pd.read_csv(analytics_path)
    print(f"\nLoaded: {df.shape[0]} postings")
    
    # Process skills
    print("\nProcessing skills...")
    skill_df = process_all_skills(df)
    print(f"Mapped: {len(skill_df)} skill mentions")
    
    # Compute statistics
    print("\nComputing statistics...")
    stats = compute_skill_statistics(skill_df)
    
    # Save results
    print("\nSaving results...")
    save_skill_analysis(skill_df, stats)
    
    # Print dimension distribution
    print("\n" + "=" * 60)
    print("DIMENSION DISTRIBUTION")
    print("=" * 60)
    for dim, count in stats['dimension_distribution'].items():
        pct = 100 * count / stats['total_mappings']
        print(f"  {dim:25s}: {count:5d} ({pct:5.1f}%)")
    
    print("\nTop 10 skills:")
    for i, skill in enumerate(stats['top_skills'][:10], 1):
        print(f"  {i:2d}. {skill['skill']:30s} ({skill['frequency']:4d}) [{skill['dimension']}]")
    
    # SQL sensitivity note
    sql_count = skill_df[skill_df['canonical_skill'] == 'sql'].shape[0]
    print(f"\nNote: SQL appears {sql_count} times, mapped to 'coding' dimension.")
    print(f"      Sensitivity analysis reassigns SQL to 'big_data' dimension.")
    
    return skill_df

if __name__ == "__main__":
    run_skill_engine()
