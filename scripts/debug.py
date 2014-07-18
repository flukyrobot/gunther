from ScriptBase import ScriptBase
import logging

class Debug(ScriptBase):


	def respond(self, input="test", cache=[]):
		logging.info("This is a debug")
		self.send('wat')

	def trigger(self):
		return "^debug"


if __name__ == '__main__':
	d = Debug()
	d.respond()