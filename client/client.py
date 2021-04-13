import socket
import threading
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DC_MSG = "!DISCONNECT"
SERVER = "192.168.1.65"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
erase = '\x1b[1A\x1b[K'


def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)


def recvThread():
    try:
        while True:
            msg_len = client.recv(HEADER).decode(FORMAT)
            if msg_len:
                msg_len = int(msg_len)
                msg = client.recv(msg_len).decode(FORMAT)
                print(f"\n{erase}{msg}\n[{uname}]: ", end="")
    except Exception as e:
        return e


try:
    uname = input("Enter a username: ")
    send(uname)
    RECVTHREAD = threading.Thread(target=recvThread)
    RECVTHREAD.start()
    while True:
        msg = input(f"[{uname}]: ")
        send(msg)
        print("\x1b[A\x1b[K", end="")
        if msg == DC_MSG:
            break

finally:
    send(DC_MSG)
    time.sleep(0.5)
    client.close()
    print("\ngoodbye")
    exit()
