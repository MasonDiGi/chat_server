# Import some variables needed for sending
from vars import FORMAT, HEADER


# A class to allow the server to handle the separate clients connected to it
class Client:
	# Initialize attributes for the client
	def __init__(self, conn, addr):
		# the conn object from socket
		self.conn = conn
		# IP address of the client
		self.addr = addr

	# Send a message to the client
	def send(self, msg):
		# Encoding to utf-8 for ease of sending over network
		message = msg.encode(FORMAT)
		# Add len of the message to create a message header
		msg_len = len(message)
		send_len = str(msg_len).encode(FORMAT)
		send_len += b' ' * (HEADER - len(send_len))
		# Send the header and then the message
		self.conn.send(send_len)
		self.conn.send(message)
