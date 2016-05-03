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
	print('Mnemosyne reborn by /u/ITSigno')

	# verify that the config file exists
	if not os.path.exists('mnemosyne.cfg'):
		print('No config file.')
		sys.exit() #bail

	# parse the config file
	config = ConfigParser.ConfigParser();
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

	# TODO Move exclusions into confiog file
	EXCLUDE = re.compile('youtube\.com|archive\.is|web\.archive\.org')

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
	foot = "----\n\nI am Mnemosyne reborn. 418 I'm a teapot. ^^^/r/botsrights"

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

					url = get_archive_url(SUBMIT_URL,p.url)
					
					if not url:
						log("Failed to archive: " + p.permalink + "\nurl: " + url, file="failed.txt")
						continue #failed to get url

					# use the right head based on post type
					head = d_head if p.is_self else p_head

					c = head + "* **Archive:** " + url + "\n\n" + foot
					p.add_comment(c)
					# done
						
			sleep(SLEEP_TIME)
		except Exception as e:
			log(traceback.format_exc() + "\n" + 'ERROR: ' + str(e) + "\n", file="error_log.txt")
			sleep(SLEEP_TIME)
			continue
			

def log(message, **kwargs):
	logfile = kwargs.get('file', 'error_log.txt')
	now = datetime.datetime.now()
	with open(logfile, 'a') as f:
		f.write(now.strftime("%m-%d-%Y %H:%M\n"))
		f.write(str(message) + "\n")


def get_archive_url(service_url, url):
	req = requests.post(service_url, data={'url':url}, allow_redirects=False)
	loc = req.headers.get('Location')
	ref = req.headers.get('Refresh')

	archive_url = ''
	if ref:
		archive_url = re.sub('^\d+;url=','', ref)
	else:
		#failed to get fresh archive
		#fallback will use a hash if possible, query param otherwise
		f = furl(url)
		if not str(f.fragment):
			f.fragment.path = str(time.time());
		else:
			f.add({ 'ar': str(time.time())})
		
		freq = requests.post(service_url, data={'url':f.url}, allow_redirects=False)
		fref = freq.headers.get('refresh')
		floc = freq.headers.get('location')

		if fref:
			archive_url = re.sub('^\d+;url=','', fref)
		elif floc:
			archive_url = floc

		#anything else is a failure
	
	return archive_url
			
main()
