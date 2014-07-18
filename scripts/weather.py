from ScriptBase import ScriptBase
from google.appengine.api import urlfetch

import logging
import urllib
import json
import random

class Weather(ScriptBase):

	def respond(self, input="test", cache=[]):
		# loc_str = cmd[len('weather '):]
		logging.info("!Weather requested for: %s", input)

		loc_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s" % urllib.quote_plus(input)

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

		self.send("It's currently %s and %s" % (weather_desc, weather_temp))

	def trigger(self):
		return r"^weather"


if __name__ == '__main__':
	d = Debug()
	d.respond()