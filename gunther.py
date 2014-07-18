# from google.appengine.api import users
# from google.appengine.ext import ndb

import webapp2
import logging

from google.appengine.api import urlfetch
from google.appengine.api import memcache

import urllib
import json
import cgi
import re

import random

from scripts import debug, image, weather


class Gunther():

    def __init__(self, request):
        self.request = request

        self.payload_obj = {
            "channel": "#general",
            "username": "gunther",
            "text": "I dont know that one."
            # "icon_url": "http://www.guntherfans.com/pictures/full/gunther1.jpg",
            # "text": "I touch my tralala."
        }

    def send(self, msg='send'):
        self.payload_obj["text"] = msg;
        self.payload_obj["channel"] = self.request.get('channel')
        form_data = json.dumps(self.payload_obj)
        webhook_url = "https://nsdt.slack.com/services/hooks/incoming-webhook?token=AxfgsYiyFAJPVMzwJEPtD4T4"
        result = urlfetch.fetch(url=webhook_url,
            payload=form_data,
            method=urlfetch.POST,
            headers={'Content-Type': 'applicaton/json'})




# for script in scripts:
#     logging.info(script(Gunther).trigger())
	

class GuntherResponder(webapp2.RequestHandler):

    scripts = [debug.Debug, image.Image, weather.Weather]

    
    def post(self):
        usr = self.request.get('user_name')
        logging.info(usr)
        text = self.request.get('text')
        logging.info(text)

        if usr.lower().startswith("slackbot"):
            logging.info("cant answer self")
        elif memcache.get('last_request'):
            logging.info("too many requests too fast")
        elif len(text) > 9:
            cmd = text[8:].strip()
            memcache.add('last_request', cmd, 3)
            gunther = Gunther(self.request)
            for script in GuntherResponder.scripts:
                s = script(gunther)
                logging.info(s.trigger())
                if re.search(s.trigger(), cmd, re.IGNORECASE):
                    s.respond(cmd[len(s.trigger()):])       
        

application = webapp2.WSGIApplication([
    ('/', GuntherResponder),
], debug=True)
