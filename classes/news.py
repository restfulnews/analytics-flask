from flask_restful import Resource, Api
from flask import Flask, request, send_from_directory, render_template, send_file
import requests


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