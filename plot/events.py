from django_socketio import events
from views import *

@events.on_connect
def startup(request, socket, context):
	print "Starting up"
	print socket
	return socket


@events.on_message
def message(request, socket, context, message):
	if message["action"] == "send":
		 print "Message received"
		 formatData(request)
	else:
		print "Received something."
