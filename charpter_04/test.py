import time

clients = {}
client = {}

client['a'] = 'a'
client['b'] = time.time()
clients['0'] = client

client = {}
client['a'] = 'a'
client['b'] = time.time()
clients['1'] = client

print client

for key,value in client.iteritems():
	print key
	print value