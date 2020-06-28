import socket
import threading
from client import Client
from vars import *

clients = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def broadcast(msg):
	for client in clients:
		print(client.addr)
		client.send("Hello")

def handleRecv(client):
	print(f"[CLIENTS] {client.addr[0]} has connected")

	connected = True
	while connected:
		msg_len = client.conn.recv(HEADER).decode(FORMAT)
		if msg_len:
			msg_len = int(msg_len)
			msg = client.conn.recv(msg_len).decode(FORMAT)
			if msg == DC_MSG:
				connected = False
			else:
				print(f"[{client.addr[0]}] {msg}")
				broadcast(f"[{client.addr[0]}] {msg}")
	client.conn.close()
	clients.remove(client)
	print(f"[CLIENTS] {client.addr[0]} had disconnected")

def start():
	server.listen()
	print(f"[SERVER] Server is listening on {SERVER}")
	try:
		while True:
			conn, addr = server.accept()
			clients.append(Client(conn, addr))
			thread = threading.Thread(target=handleRecv, args=(clients[len(clients)-1],))
			thread.start()
			print(f"[SERVER] {threading.activeCount() - 1} active connections")
		server.close()
	except KeyboardInterrupt:
		server.close()
		print("[SERVER] Keyboard Interrupt detected. Exiting program.")
		exit()

print("[SERVER] Server starting up")
start()