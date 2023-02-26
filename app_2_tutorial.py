import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# import pandas and plotly graph object
import pandas as pd
import plotly.graph_objs as go

from df_wrangling import identify_the_winners, clean_df

app = dash.Dash()

# read in the data
ge_df = pd.read_excel(
    "./data/2017_General_Election_Results.xls"
)
ge_df = clean_df(ge_df)


"""
Static Functions
"""
def plot_the_winners():
    """
    rearrange the last election results and plot a bar graph with the
    number of seats won by each party.
    """

    ge_winners_df = identify_the_winners(ge_df)

    graph = dcc.Graph(
        id="winners_graph",
        figure=go.Figure(
            data=[
                # background dist
                go.Bar(
                    x=ge_winners_df['party'],
                    y=ge_winners_df['seats_won'],
                    marker=dict(color="rgb(0,174,249)"),
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


# Create another dbc.Card with a heading, a horizontal rule, and the graph
# created by plot_the_winners.
# hint: html.Div([plot_the_winners()]), is how you can place the graph in
# the card.



"""
Build the Page
"""
app.layout = dbc.Container(
    children=[
        dbc.Row([heading_card])
        # Add the card that you just created as another dbc.Row()
    ]
)



if __name__ == "__main__":
    app.run_server(port=8888, debug=True)

