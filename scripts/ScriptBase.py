import abc

class ScriptBase():
	__metaclass__ = abc.ABCMeta

	def __init__(self, bot):
		self.bot = bot

	def send(self,msg):
		self.bot.send(msg)

	@abc.abstractmethod
	def respond(self, bot):
		return

	@abc.abstractmethod
	def trigger(self):
		"""should return a regex to match"""
		return


