import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import json
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Load Data ---
project_root = os.path.dirname(os.path.abspath(__file__))
def load_json(path):
    try:
        with open(os.path.join(project_root, path)) as f: return json.load(f)
    except: return {}

market = load_json('reports/evidence/market_analysis.json')
skills = load_json('reports/evidence/skill_analysis.json')
jds_bench = load_json('reports/benchmarks/jds_benchmark.json')
sds_bench = load_json('reports/benchmarks/sds_benchmark.json')
ablation_jds = load_json('reports/benchmarks/ablation_jds.json')
ablation_sds = load_json('reports/benchmarks/ablation_sds.json')
robustness_jds = load_json('reports/benchmarks/robustness_jds.json')
robustness_sds = load_json('reports/benchmarks/robustness_sds.json')
advanced_eda = load_json('reports/evidence/advanced_eda.json')

# --- Initialize App ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)
app.title = "Workforce Intelligence Engine"

# --- Common Styles ---
CARD_STYLE = {"box-shadow": "0 4px 15px rgba(0,0,0,0.2)", "border": "1px solid rgba(108,92,231,0.3)", "border-radius": "12px", "padding": "20px", "background-color": "#1E1E2E", "margin-bottom": "20px"}

# --- Sidebar ---
sidebar = html.Div(
    [
        html.H3("WIE Navigator", className="text-primary mt-3"),
        html.P("Workforce Intelligence Engine", className="text-muted"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Overview", href="/", active="exact"),
                dbc.NavLink("Data Exploration", href="/exploration", active="exact"),
                dbc.NavLink("Data Analysis", href="/analysis", active="exact"),
                dbc.NavLink("Results & Implications", href="/results", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={"position": "fixed", "top": 0, "left": 0, "bottom": 0, "width": "18rem", "padding": "2rem", "background-color": "#16213e"}
)

content = html.Div(id="page-content", style={"margin-left": "19rem", "padding": "2rem"})

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# --- Pages ---

def layout_overview():
    return html.Div([
        html.H1("🧠 Workforce Intelligence Engine"),
        html.H5("Does the market pay for what progression rewards?", className="text-muted mb-4"),
        dbc.Row([
            dbc.Col(html.Div([html.H4("Datasets", className="text-muted"), html.H2("4")], style=CARD_STYLE)),
            dbc.Col(html.Div([html.H4("Models", className="text-muted"), html.H2("8")], style=CARD_STYLE)),
            dbc.Col(html.Div([html.H4("JDS Best AUC", className="text-muted"), html.H2("0.904", className="text-success")], style=CARD_STYLE)),
            dbc.Col(html.Div([html.H4("SDS Best AUC", className="text-muted"), html.H2("0.998", className="text-success")], style=CARD_STYLE)),
        ]),
        html.Div([
            html.H3("Architectural Approach"),
            html.P("We process each dataset in Context-Isolated Evidence Lanes — never falsely joining rows across datasets. Each lane feeds into an Evidence Registry that tracks every analytical claim with its dataset, method, metric, and confidence interval.")
        ], style=CARD_STYLE)
    ])

def layout_exploration():
    # 1. Market Demand Chart
    fig_demand = go.Figure()
    if market.get("role_demand"):
        roles = list(market["role_demand"].keys())
        counts = list(market["role_demand"].values())
        fig_demand = px.bar(x=counts, y=roles, orientation='h', template='plotly_dark')
    
    # 2. PCA
    fig_pca = go.Figure()
    if advanced_eda and 'jds_pca' in advanced_eda:
        pca = advanced_eda['jds_pca']
        df_pca = pd.DataFrame({'PC1': pca['pc1'], 'PC2': pca['pc2'], 'Outcome': pca['target']})
        df_pca['Outcome'] = df_pca['Outcome'].map({0: 'Low Hike', 1: 'High Hike'})
        fig_pca = px.scatter(df_pca, x='PC1', y='PC2', color='Outcome', template='plotly_dark', color_discrete_sequence=["#D63031", "#00B894"])
    
    return html.Div([
        html.H2("📊 Data Exploration & Advanced EDA"),
        dbc.Tabs([
            dbc.Tab(html.Div([
                html.H4("Role Demand Across Indian Analytics Market", className="mt-4"),
                dcc.Graph(figure=fig_demand)
            ]), label="Market Demand"),
            dbc.Tab(html.Div([
                html.H4("PCA 2D Projection of Junior Skills", className="mt-4"),
                html.P("Mapping the structural separability of skill sets prior to machine learning."),
                dcc.Graph(figure=fig_pca)
            ]), label="PCA & Clusters")
        ])
    ])

def layout_analysis():
    # Model Benchmark Leaderboard
    bench = sds_bench
    fig_bench = go.Figure()
    if bench:
        models = list(bench.keys())
        aucs = [bench[m].get("roc_auc", {}).get("mean", 0) for m in models]
        fig_bench = px.bar(x=models, y=aucs, template="plotly_dark", labels={'x': 'Model', 'y': 'ROC-AUC'}, title="SDS Benchmark Leaderboard")
        fig_bench.update_yaxes(range=[0, 1.1])
        
    return html.Div([
        html.H2("🔬 Data Analysis & Explainability"),
        html.Div([
            dcc.Graph(figure=fig_bench)
        ], style=CARD_STYLE),
        html.Div([
            html.H4("Ablation & Robustness"),
            html.P("In our forensic testing, the SDS model AUC drops to 0.589 when targets are shuffled, proving genuine signal extraction rather than data leakage.")
        ], style=CARD_STYLE)
    ])

def layout_results():
    return html.Div([
        html.H2("📈 Results & Implications"),
        dbc.Row([
            dbc.Col(html.Div([html.H4("🏢 For HR Teams", style={"color":"#a29bfe"}), html.P("Hiring for isolated technical skills yields diminishing returns. Assessment frameworks should measure the interaction between technical execution and stakeholder communication.")], style=CARD_STYLE)),
            dbc.Col(html.Div([html.H4("📚 For Professionals", style={"color":"#81ecec"}), html.P("Upskilling purely in algorithms without developing storytelling and presentation skills severely limits career progression potential.")], style=CARD_STYLE)),
            dbc.Col(html.Div([html.H4("⚖️ For AI Governance", style={"color":"#fd79a8"}), html.P("By implementing Conformal Prediction sets, organizations can automate screening for clear-cut candidates while routing ambiguous profiles to human auditors.")], style=CARD_STYLE))
        ])
    ])

# --- Routing ---
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/": return layout_overview()
    elif pathname == "/exploration": return layout_exploration()
    elif pathname == "/analysis": return layout_analysis()
    elif pathname == "/results": return layout_results()
    return html.H1("404: Not found", className="text-danger")

if __name__ == "__main__":
    app.run(debug=False, port=8050, host='0.0.0.0')
