#!/usr/bin/env python

"""
Insert custom messages into HP printer displays

Works for most network-enabled HP printers.
"""

import socket
import sys
import random
import os.path

# Default configuration
host = 'hp4700'
port = 9100 #9100 is the default JetDirect port.

import random

def random_line(filename):
	"Retrieve a  random line from a file, reading through the file once"
	source = open(filename, "r")
	line_number = 0
	result = ''

	while 1:
		textline = source.readline()
		line_number += 1
		if textline != "":
			#
			# How likely is it that this is the last line of the file ? 
			if random.uniform(0, line_number) < 1:
				result = textline
		else:
			break

	source.close()

	return result

sock = socket.socket()
try:
    sock.connect((host, port))
except socket.error, e:
    sys.exit('Connection error %s: %s.' % (e[0], e[1]))

print 'Connected'

message = random_line(os.path.join(os.path.dirname(__file__), 'messages.txt')).replace("\r\n", '').replace("\n", '')
print 'Setting ready message to "%s" on %s' % (message, host)
command = "\x1B%%-12345X@PJL RDYMSG DISPLAY = \"%s\"\r\n\x1B%%-12345X\r\n" % message
sock.sendall(command)

