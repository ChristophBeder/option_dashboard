# Rewrite csv to parquet
#df = pd.read_csv('volatility_history.csv')
#df.to_parquet('volatility_history.parquet')
#option_chain = pd.read_parquet("option_chain.parquet")
#print(option_chain.expiration.unique())




# Manually download file
#import requests
#local_file = 'option_test.csv'
#res = requests.get('https://www.dolthub.com/csv/post-no-preference/options/1brvscel97j3tef5mkrfticvp7ebks2c/option_chain')
#with open(local_file, 'wb') as file:
#  file.write(res.content)
