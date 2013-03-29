#!/usr/bin/python

import websocket, json, math, time

w=12
h=12

screen = [0xff]*(w*h*3)

ws = websocket.create_connection("ws://localhost:1024")
cnt = 0

#font_lines = open("ff.txt").readlines()

def put_pixel(x, y, c):
	global screen
	idx = (y*w)+x
	idx = idx*3

	screen[idx+0] = c[0]
	screen[idx+1] = c[1]
	screen[idx+2] = c[2]

def render_str(s):
	global font_lines
	lut=list(" !\"#\$%&'()*+,-/0123456789:;<=>?ABCDEFGHIJKLMNOPQRSTUVWXYZ")

	out=[""]*5

	for c in list(s):
		c=lut.index(c)
		c=c-0

		for i in xrange(5):
			out[i] += font_lines[(c*5)+i].strip("\n") + " "

	return out

#scrollie = render_str("   CYSO MANAGED HOSTING WOOT WOOT !!! THIS IS A TEST FOR A SCROLLING TEXT! I HOPE IT WORKS!! ")
spos=0
while True:
	for y in xrange(h):
		for x in xrange(w):
			r = (((cnt + (y*10)) + (x*10)) % 360) * (math.pi/180)
			v = int(abs(math.sin(r))*255)

			r = (((cnt - (y*10) - (x*10)) % 360) * (math.pi/180))
			v2 = int(abs(math.cos(r))*255)

			r = (((cnt + (x^y)) % 360) * (math.pi/180))
			v3 = int(abs(math.cos(r))*255)

			idx = (y*w)+x
			idx = idx*3

			screen[idx+0] = (255-v2)&0xff
			screen[idx+1] = ((v+v2)>>1)&0xff
			screen[idx+2] = (v3)&0xff


	r = ((cnt) % 360) * (math.pi/180)
	v = int(abs(math.cos(r))*3)
	#for i in xrange(12):
	#	for yy in xrange(5):
	#		if scrollie[yy][(i+spos) % len(scrollie[yy]) ] == "*":
	#			yy=yy
	#			put_pixel(i, yy+2, [0,0,0])

	msg = {
		'action' : 'set_pixels', 
		'x' : 0, 
		'y' : 0, 
		'pixels' : screen
	}

	ws.send(json.dumps(msg))

	cnt = cnt+2
	if cnt%16 == 0:
		spos=spos+1
	time.sleep(0.01)

ws.close()
