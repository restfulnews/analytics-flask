from flask_restful import Resource, Api
from flask import Flask, request, send_from_directory, render_template, send_file
import requests
import re


#http://localhost:5000/facebook?companyid=wow.ax
class Facebook(Resource):
    def get(self):
        company = request.args['companyid'].split('.')[0]


        url = 'http://188.166.238.3/api/v1/fbstats'
        params = {"startdate": "2018-1-1T0:0:0",
                "enddate": "2018-5-1T0:0:0",
                "instid": company,
                "stats": "id, name, website, description ,category, fan_count"
            }
        resp = requests.get(url=url, params=params)
        json = resp.json()
        final = json['Facebook Statistic Data']
        '''
        final = []

        for post in resp.json()['Facebook Statistic Data']['posts']:
            print(post['post_created_time'])
            if re.search('plastic', (post['post_message'])):
                final.append(post)
        '''

        return final