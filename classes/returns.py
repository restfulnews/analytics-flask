from flask_restful import Resource, Api
from flask import Flask, request, send_from_directory, render_template, send_file
import requests


class Returns(Resource):
    def get(self):
        if 'companyid' in request.args:
            companyid = request.args['companyid']
            companyid = companyid.split('.')[0]
        else:
            companyid = 'WOW.AX'

        if 'start_date' in request.args:
            start_date =request.args['start_date']

        alpha_api_key = '8ZENAOK5JN09QWB1'
        alpha_url = 'https://www.alphavantage.co/query'
        function = 'TIME_SERIES_DAILY_ADJUSTED'
        symbol = companyid

        params = {"function": function, "symbol": symbol, "apikey": alpha_api_key}
        resp = requests.get(url=alpha_url, params=params)
        data = resp.json()['Time Series (Daily)']
        print(data)

        finalList =  []
        for key, value in data.items():
            final = dict()
            final['date'] = key
            final['price'] = value['4. close']
            finalList.append(final)

        #sort the final list
        finalList = sorted(finalList, key=lambda k: k['date'])

        return finalList