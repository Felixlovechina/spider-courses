import socket
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 20012))
sock.listen(5)
conn, addr = sock.accept()

try:
	while True:
		print 'blocking receive'
		conn.recv(16)
		print 'send OK'
		conn.sendall('OK')
except socket.error as msg:
	print 'Error Code: %d, Message is %s'%(msg[0], msg[1])
conn.close()
sock.close()