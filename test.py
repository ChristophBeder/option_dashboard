import yfinance as yf
import pandas as pd
import datetime as dt

#msft = yf.Ticker("MSFT")
#print(msft.info.keys())
#df = pd.DataFrame({'Parameter': msft.info.keys(), 'Value': msft.info.values()})
#
#keys and values
#print(df)
#print(msft.options)
#print(msft.option_chain('2022-01-21')[0])

data = pd.read_csv("option_chain.csv")
data.expiration = pd.to_datetime(data.expiration)
data.date = pd.to_datetime(data.date)
year = dt.datetime(2022, 5, 1)
print(year)

example_df = data.loc[(data["act_symbol"]=="AAPL") & (data["expiration"] >year) & (data["date"]==data.date.unique()[-1]),]
print(example_df)
#print(example_df.date.unique()[-1])