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

import about


PREDICT_YEAR_START = 2020

data_path = '../data/matrix/matrix_consol_v2.zip'
model_rank_path = '../model/model_rank.csv'
data_forecast_path = '../model/forecast_2020_2021.csv'

#forecast_group_column_format = 'Forecast_{Rank}_{model_type}_CC{loss_cover_scenario}'
forecast_group_column_format = 'Forecast_{}_{}_LossCover{}'

variables_graph = [
    {'variable':'flow', 'label':'Flow', 'color': ['#B855A4'], 'axis': '1'}, 
    {'variable':'rainfall', 'label':'Precipitation',  'color': ['#4ABEEE'], 'axis': '2'}, 
    {'variable':'temperature', 'label':'Temperature', 'color': ['#FCA93A'], 'axis': '3'},
    {'variable':'Forecast', 'color': ['#394ACA','#33D045','#99D045','#AAE156','#AAE156','#AAE156','#AAE156','#AAE156','#AAE156'], 'axis': '1'}, 
    ]
    
#
basins_map_options = [
    #{'label':'todas', 'value':'../data/shapes/Macro_Cuencas2.json'},
    {'label':'Macrobasins 1-38,42,45', 'value':'../data/shapes/Cuencas_ 1a38_42_45.json,1'},
    {'label':'Macrobasins 39,43,46', 'value':'../data/shapes/Cuencas_39_43_46.json,39'},
    {'label':'Macrobasins 40,44,47', 'value':'../data/shapes/Cuencas_40_44_47.json,40'},
    {'label':'Macrobasins 41,48', 'value':'../data/shapes/Cuencas_41_48.json,41'}]




#################  DEFINE THE DASH APP  ####################
app = dash.Dash(external_stylesheets=[dbc.themes.MATERIA, "https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"])
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
scenarios = {1:'A1', 2:'A2', 3:'B1', 4:'B2'}
scn_slider = html.Div([
        dcc.Slider(
            min=1,
            max=4,
            step=None,
            marks=scenarios,
            value=1,
            id = "scenarios-slider",
        ),
        dbc.Tooltip(
            "slide to choose between different climate change scenarios",
            target="scenarios-slider",
        ),
    ], 
    style= {'display': 'none'},
    id = "scenarios"
)
#Cover Loss Slider
# cover_loss_marks = {x: f'{x}%' for x in [0, 25, 50, 100]}
# cover_loss_slider = html.Div([
#         dcc.Slider(
#             min=0,
#             max=100,
#             marks=cover_loss_marks,
#             value=30,
#             id = "cover-loss-scenario-value"
#         )
#     ], 
#     style= {'display': 'none'},
#     id = "cover-loss-scenario"
# )
kwargs = {"data-step" : "1", "data-intro" : "In this Cards you can find the average/Year of each variable"} 
cards = html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                            dbc.Card([
                                html.Img(src="assets/img/cover_loss.png",  className="card-img"),
                                html.Div([
                                    html.H5("Cover Loss", className="card-title"), 
                                    html.H1(["30", html.Small("%")], className="display-5", id= 'cover-loss-value')
                                ], className = "card-img-overlay card_ds4a"),
                                ], 
                                className = "text-right",
                                id="cover-loss-card"
                            ),
                            # cover_loss_slider,
                        ],
                        md = 6
                    ),
                    dbc.Col(
                        dbc.Card([
                            html.Img(src="assets/img/flow.png",  className="card-img"),
                            html.Div([
                                html.H5("Flow", className="card-title"), 
                                html.H1(["17", html.Small(["m",html.Sup("3"), "/s"])], className="display-5", id = 'flow-value')
                            ], className = "card-img-overlay card_ds4a"),
                            ], 
                            className = "text-left",
                            id = "flow-card"
                        ),
                        md = 6
                    ),
                ]),
                html.Div([
                    html.H3("Select a Macrobasin in the map", style={"color":"purple"}, id="macrobasin-title"), 
                    html.Div(id='macrobasin-current', children='1', style={'display': 'none'})
                ])
            ], 
            md=6),
            dbc.Col([
                    dbc.Card([
                        html.Img(src="assets/img/precipitation.png",  className="card-img"),
                        html.Div([
                            html.H5("Precipitation", className="card-title"), 
                            html.H1(["25", html.Small("mm")], className="display-5", id= 'precipitation-value')
                        ], className = "card-img-overlay card_ds4a"),
                        ], 
                        className = "text-left",
                        id = "precititation-card"
                    ),
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
                            html.H1(["28", html.Small("°"), "C"], className="display-5", id= 'temperature-value')
                        ], className = "card-img-overlay card_ds4a"),
                        ], 
                        className = "text-right",
                        id = "temperature-card"
                    ),
                ],
                md = 3
            ),
        ], className="vertical-center")

    ], 
    className="container_ds4a container", **kwargs)
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

y_slider_marks = {value: str(value) for value in range(2000, 2020)}
y_slider_marks[2020] = {"label": "*2020", 'style': {'color': '#f00', 'font-weight': 'bold'}}
y_slider_marks[2021] = {"label": "*2021", 'style': {'color': '#f00', 'font-weight': 'bold'}}

kwargs = {"data-step":"2", "data-intro":"Here you can explore each year of data, and for 2020, 2021 get the Flow prediction", "data-position":'right', "data-scrollTo":'tooltip'}
year_slider = html.Div([
    dcc.Slider(
        min=2000,
        max=2021,
        step=None,
        marks=y_slider_marks,
        value=2010,
        className="slider-ds4a",
        id='year-slider',
    )  
], id='year-slider-div',**kwargs)

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
kwargs = {"data-step":"5", "data-intro":"Here you can find more information about the selected Basin", "data-position":'right', "data-scrollTo":'tooltip'}
more_info = html.Div(
    [
        dbc.Button(html.I(className="fa fa-info-circle", style={"font-size": "32px"}, **kwargs), 
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
    ], 
)

##########################################################
########################## ABOUT #########################
##########################################################
kwargs = {"data-step":"6", "data-intro":"Do U want to know our Awesome Team? Here we are", "data-position":'right', "data-scrollTo":'tooltip'}
about_div = html.Div(
    [
        dbc.Button([html.I(className="fa fa-users", style={"font-size": "16px", "margin-right": "5px"}), "   OUR TEAM"],
            id="open-our-team", color="primary", className="mr-1", style={"margin": "15px"}
        ),
        dbc.Modal(#put here the content
            [
                dbc.ModalHeader("TEAM 28"),
                dbc.ModalBody(
                    html.Div(
                        [
                            dbc.Row(
                                [ # dbc.Col(html.Img(src=f"assets/img/col-gov-logo.png", width="200px")),
                                    about.create_team_mate_card('Diana Camila', 'diana.jpg', 'Statistician, PhD in Biomedicine. Specialized in bioinformatics and high-throughput sequencing analysis. Skilled in machine learning and data mining. Experience working in research projects with multidisciplinary teams. I\'m passionate about traveling, nature and music.'), 
                                    about.create_team_mate_card('Jesus Alfonso', 'jesus.jpg', 'Civil Engineer Javeriana University / Specialist in Hydraulic Engineering IHE - Delft, Netherlands'), 
                                    about.create_team_mate_card('Jhon William', 'jhon.jpg', 'Electrical Engineer (Universidad Nacional de Colombia) / Specialist in Networks and Telecommunications (Universidad de Manizales) / Specialist in Energy and Gas Regulation (Universidad Esxternado de Colombia) / Specialist in Statistics (Universidad Nacional de Colombia) \
                                                                 / Oracle Certified Associate (Oracle) / .Net Development Certificate (Microsoft), Hobbies: Reading, learning office tools, Karate Do'), 
                                ],
                            ),
                            dbc.Row(
                                [ # dbc.Col(html.Img(src=f"assets/img/col-gov-logo.png", width="200px")),
                                    about.create_team_mate_card('Diego', 'diego.jpg', 'Ingeniero de Petróleos Universidad America. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat'), 
                                    about.create_team_mate_card('Juan Carlos', 'juan.jpg', 'Electronic Engineer National University of Colombia, Master in Management and Development of Software Projects Autonomous University of Manizales. Certificate in Development. Net. Microsoft.'), 
                                    about.create_team_mate_card('William', 'william.jpg', 'Electronic Engineer National University of Colombia, Master in Industrial Automation. Passionate about art, music and learning new things.'), 
                                ],
                            )
                        ], 
                    ),
                ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-our-team", className="ml-auto")
                ),
            ],
            id="our-team-modal",
            size="xl", #"lg" lg -> large,  xl -> extra-large
            #scrollable=True, #comment if you want 
        ),   
    ],
    **kwargs
)


################################################################################
############################## help button #####################################
################################################################################

help_div = html.Div(
    [
        dbc.Button(
            html.I(className="fa fa-question-circle", style={"font-size": "16px"}), 
            id="help-button", 
            className="btn pmd-btn-fab pmd-ripple-effect btn-success pmd-btn-raised help-button",
            color="success",
        ),
    ]
)




######################### Data ###########################
data = pd.read_csv(data_path,  parse_dates = ['date'])
data.set_index(['mc'], inplace = True)

model_rank = pd.read_csv(model_rank_path)

data_forecast = pd.read_csv(data_forecast_path,  parse_dates = ['date'])
data_forecast.rename(columns={'mc':'MC','v_flow_mean_pred':'flow','v_loss_cover_assum':'v_loss_cover',
                        'v_rainfall_total_assum':'v_rainfall_total'}, inplace=True)

data_forecast = data_forecast.merge(model_rank, left_on=['MC','model_type'], right_on=['MC','Model'], how = 'inner')
#data_forecast.loc[data_forecast.Model.isna(), ['Rank']] = 1
#data_forecast.loc[data_forecast.Model.isna(), ['Model']] = data_forecast[data_forecast.Model.isna()]['model_type']

#data_forecast['Group'] = forecast_group_column_format.format('Rank': data_forecast['Rank'], 'model_type': data_forecast['model_type'], 'loss_cover_scenario': data_forecast['loss_cover_scenario'])
data_forecast['Group'] = data_forecast.apply(lambda x: forecast_group_column_format.format(x['Rank'], x['model_type'], x['loss_cover_scenario']), axis=1)



###################### Map ###############################
year_current = 2010
#macrobasin_id_current = 1

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
    year = year if year < PREDICT_YEAR_START else PREDICT_YEAR_START - 1
    #print(year)
    dfc = data.loc[macrobasin].copy()
    dfc = dfc.loc[(dfc.year == year) & (dfc.month == 12), 'v_loss_cover']
    #print(dfc)
    return dfc.values[0]
    

def get_style(feature):
    global year_current
    macrobasin_id = get_macrobasin_id(feature)
    loss_cover_value = get_loss_cover(macrobasin_id, year_current)
    
    color = [colorscale[i] for i, item in enumerate(marks) if loss_cover_value > item][-1]
    return dict(fillColor=color, weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)

def get_info(feature=None, year=None):
    if feature is None:
        return None#["Hoover over a macrobasin"]

    macrobasin_id = get_macrobasin_id(feature)
    loss_cover_value = get_loss_cover(macrobasin_id, year)

    return [html.H4("Macrobasin " + str(macrobasin_id)), 
            "Loss Cover: {:.2f}".format(loss_cover_value * 100), html.Br(),
            "Area: {:.1f} ha".format(feature["properties"]["Area"])
            ]

def get_macrobasin_id(feature):
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
with open(basins_map_options[0]['value'].split(",")[0]) as f:
    _ = json.load(f)
    basins_map_json = dlx.geojson(_, id="basins_map", defaultOptions=options, style=get_style)
map_graph = dl.Map(children=[dl.TileLayer(), basins_map_json, colorbar, info], center=[4.60971, -74.08175], zoom=5)


#print(type(map_graph))

#map_graph = show_map(basins_map_options[0]['value'])

@app.callback(Output("info", "children"), [Input("basins_map", "featureHover"), Input('year-slider', 'value')])
def info_hover(feature, year):
    #global year_current
    #global macrobasin_id_current
    
    #macrobasin_id = None
    #if feature is None:
    #    macrobasin_id = get_macrobasin_id(feature)
    
    #if not year == None:
    #    year_current = year

    return get_info(feature, year)


@app.callback(
    [Output('basins_map', 'children')], #Output('macrobasin-current', 'children')
    [Input('macro-basins', 'value'), Input('year-slider', 'value')])
def update_map(map_value, year):
    map_path, macrobasin_id = map_value.split(",")
    with open(map_path) as f:
        _ = json.load(f)
        basins_map_json = dlx.geojson(_, id="basins_map", defaultOptions=options, style=get_style)

    #TODO: Buscar la primera macrozona del mapa
    return [dl.Map(children=[dl.TileLayer(), basins_map_json, colorbar, info], 
                    center=[4.60971, -74.08175], zoom=5)]
    #macrobasin_id


############################### Graphs ###############################
def plot_data(macrobasin, variables, year, climate_change):
    dfc = data.loc[macrobasin].copy()
    dfc.reset_index(drop=True, inplace=True)
    
    print('+'*30, macrobasin, year, climate_change, [v['variable'] for v in variables],'+'*30)

    if year >= PREDICT_YEAR_START:
        data_forecast_mc = \
        data_forecast.loc[(data_forecast.MC == macrobasin) 
                            & (data_forecast.climate_change_scenario == climate_change) 
                            & ((data_forecast.Rank == 1) | (data_forecast.loss_cover_scenario == '100%')), 
                        ['date','year','month','flow','Group','v_loss_cover','v_rainfall_total']]
        
        if data_forecast_mc.shape[0] > 0:    
            data_forecast_mc2 = \
                data_forecast_mc.pivot_table(index=['date','year','month'], columns='Group', values='flow', aggfunc='first')
            data_forecast_mc2.reset_index(inplace=True)

            data_forecast_mc = data_forecast_mc.merge(data_forecast_mc2, on=['date','year','month'], how = 'inner')
            data_forecast_mc.drop(columns=['flow','Group'], inplace=True)

            data_forecast_mc.reset_index(inplace=True)
            dfc = pd.concat([dfc,data_forecast_mc])



    #print(dfc[['date','v_flow_mean','v_loss_cover','v_rainfall_total','v_temperature_mean']].tail())
    #print(dfc.tail())

    has_temperature = True
    if False:#np.isnan(dfc.iloc[0,6]):
        has_temperature = False
        variables = [v for v in variables if v['label'] != 'Temperature']


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


@app.callback(Output('macrobasin-current', 'children'), [Input('basins_map', 'featureClick')], [State('macrobasin-current', 'children')])
def select_macrobasin(feature:None, macrobasin_id_ini):
    if feature is None:
        macrobasin_id = int(macrobasin_id_ini)
    else: 
        macrobasin_id = get_macrobasin_id(feature)
    return macrobasin_id

@app.callback([Output('graph', 'figure'), Output('cover-loss-value', 'children'), Output('flow-value', 'children'), 
               Output('precipitation-value', 'children'), Output('temperature-value', 'children'), 
               Output('macrobasin-title', 'children')],
    [Input('year-slider', 'value'), Input('scenarios-slider', 'value'), Input("macrobasin-current", "children")])
def update_graph(y_value, climate_change, macrobasin_id):
    global year_current
    year_current = y_value

    climate_change = scenarios[climate_change]
    #macrobasin_id = macrobasin_id_current if macrobasin_id_current != None else 1
    #if not feature is None:
    #    macrobasin_id = get_macrobasin_id(feature)
    loss_cover = get_loss_cover(macrobasin_id, y_value)
    loss_cover = round(loss_cover*100, 1) if loss_cover else '-'
    flow = get_flow(macrobasin_id, y_value)
    flow = round(flow, 1) if flow else '-'
    precip = get_precipitation(macrobasin_id, y_value)
    precip = round(precip, 1) if precip else '-'
    temperature = get_temperature(macrobasin_id, y_value)
    temperature = round(temperature, 1) if not np.isnan(temperature) else '-'
    macrobasin_title = f"Macrobasin {macrobasin_id} >> Year {y_value}"

    return (plot_data(macrobasin_id, variables_graph, y_value, climate_change), [f"{loss_cover}", html.Small("%")], [f"{flow}"[:5], html.Small(["m",html.Sup("3"), "/s"])],
            [f"{precip}", html.Small("mm")], [f"{temperature}", html.Small("°"), "C"], macrobasin_title)





@app.callback(
    Output("more-info-modal", "is_open"),
    [Input("open-more-info", "n_clicks"), Input("close-more-info", "n_clicks")],
    [State("more-info-modal", "is_open")],)
def toggle_more_info(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("our-team-modal", "is_open"),
    [Input("open-our-team", "n_clicks"), Input("close-our-team", "n_clicks")],
    [State("our-team-modal", "is_open")])
def toggle_our_team(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

def get_flow(macrobasin, year):
    year = year if year < PREDICT_YEAR_START else PREDICT_YEAR_START - 1
    
    dfc = data.loc[macrobasin].copy()
    dfc = dfc.loc[(dfc.year == year), 'v_flow_mean'].mean()
    #print(dfc)
    return dfc

def get_precipitation(macrobasin, year):
    year = year if year < PREDICT_YEAR_START else PREDICT_YEAR_START - 1
    dfc = data.loc[macrobasin].copy()
    dfc = dfc.loc[(dfc.year == year), 'v_rainfall_total'].mean()
    #print(dfc)
    return dfc

def get_temperature(macrobasin, year):
    year = year if year < PREDICT_YEAR_START else PREDICT_YEAR_START - 1
    dfc = data.loc[macrobasin].copy()
    dfc = dfc.loc[(dfc.year == year), 'v_temperature_mean'].mean()
    #print(dfc)
    return dfc

app.clientside_callback(
    """
    function(help) {
        introJs().start();
        return "success";
    }
    """,
    Output("help-button", 'color'),
    [Input("help-button", "n_clicks")
     ]
)



#TODO: Capturar el cambio y filtrar la data, las gráficas estén supervisando esta data para que se propague

@app.callback([Output('scenarios', 'style'), Output("cover-loss-card", "className"), Output("temperature-card", "className")],[Input('year-slider', 'value')], [State("cover-loss-card", "className"), State("temperature-card", "className")])
def on_switch(value, cover_loss_class, temperature_class):
    return {"display": "block" if value > 2019 else "none"}, f"{cover_loss_class} disabled-card" if value > 2019 else cover_loss_class.split()[0], f"{temperature_class} disabled-card" if value > 2019 else temperature_class.split()[0]


kwargs = {"data-step":"3", "data-intro":"You Can Select any macro basin you are interested", "data-position":'right', "data-scrollTo":'tooltip'}
kwargs1 = {"data-step":"4", "data-intro":"You Can Visualize the values of flow, precipitation and temperature, of the selected Basin in a selected year", "data-position":'right', "data-scrollTo":'tooltip'}
main_card = html.Div(
        dbc.Card([
            dbc.Row([ #switch and timeline
                #dbc.Col(#md2 predictive/descriptive switch
                #    switch, 
                #    md=2
                #),
                dbc.Col(#md10 years slider
                    year_slider,
                    #md=10,
                ),
            ]),
            dbc.Row([#map and graphs
                dbc.Col([#map and month_slider
                        dbc.Row([dbc.Col(basins_dropdown,)]),
                        dbc.Row([
                            dbc.Col([
                                html.Div(
                                    map_graph,
                                    style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block", "margin-left": "15px"}, 
                                    id="map",
                                    **kwargs
                                ),
                                about_div,
                            ]),
                            ],
                        ),

                    ], 
                    md=6
                ),
                dbc.Col([#graphs
                    dbc.Row([
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(id="graph"),
                                    **kwargs1
                                )
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
        more_info,
        help_div,
    ]),
    fluid=True,
)

if __name__ in ["__main__"]:
    app.run_server(debug=True)