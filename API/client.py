import socket
import time
from vars import ADDR, FORMAT, HEADER, DC_MSG


class Client:
	def __init__(self, name, index):
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.conn.connect(ADDR)
		self.name = name
		self.index = index
		self.send(self.name)

	def send(self, msg):
		message = msg.encode(FORMAT)
		msg_len = len(message)
		send_len = str(msg_len).encode(FORMAT)
		send_len += b' ' * (HEADER - len(send_len))
		self.conn.send(send_len)
		self.conn.send(message)

	def close(self):
		self.send(DC_MSG)
		time.sleep(0.5)
		self.conn.close()
