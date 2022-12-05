from datetime import date
from dash import Dash, html, dcc
import plotly.graph_objs as go

import services

app = Dash(__name__)


def get_layout():
    """wrapper to generate main page.

    Wrapped to protect from unintended execution on import.
    """
    yc = services.get_yield_curve(start_date=date(2005, 1, 1))
    spreads = services.calculate_rate_spreads(yc)
    fig = go.Figure(
        data=[
            go.Scatter(
                x=spreads.index,
                y=spreads["DGS10-EFFR"],
                name="10y-FED Funds Effective Rate",
            ),
            go.Scatter(
                x=spreads.index,
                y=spreads["DGS10-DGS1MO"],
                name="10y-1m",
                visible="legendonly",
            ),
            go.Scatter(
                x=spreads.index,
                y=spreads["DGS10-DGS3MO"],
                name="10y-3m",
            ),
            go.Scatter(
                x=spreads.index,
                y=spreads["DGS10-DGS6MO"],
                name="10y-6m",
                visible="legendonly",
            ),
            go.Scatter(
                x=spreads.index,
                y=spreads["DGS10-DGS1"],
                name="10y-1y",
                visible="legendonly",
            ),
            go.Scatter(
                x=spreads.index,
                y=spreads["DGS10-DGS2"],
                name="10y-2y",
            ),
            go.Scatter(
                x=spreads.index,
                y=spreads["DGS10-DGS3"],
                name="10y-3y",
                visible = "legendonly",
            ),
            go.Scatter(
                x=spreads.index,
                y=spreads["DGS10-DGS5"],
                name="10y-5y",
                visible="legendonly",
            ),
            go.Scatter(
                x=spreads.index,
                y=spreads["DGS10-DGS7"],
                name="10y-7y",
                visible="legendonly",
            ),
        ]

    )

    layout = html.Div(children=[
        html.H1(children="Inversionwatch"),

        html.Div(children='''
            The following interactive plot shows various rate spreads against the 10y rate.
        '''),

        dcc.Graph(
            id="time-series-spreads-against-10y",
            figure=fig,
        )
    ])
    return layout


if __name__ == "__main__":
    app.layout = get_layout()
    app.run_server(
        debug=True,
        host="0.0.0.0",
        port=8050,
    )
