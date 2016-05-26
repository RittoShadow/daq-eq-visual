import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import sys

port = 5000
s = socket.socket()
host = 'localhost'
s.bind((host, port))
s.listen(5)

class WSHandler(tornado.websocket.WebSocketHandler):
  clients = []
  def check_origin(self, origin):
    return True

  def open(self):
    self.clients.append(self)
    print 'user is connected.\n' + str(self)
    while True:
        conn, addr = s.accept()
        while True:
            data = conn.recv(256)
            if data:
                data = data.splitlines()
                for d in data:
                    self.write_message(d)
            else:
                break

  def on_message(self, message):
    print 'received message: %s\n' %message
    self.write_message(message + ' OK')

  def on_close(self):
    print 'connection closed\n'

application = tornado.web.Application([(r'/ws', WSHandler),])

if __name__ == "__main__":
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(7000)
  tornado.ioloop.IOLoop.instance().start()
