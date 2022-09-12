import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, ctx
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from dash import dash_table
import datetime as dt
import yfinance as yf
import numpy as np

option_chain = pd.read_parquet("backend/data/option_chain.parquet")

symbol = "AAPL"
ticker = option_chain.act_symbol.unique()
expiration_date = option_chain.loc[option_chain.act_symbol==symbol,"expiration"].unique()
call_put = ['Call', 'Put']
strike = np.sort(option_chain.loc[option_chain.act_symbol==symbol,"strike"].unique())
expiration = "2022-05-20"

select_data = option_chain[(option_chain.act_symbol==symbol) & (option_chain.expiration==expiration)]

select_data.date = pd.to_datetime(select_data.date)
select_data.expiration = pd.to_datetime(select_data.expiration)
year = dt.datetime(2022, 5, 1)
example_df = select_data.loc[
    (select_data["expiration"] > year) & (select_data["date"] == select_data.date.unique()[-1]),]
example_df["date"] = example_df["date"].dt.strftime('%Y.%m.%d')
example_df["expiration"] = example_df["expiration"].dt.strftime('%Y.%m.%d')
data_cols = ['strike', 'bid', 'ask', 'vol', 'delta', 'gamma', 'theta', 'vega', 'rho', "call_put"]
call_data = example_df.loc[example_df["call_put"]=="Call", data_cols].reset_index(drop=True)
call_data.columns = ['c_strike', 'c_bid', 'c_ask', 'c_vol', 'c_delta', 'c_gamma', 'c_theta', 'c_vega', 'c_rho', "c_call_put"]
put_data = example_df.loc[example_df["call_put"]=="Put", data_cols].reset_index(drop=True)
put_data.columns = ['p_strike', 'p_bid', 'p_ask', 'p_vol', 'p_delta', 'p_gamma', 'p_theta', 'p_vega', 'p_rho', "p_call_put"]
all_data = pd.concat([call_data, put_data], axis=1)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.Br(),

    html.Div(
        className="row", children=[

            html.Div(className='one columns', children=[
                dcc.Dropdown(id='my-dpdn', multi=False, value='AAPL',
                             options=[{'label': x, 'value': x}
                                      for x in ticker],
                             )], style=dict(width='30%')),

            html.Div(className='three columns', children=[

                dbc.Button('Today', id='btn-nclicks-1', outline=True, color="dark", n_clicks=0),
                dbc.Button('Week', id='btn-nclicks-2', outline=True, color="dark", n_clicks=0),
                dbc.Button('Month', id='btn-nclicks-3', outline=True, color="dark", n_clicks=0),
                dbc.Button('Year', id='btn-nclicks-4', outline=True, color="dark", n_clicks=0),
                dbc.Button('Full History', id='btn-nclicks-5', outline=True, color="dark", n_clicks=0),

            ], style=dict(width='70%')),
        ]
    ,style={'width': '95%','padding-left':'2.5%', 'padding-right':'2.5%'}),

    html.Br(),

    html.Div(
        dcc.Graph(id="graph"),
        style={'width': '95%','padding-left':'2.5%', 'padding-right':'2.5%'}
    ),

    html.Br(),
    html.Div(
    dash_table.DataTable(all_data.to_dict('records'), [{"name": i, "id": i} for i in all_data.columns]), id='tbl',
        style={'width': '95%','padding-left':'2.5%', 'padding-right':'2.5%'}),

    html.Br(),
    html.Br(),

    html.Div(
        className="row", children=[
            html.Div(className='one columns', children=[
                dcc.Dropdown(id='expiration_date', multi=False, value='2022-05-20',
                             options=[{'label': x, 'value': x}
                                      for x in expiration_date],
                             )], style=dict(width='33%')),

            html.Div(className='one columns', children=[
                dcc.Dropdown(id='call_put', multi=False, value='Put',
                             options=[{'label': x, 'value': x}
                                      for x in call_put],
                             )], style=dict(width='33%')),

            html.Div(className='one columns', children=[
                dcc.Dropdown(id='strike', multi=False, value=165.0,
                             options=[{'label': x, 'value': x}
                                      for x in strike],
                             )], style=dict(width='33%')),

    ],  style={'width': '95%','padding-left':'2.5%', 'padding-right':'2.5%'}, id="option_settings"),

    dcc.Graph(id="graph_2"),

    html.Br(),

    dcc.Graph(id="graph_3")

])

# ------------------------------------------------------------------------------
#
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output('graph', 'figure'),
    [Input('my-dpdn', 'value'),
     Input('btn-nclicks-1', 'n_clicks'),
     Input('btn-nclicks-2', 'n_clicks'),
     Input('btn-nclicks-3', 'n_clicks'),
     Input('btn-nclicks-4', 'n_clicks'),
     Input('btn-nclicks-5', 'n_clicks')]
)
def display_candlestick(ticker, n_clicks_1, n_clicks_2, n_clicks_3, n_clicks_4, n_clicks_5):

    if "btn-nclicks-1" == ctx.triggered_id:
        fig_data = yf.Ticker(ticker).history(period="1d").reset_index(level=0)
    elif "btn-nclicks-2" == ctx.triggered_id:
        fig_data = yf.Ticker(ticker).history(period="5d").reset_index(level=0)
    elif "btn-nclicks-3" == ctx.triggered_id:
        fig_data = yf.Ticker(ticker).history(period="1mo").reset_index(level=0)
    elif "btn-nclicks-4" == ctx.triggered_id:
        fig_data = yf.Ticker(ticker).history(period="1y").reset_index(level=0)
    elif "btn-nclicks-5" == ctx.triggered_id:
        fig_data = yf.Ticker(ticker).history(period="max").reset_index(level=0)
    else:
        fig_data = yf.Ticker(ticker).history(period="1y").reset_index(level=0)

    fig = go.Figure(go.Candlestick(
        x=fig_data['Date'],
        open=fig_data['Open'],
        high=fig_data['High'],
        low=fig_data['Low'],
        close=fig_data['Close']
        )
    )

    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            showline=True,
            showticklabels=False,
        ),
        autosize=True,
        margin=dict(
            autoexpand=True,
            l=10,
            r=10,
            t=10,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    return fig

@app.callback(
    Output('tbl', 'children'),
    [Input('my-dpdn', 'value')]
)

def display_table(ticker):

    select_data = option_chain[option_chain.act_symbol==ticker]

    select_data.date = pd.to_datetime(select_data.date)
    select_data.expiration = pd.to_datetime(select_data.expiration)
    example_df = select_data.loc[(select_data["expiration"] == select_data.expiration.unique()[-1]) & (select_data["date"] == select_data.date.unique()[-1]),]
    example_df["date"] = example_df["date"].dt.strftime('%Y.%m.%d')
    example_df["expiration"] = example_df["expiration"].dt.strftime('%Y.%m.%d')
    call_data = example_df.loc[example_df["call_put"] == "Call", data_cols].reset_index(drop=True)
    call_data.columns = ['c_strike', 'c_bid', 'c_ask', 'c_vol', 'c_delta', 'c_gamma', 'c_theta', 'c_vega', 'c_rho',
                         "c_call_put"]
    put_data = example_df.loc[example_df["call_put"] == "Put", data_cols].reset_index(drop=True)
    put_data.columns = ['p_strike', 'p_bid', 'p_ask', 'p_vol', 'p_delta', 'p_gamma', 'p_theta', 'p_vega', 'p_rho',
                        "p_call_put"]
    all_data = pd.concat([call_data, put_data], axis=1)
    all_data = all_data.round(decimals=3)

    table = html.Div(
        dash_table.DataTable(all_data.to_dict('records'), [{"name": i, "id": i} for i in all_data.columns],
                             style_cell={"textAlign": "center"},
                             style_header={'backgroundColor': '#6cb1ff', 'fontWeight': 'bold'}),
                             id='tbl'
    )

    return table

@app.callback(
    Output('graph_2', 'figure'),
    [Input('my-dpdn', 'value'), Input('expiration_date', 'value'),
     Input('call_put', 'value'), Input('strike', 'value')]
)
def display_candlestick(ticker, expiration_date, call_put, strike):

    select_data = option_chain[(option_chain.act_symbol==ticker) & (option_chain.expiration==expiration_date)
                               & (option_chain.call_put==call_put) & (option_chain.strike==strike)]

    fig = go.Figure(
        data=[go.Scatter(x=select_data.date, y=select_data.ask)]

    )

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )
    return fig

@app.callback(
    Output('graph_3', 'figure'),
    [Input('my-dpdn', 'value'),
     Input('call_put', 'value')]
)
def display_candlestick(ticker, call_put):

    select_data = option_chain[(option_chain.act_symbol==ticker) & (option_chain.call_put==call_put)]
    example_df = select_data.loc[(select_data["date"] == select_data.date.unique()[-1]),]

    fig = go.Figure(data=[go.Mesh3d(x=example_df.strike,
                                    y=example_df.expiration,
                                    z=example_df.ask,
                                    opacity=0.5,
                                    color='rgba(244,22,100,0.6)'
                                    )])

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )
    return fig


@app.callback(
    Output('option_settings', 'children'),
    [Input('my-dpdn', 'value')]
)

def display_dropdown(ticker):

    call_put = ['Call', 'Put']
    expiration_date = option_chain.loc[option_chain.act_symbol == ticker, "expiration"].unique()
    strike = np.sort(option_chain.loc[option_chain.act_symbol == ticker, "strike"].unique())


    result = html.Div(
        className="row", children=[
            html.Div(className='three columns', children=[
                dcc.Dropdown(id='expiration_date', multi=False, value=expiration_date[-1],
                             options=[{'label': x, 'value': x}
                                      for x in expiration_date],
                             )], style=dict(width='33%')),

            html.Div(className='three columns', children=[
                dcc.Dropdown(id='call_put', multi=False, value='Put',
                             options=[{'label': x, 'value': x}
                                      for x in call_put],
                             )], style=dict(width='33%')),

            html.Div(className='three columns', children=[
                dcc.Dropdown(id='strike', multi=False, value=strike[1],
                             options=[{'label': x, 'value': x}
                                      for x in strike],
                             )], style=dict(width='33%')),

    ],  style={'width': '95%','padding-left':'2.5%', 'padding-right':'2.5%'}, id="option_settings"),

    return result

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)