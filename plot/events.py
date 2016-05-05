from django_socketio import events
from views import *

@events.on_connect
def startup(request, socket, context):
    


 @events.on_message
 def message(request, socket, context, message):
     if message["action"] == "send":
         formatData(request)
