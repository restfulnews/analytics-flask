from flask_restful import Resource, Api
from flask import Flask, request, send_from_directory, render_template, send_file
import requests


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