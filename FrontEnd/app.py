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
import numpy as np
import datetime


data_path = '../data/matrix/matrix_consol_v2.zip'
model_rank_path = '../model/model_rank.csv'
data_forecast_path = '../model/forecast.csv'

variables_graph = [
    {'variable':'flow', 'label':'Flow', 'color': ['#B855A4'], 'axis': '1'}, 
    {'variable':'rainfall', 'label':'Rain Fall',  'color': ['#4ABEEE'], 'axis': '2'}, 
    {'variable':'temperature', 'label':'Temperature', 'color': ['#FCA93A'], 'axis': '3'},
    {'variable':'fc', 'color': ['#394ACA', '#33D045', '#99D045'], 'axis': '1'}, 
    ]
    
#
basins_map_options = [
    #{'label':'todas', 'value':'../data/shapes/Macro_Cuencas2.json'},
    {'label':'Macrobasins 1-38,42,45', 'value':'../data/shapes/Cuencas_ 1a38_42_45.json'},
    {'label':'Macrobasins 39,43,46', 'value':'../data/shapes/Cuencas_39_43_46.json'},
    {'label':'Macrobasins 40,44,47', 'value':'../data/shapes/Cuencas_40_44_47.json'},
    {'label':'Macrobasins 41,48', 'value':'../data/shapes/Cuencas_41_48.json'}]




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

# months = {1:'JAN', 2:'FEB', 3:'MAR', 4:'APR', 5:'MAY', 6:'JUN', 
#           7:'JUL', 8:'AGO', 9:'SEP', 10:'OCT', 11:'NOV', 12:'DEC'}
# month_slider = html.Div([
#     dcc.Slider(
#         min=1,
#         max=12,
#         step=None,
#         marks=months,
#         value=10,
#         id='month-slider',
#     )  
# ])

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







######################### Data ###########################
data = pd.read_csv(data_path,  parse_dates = ['date'])
data.set_index(['mc'], inplace = True)

model_rank = pd.read_csv(model_rank_path)

data_forecast = pd.read_csv(data_forecast_path,  parse_dates = ['date'])
data_forecast = data_forecast.merge(model_rank, left_on=['MC','model_type'], right_on=['MC','Model'], how = 'inner')
data_forecast['Rank_model'] = 'fc_'+data_forecast['Rank'].astype(str) +'_' + data_forecast['model_type']



###################### Map ###############################
year_current = 2010
macrobasin_id_current = 1

colorscale = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026']

def get_color_marks(x, cs):
    x_min = x.min()
    x_max = x.max()
    x_len = len(cs)
    x_step = (x_max - x_min) / (x_len - 1)

    #print(x_min, x_max)
    _ = []
    for i in range(x_len + 1):
        _.append(x_min + i * x_step)
    
    #_[-1] = x_max
    return _


def get_loss_cover(macrobasin, year):
    dfc = data.loc[macrobasin].copy()
    dfc = dfc.loc[(dfc.year == year) & (dfc.month == 12), 'v_loss_cover']
    #print(dfc)
    return dfc.values[0]
    

def get_style(feature):
    #cmap = matplotlib.cm.get_cmap('OrRd')
    #matplotlib.colors.Normalize(vmin=loss_cover.min(), vmax=loss_cover.max())
    #color = matplotlib.colors.rgb2hex(cmap(0.025958))
    #return dict(fillColor='#FFEDA0', weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)
    macrobasin_id = get_macrobasin_id(feature)
    loss_cover_value = get_loss_cover(macrobasin_id, year_current)
    #print(loss_cover_value)
    color = [colorscale[i] for i, item in enumerate(marks) if loss_cover_value > item][-1]
    return dict(fillColor=color, weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)

def get_info(feature=None):
    if not feature:
        return None#["Hoover over a macrobasin"]

    macrobasin_id = get_macrobasin_id(feature)
    loss_cover_value = get_loss_cover(macrobasin_id, year_current)

    return [html.H4("Macrobasin " + str(macrobasin_id)), 
            "Loss Cover: {:.2f}".format(loss_cover_value * 100), html.Br(),
            "Area: {:.1f} ha".format(feature["properties"]["Area"])
            ]

def get_macrobasin_id(feature=None):
    return feature["properties"]["Macrocuenca"]

loss_cover_all = data['v_loss_cover']
marks = get_color_marks(loss_cover_all, colorscale)

basins_dropdown = dcc.Dropdown(
        id='macro-basins',
        options=basins_map_options,
        value=basins_map_options[0]['value']
    ) 


ctg = ["{:.0f}+".format(mark * 100, marks[i + 1]*100) for i, mark in enumerate(marks[:-1])]# + ["{:.0f}+".format(marks[-1] * 100)]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")

options = dict(hoverStyle=dict(weight=5, color='#666', dashArray=''), zoomToBoundsOnClick=False)
info = html.Div(children=get_info(), id="info", className="info",
            style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})


#def show_map(path):
#basins_map_data = None
#map_graph = None
with open(basins_map_options[0]['value']) as f:
    _ = json.load(f)
    basins_map_json = dlx.geojson(_, id="basins_map", defaultOptions=options, style=get_style)
map_graph = dl.Map(children=[dl.TileLayer(), basins_map_json, colorbar, info], center=[4.60971, -74.08175], zoom=5)


#print(type(map_graph))

#map_graph = show_map(basins_map_options[0]['value'])

@app.callback(Output("info", "children"), [Input("basins_map", "featureHover")])
def info_hover(feature:None):
    global year_current
    global macrobasin_id_current
    
    if not feature == None:
        macrobasin_id_current = get_macrobasin_id(feature)
    
    #if not year == None:
    #    year_current = year

    return get_info(feature)


@app.callback(
    Output('basins_map', 'children'),
    [Input('macro-basins', 'value'), Input('year-slider', 'value')])
def update_map(map_path, year):
    global year_current
    global macrobasin_id_current
    year_current = year
    macrobasin_id_current = None#get_macrobasin_id(feature)

    with open(map_path) as f:
        _ = json.load(f)
        basins_map_json = dlx.geojson(_, id="basins_map", defaultOptions=options, style=get_style)

    return [dl.Map(children=[dl.TileLayer(), basins_map_json, colorbar, info], center=[4.60971, -74.08175], zoom=5)]




############################### Graphs ###############################
def plot_data(macrobasin, variables, year):
    dfc = data.loc[macrobasin].copy()
    dfc.reset_index(drop=True, inplace=True)
    
    data_forecast_mc = \
    data_forecast.loc[(data_forecast.MC == macrobasin) & 
                      (data_forecast.climate_change_scenario == 1) & (data_forecast.loss_cover_scenario == 0),
                     ['date','year','month','flow','Rank_model']]
    data_forecast_mc = \
        data_forecast_mc.pivot_table(index=['date','year','month'], columns='Rank_model', values='flow', aggfunc='first')
    data_forecast_mc.reset_index(inplace=True)
    

    if data_forecast_mc.shape[0] > 0:
        dfc = pd.concat([dfc,data_forecast_mc])

    has_temperature = True
    if False:#np.isnan(dfc.iloc[0,6]):
        has_temperature = False
        variables = [v for v in variables if v['label'] != 'Temperature']

    print('+'*30, macrobasin, year, [v['variable'] for v in variables],'+'*30)

    _fig = go.Figure()
    _fig.update_layout(
        autosize=True,
        #width=500,
        #height=500,
        margin=go.layout.Margin(l=0,r=40,b=0,t=70,pad=0)
    )

    #for i, var in enumerate(variables):
    color_var_index = {}
    for c in dfc.columns:
        v = next((v for v in variables if v["variable"] in c), None)
        if v:
            if v["variable"] in color_var_index:
                color_var_index[v["variable"]] += 1
            else:
                color_var_index[v["variable"]] = 0

            color = v['color'][color_var_index[v["variable"]]]
            
            _fig.add_trace(go.Scatter(
                x=dfc['date'], y=dfc[c], 
                name=c if not 'label' in v else v['label'],
                yaxis='y' + v['axis'],
                line=dict(color=color),
                line_shape='spline'
            ))

    _fig.update_layout(xaxis_range=[datetime.datetime(year, 1, 1), datetime.datetime(year, 12, 31)])

    _fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1
    ))

    _fig.update_xaxes(rangeslider_visible=True)

    _fig.update_layout(
        yaxis1=dict(
            tickfont=dict(
                color=variables[0]['color'][0]
            )
        ),
        yaxis2=dict(
            tickfont=dict(
                color=variables[1]['color'][0]
            ),
            anchor="x",
            overlaying="y",
            side="right",
        ),
    )

    if has_temperature:
        _fig.update_layout(
            yaxis3=dict(
                #title=variables[2],
                # titlefont=dict(color="#FCA93A"),
                tickfont=dict(
                    color=variables[2]['color'][0]
                ),
                anchor="free",
                overlaying="y",
                side="right",
                position=0.945
            )
    )

    return _fig


@app.callback(Output('graph', 'figure'), 
    [Input('year-slider', 'value'), Input("basins_map", "featureClick")])
def update_graph(y_value, feature=None):
    macrobasin_id = 1
    if not feature is None:
        macrobasin_id = get_macrobasin_id(feature)
    return plot_data(macrobasin_id, variables_graph, y_value)





@app.callback(
    Output("more-info-modal", "is_open"),
    [Input("open-more-info", "n_clicks"), Input("close-more-info", "n_clicks")],
    [State("more-info-modal", "is_open")],)
def toggle_more_info(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


#TODO: Capturar el cambio y filtrar la data, las gráficas estén supervisando esta data para que se propague

@app.callback([Output('scenarios', 'style'), Output('cover-loss-scenario', 'style'), Output('year-slider-div', 'style')],[Input("predictive-descriptive-switch", 'value')])
def on_switch(value):
    return {"display": "block" if value else "none"}, {"display": "block" if value else "none"}, {"display": "none" if value else "block"}


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
                        dbc.Row([dbc.Col(basins_dropdown,)]),
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
                                dcc.Graph(id="graph"),
                                #style={"margin-left":" 10px"}
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