from app import app
from flask import render_template, redirect, flash, session
import sys
import sqlite3 as lite
import os
from flask import request
from flask import Flask
import json

import requests
import oauth2 as oauth


def get_git_repos(username):
	new = []
	response = requests.get('https://api.github.com/users/'+username+'/repos')
	if response.status_code != 200:
		return new
	else:
		for repo in response.json():
			r = format(repo['name'])
			l = format(repo['language'])
			com = [r,l]
			new.append(com)
		return new

CONSUMER_KEY = "cwUsz3slwPi9RuIP3U0hT5quQ"
CONSUMER_SECRET = "BgZd2QUevhcPjDXYzx87F3yFht7UYSNQqrFWwi76zZwM4HoH9p"
ACCESS_KEY = "3014167189-nhD1oedU6bFeLK41TGhKMvdapPSbfwjqzx2W72q"
ACCESS_SECRET = "i8ryrRgaf8RUPXSPBpuYegGESsgAjcYFKVk0wkxNaI9ix"

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

def get_tweets(username):
	count = '5'
	twt = []
	timeline_endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="+username+"&count="+count
	response, data = client.request(timeline_endpoint)

	tweets = json.loads(data)
	for tweet in tweets:
		twt.append(tweet['text'])
	return twt


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/get_git')
def get_git():
	return render_template('get_git.html')

@app.route('/process_git', methods=['POST', 'GET'])
def procee_git():
	git_id = request.form['git_id']

	if git_id == '':
		return redirect('/get_git')
	
	repos = get_git_repos(git_id)
	if len(repos) == 0:
		return '''
		<html>
			<head>
			<title>Error</title>
			</head>
			<body>
				<center>
				<h3>Error</h3>
				</center>
			</body>
		</html> '''
	else:
		return render_template('git.html', repos=repos)

@app.route('/get_twitter')
def get_twitter():
	return render_template('get_twitter.html')

@app.route('/process_twitter', methods=['POST', 'GET'])
def process_twitter():
	twitter_id = request.form['twitter_id']

	if twitter_id == '':
		return redirect('/get_twitter')
	tweets = get_tweets(twitter_id)	
	return render_template('twitter.html', tweets=tweets)
