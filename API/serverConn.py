import threading
from client import Client

from vars import HEADER, FORMAT


# A wrapper class for a client that represents the main client of the API
# (mainly for handling receiving messages)
class ServerConn:
    # Set up client connection and receive thread, as well as list to hold all the messages
    def __init__(self):
        self.client = Client("SERVER", -1)
        self.conn = self.client.conn
        recv = threading.Thread(target=self.recvThread)
        recv.start()
        self.msgs = []

    # A thread to receive all messages from the server and store them in the object
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

    # Getter for messages
    def getMessages(self):
        return self.msgs

    # Disconnect from server
    def dc(self):
        self.client.close()
