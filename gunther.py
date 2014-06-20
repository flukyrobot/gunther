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
        elif memcache.get('last_request'):
            logging.info("too many requests too fast")
        else:
            payload_obj = {
                "channel": "#general",
                "username": "gunther",
                "text": "I dont know that one."
                # "icon_url": "http://www.guntherfans.com/pictures/full/gunther1.jpg",
                # "text": "I touch my tralala."
            }
            if len(text) > 9:
                cmd = text[8:].strip()
                memcache.add('last_request', cmd, 3)

                logging.info("command is: %s" % cmd)
                if re.search('^what do you do', cmd, re.IGNORECASE):
                    
                    payload_obj["text"] = "I touch my tralala."

                    

                elif re.search("^weather", cmd, re.IGNORECASE):
                    loc_str = cmd[len('weather '):]
                    logging.info("!Weather requested for: %s", loc_str)

                    loc_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s" % urllib.quote_plus(loc_str)

                    logging.info("loc_url: %s" % loc_url)

                    result = urlfetch.fetch(loc_url, method=urlfetch.GET)
                    # logging.info("weather result: %s" % result.content)
                    json_data = json.loads(result.content)
                    location = json_data["results"][0]["geometry"]["location"]
                    logging.info("location: %s" % location)

                    weather_url = "http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&mode=json" % (str(location["lat"]).split('.')[0], str(location["lng"]).split('.')[0])
                    weather_result = urlfetch.fetch(weather_url, method=urlfetch.GET)
                    weather_json = json.loads(weather_result.content)
                    weather_desc = weather_json["weather"][0]["description"]
                    weather_temp = ((weather_json["main"]["temp"]-273.15)*1.8)+32

                    logging.info("%s %s"% (weather_desc,weather_temp))

                    payload_obj["text"] = "It's currently %s and %s" % (weather_desc, weather_temp)

                elif re.search("^find me a ", cmd, re.IGNORECASE):
                    q = urllib.quote_plus(cmd[len('find me a'):].strip())
                    logging.info("Find request: %s" % q)

                    image_search_url = "https://ajax.googleapis.com/ajax/services/search/images?safe=active&v=1.0&q=%s&rsz=8" % q

                    result = urlfetch.fetch(image_search_url, method=urlfetch.GET)
                    json_data = json.loads(result.content)

                    results = json_data["responseData"]["results"]
                    idx = random.randrange(0, len(results), 2)

                    first_image = results[idx]["url"]
                    logging.info("first_image: %s" % first_image)

                    payload_obj["text"] = first_image


                else:
                    logging.info("no matching commands")
                
                form_data = json.dumps(payload_obj)
                webhook_url = "https://nsdt.slack.com/services/hooks/incoming-webhook?token=HVp85OD7f1gJzZh0xxqIsvDH"
                result = urlfetch.fetch(url=webhook_url,
                    payload=form_data,
                    method=urlfetch.POST,
                    headers={'Content-Type': 'applicaton/json'})

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
