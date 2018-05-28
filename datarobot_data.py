from datetime import date, datetime, timedelta
import json
import requests
import time
from classes.twitter import daterange, get_num_tweets
import pandas as pd
from pymongo import MongoClient
import datarobot as dr

api_key = "apuu5rs3mpuIbAGGbadkMOQicY5btndS"
dr.Client(token=api_key, endpoint='https://app.datarobot.com/api/v2')

def build_model_data(name, topics, companyid, companyname):
    client = MongoClient('localhost', 27017)
    db = client.restfulnews
    tweetdb = db.tweets
    end_date = date.today()
    start_date = end_date - timedelta(days=200)
    time1 = time.time()
    tweet_data = []

    for single_date in daterange(start_date, end_date):
        record = dict()
        start = single_date.strftime("%Y-%m-%d")
        end = (single_date + timedelta(days=1)).strftime("%Y-%m-%d")

        filter_ = {
            'start': start,
            'company': companyname,
            'topics' : topics
        }
        tweets = tweetdb.find_one(filter_)
        print(tweets)

        if tweets == None:
            numtweets = get_num_tweets(start, end, (topics + " " + companyname))
            newtweet = {
                'start': start,
                'company' : companyname, 
                'topics' : topics,
                'numtweets' : numtweets
            }
            tweetdb.insert_one(newtweet)
        else:
            numtweets = tweets['numtweets']
        
        record['date'] = start
        record['tweet count'] = numtweets
        tweet_data.append(record)

    time2 = time.time()

    tweet_json = ""
    tweet_json +=('[\n')
    i = 0
    for line in tweet_data:
        if i == len(tweet_data) - 1:
            tweet_json +=(json.dumps(line) + "\n")
        else:
            tweet_json +=(json.dumps(line) + ",\n")
        i += 1
    tweet_json +=(']\n')

    print('function took %0.3f ms' % (time2-time1))

    alpha_api_key = '8ZENAOK5JN09QWB1'
    alpha_url = 'https://www.alphavantage.co/query'
    function = 'TIME_SERIES_DAILY_ADJUSTED'
    symbol = companyid

    params = {"function": function, "symbol": symbol, "apikey": alpha_api_key, "outputsize" :"full" }
    resp = requests.get(url=alpha_url, params=params)
    data = resp.json()['Time Series (Daily)']

    returns_data =  []
    for key, value in data.items():
        final = dict()
        final['date'] = key
        final['price'] = value['4. close']
        keydate = datetime.strptime(key, "%Y-%m-%d").date()
        if start_date <= keydate <= end_date:
            returns_data.append(final)

    returns_json = ""

    returns_json +=('[\n')
    i = 0
    for line in returns_data:
        if i == len(returns_data) - 1:
            returns_json +=(json.dumps(line) + "\n")
        else:
            returns_json +=(json.dumps(line) + ",\n")
        i += 1
    returns_json +=(']\n')

    company_returns = pd.read_json(returns_json)
    twitter_values = pd.read_json(tweet_json)
    combined = company_returns.merge(twitter_values, on="date")
    combined['prev'] = combined.price.shift(1)
    combined.rename(columns={'price': 'target'}, inplace=True)
    combined = combined.dropna()
    combined.to_csv('data/' + name + '.csv', index=False)

    return combined

def get_models_from_project(projectid):

    project = dr.Project.get(projectid)
    models = project.get_models()

    processed_models = []
    parameters = []
    for model in models:
        print(model.metrics['RMSE']['validation'])
        if parameters == []:
            parameters = model.get_features_used()
        processed_model = {'model name': model.model_type, 'score' : model.metrics['RMSE']['validation'], 'model id' : model.id, 'model parameters' : parameters}
        processed_models.append(processed_model)

    return processed_models