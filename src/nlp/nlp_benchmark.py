import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

TAXONOMY = {
    'big_data': ['hadoop', 'spark', 'hive', 'kafka', 'data warehousing', 'big data'],
    'maths_statistics': ['statistics', 'regression', 'probability', 'forecasting'],
    'coding': ['python', 'java', 'scala', 'c++', 'r', 'sql'],
    'ai_ml': ['machine learning', 'deep learning', 'nlp', 'tensorflow', 'pytorch'],
    'dashboard_storytelling': ['tableau', 'power bi', 'data visualization', 'reporting']
}

# 50 common skills manually mapped (gold standard)
GOLD_STANDARD = {
    'python': 'coding', 'java': 'coding', 'c++': 'coding', 'sql': 'coding', 'r': 'coding',
    'scala': 'coding', 'javascript': 'unmapped', 'html': 'unmapped', 'css': 'unmapped', 'aws': 'unmapped',
    'machine learning': 'ai_ml', 'deep learning': 'ai_ml', 'nlp': 'ai_ml', 'tensorflow': 'ai_ml', 'pytorch': 'ai_ml',
    'computer vision': 'ai_ml', 'keras': 'ai_ml', 'scikit learn': 'ai_ml', 'neural networks': 'ai_ml', 'ai': 'ai_ml',
    'hadoop': 'big_data', 'spark': 'big_data', 'hive': 'big_data', 'kafka': 'big_data', 'big data': 'big_data',
    'data warehousing': 'big_data', 'etl': 'big_data', 'nosql': 'big_data', 'mongodb': 'big_data', 'cassandra': 'big_data',
    'tableau': 'dashboard_storytelling', 'power bi': 'dashboard_storytelling', 'data visualization': 'dashboard_storytelling',
    'reporting': 'dashboard_storytelling', 'qlikview': 'dashboard_storytelling', 'd3': 'dashboard_storytelling', 'looker': 'dashboard_storytelling',
    'statistics': 'maths_statistics', 'regression': 'maths_statistics', 'probability': 'maths_statistics', 'forecasting': 'maths_statistics',
    'predictive modeling': 'maths_statistics', 'ab testing': 'maths_statistics', 'optimization': 'maths_statistics',
    'excel': 'unmapped', 'agile': 'unmapped', 'scrum': 'unmapped', 'communication': 'unmapped', 'leadership': 'unmapped', 'management': 'unmapped'
}

def clean_skill(skill):
    return re.sub(r'[^a-z0-9\s]', '', str(skill).lower().strip()).strip()

def level1_exact_match(skill):
    skill = clean_skill(skill)
    for dim, keywords in TAXONOMY.items():
        if skill in keywords:
            return dim
    return 'unmapped'

def level2_tfidf_match(skills, threshold=0.3):
    corpus = []
    labels = []
    for dim, keywords in TAXONOMY.items():
        for kw in keywords:
            corpus.append(kw)
            labels.append(dim)
            
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    results = {}
    for skill in skills:
        cleaned = clean_skill(skill)
        skill_vec = vectorizer.transform([cleaned])
        sims = cosine_similarity(skill_vec, tfidf_matrix)[0]
        max_idx = np.argmax(sims)
        if sims[max_idx] >= threshold:
            results[skill] = labels[max_idx]
        else:
            results[skill] = 'unmapped'
    return results

def level3_ngram_match(skill):
    skill = clean_skill(skill)
    for dim, keywords in TAXONOMY.items():
        for kw in keywords:
            # simple substring/ngram overlap check
            if kw in skill or skill in kw:
                return dim
    return 'unmapped'

def evaluate(predictions, gold):
    correct = 0
    total = len(gold)
    for k, v in gold.items():
        if predictions.get(k) == v:
            correct += 1
    return correct / total

def run_benchmark():
    print("Starting NLP Benchmark...")
    skills = list(GOLD_STANDARD.keys())
    
    # Level 1
    preds1 = {s: level1_exact_match(s) for s in skills}
    acc1 = evaluate(preds1, GOLD_STANDARD)
    
    # Level 2
    preds2 = level2_tfidf_match(skills)
    acc2 = evaluate(preds2, GOLD_STANDARD)
    
    # Level 3
    preds3 = {s: level3_ngram_match(s) for s in skills}
    acc3 = evaluate(preds3, GOLD_STANDARD)
    
    results = {
        'level1_accuracy': acc1,
        'level2_accuracy': acc2,
        'level3_accuracy': acc3,
        'gold_standard_size': len(GOLD_STANDARD)
    }
    
    with open('../../reports/benchmarks/nlp_benchmark.json', 'w') as f:
        json.dump(results, f, indent=4)
        
    md_content = f"""# NLP Benchmark Results

## Evaluation against 50 manually mapped skills

- **Level 1 (Exact Match):** Accuracy = {acc1:.2%}
- **Level 2 (TF-IDF Similarity):** Accuracy = {acc2:.2%}
- **Level 3 (N-gram Matching):** Accuracy = {acc3:.2%}

### Observations
- Exact matching works well for taxonomy keywords but fails for variations.
- TF-IDF depends on overlap; short phrases can be tricky.
- N-gram/substring matching captures variations like 'python programming' -> 'python' but can introduce false positives.
"""
    with open('../../reports/benchmarks/nlp_benchmark.md', 'w') as f:
        f.write(md_content)
        
    print("NLP Benchmark Complete.")

if __name__ == '__main__':
    run_benchmark()
