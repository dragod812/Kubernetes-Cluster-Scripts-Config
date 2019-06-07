from pyignite import Client
import os

class Database:
	def __init__(self, url='127.0.0.1', port=10800) :
		if ("IGNITE_CLUSTER_IP" in os.environ):
			url = os.environ["IGNITE_CLUSTER_IP"]
		if ("IGNITE_CLUSTER_PORT" in os.environ):
			port = int(os.environ["IGNITE_CLUSTER_PORT"])
		print(url, port)
		self.client = Client()
		self.client.connect(url, port)

	def getClient(self) :
		return self.client
	def closeClient(self, client) :
		client.close()
