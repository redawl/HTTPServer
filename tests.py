import socket
from server_functions import read_config

def test_outside_dir(client, host, port):
	client.send(b"GET /../README.md HTTP/1.1\r\n")
	assert(client.recv(4096) == b'HTTP/1.1 403 Forbidden'), "Client gained access to private info!"
	client.detach()
	client = socket.socket()
	client.connect((host, port))
	client.send(b"GET /www/ww/../w/../../../README.md HTTP/1.1\r\n")
	assert(client.recv(4096) == b'HTTP/1.1 403 Forbidden'), "Client gained access to private info!"

def this_file_doesnt_exist(client):
	assert("" == ""), "Empty for now"


client = socket.socket()
config = read_config()
host = config[0]
port = int(config[1])
client.connect((host, port))
test_outside_dir(client, host, port)
