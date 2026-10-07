import pandas as pd
import networkx as nx
import json
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import itertools
from networkx.algorithms.community import greedy_modularity_communities

def clean_skill(skill):
    return re.sub(r'[^a-z0-9\s]', '', str(skill).lower().strip()).strip()

def build_graph():
    print("Starting Skill Graph Analysis...")
    analytics_jobs = pd.read_csv('../../data/processed/analytics_jobs_clean.csv')
    
    cooccurrences = {}
    skill_counts = {}
    
    for idx, row in analytics_jobs.iterrows():
        skills_str = str(row['key_skills'])
        if pd.isna(skills_str) or skills_str == 'nan':
            continue
            
        raw_skills = re.split(r'[,|]', skills_str)
        job_skills = set([clean_skill(s) for s in raw_skills if clean_skill(s)])
        
        for s in job_skills:
            skill_counts[s] = skill_counts.get(s, 0) + 1
            
        for s1, s2 in itertools.combinations(sorted(list(job_skills)), 2):
            pair = (s1, s2)
            cooccurrences[pair] = cooccurrences.get(pair, 0) + 1
            
    # Filter to top skills to keep graph manageable
    top_skills = set([s for s, c in sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:100]])
    
    G = nx.Graph()
    for s in top_skills:
        G.add_node(s, count=skill_counts[s])
        
    for (s1, s2), weight in cooccurrences.items():
        if s1 in top_skills and s2 in top_skills:
            G.add_edge(s1, s2, weight=weight)
            
    # Metrics
    weighted_degree = dict(G.degree(weight='weight'))
    betweenness = nx.betweenness_centrality(G, weight='weight')
    pagerank = nx.pagerank(G, weight='weight')
    
    # Community detection
    communities = list(greedy_modularity_communities(G))
    community_map = {}
    for i, comm in enumerate(communities):
        for node in comm:
            community_map[node] = i
            
    metrics = {}
    for node in G.nodes():
        metrics[node] = {
            'frequency': skill_counts[node],
            'weighted_degree': weighted_degree[node],
            'betweenness': betweenness[node],
            'pagerank': pagerank[node],
            'community': community_map.get(node, -1)
        }
        
    with open('../../reports/evidence/skill_graph_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
        
    # Visualization
    plt.figure(figsize=(15, 15))
    pos = nx.spring_layout(G, k=0.15, iterations=20, seed=42)
    node_sizes = [skill_counts[n] * 10 for n in G.nodes()]
    node_colors = [community_map.get(n, 0) for n in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, cmap=plt.cm.tab20, alpha=0.7)
    nx.draw_networkx_edges(G, pos, alpha=0.1)
    
    # Add labels only for top 30 skills to avoid clutter
    top_30_nodes = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:30]
    labels = {n: n for n, _ in top_30_nodes if n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_weight='bold')
    
    plt.title('Skill Co-occurrence Graph (Top 100 Skills)')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('../../reports/figures/skill_cooccurrence_graph.png')
    plt.close()
    
    print("Skill Graph Analysis Complete.")

if __name__ == '__main__':
    build_graph()
