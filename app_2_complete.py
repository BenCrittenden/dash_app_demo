import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# import pandas and plotly graph object
import pandas as pd
import plotly.graph_objs as go

from df_wrangling import identify_the_winners, clean_df

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
                # background dist
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

"""
Build the Page
"""
app.layout = dbc.Container(
    children=[
        dbc.Row([heading_card]),
        dbc.Row([winners_chart])
    ]
)



if __name__ == "__main__":
    app.run_server(port=8888, debug=True)

