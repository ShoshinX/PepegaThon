class Contract(object):
	def __str__(self):
		return "Contract " + self.index + " - " + self.data + "\n"

	def __init__(self, index, timestamp, source, destination, provider, payload, amount):
		self.index = index
		self.timestamp = timestamp
		self.source = source
		self.destination = destination
		self.provider = provider
		self.payload = payload
		self.amount = amount
		self.status = False

	def serialize(self):
		rep = {}
		rep['index'] = self.index
		rep['timestamp'] = self.timestamp
		rep['source'] = self.source
		rep['destination'] = self.destination
		rep['provider'] = self.provider
		rep['payload'] = self.payload
		rep['amount'] = self.amount
		rep['status'] = self.status

		return rep
