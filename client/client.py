import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DC_MSG = "!DISCONNECT"
SERVER = "localhost"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
	message = msg.encode(FORMAT)
	msg_len = len(message)
	send_len = str(msg_len).encode(FORMAT)
	send_len += b' ' * (HEADER - len(send_len))
	client.send(send_len)
	client.send(message)


def recvThread():
	print("Receiving")
	while True:
		msg_len = client.recv(HEADER).decode(FORMAT) 
		if msg_len:
			msg_len = int(msg_len)
			msg = client.recv(msg_len).decode(FORMAT)
		else:
			print(f"\n[{ADDR[0]}] {msg}")


try:
	uname = input("Enter a username: ")
	RECVTHREAD = threading.Thread(target=recvThread)
	RECVTHREAD.start()
	while True:
		msg = input(f"[{uname}]: ")
		send(msg)
		if msg == DC_MSG:
			break

finally:
	send(DC_MSG)
	client.close()
	print("\ngoodbye")
	exit()