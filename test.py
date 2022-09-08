import pandas as pd
import datetime as dt

#import requests
#owner, repo, branch = 'post-no-preference', 'options', 'master'
#query = '''SELECT * FROM `option_chain` ORDER BY `date` ASC, `act_symbol` ASC, `expiration` ASC, `strike` ASC, `call_put` ASC LIMIT 200; '''
#res = requests.get('https://www.dolthub.com/api/v1alpha1/{}/{}/{}'.format(owner, repo, branch), params={'q': query})
#print(res.json())
#data = res.json()
#print(pd.DataFrame(data["rows"]))


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
