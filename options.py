import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect('C:/Users/Chris/PycharmProjects/Dash-Project/option_data.db')
c = conn.cursor()
symbol = '\'A\''
expiration = '\'2022-05-20\''
call_put = '\'Put\''
strike = '\'110.0\''

select_data = pd.read_sql_query(
    'SELECT * FROM option_chain WHERE act_symbol=' + symbol + ' AND expiration=' + expiration +
    ' AND call_put=' + call_put + ' AND strike=' + strike,
    con=conn)

print(select_data)


#data = pd.read_csv("option_chain.csv")
#print(data)
#data.to_sql("option_chain", con=conn, index=False, if_exists='replace', chunksize=1000000)
#select_data = data.loc[(data.act_symbol == "A") & (data.expiration == "2022-05-20") & (data.call_put == "Put") &
#                       (data.strike == 110.0), ]
#print(select_data)
#select_data.plot(x="date", y="ask", kind='line')
#plt.show()

#strike
#expiration
#1886 unique symbols
#

dcc.Dropdown(id='expiration_date', multi=False, value='2022-05-20',
             options=[{'label': x, 'value': x}
                      for x in expiration_date.expiration],
             ),
dcc.Dropdown(id='call_put', multi=False, value='Put',
             options=[{'label': x, 'value': x}
                      for x in call_put],
             ),
dcc.Dropdown(id='strike', multi=False, value=110.0,
             options=[{'label': x, 'value': x}
                      for x in strike.strike],
             ),
