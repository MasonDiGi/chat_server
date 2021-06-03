# Import libraries and necessary variables/classes
import socket
import threading
from client import Client
from vars import *

# Intialize all variables needed for the server
# TODO: make these not global and as parameters
clients = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
stop_thread = False


# Send a message to all clients
def broadcast(msg):
	for client in clients:
		client.send(msg)


# A separate thread to receive and handle messages for a specific client
def handleRecv(client):
	global stop_thread

	connected = True
	# Handle the intial message (defines client's name)
	msg_len = client.conn.recv(HEADER).decode(FORMAT)
	if msg_len:
		# Once header is accepted, take the next msg_len bytes and use that as name
		msg_len = int(msg_len)
		msg = client.conn.recv(msg_len).decode(FORMAT)
		client.name = msg
	print(f"[CLIENTS] {client.name} has connected")
	# Keep receiving messages and broadcasting them until the client disconnects
	while connected and not stop_thread:
		msg_len = client.conn.recv(HEADER).decode(FORMAT)
		if msg_len:
			msg_len = int(msg_len)
			msg = client.conn.recv(msg_len).decode(FORMAT)
			if msg == DC_MSG:
				connected = False
			else:
				print(f"[{client.name}]: {msg}")
				broadcast(f"[{client.name}]: {msg}")
	# Once the client disconnects, gracefully remove any trace of their existence
	client.conn.close()
	clients.remove(client)
	print(f"[CLIENTS] {client.name} has disconnected")


# Start running the server
def start():
	# Open up the port
	server.listen()
	print(f"[SERVER] Server is listening on {SERVER}")
	try:
		# While the server is running, handle all new clients and give them a receive thread
		while True:
			conn, addr = server.accept()
			clients.append(Client(conn, addr))
			thread = threading.Thread(target=handleRecv, args=(clients[len(clients)-1],))
			thread.start()
			print(f"[SERVER] {threading.activeCount() - 1} active connections")
	except KeyboardInterrupt:
		print("[SERVER] Keyboard Interrupt detected. Exiting program.")
	finally:
		# Close everything down gracefully (hopefully)
		global stop_thread
		stop_thread = True
		server.detach()
		server.shutdown(socket.SHUT_RDWR)
		server.close()
		print("[SERVER] Good Night")
		exit()


# If this file is being run
if __name__ == "__main__":
	print("[SERVER] Server starting up")
	start()
