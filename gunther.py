# from google.appengine.api import users
# from google.appengine.ext import ndb

import webapp2
import logging

from google.appengine.api import urlfetch

import urllib
import json
import cgi
import re

# class Event(ndb.Model):
# 	author = ndb.UserProperty()
# 	start = ndb.DateTimePropert()
# 	end = ndb.DateTimeProperty()

# class EventAncestors(ndb.Model):
# 	ancestors = ndb.StringListProperty()
	

class TestMessage(webapp2.RequestHandler):
    def get(self):

        payload_obj = {
            "channel": "#general",
            "username": "gunther",
            "text": "I am not useful."
        }

        form_data = json.dumps(payload_obj)
        # print "form data: %s" % form_data
        # logging.info("Preparing")

        webhook_url = "https://nsdt.slack.com/services/hooks/incoming-webhook?token=HVp85OD7f1gJzZh0xxqIsvDH"
        result = urlfetch.fetch(url=webhook_url,
            payload=form_data,
            method=urlfetch.POST,
            headers={'Content-Type': 'applicaton/json'})



        # logging.info("response: %s" % result.status_code)

        # Checks for active Google account session
        # user = users.get_current_user()

        # if user:
        #     self.response.headers['Content-Type'] = 'text/plain'
        #     self.response.write('Hello, ' + user.nickname())
        # else:
        #     self.redirect(users.create_login_url(self.request.uri))
    def post(self):
        usr = self.request.get('user_name')
        text = self.request.get('text')
        logging.info("Got request from %s" % usr)
        logging.info("body: %s" % text)
        logging.info(usr)

        if usr.lower().startswith("slackbot"):
            logging.info("cant answer self")
        else:
            if len(text) > 9:
                cmd = text[9:]
                logging.info("command is: %s" % cmd)
                if re.search('^what do you do', cmd, re.IGNORECASE):
                    payload_obj = {
                        "channel": "#general",
                        "username": "gunther",
                        # "icon_url": "http://www.guntherfans.com/pictures/full/gunther1.jpg",
                        "text": "I touch my tralala."
                    }

                    form_data = json.dumps(payload_obj)
                    logging.info("Sending request: %s" % form_data)

                    webhook_url = "https://nsdt.slack.com/services/hooks/incoming-webhook?token=HVp85OD7f1gJzZh0xxqIsvDH"
                    result = urlfetch.fetch(url=webhook_url,
                        payload=form_data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'applicaton/json'})


                else:
                    logging.info("no matching commands")
            else:
                logging.info("Command invalid")

        # echo = cgi.escape(self.request.get('text'))
        # logging.info("Prepaing to send %s" % echo)


        # payload_obj = {
        #     "channel": "#general",
        #     "username": "gunther",
        #     "text": echo
        # }

        # form_data = json.dumps(payload_obj)
        # # print "form data: %s" % form_data
        # # logging.info("Preparing")

        # webhook_url = "https://nsdt.slack.com/services/hooks/incoming-webhook?token=LKeCkWUSqbq85AKc1MjtAIq0"
        # result = urlfetch.fetch(url=webhook_url,
        #     payload=form_data,
        #     method=urlfetch.POST,
        #     headers={'Content-Type': 'applicaton/json'})

application = webapp2.WSGIApplication([
    ('/', TestMessage),
], debug=True)