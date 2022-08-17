import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from dash import dash_table
import sqlite3
import datetime as dt

conn = sqlite3.connect('C:/Users/Chris/PycharmProjects/Dash-Project/option_data.db', check_same_thread=False)


ticker = pd.read_sql_query('SELECT distinct act_symbol FROM option_chain', con=conn)
expiration_date = pd.read_sql_query('SELECT distinct expiration FROM option_chain', con=conn)
call_put = ['Call', 'Put']
strike = pd.read_sql_query('SELECT distinct strike FROM option_chain', con=conn)
stock_prices = pd.read_csv("stock_prices.csv")


symbol = '\'' + "AAPL" + '\''
expiration = '\'' + "2022-05-20" + '\''

select_data = pd.read_sql_query(
    'SELECT * FROM option_chain WHERE act_symbol=' + symbol + ' AND expiration=' + expiration,
    con=conn)

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
        dcc.Checklist(
            id='toggle-rangeslider',
            options=[{'label': 'Include Rangeslider',
                      'value': 'slider'}],
            value=['slider']
        ), style={'width': '95%','padding-left':'2.5%', 'padding-right':'2.5%'}
    ),


    html.Div(
        dcc.Dropdown(id='my-dpdn', multi=False, value='AAPL',
                     options=[{'label': x, 'value': x}
                              for x in ticker.act_symbol],
                     ) , style={'width': '95%','padding-left':'2.5%', 'padding-right':'2.5%'}
    ),

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
                                      for x in expiration_date.expiration],
                             )], style=dict(width='33%')),

            html.Div(className='one columns', children=[
                dcc.Dropdown(id='call_put', multi=False, value='Put',
                             options=[{'label': x, 'value': x}
                                      for x in call_put],
                             )], style=dict(width='33%')),

            html.Div(className='one columns', children=[
                dcc.Dropdown(id='strike', multi=False, value=165.0,
                             options=[{'label': x, 'value': x}
                                      for x in strike.strike],
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
     Input('toggle-rangeslider', 'value')]
)
def display_candlestick(ticker, value):


    fig_data = stock_prices.loc[stock_prices["act_symbol"] == str(ticker), ]
    fig_data = fig_data.reset_index(drop=False)

    fig = go.Figure(go.Candlestick(
        x=fig_data['date'],
        open=fig_data['open'],
        high=fig_data['high'],
        low=fig_data['low'],
        close=fig_data['close']
    )
    )
    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value
    )
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

    symbol = '\'' + str(ticker) + '\''
    #call_put = '\'' + str(call_put) + '\''

    select_data = pd.read_sql_query(
        'SELECT * FROM option_chain WHERE act_symbol=' + symbol,
        con=conn)

    select_data.date = pd.to_datetime(select_data.date)
    select_data.expiration = pd.to_datetime(select_data.expiration)
    year = dt.datetime(2022, 5, 1)
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

    symbol = '\'' + str(ticker) + '\''
    expiration = '\'' + str(expiration_date) + '\''
    call_put = '\'' + str(call_put) + '\''
    strike = '\'' + str(strike) + '\''


    select_data = pd.read_sql_query(
        'SELECT * FROM option_chain WHERE act_symbol=' + symbol + ' AND expiration=' + expiration +
        ' AND call_put=' + call_put + ' AND strike=' + strike,
        con=conn)
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
    [Input('my-dpdn', 'value'), Input('expiration_date', 'value'),
     Input('call_put', 'value'), Input('strike', 'value')]
)
def display_candlestick(ticker, expiration_date, call_put, strike):

    symbol = '\'' + str(ticker) + '\''
    expiration = '\'' + str(expiration_date) + '\''
    call_put = '\'' + str(call_put) + '\''
    strike = '\'' + str(strike) + '\''


    select_data = pd.read_sql_query(
        'SELECT * FROM option_chain WHERE act_symbol=' + symbol +
        ' AND call_put=' + call_put,
        con=conn)

    example_df = select_data.loc[(select_data["date"] == select_data.date.unique()[-1]),]

    #fig = go.Figure(
    #    data=[go.Scatter(x=example_df.strike, y=example_df.ask)])

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
    symbol = '\'' + str(ticker) + '\''
    call_put = ['Call', 'Put']

    select_data = pd.read_sql_query(
        'SELECT * FROM option_chain WHERE act_symbol=' + symbol,
        con=conn)

    result = html.Div(
        className="row", children=[
            html.Div(className='three columns', children=[
                dcc.Dropdown(id='expiration_date', multi=False, value='2022-05-20',
                             options=[{'label': x, 'value': x}
                                      for x in select_data.expiration],
                             )], style=dict(width='33%')),

            html.Div(className='three columns', children=[
                dcc.Dropdown(id='call_put', multi=False, value='Put',
                             options=[{'label': x, 'value': x}
                                      for x in call_put],
                             )], style=dict(width='33%')),

            html.Div(className='three columns', children=[
                dcc.Dropdown(id='strike', multi=False, value=110.0,
                             options=[{'label': x, 'value': x}
                                      for x in select_data.strike],
                             )], style=dict(width='33%')),

    ],  style={'width': '95%','padding-left':'2.5%', 'padding-right':'2.5%'}, id="option_settings"),

    return result

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)