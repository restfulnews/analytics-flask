#!/usr/bin/python3.6
from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS
from flask_restful import Resource, Api
import pythonRestfulNews as prn
import requests
import json
import dominate
from dominate.tags import *

alpha_api_key = '8ZENAOK5JN09QWB1'
alpha_url = 'https://www.alphavantage.co/query'

app = Flask(__name__)

CORS(app)
api = Api(app)

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
        for key, value in data.items():
            if prev == 0:
                value['6. difference'] = '0'
            else:
                value['6. difference'] = float(value['4. close']) - float(prev)

            prev = value['4. close']
            print(key, value)

        return data



@app.route('/website')
def trial():
    if 'title' in request.args:
        title = request.args['title']
    else:
        title = 'Awesome Website'

    return render_template('basic.html', title=title)

api.add_resource(News, '/news')
api.add_resource(Returns, '/returns')
#the other route is the app.route website which uses jinja 2 to render basic html with other stuff



if __name__ == '__main__':
    app.run(debug=True)