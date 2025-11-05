import dash
from dashboards import TopicModelDashboard

from app import dm

dash.register_page(__name__, path="/topic_model", title='Orthosphere Topic Model')
t = TopicModelDashboard(data_manager=dm)
layout = t.layout

app = dash.get_app()
# Register callbacks *after* layout is defined
def register_callbacks(app):
    t.register_callbacks(app)