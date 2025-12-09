import dash
from dash import html, dcc

dash.register_page(__name__, path="/", name="Home", title="The Orthosphere Dashboard")

layout = html.Div([
        html.Div(
            [
                html.H2("1 Introduction", style={"textAlign": "center"}),
                html.P("""
                    This website showcases the use of LLMs for qualitative analysis of large unstructured datasets. 
                    It does so by exploring the Orthosphere blog, which is part of my current research. 
                    The term ‘orthosphere’ (following ‘manosphere’) has also come to be used to denote 
                    the online presence of religious traditionalists.
                """),
                html.P("""
                    The blog has been active since 2012 and provides an interesting perspective 
                    on what has come to be known as the ‘alt-right’. While it does occasionally repeat 
                    some far-right talking points, it also includes a large amount of nuanced opinions 
                    and analyses of various philosophers, theologians, and musical composers.
                """),
                html.P([
                    html.B("Disclaimer: "),
                    "Note that some of the blog’s content can be sensitive. While exploring it, I have come across fair amounts of sexism, bigotry, and some lower-key racism."
                ]),
                html.P([
                    html.B("Mobile use: "),
                    "The dashboard is incompatible with mobile phones, as the plotly graphs are planned with only the desktop version in mind (reliance on select and hover tools)."
                ]),
                
                html.H2("2 Data Preparation", style={"textAlign": "center"}),

                html.P([
                    "The code for the data preparation and the app itself is available at ",
                    html.A(
                        "https://github.com/ai-tonchev/orthosphere-dashboard",
                        href="https://github.com/ai-tonchev/orthosphere-dashboard",
                        target="_blank",
                        style={"color": "#003366", "textDecoration": "underline"},
                    ),
                    "."
                ]),

                html.H3("2.1 Scraping and Modelling"),
                html.P("""
                    I developed a custom script to scrape https://orthosphere.wordpress.com/’s articles. 
                    Then, I organized the information into a relational model with tables for authors, articles, 
                    comments (currently not used in the dashboard), and paragraphs.
                """),

                html.H3("2.2 Embeddings"),
                html.P("""
                    The second step was the generation of vector embeddings (Camacho-Collados & Pilehvar, 2018) 
                    of all texts collected. I split all paragraphs larger than 500 words 
                    (the model context window is 768 tokens) and processed all documents through SBERT 
                    (all-mpnet-base-v2), which provided multidimensional numeric representations 
                    of the meaning of each document.
                """),

                html.H3("2.3 Topic Modelling"),
                html.P(["""
                    Then, I applied BERTopic on the generated embeddings, which essentially runs HDBSCAN clustering 
                    on the embeddings and then generates keywords from each cluster’s documents. Thus, even if the 
                    keywords don’t fully represent the cluster, it is likely that the cluster is built from 
                    meaningfully connected documents. The results from this analysis can be seen at the 
                """,
                    html.A("Topic Model page", href="/topic_model", style={"color": "#003366", "textDecoration": "underline"}),
                    "."
                ]),

                html.H3("2.4 Graph Analysis"),
                html.P("""
                    Using the similarity matrix of all embeddings, I built a graph that links semantically connected 
                    paragraphs. This graph can be used to explore interactions between websites, users, and texts. 
                    Importantly, using the graph’s centrality metrics, important texts and authors can be identified 
                    as starting points of analysis. On the other hand, topic model clusters can be evaluated for 
                    coherence based on graph density and connectivity within them. The graph-based dashboard 
                    will be added soon.
                """),

                html.H3("2.5 Querying"),
                html.P("""
                    Using an embedding model, a user can ‘converse’ with the dataset through vector querying, 
                    where a free-form textual query is embedded and then the top n most similar documents from 
                    the dataset are returned. Analyzing query results can also be a powerful method for better 
                    understanding the capabilities and limitations of LLMs when working with deeper layers of meaning.
                """),
                
                
                html.H2('3 Dashboards', style={"marginTop": "50px", "textAlign": "center"}),
                
                
                
                html.Ul([
                    html.Li(dcc.Link("📊 Topic Model Dashboard", href="/topic_model")),
                    html.Li(dcc.Link("🔍 Vector Query Dashboard", href="/query")),
                ]),

                html.H2("4 Bibliography", style={"marginTop": "50px", "textAlign": "center"}),

                html.Ul([
                    html.Li([
                        html.B("Camacho-Collados, J. and Pilehvar, M.T. (2018). "),
                        "“From Word To Sense Embeddings: A Survey on Vector Representations of Meaning,” ",
                        html.I("Journal of Artificial Intelligence Research, 63"),
                        ", pp. 743–788. ",
                        html.A("https://doi.org/10.1613/jair.1.11259",
                               href="https://doi.org/10.1613/jair.1.11259",
                               target="_blank",
                               style={"color": "#003366"}),
                    ]),
                    html.Li([
                        html.B("Gerbaudo, P. (2016). "),
                        "“From Data Analytics to Data Hermeneutics. Online Political Discussions, Digital Methods and the Continuing Relevance of Interpretive Approaches,” ",
                        html.I("Digital Culture & Society, 2(2)"),
                        ", pp. 95–112. ",
                        html.A("https://doi.org/10.14361/dcs-2016-0207",
                               href="https://doi.org/10.14361/dcs-2016-0207",
                               target="_blank",
                               style={"color": "#003366"}),
                    ]),
                    html.Li([
                        html.B("Kelaidis, K. (2019). "),
                        "“Orthodoxy’s Extremist Appeal,” ",
                        html.I("Orthodox Christian Laity"),
                        ". Available at: ",
                        html.A("https://ocl.org/orthodoxys-extremist-appeal/",
                               href="https://ocl.org/orthodoxys-extremist-appeal/",
                               target="_blank",
                               style={"color": "#003366"}),
                        " (Accessed: October 30, 2025)."
                    ]),
                    html.Li([
                        html.B("Mohr, J.W., Wagner-Pacifici, R. and Breiger, R.L. (2015). "),
                        "“Toward a computational hermeneutics,” ",
                        html.I("Big Data & Society, 2(2)"),
                        ", p. 2053951715613809. ",
                        html.A("https://doi.org/10.1177/2053951715613809",
                               href="https://doi.org/10.1177/2053951715613809",
                               target="_blank",
                               style={"color": "#003366"}),
                    ]),
                
                
                
            
                ],
                style={
                    "maxWidth": "800px",
                    "width": "100%",
                    "margin": "0 auto",             # centers the block itself
                    "fontFamily": "Garamond, serif",
                    "fontSize": "18px",
                    "lineHeight": "1.6",
                    "textAlign": "justify"
                },
            )
        ],
        style={
            "maxWidth": "900px",
                "margin": "0 auto",
                "padding": "50px 20px",
                "fontFamily": "Garamond, serif",
                "fontSize": "18px",
                "lineHeight": "1.6",
                # "backgroundColor": "#ffffee",
                # "borderRadius": "10px",
                # "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"
        })],
    style={
    "display": "flex",
    "justifyContent": "center",
    # "backgroundColor": "#faf7e6"
    }
        
)
