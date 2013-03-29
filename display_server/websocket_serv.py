from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler

import json

w=12
h=12

screen = [0]*(w*h*3)

class Handler(WebSocketHandler):
	def open(self):
		print "New connection opened."

	def on_message(self, message):
		global screen
		message = json.loads(message)
		#print message

		if message['action'] == "get_screen":
			self.write_message(json.dumps(screen))

		elif message['action'] == "set_pixel":
			idx = (message['y']*w)+message['x'];
			idx = idx*3;

			screen[ idx+0 ] = message['r']
			screen[ idx+1 ] = message['g']
			screen[ idx+2 ] = message['b']

		elif message['action'] == "set_pixels":
			idx = (message['y']*w)+message['x'];
			idx = idx*3;

			n=0

			for pixel in message['pixels']:
				screen[ idx+n ] = pixel
				n=n+1

	def on_close(self):
		print "Connection closed."

print "Server started."
HTTPServer(Application([("/", Handler)])).listen(1024)
IOLoop.instance().start()
