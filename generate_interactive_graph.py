import json
import networkx as nx
from pyvis.network import Network
import os

with open('reports/evidence/knowledge_graph.json', 'r') as f:
    data = json.load(f)

net = Network(height="800px", width="100%", bgcolor="#0d1117", font_color="white", directed=True)
net.force_atlas_2based(gravity=-50, central_gravity=0.01, spring_length=100, spring_strength=0.08, damping=0.4, overlap=0)

COLORS = {
    'ROLE': '#58a6ff',
    'SKILL': '#3fb950',
    'SALARY': '#d2a8ff',
    'EXPERIENCE': '#ff7b72',
    'UNKNOWN': '#8b949e'
}

added_nodes = set()

# First pass: add explicit nodes
for node in data.get('nodes', []):
    node_id = str(node['id'])
    ntype = node.get('type', 'UNKNOWN')
    
    label = node_id.replace('_', ' ').title()
    if ntype == 'SALARY' and 'value' in node:
        label = f"₹{node['value']/100000:.1f}L"
    elif ntype == 'EXPERIENCE' and 'value' in node:
        label = f"{node['value']:.1f} Yrs"
        
    color = COLORS.get(ntype, COLORS['UNKNOWN'])
    size = 20 if ntype == 'ROLE' else 15
    
    net.add_node(node_id, label=label, color=color, size=size, title=ntype)
    added_nodes.add(node_id)

# Second pass: add missing nodes from edges
for edge in data.get('edges', []):
    src = str(edge['source'])
    tgt = str(edge['target'])
    
    if src not in added_nodes:
        net.add_node(src, label=src.title(), color=COLORS['UNKNOWN'], size=15)
        added_nodes.add(src)
    if tgt not in added_nodes:
        net.add_node(tgt, label=tgt.title(), color=COLORS['UNKNOWN'], size=15)
        added_nodes.add(tgt)
        
    net.add_edge(src, tgt, value=edge.get('weight', 1), color='#30363d')

os.makedirs('docs', exist_ok=True)
net.save_graph("docs/interactive_graph.html")
print("Generated docs/interactive_graph.html")
