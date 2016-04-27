#!/usr/bin/env python

import praw
import os
import ConfigParser
import requests
import time
import datetime
import traceback
import re
from furl import furl
from os.path import sys
from time import sleep
from urlparse import urlparse

def main():
	print('Mnemosyne reborn by /u/ITSigno and chugga_fan (for autoconfiguration)')

	# verify that the config file exists
	if not os.path.exists('mnemosyne.cfg'):
		print('No config file')
		sys.exit()

	# parse the config file
	config = ConfigParser.ConfigParser()
	config.read('mnemosyne.cfg')

	# get the basic info for the bot user
	USERNAME = config.get('Bot', 'username')
	PASSWORD = config.get('Bot', 'password')
	USERAGENT = config.get('Bot', 'useragent')

	# Get our reddit settings
	SUBREDDIT = config.get('Reddit', 'subreddit')
	REQ_LIMIT = config.get('Reddit', 'request_limit')

	# other misc. config options
	SUBMIT_URL = config.get('Config', 'submit_url')
	SLEEP_TIME = config.getint('Config', 'sleep_time')

	# TODO make the exclude system friendlier
	# Note, the excluded terms still need to have periods escaped
	EXCLUDE = config.get('Config', 'exclude')
	EXCLUDE = re.compile("|".join(EXCLUDE.split(',\s?')))

	# Login to reddit
	# TODO setup OAuth method
	r = praw.Reddit(USERAGENT)
	r.login(USERNAME,PASSWORD, disable_warning=True)

	# get our designated sub
	s = r.get_subreddit(SUBREDDIT);

	# based on legacy message header
	d_head = "Archive links for this discussion: \n\n"
	p_head = "Archive links for this post: \n\n"

	# BotLivesMatter
	foot = "----\n\nI am Mnemosyne reborn. This space for rent. ^^^/r/botsrights"

	# initialize our array of "already_done" posts, so we don't repeat work
	if not os.path.exists('replied_to.txt'):
		already_done = []
	else:
		with open('replied_to.txt', "r") as f:
			already_done = f.read()
			already_done = already_done.split("\n")
			already_done = filter(None, already_done)

	# loop forever and ever and ever and ever and ever and ever
	while True:
		try:
			# loop over every post returned by get_new
			# p is a Submission object
			for p in s.get_new(limit=REQ_LIMIT):
				#verify that the the post isn't already done...
				if p.id not in already_done:
					# Add the post id to the current array and the file
					already_done.append(p.id)
					with open('replied_to.txt', 'a') as f:
						f.write(p.id + "\n")

					# parse the url, get the domain, and run our exlude regex
					parsed_uri = urlparse(p.url)
					if EXCLUDE.search(parsed_uri.netloc) is not None:
						continue

					# add the timestamp parameter to the post's url, and submit to archive.is
					req = requests.post(SUBMIT_URL, data={'url':furl(p.url).add({ 'ar': str(time.time())})})

					# grab the headers
					loc = req.headers.get('location')
					ref = req.headers.get('refresh')

					# if the url has been archived before, archive.is returns a location header. If it's new, it sends a refresh header
					url = ''
					if ref:
						url = re.sub(r'^\d+;url=','', ref) 
					elif loc:
						url = loc
					
					if not url:
						continue #failed to get url

					# use the right head based on post type
					head = d_head if p.is_self else p_head

					c = head + "* **Archive:** " + url + "\n\n" + foot
					p.add_comment(c)
					# done
						
			sleep(SLEEP_TIME)
		except Exception as e:
			now = datetime.datetime.now()
			with open('error_log.txt', 'a') as f:
				f.write(now.strftime("%m-%d-%Y %H:%M"))
				f.write(traceback.format_exc())
				f.write('ERROR: ' + str(e))
				f.write('Going to sleep...\n')
			sleep(SLEEP_TIME)
			continue
			
			
main()
