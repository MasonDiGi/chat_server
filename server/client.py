import socket
from vars import FORMAT, HEADER, DC_MSG

class Client:
	def __init__(self, conn, addr):
		self.conn = conn
		self.addr = addr

	def send(self, msg):
		message = msg.encode(FORMAT)
		msg_len = len(message)
		send_len = str(msg_len).encode(FORMAT)
		send_len += b' ' * (HEADER - len(send_len))
		self.conn.send(send_len)
		self.conn.send(message)