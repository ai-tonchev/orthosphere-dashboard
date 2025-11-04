import dash
from dash import html, dcc

dash.register_page(__name__, path="/", name="Home", title="Welcome")

layout = html.Div(
    [
        html.H1("Welcome to the Orthosphere Dashboards"),
        html.P(
            "Explore two complementary analytical dashboards:"
        ),
        html.Ul(
            [
                html.Li(dcc.Link("📊 Topic Model Dashboard", href="/topic_model")),
                html.Li(dcc.Link("🔍 Vector Query Dashboard", href="/query")),
            ]
        ),
        html.Br(),
        html.P("Use the navigation bar or links above to explore the data."),
    ],
    style={
        "margin": "50px",
        "maxWidth": "800px",
        "fontFamily": "Garamond, serif",
        "fontSize": "18px",
        "lineHeight": "1.6",
    },
)
