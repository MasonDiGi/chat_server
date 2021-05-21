import threading
from client import Client

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DC_MSG = "!DISCONNECT"
SERVER = "192.168.1.65"
ADDR = (SERVER, PORT)


class ServerConn:
	def __init__(self):
		self.client = Client("SERVER", -1)
		self.conn = self.client.conn
		recv = threading.Thread(target=self.recvThread)
		recv.start()
		self.msgs = []

	def recvThread(self):
		try:
			while True:
				msg_len = self.conn.recv(HEADER).decode(FORMAT)
				if msg_len:
					msg_len = int(msg_len)
					msg = self.conn.recv(msg_len).decode(FORMAT)
					self.msgs.append(msg)
		except Exception as e:
			return e

	def getMessages(self):
		return self.msgs

	def dc(self):
		self.client.close()
