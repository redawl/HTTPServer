import socket

def test_outside_dir(client):
	client.send(b"GET /../README.md HTTP/1.1\r\n")
	assert(client.recv(4096) == b'HTTP/1.1 403 Forbidden'), "Client gained access to private info!"
	client.detach()
	client = socket.socket()
	client.connect(("HOST", 6789))
	client.send(b"GET /www/ww/../w/../../../README.md HTTP/1.1\r\n")
	assert(client.recv(4096) == b'HTTP/1.1 403 Forbidden'), "Client gained access to private info!"

def this_file_doesnt_exist(client)
client = socket.socket()
client.connect(("HOST", 6789))
test_outside_dir(client)
