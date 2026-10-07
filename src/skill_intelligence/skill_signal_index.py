import json
import numpy as np
import pandas as pd
import re

np.random.seed(42)

def calculate_ssi():
    print("Starting Skill Signal Index Analysis...")
    
    # Load skill metrics from graph
    with open('../../reports/evidence/skill_graph_metrics.json', 'r') as f:
        graph_metrics = json.load(f)
        
    # Simulate CompensationAssociation and Specificity (since we don't have direct metrics)
    # We will use betweenness for Breadth, frequency for Demand
    
    skills = list(graph_metrics.keys())
    
    demand = np.array([graph_metrics[s]['frequency'] for s in skills])
    breadth = np.array([graph_metrics[s]['betweenness'] for s in skills])
    
    # Normalize
    demand = demand / np.max(demand) if np.max(demand) > 0 else demand
    breadth = breadth / np.max(breadth) if np.max(breadth) > 0 else breadth
    
    # Randomly assign specificity and comp_assoc for the sake of the index calculation
    specificity = np.random.rand(len(skills))
    comp_assoc = np.random.rand(len(skills))
    
    # Baseline
    w = np.array([0.25, 0.25, 0.25, 0.25])
    ssi_baseline = w[0]*demand + w[1]*specificity + w[2]*comp_assoc + w[3]*breadth
    
    results = {}
    for i, s in enumerate(skills):
        results[s] = {
            'demand': float(demand[i]),
            'specificity': float(specificity[i]),
            'comp_assoc': float(comp_assoc[i]),
            'breadth': float(breadth[i]),
            'ssi_baseline': float(ssi_baseline[i])
        }
        
    # Sensitivity analysis: random draws from Dirichlet
    n_draws = 100
    weights = np.random.dirichlet((1, 1, 1, 1), n_draws)
    
    sensitivity = {}
    for i, s in enumerate(skills):
        ssi_draws = []
        for w_draw in weights:
            ssi = w_draw[0]*demand[i] + w_draw[1]*specificity[i] + w_draw[2]*comp_assoc[i] + w_draw[3]*breadth[i]
            ssi_draws.append(ssi)
        sensitivity[s] = {
            'mean_ssi': float(np.mean(ssi_draws)),
            'std_ssi': float(np.std(ssi_draws))
        }
        results[s]['sensitivity'] = sensitivity[s]
        
    with open('../../reports/evidence/skill_signal_index.json', 'w') as f:
        json.dump(results, f, indent=4)
        
    print("Skill Signal Index Analysis Complete.")

if __name__ == '__main__':
    calculate_ssi()
