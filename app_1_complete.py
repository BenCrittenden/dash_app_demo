import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])
# https://www.bootstrapcdn.com/bootswatch/

"""
Page Contents
"""
heading_card = dbc.Card(
    [html.H3("General Election Results"), html.Hr()],
    body=True,
    style={"height": "100%"},
)

"""
Build the Page
"""

app.layout = dbc.Container(
    children = [dbc.Row(heading_card)]
)

if __name__ == "__main__":
    app.run_server(port=8888, debug=True)
    #
