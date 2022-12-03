from dash import Dash, html, dcc
import plotly.express as px

import services

app = Dash(__name__)


yc = services.get_yield_curve()
spreads = services.calculate_rate_spreads(yc)
fig = px.line(spreads, x=spreads.index, y="DGS10-DGS2")

app.layout = html.Div(children=[
    html.H1(children='US 10 - 2 year spread'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig,
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
