#!/usr/bin/python3.6
from flask import Flask, request, send_from_directory, render_template, send_file
from flask_cors import CORS
from flask_restful import Resource, Api
import pythonRestfulNews as prn
import requests
import json
import got3 as got
from datetime import date, datetime, timedelta
import re
import os
from generate import generate_website, generate_model

alpha_api_key = '8ZENAOK5JN09QWB1'
alpha_url = 'https://www.alphavantage.co/query'

app = Flask(__name__)

CORS(app)
api = Api(app)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)



class News(Resource):
    def get(self):
        #this should also return information about frequency

        if 'topics' in request.args:
            topics = request.args['topics']
        else:
            topics = ''

        if 'companyids' in request.args:
            companyids = request.args['companyids']
        else:
            companyids = ''

        if 'start_date' in request.args:
            start_date = request.args['start_date']
        else:
            start_date = '2018-03-01T02:22:17.308Z'

        if 'end_date' in request.args:
            end_date = request.args['end_date']
        else:
            end_date = '2018-03-25T02:22:17.308Z'

        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVhZWJiYjIxY2Q4Y2M0Mzk2YWQ1ODA1ZSIsImlhdCI6MTUyNTM5ODMwNX0.cuwdAJyYKR9_6GRMGujvqHEd58nss33ZPNB8ON82Nj4"

        url =  'http://api.restfulnews.com/search'
        auth = 'Bearer ' + token

        headers = {'content-type': 'application/json', 'authorization': auth}  

        params = {"topics": topics, "companyids": companyids, "start_date": start_date, "end_date": end_date}

        resp = requests.get(url=url, params=params, headers=headers)
        data = resp.json()
        return data

class Returns(Resource):
    def get(self):
        if 'companyid' in request.args:
            companyid = request.args['companyid']
        else:
            companyid = 'WOW.AX'
        
        alpha_api_key = '8ZENAOK5JN09QWB1'
        alpha_url = 'https://www.alphavantage.co/query'
        function = 'TIME_SERIES_DAILY'
        symbol = companyid

        params = {"function": function, "symbol": symbol, "apikey": alpha_api_key}
        resp = requests.get(url=alpha_url, params=params)
        data = resp.json()['Time Series (Daily)']

        prev = 0
        finalList =  []
        for key, value in data.items():
            final = dict()
            final['date'] = key
            if prev == 0:
                value['6. difference'] = '0'
            else:
                value['6. difference'] = float(value['4. close']) - float(prev)

            prev = value['4. close']
            #print(key, value)
            final['difference'] = value['6. difference']
            final['price'] = value['4. close']
            finalList.append(final)


        return finalList

class Twitter(Resource):
    def get(self):
        if 'topics' in request.args:
            topics = request.args['topics']
        else:
            return "must have topics"

        if 'company' in request.args:
            company = request.args['company']
        else:
            return "must have company names"
        
        if 'start_date' in request.args:
            start_date = datetime.strptime(request.args['start_date'], "%Y-%m-%d").date()
             
        else:
            return "must have start date"

        if 'end_date' in request.args:
            end_date = datetime.strptime(request.args['end_date'], "%Y-%m-%d").date()
        else:
            return "must have end date"

        data = []

        for single_date in daterange(start_date, end_date):
            record = dict()
            start = single_date.strftime("%Y-%m-%d")
            end = (single_date + timedelta(days=1)).strftime("%Y-%m-%d")
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(topics+ " " + company).setSince(start).setUntil(end).setMaxTweets(5)
            numtweets = len(got.manager.TweetManager.getTweets(tweetCriteria))
            record['date'] = start
            record['tweet count'] = numtweets
            data.append(record)

        final = dict()
        final['data'] = data

        return final

class Facebook(Resource):
    def get(self):
        url = 'http://188.166.238.3/api/v1/fbstats'
        params = {"startdate": "2018-1-1T0:0:0",
                "enddate": "2018-5-1T0:0:0",
                "instid": "wow",
                "stats": "post_message, post_created_time, post_like_count"
            }
        resp = requests.get(url=url, params=params)
        json = resp.json()
        final = []

        for post in resp.json()['Facebook Statistic Data']['posts']:
            print(post['post_created_time'])
            if re.search('plastic', (post['post_message'])):
                final.append(post)

        return final

@app.route('/website', methods=["POST"])
def website():
    #customize the website
    name = request.args['name']
    data = request.get_json(force=True)

    #need to reject website if name already taken

    generate_website(name, data)

    return "made website"

@app.route('/websitedownload')
def websitedownload():
    name = request.args['name']
    path = os.getcwd() + "/" + name + '.zip'

    #check this path actually exists

    return send_file(path)

@app.route('/websiteview')
def websiteview():
    name = request.args['name']
    return render_template(name +'.html')


@app.route('/datarobot', methods=["POST"])
def datarobot():
    name = request.args['name']
    data = request.get_json(force=True)

    #need to reject model if name already taken

    generate_model(name, data)

    return "model made"


#need to add all of our api resources here (note the website one is a flask route as it needs the send_file function):
api.add_resource(News, '/news')
api.add_resource(Returns, '/returns')
api.add_resource(Twitter, '/twitter')
api.add_resource(Facebook, '/facebook')

if __name__ == '__main__':
    app.run(debug=True)