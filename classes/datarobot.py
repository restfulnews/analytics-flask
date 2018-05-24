from flask_restful import Resource, Api
from flask import Flask, request, send_from_directory, render_template, send_file
import requests
from twitter import get_num_tweets

class DataRobot(Resource):
    def get(self):
        #this should also return information about frequency
        name = request.args['name']
        topics = request.args['topics']
        companyid = request.args['companyids']


        for single_date in daterange(start_date, end_date):
            record = dict()
            start = single_date.strftime("%Y-%m-%d")
            end = (single_date + timedelta(days=1)).strftime("%Y-%m-%d")
            numtweets = get_num_tweets(start, end, (topics + " " + company))
            record['date'] = start
            record['tweet count'] = numtweets
            data.append(record)


        filter_ = {
            'name': user,
        }
        update =  {
            '$push': {
                'models': modelid
            }
        }
        users.update_one(filter_, update, upsert=True)


        return "model"