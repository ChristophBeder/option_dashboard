import yfinance as yf
import pandas as pd

msft = yf.Ticker("MSFT")
#print(msft.info.keys())
#df = pd.DataFrame({'Parameter': msft.info.keys(), 'Value': msft.info.values()})
#
#keys and values
#print(df)
print(msft.options)
print(msft.option_chain('2022-01-21')[0])