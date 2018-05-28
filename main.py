#!/usr/bin/python3.6
#import the main other libraries that we need
from flask import Flask, request, send_from_directory, render_template, send_file
from flask_cors import CORS
from flask_restful import Resource, Api
import os
import pandas as pd
import re
from pymongo import MongoClient # Database connector
#from bson.objectid import ObjectId # For ObjectId to work
import bcrypt
from datetime import date, datetime, timedelta
import json
import requests
import time
from datarobot_data import build_model_data, get_models_from_project
import datarobot as dr
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer

#these are functions required to do some
from generate import generate_website, generate_model

#these are our classes for the different main routes
from classes.news import News
from classes.returns import Returns
from classes.twitter import Twitter, get_num_tweets, daterange
from classes.facebook import Facebook
from classes.text import Text
from classes.email import Email

#connect to the database
client = MongoClient('localhost', 27017)
db = client.restfulnews
users = db.users

#setup datarobot things
api_key = "apuu5rs3mpuIbAGGbadkMOQicY5btndS"
dr.Client(token=api_key, endpoint='https://app.datarobot.com/api/v2')
#pre-train sentiment analyser
tb = Blobber(analyzer=NaiveBayesAnalyzer())

#create the flask app and enable it to be an api
app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route('/userdetails')
def userdetails():
    user = request.args['user']
    filter_ = {
        'name': user,
    }
    userDB = users.find_one(filter_)

    if userDB == None:
        print("no user")
        return "no user"
    else:
        if "projects" not in userDB:
            userDB['projects'] = []
        else:
            for project in userDB['projects']:
                models = get_models_from_project(project['projectid'])
                project['models'] = models

        if "websites" not in userDB:
            userDB['websites'] = []

        userDB = {"websites" : userDB['websites'], "projects" : userDB['projects']}

        return json.dumps(userDB)


@app.route('/website', methods=["POST"])
def website():
    #customize the website
    name = request.args['name']
    user = request.args['user']
    data = request.get_json(force=True)
    generate_website(name, data, tb)

    #need to add the website to the associated user
    filter_ = {
        'name': user
    }
    update =  {
        '$push': {
            'websites': {'name' : name, 'route' : 'http://analytics.api.restfulnew.com/websiteview?name=' + name}
        }
    }
    users.update_one(filter_, update, upsert=True)

    return "made website"

#http://localhost:5000/websitedownload?name=test
@app.route('/websitedownload')
def websitedownload():
    name = request.args['name']
    path = os.getcwd() + "/" + name + '.zip'

    #check this path actually exists
    if os.path.exists(path):
        return send_file(path)
    else:
        return "the website does not exist"

#http://localhost:5000/websiteview?name=test
@app.route('/websiteview')
def websiteview():
    name = request.args['name']
    path = os.getcwd() + '/templates/' + name + '.html'

    if os.path.exists(path):
        return render_template(name +'.html')
    else:
        return "the website does not exist"

#localhost:5000/datarobot?name=hello&companyid=wow&companyname=woolworths&topics=plastic bags
@app.route('/datarobot')
def datarobot():
    user = request.args['user']
    name = request.args['name']
    topics = request.args['topics']
    companyid = request.args['companyid']
    companyname = request.args['companyname']

    data = build_model_data(name, topics, companyid, companyname)
    #projectid = generate_model(name, 'data/hello.csv')
    projectid = generate_model(name, data)
    filter_ = {
        'name': user,
    }
    update =  {
        '$push': {
            'projects': {"projectid" : projectid, 'name' : name, 'companyname' : companyname, 'topics' : topics }
        }
    }
    users.update_one(filter_, update, upsert=True)

    return "models started"

@app.route('/predict', methods=['POST'])
def deploy():
    modelid = request.args['modelid']
    projectid = request.args['projectid']
    data = request.get_json(force=True)
   
    with open('data_to_predict.csv', 'w') as f:
        i = 0
        for key, value in (data).items():
            if i == 0:
                f.write(key)
            else:
                f.write("," + key)
            i += 1
        i = 0
        f.write("\n")
        for key, value in (data).items():
            if i == 0:
                f.write(str(value))
            else:
                f.write("," + str(value))
            i += 1

    project = dr.Project.get(projectid)
    model = dr.Model.get(project=projectid,
                        model_id=modelid)

    dataset_from_path = project.upload_dataset('data_to_predict.csv')
    predict_job = model.request_predictions(dataset_from_path.id)
    print("predict job started")
    predictions = predict_job.get_result_when_complete()
    prediction = (predictions['prediction'].iloc[0])

    return json.dumps({'prediction' : prediction})

@app.route('/correlation', methods=["POST"])
def correlation():
    data = request.get_json(force=True)

    newData = str(data)
    newData = re.sub("'", "\"", newData)
    tempJson = "temp.json"

    with open(tempJson, 'w') as f:
        f.write(str(newData))

    df = pd.read_json(tempJson)

    correlation = df['stock'].corr(df['tweet'])

    return str(correlation)

#need to add all of our api resources here
api.add_resource(News, '/news')
api.add_resource(Returns, '/returns')
api.add_resource(Twitter, '/twitter')
api.add_resource(Facebook, '/facebook')
api.add_resource(Text, '/text')
api.add_resource(Email, '/email')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
