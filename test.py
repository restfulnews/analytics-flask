import pandas as pd


company_returns = pd.read_json('returns.txt')
twitter_values = pd.read_json('tweet.txt')
combined = company_returns.merge(twitter_values, on="date")
combined['prev'] = combined.price.shift(1)
combined.rename(columns={'price': 'target'}, inplace=True)
combined = combined.dropna()
print(combined)
