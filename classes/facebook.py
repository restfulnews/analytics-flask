from flask_restful import Resource, Api
from flask import Flask, request, send_from_directory, render_template, send_file
import requests
import re

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