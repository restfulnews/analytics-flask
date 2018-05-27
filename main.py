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
from datarobot_data import build_model_data

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
client = MongoClient('localhost', 27017)    #Configure the connection to the database
db = client.restfulnews    #Select the database
users = db.users #Select the collection


#create the flask app and enable it to be an api
app = Flask(__name__)

api = Api(app)
CORS(app)


@app.route('/userdetails')
def userdetails():
    #need to also do a request to the node backend so we get the right stuff


    user = request.args['user']

    filter_ = {
        'name': user,
    }

    userDB = users.find_one(filter_)

    if userDB == None:
        return "no user"
    else:
        return str(userDB)


@app.route('/website', methods=["POST"])
def website():
    #customize the website
    name = request.args['name']
    user = request.args['user']
    data = request.get_json(force=True)

    #need to reject website if name already taken

    generate_website(name, data)

    #need to add the website to the associated user
    filter_ = {
        'name': user,
    }
    update =  {
        '$push': {
            'websites': name
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
    name = request.args['name']
    topics = request.args['topics']
    companyid = request.args['companyid']
    companyname = request.args['companyname']

    data = build_model_data(name, topics, companyid, companyname)
    projectid = generate_model(name, 'data/hello.csv')
    
    filter_ = {
        'name': name,
    }
    update =  {
        '$push': {
            'projects': projectid
        }
    }
    users.update_one(filter_, update, upsert=True)
    
    return "models started"

@app.route('/models')
def models():
    return "hello"




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
