import pandas as pd


company_returns = pd.read_json('temp.json')
twitter_values = pd.read_json('twitter.json')
company_twitter = company_returns.merge(twitter_values, on="date")
company_twitter = company_twitter[['difference', 'price', 'tweets']]
company_twitter.rename(columns={'price': 'target'}, inplace=True)
print(company_twitter)
company_twitter.to_csv('test.csv', index=False)