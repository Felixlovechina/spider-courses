import socket
import sys


sock = socket.create_connection(('localhost', 20012))

sock.send('Client Request')

data = sock.recv(1024)
print 'data received: ' + data

sock.close()