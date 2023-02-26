import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.graph_objs as go
import json

from df_wrangling import clean_df, swing_to_new_party, identify_the_winners

app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])

# read in the data
ge_df = pd.read_excel(
    "./data/2017_General_Election_Results.xls"
)
ge_df = clean_df(ge_df)



"""
Static Functions
"""
def plot_the_winners():

    ge_winners_df = identify_the_winners(ge_df)

    graph = dcc.Graph(
        id="winners_graph", 
        figure=go.Figure(
            data=[
                go.Bar(
                    x=ge_winners_df['party'],
                    y=ge_winners_df['seats_won'],
                    marker=dict(color="rgb(248, 131, 121)"),
                    width=0.9,
                    orientation="v",
                )
            ],
            layout=go.Layout(
                height=500,
                margin={"l": 60, "r": 20, "b": 20, "t": 60, "pad": 0},
            ),
        )
    )

    return graph


"""
Page Contents
"""
heading_card = dbc.Card(
    [html.H3("General Election Results"), html.Hr()],
    body=True,
    style={"height": "100%"},
)

winners_chart = dbc.Card(
    [
        html.H3("Number of constituencies won by each party"),
        html.Hr(),
        html.Div([plot_the_winners()]),
    ],
    body=True,
    style={"height": "100%"},
)

new_winners_chart = dbc.Card(
    [
        html.H3("New number of constituencies won by each party"),
        html.Hr(),
        html.Div(id="new_outcome_graph", children=[]),
    ],
    body=True,
    style={"height": "100%"},
)

markers = {i: str(i) for i in range(0,105,10)}

con_scale = dbc.Card(
    [
        html.H3("Conservative swing"),
        dcc.Slider(
            min=0,
            max=100,
            marks=markers,
            value=0,
            id="con_slider",
        )
    ],
    className = "mb-10"
)
lab_scale = dbc.Card(
    [
        html.H3("Labour swing"),
        dcc.Slider(
            min=0,
            max=100,
            marks=markers,
            value=0,
            id="lab_slider",
        )
    ]
)
snp_scale = dbc.Card(
    [
        html.H3("SNP swing"),
        dcc.Slider(
            min=0,
            max=100,
            marks=markers,
            value=0,
            id="snp_slider",
        )
    ]
)
ld_scale = dbc.Card(
    [
        html.H3("Lib Dem swing"),
        dcc.Slider(
            min=0,
            max=100,
            marks=markers,
            value=0,
            id="ld_slider",
        )
    ]
)
green_scale = dbc.Card(
    [
        html.H3("Green swing"),
        dcc.Slider(
            min=0,
            max=100,
            marks=markers,
            value=0,
            id="green_slider",
        )
    ]
)
pc_scale = dbc.Card(
    [
        html.H3("Plaid Cymru swing"),
        dcc.Slider(
            min=0,
            max=100,
            marks=markers,
            value=0,
            id="pc_slider",
        )
    ]
)

"""
Build the Page
"""
app.layout = dbc.Container(
    children=[
        dbc.Row([heading_card]),
        html.Br(),
        dbc.Row([
            winners_chart,
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                con_scale,
                html.Br(),
                lab_scale,
                html.Br(),
                snp_scale,
                html.Br(),
                ld_scale,
                html.Br(),
                green_scale,
                html.Br(),
                pc_scale,
                html.Br(),
            ]),
            dbc.Col([
                new_winners_chart
            ]),
        ]),
    ]
)

"""
callback functions
"""
@app.callback(
    Output("new_outcome_graph","children"),
    [
        Input("con_slider", "value"),
        Input("lab_slider", "value"),
        Input("snp_slider", "value"),
        Input("ld_slider", "value"),
        Input("green_slider", "value"),
        Input("pc_slider", "value")
    ],
)
def plot_new_outcome(con_swing, lab_swing, snp_swing, ld_swing, green_swing, plaid_swing):
    
    party_swings = {
        "C": con_swing,
        "Lab": lab_swing,
        "SNP": snp_swing,
        "LD": ld_swing,
        "Green": green_swing,
        "PC": plaid_swing
    }

    adjusted_winners_df = swing_to_new_party(ge_df, party_swings)

    graph = dcc.Graph(
        id="new_winners_graph",
        figure=go.Figure(
            data=[
                go.Bar(
                    x=adjusted_winners_df['party'],
                    y=adjusted_winners_df['seats_won'],
                    marker=dict(color="rgb(248, 131, 121)"),
                    width=0.9,
                    orientation="v",
                )
            ],
            layout=go.Layout(
                height=500,
                margin={"l": 60, "r": 20, "b": 100, "t": 60, "pad": 0},
            ),
        )
    )
    
    return graph


if __name__ == "__main__":
    app.run_server(port=8888, debug=True)

