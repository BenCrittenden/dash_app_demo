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
            value=33,
            id="con_slider",
        )
    ]
)
lab_scale = dbc.Card(
    [
        html.H3("Labour swing"),
        dcc.Slider(
            min=0,
            max=100,
            marks=markers,
            value=33,
            id="lab_slider",
        )
    ]
)

#1. Create sliders for the SNP, LibDems, Greens and Plaid Cymru

"""
Build the Page
"""
app.layout = dbc.Container(
    children=[
        dbc.Row([heading_card]),
        dbc.Row([
            winners_chart,
        ]),
        dbc.Row([
            dbc.Col([
                con_scale,
                lab_scale,
                # Add your sliders here
            ]),
            # Add the new winners chart as a new column
        ]),
    ]
)

"""
callback functions

This is how you make your app interactive. Everytime you interact with a component
of your app, these functions are evaluated and that is how your app updates.
These are somewhat limited - you can only have a single output, which can mean that
you need to get creative sometimes.
"""

@app.callback(
    Output("new_outcome_graph","children"),
    [
        Input("con_slider", "value"),
        Input("lab_slider", "value")
        #2. Add the input from your additional sliders
    ]
)
def plot_new_outcome(con_swing, lab_swing): #3. any new arguments?
    
    party_swings = {
        "C": con_swing,
        "Lab": lab_swing,
        #4. anything to add here?
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
                margin={"l": 60, "r": 20, "b": 20, "t": 60, "pad": 0},
            ),
        )
    )
    
    return graph


if __name__ == "__main__":
    app.run_server(port=8888, debug=True)

