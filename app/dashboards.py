from dash import Dash, html, dcc, Input, Output, State, callback_context
import plotly.express as px
# from bertopic import BERTopic

import pandas as pd


class BaseDashboard:
    """Base class for building Plotly Dash dashboards."""

    def __init__(self, title="Plotly Dashboard"):
        self.title = title
        # self.app = Dash(__name__, title=self.title)
        self.layout = None

    def create_layout(self):
        """Subclasses implement to return full Dash layout."""
        raise NotImplementedError("Subclasses must implement `create_layout`.")

    def run(self, **kwargs):
        """Run the Dash app."""
        self.app.layout = self.layout or self.create_layout()
        self._register_callbacks()
        self.app.run(**kwargs)

    def register_callbacks(self, app):
        """Optional: override this in subclasses if needed."""
        pass



class VectorQueryDashboard(BaseDashboard):
    """Dashboard for querying a vector data model and visualizing similar documents."""

    def __init__(self, vector_model, title="Vector Query Dashboard"):
        self.vector_model = vector_model
        super().__init__(title)
        self.layout = self.create_layout()

    def create_layout(self):
        """Define the layout for the dashboard."""
        return html.Div([
            # dcc.Store(id="query-store"),
            html.H2(self.title),
            
            html.Div([
                html.H3("Instructions"),
            
                html.P('''
                    The below dashboards allows you to query the Orthosphere through embedding similarity. 
                    Simply enter a text to query (it can be a keyword, a question, or a sentence from the dataset), 
                    select the amoutn fo results you would like retrieved, and click "Run Query".
                    
                
                    
                '''),
                
                html.P('The results will be visualized in two plots:'),
                html.Ul([
                    html.Li("A timeline plot showing the proportion of documents mentioning the query over time, broken down by author."),
                    html.Li("A UMAP projection of the retrieved documents, allowing you to explore their distribution in embedding space. You can select points in the UMAP plot to see details of the corresponding documents below the plots."),
                    html.Li('A list of documents selected through the UMAP plot.'),
                    html.Li('A list of the top N retrieved documents, sorted by similarity to the query.')
                ]),
                html.P('You can select points in the UMAP plot to see details of the corresponding documents below the plots.'),
                
            ]),
            
            

            html.Div([
                dcc.Input(
                    id="query-text",
                    type="text",
                    placeholder="Enter query text...",
                    style={"width": "50%", "marginRight": "10px"}
                ),
                dcc.Dropdown(
                    id="num-results",
                    options=[{"label": f"top {x}", "value": x} for x in [10, 25, 50, 100, 500, 1000]],
                    value=100,
                    clearable=False,
                    style={"width": "120px", "display": "inline-block", "marginRight": "10px"}
                ),
                html.Button("Run Query", id="run-query", n_clicks=0, style={"backgroundColor": "#0074D9", "color": "white"}),
            ], style={"marginBottom": "20px", 'display' : 'flex', 'alignItems': 'center'}),

            html.Div([
                dcc.Graph(id="timeline-plot", style={"flex": "2", "marginRight": "10px"}),
                dcc.Graph(id="umap-plot", style={"flex": "1"}),
            ], style={
                "display": "flex",
                "flexDirection": "row",
                "gap": "20px",
                "alignItems": "stretch",
                 "marginTop": "100px"
            }),

            html.Div(id="selected-results", style={"marginTop": "20px"}),

            html.Div(id="results-list", style={"marginTop": "20px"})
        ], style={"margin": "40px"})

    def register_callbacks(self, app):
        """Register Dash callbacks for interactivity."""

        @app.callback(
            [
                Output("timeline-plot", "figure"),
                Output("umap-plot", "figure"),
                Output("results-list", "children")
            ],
            [Input("run-query", "n_clicks")],
            [State("query-text", "value"), State("num-results", "value")]
        )
        def update_dashboard(n_clicks, query_text, n_results):
            """Run query and update all visualizations."""
            if not n_clicks or not query_text:
                # Empty default state
                empty_fig = px.scatter()
                return empty_fig, empty_fig, html.P("Enter a query and click 'Run Query'.")

            # Query the vector model
            q = self.vector_model.query(query_text, n_results)
            # df = pd.DataFrame(results)
            
            grouper = ['year', 'name']
            
            q_ids = q.chunkID.values.tolist()
            q_ilocs = q.index.values.tolist()
            
            
            
            all_articles = self.vector_model.flat_data.groupby(grouper, as_index=True).date.count()
            qg = q.groupby(grouper, as_index=True).distance.count()
            df = (qg/all_articles).reset_index().fillna(0).rename(columns={0:'mention_proportion'})
            

            # --- Timeline Plot ---
            timeline_fig = px.line(
                df,
                x="year",
                y='mention_proportion',
                hover_data=['name', 'mention_proportion'],
                color="name",
                title="Mentions Over Time"
            )
            timeline_fig.update_layout(height=400, width=1200, margin=dict(l=10, r=10, t=50, b=10))
            
            

            # --- UMAP Plot ---
            umap_embeds = self.vector_model.umap_embeddings[q_ilocs]
            umap_data = self.vector_model.flat_data.iloc[q_ilocs]
            umap_data = pd.concat(
                [
                    umap_data.reset_index(drop=True),
                    pd.DataFrame(umap_embeds, columns=['x', 'y'])
                ],
                axis=1
            )
            
            # display(umap_data.head())
            
            # print(umap_data.columns)
            
            umap_fig = px.scatter(
                umap_data,
                x="x",
                y="y",
                hover_data=["name", "title", 'year', 'month'],
                color="name",
                title="UMAP Projection",
                custom_data=['chunkID']
            )
            umap_fig.update_layout(height=400, margin=dict(l=10, r=10, t=50, b=10))
            
            results = q.sort_values(by="distance").to_dict(orient="records")

            # --- Results List ---
            results_children = [
                html.H3(f"Top {n_results} Results"),
                html.Ul([
                    html.Li([
                        html.B(f'{r["title"]} (by {r["name"]}; distance {r["distance"]: .2f}): '),
                        html.Span(r["content"])
                    ]) for r in results
                ])
            ]

            return timeline_fig, umap_fig, results_children
        
        @app.callback(
            Output("selected-results", "children"),
            Input("umap-plot", "selectedData"),
            
        )
        def filter_texts(selectedData):
            if selectedData is None:
                return html.P("Select points in the UMAP plot to see details here.")
            
            # print(selectedData)
            
            indices = [p['customdata'][0] for p in selectedData['points']]
            # print(indices)
            
            df = self.vector_model.flat_data
            df = df[df['chunkID'].isin(indices)]
            
            
            
            return [
                html.H3(f"Selected {len(indices)} Results"),
                html.Ul([
                    html.Li([
                        html.B(f'{i["title"]} (by {i["name"]} on {i["date"].strftime("%d.%m.%Y")}): '),
                        html.Span(i["content"])
                    ]) for i in df.to_dict(orient="records")
                ])
            ]



class TopicModelDashboard(BaseDashboard):
    def __init__(self, data_manager, title="Topic Model Dashboard"):
        self.data_manager = data_manager
        super().__init__(title)
        self.layout = self.create_layout()

    def create_layout(self):    
        """Define the layout for the dashboard."""
        
        topic_model = self.data_manager.topic_model
        topics_over_time = self.data_manager.topics_over_time
        
        fig1 = topic_model.visualize_topics()
        fig2 = topic_model.visualize_barchart()
        fig3 = topic_model.visualize_topics_over_time(topics_over_time, topics=[range(5)])
        text = html.Div([])
        
        for fig in [fig1, fig2, fig3]:
        
            fig.update_layout(
                paper_bgcolor="#ffffee",
                plot_bgcolor="#ffffee",
                font=dict(family="Garamond, serif", color="#222")
            )

        
        for trace in fig1.data:
            if hasattr(trace, 'customdata') and trace.customdata is not None:
                continue
            trace.customdata = list(range(len(trace.x)))
        
        layout = html.Div([
            html.H1("Orthosphere Topic Analysis Dashboard", style={"textAlign": "center"}),
            
            html.H2('Topic Overview', style={"textAlign": "center"}),
            html.Div([
                
                dcc.Graph(figure=fig1, id='graph'),
                dcc.Graph(figure=fig2, id='bars')
            ], style={"display": "flex",
                "justifyContent": "center",   # center horizontally
                "gap": "20px",
                "marginBottom": "40px"}),
            
            
            html.Div([
                dcc.Graph(
                    figure=fig3, id='timeline'
                )
            ], style={"display": "flex",
                "justifyContent": "center",   # center horizontally
                "gap": "20px",
                "marginBottom": "40px"}),
            
            
            html.H2('Representative Texts', style={"textAlign": "center"}),
            html.Div([
                html.Div(text, id='text-display')
            ]),
            
        ])
        
        return layout
    
    def register_callbacks(self, app):
        """Register Dash callbacks for interactivity."""
        @app.callback(
            Output('bars', 'figure'),
            Input('graph', 'selectedData')
        )
        def update_bars(selectedData):
            # print(selectedData)
            if selectedData:
                topics = [p['pointIndex'] for p in selectedData['points']]
            else:
                topics = [0,1,2,3,4]  

            # filtered = df[df.year == int(year)]
            fig = self.data_manager.topic_model.visualize_barchart(topics)
            fig.update_layout(
                paper_bgcolor="#ffffee",
                plot_bgcolor="#ffffee",
                font=dict(family="Garamond, serif", color="#222")
            )
            return fig

        @app.callback(
            Output('timeline', 'figure'),
            Input('graph', 'selectedData')
        )
        def update_trendline(selectedData):
            # print(selectedData)
            if selectedData:
                topics = [p['pointIndex'] for p in selectedData['points']]
            else:
                topics = [0]  

            # filtered = df[df.year == int(year)]
            fig = self.data_manager.topic_model.visualize_topics_over_time(self.data_manager.topics_over_time, topics=topics)
            fig.update_layout(
                paper_bgcolor="#ffffee",
                plot_bgcolor="#ffffee",
                font=dict(family="Garamond, serif", color="#222")
            )
            return fig

        @app.callback(
            Output('text-display', 'children'),
            Input('graph', 'selectedData')
        )
        def update_texts(selectedData):
            if selectedData:
                topics = [p['pointIndex'] for p in selectedData['points']]
            else:
                topics = [0]
                
            # print(selectedData)
            # print(topics)

            text_blocks = []
            for t in topics:
                docs = self.data_manager.topic_model.get_representative_docs(t)
                if not docs:
                    continue
                text_blocks.append(
                    html.Div([
                        html.H3(f"Topic {t}"),
                        html.Div([
                            html.P(c) for c in docs
                        ])
                        
                    ],
                    style={'marginBottom': '20px'})
                )
            
            if not text_blocks:
                return [html.Div("No representative documents found.")]
            
            

            return text_blocks
        
        
        