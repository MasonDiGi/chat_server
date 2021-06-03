from flask import Flask, request, jsonify
from client import Client
import serverConn as sc
import atexit
from flask_cors import CORS
import random


# Create a flask app for serving API routes
# Add CORS bc web development sucks
app = Flask(__name__)
CORS(app)


# Run this when the server exits to leave gracefully
def onExit(serverC):
	serverC.dc()
	for client in clients:
		client.close()


# Just the root route (should never be used)
@app.route("/")
def home():
	return "Hello"


# To get all messages from the server
@app.route("/getmessages")
def getMessages():
	msgs = serverConn.getMessages()
	return jsonify(msgs)


# To send a message (needs a client ID)
@app.route("/sendmessage", methods=["POST"])
def sendMessage():
	# Get the POST params in x-www-form-urlencoded format
	req = request.form
	msgs = serverConn.getMessages()
	origLen = len(msgs)
	# Try to get the id and handle if it is incorrect
	try:
		clientId = int(req["id"])
	except ValueError:
		return "Not a valid ID"
	except KeyError:
		return "No ID specified"
	if clientId not in clients:
		return "That ID does not exist"
	if req["msg"] is None:
		return "no message provided"
	# Send the message, wait until it has been send and received by the API, and then return the new msgs list
	clients[clientId].send(req["msg"])
	while origLen == len(msgs):
		msgs = serverConn.getMessages()
	return jsonify(serverConn.getMessages())


# Sign in with a username and receive your index back to be used when sending and logging out
@app.route("/login", methods=["POST"])
def login():
	req = request.form
	index = random.randint(1000, 9999)
	while index in clients:
		index = random.randint(1000, 9999)
	client = Client(req["name"], index)
	clients[index] = client
	return str(index)


# Gracefully log out from API and disconnect from server
@app.route("/logout", methods=["POST"])
def logout():
	req = request.form
	index = int(req['id'])
	if index not in clients:
		return "Not a valid ID"
	clients[index].close()
	clients.pop(index)
	return "Done!"


# Set up vars and connection to server
clients = {}
serverConn = sc.ServerConn()
atexit.register(onExit, serverConn)
