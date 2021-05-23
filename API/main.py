from flask import Flask, request, jsonify
from client import Client
import serverConn as sc
import atexit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def onExit(serverC):
	serverC.dc()
	for client in clients:
		client.close()


@app.route("/")
def home():
	return "Hello"


@app.route("/getmessages")
def getMessages():
	msgs = serverConn.getMessages()
	return jsonify(msgs)


@app.route("/sendmessage", methods=["POST"])
def sendMessage():
	req = request.form
	msgs = serverConn.getMessages()
	origLen = len(msgs)
	try:
		clientId = int(req["id"])
	except ValueError:
		return "Not a valid ID"
	except KeyError:
		return "No ID specified"
	if clientId >= len(clients):
		return "That ID does not exist"
	if req["msg"] is None:
		return "no message provided"
	clients[clientId].send(req["msg"])
	while origLen == len(msgs):
		msgs = serverConn.getMessages()
	return jsonify(serverConn.getMessages())


@app.route("/login", methods=["POST"])
def login():
	req = request.form
	index = len(clients)
	client = Client(req["name"], index)
	clients.append(client)
	return str(index)


@app.route("/logout", methods=["POST"])
def logout():
	req = request.form
	index = int(req['id'])
	if index >= len(clients) or index < 0:
		return "Not a valid ID"
	clients[index].close()
	clients.pop(index)
	return "Done!"


clients = []
serverConn = sc.ServerConn()
atexit.register(onExit, serverConn)
