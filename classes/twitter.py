from datetime import date, datetime, timedelta
from flask_restful import Resource, Api
from flask import Flask, request, send_from_directory, render_template, send_file
import requests
import got3 as got
import re
import random
from bs4 import BeautifulSoup


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)



#http://localhost:5000/twitter?topics=plastic%20bags&company=woolworths&start_date=2018-02-07&end_date=2018-02-15
class Twitter(Resource):
    def get(self):
        if 'topics' in request.args:
            topics = request.args['topics']
        else:
            return "must have topics"

        if 'company' in request.args:
            company = request.args['company']
        else:
            return "must have company names"

        if 'start_date' in request.args:
            start_date = datetime.strptime(request.args['start_date'], "%Y-%m-%d").date()

        else:
            return "must have start date"

        if 'end_date' in request.args:
            end_date = datetime.strptime(request.args['end_date'], "%Y-%m-%d").date()
        else:
            return "must have end date"

        topics = topics.replace(',', ' ')

        data = []

        for single_date in daterange(start_date, end_date):
            record = dict()
            start = single_date.strftime("%Y-%m-%d")
            end = (single_date + timedelta(days=1)).strftime("%Y-%m-%d")
            #tweetCriteria = got.manager.TweetCriteria().setQuerySearch(topics+ " " + company).setSince(start).setUntil(end).setMaxTweets(5)
            #numtweets = len(got.manager.TweetManager.getTweets(tweetCriteria))
            #print(numtweets)
            numtweets = get_num_tweets(start, end, (topics + " " + company))
            record['date'] = start
            record['tweet count'] = numtweets
            data.append(record)

        final = dict()
        final['data'] = data

        return final


def get_num_tweets(since, until, terms):
    url = "https://twitter.com/search?q= since:"+since+" until:"+until+" "+terms+"&src=typd"

    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })

    reddit1Link = requests.get(url, headers=headers)
    reddit1Content = BeautifulSoup(reddit1Link.content,"lxml")
    myspan = reddit1Content.findAll("span", {"class": "ProfileTweet-actionCountForAria"})

    count = 0
    for span in myspan:
        if re.search("replies", str(span)):
            count += 1
            

    return count