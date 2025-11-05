from dash import Dash, html, dcc, Input, Output, State, callback_context
import dash
import plotly.express as px
from data_manager import DataManager

import pandas as pd

import plotly.io as pio

pio.templates["orthosphere"] = pio.templates["plotly_white"]

pio.templates["orthosphere"].layout.update(
    font=dict(family="Garamond, Ysabeau, serif", size=16, color="#222"),
    title=dict(font=dict(family="Ysabeau, sans-serif", size=22, color="#111")),
    paper_bgcolor="#ffffee",
    plot_bgcolor="#ffffee",
    margin=dict(l=50, r=30, t=60, b=50),
    xaxis=dict(
        showgrid=True,
        gridcolor="#ffffee",
        zeroline=False,
        linecolor="#ccc",
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#ffffee",
        zeroline=False,
        linecolor="#ccc",
        tickfont=dict(size=14)
    ),
)

pio.templates.default = "orthosphere"

    
dm = DataManager('.data/')
dm._load_topic_model()
dm._load_umap_embeddings()   

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.Header([
    html.H1([
        dcc.Link("The Orthosphere Dashboard", href="/", className="site-title-link")
    ], className="site-title"),
    html.Nav([
        dcc.Link("Home", href="/"),
        dcc.Link("Topic Model", href="/topic_model"),
        dcc.Link("Vector Query", href="/query"),
    ], className="navbar")
], className="site-header"),
    html.Hr(),
    dash.page_container
])

# Register callbacks for all pages
from pages import topic_model, query

topic_model.register_callbacks(app)
query.register_callbacks(app)

server = app.server

if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0', port = 8050)
    
