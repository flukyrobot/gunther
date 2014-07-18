from ScriptBase import ScriptBase
import logging

from google.appengine.ext import ndb

class DebugModel(ndb.Expando):
	pass

class Debug(ScriptBase):

	def respond(self, input="test", cache=[]):

		if input.startswith('save'):
			thing = DebugModel()
			atts = input[len('save'):].strip().split(' ')
			logging.info(atts)
			object_name = atts[0]
			thing.label = "debug"

			# thing[object_name] = " ".join(atts)
			setattr(thing, object_name, " ".join(atts))

			thing.put()

			logging.info(thing)

			# self.send("Saved debug to data base with: %s: %s" % (object_name, " ".join(atts)))
		elif input.startswith('get'):
			atts = input[len('get'):].split(' ')
			
			q = DebugModel.query(ndb.GenericProperty('label') == 'debug')

			valstr = []
			d = q.fetch()
			# logging.info("wat? %s"%d[0]._properties)
			for key,val in d[0]._properties.iteritems():
				logging.info(key + ":" + getattr(d[0], key))
				valstr.append("%s:%s"%(key,getattr(d[0], key)))

			self.send("Got db entry with values, %s" % ",".join(valstr))


		# logging.info("This is a debug")
		# self.send('wat')

	def trigger(self):
		return "^debug"


if __name__ == '__main__':
	d = Debug()
	d.respond()