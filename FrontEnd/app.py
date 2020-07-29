import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt

import dash_leaflet as dl
from dash_leaflet import express as dlx
import json

from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import os
import glob
import flask
import pandas as pd
#import seaborn as sns


data_path = '../data/matrix/matrix_consol_v2.zip'
basins_map_path = '../data/shapes/Macro_Cuencas.json'

#################  DEFINE THE DASH APP  ####################
app = dash.Dash(external_stylesheets=[dbc.themes.MATERIA])
# image_directory =  os.getcwd() + '/img/'
# list_of_images = [os.path.basename(x) for x in glob.glob('{}*.*'.format(image_directory))]
# static_image_route = '/static/'

# Add a static image route that serves images from local directory
# @app.server.route('{}<image_path>'.format(static_image_route))
# def serve_image(image_path):
#     image_name = '{}'.format(image_path)
#     if image_name not in list_of_images:
#         raise Exception('"{}" is excluded from the allowed static files'.format(image_path))
#     return flask.send_from_directory(image_directory, image_name)


############################################################
########################## LAYOUT ##########################
############################################################

##########    HEADER    ###########
header = html.Div([
        dbc.Row([
            dbc.Col(html.Img(src=f"assets/img/DS4A.svg",  className="vertical-center"), md = 2),
            dbc.Col(html.H3(u"IMPACT OF FOREST COVER LOSS ON RIVER FLOW REGIME IN COLOMBIA", id="titulo", 
                            style={"color":"purple", "text-align": "center"}), 
                            md = 8), 
            dbc.Col(html.Img(src=f"assets/img/col-gov-logo.png", width="200px"), md = 2),
        ], className="vertical-center")
    ], 
    className="container_ds4a container")
###########    CARDS   #############
#climate scenario slider
scenarios = {1:'1', 2:'2', 3:'3', 4:'4'}
scn_slider = html.Div([
        dcc.Slider(
            min=1,
            max=4,
            step=None,
            marks=scenarios,
            value=2,
        )
    ], 
    style= {'display': 'none'},
    id = "scenarios"
)
#Cover Loss Slider
cover_loss_marks = {x: f'{x}%' for x in [0, 25, 50, 100]}
cover_loss_slider = html.Div([
        dcc.Slider(
            min=0,
            max=100,
            marks=cover_loss_marks,
            value=30,
            id = "cover-loss-scenario-value"
        )
    ], 
    style= {'display': 'none'},
    id = "cover-loss-scenario"
)

cards = html.Div([
        dbc.Row([
            dbc.Col([
                    dbc.Card([
                        html.Img(src="assets/img/cover_loss.png",  className="card-img"),
                        html.Div([
                            html.H5("Cover Loss", className="card-title"), 
                            html.H1(["30", html.Small("%")], className="display-4", id= 'cover-loss-value')
                        ], className = "card-img-overlay card_ds4a"),
                        ], className = "text-right"),
                    cover_loss_slider,
                ],
                md = 3
            ),
            dbc.Col(
                dbc.Card([
                    html.Img(src="assets/img/flow.png",  className="card-img"),
                    html.Div([
                        html.H5("Flow", className="card-title"), 
                        html.H1(["17", html.Small("mm")], className="display-4", id = 'flow-value')
                    ], className = "card-img-overlay card_ds4a"),
                    ], className = "text-left"),
                md = 3
            ),
            dbc.Col([
                    dbc.Card([
                        html.Img(src="assets/img/precipitation.png",  className="card-img"),
                        html.Div([
                            html.H5("Precipitation", className="card-title"), 
                            html.H1(["25", html.Small("mm")], className="display-4")
                        ], className = "card-img-overlay card_ds4a"),
                        ], className = "text-left"),
                    scn_slider,
                ],
                md = 3
            ),
            dbc.Col(
                [
                    dbc.Card([
                        html.Img(src="assets/img/temperature.png",  className="card-img"),
                        html.Div([
                            html.H5("Temperature", className="card-title"), 
                            html.H1(["28", html.Small("°"), "C"], className="display-4")
                        ], className = "card-img-overlay card_ds4a"),
                        ], className = "text-right"
                    ),
                ],
                md = 3
            ),
        ], className="vertical-center")

    ], 
    className="container_ds4a container")
###########    BODY    ############# 
switch = html.Div([
    html.Div([
        dbc.Label("Predictive", style={"margin-bottom": "5px",}),
        html.Br(),
        dbc.Label("Descriptive"),
        ],
        className="switch-container",
    ),
    html.Div(
        [
            dbc.Checklist(
                options=[
                    {"value": 1},
                ],
                value=[],
                id="predictive-descriptive-switch",
                inline=True,
                switch=True,
            )
        ], 
        className = "custom-control custom-switch"
    )
])

year_slider = html.Div([
    dcc.Slider(
        min=2000,
        max=2019,
        step=None,
        marks={value: str(value) for value in range(2000, 2020)},
        value=2010,
        className="slider-ds4a",
        id='year-slider',
    )  
], id='year-slider-div',)

months = {1:'JAN', 2:'FEB', 3:'MAR', 4:'APR', 5:'MAY', 6:'JUN', 
          7:'JUL', 8:'AGO', 9:'SEP', 10:'OCT', 11:'NOV', 12:'DEC'}
month_slider = html.Div([
    dcc.Slider(
        min=1,
        max=12,
        step=None,
        marks=months,
        value=10,
        id='month-slider',
    )  
])

##########################################################
######################### + INFO #########################
##########################################################

more_info = html.Div(
    [
        dbc.Button(html.I("+", className = "material-icons pmd-sm "), 
            id="open-more-info", className="btn pmd-btn-fab pmd-ripple-effect btn-info pmd-btn-raised more-info"
        ),
        dbc.Modal(#put here the content
            [
                dbc.ModalHeader("Title of more info Section"),
                dbc.ModalBody(
                    html.Div(
                        [
                            dbc.Row(
                                [ 
                                    dbc.Col(html.Img(src=f"assets/img/col-gov-logo.png", width="200px")),
                                ],
                            )
                        ], 
                    ),
                ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-more-info", className="ml-auto")
                ),
            ],
            id="more-info-modal",
            size="xl", #"lg" lg -> large,  xl -> extra-large
            scrollable=True, #comment if you want 
        ),   
    ]
)

#https://dash-leaflet.herokuapp.com/#us_states
basins_map_js = pd.read_json(basins_map_path)
basins_map_data = None
with open(basins_map_path) as f:
    basins_map_data = json.load(f)

marks = [0, 7, 14, 21, 28, 35, 42, 48]
colorscale = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026']

@app.callback(
    Output("more-info-modal", "is_open"),
    [Input("open-more-info", "n_clicks"), Input("close-more-info", "n_clicks")],
    [State("more-info-modal", "is_open")],)
def toggle_more_info(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


def get_style(feature):
    #return dict(fillColor='#FFEDA0', weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)
    color = [colorscale[i] for i, item in enumerate(marks) if feature["properties"]["Macrocuenca"] > item][-1]
    return dict(fillColor=color, weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)

def get_info(feature=None):
    header = [html.H4("Macrobasin")]
    #return header
    if not feature:
        return header + ["Hoover over a macrobasin"]
    return header + [html.B(feature["properties"]["Macrocuenca"]), html.Br(),
                     "{:.1f} ha".format(feature["properties"]["Area"])]

def get_macrobasin_id(feature=None):
    return feature["properties"]["Macrocuenca"]

ctg = ["{}-{}+".format(mark, marks[i + 1]) for i, mark in enumerate(marks[:-1])] + ["{}+".format(marks[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")

options = dict(hoverStyle=dict(weight=5, color='#666', dashArray=''), zoomToBoundsOnClick=True)
basins_map_json = dlx.geojson(basins_map_data, id="basins_map", defaultOptions=options, style=get_style)

info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})

map_graph = [dl.Map(children=[dl.TileLayer(), basins_map_json, colorbar, info], center=[4.60971, -74.08175], zoom=5)]

@app.callback(Output("info", "children"), [Input("basins_map", "featureHover")])
def info_hover(feature):
    return get_info(feature)

#graficos
data = pd.read_csv(data_path,  parse_dates = ['date'])
data.set_index(['mc'], inplace = True)

def plot_data(macrobasin, variables, year, month=12):
    dfc = data.loc[macrobasin].copy()
    #_figs = []
    #for i, var in enumerate(variables):
    print('+'*30, macrobasin, variables, year, month,'+'*30)

    var = variables[0]
    _fig = px.line(dfc, x='date', y=var
                    , range_x=[str(year)+'-01-01',str(year)+'-12-31']
                    , height=250)
        #_figs.append(_fig)
    return _fig

#flow_graph = dcc.Graph(id="flow-graph")
#flow_graph.figure = plot_data(1, ['v_rainfall_total'], '2010', '1')


#TODO: Capturar el cambio y filtrar la data, las gráficas estén supervisando esta data para que se propague

@app.callback([Output('scenarios', 'style'), Output('cover-loss-scenario', 'style'), Output('year-slider-div', 'style')],[Input("predictive-descriptive-switch", 'value')])
def on_switch(value):
    return {"display": "block" if value else "none"}, {"display": "block" if value else "none"}, {"display": "none" if value else "block"}


@app.callback([Output('flow-graph', 'figure'), Output('flow-value', 'children')], 
    [Input('year-slider', 'value'), Input("basins_map", "featureClick")])
def update_flow_graph(y_value, feature=None):
    macrobasin_id = 1
    if not feature is None:
        macrobasin_id = get_macrobasin_id(feature)
    df = data.loc[macrobasin_id].copy()
    flow = round(df[(df['date'] > f'{y_value}-01-01') & (df['date'] < f'{y_value}-12-31')]['v_flow_mean'].mean(),1)
    return plot_data(macrobasin_id, ['v_flow_mean'], y_value), ["{:.1e}".format(flow), html.Small("mm")]

@app.callback(Output('precipitation-graph', 'figure'),
    [Input('year-slider', 'value'), Input("basins_map", "featureClick")])
def update_precipitation_graph(y_value, feature=None):
    macrobasin_id = 1
    if not feature is None:
        macrobasin_id = get_macrobasin_id(feature)
    return plot_data(macrobasin_id, ['v_rainfall_total'], y_value)

@app.callback(Output('temperature-graph', 'figure'),
    [Input('year-slider', 'value'), Input("basins_map", "featureClick")])
def update_temperature_graph(y_value, feature=None):
    macrobasin_id = 1
    if not feature is None:
        macrobasin_id = get_macrobasin_id(feature)
    return plot_data(macrobasin_id, ['v_temperature_mean'], y_value)

@app.callback(Output('cover-loss-value', 'children'),[Input("cover-loss-scenario-value", 'value')])
def on_cover_loss_slider(value):
    return [f"{value}", html.Small("%")]



main_card = html.Div(
        dbc.Card([
            dbc.Row([ #switch and timeline
                dbc.Col(#md2 predictive/descriptive switch
                    switch, 
                    md=2
                ),
                dbc.Col(#md10 years slider
                    year_slider,
                    md=10,
                ),
            ]),
            dbc.Row([#map and graphs
                dbc.Col([#map and month_slider
                        #dbc.Row([dbc.Col(month_slider,)]),
                        dbc.Row([
                            dbc.Col(
                                html.Div(map_graph,
                                style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block", "margin-left": "15px"}, id="map"
                                )
                            ),
                            ],
                        ),

                    ], 
                    md=6
                ),
                dbc.Col([#graphs
                    dbc.Row([
                            dbc.Col(
                                dcc.Graph(id="flow-graph"),
                                #style={"margin-left":" 10px"}
                            ),
                            ],no_gutters=True,
                        ),
                    dbc.Row([
                            dbc.Col(
                                dcc.Graph(id="precipitation-graph"),
                                #style={"margin-left":" 10px"}
                            ),
                            ],no_gutters=True,
                        ),
                    dbc.Row([
                            dbc.Col(
                                dcc.Graph(id="temperature-graph"),
                                #style={"margin-left":" 10px"} figure=figs[2], 
                            ),
                            ],no_gutters=True,
                        ),

                    ], 
                    md=6
                )

            ])
        ], 
        className='main-card'
    ),
    className="container"
)

app.title = 'Team 28'
app.layout = dbc.Container(
    html.Div(
    [
        header,
        cards,
        main_card,
        more_info
    ]),
    fluid=True,
)

if __name__ in ["__main__"]:
    app.run_server(debug=True)