import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Output, Input
from dash import dash_table
import yfinance as yf
import sqlite3

conn = sqlite3.connect('C:/Users/Chris/PycharmProjects/Dash-Project/option_data.db', check_same_thread=False)

ticker = pd.read_sql_query('SELECT distinct act_symbol FROM option_chain', con=conn)
expiration_date = pd.read_sql_query('SELECT distinct expiration FROM option_chain', con=conn)
call_put = ['Call', 'Put']
strike = pd.read_sql_query('SELECT distinct strike FROM option_chain', con=conn)

nasdaq_listed_url = "ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt"
nasdaq_listed_data = pd.read_csv(nasdaq_listed_url,  delimiter="|")
nasdaq_listed_data = nasdaq_listed_data.loc[nasdaq_listed_data["Test Issue"] == "N"]
nasdaq_listed_data = nasdaq_listed_data.loc[nasdaq_listed_data["Financial Status"] == "N"]
nasdaq_listed_symbols = nasdaq_listed_data['Symbol'].drop(nasdaq_listed_data.iloc[-1:, :].index, axis=0)
tickers = nasdaq_listed_symbols.to_list()

msft = yf.Ticker("AAPL")
df = pd.DataFrame({'Parameter': msft.info.keys(), 'Value': msft.info.values()})


app = Dash(__name__)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    dcc.Checklist(
        id='toggle-rangeslider',
        options=[{'label': 'Include Rangeslider',
                  'value': 'slider'}],
        value=['slider']
    ),
    dcc.Dropdown(id='my-dpdn', multi=False, value='AAPL',
                         options=[{'label':x, 'value':x}
                                  for x in ticker.act_symbol],
                         ),
    dcc.Graph(id="graph"),
    html.Div([
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )
    ], id='table'),

    html.Br(),

    html.Div(
        className="row", children=[
            html.Div(className='three columns', children=[
                dcc.Dropdown(id='expiration_date', multi=False, value='2022-05-20',
                             options=[{'label': x, 'value': x}
                                      for x in expiration_date.expiration],
                             )], style=dict(width='50%')),

            html.Div(className='three columns', children=[
                dcc.Dropdown(id='call_put', multi=False, value='Put',
                             options=[{'label': x, 'value': x}
                                      for x in call_put],
                             )], style=dict(width='50%')),

            html.Div(className='three columns', children=[
                dcc.Dropdown(id='strike', multi=False, value=110.0,
                             options=[{'label': x, 'value': x}
                                      for x in strike.strike],
                             )], style=dict(width='50%')),

    ],  style=dict(display='flex'), id="option_settings"),

    dcc.Graph(id="graph_2")

])

# ------------------------------------------------------------------------------
#
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output('graph', 'figure'),
    Output('table', 'children'),
    [Input('my-dpdn', 'value'),
     Input('toggle-rangeslider', 'value')]
)
def display_candlestick(ticker, value):

    input_value = ticker
    stock = yf.Ticker(input_value)
    hist = stock.history(period="max")
    hist = hist.reset_index(drop=False)
    info_df = pd.DataFrame({'Parameter': stock.info.keys(), 'Value': stock.info.values()})

    fig = go.Figure(go.Candlestick(
        x=hist['Date'],
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close']
    ))

    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value
    )

    table = html.Div([
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in info_df.columns],
        data=info_df.to_dict('records'),
    )], id='table')

    return fig, table

@app.callback(
    Output('graph_2', 'figure'),
    [Input('my-dpdn', 'value'), Input('expiration_date', 'value'),
     Input('call_put', 'value'), Input('strike', 'value')]
)
def display_candlestick(ticker, expiration_date, call_put, strike):

    #select_data = data.loc[(data.act_symbol == ticker) & (data.expiration == expiration_date)
    #                       & (data.call_put == call_put) & (data.strike == strike), ]
    #select_data = pd.read_sql_query('SELECT * FROM option_chain WHERE act_symbol=ticker AND WHERE expiration=expiration_date AND WHERE call_put=call_put AND WHERE strike=strike', con=conn)
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
                             )], style=dict(width='50%')),

            html.Div(className='three columns', children=[
                dcc.Dropdown(id='call_put', multi=False, value='Put',
                             options=[{'label': x, 'value': x}
                                      for x in call_put],
                             )], style=dict(width='50%')),

            html.Div(className='three columns', children=[
                dcc.Dropdown(id='strike', multi=False, value=110.0,
                             options=[{'label': x, 'value': x}
                                      for x in select_data.strike],
                             )], style=dict(width='50%')),

    ],  style=dict(display='flex'), id="option_settings"),

    return result

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)