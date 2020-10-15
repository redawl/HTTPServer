import socket
dictionary = {
	b'cat': "an animal with ears",
	b'lizard': " an animal without ears"
}
sock = socket.create_server(('192.168.0.16', 6789))
sock.listen()
conn = sock.accept()[0]
conn.send(b'Hello Eli\r\n')
reply = b'none'
while(reply != b'q'):
	conn.send(b'Look up word: ')
	reply = conn.recv(4096)
	try:
		word = dictionary[reply]
		conn.send(str.encode(word) + b"\r\n")
	except:
		if(reply != b'q'):
			conn.send(b"ERROR word not found\r\n")
	conn.recv(4096)
conn.close()
