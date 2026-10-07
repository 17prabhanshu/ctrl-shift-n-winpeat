import json
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def build_knowledge_graph():
    print("Starting Knowledge Graph construction...")
    
    # Load analysis results
    with open('../../reports/evidence/market_analysis.json', 'r') as f:
        market = json.load(f)
        
    with open('../../reports/evidence/skill_analysis.json', 'r') as f:
        skills = json.load(f)
        
    G = nx.DiGraph()
    
    # Add nodes and edges
    # ROLES
    for role, count in market['role_demand'].items():
        G.add_node(role, type='ROLE', demand=count)
        
        salary = market['salary_by_role'].get(role)
        if salary:
            G.add_node(f"Salary_{role}", type='SALARY', value=salary)
            G.add_edge(role, f"Salary_{role}", rel='HAS_SALARY', source='observed')
            
        exp = market['experience_by_role'].get(role)
        if exp:
            G.add_node(f"Exp_{role}", type='EXPERIENCE', value=exp)
            G.add_edge(role, f"Exp_{role}", rel='REQUIRES_EXPERIENCE', source='observed')
            
        # SKILLS
        role_skills = skills['role_skill_associations'].get(role, {})
        for skill, freq in role_skills.items():
            G.add_node(skill, type='SKILL')
            G.add_edge(role, skill, rel='REQUIRES_SKILL', weight=freq, source='observed')
            
    # Serialize for JSON
    nodes_data = [{'id': n, **d} for n, d in G.nodes(data=True)]
    edges_data = [{'source': u, 'target': v, **d} for u, v, d in G.edges(data=True)]
    
    kg_data = {
        'nodes': nodes_data,
        'edges': edges_data
    }
    
    with open('../../reports/evidence/knowledge_graph.json', 'w') as f:
        json.dump(kg_data, f, indent=4)
        
    # Visualization (simplified, top connected components)
    plt.figure(figsize=(12, 8))
    # Filter nodes for visualization to keep it readable (Roles + top skills)
    roles = [n for n, d in G.nodes(data=True) if d.get('type') == 'ROLE']
    viz_nodes = roles.copy()
    for r in roles:
        edges = sorted([(u, v, d) for u, v, d in G.out_edges(r, data=True) if G.nodes[v].get('type') == 'SKILL'], key=lambda x: x[2].get('weight', 0), reverse=True)[:3]
        for e in edges:
            viz_nodes.append(e[1])
            
    H = G.subgraph(viz_nodes)
    pos = nx.spring_layout(H, seed=42)
    
    node_colors = []
    for n in H.nodes():
        if G.nodes[n].get('type') == 'ROLE':
            node_colors.append('lightblue')
        else:
            node_colors.append('lightgreen')
            
    nx.draw(H, pos, with_labels=True, node_color=node_colors, node_size=1500, font_size=8, font_weight='bold', arrows=True)
    plt.title('Knowledge Graph Extract (Roles and Top Skills)')
    plt.tight_layout()
    plt.savefig('../../reports/figures/knowledge_graph.png')
    plt.close()
    
    print("Knowledge Graph construction Complete.")

if __name__ == '__main__':
    build_knowledge_graph()
