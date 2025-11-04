import dash
from dashboards import VectorQueryDashboard

dash.register_page(__name__, path="/query")

# Reuse the shared data manager from app.py
from app import dm

vq = VectorQueryDashboard(vector_model=dm)
layout = vq.layout

app = dash.get_app()
# Register callbacks *after* layout is defined
def register_callbacks(app):
    vq.register_callbacks(app)