#!/usr/bin/python3.6
#import the main other libraries that we need
from flask import Flask, request, send_from_directory, render_template, send_file
from flask_cors import CORS
from flask_restful import Resource, Api
import os
import pandas as pd
import re

#these are functions required to do some
from generate import generate_website, generate_model

#these are our classes for the different main routes
from classes.news import News
from classes.returns import Returns
from classes.twitter import Twitter
from classes.facebook import Facebook
from classes.text import Text
from classes.email import Email

alpha_api_key = '8ZENAOK5JN09QWB1'
alpha_url = 'https://www.alphavantage.co/query'

#create the flask app and enable it to be an api
app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route('/website', methods=["POST"])
def website():
    #customize the website
    name = request.args['name']
    data = request.get_json(force=True)

    #need to reject website if name already taken

    generate_website(name, data)

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

@app.route('/datarobot', methods=["POST"])
def datarobot():
    name = request.args['name']
    data = request.get_json(force=True)

    #need to reject model if name already taken

    generate_model(name, data)

    return "model made"

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
