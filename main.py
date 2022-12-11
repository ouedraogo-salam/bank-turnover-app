import pandas as pd
import numpy as np
from dash import Dash, dcc, html, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

app = Dash(__name__)

churn_df = pd.read_csv(
    "C:\\Users\\user\\Data_Science\\Bank_Turnover\\dash_app\\Churn_Modelling_clean.csv")

geography_graph = go.Figure(
    px.histogram(data_frame=churn_df, x="geography",
                 color="exited")
)

app.layout = html.Div([
    html.Div(
        children="Bank Turnover Customer Dashboard",
        className="display-5 text-center text-underline",
        style={"color": "#fd7b12"}
    ),

    html.Div(
        [
            dcc.Graph(id="geography_graph", figure=geography_graph),
        ],
    ),

    html.Div(
        [
            html.Hr(),
            html.Div([
                html.Label(
                    children="Geography", className="mb-2 text-center w-100 text-uppercase"
                ),
                dcc.Dropdown(
                    id="geography_select",
                    options=[
                        {'label': 'France', 'value': 'France'},
                        {'label': 'Spain', 'value': 'Spain'},
                        {'label': 'Germany', 'value': 'Germany'},
                    ],
                    value="France",
                )
            ],
                className="col-3"
            ),
            html.Hr(className="mt-4"),
        ],
        className='row d-flex justify-content-center'
    ),

    html.Div(
        [
            dcc.Graph(id="products_graph")
        ]
    ),

    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(id="age_graph"),
                ],
                className='col-lg-6',
            ),
            html.Div(
                [
                    dcc.Graph(id="balance_graph"),
                ],
                className='col-lg-6',
            ),
        ],
        className='row'
    ),

    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(id="gender_graph"),
                ],
                className='col-lg-6',
            ),
            html.Div(
                [
                    dcc.Graph(id="tenure_graph"),
                ],
                className='col-lg-6',
            ),
        ],
        className='row'
    ),

    html.Footer([
        html.Span("Copyright @ 2022 All rights reserved"),
    ],
        className="d-flex justify-content-center align-items-center text-uppercase",
        style={"backgroundColor": "#555", "height": 45}
    )


])


@callback(
    Output("products_graph", "figure"),
    Output("age_graph", "figure"),
    Output("balance_graph", "figure"),
    Output("gender_graph", "figure"),
    Output("tenure_graph", "figure"),
    Input("geography_select", "value"),
)
def update_callback(geography_value):
    df_country = churn_df.query("geography==@geography_value")

    products_graph = go.Figure(
        px.pie(data_frame=df_country, values="num_of_products",
               names="num_of_products", category_orders=dict(num=[1, 2, 3, 4]))
    )
    age_graph = go.Figure(
        px.histogram(data_frame=df_country, x="age",
                     pattern_shape="exited", color="exited", nbins=92)
    )

    balance_graph = go.Figure(
        px.histogram(data_frame=df_country, x="balance", pattern_shape="exited", color="exited",
                     nbins=30)
    )

    gender_graph = go.Figure(
        px.histogram(data_frame=df_country, x="gender", pattern_shape="exited",
                     y="balance", color="exited")
    )

    tenure_graph = go.Figure(
        px.histogram(data_frame=df_country, x="tenure", color="exited",
                     category_orders=dict(mounth=list(f'{num}' for num in np.arange(10))), pattern_shape="exited"
                     )
    )

    tenure_graph.update_layout(
        bargap=0.2,
    )
    return products_graph, age_graph, balance_graph, gender_graph, tenure_graph


if __name__ == "__main__":
    app.run_server(debug=True)
