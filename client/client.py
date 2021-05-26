import socket
import threading
import time

# Create constants
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DC_MSG = "!DISCONNECT"
SERVER = "localhost"
ADDR = (SERVER, PORT)

# Set up client var and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
erase = '\x1b[1A\x1b[K'


# Handles sending a message to the server
def send(sendMsg):
    # Encode and create header
    message = sendMsg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    # Send the actual text
    client.send(message)


# A thread to handle receiving messages broadcast from the server
def recvThread():
    try:
        # Wait for a message from the server and then decode and print it, while keeping the prompt on the same line
        while True:
            msg_len = client.recv(HEADER).decode(FORMAT)
            if msg_len:
                msg_len = int(msg_len)
                recvMsg = client.recv(msg_len).decode(FORMAT)
                print(f"\n{erase}{recvMsg}\n[{uname}]: ", end="")
    except Exception as e:
        return e


# Main thread
try:
    # Send initial message to set up username
    uname = input("Enter a username: ")
    send(uname)
    # Start handling received messages
    RECVTHREAD = threading.Thread(target=recvThread)
    RECVTHREAD.start()
    # Handle the prompt and sending messages
    while True:
        msg = input(f"[{uname}]: ")
        send(msg)
        print("\x1b[A\x1b[K", end="")
        if msg == DC_MSG:
            break

# Close everything if ctrl+c is pressed
finally:
    send(DC_MSG)
    time.sleep(0.5)
    client.close()
    print("\ngoodbye")
    exit()
