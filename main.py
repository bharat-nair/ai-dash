import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import networkx as nx
import json
import timeit

app = app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


graph = nx.Graph()
graph.add_edges_from([(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (2, 10), (4, 11), (4, 12), (13, 6), (6, 14), (8, 15), (8, 16), (8, 17), (16, 18), (17, 19), (17, 20), (17, 21), (17, 22),
                      (20, 23), (20, 24), (21, 25), (21, 26), (25, 27), (26, 28), (26, 29), (28, 29), (29, 30), (22, 31), (22, 14), (31, 32), (11, 33), (11, 34), (11, 35), (11, 36), (35, 37), (12, 38), (12, 39), (39, 40)])
cytoscape = nx.readwrite.json_graph.cytoscape_data(graph)
cytoscape_tree = cyto.Cytoscape()


def generate_graph(start, goal, search):
    path = []
    if search == 'bfs':
        path = nx.dijkstra_path(graph, start, goal)
    elif search == 'dfs':
        path = next(nx.all_simple_paths(graph, start, goal))
    stylesheet = []
    for node in range(1, 41):
        if node in path:
            stylesheet.append({
                'selector': '#{}'.format(node),
                'style': {
                    'background-color': '#FF4136',
                    'width': '25px',
                    'height': '25px',
                    'content': 'data(label)',
                    'text-halign': 'center',
                    'text-valign': 'center',
                    'color': 'white'

                }
            })
            stylesheet.append({
                'selector': 'edge #{}'.format(node),
                'style': {
                    'line-color': '#FF4136'
                    # 'background-color': '#FF4136',

                }
            })
        else:
            stylesheet.append({
                'selector': '#{}'.format(node),
                'style': {
                    'width': '25px',
                    'height': '25px',
                    'content': 'data(label)',
                    'text-halign': 'center',
                    'text-valign': 'center',
                    'color': 'white'

                }
            })

    return {'stylesheet': stylesheet, 'path': path}


def generate_spanning_tree(source, search):
    tree = nx.DiGraph()
    stylesheet = []
    if search == 'dfs':
        tree = nx.dfs_tree(graph, source)
        print(type(tree))
    elif search == 'bfs':
        tree = nx.bfs_tree(graph, source)
    for node in tree:
        stylesheet.append({
            'selector': '#{}'.format(node),
            'style': {
                'width': '25px',
                'height': '25px',
                'content': 'data(label)',
                'text-halign': 'center',
                'text-valign': 'center',
                'color': 'white'

            }
        })
    return nx.readwrite.json_graph.cytoscape_data(tree),  stylesheet


for node in cytoscape['elements']['nodes']:
    node['data']['label'] = node['data']['name']

tab1_content = dbc.Card([
    dbc.CardHeader("Path finding using BFS and DFS",),
    dbc.CardBody(
        dbc.Row(
            [dbc.Col([
                dbc.Row([
                        dbc.Col(
                            dbc.Input(type="number", min=1, max=40,
                                      step=1, placeholder="1-40", id="start", value=1),
                        ),
                        dbc.Col(
                            dbc.Input(type="number", min=1, max=40,
                                      step=1, placeholder="1-40", id="goal", value=2)
                        ),
                        dbc.Col(
                            dbc.RadioItems(
                                options=[
                                    {"label": "BFS", "value": 'bfs'},
                                    {"label": "DFS", "value": 'dfs'},

                                ],
                                value='bfs',
                                id="search",
                            ),
                        ),

                        ]),
                dbc.Row([
                        dbc.Col(id="path"),
                        # dbc.Col(

                        # ),
                        # dbc.Col()
                        ]),
                dbc.Row([
                        dbc.Col(
                            [dcc.Link("Dataset source", href="http://konect.cc/networks/hiv")]),
                        # dbc.Col(

                        # ),
                        # dbc.Col()
                        ]),
            ], lg=3), dbc.Col(
                cyto.Cytoscape(
                    id='cytoscape',
                    elements=cytoscape['elements'],
                    layout={
                        'name': 'breadthfirst',
                        'spacingFactor': 2.5,
                    },
                    style={'width': '100%', 'height': '400px'},
                    stylesheet=generate_graph(
                        1, 2, 'bfs')['stylesheet'],
                    userZoomingEnabled=False,
                    pan={'x': 400, 'y': 75},
                    # responsive=True,
                    # panningEnabled=False,
                    # minZoom=10,
                    # maxZoom=10,
                    # zoom=2,

                ), lg=9
            )]
        )
    )

])

cytoscape_tree = generate_spanning_tree(1, 'bfs')

tab2_content = dbc.Card([
    dbc.CardHeader("Spanning Tree with BFS and DFS",),
    dbc.CardBody(
        dbc.Row(
            [dbc.Col([
                dbc.Row([
                        dbc.Col(
                            dbc.Input(type="number", min=1, max=40,
                                      step=1, placeholder="1-40", id="source", value=1),
                        ),
                        dbc.Col(
                            dbc.RadioItems(
                                options=[
                                    {"label": "BFS", "value": 'bfs'},
                                    {"label": "DFS", "value": 'dfs'},

                                ],
                                value='bfs',
                                id="search_span",
                            ),
                        ),

                        ]),
                # dbc.Row([
                #         dbc.Col(id="path"),
                #         # dbc.Col(

                #         # ),
                #         # dbc.Col()
                #         ]),
                dbc.Row([
                        dbc.Col(
                            [dcc.Link("Dataset source", href="http://konect.cc/networks/hiv")]),
                        # dbc.Col(

                        # ),
                        # dbc.Col()
                        ]),
            ], lg=3), dbc.Col(
                cyto.Cytoscape(
                    id='cytoscape_2',
                    elements=generate_spanning_tree(1, 'bfs')[0]['elements'],
                    layout={
                        'name': 'breadthfirst',
                        'spacingFactor': 2.5,
                    },
                    style={'width': '100%', 'height': '600px'},

                    userZoomingEnabled=False,
                    pan={'x': 400, 'y': 100},
                    # responsive=True,
                    # panningEnabled=False,
                    # minZoom=10,
                    # maxZoom=10,
                    # zoom=2,

                ), lg=9
            )]
        )
    )

])

app.layout = dbc.Container([
    dbc.Tabs(
        [
            dbc.Tab(tab1_content, label="Path Finding"),
            dbc.Tab(tab2_content, label="Spanning Tree"),
        ]
    ),
], className="m-5")


@app.callback(
    # Output(component_id='path', component_property='children'),
    Output(component_id='cytoscape', component_property='stylesheet'),
    Output(component_id='cytoscape_2', component_property='elements'),
    Output(component_id='cytoscape_2', component_property='stylesheet'),
    Output(component_id='path', component_property='children'),
    Input(component_id='start', component_property='value'),
    Input(component_id='goal', component_property='value'),
    Input(component_id='search', component_property='value'),
    Input(component_id='search_span', component_property='value'),
    Input(component_id='source', component_property='value'),
)
def update_output_div(start, goal, search, search_span, source):
    start_time = timeit.default_timer()
    stylesheet_graph = generate_graph(
        int(start), int(goal), search)['stylesheet']
    stop_time = timeit.default_timer()

    # print('Time: ', stop - start)
    # print(source, search_span)
    # print(generate_spanning_tree(source, search_span)['elements'])
    tree,stylesheet_tree = generate_spanning_tree(source, search_span)
    print(tree,stylesheet_tree)
    return stylesheet_graph, tree['elements'],stylesheet_tree, 'Path found in {}s'.format(stop_time-start_time)
    # return [], generate_spanning_tree(source, search_span)['elements'], ''


app.run_server(debug=True)
