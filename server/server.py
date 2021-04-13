import socket
import threading
from client import Client
from vars import *

clients = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
stop_thread = False


def broadcast(msg):
	for client in clients:
		client.send(msg)


def handleRecv(client):
	global stop_thread
	print(f"[CLIENTS] {client.addr[0]} has connected")

	connected = True
	msg_len = client.conn.recv(HEADER).decode(FORMAT)
	if msg_len:
		msg_len = int(msg_len)
		msg = client.conn.recv(msg_len).decode(FORMAT)
		client.name = msg
	while connected and not stop_thread:
		msg_len = client.conn.recv(HEADER).decode(FORMAT)
		if msg_len:
			msg_len = int(msg_len)
			msg = client.conn.recv(msg_len).decode(FORMAT)
			if msg == DC_MSG:
				connected = False
			else:
				print(f"[{client.name}] {msg}")
				broadcast(f"[{client.name}]: {msg}")
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
	except KeyboardInterrupt:
		print("[SERVER] Keyboard Interrupt detected. Exiting program.")
	finally:
		global stop_thread
		stop_thread = True
		server.shutdown(socket.SHUT_RDWR)
		server.close()
		print("[SERVER] Good Night")
		exit()


print("[SERVER] Server starting up")
start()
