from flask import Flask, request, jsonify
from client import Client
import serverConn as sc

app = Flask(__name__)
clients = []
serverConn = sc.ServerConn()


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
	req = request.json
	index = req['index']
	clients[index].close()
	clients.pop(index)
	print(clients)
	return "Done!"


try:
	app.run(host="localhost", port=5000, debug=True)
finally:
	serverConn = sc.ServerConn()
	serverConn.dc()
	for client in clients:
		client.close()
		exit()
