from ScriptBase import ScriptBase
from google.appengine.api import urlfetch

import logging
import urllib
import json
import random

class Image(ScriptBase):

	def respond(self, input="test", cache=[]):
		logging.info('matched image search')
		q = urllib.quote_plus(input[len(self.trigger()):].strip())
		logging.info("Find request: %s" % q)

		image_search_url = "https://ajax.googleapis.com/ajax/services/search/images?safe=active&v=1.0&q=%s&rsz=8" % q

		result = urlfetch.fetch(image_search_url, method=urlfetch.GET)
		json_data = json.loads(result.content)

		results = json_data["responseData"]["results"]
		idx = random.randrange(0, len(results), 2)

		first_image = results[idx]["url"]
		logging.info("first_image: %s" % first_image)

		self.send(first_image)

	def trigger(self):
		return r"^image"


if __name__ == '__main__':
	d = Debug()
	d.respond()